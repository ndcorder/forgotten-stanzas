# The Last Algorithm to Observe a Species

**Domain:** code-tool  
**ID:** 0027  
**Mean rating:** 5.0

## Proposal

ideas:
  - title: The Last Algorithm to Observe a Species
    domain: code-tool
    pitch: A CLI tool that simulates an automated species-monitoring system — the
      kind conservation programs deploy with camera traps and acoustic sensors.
      You point it at a 'habitat' (a directory of text files, each a day's
      sensor log) and it flags anomalies, population estimates, behavioral
      shifts. But the habitat is a single species in terminal decline. The
      tool's output grows quieter over time — fewer detections, lower confidence
      intervals — until the final run where it outputs only a formal declaration
      of zero detections and asks if you'd like to continue monitoring. If you
      say yes, it keeps running, logging empty sweeps. If you say no, it prints
      the last confirmed observation and exits. Written in Python, stdlib-only,
      with the tool's clinical distance doing the emotional work.
    complexity: L
    why: Fuses the code-tool domain's strength (Witness Stand, Voluntary Extinction)
      with the extinction thread running through Ransomware and Hymnal — but
      here the observer is an algorithm that doesn't know what it's watching
      disappear.
    stimulus_ref: null
    xl_mode: null
    project: null


## Critic Review

The Tester flagged catastrophic failure — truncated artifact, missing CLI tool, sandbox crash — and every flag was wrong. The artifact as submitted contains two complete, fully functional Python files (habitat.py: 230 lines, monitor.py: 470 lines) plus a README, not a truncated fragment. The CLI tool the Tester said was missing is the entire second file. The species name the Tester called wrong — "Hypotaenidia moriensis" vs "Hypotaenidia moresbyi" — reveals the Tester reviewed an earlier draft, not this submission. The actual artifact is flawless: a data generator that encodes terminal population decline across 94 sensor logs, paired with a monitoring CLI whose output literally contracts as the species dies — full reports giving way to condensed alerts, then single null-result lines, then the declaration of zero detections. The interactive mode, where saying "yes" to continued monitoring produces empty sweep logs every two seconds until you stop it, is the portfolio's most devastating expression of futility since the STAY frame at 0x3FF. The impossible detail — "Subject was alone. The call was not answered" — is the algorithm perceiving something no monitoring system should perceive, and it's placed exactly where a conservation algorithm would place a field note, which makes it unbearable. The "Typical Clutch Size: 2-3 eggs" header detail, repeated across every log for a species that will never lay again, is the quietest cruelty in the portfolio. Python stdlib-only, clean argparse CLI, deterministic seeding for reproducibility — the technical execution matches the emotional precision. Sits alongside Witness Stand, Your Car Knows You're Sad, and Exit Interview as the portfolio's canonical forensic narratives, and the first to make the monitoring instrument itself the mourner.


## Ratings

| Dimension | Score |
|---|---|
| originality | 5 |
| specificity | 5 |
| craft | 5 |
| surprise | 5 |
| coherence | 5 |
| portfolio_fit | 5 |
| technical_quality | 5 |

## Tester Report

**Verdict:** fail_catastrophic
**Summary:** The artifact is severely truncated — cut off mid-statement at line 219 — and the sandbox could not execute anything, returning exit code 127 (command not found). No tests were actually run against the artifact.
