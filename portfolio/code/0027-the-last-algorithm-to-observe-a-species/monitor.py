#!/usr/bin/env python3
"""
Automated Species Monitor — Moresby Mangrove Conservation Programme

CLI tool for analysing passive sensor data from the Moresby Island
monitoring array. Processes acoustic and camera-trap logs, estimates
population metrics, and produces formatted survey reports.

As detections decline, output contracts. When silence is sustained,
a formal declaration is issued.

Usage:
    python monitor.py <habitat_directory> [options]

Options:
    --summary       Print only aggregate statistics, not daily reports
    --from DAY      Begin analysis at specified monitoring day (default: 1)
    --to DAY        End analysis at specified monitoring day (default: last)
    --interactive   Enable interactive mode for zero-detection terminal
"""

import os
import sys
import glob
import re
import argparse
import time


SPECIES_NAME = "Moresby mangrove rail"
SPECIES_BINOMIAL = "Hypotaenidia moresbyi"
SURVEY_SITE = "Moresby Island Group, Papua New Guinea"

SEPARATOR_THICK = "=" * 72
SEPARATOR_THIN = "-" * 72


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_sensor_log(filepath):
    """Parse a single sensor log file into a structured record."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    record = {
        "filename": os.path.basename(filepath),
        "filepath": filepath,
        "raw_text": raw,
        "call_detections": [],
        "camera_detections": [],
        "population_estimate": None,
        "ci_lower": None,
        "ci_upper": None,
        "total_detections": 0,
        "date": None,
        "day_number": None,
    }

    m = re.search(r"Day of Monitoring:\s*(\d+)", raw)
    if m:
        record["day_number"] = int(m.group(1))

    m = re.search(r"Survey Date:\s*(.+)", raw)
    if m:
        record["date"] = m.group(1).strip()

    for m in re.finditer(
        r"CALL DETECTED \| (.+?) \| duration=(\d+)ms "
        r"\| freq=([\d.]+)Hz \| confidence=([\d.]+) "
        r"\| classified=(\w+)",
        raw,
    ):
        record["call_detections"].append({
            "time": m.group(1).strip(),
            "duration_ms": int(m.group(2)),
            "frequency_hz": float(m.group(3)),
            "confidence": float(m.group(4)),
            "classified": m.group(5),
        })

    for m in re.finditer(
        r"IMAGE CAPTURED \| (.+?) \| station=(\S+) "
        r"\| subject=(\S+) \| confidence=([\d.]+) "
        r"\| tagged=(\w+)",
        raw,
    ):
        record["camera_detections"].append({
            "time": m.group(1).strip(),
            "station": m.group(2),
            "subject": m.group(3),
            "confidence": float(m.group(4)),
            "tagged": m.group(5),
        })

    m = re.search(
        r"Population Estimate\s*:\s*(\d+)\s*\[CI:\s*(\d+)-(\d+)\]",
        raw,
    )
    if m:
        record["population_estimate"] = int(m.group(1))
        record["ci_lower"] = int(m.group(2))
        record["ci_upper"] = int(m.group(3))

    record["total_detections"] = (
        len(record["call_detections"]) + len(record["camera_detections"])
    )

    return record


def load_habitat(habitat_dir, day_from=None, day_to=None):
    """Load and parse all sensor logs from a habitat directory."""
    pattern = os.path.join(habitat_dir, "sensor_log_*.txt")
    files = sorted(glob.glob(pattern))

    if not files:
        print(
            f"ERROR: No sensor log files found in {habitat_dir}",
            file=sys.stderr,
        )
        print(
            "Run 'python habitat.py' to generate sample data.",
            file=sys.stderr,
        )
        sys.exit(1)

    records = []
    for fp in files:
        rec = parse_sensor_log(fp)
        if rec["day_number"] is not None:
            records.append(rec)

    records.sort(key=lambda r: (r["day_number"] or 0))

    if day_from is not None:
        records = [r for r in records if r["day_number"] >= day_from]
    if day_to is not None:
        records = [r for r in records if r["day_number"] <= day_to]

    return records


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyse_records(records):
    """Run population analysis across a sequence of daily records."""
    total_days = len(records)
    days_with_detections = sum(
        1 for r in records if r["total_detections"] > 0
    )
    days_without = total_days - days_with_detections
    total_call = sum(len(r["call_detections"]) for r in records)
    total_camera = sum(len(r["camera_detections"]) for r in records)

    pop_estimates = [
        r["population_estimate"]
        for r in records
        if r["population_estimate"] is not None
    ]
    max_pop = max(pop_estimates) if pop_estimates else 0
    min_pop = min(pop_estimates) if pop_estimates else 0
    first_pop = pop_estimates[0] if pop_estimates else 0
    last_pop = pop_estimates[-1] if pop_estimates else 0

    all_confidences = []
    for r in records:
        for d in r["call_detections"]:
            all_confidences.append(d["confidence"])
    for r in records:
        for d in r["camera_detections"]:
            all_confidences.append(d["confidence"])

    mean_conf = (
        sum(all_confidences) / len(all_confidences)
        if all_confidences
        else 0
    )
    max_conf = max(all_confidences) if all_confidences else 0
    min_conf = min(all_confidences) if all_confidences else 0

    last_detected = None
    last_record = None
    for r in reversed(records):
        if r["total_detections"] > 0:
            last_detected = r["day_number"]
            last_record = r
            break

    consecutive_null = 0
    for r in reversed(records):
        if r["total_detections"] == 0:
            consecutive_null += 1
        else:
            break

    return {
        "total_days": total_days,
        "days_with_detections": days_with_detections,
        "days_without_detections": days_without,
        "total_call_detections": total_call,
        "total_camera_detections": total_camera,
        "max_population": max_pop,
        "min_population": min_pop,
        "first_population": first_pop,
        "last_population": last_pop,
        "mean_confidence": mean_conf,
        "max_confidence": max_conf,
        "min_confidence": min_conf,
        "total_confidence_events": len(all_confidences),
        "last_detected_day": last_detected,
        "last_detected_record": last_record,
        "consecutive_null_days": consecutive_null,
    }


# ---------------------------------------------------------------------------
# Reporting — output contracts as detections decline
# ---------------------------------------------------------------------------

def _pop_tier(pop_estimate):
    """Classify population into a display tier.

    Tiers control output verbosity:
      4 = healthy (>= 8): full detail
      3 = declining (4-7): full detail, warning
      2 = critical (1-3): reduced detail
      1 = zero (0): minimal
    """
    if pop_estimate is None:
        return 1
    if pop_estimate >= 8:
        return 4
    if pop_estimate >= 4:
        return 3
    if pop_estimate >= 1:
        return 2
    return 1


def print_daily_report(record):
    """Print a formatted daily monitoring report.

    Output verbosity contracts as the population declines.
    Healthy population: full acoustic + camera detail.
    Critical: condensed single-line detections.
    Zero: single null-result line.
    """
    day = record["day_number"]
    date = record["date"] or "UNKNOWN"
    n_calls = len(record["call_detections"])
    n_cam = len(record["camera_detections"])
    total = record["total_detections"]
    pop = record["population_estimate"]
    ci_lo = record["ci_lower"]
    ci_hi = record["ci_upper"]

    tier = _pop_tier(pop)

    # --- Tier 1: Zero detections — minimal line ---
    if tier == 1 and total == 0:
        print(
            f"  Day {day:>3d} | {date} "
            f"| Acoustic: {n_calls}  Camera: {n_cam}  "
            f"| Est: {pop} [CI: {ci_lo}-{ci_hi}] "
            f"| NO DETECTION"
        )
        return

    # --- Tier 2: Critical — condensed ---
    if tier == 2:
        print()
        print(SEPARATOR_THIN)
        print(f"  Day {day} | {date}")
        print(f"  Population Estimate: {pop} [CI: {ci_lo}-{ci_hi}]")
        print(f"  Detections: {n_calls} acoustic, {n_cam} camera")
        for d in record["call_detections"]:
            print(f"    CALL  {d['time']}  conf={d['confidence']:.3f}")
        for d in record["camera_detections"]:
            print(
                f"    IMAGE {d['time']}  station={d['station']}  "
                f"conf={d['confidence']:.3f}"
            )
        print(
            "  STATUS: CRITICAL — population below viability threshold"
        )
        print(SEPARATOR_THIN)
        return

    # --- Tier 3-4: Full report ---
    print()
    print(SEPARATOR_THICK)
    print(f"  DAILY MONITORING REPORT — {SPECIES_NAME}")
    print(f"  {SURVEY_SITE}")
    print("  Protocol: MMCR-2019-v3.2")
    print(SEPARATOR_THIN)
    print(f"  Date          : {date}")
    print(f"  Monitoring Day: {day}")
    print(SEPARATOR_THIN)
    print(f"  Acoustic Detections  : {n_calls}")
    print(f"  Camera Captures      : {n_cam}")
    print(f"  Total Detections     : {total}")
    print()

    if n_calls > 0:
        print("  ACOUSTIC ANALYSIS:")
        for d in record["call_detections"]:
            print(
                f"    {d['time']}  dur={d['duration_ms']}ms  "
                f"freq={d['frequency_hz']:.1f}Hz  "
                f"conf={d['confidence']:.3f}"
            )
        print()

    if n_cam > 0:
        print("  CAMERA TRAP ANALYSIS:")
        for d in record["camera_detections"]:
            print(
                f"    {d['time']}  station={d['station']}  "
                f"conf={d['confidence']:.3f}"
            )
        print()

    print(f"  POPULATION ESTIMATE: {pop} [95% CI: {ci_lo}-{ci_hi}]")
    print()

    if tier == 3:
        print("  STATUS: DECLINING — continued monitoring recommended")
    else:
        print("  STATUS: MONITORING CONTINUES")

    print(SEPARATOR_THICK)


def print_summary_report(analysis):
    """Print aggregate monitoring statistics."""
    print()
    print(SEPARATOR_THICK)
    print("  MONITORING SUMMARY")
    print(SEPARATOR_THICK)
    print(
        f"  Species             : {SPECIES_NAME} ({SPECIES_BINOMIAL})"
    )
    print(f"  Site                : {SURVEY_SITE}")
    print()
    print(f"  Total Days Analysed : {analysis['total_days']}")
    print(f"  Days w/ Detections  : {analysis['days_with_detections']}")
    print(
        f"  Days w/o Detections : {analysis['days_without_detections']}"
    )
    print()
    print(f"  Acoustic Detections : {analysis['total_call_detections']}")
    print(f"  Camera Captures     : {analysis['total_camera_detections']}")
    print()
    print(
        f"  Population Estimate : {analysis['first_population']} "
        f"(first) \u2192 {analysis['last_population']} (last)"
    )
    print(
        f"  Range               : {analysis['min_population']}\u2013"
        f"{analysis['max_population']}"
    )
    print()

    if analysis["total_confidence_events"] > 0:
        print(f"  Mean Confidence     : {analysis['mean_confidence']:.3f}")
        print(
            f"  Confidence Range    : {analysis['min_confidence']:.3f}\u2013"
            f"{analysis['max_confidence']:.3f}"
        )
    print()

    if analysis["last_detected_day"] is not None:
        print(
            f"  Last Confirmed Det. : Day {analysis['last_detected_day']}"
        )
        print(
            f"  Consecutive Nulls   : "
            f"{analysis['consecutive_null_days']}"
        )
    else:
        print("  Last Confirmed Det. : NONE")

    print(SEPARATOR_THICK)


def print_final_declaration(analysis):
    """Print formal declaration of sustained zero detections.

    This is the emotional centre of the tool. The declaration is
    clinical, specific, and quiet. The last confirmed observation
    is printed with full detail — including one thing no monitoring
    algorithm should record.
    """
    print()
    print(SEPARATOR_THICK)
    print()
    print("  DECLARATION — ZERO DETECTION EVENT")
    print()
    print(SEPARATOR_THIN)
    print(
        f"  Species         : {SPECIES_NAME} ({SPECIES_BINOMIAL})"
    )
    print(
        f"  Habitat         : Mangrove, 4.2 km\u00b2, {SURVEY_SITE}"
    )
    print(
        "  Detection Method: Territorial call analysis (dawn survey)"
    )
    print("  Typical Clutch  : 2-3 eggs")
    print()
    print(
        "  Consecutive survey days without target species detection: "
        f"{analysis['consecutive_null_days']}"
    )
    print()
    print(
        f"  No acoustic or camera-trap evidence of {SPECIES_NAME}"
    )
    print(
        "  has been recorded during this period. Survey effort has"
    )
    print(
        "  been maintained at full protocol specification throughout."
    )
    print()
    print(
        f"  Last confirmed detection: Day {analysis['last_detected_day']}"
    )
    print()

    rec = analysis.get("last_detected_record")
    if rec:
        print("  LAST CONFIRMED OBSERVATION:")
        print(f"  {SEPARATOR_THIN}")

        for d in rec["call_detections"]:
            print("    Source : Acoustic sensor array")
            print(f"    Time   : {d['time']}")
            print(
                f"    Signal : {d['duration_ms']}ms "
                f"at {d['frequency_hz']:.1f} Hz"
            )
            print(f"    Class. : {d['classified']}")
            print(f"    Conf.  : {d['confidence']:.3f}")
            print()
            # The impossible detail. A monitoring algorithm records
            # signal parameters and classification confidence. It does
            # not perceive aloneness. It does not notice that a call
            # went unanswered. But here, it does.
            if d["confidence"] == 1.0:
                print(
                    "    Note   : Subject was alone. "
                    "The call was not answered."
                )
                print()

        for d in rec["camera_detections"]:
            print(f"    Source : Camera trap, station {d['station']}")
            print(f"    Time   : {d['time']}")
            print(f"    Class. : {d['tagged']}")
            print(f"    Conf.  : {d['confidence']:.3f}")
            print()

    print(SEPARATOR_THICK)


def print_null_sweep(day_number):
    """Print a null-result sweep line for interactive continuation."""
    print(
        f"  [{day_number:>4d}] Survey complete. "
        f"Acoustic: 0/8460 scans. Camera: 0/12 stations. "
        f"Result: NULL"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        description=f"Automated monitoring analysis for {SPECIES_NAME}",
        epilog="Generate habitat data first with 'python habitat.py'.",
    )
    parser.add_argument(
        "habitat_dir",
        help="Directory containing sensor_log_*.txt files",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print only aggregate statistics, not daily reports",
    )
    parser.add_argument(
        "--from",
        dest="day_from",
        type=int,
        default=None,
        help="Begin analysis at specified monitoring day",
    )
    parser.add_argument(
        "--to",
        dest="day_to",
        type=int,
        default=None,
        help="End analysis at specified monitoring day",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Enable interactive mode for zero-detection terminal",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    habitat_dir = os.path.abspath(args.habitat_dir)
    if not os.path.isdir(habitat_dir):
        print(
            f"ERROR: Directory not found: {habitat_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    records = load_habitat(habitat_dir, args.day_from, args.day_to)

    if not records:
        print(
            "No sensor logs found in the specified range.",
            file=sys.stderr,
        )
        sys.exit(1)

    analysis = analyse_records(records)

    # --- Header ---
    print()
    print(SEPARATOR_THICK)
    print("  AUTOMATED WILDLIFE MONITORING SYSTEM")
    print("  Analysis Engine v2.4.1")
    print(f"  Target: {SPECIES_NAME} ({SPECIES_BINOMIAL})")
    print(f"  Site  : {SURVEY_SITE}")
    print(SEPARATOR_THICK)
    print(f"  Habitat directory : {habitat_dir}")
    print(f"  Log files loaded  : {len(records)}")
    day_min = records[0]["day_number"]
    day_max = records[-1]["day_number"]
    print(
        f"  Monitoring period : Day {day_min} through Day {day_max}"
    )
    print(SEPARATOR_THICK)

    if args.summary:
        print_summary_report(analysis)
        return

    # --- Daily reports ---
    for rec in records:
        print_daily_report(rec)

    # --- Summary ---
    print_summary_report(analysis)

    # --- Terminal interaction ---
    if analysis["consecutive_null_days"] >= 3 and args.interactive:
        print()
        print(SEPARATOR_THICK)
        print(
            f"  {analysis['consecutive_null_days']} consecutive "
            f"survey days without detection of {SPECIES_NAME}."
        )
        print(
            "  Population estimate at last detection: "
            f"{analysis['last_population']}"
        )
        print(SEPARATOR_THICK)
        print()

        try:
            response = input(
                "  Continue monitoring? [y/N]: "
            ).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            response = "n"

        if response in ("n", "no", ""):
            print_final_declaration(analysis)
            print()
            print("  Monitoring session ended.")
            print(f"  {SEPARATOR_THIN}")
        else:
            print()
            print("  Continuing monitoring. Press Ctrl+C to stop.")
            print(f"  {SEPARATOR_THIN}")
            next_day = day_max + 1
            try:
                while True:
                    print_null_sweep(next_day)
                    next_day += 1
                    time.sleep(2.0)
            except KeyboardInterrupt:
                total_nulls = (
                    analysis["consecutive_null_days"]
                    + (next_day - 1 - day_max)
                )
                print()
                print()
                print(
                    f"  Monitoring terminated by operator at "
                    f"Day {next_day - 1}."
                )
                print(
                    f"  Total consecutive null-sweep days: "
                    f"{total_nulls}"
                )
                print(SEPARATOR_THICK)

    elif analysis["consecutive_null_days"] >= 3:
        print()
        print(
            f"  NOTE: {analysis['consecutive_null_days']} consecutive "
            f"days without detection."
        )
        print(
            "  Run with --interactive for terminal monitoring options."
        )
        print()


if __name__ == "__main__":
    main()
