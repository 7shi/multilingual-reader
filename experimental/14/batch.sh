#!/bin/bash
# Experiment 14: every run, in order, skipping the ones already done.
#
#     bash experimental/14/batch.sh
#
# One section per wording, writing to run1/ .. run12/. A section whose directory already
# holds results is skipped, so this is safe to re-run after an interruption: it does what
# is left and nothing else. To redo one, move its directory aside and run this again.
#
# Each section is a single call. trend14.py loops the targets on the outside and the
# variants on the inside, so every variant of a target sends the same original and the
# same translation one after another and that prefix stays in the server's cache; the
# other order re-sends a different translation on every call and throws it away. Per
# variant it writes <variant>.jsonl, and the console output -- the variants grouped under
# their target, beside the phrase currently in TRENDS.jsonl -- goes to the terminal and is
# not kept. Runs 1-12 teed it into runX/batch.log; nothing was ever read out of one that the
# JSONL did not already hold, and they have been deleted.
#
# Each section runs only what its own wording change puts in question. Repeating a variant
# an earlier run settled would cost more than it says, and the earlier runs are still on
# disk. The superseded wordings stay reachable through the flags --locate, --no-line-rule,
# --strict-level3, --axis-b and --no-original, so any section can be re-run as it was.
# Runs 1-6 all carry --locate: they asked the writer to find the lines that fall short,
# which run 7 stopped asking for, so without the flag they would not send what they sent.
#
# The writer is one model throughout: which generative model writes the column is a
# separate question that experimental/13/PLAN.md section 5.1 leaves open, and mixing it in
# here would confound it with the wording. PLAN.md is what each run is for and settled.

set -eu

cd "$(dirname "$0")/../.."
BASE=experimental/14

# Runs 1-8 are one model throughout, and it is pinned rather than taken from the
# environment: which generative model writes the column is a separate question
# (experimental/13/PLAN.md section 5.1), and letting it vary would confound it with the
# wording those runs were varying. Run 9 is where the model does change, and it takes MODEL
# from the environment because the writer there is a commercial one, named by whoever runs
# it rather than by this file.
WRITER=ollama:qwen3.6

# Opens a section, or returns non-zero if its directory already has results in it. A
# half-old, half-new set of phrases is worse than no set, so nothing is ever added to one.
# trend14.py writes its JSONL at the end, so an interrupted run leaves the directory empty
# and the section runs again -- which the batch.log tee used to prevent, by filling the
# directory from the first line of output.
section() {
    RUN=$1
    OUT=$BASE/$RUN
    if [ -n "$(ls -A "$OUT" 2>/dev/null)" ]; then
        echo "$OUT already done; skipping"
        return 1
    fi
    mkdir -p "$OUT"
    echo
    echo "########## $RUN"
    return 0
}

run() {
    uv run $BASE/trend14.py -m "$WRITER" -d "$OUT" "$@"
}

# Same, for a section whose writer comes from MODEL instead of the pinned one.
run_model() {
    uv run $BASE/trend14.py -m "$MODEL" -d "$OUT" "$@"
}

# --- run 1: the wording as first written -----------------------------------------------
# The focus sentence on, no rule about line numbers, and the level-3 instruction that
# forbids answering with a general assessment -- today's defaults inverted, so the flags
# restore them. Establishes whether the level-3 band names places at all, whether the
# phrases are specific enough to be worth a column, whether line numbers can be trusted,
# and whether the English original earns its half of the input.
if section run1; then
    W="--locate --no-line-rule --strict-level3"
    run $W \
        -v both:axis-b \
        -v both-2:axis-b \
        -v axis-a \
        -v no-original:axis-b,no-original
fi

# --- run 2: a ban on citing line numbers ------------------------------------------------
# Run 1 fabricated six line citations in 44 phrases, so the prompt now says to quote the
# words instead. `both` repeats run 1's configuration with the rule added, which is what
# the rule is judged on. The two focus-* variants are the first over FOCUS_TARGETS, the
# set weighted toward the criteria the focus sentence can point at -- DEFAULT_TARGETS has
# three such rows in eleven, too thin for run 1 to settle anything. --no-original was
# rejected in run 1 and is not repeated.
if section run2; then
    W="--locate --strict-level3"
    run $W -v both:axis-b
    run $W --focus-targets \
        -v focus-axis-b:axis-b \
        -v focus-main
fi

# --- run 3: the focus sentence dropped --------------------------------------------------
# Run 2 found it changing nothing that two runs of one prompt did not change by more, even
# over the set built to give it its best chance, so the level steers the phrase alone. The
# level-3 wording is still run 1's. Twice, because the writer is not deterministic and a
# phrase that changes completely between runs is a column of noise however well it reads
# once.
if section run3; then
    run --locate --strict-level3 -v main -v main-2
fi

# --- run 4: level 3 may report soundness, and may not invent a defect --------------------
# Run 3's level-3 wording forbade answering with a general assessment, and on a translation
# with nothing to find the writer invented a defect rather than leave the answer empty.
# The ban is replaced by permission to report soundness, with inventing a defect forbidden
# in its place. This is the current wording, so no flags.
if section run4; then
    run --locate -v main -v main-2
fi

# --- run 5: level 3 split by the unrounded minimum ------------------------------------
# Run 4's permission to report soundness was not taken: it sits after an instruction that
# has already asserted the shortfall exists, and the assertion wins. So what is asserted
# changes instead. Level 3 is 632 records whose weakest criterion runs 2.50 to 3.49, and
# every fabricated phrase in runs 1-4 came from the band's top tenth; above 3.3 the
# instruction now says the shortfall is slight and may not be visible at all.
#
# Over SLIGHT_TARGETS, the eleven records that branch -- DEFAULT_TARGETS has one. The rows
# below the threshold get run 4's instruction unchanged, so re-running them would only
# repeat run 4. --no-level3-split restores it if this needs comparing.
if section run5; then
    run --locate --slight-targets -v main -v main-2
fi

# --- run 6: three rules run 5 asked for, and their combinations -------------------------
# Run 5 got a named defect in all 22 phrases and "reads as sound" in none, so the slight
# branch is not reaching the writer; it also produced a failure that was not there before,
# judging the translation by rendering it back into English -- "psi in squares" for a
# correct пси в квадрате, "Naruhodo" for なるほど -- and went on quoting strings that are
# in neither file, usually because the quotes held a correction rather than the text.
#
# Three rules, and every combination, since the prefix is cached and the variants are
# nearly free: --sound-rule makes soundness the ordinary answer rather than a fallback,
# --backtrans-rule forbids judging the rendering instead of the translation, --quote-rule
# keeps corrections outside the quotation marks so a quoted string can be checked against
# the files mechanically. `base` is run 5 unchanged, as the control.
#
# The eight go over SLIGHT_TARGETS, where the fabrication lives. DEFAULT_TARGETS gets the
# control and the full set only: the rows there have real defects, and what they have to
# show is that the rules do not suppress a true finding.
if section run6; then
    run --locate --slight-targets \
        -v base \
        -v sound:sound-rule \
        -v backtrans:backtrans-rule \
        -v quote:quote-rule \
        -v sound-backtrans:sound-rule,backtrans-rule \
        -v sound-quote:sound-rule,quote-rule \
        -v backtrans-quote:backtrans-rule,quote-rule \
        -v all:sound-rule,backtrans-rule,quote-rule
    run --locate -v default-base \
        -v default-all:sound-rule,backtrans-rule,quote-rule
fi

# --- run 7: the column as a characterisation, not a location -----------------------------
# Runs 1-6 kept finding new ways for the writer to be wrong about WHERE -- invented speaker
# swaps, misquoted strings, corrections to correct text, and finally "reads as sound" in 41
# of 44, which is an absence of a location rather than a description of a translation. The
# column being replaced was measured after run 6 and it never pointed at anything: 1,072
# entries, median five words, a quotation mark in 23 of them and a line number in none. It
# is `<severity> <kind of defect>` -- "Minor stylistic phrasing issues", "Severe structural
# corruption and gibberish" -- and the severity word tracks the score almost monotonically,
# which is exactly what Jev's level can set. So the genre changes and the level now sets
# the register, leaving the writer the kind alone. That is the default from here; runs 1-6
# are behind --locate.
#
# Over DEFAULT_TARGETS, which spans all five levels -- SLIGHT_TARGETS was built for a
# failure mode that belongs to the other genre, and only its two hardest rows are worth
# carrying over. `char` is the design and `char-2` its repeat, because run 3 showed a
# phrase that changes completely between runs is a column of noise however well it reads
# once. `char-ex` shows seven entries of the old column as the shape: whether the
# instruction alone carries the genre is the thing to read off this run, and a run that
# showed examples from the start could not tell. `char-word` opens the one exception the
# old column took -- a single word, never a correction beside it, which is all its 2% of
# quotations ever held.
#
# Sent as two calls because --slight-targets replaces the target list. That was a mistake:
# unlike run 6, the two calls carry the same wording and differ only in their targets, so
# `da`, the sets' one shared row, went twice under two variant names and the counter
# restarted. --all-targets is the one-call form; run 8 uses it.
#
# --extent-clause restores what run 8 took out: run 7 asked how far the defect reaches, in
# the closing line and again in the no-pointing rule, and that is where its invented
# quantities came from.
if section run7; then
    W="--extent-clause"
    run $W -v char \
        -v char-2 \
        -v char-ex:examples \
        -v char-word:word-rule
    run $W --slight-targets \
        -v slight-char \
        -v slight-char-ex:examples
fi

# --- run 8: the extent asked for twice, taken out ----------------------------------------
# Run 7's genre was right -- the phrases match the old column's length distribution almost
# exactly, and gpt-5.6-luna/da stopped fabricating for the first time in seven runs -- but
# it asked for the extent in the two places a writer reads last, the closing line and the
# no-pointing rule, and got it answered with a number nobody had supplied. Eleven of 66
# phrases carried one; gpt-oss/sv was given three unlabelled lines when it has eight; one
# translation drew "approx three lines", "approx 5%" and "approximately 10 lines" from three
# variants of a single wording. The level already says how much, so both clauses go.
#
# `drop` is that alone and `drop-2` its repeat, because a phrase that changes completely
# between runs is a column of noise however well it reads once. `no-mag` adds the ban
# outright, run 4 being the precedent for removing a prompt and finding the behaviour still
# there. `no-mag-word` carries it with the old column's single-word exception, which run 7
# left doubtful: three of its four false phrases were in the variant that opened it, each
# one a word the writer went looking for. --examples is not repeated -- eight of its 22
# phrases were one of the seven examples verbatim, three translations sharing one string.
#
# One call over --all-targets, the 21 rows of both sets.
if section run8; then
    run --all-targets \
        -v drop \
        -v drop-2 \
        -v no-mag:no-magnitude \
        -v no-mag-word:no-magnitude,word-rule
fi

# --- run 9: the task the old column was actually given, on a commercial writer ------------
# Runs 7 and 8 asked the writer to characterise a translation it had just read, and that is
# not how the column being replaced was made. trtools/trend.py hands an LLM the
# overall_comment of three evaluation runs and asks it to summarise them: the writer never
# saw the translation, and the phrase is a summary of someone else's verdict. Under Jev
# there is no verdict, so the writer's own reading has to be it -- which is why this is the
# first section to run with thinking on. The reasoning plays the part of the
# overall_comment and the phrase is its summary, in the same relation the old pipeline had.
#
# The closing line and the output format are trtools/trend.py's own sentences, and the level
# is stripped to the extent alone, standing in for that prompt's "Trust these evaluations as
# given". Note the length: 8 words, where runs 7 and 8 asked for about five and got four.
#
# Three things change at once here -- the genre, thinking, and the model -- so `drop` is
# carried over as the control: it is run 8's winning wording, and having it on this writer
# is what separates the prompt from the model. `summary-free` drops the ban on pointing,
# which the old prompt did not carry because its writer had nothing to point at.
#
# MODEL is required and comes from the environment:
#
#     MODEL=... bash experimental/14/batch.sh
#
if section run9; then
    if [ -z "${MODEL:-}" ]; then
        echo "run9 needs MODEL set, e.g. MODEL=... bash $0" >&2
        rmdir "$OUT" 2>/dev/null
        exit 1
    fi
    run_model --all-targets --think \
        -v drop \
        -v summary:summary \
        -v summary-2:summary \
        -v summary-free:summary,summary-free
fi

# --- run 10: the same, without thinking --------------------------------------------------
# Run 9 changed the genre, the writer and the thinking all at once. `drop` was its control
# for the genre and separated that much: run 8's wording on run 9's writer still medians at
# four words and produces none of the seven findings. What it did not separate is the
# thinking from the model.
#
# That separation is about which writer to use, not about this one. The commercial writer is
# a yardstick and will not be adopted -- one pass over the corpus sends 1,072 whole
# translations, and PLAN.md section 10 is what that costs. So the live question is how much
# of run 9 a local model keeps, and the answer depends on where the findings come from: if
# the reasoning produces them, a local model with thinking on may reach them; if the model's
# own knowledge of Croatian and Catalan does, no wording gets them out of a smaller one.
# This run is the cheap half of telling those apart -- reasoning was 10,601 of run 9's
# 11,700 output tokens.
#
# Identical to run 9 in every other respect: same MODEL, same --all-targets, same wording,
# no --think. trend14.py does not think unless asked, so the flag's absence is the change.
#
# `summary-free` is the variant under test -- six of run 9's seven checked findings are its,
# and naming the string is what made them checkable. `summary-free-2` repeats it, because
# run 9's stability (17 of 21) was measured with thinking on and is exactly what might not
# survive without it. `summary` carries the ban on pointing across, so the comparison run 9
# left open -- whether to keep it -- is answered on both sides of the thinking.
if section run10; then
    if [ -z "${MODEL:-}" ]; then
        echo "run10 needs MODEL set, e.g. MODEL=... bash $0" >&2
        rmdir "$OUT" 2>/dev/null
        exit 1
    fi
    run_model --all-targets \
        -v summary-free:summary,summary-free \
        -v summary-free-2:summary,summary-free \
        -v summary:summary
fi

# --- run 11: how close the local writer gets ---------------------------------------------
# The commercial writer is a yardstick and will not be adopted -- one pass over the corpus
# sends 1,072 whole translations and PLAN.md section 10 is what that costs. So what remains
# before the port is how much of run 10 `ollama:qwen3.6` reaches under the same wording.
#
# Back to the pinned WRITER, and to --think, which on ollama genuinely turns thinking on --
# unlike the openai path, where PLAN.md section 11 found it only suppresses the reasoning
# summary. Runs 9 and 10 both reasoned; this is the variant of that a local model can do.
#
# Both sides of the question runs 9 and 10 left open, since the target set is run 10's and
# the ban is what decides how specific the column gets: `summary` keeps it and quotes in 0
# of 21 there, `summary-free` drops it and quotes in 29%, against the old column's 2%. Each
# is repeated, because the comparison is with run 10's phrases and a single draw of either
# would not say whether a difference is the model or the draw.
if section run11; then
    run --all-targets --think \
        -v summary:summary \
        -v summary-2:summary \
        -v summary-free:summary,summary-free \
        -v summary-free-2:summary,summary-free
fi

# --- run 12: run 11 without the thinking -------------------------------------------------
# Run 11 put `ollama:qwen3.6` under run 9's wording with --think and came back with three
# things at once: findings run 10 never reached -- the amplitude/width collapse in Greek,
# the Latin-in-Hebrew filler, `cuvanje` for conservation -- and, against those, seven false
# phrases where runs 9 and 10 had two each, and a repeat agreement of 13-14 of 21 against
# their 16 and 17. PLAN.md section 12 is the checking.
#
# What is not known is whether the reasoning caused either half. On ollama --think really
# does turn the thinking on and off, unlike the openai path of PLAN.md section 11, so this
# is the comparison runs 9 and 10 could not make: if the false phrases and the instability
# come from the reasoning, they drop here; if they come from the model, they stay and the
# next step is another local writer rather than another wording.
#
# Run 11 exactly, minus --think. The same four variants and not fewer: run 11 took
# 163m58.240s for its 84 phrases and the cost of this wording on a local writer is wall
# clock rather than tokens, so the two runs have to be the same size for their times to be
# comparable at all. The variants also have to be the same, because `summary-free` is where
# the specificity lives and dropping the reasoning is most likely to show there first.
if section run12; then
    run --all-targets \
        -v summary:summary \
        -v summary-2:summary \
        -v summary-free:summary,summary-free \
        -v summary-free-2:summary,summary-free
fi

echo
echo "########## done"
