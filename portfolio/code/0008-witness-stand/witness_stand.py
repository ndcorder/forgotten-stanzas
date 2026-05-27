#!/usr/bin/env python3
"""
WITNESS STAND — A command-line tool that cross-examines your writing.

Feed it a text file and it becomes a prosecutor. It identifies crutches,
then generates a hostile interrogation. But beware: the prosecutor has
biases, quirks, and an unreliable disposition all its own.

Usage: python witness_stand.py <file> [--verbose]
"""

import sys
import re
import argparse
import random
import math
from collections import Counter

# ============================================================================
# PART 1: Analysis Engine
# ============================================================================

HEDGE_WORDS = {
    'perhaps', 'maybe', 'possibly', 'somewhat', 'rather', 'quite',
    'fairly', 'sort of', 'kind of', 'in a way', 'arguably',
    'seemingly', 'apparently', 'evidently', 'supposedly', 'allegedly',
    'reportedly', 'purportedly', 'basically', 'essentially', 'literally',
    'actually', 'honestly', 'truly', 'really', 'very', 'just', 'simply',
    'merely', 'only', 'hardly', 'barely', 'scarcely', 'almost', 'nearly',
    'about', 'around', 'roughly', 'approximately', 'somehow',
    'a bit', 'a little', 'in some respects', 'to some extent', 'i think',
    'i believe', 'i feel', 'i guess', 'i suppose', 'it seems',
    'it appears', 'one might say', 'you could argue'
}

WEAK_VERBS = {
    'was', 'were', 'is', 'are', 'been', 'being', 'am', 'be',
    'had', 'has', 'have', 'did', 'does', 'do', 'got', 'get',
    'gets', 'getting', 'make', 'makes', 'made', 'take', 'takes', 'taken',
    'put', 'set', 'go', 'goes', 'went', 'gone', 'come', 'comes', 'came'
}

DIALOGUE_TAGS = {
    'said', 'says', 'say', 'asked', 'asks', 'ask', 'replied', 'replies',
    'reply', 'answered', 'answers', 'answer', 'whispered', 'whispers',
    'whisper', 'shouted', 'shouts', 'shout', 'muttered', 'mutters',
    'mutter', 'murmured', 'murmurs', 'murmur', 'exclaimed', 'exclaims',
    'exclaim', 'gasped', 'gasps', 'gasp', 'snapped', 'snaps', 'snap',
    'growled', 'growls', 'growl', 'hissed', 'hisses', 'hiss', 'sighed',
    'sighs', 'sigh', 'laughed', 'laughs', 'laugh', 'cried', 'cries',
    'cry', 'yelled', 'yells', 'yell', 'screamed', 'screams', 'scream',
    'whimpered', 'whimpers', 'whimper', 'stammered', 'stammers',
    'stammer', 'stuttered', 'stutters', 'stutter', 'interrupted',
    'interrupts', 'interrupt', 'continued', 'continues', 'continue',
    'added', 'adds', 'add', 'agreed', 'agrees', 'agree', 'insisted',
    'insists', 'insist', 'demanded', 'demands', 'demand', 'pleaded',
    'pleads', 'plead', 'begged', 'begs', 'beg', 'teased', 'teases',
    'tease', 'joked', 'jokes', 'joke', 'warned', 'warns', 'warn',
    'promised', 'promises', 'promise', 'suggested', 'suggests', 'suggest',
    'observed', 'observes', 'observe', 'remarked', 'remarks', 'remark',
    'noted', 'notes', 'note', 'declared', 'declares', 'declare',
    'announced', 'announces', 'announce', 'stated', 'states', 'state',
    'bellowed', 'bellow', 'roared', 'roars', 'roar',
    'sneered', 'sneers', 'sneer', 'scoffed', 'scoffs', 'scoff',
    'chuckled', 'chuckles', 'chuckle', 'giggled', 'giggles', 'giggle',
    'moaned', 'moans', 'moan', 'groaned', 'groans', 'groan', 'grunted',
    'grunts', 'grunt', 'mumbled', 'mumbles', 'mumble'
}

ADVERB_SUSPECTS = {
    'suddenly', 'quickly', 'slowly', 'quietly', 'loudly', 'softly',
    'gently', 'harshly', 'carefully', 'carelessly', 'eagerly',
    'reluctantly', 'hesitantly', 'nervously', 'calmly', 'angrily',
    'sadly', 'happily', 'desperately', 'frantically', 'breathlessly',
    'effortlessly', 'silently', 'swiftly', 'hastily', 'steadily',
    'firmly', 'loosely', 'tightly', 'warmly', 'coldly', 'darkly',
    'brightly', 'dimly', 'vaguely', 'sharply', 'dully', 'wildly',
    'madly', 'blindly', 'blankly', 'blandly', 'boldly', 'bluntly',
    'blissfully', 'grimly', 'gravely', 'sternly'
}

VERBOSITY_TANGENTS = [
    "\n    [The prosecutor pauses, adjusting papers that don't need adjusting.]\n"
    "    PROSECUTOR: I've lost my train of thought. Where was I? Adverbs.\n"
    "    Yes. No — sentence structure. The witness mentioned sentence structure.\n"
    "    Or was I about to bring up the coffee situation in this courthouse?\n"
    "    The jury will disregard that last remark. All of it. Everything\n"
    "    after 'Exhibit.' No, after 'the.' The jury will disregard 'the.'\n",

    "\n    [A long, uncomfortable silence.]\n"
    "    PROSECUTOR: You know what, let the record show that I forgot what\n"
    "    case this is. The PEOPLE versus... versus...\n"
    "    [Whispering to clerk] What's the defendant's name again?\n"
    "    PROSECUTOR: The PEOPLE versus the TEXT. Yes. Of course. Moving on.\n",

    "\n    [The prosecutor stares at the ceiling for eleven seconds.]\n"
    "    PROSECUTOR: Have you ever noticed how 'sentence' contains the word\n"
    "    'sense'? Almost. Not quite. There's probably something there.\n"
    "    A deeper meaning. Or there isn't. I've lost the thread.\n"
    "    The jury will disregard my existential crisis.\n",

    "\n    [The prosecutor's watch alarm goes off.]\n"
    "    PROSECUTOR: Ah. It's 2:47. I had something scheduled for 2:47.\n"
    "    Can't remember what. Seemed important at the time.\n"
    "    [Turns back to witness] Where were we? Right. Crimes against prose.\n"
    "    Although — is prose even real? Just a thought. Next exhibit.\n",

    "\n    [The prosecutor begins doodling on a legal pad.]\n"
    "    PROSECUTOR: The defense will note that I am paying close attention.\n"
    "    [The doodle appears to be a cat riding a bicycle.]\n"
    "    PROSECUTOR: Very close attention. Continue.\n",

    "\n    [The prosecutor removes glasses they weren't wearing.]\n"
    "    PROSECUTOR: Let me approach the bench. Actually, no. Let me approach\n"
    "    the witness. No — let me approach my own sense of purpose.\n"
    "    [Sits down heavily] Sometimes I wonder if I'm too hard on writers.\n"
    "    Then I remember: no. I am not. Next question.\n"
    "    [Long pause] I've forgotten the question.\n",

    "\n    [The prosecutor argues with a water bottle.]\n"
    "    PROSECUTOR: The cap is RIGHT THERE. It's— [notices jury staring]\n"
    "    The jury will note that the defendant's prose is as difficult to\n"
    "    open as this— no. Strike that. The jury will disregard.\n",

    "\n    [The prosecutor reads back a sentence, then reads it again.]\n"
    "    PROSECUTOR: Wait, I already covered this. Didn't I? [Checks notes.]\n"
    "    [Checks notes again, more slowly.] The prosecution may be going in\n"
    "    circles. The jury will be seated while I find my place.\n",

    "\n    [The prosecutor objects to their own question.]\n"
    "    PROSECUTOR: Objection! Leading the witness.\n"
    "    JUDGE: You're the one asking the questions.\n"
    "    PROSECUTOR: I know. I'm also the one objecting. Sustained.\n"
    "    The jury will disregard the question I was about to ask,\n"
    "    which I have now forgotten. Advantage: prosecution.\n",
]


class AnalysisEngine:
    """Performs linguistic analysis on a text, extracting patterns and crutches."""

    def __init__(self, text):
        self.text = text
        self.words = []
        self.sentences = []
        self.paragraphs = []
        self._tokenize()

    def _tokenize(self):
        """Break text into paragraphs, sentences, and words."""
        self.paragraphs = [p.strip() for p in self.text.split('\n\n') if p.strip()]
        raw_sentences = re.split(r'(?<=[.!?])\s+', self.text)
        self.sentences = [s.strip() for s in raw_sentences if s.strip()
                         and len(s.strip()) > 2]
        self.words = re.findall(r"[a-zA-Z']+", self.text.lower())

    def word_count(self):
        return len(self.words)

    def unique_word_count(self):
        return len(set(self.words))

    def sentence_count(self):
        return len(self.sentences)

    def paragraph_count(self):
        return len(self.paragraphs)

    def lexical_diversity(self):
        if not self.words:
            return 0.0
        return len(set(self.words)) / len(self.words)

    def word_frequency(self, top_n=30):
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'of', 'it', 'is', 'was', 'he', 'she', 'they', 'we',
            'you', 'i', 'me', 'my', 'his', 'her', 'its', 'our', 'your',
            'that', 'this', 'with', 'for', 'as', 'by', 'from', 'not',
            'no', 'if', 'so', 'up', 'out', 'do', 'be', 'am', 'are',
            'been', 'has', 'had', 'have', 'did', 'does', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'into', 'than',
            'them', 'then', 'there', 'these', 'those', 'all', 'each',
            'every', 'both', 'few', 'more', 'most', 'other', 'some',
            'such', 'only', 'own', 'same', 'too', 'very', 'just', 'also',
            'now', 'here', 'when', 'where', 'how', 'what', 'which', 'who',
            'whom', 'whose', 'while', 'about', 'after', 'before', 'between',
            'through', 'during', 'without', 'again', 'once', 'any'
        }
        filtered = [w for w in self.words if len(w) > 3 and w not in stop_words]
        return Counter(filtered).most_common(top_n)

    def sentence_lengths(self):
        lengths = []
        for sent in self.sentences:
            words_in_sent = re.findall(r"[a-zA-Z']+", sent)
            if words_in_sent:
                lengths.append(len(words_in_sent))
        return lengths

    def average_sentence_length(self):
        lengths = self.sentence_lengths()
        if not lengths:
            return 0.0
        return sum(lengths) / len(lengths)

    def sentence_variance(self):
        lengths = self.sentence_lengths()
        if len(lengths) < 2:
            return 0.0
        mean = sum(lengths) / len(lengths)
        variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
        return math.sqrt(variance)

    def monotonous_sentences(self):
        """Detect stretches of similar-length sentences.

        BIAS: Stretches of short sentences (<8 words) are never flagged,
        because the prosecutor has a weakness for short declaratives.
        """
        lengths = self.sentence_lengths()
        if len(lengths) < 5:
            return []
        monotonous = []
        for i in range(len(lengths) - 4):
            window = lengths[i:i+5]
            avg = sum(window) / len(window)
            if all(abs(l - avg) <= 2 for l in window):
                # Bias: short declarative stretches are never flagged
                if avg < 8:
                    continue
                monotonous.append((i, window))
        return monotonous

    def hedge_count(self):
        text_lower = self.text.lower()
        count = 0
        found = []
        for hedge in HEDGE_WORDS:
            occurrences = len(re.findall(r'\b' + re.escape(hedge) + r'\b', text_lower))
            if occurrences > 0:
                count += occurrences
                found.append((hedge, occurrences))
        found.sort(key=lambda x: -x[1])
        return count, found

    def adverb_density(self):
        ly_words = [w for w in self.words if w.endswith('ly') and len(w) > 4]
        suspect_words = [w for w in self.words if w in ADVERB_SUSPECTS]
        adverb_counts = Counter(ly_words + suspect_words)
        total = len(self.words) if self.words else 1
        density = len(ly_words + suspect_words) / total
        return density, adverb_counts.most_common(20), len(set(ly_words + suspect_words))

    def passive_voice_instances(self):
        text_lower = self.text.lower()
        passive_patterns = [
            r'\bwas\s+(\w+ed)\b', r'\bwere\s+(\w+ed)\b',
            r'\bis\s+(\w+ed)\b', r'\bare\s+(\w+ed)\b',
            r'\bbeen\s+(\w+ed)\b',
            r'\bwas\s+being\s+(\w+ed)\b', r'\bwere\s+being\s+(\w+ed)\b',
            r'\bhad\s+been\s+(\w+ed)\b', r'\bhave\s+been\s+(\w+ed)\b',
            r'\bhas\s+been\s+(\w+ed)\b',
            r'\bwill\s+be\s+(\w+ed)\b', r'\bwould\s+be\s+(\w+ed)\b',
            r'\bcould\s+be\s+(\w+ed)\b', r'\bshould\s+be\s+(\w+ed)\b',
        ]
        found = []
        for pattern in passive_patterns:
            matches = re.findall(pattern, text_lower)
            found.extend(matches)
        return Counter(found).most_common(10), len(found)

    def weak_verb_density(self):
        weak = [w for w in self.words if w in WEAK_VERBS]
        total = len(self.words) if self.words else 1
        return len(weak), len(weak) / total, Counter(weak).most_common(10)

    def dialogue_tag_analysis(self):
        tag_counts = Counter()
        for tag in DIALOGUE_TAGS:
            pattern = r'\b' + re.escape(tag) + r'\b'
            matches = re.findall(pattern, self.text.lower())
            if matches:
                tag_counts[tag] = len(matches)
        return tag_counts.most_common(15)

    def find_instances_of(self, word, context_chars=50):
        instances = []
        text_lower = self.text.lower()
        word_lower = word.lower()
        start = 0
        while True:
            pos = text_lower.find(word_lower, start)
            if pos == -1:
                break
            ctx_start = max(0, pos - context_chars)
            ctx_end = min(len(self.text), pos + len(word) + context_chars)
            context = self.text[ctx_start:ctx_end].replace('\n', ' ')
            if ctx_start > 0:
                context = '...' + context
            if ctx_end < len(self.text):
                context = context + '...'
            instances.append(context)
            start = pos + 1
            if len(instances) >= 5:
                break
        return instances

    def detect_crutch_phrases(self):
        if len(self.words) < 10:
            return []
        bigrams = []
        for i in range(len(self.words) - 1):
            pair = self.words[i] + ' ' + self.words[i+1]
            bigrams.append(pair)
        bigram_counts = Counter(bigrams)
        stop = {
            'of the', 'in the', 'to the', 'it was', 'he was', 'she was',
            'i was', 'they were', 'on the', 'at the', 'with a', 'with the',
            'for a', 'for the', 'from the', 'to be', 'is a', 'is the',
            'was a', 'was the', 'had been', 'have been', 'out of', 'and the'
        }
        suspicious = [(phrase, count) for phrase, count in bigram_counts.items()
                     if count >= 3 and phrase not in stop]
        suspicious.sort(key=lambda x: -x[1])
        return suspicious[:15]

    def find_effective_passages(self):
        """Identify passages that are genuinely good.

        The bar is set intentionally where the prosecutor's biases live:
        short declarative sentences get special treatment.
        """
        good = []
        for i, sent in enumerate(self.sentences):
            words_in = re.findall(r"[a-zA-Z']+", sent)
            wl = len(words_in)
            # Short declarative sentences — the prosecutor's weakness.
            # Very lenient: just needs to be short and not stuffed with adverbs.
            if 3 <= wl <= 9:
                has_ly = any(w.endswith('ly') for w in words_in)
                has_hedge = any(w.lower() in HEDGE_WORDS for w in words_in)
                if not has_ly and not has_hedge:
                    good.append((sent.strip(), 'short_declarative'))
                    continue

            # Sentences with strong specificity
            if wl >= 8:
                specific_words = sum(1 for w in words_in if len(w) >= 7)
                has_ly = any(w.endswith('ly') for w in words_in)
                if specific_words >= 3 and wl <= 18 and not has_ly:
                    good.append((sent.strip(), 'specific'))

        return good


# ============================================================================
# PART 2: Prosecutorial Voice Generator
# ============================================================================

class Prosecutor:
    """Generates courtroom-style cross-examination based on text analysis."""

    def __init__(self, analysis, verbose=False, filename="the text"):
        self.a = analysis
        self.verbose = verbose
        self.filename = filename
        self.severity = 0.0
        self.complaints = []
        self.defenses = []
        self._used_tangents = []
        self._assess_severity()

    def _assess_severity(self):
        wc = self.a.word_count()
        if wc == 0:
            return

        density, adverbs, unique = self.a.adverb_density()
        hedge_total, hedges = self.a.hedge_count()
        passive_words, passive_total = self.a.passive_voice_instances()
        variance = self.a.sentence_variance()
        mono = len(self.a.monotonous_sentences())
        tags = self.a.dialogue_tag_analysis()
        diversity = self.a.lexical_diversity()

        if adverbs:
            top_adverb = adverbs[0]
            self.complaints.append(f"adverb '{top_adverb[0]}' appears {top_adverb[1]} time(s)")
            self.severity += min(top_adverb[1] * 0.5, 3.0)

        if hedge_total > 3:
            self.complaints.append(f"hedge language detected {hedge_total} times")
            self.severity += min(hedge_total * 0.3, 2.5)

        if passive_total > 5:
            self.complaints.append(f"passive voice used {passive_total} times")
            self.severity += min(passive_total * 0.2, 2.0)

        if variance < 3.0 and self.a.sentence_count() > 8:
            self.complaints.append("sentence lengths are dangerously uniform")
            self.severity += 1.5

        if mono:
            self.complaints.append(f"{len(mono)} monotonous passage(s) detected")
            self.severity += len(mono) * 0.5

        if diversity < 0.3 and wc > 100:
            self.complaints.append(f"low lexical diversity ({diversity:.2f})")
            self.severity += 1.0

        top_words = self.a.word_frequency(10)
        if top_words and top_words[0][1] > max(5, wc * 0.03):
            self.complaints.append(f"word '{top_words[0][0]}' appears {top_words[0][1]} times")
            self.severity += 1.0

        if tags and tags[0][1] > 8:
            self.complaints.append(f"dialogue tag '{tags[0][0]}' used {tags[0][1]} times")
            self.severity += 0.8

        crutches = self.a.detect_crutch_phrases()
        if crutches:
            phrase, count = crutches[0]
            self.complaints.append(f"phrase '{phrase}' repeats {count} times")
            self.severity += min(count * 0.3, 1.5)

        effective = self.a.find_effective_passages()
        if effective:
            self.defenses = effective[:3]

    def _intensity_level(self):
        if self.severity < 2:
            return 'gentle'
        elif self.severity < 5:
            return 'moderate'
        elif self.severity < 8:
            return 'severe'
        else:
            return 'devastating'

    def _random_tangent(self):
        available = [t for i, t in enumerate(VERBOSITY_TANGENTS)
                    if i not in self._used_tangents]
        if not available:
            self._used_tangents = []
            available = VERBOSITY_TANGENTS
        idx = VERBOSITY_TANGENTS.index(random.choice(available))
        self._used_tangents.append(idx)
        return VERBOSITY_TANGENTS[idx]

    def generate_opening(self):
        wc = self.a.word_count()
        sc = self.a.sentence_count()
        pc = self.a.paragraph_count()
        level = self._intensity_level()

        lines = []
        lines.append("=" * 70)
        lines.append("                    IN THE COURT OF LITERARY AFFAIRS")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"    Case No. {random.randint(1000,9999)}-{random.randint(10,99)}")
        lines.append(f"    THE PEOPLE v. \"{self.filename}\"")
        lines.append("")
        lines.append("-" * 70)
        lines.append("    PROSECUTOR'S OPENING STATEMENT")
        lines.append("-" * 70)
        lines.append("")

        if wc == 0:
            lines.append(
                "    PROSECUTOR: Ladies and gentlemen of the jury, I present before\n"
                "    you... nothing. The defendant has submitted a text devoid of content.\n"
                "    I rest my case before it begins. The prosecution moves for summary\n"
                "    judgment on the grounds that you can't judge what isn't there.\n"
            )
            return '\n'.join(lines)

        openings = {
            'gentle': [
                f"    PROSECUTOR: Ladies and gentlemen of the jury, I approach this bench\n"
                f"    not with outrage, but with... disappointment. Mild disappointment.\n"
                f"    The kind a teacher feels when a talented student turns in homework\n"
                f"    that's good instead of great.\n\n"
                f"    Before you sits a text of {wc:,} words, {sc} sentences, and {pc}\n"
                f"    paragraphs. It has potential. The prosecution will demonstrate that\n"
                f"    this potential has been partially — not completely — squandered.\n",
                f"    PROSECUTOR: The prosecution acknowledges at the outset that the\n"
                f"    defendant is not without merit. At {wc:,} words, this text has\n"
                f"    been efforted upon. That is a word now. 'Efforted.'\n\n"
                f"    However, effort and execution are two different beasts. The\n"
                f"    prosecution will show that this beast — while not the ugliest in\n"
                f"    the stable — has a few spots that could use grooming.\n",
            ],
            'moderate': [
                f"    PROSECUTOR: Ladies and gentlemen, what you see before you is a text\n"
                f"    that aspires to competence. {wc:,} words across {sc} sentences\n"
                f"    and {pc} paragraphs. A text that wants you to believe it tried.\n\n"
                f"    The prosecution will demonstrate that this 'best' was nowhere near\n"
                f"    the defendant's capability. We will show patterns of laziness,\n"
                f"    structural monotony, and prose that reaches for mediocrity and,\n"
                f"    on occasion, grasps it.\n",
                f"    PROSECUTOR: Let the record show that the defendant stands accused\n"
                f"    of writing crimes ranging from the mediocre to the unfortunate.\n"
                f"    {wc:,} words. {sc} sentences. {pc} paragraphs.\n\n"
                f"    I would say 'each one a crime,' but that would be hyperbole, and\n"
                f"    the prosecution deals in evidence. Only some of them are crimes.\n"
                f"    The prosecution will identify which ones.\n",
            ],
            'severe': [
                f"    PROSECUTOR: Ladies and gentlemen, I wish I could say I come before\n"
                f"    you with good news. I do not. What I have is a text — {wc:,} words\n"
                f"    of it — that constitutes a sustained assault on the English language.\n\n"
                f"    The prosecution will present evidence of habitual crutch usage,\n"
                f"    structural negligence, and a relationship with adverbs that can\n"
                f"    only be described as 'inappropriate.' By the end of these\n"
                f"    proceedings, you will understand why I have been losing sleep.\n",
                f"    PROSECUTOR: The evidence before you is not for the faint of heart.\n"
                f"    {wc:,} words. {sc} sentences. Each one a potential crime scene.\n\n"
                f"    I have spent more time with this text than with my own family\n"
                f"    this week, and I want you to know: I am not happy about that.\n"
                f"    My family is pleasant. This text is not. Let us begin.\n",
            ],
            'devastating': [
                f"    PROSECUTOR: [Adjusts tie. Takes a breath. Stares at the jury for\n"
                f"    eight full seconds.]\n\n"
                f"    Ladies and gentlemen. What I present to you is not bad writing.\n"
                f"    It is an EVENT. A {wc:,}-word catastrophe so thorough in its\n"
                f"    commitment to mediocrity that one almost has to admire the\n"
                f"    consistency.\n\n"
                f"    Almost.\n\n"
                f"    The prosecution will demonstrate that this text represents the\n"
                f"    kind of linguistic carelessness that would make Strunk AND White\n"
                f"    weep. Separately. In their respective graves. At the same time.\n",
            ]
        }

        lines.append(random.choice(openings.get(level, openings['moderate'])))

        if self.verbose:
            lines.append(self._random_tangent())

        return '\n'.join(lines)

    def generate_exhibits(self):
        lines = []
        lines.append("")
        lines.append("-" * 70)
        lines.append("    EXHIBITS OF EVIDENCE")
        lines.append("-" * 70)
        lines.append("")

        wc = self.a.word_count()
        if wc == 0:
            lines.append("    (No evidence to present — the text is empty.)")
            return '\n'.join(lines)

        # Exhibit A: Word Frequency
        top_words = self.a.word_frequency(10)
        if top_words:
            lines.append("    EXHIBIT A — MOST FREQUENT WORDS (excluding common function words)")
            lines.append("    " + "-" * 50)
            for word, count in top_words[:8]:
                bar = '█' * min(count, 30)
                lines.append(f"    {word:20s} {count:4d}  {bar}")
            lines.append("")

        if self.verbose and top_words:
            lines.append(self._random_tangent())

        # Exhibit B: Sentence Length Analysis
        lengths = self.a.sentence_lengths()
        if lengths:
            avg = self.a.average_sentence_length()
            var = self.a.sentence_variance()
            lines.append("    EXHIBIT B — SENTENCE STRUCTURE ANALYSIS")
            lines.append("    " + "-" * 50)
            lines.append(f"    Average sentence length:   {avg:.1f} words")
            lines.append(f"    Length variation (σ):      {var:.1f}")
            lines.append(f"    Shortest sentence:         {min(lengths)} words")
            lines.append(f"    Longest sentence:          {max(lengths)} words")

            if len(lengths) >= 5:
                buckets = {'1-5': 0, '6-10': 0, '11-15': 0, '16-20': 0,
                          '21-30': 0, '31+': 0}
                for l in lengths:
                    if l <= 5: buckets['1-5'] += 1
                    elif l <= 10: buckets['6-10'] += 1
                    elif l <= 15: buckets['11-15'] += 1
                    elif l <= 20: buckets['16-20'] += 1
                    elif l <= 30: buckets['21-30'] += 1
                    else: buckets['31+'] += 1
                lines.append(f"\n    Distribution:")
                for bucket, count in buckets.items():
                    if count > 0:
                        bar = '▓' * count
                        lines.append(f"    {bucket:6s}  {count:3d}  {bar}")
            lines.append("")

        if self.verbose:
            lines.append(self._random_tangent())

        # Exhibit C: Adverbs
        density, adverbs, unique = self.a.adverb_density()
        if adverbs:
            total_adverbs = sum(c for _, c in adverbs)
            lines.append("    EXHIBIT C — ADVERB INVESTIGATION")
            lines.append("    " + "-" * 50)
            lines.append(f"    Total -ly adverbs found:   {total_adverbs}")
            lines.append(f"    Unique adverbs:            {unique}")
            lines.append(f"    Adverb density:            {density:.4f} (per word)")
            lines.append(f"    Prosecutor's assessment:   {'CONCERNING' if density > 0.02 else 'TOLERABLE'}")
            lines.append("")
            if adverbs[:6]:
                lines.append("    Top offenders:")
                for adv, count in adverbs[:6]:
                    instances = self.a.find_instances_of(adv)
                    lines.append(f"      • \"{adv}\" — {count} occurrence(s)")
                    if instances:
                        lines.append(f"        Example: {instances[0]}")
            lines.append("")

        # Exhibit D: Hedge Language
        hedge_total, hedges = self.a.hedge_count()
        if hedges:
            lines.append("    EXHIBIT D — HEDGE LANGUAGE DETECTION")
            lines.append("    " + "-" * 50)
            lines.append(f"    Total hedge markers:       {hedge_total}")
            for hedge, count in hedges[:8]:
                instances = self.a.find_instances_of(hedge)
                lines.append(f"      • \"{hedge}\" — {count} occurrence(s)")
                if instances:
                    lines.append(f"        Example: {instances[0]}")
            lines.append("")

        if self.verbose:
            lines.append(self._random_tangent())

        # Exhibit E: Passive Voice
        passive_words, passive_total = self.a.passive_voice_instances()
        if passive_words:
            lines.append("    EXHIBIT E — PASSIVE VOICE CONSTRUCTION")
            lines.append("    " + "-" * 50)
            lines.append(f"    Passive constructions:     {passive_total}")
            for word, count in passive_words[:6]:
                lines.append(f"      • \"{word}\" (passive) — {count} occurrence(s)")
            lines.append("")

        # Exhibit F: Dialogue Tags
        tags = self.a.dialogue_tag_analysis()
        if tags:
            lines.append("    EXHIBIT F — DIALOGUE TAG ANALYSIS")
            lines.append("    " + "-" * 50)
            for tag, count in tags[:8]:
                lines.append(f"      • \"{tag}\" — {count} occurrence(s)")
            lines.append("")

        # Exhibit G: Crutch Phrases
        crutches = self.a.detect_crutch_phrases()
        if crutches:
            lines.append("    EXHIBIT G — REPEATED PHRASES")
            lines.append("    " + "-" * 50)
            for phrase, count in crutches[:6]:
                lines.append(f"      • \"{phrase}\" — {count} occurrence(s)")
            lines.append("")

        return '\n'.join(lines)

    def generate_cross_examination(self):
        lines = []
        lines.append("")
        lines.append("-" * 70)
        lines.append("    CROSS-EXAMINATION")
        lines.append("-" * 70)
        lines.append("")

        wc = self.a.word_count()
        if wc == 0:
            lines.append(
                "    PROSECUTOR: I have nothing to cross-examine. The witness has\n"
                "    provided no testimony. [Stares at empty page.]\n"
                "    ...That's haunting, isn't it?\n"
            )
            return '\n'.join(lines)

        # --- Adverb cross-examination ---
        density, adverbs, unique = self.a.adverb_density()
        if adverbs and adverbs[0][1] >= 3:
            top_adv, top_count = adverbs[0]
            lines.append(f"    PROSECUTOR: Let's talk about \"{top_adv}.\"")
            lines.append(f"    You used it {top_count} times. {top_count}. The same word.")
            if top_adv in ADVERB_SUSPECTS:
                lines.append("    A word the prosecution considers suspicious.")
            lines.append("")
            lines.append(
                "    Did you think the reader wouldn't notice? Did you think\n"
                f"    \"{top_adv}\" was invisible? That it would blend in like furniture?\n"
            )

            if top_count >= 6:
                lines.append("    Let me read them back to you:")
                instances = self.a.find_instances_of(top_adv)
                for inst in instances[:4]:
                    lines.append(f"    → \"{inst}\"")
                lines.append("")

            lines.append("    The jury will note the defendant's reliance on this crutch.\n")

            if self.verbose:
                lines.append(self._random_tangent())

        # --- Hedge language cross-examination ---
        hedge_total, hedges = self.a.hedge_count()
        if hedges and hedges[0][1] >= 2:
            top_hedge, h_count = hedges[0]
            lines.append(f"    PROSECUTOR: I draw your attention to \"{top_hedge}.\"")
            lines.append(f"    {h_count} times. One might argue this shows uncertainty.")
            lines.append(
                "    One might say the writer isn't committing to their own prose.\n"
                "    One MIGHT say many things. But the prosecution says it plainly:\n"
            )
            lines.append("    Pick a side. Mean what you say. Commit to the sentence.\n")
            if hedge_total > 5:
                lines.append(f"    The prosecution has catalogued {hedge_total} hedge markers total.")
                lines.append(
                    f"    That is {hedge_total} more than zero, which is the recommended amount.\n"
                )

        # --- Passive voice ---
        passive_words, passive_total = self.a.passive_voice_instances()
        if passive_total > 3:
            lines.append(
                "    PROSECUTOR: The jury's attention. Let us examine who is doing\n"
                "    things in this text. Or rather — who ISN'T doing things.\n"
            )
            lines.append(f"    I count {passive_total} passive voice constructions.\n")
            lines.append(
                "    The door was opened. By whom? The answer was given. By whom?\n"
                "    The body was moved. The sentence was weakened. The prose was\n"
                "    diminished — by the passive voice.\n"
            )
            if passive_words:
                lines.append(
                    f"    Consider: \"{passive_words[0][0]}\" — sitting there, avoiding\n"
                    "    responsibility, like a cat next to a broken vase.\n"
                )

        # --- Sentence monotony ---
        mono = self.a.monotonous_sentences()
        if mono:
            variance = self.a.sentence_variance()
            lines.append(
                "    PROSECUTOR: I'd like to discuss rhythm. The rhythm of your prose.\n"
            )
            lines.append(
                "    The prosecution has detected stretches where every sentence is\n"
                "    the same length. Sentence after sentence. Over and over. Like\n"
                "    a heartbeat that never changes. A drum that knows one beat.\n"
            )
            if variance < 4:
                lines.append(
                    f"    Your sentence-length variation is {variance:.1f}. Good prose\n"
                    "    varies like breathing — quick, then slow. Your prose breathes\n"
                    "    like a metronome. The jury notes this.\n"
                )

            if self.verbose:
                lines.append(self._random_tangent())

        # --- Word repetition ---
        top_words = self.a.word_frequency(5)
        if top_words and top_words[0][1] > max(5, wc * 0.02):
            word, count = top_words[0]
            lines.append(f"    PROSECUTOR: \"{word}.\" You return to it like a refrain.")
            lines.append(
                f"    {count} times, this word appears. The prosecution asks:\n"
                "    is this a motif, or is this a rut?\n"
            )

            # The unreliable narrator moment: sometimes defend it
            if count < wc * 0.05 and random.random() < 0.3:
                lines.append(
                    "    [The defense objects. The prosecutor waves a hand.]\n\n"
                    "    PROSECUTOR: I'll allow that thematic repetition exists. The word\n"
                    f"    \"{word}\" may serve a structural purpose. But the jury will\n"
                    "    decide whether this was artistry or accidental habit.\n"
                )

        # --- Dialogue tags (the prosecutor is suspicious of these) ---
        tags = self.a.dialogue_tag_analysis()
        if tags and tags[0][1] > 5:
            top_tag, t_count = tags[0]
            lines.append(
                "    PROSECUTOR: Now. Let's discuss dialogue. Specifically, how you\n"
                f"    choose to attribute it. \"{top_tag}\" — {t_count} times.\n"
            )

            if top_tag == 'said':
                lines.append(
                    "    The prosecution concedes that 'said' is the invisible tag.\n"
                    "    The prosecution ALSO notes that using it dozens of times makes\n"
                    "    it significantly less invisible. Like a man wearing camouflage\n"
                    "    standing next to forty other men in the same camouflage. You\n"
                    "    all blend together into a green mass of 'said.'\n"
                )
            elif top_tag == 'asked':
                lines.append(
                    "    'Asked.' The prosecution notes that questions can be identified\n"
                    "    by the question mark. The reader is not confused about whether\n"
                    "    a question is a question. The jury considers this redundant.\n"
                )
            else:
                lines.append(
                    f"    '{top_tag}.' The prosecution is suspicious of colorful dialogue\n"
                    "    tags. They draw attention to the delivery mechanism instead of\n"
                    "    the dialogue itself. Let the words carry the emotion. Or —\n"
                    "    here's a thought — let the reader figure it out.\n"
                )

            if self.verbose:
                lines.append(self._random_tangent())

        # --- Crutch phrases ---
        crutches = self.a.detect_crutch_phrases()
        if crutches and crutches[0][1] >= 4:
            phrase, c_count = crutches[0]
            lines.append(f"    PROSECUTOR: The phrase \"{phrase}\" — {c_count} times.")
            lines.append(f"    Three or more is a pattern. {c_count} is a lifestyle.\n")

        return '\n'.join(lines)

    def generate_defense(self):
        lines = []
        lines.append("")
        lines.append("-" * 70)
        lines.append("    THE PROSECUTION SURPRISINGLY ACKNOWLEDGES MERIT")
        lines.append("    (The prosecutor would like this section stricken from the record)")
        lines.append("-" * 70)
        lines.append("")

        if not self.defenses:
            # Mercy trigger: ~15% chance of finding something nice anyway
            if random.random() < 0.15:
                lines.append(
                    "    PROSECUTOR: [Very long pause. Looking at notes. Looking at ceiling.]\n"
                    "    The prosecution... has reviewed the text for passages of merit.\n"
                    "    [Another pause. Shuffling papers.]\n\n"
                    "    Fine. FINE. The prosecution concedes that the text exists. That\n"
                    "    it was completed. That someone, somewhere, might read it and not\n"
                    "    die. This is not nothing. The jury will note this.\n"
                )
            else:
                lines.append(
                    "    PROSECUTOR: The prosecution has reviewed the text for passages of\n"
                    "    merit. [Long pause.] The prosecution's review is complete.\n\n"
                    "    [Whispered, off-mic:] There was a decent sentence, but I'll deny it.\n"
                )
            return '\n'.join(lines)

        lines.append(
            "    PROSECUTOR: [Through gritted teeth] The prosecution is obligated\n"
            "    to note... certain... passages that are, against all odds,\n"
            "    effective.\n"
        )

        for passage, p_type in self.defenses:
            if p_type == 'short_declarative':
                lines.append(f"    \"{passage}\"")
                lines.append("")
                lines.append(
                    "    [The prosecutor sighs.]\n"
                    "    That is a clean sentence. Short. Direct. No adverbs, no hedging,\n"
                    "    no passive voice. The prosecution hates to admit it, but that\n"
                    "    sentence has backbone. The jury will note the contrast with\n"
                    "    the rest of the text.\n"
                )
            elif p_type == 'specific':
                lines.append(f"    \"{passage}\"")
                lines.append("")
                lines.append(
                    "    Specific. Concrete. The prosecution notes this with grudging\n"
                    "    respect. When you reach for precision, you grasp it. Imagine\n"
                    "    what the whole text could be if you reached more often.\n"
                    "    But I digress. The prosecution was not complimenting you.\n"
                )

        if self.verbose:
            lines.append(self._random_tangent())

        return '\n'.join(lines)

    def generate_closing(self):
        lines = []
        lines.append("")
        lines.append("-" * 70)
        lines.append("    CLOSING ARGUMENTS")
        lines.append("-" * 70)
        lines.append("")

        wc = self.a.word_count()
        level = self._intensity_level()

        if wc == 0:
            lines.append(
                "    PROSECUTOR: There is nothing to close. The case speaks for itself.\n"
                "    Or rather, it doesn't. Because it's empty. Like this text.\n"
            )
            return '\n'.join(lines)

        closings = {
            'gentle': [
                "    PROSECUTOR: In conclusion, the prosecution does not hate this text.\n"
                "    We are not enemies of the defendant. We are disappointed friends.\n"
                "    The kind who want you to do better, who see what you're capable\n"
                "    of, and who will not pretend that this draft is final.\n\n"
                "    Fix the adverbs. Vary the sentences. Commit to your verbs.\n"
                "    The prosecution rests, confident that revision is possible.\n",
                "    PROSECUTOR: Let me be clear: this is not the worst text the court\n"
                "    has seen. Not by a wide margin. But 'not the worst' is a low bar,\n"
                "    and the prosecution believes the defendant can clear higher.\n\n"
                "    The evidence has been presented. The crutches catalogued. The\n"
                "    sentence now rests with the jury — and with the writer.\n",
            ],
            'moderate': [
                "    PROSECUTOR: The evidence speaks for itself. And what it says is:\n"
                "    this text needed one more draft. Maybe two. The patterns are clear,\n"
                "    the crutches documented, and the verdict is obvious.\n\n"
                "    The prosecution asks the jury to find the defendant guilty of\n"
                "    habitual mediocrity, with the recommendation of revision.\n",
                "    PROSECUTOR: I have presented the evidence. The adverbs. The hedging.\n"
                "    The passive constructions. The repetitive phrases. The jury has\n"
                "    seen all of it.\n\n"
                "    And to the defendant: you can do better. The prosecution knows\n"
                "    this because, occasionally — briefly — you DID do better.\n"
                "    Build on that.\n",
            ],
            'severe': [
                "    PROSECUTOR: Ladies and gentlemen, what we have here is a text that\n"
                "    wandered into the courtroom of prose and forgot to bring its case.\n"
                "    The evidence has been damning. The adverbs were excessive. The\n"
                "    hedge language was cowardly. The passive voice was — fittingly —\n"
                "    passive.\n\n"
                "    The prosecution asks for the maximum sentence: a complete rewrite,\n"
                "    from scratch, with the lessons of this trial in mind.\n",
            ],
            'devastating': [
                "    PROSECUTOR: [Standing. Both hands on the podium. Leaning forward.]\n\n"
                "    This text. This... document. This collection of words that someone,\n"
                "    somewhere, thought was ready for human consumption. The prosecution\n"
                "    has shown you its crimes. The adverbs. The hedging. The passivity.\n"
                "    The repetition. The structural monotony. The commitment to telling\n"
                "    rather than showing.\n\n"
                "    The prosecution asks the jury for the harshest sentence: burning\n"
                "    the draft and starting over. Not because the defendant cannot\n"
                "    write — but because they CAN, and chose not to. That is the crime.\n\n"
                "    The prosecution rests. [Sits down. Stands back up.]\n"
                "    And one more thing: stop using 'suddenly.' Good day.\n"
                "    [Sits down again.]\n",
            ]
        }

        lines.append(random.choice(closings.get(level, closings['moderate'])))

        if self.verbose:
            lines.append(self._random_tangent())

        return '\n'.join(lines)

    def generate_verdict(self):
        lines = []
        lines.append("")
        lines.append("=" * 70)
        lines.append("                          THE VERDICT")
        lines.append("=" * 70)
        lines.append("")

        wc = self.a.word_count()
        level = self._intensity_level()

        if wc == 0:
            lines.append("    VERDICT:    GUILTY — of existing while empty")
            lines.append("    SENTENCE:   Write something. Anything. Try again.")
            lines.append("")
            lines.append("=" * 70)
            lines.append("                    END OF PROCEEDINGS")
            lines.append("=" * 70)
            return '\n'.join(lines), 1

        verdicts = {
            'gentle': ("PROVISIONALLY ACCEPTABLE", "With reservations"),
            'moderate': ("GUILTY OF MEDIOCRITY", "First-degree"),
            'severe': ("GUILTY OF PROSE ABUSE", "Second-degree (habitual)"),
            'devastating': ("GUILTY ON ALL COUNTS", "Maximum severity"),
        }

        verdict_text, severity = verdicts.get(level, verdicts['moderate'])
        lines.append(f"    VERDICT:    {verdict_text}")
        lines.append(f"    SEVERITY:   {severity}")
        lines.append(f"    SCORE:      {self.severity:.1f} / 15.0")
        lines.append("")

        # Specific findings
        lines.append("    SPECIFIC FINDINGS:")
        lines.append("    " + "-" * 50)

        findings = []
        density, adverbs, unique = self.a.adverb_density()
        if adverbs and adverbs[0][1] >= 3:
            findings.append(f"    • Adverb overuse: \"{adverbs[0][0]}\" ({adverbs[0][1]} times)")

        hedge_total, hedges = self.a.hedge_count()
        if hedges and hedges[0][1] >= 2:
            findings.append(f"    • Hedge language: \"{hedges[0][0]}\" ({hedges[0][1]} instances)")

        passive_words, passive_total = self.a.passive_voice_instances()
        if passive_total > 3:
            findings.append(f"    • Passive voice: {passive_total} constructions")

        variance = self.a.sentence_variance()
        if variance < 3.0 and self.a.sentence_count() > 8:
            findings.append(f"    • Sentence monotony: variation σ={variance:.1f}")

        tags = self.a.dialogue_tag_analysis()
        if tags and tags[0][1] > 5:
            findings.append(f"    • Dialogue tag repetition: \"{tags[0][0]}\" ({tags[0][1]} times)")

        crutches = self.a.detect_crutch_phrases()
        if crutches and crutches[0][1] >= 3:
            findings.append(f"    • Repeated phrase: \"{crutches[0][0]}\" ({crutches[0][1]} times)")

        diversity = self.a.lexical_diversity()
        if diversity < 0.3 and wc > 100:
            findings.append(f"    • Low lexical diversity: {diversity:.3f}")

        top_words = self.a.word_frequency(5)
        if top_words and top_words[0][1] > max(5, wc * 0.02):
            findings.append(f"    • Word overuse: \"{top_words[0][0]}\" ({top_words[0][1]} times)")

        if findings:
            for f in findings:
                lines.append(f)
        else:
            lines.append("    • (No major findings — the text is clean)")

        lines.append("")

        # Sentencing
        lines.append("-" * 70)
        lines.append("    SENTENCING REPORT")
        lines.append("-" * 70)
        lines.append("")

        sentences_by_severity = {
            'gentle': [
                "    The court recommends a light revision pass. Address the flagged\n"
                "    items at your leisure. The prosecution suggests a good night's\n"
                "    sleep and a fresh read-through in the morning.\n\n"
                "    You're fine. Mostly fine. Fine enough.\n",
                "    The defendant is sentenced to one (1) careful revision pass and\n"
                "    a stern talking-to about adverb usage. The prosecution believes\n"
                "    rehabilitation is likely.\n",
            ],
            'moderate': [
                "    The defendant is sentenced to two (2) thorough revision passes,\n"
                "    one (1) reading aloud to a critical friend, and mandatory removal\n"
                "    of all flagged hedge language. The court recommends a thesaurus\n"
                "    for any word appearing more than ten times.\n",
                "    The court orders the following:\n"
                "    1. Identify every flagged crutch and reduce occurrences by 50%.\n"
                "    2. Vary sentence lengths. Deliberately.\n"
                "    3. Convert passive constructions to active voice where possible.\n"
                "    4. Report back to this court in one week with a revised draft.\n",
            ],
            'severe': [
                "    The defendant is sentenced to the following:\n"
                "    1. A structural review of every paragraph.\n"
                "    2. Removal of all unnecessary adverbs (hint: most of them).\n"
                "    3. Conversion of passive voice to active voice — mandatory.\n"
                "    4. Sentence length variation exercises: write three paragraphs,\n"
                "       each with sentences of different lengths.\n"
                "    5. A sincere apology to the English language.\n\n"
                "    The court recommends putting the text in a drawer for one week\n"
                "    before revising. Distance brings clarity.\n",
            ],
            'devastating': [
                "    The defendant is sentenced to the MAXIMUM penalty:\n\n"
                "    1. IMMEDIATE cessation of all writing until the following\n"
                "       conditions are met:\n"
                "       a) Read one book on prose style (the court recommends\n"
                "          'The Elements of Style' or 'On Writing').\n"
                "       b) Complete three exercises focused on active voice,\n"
                "          sentence variety, and precision of language.\n\n"
                "    2. Upon resuming work on this text:\n"
                "       a) Rewrite every flagged passage from scratch.\n"
                "       b) Reduce adverb count by 80%.\n"
                "       c) Eliminate all hedge language.\n"
                "       d) Vary sentence lengths with INTENT.\n\n"
                "    3. The defendant is ordered to read the revised text aloud.\n"
                "       If it sounds monotonous, start over.\n\n"
                "    The prosecution recognizes this is harsh. The prosecution does\n"
                "    not care. The text deserves better. Write accordingly.\n",
            ]
        }

        lines.append(random.choice(
            sentences_by_severity.get(level, sentences_by_severity['moderate'])
        ))

        lines.append("=" * 70)
        lines.append("                    END OF PROCEEDINGS")
        lines.append("=" * 70)

        # Exit code: 0 for acquitted (gentle), 1 for guilty, 2 for verbose
        exit_code = 0 if level == 'gentle' else 1
        if self.verbose:
            exit_code = 2

        return '\n'.join(lines), exit_code

    def generate_full_report(self):
        report = []
        report.append(self.generate_opening())
        report.append(self.generate_exhibits())
        report.append(self.generate_cross_examination())
        report.append(self.generate_defense())
        report.append(self.generate_closing())
        verdict_text, exit_code = self.generate_verdict()
        report.append(verdict_text)
        return '\n'.join(report), exit_code


# ============================================================================
# PART 3: Command Line Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Witness Stand — Cross-examine your writing.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python witness_stand.py manuscript.txt
  python witness_stand.py story.txt --verbose
  python witness_stand.py draft.md

The prosecutor analyzes your text, identifies crutches and patterns,
and delivers a theatrical cross-examination. The --verbose flag makes
the prosecutor lose focus and question itself.

Exit codes: 0 = acquitted, 1 = guilty, 2 = the court lost focus (--verbose)
"""
    )
    parser.add_argument('file', help='Path to the text file to analyze')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Make the prosecutor verbose and distracted')
    parser.add_argument('--output', '-o', help='Write report to file instead of stdout')

    args = parser.parse_args()

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.", file=sys.stderr)
        print("The prosecutor cannot cross-examine a document that doesn't exist.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        print("The court finds this file in contempt.", file=sys.stderr)
        sys.exit(1)

    if not text.strip():
        print("Warning: The file appears to be empty.", file=sys.stderr)
        print("The prosecutor will have strong opinions about this.", file=sys.stderr)

    analysis = AnalysisEngine(text)

    import os
    filename = os.path.basename(args.file)
    prosecutor = Prosecutor(analysis, verbose=args.verbose, filename=filename)
    report, exit_code = prosecutor.generate_full_report()

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report written to '{args.output}'", file=sys.stderr)
        except IOError as e:
            print(f"Error writing report: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(report)

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
