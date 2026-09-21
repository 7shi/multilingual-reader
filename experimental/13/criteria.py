"""The old scheme's 5 criteria, and the two wordings of the levels they are scored on.

A copy of experiment 12's criteria.py, frozen at the revision this experiment was run on.
Experiment 12 is a finished record rather than a library, and its levels are the variable
that experiment tested, so sharing the file would let a later edit there silently change
what the results in evals-degrees/ claim to mean. Diff the two before assuming they agree.

The criterion descriptions are `trtools/evaluate.py`'s field descriptions verbatim: this
experiment changes how the judgment is asked for, not what is being asked, so anything
reworded there would confound the result.

The levels are a variable. The first run of this experiment turned the old prompt's
CRITICAL GUIDELINES 3-6 into the rubric directly, and experiment 12's README section 3
records what
that produced: the clean level never won once across 120 judgments, and a structurally
sound Polish translation landed on "mixed languages, markup fragments" at probability
0.87. The guidelines name concrete defects at the bottom of the scale and state vague
absolutes at the top, so probability was pulled toward whichever wording could be matched
against the text; and the defect taxonomy they name is structural, which is not what three
of the five criteria are asking about.

Both wordings are therefore kept and selectable (`--levels`), because the claim they test
together -- that how specifically a Score level is worded moves its probability mass -- is
about the primitive rather than about this rubric, and a control that cannot be re-run is
not a control. They differ in nothing but the level text.

The one thing the old prompt has and neither set carries is its guideline 1, "if missing
or incomplete, assign 0 points to ALL criteria". That is the score cliff experiment 11's
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

# Two wordings of the same five ascending severity levels, selectable so that either can
# be re-run rather than only one of them being reproducible. Five levels rather than
# twenty-one in both: a Score's levels have to describe situations that can be told
# apart, and "what separates 14 from 17" is precisely the question the old rubric could
# not answer. The distance between levels is recovered from the probability distribution
# instead.
#
# What differs between the two is only how a level is described, which is what makes the
# pair a controlled test of a general property of the primitive. Each set has five levels
# in the same order and the same point mapping, so their scores are on one scale.
LEVEL_SETS = {}

# The replacement, and the default. Each level says only HOW MUCH of the document falls
# short of the criterion, never what kind of defect is responsible. That is the one
# property experiment 11's working anchor has and the old prompt's guidelines do not:
# `no`/`partial`/`yes` are degrees, identical across all 50 items, and pinned to line
# counts rather than defect kinds. Levels 2, 3 and 4 here are that anchor transplanted --
# eval50_jev.py's standalone phrasing of eval50.py's ANCHOR, with "the property" widened
# to "the criterion" -- and levels 0 and 1 extend the same ladder downward to cover the
# old prompt's critical band. Keeping the middle three verbatim means a run of this set
# also says whether the anchor carries across rubrics.
#
# Level 0 does not name missing or empty text, though the banded set does: a translation
# that is not there fails every criterion everywhere, which is what "not met anywhere"
# already says, and naming the case would put a defect kind back at the bottom of the
# scale.
LEVEL_SETS["degrees"] = [
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

# The original set, whose results are in `evals/`: the old prompt's CRITICAL GUIDELINES
# 3-6 turned into an ordered rubric, kept so the control can be re-run rather than only
# read off disk. Its severity
# ordering is the one the degree set preserves; what it additionally carries is the
# guidelines' defect taxonomy, and experiment 12's README section 3 records what that
# costs.
LEVEL_SETS["bands"] = [
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

DEFAULT_LEVEL_SET = "degrees"
# The result directory each set writes to by default, so a run cannot quietly mix the two
# wordings in one directory. The banded set keeps `evals/`, the name its results were
# written under before there was anything to distinguish them from; the degree set, being
# the newer of the two, is the one that takes a qualified name.
EVAL_DIRS = {"bands": "evals", "degrees": "evals-degrees"}

# Points per level on the old 0-20 scale. The banded set's own bands were 0-5 for a
# critical failure, 6-12 major, 13-17 minor and 18-20 clean, so an even split puts each
# level at the top of its band and within a point of the middle of the two bands wide
# enough to have one. The degree set states no bands, and an even split is the only
# mapping its wording supports; landing in the same place is what keeps `evals/` and
# `evals-degrees/` comparable.
POINTS_PER_LEVEL = 5.0

assert len(CRITERIA) == 5, f"expected 5 criteria, got {len(CRITERIA)}"
assert set(LEVEL_SETS) == set(EVAL_DIRS), "every level set needs a result directory"
assert DEFAULT_LEVEL_SET in LEVEL_SETS
for _name, _levels in LEVEL_SETS.items():
    assert len(_levels) == 5, f"expected 5 levels in {_name}, got {len(_levels)}"
    assert POINTS_PER_LEVEL * (len(_levels) - 1) == 20
