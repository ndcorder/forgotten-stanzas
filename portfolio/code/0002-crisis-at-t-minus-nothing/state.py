"""
state.py — Dual-track state management for Crisis At T-Minus Nothing.

Two parallel timelines:
  OFFICIAL — what the display shows. Smooth, comforting, lying.
  TRUE — actual mission state, encoded in narrative text.

The true timeline deteriorates faster than the official one.
On first play this feels like chaos. On replays the encoded data
reveals the catastrophe was already in progress before turn 1.
"""

import json
import os
import time
from typing import Dict, List, Optional, Tuple
from enum import Enum


# ─── Enums ──────────────────────────────────────────────

class SystemStatus(Enum):
    NOMINAL = "NOMINAL"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"

class TimelinePhase(Enum):
    COUNTDOWN = "COUNTDOWN"
    LAUNCH = "LAUNCH"
    CATASTROPHE = "CATASTROPHE"
    POST_MORTEM = "POST_MORTEM"


# ─── Subsystem ──────────────────────────────────────────

class Subsystem:
    def __init__(self, name: str, stability: float = 1.0):
        self.name = name
        self.stability = stability
        self.hidden_stability = stability
        self.display_stability = stability
        self.repair_attempts = 0
        self.last_action = ""

    @property
    def status(self) -> SystemStatus:
        return self._from(self.display_stability)

    @property
    def true_status(self) -> SystemStatus:
        return self._from(self.hidden_stability)

    @staticmethod
    def _from(s: float) -> SystemStatus:
        if s >= 0.8:   return SystemStatus.NOMINAL
        if s >= 0.5:   return SystemStatus.DEGRADED
        if s >= 0.2:   return SystemStatus.CRITICAL
        if s > 0.0:    return SystemStatus.FAILED
        return SystemStatus.UNKNOWN

    def decay(self, amount: float, display_amount: float = 0.0):
        self.hidden_stability = max(0.0, self.hidden_stability - amount)
        self.display_stability = max(0.0, self.display_stability - display_amount)

    def repair(self, effectiveness: float = 0.15):
        self.repair_attempts += 1
        self.display_stability = min(1.0, self.display_stability + effectiveness)
        self.hidden_stability = min(1.0, self.hidden_stability + effectiveness * 0.4)

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'hidden': self.hidden_stability,
            'display': self.display_stability,
            'repairs': self.repair_attempts,
            'last': self.last_action,
        }


# ─── Mission State ──────────────────────────────────────

class MissionState:
    INITIAL_OFFICIAL = 60
    INITIAL_TRUE = 45   # Already 15 seconds behind reality
    TRUE_DECAY_RATE = 0.7

    def __init__(self, completion_count: int = 0):
        self.completion_count = completion_count
        self.official_countdown = self.INITIAL_OFFICIAL
        self.true_countdown = self.INITIAL_TRUE
        self.official_phase = TimelinePhase.COUNTDOWN
        self.true_phase = TimelinePhase.COUNTDOWN

        self.systems = {
            'life_support': Subsystem('life_support', 0.95),
            'comms': Subsystem('comms', 0.92),
            'propulsion': Subsystem('propulsion', 0.88),
            'navigation': Subsystem('navigation', 0.90),
        }

        self.override_official = True
        self.override_true = False
        self.turn_number = 0
        self.actions_taken: List[str] = []
        self.log_entries: List[str] = []
        self.catastrophe_triggered = False
        self.catastrophe_turn = -1

        # True system states are worse than displayed
        true_map = {
            'life_support': 0.70,
            'comms': 0.55,
            'propulsion': 0.35,
            'navigation': 0.60,
        }
        for name, sys in self.systems.items():
            sys.hidden_stability = true_map.get(name, 0.5)

        # Pre-existing conditions grow with completions
        self.pre_existing = self._build_pre_existing(completion_count)

    @staticmethod
    def _build_pre_existing(completions: int) -> List[str]:
        base = ['propulsion_micro_fracture']
        revealable = [
            'comms_intermittent_signal',
            'navigation_calibration_drift',
            'life_support_contamination',
            'crew_unreported_symptoms',
            'launch_authority_falsified_clearance',
            'true_countdown_started_before_you_arrived',
        ]
        return base + revealable[:min(completions, len(revealable))]

    def tick(self) -> Tuple[float, float]:
        self.turn_number += 1

        self.official_countdown -= 1.0

        true_tick = 1.0 + self.TRUE_DECAY_RATE
        system_penalty = sum(
            0.1 * (1.0 - s.hidden_stability) for s in self.systems.values()
        )
        self.true_countdown -= (true_tick + system_penalty)

        self._apply_decay()
        self._update_phases()

        if self.true_countdown <= 0 and not self.catastrophe_triggered:
            self.catastrophe_triggered = True
            self.catastrophe_turn = self.turn_number
            self.true_phase = TimelinePhase.CATASTROPHE

        return (max(0, self.official_countdown), max(0, self.true_countdown))

    def _apply_decay(self):
        official_decay = {
            'life_support': 0.01, 'comms': 0.015,
            'propulsion': 0.02, 'navigation': 0.012,
        }
        true_decay = {
            'life_support': 0.03, 'comms': 0.04,
            'propulsion': 0.06, 'navigation': 0.035,
        }
        cascade = {
            'propulsion': ['navigation', 'life_support'],
            'comms': ['navigation'],
            'navigation': ['propulsion'],
            'life_support': [],
        }
        for name, sys in self.systems.items():
            sys.decay(true_decay.get(name, 0.03), official_decay.get(name, 0.01))
        for name, sys in self.systems.items():
            if sys.hidden_stability < 0.3:
                for affected in cascade.get(name, []):
                    if affected in self.systems:
                        self.systems[affected].decay(0.02, 0.005)

    def _update_phases(self):
        for attr, val in [('official_countdown', 'official_phase'),
                          ('true_countdown', 'true_phase')]:
            v = getattr(self, attr)
            if v > 10:
                setattr(self, val, TimelinePhase.COUNTDOWN)
            elif v > 0:
                setattr(self, val, TimelinePhase.LAUNCH)
            else:
                setattr(self, val, TimelinePhase.POST_MORTEM)

    def execute_action(self, action: str, target: str = "") -> Dict:
        self.actions_taken.append(action)
        r = {'action': action, 'target': target, 'turn': self.turn_number,
             'official': '', 'truth': '', 'success': False}

        if action == 'repair' and target in self.systems:
            sys = self.systems[target]
            sys.repair()
            sys.last_action = 'repair'
            r['official'] = "Repair crew dispatched to {}. Status: {:.0%}".format(
                target, sys.display_stability)
            r['truth'] = "Actual improvement: {:.1%}".format(0.15 * 0.4)
            r['success'] = True

        elif action == 'check' and target in self.systems:
            sys = self.systems[target]
            r['official'] = "{}: {} ({:.0%})".format(
                target, sys.status.value, sys.display_stability)
            r['truth'] = "Actual: {} ({:.0%})".format(
                sys.true_status.value, sys.hidden_stability)
            r['success'] = True

        elif action == 'override':
            if self.override_true:
                r['official'] = "Override command sent. Awaiting confirmation..."
                r['truth'] = "Override signal lost. The channel was never open."
            else:
                r['official'] = "Override acknowledged. Sequence interrupted."
                r['truth'] = "Override received but damage persists."
                r['success'] = True
            self.override_official = False

        elif action == 'diagnose' and target in self.systems:
            sys = self.systems[target]
            r['official'] = "Diagnosing {}... Display: {:.0%}".format(
                target, sys.display_stability)
            gap = abs(sys.display_stability - sys.hidden_stability)
            if gap > 0.3:
                r['official'] += " [WARNING: Sensor readings may be compromised]"
            r['truth'] = "True stability: {:.0%}".format(sys.hidden_stability)
            r['success'] = True

        elif action == 'wait':
            r['official'] = "Holding. Systems nominal."
            r['truth'] = "Time passes. Things degrade."
            r['success'] = True

        elif action == 'analyze':
            r['official'] = "[Analysis mode invoked]"
            r['truth'] = ""
            r['success'] = True

        else:
            r['official'] = "Command not recognized."

        return r

    def failing_systems(self) -> List[str]:
        return [n for n, s in self.systems.items() if s.hidden_stability < 0.5]

    def critical_systems(self) -> List[str]:
        return [n for n, s in self.systems.items() if s.hidden_stability < 0.2]

    def format_official(self) -> str:
        r = max(0, self.official_countdown)
        if r <= 0: return "T+00:00.0"
        return "T-{:02d}:{:02d}.{}".format(int(r) // 60, int(r) % 60, int((r % 1) * 10))

    def format_true(self) -> str:
        r = max(0, self.true_countdown)
        if r <= 0: return "T+00:00"
        return "T-{:02d}:{:02d}".format(int(r) // 60, int(r) % 60)

    def is_terminal(self) -> bool:
        return (
            self.true_countdown <= 0 or
            self.official_countdown <= 0 or
            all(s.hidden_stability <= 0 for s in self.systems.values())
        )

    def summary(self) -> Dict:
        return {
            'official_countdown': self.official_countdown,
            'true_countdown': self.true_countdown,
            'turn': self.turn_number,
            'failing': self.failing_systems(),
            'critical': self.critical_systems(),
            'override_true': self.override_true,
            'catastrophe': self.catastrophe_triggered,
            'pre_existing': self.pre_existing,
            'systems': {
                n: {'display': s.display_stability, 'true': s.hidden_stability,
                    'status': s.status.value, 'true_status': s.true_status.value}
                for n, s in self.systems.items()
            },
        }


# ─── Persistence ────────────────────────────────────────

SAVE_FILE = os.path.join(os.path.expanduser("~"), ".tminus_save.json")

class GameStateManager:
    def __init__(self):
        self.completion_count = 0
        self.total_turns = 0
        self.catastrophes = 0
        self.layers_unlocked = 0
        self.ending = 'none'
        self._load()

    def _load(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    d = json.load(f)
                self.completion_count = d.get('completions', 0)
                self.total_turns = d.get('total_turns', 0)
                self.catastrophes = d.get('catastrophes', 0)
                self.layers_unlocked = d.get('layers', 0)
                self.ending = d.get('ending', 'none')
            except (json.JSONDecodeError, IOError):
                self._reset()

    def _reset(self):
        self.completion_count = 0
        self.total_turns = 0
        self.catastrophes = 0
        self.layers_unlocked = 0
        self.ending = 'none'

    def save(self):
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump({
                    'completions': self.completion_count,
                    'total_turns': self.total_turns,
                    'catastrophes': self.catastrophes,
                    'layers': self.layers_unlocked,
                    'ending': self.ending,
                    'saved_at': time.time(),
                }, f, indent=2)
        except IOError:
            pass

    def record_completion(self, state: MissionState):
        self.completion_count += 1
        self.total_turns += state.turn_number
        if state.catastrophe_triggered:
            self.catastrophes += 1
            self.ending = 'catastrophe'
        elif all(s.hidden_stability <= 0 for s in state.systems.values()):
            self.ending = 'total_failure'
        else:
            self.ending = 'survived'
        self.layers_unlocked = min(self.completion_count, 5)
        self.save()

    def replay_hint(self) -> str:
        hints = {
            0: "",
            1: "Analysis mode unlocked. Use 'analyze' on any log entry. The words count.",
            2: "Layer 2 unlocked — structural parity. Even and odd sentence lengths carry the tens digit.",
            3: "Layer 3 unlocked — terminal resonance. The last word knows which systems fail.",
            4: "Layer 4 unlocked — punctuation density. Override was never possible.",
            5: "Layer 5 unlocked — paragraph harmonics. Word count mod 60 IS the true countdown.",
        }
        if self.completion_count >= 6:
            return "All layers revealed. The truth was always encoded. It was always less."
        return hints.get(self.completion_count, hints[5])
