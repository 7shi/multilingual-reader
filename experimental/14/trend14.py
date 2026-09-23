#!/usr/bin/env python3
"""Experiment 14: the trend column's prose, written from the translation.

README.md is what this is for. In short: `trtools trend` builds each language's one-line
`analysis` by summarising three generative evaluations' `overall_comment`, and Jev returns
no prose, so under the new evaluator that column has no source. The replacement writes the
phrase from the translation itself, with Jev's per-criterion breakdown steering what the
writer looks for rather than appearing in the output.

What steers it is **the level of the weakest criterion**, read back in the rubric's own
terms -- how much of the document falls short. This is the part a writer cannot infer from
the text alone, and it is what keeps the phrase on the same scale as the score without
asking the writer to be measured about it.

What the phrase *is* changed at run 7. Runs 1-6 asked for the lines that fall short and
what is wrong with them, and every failure they found was a failure at pointing. The column
being replaced never pointed: 1,072 entries, median five words, a quotation mark in 2% of
them and a line number in none. It is `<severity> <kind of defect>` about the translation
as a whole, and the severity is what the level supplies. That is the default here; runs 1-6
are behind --locate.

A second axis was tried and dropped: pointing the writer at whichever criteria sit below
the record's own mean. It changed nothing that two runs of the same prompt did not change
by more, including over FOCUS_TARGETS, the set built to give it its best chance. PLAN.md
sections 3 and 4 are the comparison. `--axis-b` still switches it on, since a rejection nothing can
reproduce is not worth much.

Nothing is written to examples/. This prints the phrase beside the one currently in
TRENDS.jsonl, which is the comparison the wording is judged on; -o also appends them to a
JSONL for diffing two wordings against each other.

    uv run experimental/14/trend14.py
    uv run experimental/14/trend14.py gpt-oss/sv qwen3.6/he
    uv run experimental/14/trend14.py --focus-targets -o focus.jsonl
    uv run experimental/14/trend14.py --locate --show-prompt
"""

import argparse
import json
import statistics
from pathlib import Path

from llm7shi.usage import Usage, append_usage, print_today_totals

from trtools.jev_criteria import CRITERIA, CRITERION_IDS, LEVELS, POINTS_PER_LEVEL
from trtools.language import LANGUAGES
from trtools.llm import LLMClient, init_usage_path
from trtools.trend import _clean, _matches_lang

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
ONDE = REPO_ROOT / "examples" / "tr" / "onde"
ORIGINAL = REPO_ROOT / "examples" / "onde-en.txt"

DEFAULT_MODEL = "ollama:qwen3.6"


# ---------------------------------------------------------------------------
# The wording under test. Everything below this line is the experiment.
# ---------------------------------------------------------------------------

# How far below the record's own mean a criterion has to sit to become the focus. 0.3
# levels puts a focus on 778 of the corpus's 1,072 records; 0.5 puts one on 231.
FOCUS_THRESHOLD = 0.3

# Axis A. One per level of the weakest criterion, saying how much of the document the
# evaluator found falling short -- LEVELS restated as an instruction to a writer.
# Corpus counts: level 3 is 625 of 1,072 records and level 4 only 12. An earlier level-3
# wording forbade answering with a general assessment, and PLAN.md section 4 is the four
# false claims that produced on a translation with nothing to find. Reporting soundness is
# permitted; inventing a defect is what is forbidden in its place.
LEVEL_INSTRUCTIONS = {
    4: "The evaluation found nothing in this translation that falls short. Do not invent "
       "a defect. State briefly what it does well.",
    3: "The evaluation found that one to three lines fall short, and that the rest of the "
       "translation is sound. Find those lines and say concretely what is wrong with "
       "them. If you cannot locate the shortfall, say that the translation reads as "
       "sound -- that is a valid answer. What is not an answer is a defect you did not "
       "find in the text.",
    2: "The evaluation found that four or more lines fall short, or that one problem "
       "spreads through the whole text. Say what recurs, not where it happens once.",
    1: "The evaluation found that most of the translation falls short. Say what is wrong "
       "throughout it rather than naming a single place.",
    0: "The evaluation found nothing in this translation that meets its criteria, and "
       "there may be no usable target-language text at all. Say what the text actually "
       "is.",
}

# Level 3 is 632 records whose weakest criterion runs from 2.50 to 3.49, and rounding
# throws away the part that matters: every fabricated phrase in runs 1-4 came from a record
# in the band's top tenth, whose 90th percentile is 3.28. Above this the instruction says
# what the number supports rather than asserting lines that may not be there.
LEVEL_3_SLIGHT_MIN = 3.3

LEVEL_3_SLIGHT = ("The evaluation found this translation almost entirely sound. What falls "
                  "short of the criteria is slight -- a shade of wording rather than "
                  "anything necessarily visible as a mistake -- so there may be nothing "
                  "you can point at. Look for it; if you find something, name it from the "
                  "text. If you do not, say that the translation reads as sound. Do not "
                  "manufacture a defect to fill the answer.")

# A stronger form of the branch above, for --sound-rule. Run 5 put the slight wording in
# front of eleven records and got a named defect in all 22 phrases and "reads as sound" in
# none, so the permission as worded is not reaching the writer at all.
LEVEL_3_SLIGHT_STRONG = ("The evaluation found this translation almost entirely sound. At "
                         "this level most translations have no defect a reader can point "
                         "at, and saying that it reads as sound is the ordinary answer. "
                         "Name something only if you can quote it from the text and say "
                         "what is wrong with it. A doubt about word choice that you cannot "
                         "defend from the text is not a finding, and a defect invented to "
                         "fill the answer is worse than no answer.")

# Run 5's new failure: the writer renders the translation back into English and judges the
# rendering -- "psi in squares" for a correct пси в квадрате, "unity of fiziky", "Naruhodo"
# for なるほど. For --backtrans-rule.
BACKTRANS_RULE = ("IMPORTANT: Judge the translation in its own language. Do not render it "
                  "back into English and then judge the rendering: a correct translation "
                  "often reads oddly word for word in English, and that is not a defect.")

# Run 5 also quoted strings that are not in either file, usually because the quotes hold a
# correction rather than the text. Separating the two is what would let a quoted string be
# checked against the files mechanically. For --quote-rule.
QUOTE_RULE = ("IMPORTANT: Put inside quotation marks only text that occurs in the "
              "translation or in the original, copied exactly as it appears there. A "
              "correction, a suggested alternative or a gloss goes outside the quotation "
              "marks, so that every quoted string can be found in the files.")

# ---------------------------------------------------------------------------
# Run 7: the column as a characterisation, which is what the old one was.
# ---------------------------------------------------------------------------
# Runs 1-6 asked the writer to find the lines that fall short and say what is wrong with
# them, and every failure they turned up -- fabricated speaker swaps, misquoted strings,
# corrections to correct text, "reads as sound" -- is a failure at pointing. Measuring the
# 1,072 entries of the column being replaced says it never pointed:
#
#     median 5 words, longest 11; a quotation mark in 23 entries of 1,072, always a
#     single word; a line number in none.
#
# It is `<severity> <kind of defect>`, a noun phrase about the translation as a whole:
# "Minor stylistic phrasing issues", "Severe structural corruption and gibberish". The
# severity word tracks the score almost monotonically -- Severe at a median of 32, Critical
# 57, Notable 74, Minor 91, Exceptional 97 -- and that is the register Jev's level can set,
# leaving the writer only the kind. Naming the kind is the one thing runs 1-6 got right
# even where the location was invented.
#
# So this is the default wording from run 7 on, and runs 1-6 are behind --locate.

# One per level, in place of LEVEL_INSTRUCTIONS. The register words are the ones the old
# column actually used at that level: of its level-3 entries 298 open with "Minor", of its
# level-1 entries 58 open with "Severe" and 11 with "Pervasive", and level 4's open with
# "Exceptional" or "Excellent".
CHARACTER_INSTRUCTIONS = {
    4: "The evaluation found nothing in this translation that falls short. The column is "
       "praise here: name what it does well as a property of the whole translation. The "
       "register is 'exceptional' or 'excellent'.",
    3: "The evaluation found a small part of this translation falling short and the rest "
       "sound. Name the kind of thing that is less than ideal in it. The register is "
       "'minor': worth recording in a table, not enough to damage the translation.",
    2: "The evaluation found a substantial part falling short, or one problem running "
       "through the whole text. Name what recurs. The register is 'significant', "
       "'notable' or 'critical' -- something a reader meets again and again.",
    1: "The evaluation found most of the translation falling short. Name what is wrong "
       "with it taken as a whole. The register is 'severe' or 'pervasive'.",
    # Naming the possibilities here was tried and the writer returned all of them at once
    # ("Severe corruption gibberish untranslated text throughout"), so the level says what
    # the question is and leaves the answer to the text.
    0: "The evaluation found nothing in this translation that meets its criteria, and "
       "there may be no usable target-language text at all. Name what the text actually "
       "is instead of a translation. The register is 'severe'.",
}

# The closing line, in place of the WHERE-and-WHAT one. It is the whole difference between
# the two genres, so it says the prohibition and the request in one breath.
CHARACTER_CLOSING = ("Write one short phrase characterising the translation as a whole: "
                     "the KIND of thing that falls short. Not where an instance of it is.")

# Run 7's closing line, which ended `and how far through the text it reaches`. That half
# asks for the extent the level has already given, and the writer answered it with a number
# it had no way to know: eleven of 66 phrases carried one, `gpt-oss/sv` was told it has
# three unlabelled lines when it has eight, and one translation got "approx three lines",
# "approx 5%" and "approximately 10 lines" from three variants of one wording. Kept behind
# --extent-clause so run 7's section still sends what run7/ holds; the flag restores the
# same clause in NO_POINTING_RULE below, since run 7 carried it in both places.
CHARACTER_CLOSING_EXTENT = ("Write one short phrase characterising the translation as a "
                            "whole: the KIND of thing that falls short and how far through "
                            "the text it reaches. Not where an instance of it is.")

# Dropping the clause may not be enough on its own -- run 4 is the precedent, where removing
# what prompted a behaviour left the behaviour in place. This says it outright. For
# --no-magnitude.
NO_MAGNITUDE_RULE = ("IMPORTANT: Do not state how much. No count of lines, no percentage, "
                     "no fraction of the text. How much was measured by the evaluation and "
                     "is given above; a number of your own would be a guess, and the "
                     "phrase is about what kind of thing it is.")

# Level 4 has just been told nothing falls short, so the closing above would contradict it.
CHARACTER_CLOSING_LEVEL_4 = ("Write one short phrase characterising the translation as a "
                             "whole: the KIND of thing it does well, as a property of all "
                             "of it. Not an instance of it.")

# Under this genre the line-number ban of runs 2-6 and the quotation rules of run 6 collapse
# into one rule, and it is a prohibition rather than the regulation --quote-rule tried: run
# 6 could not make a quoted string reliable even when it asked for one, and the column being
# replaced quotes in 2% of entries.
NO_POINTING_RULE = ("IMPORTANT: Do not point at a place. No line numbers, and no strings "
                    "quoted from either text. The phrase says what kind of thing is wrong; "
                    "an instance of it is not what the column holds.")

# Run 7's form, whose tail read `and how much of the translation it affects`. It is the
# same mistake as the closing line's -- run 7 asked for the extent twice over, in the two
# places a writer reads last -- so --extent-clause restores both together.
NO_POINTING_RULE_EXTENT = ("IMPORTANT: Do not point at a place. No line numbers, and no "
                           "strings quoted from either text. The phrase says what kind of "
                           "thing is wrong and how much of the translation it affects; an "
                           "instance of it is not what the column holds.")

# The 2%, as a variant. The old column's quoted entries are all of this shape -- "Critical
# typo 'kaksoiraokeen', missing labels", "'potgooi' lexical error for podcast" -- one word
# and no correction beside it. For --word-rule.
WORD_RULE = ("One exception: if what falls short is a single word or term, you may name "
             "that word, copied from the translation exactly as it appears there. One word "
             "only, never a phrase or a line, and never a correction for it.")

# Seven entries of the column being replaced, spanning its range. None is a target of any
# run, so none of them is the answer to anything being asked. For --examples: whether the
# genre carries on the instruction alone is what run 7 has to find out, and a run that
# showed the shape from the start could not tell.
EXAMPLES = ("The column this goes into reads like this, on other translations:\n"
            "    Exceptional quality, nearly perfect\n"
            "    Minor stylistic phrasing issues\n"
            "    Minor terminology inconsistencies and anglicisms\n"
            "    Inconsistent terminology and anglicized syntax\n"
            "    Critical mixed-language glitch (Chinese)\n"
            "    Severe machine-translation artifacts\n"
            "    Severe structural corruption and gibberish\n"
            "None of those is about the translation above; they are the shape, not the "
            "answer.")

# ---------------------------------------------------------------------------
# Run 9: the task the old column was actually given.
# ---------------------------------------------------------------------------
# Runs 7 and 8 asked the writer to characterise a translation it had just read. That is not
# what produced the column being replaced. `trtools/trend.py` hands an LLM the
# `overall_comment` of three evaluation runs and asks it to summarise them; the writer never
# saw the translation, and the phrase is a summary of somebody else's verdict.
#
# Under Jev there is no verdict to summarise, so the equivalent has to come from the writer
# itself -- which is why this genre is run with thinking on, where every earlier run ran
# without it. The reasoning is the `overall_comment` and the phrase is its summary, in the
# same relation the old pipeline had. The level still supplies the extent, in place of the
# "Trust these evaluations as given" the old prompt opened with.
#
# The sentences below are the old prompt's, kept as close as the change of input allows.
# The one thing with no equivalent is `An issue mentioned in multiple runs is more reliable
# than one mentioned only once`: there is one reading here, not three.

# The level, stripped to the extent alone. CHARACTER_INSTRUCTIONS also carry a task -- name
# the kind, the register is 'minor' -- and under this genre the task is the closing line's,
# so the two would contradict each other. The register word goes with it: the old prompt
# never supplied one, its writer taking the severity from the evaluations' own prose. What
# this genre does with severity, having neither, is one of the things run 9 is for.
SUMMARY_LEVELS = {
    4: "The evaluation found nothing in this translation that falls short.",
    3: "The evaluation found a small part of this translation falling short, and the rest "
       "sound.",
    2: "The evaluation found a substantial part of this translation falling short, or one "
       "problem running through the whole text.",
    1: "The evaluation found most of this translation falling short.",
    0: "The evaluation found nothing in this translation that meets its criteria, and "
       "there may be no usable target-language text at all.",
}

SUMMARY_CLOSING = ("Summarize the single most notable characteristic of this translation "
                   "in one short phrase. If defects exist, state the most prominent one "
                   "concretely. If the translation is sound, state that briefly.")

# The old prompt's own format paragraph, minus the retry clause that belongs to trend.py's
# loop. Note the length: 8 words, where runs 7 and 8 asked for about five. The old column's
# median of five was what the writer did with an 8-word ceiling, not what it was told.
SUMMARY_FORMAT = ("OUTPUT FORMAT: Reply with the summary phrase itself and nothing else. "
                  "It goes directly into a Markdown table cell, so no labels, no quotation "
                  "marks around the whole phrase, no bullet points, no line breaks, no "
                  "trailing period, and no explanation before or after. Keep it within 40 "
                  "characters if written in Japanese, or a short phrase of about 8 words or "
                  "fewer if written in English.")

# Run 3's level-3 wording, kept behind --strict-level3 for the same reason the other
# superseded wordings are kept: so batch.sh's run-3 section still sends what run3/ holds.
STRICT_LEVEL_3 = ("The evaluation found that one to three lines fall short, and that the "
                  "rest of the translation is sound. Find those lines and say concretely "
                  "what is wrong with them. Do not answer with a general assessment of "
                  "quality: a phrase that could have been written without reading the "
                  "translation is not an answer.")

# Axis B, kept behind --axis-b after the comparison in PLAN.md sections 3 and 4 rejected it.
# Short forms of the matching `criterion` description in trtools/jev_criteria.py.
FOCUS_INSTRUCTIONS = {
    "readability": "whether the content can be understood -- unclear explanation, or "
                   "sentence structure that is illogical or hard to follow",
    "fluency": "how it reads to a native speaker -- unnatural expressions, awkward "
               "grammar, or vocabulary that is wrong, inconsistent or dated",
    "terminology": "the technical terms -- wrong or inconsistent term choice, or terms "
                   "left unexplained where the reader needs it",
    "contextual_adaptation": "whether the original's intent survives -- expressions that "
                             "ignore the reader's cultural background, or source wording "
                             "rendered literally where it does not work",
    "information_completeness": "what is missing or added -- information dropped from the "
                                "original, or padding that was never in it",
}

# Axis B's other branch, on the 294 records where no criterion stands out. Worded so it
# does not become a second way out: nothing standing out does not mean nothing falls short.
FOCUS_NONE = ("No single criterion stands out below the others, which does not mean "
              "nothing falls short -- the extent stated above still holds. Look across "
              "all five and report whichever you actually find.")


def focus_text(focus):
    """Axis B's sentence for the criteria that stand out, or FOCUS_NONE for none."""
    if not focus:
        return FOCUS_NONE
    parts = [FOCUS_INSTRUCTIONS[key] for key in focus]
    if len(parts) == 1:
        return f"Look first at {parts[0]}."
    return "Look first at " + "; and at ".join(parts) + "."


def build_prompts(original_text, translated_text, lang_name, level, focus,
                  with_original=True, axis_b=False, line_rule=True, strict_level_3=False,
                  slight=False, sound_rule=False, backtrans_rule=False, quote_rule=False,
                  locate=False, examples=False, word_rule=False,
                  extent_clause=False, no_magnitude=False,
                  summary=False, summary_free=False,
                  output_lang_name="English"):
    """The prompt list, in trtools/trend.py's shape: text blocks, then the instruction.

    Two genres. The default is run 7's: a characterisation of the translation as a whole,
    which is what the column being replaced holds. `locate` restores runs 1-6, which asked
    for the lines that fall short and what is wrong with them; every flag above it belongs
    to that genre and does nothing without it.
    """
    blocks = []
    if with_original:
        blocks.append(f'<original lang="English">\n{original_text}\n</original>')
    blocks.append(f'<translation lang="{lang_name}">\n{translated_text}\n</translation>')

    if summary:
        # The level gives the extent and nothing else; the task is the closing line's.
        verdict = SUMMARY_LEVELS[level]
        closing = SUMMARY_CLOSING
        rules = [] if summary_free else [NO_POINTING_RULE]
        output_format = SUMMARY_FORMAT
    elif not locate:
        verdict = CHARACTER_INSTRUCTIONS[level]
        closing = (CHARACTER_CLOSING_LEVEL_4 if level == len(LEVELS) - 1
                   else CHARACTER_CLOSING_EXTENT if extent_clause
                   else CHARACTER_CLOSING)
        pointing = NO_POINTING_RULE_EXTENT if extent_clause else NO_POINTING_RULE
        rules = [pointing + (" " + WORD_RULE if word_rule else "")]
        if no_magnitude:
            rules.append(NO_MAGNITUDE_RULE)
        if examples:
            rules.append(EXAMPLES)
        # A noun phrase, at the length the old column actually ran to: median 5 words,
        # longest 11. The Japanese limit is carried over from trtools/trend.py unchanged.
        output_format = (
            "OUTPUT FORMAT: Reply with the phrase itself and nothing else. It is a noun "
            "phrase going straight into a Markdown table cell, so no sentence, no verb "
            "leading it, no labels, no quotation marks around the whole phrase, no bullet "
            "points, no line breaks, no trailing period, and no explanation before or "
            "after. Keep it within 40 characters if written in Japanese, or about five "
            "words if written in English -- eight is the most the column has ever held.")
    else:
        if level == 3 and strict_level_3:
            verdict = STRICT_LEVEL_3
        elif level == 3 and slight:
            verdict = LEVEL_3_SLIGHT_STRONG if sound_rule else LEVEL_3_SLIGHT
        else:
            verdict = LEVEL_INSTRUCTIONS[level]
        # No focus at level 4: axis B exists to point at what fell short, and the level has
        # just said nothing did. Asking for both produces a prompt that contradicts itself.
        if axis_b and level > 0 and level < len(LEVELS) - 1:
            verdict += "\n" + focus_text(focus)
        closing = ("Say in one short phrase what it does well.\n"
                   if level == len(LEVELS) - 1 else
                   # With the strengthened slight branch the closing line has to leave the
                   # same door open, or it takes back what the branch just granted.
                   "Say in one short phrase what you found, or that it reads as sound."
                   if (slight and sound_rule) else
                   "Say in one short phrase WHERE the problem is and WHAT it is.")
        rules = []
        if backtrans_rule:
            rules.append(BACKTRANS_RULE)
        if quote_rule:
            rules.append(QUOTE_RULE)
        if line_rule:
            rules.append("IMPORTANT: Never cite a line number. The text you were given "
                         "carries none, and a number you count yourself will be wrong. To "
                         "point at a place, quote the words from the translation, exactly "
                         "as they appear in it.")
        output_format = (
            "OUTPUT FORMAT: Reply with the phrase itself and nothing else. It goes "
            "directly into a Markdown table cell, so no labels, no quotation marks around "
            "the whole phrase, no bullet points, no line breaks, no trailing period, and "
            "no explanation before or after. Keep it within 40 characters if written in "
            "Japanese, or about 8 words or fewer if written in English.")

    instruction = (
        f"The block above is a dialogue transcript translated into {lang_name}"
        + (", line for line against the original shown with it" if with_original else "")
        + ". A separate evaluator has already scored it. That evaluator reports only HOW "
        f"MUCH of the document falls short, never what kind of defect is responsible, so "
        f"naming the defect is your job and the extent is not.\n\n"
        f"{verdict}\n\n"
        f"Take the extent above as given and do not re-score the translation. {closing}\n"
        f"IMPORTANT: The phrase must be written in {output_lang_name}, but it describes a "
        f"translation into {lang_name}. Never confuse the language you write in with the "
        f"language being described.\n"
        f"IMPORTANT: State only what you can actually see in the translation. Do not "
        f"guess at a cause you cannot observe -- if text from another language intrudes "
        f"without your being able to tell which language it is, say so generically.\n"
        + "".join(rule + "\n" for rule in rules)
        + output_format
    )
    return blocks + [instruction]


# ---------------------------------------------------------------------------
# Run 13: the old pipeline itself, in two stages.
# ---------------------------------------------------------------------------
# Runs 9-12 asked one call to play both parts: the writer's reasoning stood in for the
# `overall_comment` and the phrase was its summary. This puts the two parts back into two
# calls, each with its own old prompt. Stage 1 is `trtools/evaluate.py`'s prompt, asked for
# the `overall_comment` alone and in plain text instead of the whole schema; stage 2 is
# `trtools/trend.py`'s prompt, handed that one comment where it used to get three. Both run
# without thinking, whatever --think says.
#
# The scores are Jev's. Its five criteria are evaluate.py's five, and a level times
# POINTS_PER_LEVEL is a score out of 20 -- the scale evaluate.py's point bands are written
# on. So stage 1 is handed the scores already given and writes the comment that goes with
# them, as the old evaluator's comment went with its own scores; without them the comment
# would be a second, independent verdict, and the column would not describe the score beside
# it. Stage 2's block header carries the Jev total where trend.py's carried each run's.

# evaluate.py's prompt verbatim, except the closing sentence: it asked for five scores, and
# what replaces it is Jev's scores and the schema's description of `overall_comment`. The
# point bands stay -- they are how that prompt says what a score means.
#
# The comment is always in English. The old schema kept it there without saying so; plain
# text does not, and a comment written in the target language would make the evaluation of
# a Hindi translation depend on how well the writer writes Hindi.
def two_stage_eval_prompts(original_text, translated_text, lang_name, scores):
    lines = "\n".join(
        f"- {CRITERIA[key][0]}: {scores[key] * POINTS_PER_LEVEL:.1f}/20"
        for key in CRITERION_IDS)
    total = sum(scores.values()) * POINTS_PER_LEVEL
    instruction = f"""Please evaluate this translation from English to {lang_name}.

**CRITICAL GUIDELINES**:
1. Verify translation exists and is in {lang_name}. If missing/incomplete, assign 0 points to ALL criteria.
2. Evaluate the ENTIRE file from beginning to end, not just the first or last lines.
3. Structural defects (mixed languages, JSON fragments, meta-commentary) are CRITICAL errors (0-5 points).
4. Major defects (grammatical errors, untranslated text) = 6-12 points.
5. Minor issues (awkward phrasing) = 13-17 points.
6. High quality (natural, accurate) = 18-20 points.

The translation has already been scored on each criterion:
{lines}
Total score: {total:.1f}/100

Do not re-score it. Write an overall comprehensive evaluation comment about the translation quality as a whole, based on the ENTIRE document, that accounts for these scores.
Write the comment in English — not in {lang_name}."""
    return [
        f"<original>\n{original_text}\n</original>",
        f"<translation>\n{translated_text}\n</translation>",
        instruction,
    ]


# trend.py's prompt, with its plurals made singular and the one sentence that has no
# referent with a single evaluation -- `An issue mentioned in multiple runs is more reliable
# than one mentioned only once` -- taken out.
def two_stage_trend_prompts(comment, total, lang_name, output_lang_name,
                            shortfall_rule=False, level=None):
    level_text = "" if level is None else JEV_LEVEL.format(LEVELS[level])
    rule = SHORTFALL_RULE if shortfall_rule else ""
    return [
        f"<evaluations lang=\"{lang_name}\">\n"
        f"# Evaluation (Score {total:.1f})\n\n{comment}\n"
        f"</evaluations>",
        f"The block above contains an evaluation of one translation "
        f"whose target language is {lang_name}. Trust this evaluation as given; "
        f"do not re-evaluate the translation yourself. {level_text}Summarize the single "
        f"most notable characteristic in one short phrase.\n"
        f"{rule}"
        f"IMPORTANT: The summary must be written in {output_lang_name}, but it "
        f"describes a translation into {lang_name}. Never confuse the language you "
        f"write in with the language being evaluated.\n"
        f"IMPORTANT: State only what the evaluation actually says. Do not add "
        f"details it does not mention. For example, if it reports a mixed-language "
        f"defect without naming the intruding language, describe it generically "
        f"rather than guessing which language it was.\n"
        f"OUTPUT FORMAT: Reply with the summary phrase itself and nothing else. "
        f"It goes directly into a Markdown table cell, so no labels, no quotation "
        f"marks around the whole phrase, no bullet points, no line breaks, no "
        f"trailing period, and no explanation before or after. "
        f"If defects exist, state the most prominent one concretely. If the "
        f"translation is sound, state that briefly. "
        f"Keep it within 40 characters if written in Japanese, or a short phrase of "
        f"about 8 words or fewer if written in English. "
        f"Write it in {output_lang_name} — not in {lang_name}.",
    ]


# ---------------------------------------------------------------------------
# Run 14: stage 2 biased toward the shortfall.
# ---------------------------------------------------------------------------
# Run 13's stage 2 answered 29 of the 44 phrases on its 89-and-over level-3 rows with praise
# alone, where the old column did so for 29% of its 90-and-over rows -- and every one of the
# 29 comments it was summarising named a shortfall, because stage 1 is told to account for
# scores below full marks. The comment has the material and the summary drops it. So stage 2
# is re-run over run 13's comments, with stage 1 left as it was.

# --shortfall-rule (A). Jev never gives full marks, so this is a rule about the comment: a
# phrase praises only when the comment names nothing.
SHORTFALL_RULE = ("IMPORTANT: If the evaluation names any shortcoming, however minor, state "
                  "the most prominent one rather than praising the translation. Praise it "
                  "only if the evaluation names no shortcoming at all.\n")

# --jev-level (B). Jev's own words for the level of the weakest criterion. Stage 1 read the
# scores through evaluate.py's point bands, where 17-19 of 20 is "high quality"; on Jev's
# scale the same level 3 means one to three lines falling short. LEVELS verbatim, since a
# rewording would say something Jev was not asked.
JEV_LEVEL = "The scoring behind it judged its weakest criterion as follows: {} "


def two_stage(client, original_text, translated_text, lang_name, scores, output_lang,
              output_lang_name):
    """(comment, phrase). Stage 2 retries on the wrong language, as trend.py does."""
    comment = client.call(
        two_stage_eval_prompts(original_text, translated_text, lang_name, scores))
    total = sum(scores.values()) * POINTS_PER_LEVEL
    prompts = two_stage_trend_prompts(comment.strip(), total, lang_name, output_lang_name)
    for attempt in range(3):
        p = prompts if attempt == 0 else prompts + [
            f"The previous reply was not in {output_lang_name}. "
            f"Reply again with the same summary written in {output_lang_name}, "
            f"and output nothing but the phrase itself."
        ]
        print("\n  -> ", end="", flush=True)
        text = client.call(p)
        if _matches_lang(text, output_lang):
            break
        print(f"  retrying: not in {output_lang_name} ({attempt + 1}/3)")
    return comment.strip(), text


# ---------------------------------------------------------------------------
# Targets and plumbing.
# ---------------------------------------------------------------------------

# A sample spanning all five levels of axis A and every branch of axis B, taken from the
# corpus's own distribution. Not representative -- deliberately weighted toward the rare
# branches, which is where a wording fails first. The ordinary case is level 3 / fluency,
# and gpt-5.6-luna/da is there for the failure the experiment is named after: the current
# column calls it "Professional-grade scientific translation ready for publication".
DEFAULT_TARGETS = [
    "gpt-5.6-luna/it",        # level 4, no focus  -- the 12 records where "sound" is right
    "gpt-5.6-luna/da",        # level 3            -- currently answered with praise
    "qwen3.6/he",             # level 3, fluency   -- the ordinary case
    "gemini-3.7-flash/el",    # level 3, no focus
    "gpt-oss/sv",             # level 3, information_completeness
    "bonsai2-27b/ne",         # level 2, fluency
    "qwen3.8/th",             # level 2, information_completeness
    "qwen3.6-27b/el",         # level 2, no focus
    "gemma4/ga",              # level 1, fluency
    "gemma4-31b/ia",          # level 1, several criteria at once
    "bonsai2-27b/cy",         # level 0, no focus
]


# The set that actually exercises axis B. In the corpus, the only criterion that stands
# out on its own without being fluency is `information_completeness` (45 records); the rest
# of axis B's branches are combinations with fluency (8 records). DEFAULT_TARGETS holds
# three of these between eleven, which is too thin for the comparison against --axis-a-only
# to show anything -- the first run's variation between two identical runs was larger than
# its variation between the two variants. Weighted here instead of sampled.
FOCUS_TARGETS = [
    "gemini-3.5-flash-lite/sv",   # level 3, information_completeness
    "gpt-oss/es",                 # level 3, information_completeness
    "gpt-5.6-terra/es",           # level 3, information_completeness
    "muse-glimmer/id",            # level 2, information_completeness
    "gemini-3-flash/eu",          # level 2, information_completeness
    "gpt-oss/id",                 # level 2, information_completeness
    "bonsai2-27b/ar",             # level 1, information_completeness
    "bonsai2-27b/id",             # level 1, information_completeness
    "gpt-oss/da",                 # level 2, fluency + information_completeness
    "bonsai2-27b/lt",             # level 1, fluency + contextual_adaptation
    "qwen3.6/th",                 # level 1, readability + fluency
]


# The set that exercises the level-3 split. Every fabricated phrase in runs 1-4 came from
# `gpt-5.6-luna/da`, which is one record; the corpus has 53 whose weakest criterion is 3.3
# or above, and these eleven spread them over eight models and ten languages. `da` is kept
# at the head for continuity -- it produced eight false claims across four runs.
SLIGHT_TARGETS = [
    "gpt-5.6-luna/da",        # 3.40, and the row every earlier run fabricated about
    "qwen3.8/es",             # 3.49
    "gemini-3.7-flash/ca",    # 3.49
    "ox-alpha/ru",            # 3.46
    "gpt-5.6-luna/ro",        # 3.45
    "union-alpha/sk",         # 3.43
    "qwen3.6/es",             # 3.43
    "ox-alpha/hr",            # 3.43
    "gemma4-31b/ru",          # 3.43
    "gemini-3.7-flash/ja",    # 3.43
    "gpt-5.6-luna/uk",        # 3.42
]


# DEFAULT_TARGETS and SLIGHT_TARGETS together, in that order and without repeating the one
# row they share. A run whose variants are the same wording over both sets should send this
# in one call rather than two: the two sets overlap only in `gpt-5.6-luna/da`, so splitting
# re-sends that row under a second variant name and restarts the counter for nothing. Run 7
# was split that way; from run 8 on, --all-targets is what a run over both sets uses.
ALL_TARGETS = DEFAULT_TARGETS + [t for t in SLIGHT_TARGETS if t not in DEFAULT_TARGETS]


def load_jev(model, lang):
    """The jev.jsonl record for one translation."""
    path = ONDE / model / "jev.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() and json.loads(line)["lang"] == lang:
            return json.loads(line)
    raise SystemExit(f"{path}: no record for {lang!r}")


def load_old_analysis(model, lang):
    """The phrase currently in TRENDS.jsonl, which is what the new one is compared with."""
    path = ONDE / model / "TRENDS.jsonl"
    if not path.is_file():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            if record["lang"] == lang:
                return record
    return None


def read_axes(scores):
    """(level, weakest score, [focus criteria]) from one record's five scores.

    The level is the rounded weakest criterion; the unrounded value comes back with it
    because level 3 is more than half the corpus and its two ends behave differently.
    """
    weakest = min(scores.values())
    level = max(0, min(len(LEVELS) - 1, int(weakest + 0.5)))
    mean = statistics.mean(scores.values())
    focus = [key for key in CRITERION_IDS if scores[key] < mean - FOCUS_THRESHOLD]
    return level, weakest, focus


# The switches a variant can carry, as `name:opt,opt` on the command line. They are the
# superseded wordings and the two rejected inputs, each of which an earlier run was made
# on; the names match the flags that set them globally.
VARIANT_OPTS = ("two-stage", "shortfall-rule", "jev-level", "summary", "summary-free",
                "locate", "examples", "word-rule", "extent-clause", "no-magnitude",
                "axis-b", "no-original", "no-line-rule", "strict-level3",
                "no-level3-split", "sound-rule", "backtrans-rule", "quote-rule")


def parse_variant(spec, defaults):
    """`name` or `name:opt,opt` -> (name, {opt: bool}), starting from the global flags."""
    name, _, opts = spec.partition(":")
    settings = dict(defaults)
    for opt in filter(None, (o.strip() for o in opts.split(","))):
        if opt not in VARIANT_OPTS:
            raise SystemExit(f"unknown variant option {opt!r}; one of {VARIANT_OPTS}")
        settings[opt] = True
    if not name:
        raise SystemExit(f"variant {spec!r} has no name")
    return name, settings


def args_comments():
    """Whether this invocation re-runs stage 2 over saved comments; set in main()."""
    return COMMENTS_DIR is not None


COMMENTS_DIR = None


def variant_label(settings):
    """What goes in the record's `variant` field."""
    if settings["two-stage"]:
        return "two-stage"
    if args_comments():
        label = "stage-2"
        for opt in ("shortfall-rule", "jev-level"):
            if settings[opt]:
                label += "/" + opt
        return label
    label = ("summary" if settings["summary"] else
             "locate" if settings["locate"] else "character")
    if settings["axis-b"]:
        label += "/axis-b"
    for opt in ("summary-free", "examples", "word-rule", "extent-clause", "no-magnitude",
                "no-original", "no-line-rule", "strict-level3",
                "no-level3-split", "sound-rule", "backtrans-rule", "quote-rule"):
        if settings[opt]:
            label += "/" + opt
    return label


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("targets", nargs="*", default=DEFAULT_TARGETS,
                        help="model/lang pairs under examples/tr/onde (default: a sample "
                             "spanning every branch of both axes)")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
                        help=f"Model that writes the phrase (default: {DEFAULT_MODEL})")
    parser.add_argument("--think", action="store_true",
                        help="Enable thinking; both evaluate: and trends: run without it")
    parser.add_argument("--no-original", action="store_true",
                        help="Send the translation alone, without the English original")
    parser.add_argument("--focus-targets", action="store_true",
                        help="Use FOCUS_TARGETS instead, the set weighted toward the "
                             "criteria the focus sentence can actually point at")
    parser.add_argument("--slight-targets", action="store_true",
                        help="Use SLIGHT_TARGETS instead, the set in level 3's top tenth "
                             "where the split changes the instruction")
    parser.add_argument("--all-targets", action="store_true",
                        help="Use both sets at once, which is what a run whose variants "
                             "are one wording over both should send -- one call, not two")
    parser.add_argument("--locate", action="store_true",
                        help="Restore runs 1-6's genre, which asked for the lines that "
                             "fall short and what is wrong with them. Every flag below "
                             "this one belongs to it and does nothing without it")
    parser.add_argument("--examples", action="store_true",
                        help="Show seven entries of the column being replaced, as the "
                             "shape the phrase is meant to have")
    parser.add_argument("--word-rule", action="store_true",
                        help="Allow naming a single word copied from the translation, "
                             "which is the only thing the old column ever quoted")
    parser.add_argument("--two-stage", action="store_true",
                        help="Run 13: evaluate.py's prompt writes an overall comment, then "
                             "trend.py's prompt summarises it. Both calls run without "
                             "thinking, and every other wording flag is ignored")
    parser.add_argument("--comments", metavar="DIR",
                        help="Run 14: re-run stage 2 alone over the stage-1 comments in "
                             "DIR's two-stage*.jsonl. Each variant writes one file per "
                             "source file, the source's -N suffix carried over; the "
                             "target list is the sources' own")
    parser.add_argument("--shortfall-rule", action="store_true",
                        help="With --comments: state the shortfall the comment names "
                             "rather than praise; praise only when it names none")
    parser.add_argument("--jev-level", action="store_true",
                        help="With --comments: give stage 2 Jev's own words for the "
                             "level of the weakest criterion")
    parser.add_argument("--summary", action="store_true",
                        help="Run 9's genre: the task `trtools trend` gives its writer, "
                             "summarising an assessment rather than characterising a text. "
                             "Meant to be run with --think, the reasoning standing in for "
                             "the `overall_comment` the old prompt was handed")
    parser.add_argument("--summary-free", action="store_true",
                        help="With --summary, drop the ban on pointing, which the old "
                             "prompt did not carry -- its writer never saw the translation")
    parser.add_argument("--no-magnitude", action="store_true",
                        help="Forbid stating how much -- no line count, percentage or "
                             "fraction. The level already gave the extent")
    parser.add_argument("--extent-clause", action="store_true",
                        help="Restore run 7's two requests for the extent, in the closing "
                             "line and in the no-pointing rule; kept so that run "
                             "reproduces")
    parser.add_argument("--sound-rule", action="store_true",
                        help="Strengthen the slight branch: saying it reads as sound is "
                             "the ordinary answer, not a fallback")
    parser.add_argument("--backtrans-rule", action="store_true",
                        help="Forbid judging the translation by rendering it back into "
                             "English first")
    parser.add_argument("--quote-rule", action="store_true",
                        help="Quotation marks only for text copied from the files; "
                             "corrections go outside them")
    parser.add_argument("--no-level3-split", action="store_true",
                        help="Treat all of level 3 alike, as run 4 did, instead of giving "
                             f"its top (weakest criterion >= {LEVEL_3_SLIGHT_MIN}) an "
                             "instruction that does not assert a locatable shortfall")
    parser.add_argument("--strict-level3", action="store_true",
                        help="Restore run 3's level-3 wording, which forbade answering "
                             "with a general assessment; kept so that run reproduces")
    parser.add_argument("--no-line-rule", action="store_true",
                        help="Drop the ban on citing line numbers, as the prompt stood "
                             "for run 1; kept so that run reproduces")
    parser.add_argument("--axis-b", action="store_true",
                        help="Re-enable the focus sentence, which an earlier run "
                             "rejected; kept so that rejection stays reproducible")
    parser.add_argument("-v", "--variant", dest="variants", action="append", metavar="SPEC",
                        help="`name` or `name:opt,opt`, repeatable. Each target is then "
                             "written by every variant in turn, so the original and the "
                             "translation stay at the head of the prompt across the whole "
                             "group and the cache holds. Options: " + ", ".join(VARIANT_OPTS))
    parser.add_argument("-d", "--out-dir",
                        help="Directory for <variant>.jsonl; required with --variant")
    parser.add_argument("-l", "--lang", choices=["en", "ja"], default="en",
                        help="Language the phrase is written in (default: en)")
    parser.add_argument("-o", "--output", dest="output_file",
                        help="JSONL to append to, for a single unnamed variant")
    parser.add_argument("--save-usage", action="store_true",
                        help="Record usage regardless of model name; otherwise it is "
                             "recorded for any writer that is not a local ollama: one")
    parser.add_argument("--show-prompt", action="store_true",
                        help="Print the instruction for each target and exit, without "
                             "calling the model")
    args = parser.parse_args()
    if args.comments:
        return run_comments(parser, args)
    for flag, targets in (("focus_targets", FOCUS_TARGETS),
                          ("slight_targets", SLIGHT_TARGETS),
                          ("all_targets", ALL_TARGETS)):
        if getattr(args, flag):
            if args.targets is not DEFAULT_TARGETS:
                raise SystemExit(f"--{flag.replace('_', '-')} replaces the target list; "
                                 f"do not name targets too")
            args.targets = targets

    defaults = {opt: getattr(args, opt.replace("-", "_")) for opt in VARIANT_OPTS}
    if args.variants:
        if not args.out_dir:
            raise SystemExit("--variant needs --out-dir")
        variants = [parse_variant(spec, defaults) for spec in args.variants]
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        # One unnamed variant, taking the global flags; -o is where it goes, if anywhere.
        variants = [(None, defaults)]
        out_dir = None

    original_text = ORIGINAL.read_text(encoding="utf-8").rstrip()
    output_lang_name = "Japanese" if args.lang == "ja" else "English"
    client = None if args.show_prompt else LLMClient(model=args.model, think=args.think)
    # The two-stage variant runs without thinking regardless of --think.
    client_no_think = None if args.show_prompt else LLMClient(model=args.model, think=False)

    # Where the cost of a run is recorded, or None when it is not worth recording, on
    # trtools.llm.init_usage_path()'s condition. Every call's Usage is summed and the sum is
    # appended as one line at the end, so a section of batch.sh leaves one row per
    # invocation rather than one per phrase. Runs 1-8 were a local model and cost nothing,
    # so this stays None for them; run 9 is the first with a commercial writer, and a run
    # over 21 targets times four variants is worth knowing the price of before it becomes
    # 67 languages times sixteen models. A commercial writer that is neither openai: nor
    # gpt- needs --save-usage.
    usage_path = init_usage_path(args.model, args.save_usage)
    total_usage = Usage()

    # Targets outer, variants inner. Every variant of one target sends the same original
    # and the same translation, and only the instruction after them differs, so running
    # them together keeps that prefix in the server's cache. The other order re-sends a
    # different translation on every call and throws it away each time.
    for n, target in enumerate(args.targets, 1):
        model, _, lang = target.partition("/")
        if not lang:
            raise SystemExit(f"expected model/lang, got {target!r}")
        record = load_jev(model, lang)
        level, weakest, focus = read_axes(record["scores"])
        total = sum(record["scores"].values()) * POINTS_PER_LEVEL
        lang_name = LANGUAGES[lang]["en"]
        tr_file = ONDE / model / "tr" / f"onde-{lang}.txt"
        translated_text = tr_file.read_text(encoding="utf-8").rstrip()

        focus_label = "+".join(focus) if focus else "none"
        print(f"\n=== ({n}/{len(args.targets)}) {target}  {lang_name}  jev {total:.1f}  "
              f"level {level} ({weakest:.2f})  focus {focus_label}")
        old = load_old_analysis(model, lang)
        if old and not args.show_prompt:
            print(f"  old ({old['score']}): {old['analysis']}")

        for name, settings in variants:
            if settings["two-stage"]:
                if args.show_prompt:
                    print(f"--- {name or 'default'} (stage 1)")
                    print(two_stage_eval_prompts("", "", lang_name, record["scores"])[-1])
                    print(f"--- {name or 'default'} (stage 2)")
                    print("\n".join(two_stage_trend_prompts("<comment>", total, lang_name,
                                                            output_lang_name)))
                    continue
                print(f"  {name or 'new'}: ", end="", flush=True)
                client_no_think.usage = Usage()
                comment, text = two_stage(client_no_think, original_text,
                                          translated_text, lang_name,
                                          record["scores"], args.lang,
                                          output_lang_name)
                text = _clean(text)
                if usage_path is not None:
                    usage = client_no_think.usage
                    total_usage += usage
                    print(f"    {usage}")
                path = out_dir / f"{name}.jsonl" if out_dir else (
                    Path(args.output_file) if args.output_file else None)
                if path:
                    result = {
                        "model": model, "lang": lang, "score": round(total, 1),
                        "level": level, "focus": focus, "analysis": text,
                        "comment": comment,
                        "writer": args.model, "variant": variant_label(settings),
                    }
                    with path.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(result, ensure_ascii=False) + "\n")
                continue

            prompts = build_prompts(
                original_text, translated_text, lang_name, level, focus,
                with_original=not settings["no-original"], axis_b=settings["axis-b"],
                line_rule=not settings["no-line-rule"],
                strict_level_3=settings["strict-level3"],
                locate=settings["locate"], examples=settings["examples"],
                word_rule=settings["word-rule"],
                extent_clause=settings["extent-clause"],
                no_magnitude=settings["no-magnitude"],
                summary=settings["summary"],
                summary_free=settings["summary-free"],
                slight=(not settings["no-level3-split"]
                        and weakest >= LEVEL_3_SLIGHT_MIN),
                sound_rule=settings["sound-rule"],
                backtrans_rule=settings["backtrans-rule"],
                quote_rule=settings["quote-rule"],
                output_lang_name=output_lang_name,
            )
            if args.show_prompt:
                print(f"--- {name or 'default'}")
                print(prompts[-1])
                continue

            # llm7shi streams the reply as it arrives, so the label goes out first and the
            # text lands after it. Printing it again would show every phrase twice.
            print(f"  {name or 'new'}: ", end="", flush=True)
            client.usage = Usage()
            text = _clean(client.call(prompts))
            if usage_path is not None:
                usage = client.usage
                total_usage += usage
                print(f"    {usage}")

            path = out_dir / f"{name}.jsonl" if out_dir else (
                Path(args.output_file) if args.output_file else None)
            if path:
                result = {
                    "model": model, "lang": lang, "score": round(total, 1),
                    "level": level, "focus": focus, "analysis": text,
                    "writer": args.model, "variant": variant_label(settings),
                }
                with path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")

    if usage_path is not None:
        append_usage(total_usage, args.model, usage_path)
        print(f"\nTotal usage: {total_usage}\n")
        print_today_totals(usage_path)


def run_comments(parser, args):
    """Run 14: stage 2 over saved stage-1 comments, one output per (variant, source file).

    Sources outer and variants inner, so every variant of one comment sends the same block
    first and the cache holds it.
    """
    global COMMENTS_DIR
    COMMENTS_DIR = Path(args.comments)
    sources = sorted(COMMENTS_DIR.glob("two-stage*.jsonl"),
                     key=lambda p: (len(p.stem), p.stem))
    if not sources:
        raise SystemExit(f"{COMMENTS_DIR}: no two-stage*.jsonl")
    if not args.variants or not args.out_dir:
        raise SystemExit("--comments needs --variant and --out-dir")
    defaults = {opt: getattr(args, opt.replace("-", "_")) for opt in VARIANT_OPTS}
    variants = [parse_variant(spec, defaults) for spec in args.variants]
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_lang_name = "Japanese" if args.lang == "ja" else "English"
    client = None if args.show_prompt else LLMClient(model=args.model, think=False)

    for source in sources:
        suffix = source.stem[len("two-stage"):]
        records = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()
                   if line.strip()]
        print(f"\n########## {source}")
        for n, src in enumerate(records, 1):
            model, lang = src["model"], src["lang"]
            jev = load_jev(model, lang)
            level, weakest, _ = read_axes(jev["scores"])
            total = sum(jev["scores"].values()) * POINTS_PER_LEVEL
            lang_name = LANGUAGES[lang]["en"]
            print(f"\n=== ({n}/{len(records)}) {model}/{lang}  jev {total:.1f}  "
                  f"level {level} ({weakest:.2f})")
            print(f"  run13: {src['analysis']}")
            for name, settings in variants:
                prompts = two_stage_trend_prompts(
                    src["comment"], total, lang_name, output_lang_name,
                    shortfall_rule=settings["shortfall-rule"],
                    level=level if settings["jev-level"] else None)
                if args.show_prompt:
                    print(f"--- {name}")
                    print(prompts[-1])
                    continue
                print(f"  {name}: ", end="", flush=True)
                for attempt in range(3):
                    p = prompts if attempt == 0 else prompts + [
                        f"The previous reply was not in {output_lang_name}. "
                        f"Reply again with the same summary written in {output_lang_name}, "
                        f"and output nothing but the phrase itself."
                    ]
                    text = client.call(p)
                    if _matches_lang(text, args.lang):
                        break
                    print(f"  retrying: not in {output_lang_name} ({attempt + 1}/3)")
                result = {
                    "model": model, "lang": lang, "score": round(total, 1),
                    "level": level, "analysis": _clean(text),
                    "source": f"{source.parent.name}/{source.name}",
                    "writer": args.model, "variant": variant_label(settings),
                }
                with (out_dir / f"{name}{suffix}.jsonl").open("a", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
