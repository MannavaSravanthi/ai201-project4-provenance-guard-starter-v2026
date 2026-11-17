"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ───────────────────────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    Coefficient of variation of sentence length (stdev / mean, in words).

    Scale: 0 and up. ~0.2 means sentences march in step; 0.6+ means a short
    sentence sits next to a long one. Higher = more human.

    Edge case: fewer than two sentences has no spread. Returns 0.0, which
    style_signal treats as "no evidence" rather than "very AI" (see there).
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean if mean else 0.0


def type_token_ratio(text: str) -> float:
    """
    Unique words / total words, measured over a moving 50-word window and
    averaged (MATTR), so long and short texts are comparable.

    Scale: 0–1. Higher = more varied vocabulary = more human.
    """
    toks = words(text)
    if not toks:
        return 0.0
    window = 50
    if len(toks) <= window:
        return len(set(toks)) / len(toks)
    ratios = [len(set(toks[i:i + window])) / window
              for i in range(len(toks) - window + 1)]
    return statistics.mean(ratios)


def punctuation_density(text: str) -> float:
    """
    "Expressive" punctuation per 100 words: ; : — – ( ) ! ? ... and quotes.
    Full stops and commas are left out — every writer uses them.

    Scale: 0 and up, typically 0–10. Higher = more varied = more human.
    """
    n_words = len(words(text))
    if n_words == 0:
        return 0.0
    marks = re.findall(r"[;:!?()\"\u2014\u2013\u201c\u201d]|\.\.\.|--| - ", text)
    return 100.0 * len(marks) / n_words


# ── Combining them ───────────────────────────────────────────────────────────

# Each measure is mapped to a 0–1 "human-ness" with a linear ramp between a
# value that looks clearly AI (-> 0) and one that looks clearly human (-> 1).
# These anchor points are my calibration choices — see README.
SPREAD_AI, SPREAD_HUMAN = 0.25, 0.65
TTR_AI, TTR_HUMAN = 0.70, 0.85
PUNCT_AI, PUNCT_HUMAN = 0.5, 5.0

W_SPREAD, W_TTR, W_PUNCT = 0.45, 0.30, 0.25


def _ramp(value: float, ai_end: float, human_end: float) -> float:
    """0 at ai_end, 1 at human_end, clipped."""
    t = (value - ai_end) / (human_end - ai_end)
    return min(max(t, 0.0), 1.0)


def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    All three measures point "higher = more human", so each is ramped to a
    0–1 human-ness, weighted (spread 0.45, vocabulary 0.30, punctuation 0.25),
    and flipped: style = 1 - human-ness.

    With fewer than two sentences there is no spread to measure, so that
    weight is dropped and the other two are renormalised instead of letting
    a missing measure count as evidence of AI.
    """
    parts = []
    if len(sentences(text)) >= 2:
        parts.append((W_SPREAD, _ramp(sentence_length_spread(text), SPREAD_AI, SPREAD_HUMAN)))
    parts.append((W_TTR, _ramp(type_token_ratio(text), TTR_AI, TTR_HUMAN)))
    parts.append((W_PUNCT, _ramp(punctuation_density(text), PUNCT_AI, PUNCT_HUMAN)))
    total_w = sum(w for w, _ in parts)
    humanness = sum(w * h for w, h in parts) / total_w
    return round(1.0 - humanness, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
