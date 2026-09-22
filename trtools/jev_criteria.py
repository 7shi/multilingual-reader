"""What `trtools jev` asks Jev, and the identifier that pins it.

The five criteria are `trtools/evaluate.py`'s field descriptions verbatim: the corpus
changed how a judgment is asked for, not what is being asked, so a rewording here would
silently make new scores incomparable with the ones already collected.

The five levels say only HOW MUCH of the document falls short of a criterion, never what
kind of defect is responsible. That is deliberate, and experiment 12's README section 3
records what the alternative cost: a rubric naming concrete defects at the bottom of the
scale and vague absolutes at the top pulled probability toward whichever wording could be
matched against the text, to the point where a structurally sound Polish translation
landed on "mixed languages, markup fragments" at probability 0.87.

Everything in this file is an input to the score. `SCHEME_ID` hashes all of it, and
experimental/13/PORT.md section 3 says why that matters and section 8 what it is checked
against.
"""

import hashlib

from typesafe_sdk import Score

# key -> (heading used in reports, description shown to the evaluator)
CRITERIA = {
    "readability": (
        "Readability & comprehensibility",
        "Whether target language readers can easily understand the content, whether "
        "complex concepts are explained clearly, and whether the sentence structure is "
        "logical and easy to follow",
    ),
    "fluency": (
        "Fluency & naturalness",
        "Whether the translated text sounds natural and smooth to native speakers of "
        "the target language, whether there are unnatural expressions or awkward "
        "grammar, and whether vocabulary choices are appropriate and contemporary",
    ),
    "terminology": (
        "Terminology appropriateness",
        "Whether technical terms are appropriately handled according to the reader's "
        "understanding level, whether explanations or paraphrases are provided when "
        "necessary, and whether term selection is consistent",
    ),
    "contextual_adaptation": (
        "Contextual adaptation",
        "Whether the original text's intent and purpose are effectively conveyed, "
        "whether expressions consider the target readers' cultural background, and "
        "whether expressions are improved or optimized as needed",
    ),
    "information_completeness": (
        "Information completeness",
        "Whether important information from the original text is conveyed without "
        "omission, whether appropriate supplements are provided to aid reader "
        "understanding, and whether redundancy is eliminated while keeping the content "
        "concise and clear",
    ),
}

CRITERION_IDS = list(CRITERIA)

# The name the corpus records alongside the hash. Experiment 13 scored a second wording
# ("bands") as a control; production runs one rubric, and the name survives so a file
# says which family it belongs to rather than only that it differs.
LEVEL_SET = "degrees"

LEVELS = [
    "The criterion is not met anywhere in the translation: it fails over the whole "
    "document, or there is no usable target-language text to judge against it.",
    "The criterion fails across most of the translation, over far more than a handful "
    "of lines.",
    "The criterion fails repeatedly, or across a wide part of the translation: roughly "
    "four lines or more, or a single occurrence whose effect spreads through the whole "
    "text.",
    "The criterion is mostly met. The places where it falls short are scattered and "
    "confined to roughly one to three lines.",
    "The criterion is met throughout the translation; not a single place where it falls "
    "short.",
]

# The two questions every criterion shares. Only `criterion` changes between them.
JUDGE = ("How well does `translation` meet the criterion below, read against `original`?")
SCOPE = ("Judge this criterion alone, over the whole document. The other four are asked "
         "about by their own questions.")

# Points per level on the old 0-20 scale. `jev.jsonl` stores levels, not points; this is
# what a report multiplies by when it wants the scale SCORES.txt has always used.
POINTS_PER_LEVEL = 5.0


def build_state(original_text, translated_text, from_lang, to_lang):
    """Named JSON state: both texts plus the facts every criterion is judged against."""
    n_lines = original_text.count("\n") + 1
    return {
        "task": f"Quality evaluation of a dialogue transcript translated from "
                f"{from_lang} into {to_lang}",
        "source_language": from_lang,
        "target_language": to_lang,
        "line_correspondence": f"Both texts have {n_lines} lines, and line i of the "
                               f"translation is meant to render line i of the original.",
        "original": original_text,
        "translation": translated_text,
    }


def build_questions():
    """One Score per criterion, all sharing the same five severity levels."""
    return {
        key: Score(
            instructions={"judge": JUDGE, "criterion": description, "scope": SCOPE},
            criteria=LEVELS,
        )
        for key, (_, description) in CRITERIA.items()
    }


def scheme_id():
    """`<level set>@<8 hex>` over everything that determines a score.

    The level texts alone would not do. What the model is asked is the instructions --
    `judge`, the per-criterion description, `scope` -- and what it is asked about is
    `build_state`'s named keys; any of those can be reworded without touching LEVELS, and
    the scores would move with nothing in the data to show it.

    Only strings are hashed, never a serialised SDK object, so a change in typesafe_sdk's
    model shape cannot invalidate results already on disk.
    """
    parts = []
    for key, (_, description) in CRITERIA.items():
        parts += [key, JUDGE, description, SCOPE]
    parts += LEVELS
    # Key order, not the values: the values are per-language text.
    parts += list(build_state("", "", "English", "Japanese"))
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()
    return f"{LEVEL_SET}@{digest[:8]}"


SCHEME_ID = scheme_id()

assert len(CRITERIA) == 5, f"expected 5 criteria, got {len(CRITERIA)}"
assert len(LEVELS) == 5, f"expected 5 levels, got {len(LEVELS)}"
assert POINTS_PER_LEVEL * (len(LEVELS) - 1) == 20
