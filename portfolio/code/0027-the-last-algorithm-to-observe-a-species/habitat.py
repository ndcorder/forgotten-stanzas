#!/usr/bin/env python3
"""
Habitat Data Generator for the Moresby Mangrove Conservation Programme

Generates synthetic sensor log files for monitoring the Moresby mangrove rail
(Hypotaenidia moresbyi), an endemic flightless rail restricted to 4.2 km²
of mangrove habitat on the Moresby Island group, Papua New Guinea.

Detection methodology:
    - Acoustic sensor array: territorial call at dawn (05:10-06:40 AEST)
    - Camera traps: passive infrared at 12 stations
    - Survey window: 120 minutes post-sunrise

Usage:
    python habitat.py [output_directory]

If no directory is specified, creates ./habitat/ in the current working directory.
"""

import os
import random
import datetime

SPECIES_NAME = "Moresby mangrove rail"
SPECIES_BINOMIAL = "Hypotaenidia moresbyi"
SURVEY_SITE = "Moresby Island Group, Papua New Guinea"
TOTAL_DAYS = 94
LAST_CONFIRMED_DAY = 88


class PopulationModel:
    """Simulates realistic population decline with stochastic variance."""

    def __init__(self, seed=4471):
        self.rng = random.Random(seed)
        self.base_pop = 14

    def count(self, day):
        if day <= 0:
            return self.base_pop

        if day <= 48:
            t = day / 48.0
            decline = 1.0 - 0.12 * t
            noise = self.rng.gauss(0, 0.8)
            return max(0, round(self.base_pop * decline + noise))

        elif day <= 76:
            t = (day - 48) / 28.0
            base = self.base_pop * 0.88
            decline = 1.0 - 0.85 * t * t
            noise = self.rng.gauss(0, 0.6)
            return max(0, round(base * decline + noise))

        elif day <= 87:
            t = (day - 76) / 11.0
            base = self.base_pop * 0.88 * 0.15
            decline = max(0, 1.0 - 2.5 * t)
            noise = self.rng.gauss(0, 0.3)
            count = max(0, round(base * decline + noise))
            # Occasional phantom detections — false positives that
            # make the silence feel like silence, not just absence
            if self.rng.random() < 0.35 and count < 2:
                count = self.rng.choice([1, 1, 2])
            return max(0, count)

        elif day == 88:
            return 1

        else:
            return 0


def _random_time(rng, hour_min, hour_max, minute_min=0, minute_max=59):
    hour = rng.randint(hour_min, hour_max)
    if hour == hour_max:
        minute = rng.randint(minute_min, min(minute_max, 30))
    else:
        minute = rng.randint(minute_min, minute_max)
    second = rng.randint(0, 59)
    return f"{hour:02d}:{minute:02d}:{second:02d}"


def _generate_call_detections(rng, pop_count, is_last_day=False):
    detections = []
    if pop_count <= 0:
        return detections

    if is_last_day:
        time = _random_time(rng, 5, 5, 14, 22)
        dur_ms = rng.randint(1800, 2400)
        freq = round(rng.uniform(1180, 1240), 1)
        detections.append(
            f"CALL DETECTED | {time} | duration={dur_ms}ms "
            f"| freq={freq}Hz | confidence=1.000 | classified={SPECIES_BINOMIAL}"
        )
        return detections

    n_calls = rng.randint(1, max(1, min(pop_count, 4)))
    for _ in range(n_calls):
        time = _random_time(rng, 5, 6, 10, 40)
        dur_ms = rng.randint(800, 2200)
        freq = round(rng.uniform(1100, 1300), 1)
        conf = round(rng.uniform(0.42, 0.71), 3)
        detections.append(
            f"CALL DETECTED | {time} | duration={dur_ms}ms "
            f"| freq={freq}Hz | confidence={conf:.3f} "
            f"| classified={SPECIES_BINOMIAL}"
        )
    return detections


def _generate_camera_detections(rng, pop_count, is_last_day=False):
    detections = []
    if pop_count <= 0:
        return detections

    if is_last_day:
        time = _random_time(rng, 5, 5, 16, 24)
        detections.append(
            f"IMAGE CAPTURED | {time} | station=E4 "
            f"| subject=AVIAN_SMALL | confidence=1.000 "
            f"| tagged={SPECIES_BINOMIAL}"
        )
        return detections

    n_captures = rng.randint(0, max(0, min(pop_count - 1, 3)))
    stations = ["A1", "A3", "B2", "B4", "C1", "C3", "D2", "E4", "F1"]
    for _ in range(n_captures):
        time = _random_time(rng, 5, 7, 0, 30)
        station = rng.choice(stations)
        conf = round(rng.uniform(0.42, 0.71), 3)
        detections.append(
            f"IMAGE CAPTURED | {time} | station={station} "
            f"| subject=AVIAN_SMALL | confidence={conf:.3f} "
            f"| tagged={SPECIES_BINOMIAL}"
        )
    return detections


def generate_sensor_log(day, model, rng, start_date):
    date = start_date + datetime.timedelta(days=day - 1)
    date_str = date.strftime("%Y-%m-%d")
    log_date_label = date.strftime("%a %b %d %Y")

    pop_count = model.count(day)
    is_last = (day == LAST_CONFIRMED_DAY)

    lines = []
    lines.append("=" * 72)
    lines.append("AUTOMATED WILDLIFE MONITORING SYSTEM")
    lines.append(f"Station: {SURVEY_SITE}")
    lines.append(f"Survey Date: {log_date_label}")
    lines.append("Protocol: MMCR-2019-v3.2")
    lines.append(f"Target Species: {SPECIES_NAME} ({SPECIES_BINOMIAL})")
    lines.append("Detection Method: Territorial call analysis (dawn survey)")
    lines.append("Typical Clutch Size: 2-3 eggs")
    lines.append("Habitat: Mangrove, 4.2 km\u00b2")
    lines.append(f"Day of Monitoring: {day}")
    lines.append("=" * 72)
    lines.append("")

    lines.append("SYSTEM STATUS:")
    lines.append("  Battery Level    : OK [87%]")
    lines.append("  Storage Available: OK [2.4 GB]")
    lines.append("  Sensor Array     : NOMINAL [12/12 stations active]")
    lines.append("  GPS Fix          : VALID [-8.4562, 148.2341, elev 3m]")
    lines.append("")

    lines.append("-" * 72)
    lines.append("ACOUSTIC SURVEY RESULTS")
    lines.append("  Survey Window : 05:10:00 - 06:40:00 AEST")
    lines.append("  Total Scans   : 8460")
    lines.append("  Threshold SNR : 12 dB")
    lines.append("")

    call_dets = _generate_call_detections(rng, pop_count, is_last)
    lines.append(f"  Target Species Detections: {len(call_dets)}")
    lines.append("")

    if call_dets:
        lines.append("  DETAILED DETECTIONS:")
        for d in call_dets:
            lines.append(f"  {d}")
    else:
        lines.append("  DETAILED DETECTIONS:")
        lines.append("  [No target species detections recorded]")
    lines.append("")

    lines.append("-" * 72)
    lines.append("CAMERA TRAP RESULTS")
    lines.append("  Active Stations : 12")
    lines.append(f"  Trigger Events  : {rng.randint(3, 45)}")
    lines.append("")

    cam_dets = _generate_camera_detections(rng, pop_count, is_last)
    lines.append(f"  Target Species Captures: {len(cam_dets)}")
    lines.append("")

    if cam_dets:
        lines.append("  DETAILED CAPTURES:")
        for d in cam_dets:
            lines.append(f"  {d}")
    else:
        lines.append("  DETAILED CAPTURES:")
        lines.append("  [No target species captures recorded]")
    lines.append("")

    total = len(call_dets) + len(cam_dets)
    lines.append("-" * 72)
    lines.append("SUMMARY")
    lines.append(f"  Target Detections (Total): {total}")
    lines.append(
        f"  Population Estimate       : {pop_count} "
        f"[CI: {max(0, pop_count - 3)}-{pop_count + 2}]"
    )
    lines.append(
        f"  Survey Effort             : COMPLETE "
        f"[8460 acoustic scans, 12 camera stations]"
    )
    lines.append("")
    lines.append("  Operator Notes: [No field notes entered]")
    lines.append("")
    lines.append(f"END OF LOG - {date_str}")
    lines.append("=" * 72)

    return "\n".join(lines)


def generate_habitat(output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "habitat")

    os.makedirs(output_dir, exist_ok=True)

    rng = random.Random(4471)
    model = PopulationModel(seed=4471)
    start_date = datetime.date(2024, 3, 15)

    for day in range(1, TOTAL_DAYS + 1):
        log_text = generate_sensor_log(day, model, rng, start_date)
        date = start_date + datetime.timedelta(days=day - 1)
        filename = f"sensor_log_{date.strftime('%Y%m%d')}.txt"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(log_text)
            f.write("\n")

    return os.path.abspath(output_dir)


def main():
    import sys
    output_dir = sys.argv[1] if len(sys.argv) > 1 else None
    path = generate_habitat(output_dir)

    print("Habitat data generated successfully.")
    print(f"  Location : {path}")
    print(f"  Files    : {TOTAL_DAYS} sensor logs")
    print(f"  Period   : Day 1 through Day {TOTAL_DAYS}")
    print(f"  Species  : {SPECIES_NAME} ({SPECIES_BINOMIAL})")
    print(f"  Site     : {SURVEY_SITE}")
    print(f"  Habitat  : 4.2 km\u00b2 mangrove")
    print()
    print("To begin monitoring, run:")
    print(f"  python monitor.py {path}")


if __name__ == "__main__":
    main()
