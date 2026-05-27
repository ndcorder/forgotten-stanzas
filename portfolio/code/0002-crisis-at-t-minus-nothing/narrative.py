"""
narrative.py — Prose generator with steganographic encoding.

Generates mission log entries that encode the true game state using
the five-layer system from encoder.py. The prose uses bureaucratic
language — passive voice, corporate euphemisms — to mask horror
in procedural routine.

Each log entry is carefully constructed so that:
  - Word counts hit encoding targets
  - Sentence structure carries hidden digits
  - Last words carry system stress codes
  - Punctuation density reflects override status
  - Paragraph totals encode the true countdown
"""

import random
from typing import Dict, List, Optional
from encoder import (
    encode_true_state, interpret_stress_code, SYSTEM_NAMES,
    _word_count, _vowel_count, _punctuation_count
)
from state import MissionState, TimelinePhase


# ─── Prose Fragments ────────────────────────────────────

# Bureaucratic openers (passive voice, no agency)
OPENERS = [
    "Routine monitoring indicates",
    "Standard diagnostics confirm",
    "Per protocol 7.4.2, attention is directed to",
    "Automated systems have logged",
    "The shift supervisor notes",
    "Post-review analysis reveals",
    "As of this timestamp,",
    "Continuous monitoring has observed",
    "Operations desk records indicate",
    "Per the duty officer's report,",
]

# System-specific observations (official language masking degradation)
SYSTEM_OFFICIAL = {
    'life_support': [
        "atmospheric composition remains within acceptable parameters",
        "oxygen recycling efficiency is tracking at nominal levels",
        "crew cabin pressure holds steady at standard configuration",
        "contaminant filters are operating within design specifications",
        "breathing air quality meets all mission criteria",
    ],
    'comms': [
        "signal clarity maintains expected throughput rates",
        "communication relay alignment is within tolerance",
        "data packet integrity remains above threshold",
        "external antenna array response times are standard",
        "channel availability meets operational requirements",
    ],
    'propulsion': [
        "engine thermal output registers within safe bands",
        "fuel flow rates maintain steady-state readings",
        "thrust vector calibration continues on profile",
        "reaction chamber pressures show expected values",
        "propellant consumption tracks with mission plan projections",
    ],
    'navigation': [
        "gyroscope alignment holds at designated coordinates",
        "trajectory calculations confirm planned flight path",
        "star tracker calibration maintains lock on reference bodies",
        "positional accuracy falls within mission specifications",
        "guidance computer solutions remain consistent with expectations",
    ],
}

# The truth, in bureaucratic dress
SYSTEM_DEGRADING = {
    'life_support': [
        "atmospheric renewal efficiency has been reclassified to require monitoring",
        "certain particulate readings have been flagged for further review",
        "air quality metrics are being re-evaluated under revised standards",
        "crew comfort indices have been adjusted downward per new guidelines",
    ],
    'comms': [
        "signal processing has been augmented with error correction protocols",
        "communication reliability is being maintained through backup channels",
        "data integrity verification has been increased to continuous mode",
        "external signal acquisition requires extended averaging periods",
    ],
    'propulsion': [
        "engine performance parameters are being managed under conservative profiles",
        "thermal management has been enhanced per contingency directive",
        "combustion stability monitoring has been upgraded to active surveillance",
        "propulsion output is being optimized for current material conditions",
    ],
    'navigation': [
        "positional certainty is being improved through additional reference fixes",
        "guidance accuracy is being verified against redundant calculation methods",
        "trajectory deviations are being corrected with increased frequency",
        "navigation solutions are being cross-referenced with secondary sensors",
    ],
}

SYSTEM_CRITICAL = {
    'life_support': [
        "life support protocols have been escalated to priority one review",
        "crew safety procedures have been activated in accordance with section 12.3",
        "atmospheric containment is being maintained via emergency protocols",
        "breathable air availability is being managed under conservation guidelines",
    ],
    'comms': [
        "communications are being maintained through auxiliary methods",
        "signal reconstruction is in progress using archived reference data",
        "contact procedures have been modified per emergency communication plans",
        "data recovery operations are ongoing for affected channels",
    ],
    'propulsion': [
        "propulsion systems are operating under emergency management protocols",
        "engine output is being sustained through alternative control pathways",
        "structural integrity monitoring for thrust assemblies has been maximized",
        "propulsive capability is being preserved through load reduction measures",
    ],
    'navigation': [
        "navigation is being conducted under degraded mode procedures",
        "positional awareness is being maintained through estimated reckoning",
        "guidance functions are being supplemented with manual calculation reserves",
        "orientation reference is being maintained via backup determination methods",
    ],
}

# Crew euphemisms — "efficiency optimization" means someone died
CREW_EUPHEMISMS = [
    "Crew efficiency optimization has been applied to section {section}.",
    "Personnel reallocation has been completed for {section} operations.",
    "Staffing levels in {section} have been adjusted per revised mission parameters.",
    "{section} duty roster has been streamlined for operational clarity.",
    "Human resources in {section} have been rationalized to reflect current needs.",
]

SECTIONS = ["alpha", "beta", "gamma", "delta", "engineering", "medical", "command"]

# Override-related language
OVERRIDE_LANGUAGE = {
    True: [
        "Override capability remains accessible to authorized personnel.",
        "Launch sequence interrupt is available per standard protocols.",
        "Mission abort option is maintained at current authorization level.",
    ],
    False: [
        "Override capability has been reclassified pending system review.",
        "Launch interrupt procedures are under administrative hold.",
        "Abort authorization requires re-verification through secured channels.",
    ],
}

# Closing formulas
CLOSINGS = [
    "This entry has been logged and indexed.",
    "Record filed under standard mission documentation.",
    "Entry complete. No further action required at this time.",
    "Log updated. All data archived per retention policy.",
    "This concludes the scheduled status update.",
]

# Words with specific vowel counts for terminal resonance
VOWEL_WORDS = {
    0: ['system', 'status', 'update', 'report', 'record', 'process'],
    1: ['review', 'report', 'assess', 'detail', 'ensure', 'advise'],
    2: ['continue', 'maintain', 'evaluate', 'surveil', 'ongoing', 'routine'],
    3: ['investigate', 'coordinate', 'document', 'calculate', 'accumulate'],
    4: ['re-evaluate', 'communicate', 're-calibrate', 'de-contaminate'],
}


# ─── Log Entry Generator ────────────────────────────────

class NarrativeEngine:
    """Generates encoded mission log prose."""

    def __init__(self, state: MissionState):
        self.state = state
        self.entry_history: List[str] = []

    def generate_log_entry(self) -> str:
        """Generate a complete mission log entry with full encoding."""
        s = self.state.summary()

        # Calculate encoding targets
        true_secs = max(0, int(s['true_countdown']))
        encoding = encode_true_state(
            true_secs,
            s['failing'],
            s['override_true'],
            base_word_count=22,
        )

        target_wc = encoding['target_word_count']
        target_para_wc = encoding['target_para_word_count']
        stress_code = encoding['stress_code']
        punct_density_target = encoding['target_punct_density']

        # Build paragraphs
        paragraphs = []
        for i in range(random.randint(2, 3)):
            para = self._build_paragraph(
                target_words=target_wc,
                stress_code=stress_code,
                punct_density=punct_density_target,
                is_critical=(i == 0),  # First paragraph gets the countdown encoding
            )
            paragraphs.append(para)

        # Adjust first paragraph to hit paragraph harmonics target
        if paragraphs:
            paragraphs[0] = self._adjust_word_count(paragraphs[0], target_para_wc)

        entry = "\n\n".join(paragraphs)
        self.entry_history.append(entry)
        return entry

    def _build_paragraph(
        self,
        target_words: int = 22,
        stress_code: int = 0,
        punct_density: float = 0.05,
        is_critical: bool = False,
    ) -> str:
        """Build a single paragraph of encoded prose."""
        sentences = []

        # 2-3 sentences per paragraph
        num_sentences = random.randint(2, 3)

        for i in range(num_sentences):
            sent = self._build_sentence(
                is_first=(i == 0),
                stress_code=stress_code,
            )
            sentences.append(sent)

        para = " ".join(sentences)

        # Adjust to target word count
        para = self._adjust_word_count(para, target_words)

        # Adjust punctuation density
        para = self._adjust_punctuation(para, punct_density)

        return para

    def _build_sentence(self, is_first: bool, stress_code: int = 0) -> str:
        """Build a single encoded sentence."""
        parts = []

        # Opener
        if is_first:
            parts.append(random.choice(OPENERS))

        # System report based on true state
        system_name = random.choice(list(SYSTEM_OFFICIAL.keys()))
        sys_state = self.state.systems[system_name]
        true_stability = sys_state.hidden_stability

        if true_stability >= 0.7:
            body = random.choice(SYSTEM_OFFICIAL[system_name])
        elif true_stability >= 0.4:
            body = random.choice(SYSTEM_DEGRADING.get(system_name, SYSTEM_DEGRADING['life_support']))
        else:
            body = random.choice(SYSTEM_CRITICAL.get(system_name, SYSTEM_CRITICAL['life_support']))

        parts.append(body)

        # Maybe add crew euphemism (10% chance if any system is critical)
        if true_stability < 0.3 and random.random() < 0.1:
            section = random.choice(SECTIONS)
            euphemism = random.choice(CREW_EUPHEMISMS).format(section=section)
            parts.append(euphemism)

        # Add closing for last sentence sometimes
        if not is_first and random.random() < 0.3:
            parts.append(random.choice(CLOSINGS))

        sentence = " ".join(parts)

        # Ensure sentence ends with period
        if sentence and sentence[-1] not in '.!?':
            sentence += "."

        # Terminal word adjustment for stress code
        sentence = self._adjust_terminal_word(sentence, stress_code)

        return sentence

    def _adjust_terminal_word(self, sentence: str, target_code: int) -> str:
        """
        Replace the last word with one that has the right vowel count
        to encode the stress code.
        """
        words = sentence.split()
        if not words:
            return sentence

        # Strip trailing punctuation from last word
        last = words[-1]
        punct_suffix = ""
        while last and last[-1] in '.,;:!?':
            punct_suffix = last[-1] + punct_suffix
            last = last[:-1]

        if not last:
            return sentence

        current_vowels = _vowel_count(last) % 5
        if current_vowels == target_code:
            return sentence

        # Find replacement word
        candidates = VOWEL_WORDS.get(target_code, VOWEL_WORDS[0])
        replacement = random.choice(candidates)
        words[-1] = replacement + punct_suffix

        return " ".join(words)

    def _adjust_word_count(self, text: str, target: int) -> str:
        """Pad or trim text to hit target word count."""
        words = text.split()
        current = len(words)

        if current == target:
            return text

        if current < target:
            # Add padding words (bureaucratic filler)
            filler = [
                "per established protocols",
                "in accordance with regulations",
                "as per standard operating procedure",
                "in compliance with mission directives",
                "consistent with operational guidelines",
            ]
            while len(words) < target:
                phrase = random.choice(filler).split()
                words.extend(phrase)
                # Don't overshoot by too much
                if len(words) > target + 5:
                    words = words[:target]

        if len(words) > target:
            words = words[:target]
            # Ensure sentence still ends properly
            if words and words[-1] and words[-1][-1] not in '.!?':
                words[-1] = words[-1] + "."

        return " ".join(words)

    def _adjust_punctuation(self, text: str, target_density: float) -> str:
        """Adjust punctuation density toward target."""
        non_space = len(text.replace(' ', ''))
        if non_space == 0:
            return text
        current_punct = _punctuation_count(text)
        current_density = current_punct / non_space

        if abs(current_density - target_density) < 0.01:
            return text

        if current_density < target_density:
            # Add punctuation — convert some commas or add semicolons
            words = text.split()
            new_words = []
            for i, w in enumerate(words):
                new_words.append(w)
                if i < len(words) - 1 and random.random() < 0.3:
                    new_words[-1] = new_words[-1] + ","
            text = " ".join(new_words)

        elif current_density > target_density:
            # Remove some punctuation
            words = text.split()
            new_words = []
            for w in words:
                # Strip internal commas sometimes
                if ',' in w and random.random() < 0.4:
                    w = w.replace(',', '')
                new_words.append(w)
            text = " ".join(new_words)

        return text

    def generate_catastrophe_text(self) -> str:
        """Generate the final catastrophe log entry."""
        entries = [
            "CONTINGENCY ALERT. All personnel are directed to emergency stations. "
            "Reactor containment status has been reclassified. This is not a drill. "
            "Crew efficiency optimization is in effect for all sections. "
            "Mission control acknowledges the situation. "
            "All logs will be preserved in accordance with directive 47. "
            "The countdown has concluded. The record will reflect nominal operations throughout. "
            "This entry is filed post-event as required by regulation. "
            "There is nothing further to report.",

            "EMERGENCY PROTOCOL ENGAGED. Propulsion anomaly detected outside "
            "predictive parameters. Containment teams have been deployed. "
            "Personnel in sections alpha through delta are reassigned. "
            "The situation is being managed per established guidelines. "
            "No further crew rotations are scheduled. "
            "All sensor data has been archived and flagged for review. "
            "The official timeline has been logged as planned. "
            "Any discrepancy in logs is attributed to sensor calibration drift. "
            "This entry concludes the mission record.",
        ]
        return random.choice(entries)

    def generate_opening_text(self, completion_count: int) -> str:
        """Generate the opening mission briefing."""
        base = (
            "MISSION BRIEFING — CLASSIFICATION: STANDARD\n"
            "Station Meridian-7, Orbital Platform, Year 2187.\n"
            "You are the duty officer for the next 60 seconds of the mission clock.\n"
            "Your responsibility is to monitor all subsystems and execute "
            "the engine test sequence at T-minus zero.\n"
            "All systems are reporting nominal. Standard protocols are in effect.\n"
            "The mission clock is authoritative. Trust the display."
        )

        if completion_count >= 3:
            base += (
                "\n\n[NOTICE: Analysis mode available. "
                "You have seen this before. Perhaps you will see what you missed.]"
            )

        return base
