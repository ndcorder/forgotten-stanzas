"""
encoder.py — Steganographic encoding layers for the hidden timeline.

Five encoding layers embed the TRUE countdown state in mission log prose.
Each layer is progressively revealed through analysis mode, unlocked
after completing the game once per layer.

Layers:
  1. Lexical Rhythm    — word count mod 3 → units digit class (0-2)
  2. Structural Parity — sentence word parity → tens digit parity
  3. Terminal Resonance — last word vowel count mod 5 → failing system bitmap
  4. Punctuation Density — punct/char ratio → override possibility
  5. Paragraph Harmonics — paragraph word count mod 60 → true countdown
"""

import re
from typing import List, Dict, Tuple


# ─── Layer Names and Descriptions ────────────────────────

LAYER_NAMES = [
    "Lexical Rhythm",
    "Structural Parity",
    "Terminal Resonance",
    "Punctuation Density",
    "Paragraph Harmonics",
]

LAYER_DESCRIPTIONS = [
    "Words per sentence, counted in threes, mark real time at its smallest scale.",
    "Even or odd sentence length carries the tens digit, hidden in plain grammar.",
    "The last word of each sentence, dissected for vowels, whispers which systems fail.",
    "Punctuation is not decoration. Its frequency encodes whether override was ever possible.",
    "Sum all words in a paragraph. Divide by sixty. The remainder is the true countdown.",
]


# ─── Utility ─────────────────────────────────────────────

def _split_sentences(text: str) -> List[str]:
    raw = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in raw if s.strip()]

def _split_paragraphs(text: str) -> List[str]:
    raw = re.split(r'\n\s*\n', text.strip())
    return [p.strip() for p in raw if p.strip()]

def _word_count(text: str) -> int:
    return len(text.split())

def _vowel_count(text: str) -> int:
    return sum(1 for c in text.lower() if c in 'aeiou')

def _punctuation_count(text: str) -> int:
    return sum(1 for c in text if c in '.,;:!?—\'"()[]-')


# ─── Layer 1: Lexical Rhythm ────────────────────────────

def encode_layer_1(seconds_unit: int, base_word_count: int = 20) -> int:
    """Adjust word count so that (count % 3) == (seconds_unit % 3)."""
    target_mod = seconds_unit % 3
    current_mod = base_word_count % 3
    if current_mod == target_mod:
        return base_word_count
    offset = (target_mod - current_mod) % 3
    if offset <= 1:
        return base_word_count + offset
    return base_word_count - (3 - offset)

def decode_layer_1(sentence: str) -> int:
    return _word_count(sentence) % 3

def decode_layer_1_full(text: str) -> List[int]:
    return [decode_layer_1(s) for s in _split_sentences(text)]


# ─── Layer 2: Structural Parity ─────────────────────────

def encode_layer_2(tens_digit: int, word_count: int) -> int:
    """Adjust word count parity to match tens_digit parity."""
    if (word_count % 2) == (tens_digit % 2):
        return word_count
    return word_count + 1

def decode_layer_2(sentence: str) -> int:
    return _word_count(sentence) % 2

def decode_layer_2_full(text: str) -> List[int]:
    return [decode_layer_2(s) for s in _split_sentences(text)]


# ─── Layer 3: Terminal Resonance ─────────────────────────

SYSTEM_NAMES = ['life_support', 'comms', 'propulsion', 'navigation']

def encode_layer_3(failing_systems: List[str]) -> int:
    bitmap = 0
    for i, name in enumerate(SYSTEM_NAMES):
        if name in failing_systems:
            bitmap |= (1 << i)
    return bitmap % 5

def decode_layer_3(sentence: str) -> int:
    words = sentence.split()
    if not words:
        return 0
    last_word = re.sub(r'[.,;:!?\'"—]+$', '', words[-1])
    return _vowel_count(last_word) % 5

def decode_layer_3_full(text: str) -> List[int]:
    return [decode_layer_3(s) for s in _split_sentences(text)]

def interpret_stress_code(code: int) -> Dict[str, bool]:
    return {name: bool(code & (1 << i)) for i, name in enumerate(SYSTEM_NAMES)}


# ─── Layer 4: Punctuation Density ────────────────────────

def encode_layer_4(override_possible: bool) -> float:
    return 0.10 if override_possible else 0.03

def decode_layer_4(text: str) -> bool:
    total_chars = len(text.replace(' ', ''))
    if total_chars == 0:
        return False
    return (_punctuation_count(text) / total_chars) > 0.06


# ─── Layer 5: Paragraph Harmonics ────────────────────────

def encode_layer_5(true_countdown: int) -> int:
    return true_countdown % 60

def decode_layer_5(paragraph: str) -> int:
    return _word_count(paragraph) % 60

def decode_layer_5_full(text: str) -> List[int]:
    return [decode_layer_5(p) for p in _split_paragraphs(text)]


# ─── Composite ───────────────────────────────────────────

def encode_true_state(
    true_seconds: int,
    failing_systems: List[str],
    override_possible: bool,
    base_word_count: int = 20,
) -> Dict:
    units = true_seconds % 10
    tens = (true_seconds // 10) % 6

    wc_l1 = encode_layer_1(units, base_word_count)
    wc_l2 = encode_layer_2(tens, wc_l1)

    return {
        'target_word_count': wc_l2,
        'stress_code': encode_layer_3(failing_systems),
        'target_punct_density': encode_layer_4(override_possible),
        'target_para_word_count': encode_layer_5(true_seconds),
        'true_seconds': true_seconds,
        'units_digit': units,
        'tens_digit': tens,
    }

def decode_full(text: str) -> Dict:
    sentences = _split_sentences(text)
    paragraphs = _split_paragraphs(text)

    results = {
        'layer_1': decode_layer_1_full(text),
        'layer_2': decode_layer_2_full(text),
        'layer_3': decode_layer_3_full(text),
        'layer_4_override': decode_layer_4(text),
        'layer_5': decode_layer_5_full(text),
    }

    if sentences:
        l1 = results['layer_1']
        l2 = results['layer_2']
        results['units_class'] = max(set(l1), key=l1.count)
        results['tens_parity'] = max(set(l2), key=l2.count)

    if paragraphs:
        results['true_countdown_estimates'] = results['layer_5']

    return results


# ─── Analysis Report Generator ───────────────────────────

def analyze_text(text: str, completion_count: int) -> str:
    lines = []
    lines.append("═" * 60)
    lines.append("  MISSION LOG ANALYSIS — CLEARANCE LEVEL {}".format(
        min(completion_count, 5)
    ))
    lines.append("═" * 60)
    lines.append("")

    sentences = _split_sentences(text)
    paragraphs = _split_paragraphs(text)

    lines.append("Words: {}  Sentences: {}  Paragraphs: {}".format(
        _word_count(text), len(sentences), len(paragraphs)
    ))
    lines.append("")

    if completion_count >= 1:
        lines.append("─" * 40)
        lines.append("LAYER 1: {}".format(LAYER_NAMES[0]))
        lines.append(LAYER_DESCRIPTIONS[0])
        lines.append("─" * 40)
        for i, (s, v) in enumerate(zip(sentences, decode_layer_1_full(text))):
            preview = s[:50] + "..." if len(s) > 50 else s
            lines.append("  S{:02d} [rhythm={}] {}".format(i + 1, v, preview))
        lines.append("")

    if completion_count >= 2:
        lines.append("─" * 40)
        lines.append("LAYER 2: {}".format(LAYER_NAMES[1]))
        lines.append(LAYER_DESCRIPTIONS[1])
        lines.append("─" * 40)
        for i, (s, v) in enumerate(zip(sentences, decode_layer_2_full(text))):
            wc = _word_count(s)
            preview = s[:50] + "..." if len(s) > 50 else s
            lines.append("  S{:02d} [words={} parity={}] {}".format(i + 1, wc, v, preview))
        lines.append("")

    if completion_count >= 3:
        lines.append("─" * 40)
        lines.append("LAYER 3: {}".format(LAYER_NAMES[2]))
        lines.append(LAYER_DESCRIPTIONS[2])
        lines.append("─" * 40)
        for i, (s, code) in enumerate(zip(sentences, decode_layer_3_full(text))):
            systems = interpret_stress_code(code)
            failing = [k for k, v in systems.items() if v]
            preview = s[:40] + "..." if len(s) > 40 else s
            tag = "FAILING: {}".format(", ".join(failing)) if failing else "NOMINAL"
            lines.append("  S{:02d} [stress={}] {} | {}".format(i + 1, code, tag, preview))
        lines.append("")

    if completion_count >= 4:
        lines.append("─" * 40)
        lines.append("LAYER 4: {}".format(LAYER_NAMES[3]))
        lines.append(LAYER_DESCRIPTIONS[3])
        lines.append("─" * 40)
        total_chars = len(text.replace(' ', ''))
        punct = _punctuation_count(text)
        density = punct / total_chars if total_chars else 0
        override = decode_layer_4(text)
        lines.append("  Punctuation: {}  Characters: {}  Density: {:.4f}".format(
            punct, total_chars, density
        ))
        lines.append("  Override: {}".format("POSSIBLE" if override else "IMPOSSIBLE"))
        lines.append("")

    if completion_count >= 5:
        lines.append("─" * 40)
        lines.append("LAYER 5: {}".format(LAYER_NAMES[4]))
        lines.append(LAYER_DESCRIPTIONS[4])
        lines.append("─" * 40)
        for i, (p, h) in enumerate(zip(paragraphs, decode_layer_5_full(text))):
            wc = _word_count(p)
            lines.append("  P{:02d} [words={} mod60={}] TRUE COUNTDOWN: T-{:02d}".format(
                i + 1, wc, h, h
            ))
        lines.append("")
        lines.append("  ▸ The countdown you saw was not the countdown that mattered.")
        lines.append("  ▸ The catastrophe was encoded from the beginning.")
        lines.append("")

    if completion_count >= 6:
        lines.append("═" * 60)
        lines.append("  ADDENDUM — FOR EYES THAT HAVE SEEN ENOUGH")
        lines.append("═" * 60)
        lines.append("")
        lines.append("  There is no layer 6.")
        lines.append("  There is only the fact that you kept looking.")
        lines.append("  The launch happened. The countdown reached zero.")
        lines.append("  Everything after that is just us, reading the logs,")
        lines.append("  trying to find the moment we could have changed things.")
        lines.append("")
        lines.append("  The moment was always before we started.")
        lines.append("")

    lines.append("═" * 60)
    lines.append("  END ANALYSIS")
    lines.append("═" * 60)
    return "\n".join(lines)

def format_layer_hint(completion_count: int) -> str:
    hints = {
        0: "The display tells you what it wants you to believe.",
        1: "Analysis mode unlocked. Count the words. Groups of three.",
        2: "Layer 2 unlocked. Even and odd. The grammar knows.",
        3: "Layer 3 unlocked. The last word of each sentence carries weight.",
        4: "Layer 4 unlocked. Punctuation is not decorative.",
        5: "Layer 5 unlocked. The paragraph remembers. T-minus the truth.",
    }
    if completion_count >= 6:
        return "All layers revealed. There is nothing left to decode. Only to understand."
    return hints.get(completion_count, hints[5])
