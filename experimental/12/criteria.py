"""The old scheme's 5 criteria and the severity levels they are scored on.

The criterion descriptions are `trtools/evaluate.py`'s field descriptions verbatim, and
the levels are that script's CRITICAL GUIDELINES 3-6 turned into an ordered rubric. Both
are copied deliberately rather than improved: this experiment changes how the judgment is
asked for, not what is being asked, so anything reworded here would confound the result.

The one thing the old prompt has and this does not is its guideline 1, "if missing or
incomplete, assign 0 points to ALL criteria". That is the score cliff experiment 11's
background blames for 0/100 scores beside enthusiastic rationales, and it cannot be
expressed as a per-criterion level anyway. Level 0 covers the same situation without
propagating it across criteria.
"""

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

# Ascending severity bands, from the old prompt's guidelines. Five levels rather than
# twenty-one: a Score's levels have to describe situations that can be told apart, and
# "what separates 14 from 17" is precisely the question the old rubric could not answer.
# The distance between levels is recovered from the probability distribution instead.
LEVELS = [
    "The translation is missing or empty, or the text is not in the target language at "
    "all, so this criterion cannot be met.",
    "Critical failure on this criterion: the text is structurally damaged, with mixed "
    "languages, JSON or markup fragments, or meta-commentary left in the body.",
    "Major failure on this criterion: defects a reader stumbles over repeatedly, such "
    "as grammatical errors or passages left untranslated.",
    "Minor issues on this criterion only: occasional awkwardness, nothing that obscures "
    "the content.",
    "No fault on this criterion: natural and accurate throughout.",
]

# Points per level on the old 0-20 scale. The old prompt's bands were 0-5 for a critical
# failure, 6-12 major, 13-17 minor and 18-20 clean, so level i lands at the top of band i
# and within a point of the middle of the two bands that have one.
POINTS_PER_LEVEL = 20 / (len(LEVELS) - 1)

assert len(CRITERIA) == 5, f"expected 5 criteria, got {len(CRITERIA)}"
assert len(LEVELS) == 5, f"expected 5 levels, got {len(LEVELS)}"
assert POINTS_PER_LEVEL == 5
