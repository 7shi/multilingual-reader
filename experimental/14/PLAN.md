# Runs: run 1 to run 14

Working document, and a companion to [README.md](README.md). The README holds the design
and what the corpus measurements say about it; this file is the ledger of what was actually
run, because the wording kept changing and a phrase only means something against the prompt
that produced it. Run 7 changed more than a wording: runs 1-6 asked the writer to find the
lines that fall short, and run 7 asks instead for a characterisation of the translation as
a whole, which is what the column being replaced holds. The two genres are not comparable
phrase by phrase.

One section of [batch.sh](batch.sh) per wording, one `runX/` each, and nothing writes into
a directory that already has results — a section whose directory is filled is skipped. Each
section is a single call with its variants named on the command line: the targets loop on
the outside and the variants on the inside, so the original and the translation stay at the
head of the prompt across a whole group rather than being re-sent and discarded per
variant. Every superseded wording stays reachable from the
current `trend14.py` through a flag — `--locate`, `--no-line-rule`, `--axis-b`,
`--strict-level3`, `--no-original` — so each section still sends what its `runX/` was run
on, even though the phrases will not come back identical. Runs 1–6 all carry `--locate`.

**Status**: frozen, 2026-09-23. Runs 1–14 are done, 1,054 phrases, and the design is
settled: section 15 closes with it, [README.md](README.md) is the result and
[PORT.md](PORT.md) is what is left to do with it. This file is not edited again. Runs 1–8 and 11–14 are
`ollama:qwen3.6`; runs 9 and 10 are `gpt-5.6-terra`, which is a yardstick rather than a
candidate — section 10 is what its input costs. Runs 1–12 had one call write the phrase
from the translation; runs 13 and 14 go back to the old pipeline's two calls, an evaluator's
comment and a summary of it, and that is what is adopted. A two-variant attempt at run 12 was
discarded and not kept; section 13 opens with why its numbers should not be quoted.

An earlier set of runs was discarded because it repeated variants an earlier run had already
settled. Run 7 was sent as two calls, over `DEFAULT_TARGETS` and then `SLIGHT_TARGETS`, which was a
mistake: unlike run 6 the two carry the same wording and differ only in their targets, so
`gpt-5.6-luna/da` went twice under two variant names. `--all-targets` is the one-call form
and run 8 is the first to use it.

A run is not limited to one change. Runs 1–5 changed one thing each, which made them easy
to read, but the prefix of a target's prompt is cached across its variants, so a variant
costs almost nothing; from run 6 on, a run carries every change worth trying and their
combinations.

| | Wording | Variants | What it settled |
|---|---|---|---|
| [1](#2-run-1--the-wording-as-first-written) | as first written | 4 | Level 3 names places; phrases are specific where a defect exists; line numbers are fabricated; the original earns its input |
| [2](#3-run-2--a-ban-on-citing-line-numbers) | + no line numbers | 3 | The rule holds; the focus sentence does nothing |
| [3](#4-run-3--the-focus-sentence-dropped) | − the focus sentence | 2 | The phrase is stable; the level-3 ban forces fabrication |
| [4](#5-run-4--level-3-may-report-soundness) | − the ban on general assessments | 2 | Permission is not taken; the wording is not the lever |
| [5](#6-run-5--level-3-split-by-the-unrounded-minimum) | level 3 split by the unrounded minimum | 2 | The fabrication changes character but does not stop; soundness is never answered |
| [6](#7-run-6--three-rules-and-their-combinations) | + three rules, and every combination | 10 | `--sound-rule` works and is adopted; the other two are dropped; the band it reaches is 53 records of 1,072 |
| [7](#8-run-7--the-column-as-a-characterisation-not-a-location) | the genre changed: a characterisation, not a location | 6 | The form matches the old column and `da` stops fabricating; examples become a lookup; the closing line invents quantities |
| [8](#9-run-8--the-extent-asked-for-twice-taken-out) | − both requests for the extent | 4 | The quantities go, 11 of 66 to 2 of 84, and the ban on top of it buys nothing; the phrases go short with them |
| [9](#10-run-9--the-task-the-old-column-was-given-on-a-commercial-writer) | the old prompt's own task, thinking on, a commercial writer | 4 | Seven checked findings and all seven hold, `fiziky` among them; the length comes back; stable on 17 of 21 |
| [10](#11-run-10--the-same-wording-with-the-reasoning-summary-off) | the same, without `--think` | 3 | `--think` does not stop an openai model reasoning, so this is not the run it was meant to be; `summary` matches the old column's quote rate and `summary-free` is ten times it |
| [11](#12-run-11--the-same-wording-on-the-local-writer) | the same, on the local writer | 4 | Findings run 10 never reached, against three times its false phrases and a repeat agreement of 13–14 of 21 |
| [12](#13-run-12--run-11-without-the-thinking) | run 11 without the thinking | 4 | The reasoning buys obedience, not accuracy: same 7 false in 84, but the ban on pointing goes from 0–5% to 19–29% and `summary` destabilises. 56× faster |
| [13](#14-run-13--the-old-pipeline-itself-in-two-stages) | two calls: evaluate.py's prompt writes a comment on Jev's scores, trend.py's summarises it; no thinking | 4 draws | The old column's form, no quotes, 3.5 hours a pass; but the top of level 3 reads as praise, which the comments do not support |
| [14](#15-run-14--stage-2-biased-toward-the-shortfall) | stage 2 alone over run 13's comments, with a shortfall rule and Jev's level | 3 | Praise at 89+ falls from 73% to 7% and nothing is invented; a phrase is as right as its comment. `level` adopted |

---

## 1. What Was Measured Before the First Run

All of it over the 1,072 records in `examples/tr/onde/*/jev.jsonl`. Two of the three
options [experiment 13's PORT.md](../13/PORT.md) section 5 then recorded are ruled out here, and
the third is shaped by it.

### A fixed sentence from the criterion scores would be nearly constant

The lowest of the five criteria is `fluency` in 960 of 1,072 translations; `gemma4`,
`gemma4-31b`, `qwen3.6` and `union-alpha` have it lowest in all 67 of their languages.

| Lowest criterion | Records |
| --- | ---: |
| fluency | 960 |
| information_completeness | 102 |
| contextual_adaptation | 6 |
| terminology | 4 |

### Replacing the prose with the five scores would add almost nothing

Across languages, each criterion correlates with the total at Pearson 0.88–0.99, and the
five values within one record have a mean standard deviation of 0.21–0.29 levels.

| Model | readability | fluency | terminology | contextual | information |
| --- | ---: | ---: | ---: | ---: | ---: |
| gpt-5.6-luna | 0.984 | 0.881 | 0.944 | 0.972 | 0.893 |
| qwen3.6 | 0.989 | 0.970 | 0.972 | 0.993 | 0.923 |
| bonsai2-27b | 0.992 | 0.961 | 0.970 | 0.993 | 0.953 |

This is also why axis B turned out to do nothing in sections 3 and 4: the weakest criterion
is rarely a different defect, only the same defect seen through another criterion.

### The level of the weakest criterion is well spread, and its identity is not

Axis A's five buckets, and axis B's branches at 0.3 levels below the record's own mean:

| Level | Records | | Focus | Records |
| ---: | ---: | --- | --- | ---: |
| 4 | 12 | | fluency | 733 |
| 3 | 625 | | information_completeness | 47 |
| 2 | 335 | | contextual_adaptation | 6 |
| 1 | 88 | | readability | 2 |
| 0 | 12 | | nothing stands out | 294 |

Taken on its own without being fluency, `information_completeness` is the only criterion
that stands out at all — 45 records — the rest of axis B's branches being combinations with
fluency, 8 records. That is what `FOCUS_TARGETS` is built from.

### `confidence` carries information the total does not

It correlates with the total at only +0.437 (mean 0.588, sd 0.099). It says nothing about
*what* is wrong, so it is not a candidate for this column, but it is the one field of
`jev.jsonl` that nothing currently reads.

## 2. Run 1 — the wording as first written

The focus sentence on, no rule about line numbers, and the level-3 instruction that forbids
answering with a general assessment. Four variants over the eleven `DEFAULT_TARGETS`: the
design, a repeat, one without the focus sentence, and one without the English original.

**Level 3 names a place, in every variant.** `gpt-5.6-luna/da`, which the corpus's own
column calls `Professional-grade scientific translation ready for publication`, came back
with four different concrete claims. Not one of the 44 phrases could have been written
without reading the translation.

**All four of those claims are false**, which is section 4's subject and was already
visible here:

| Variant | Claim | |
|---|---|---|
| `both` | Lines 73-75: amplitude is labeled power | lines 73–75 are about evanescent waves |
| `both-2` | Luc's final lines swap speaker roles with Camille's | all 99 speaker attributions match the original |
| `axis-a` | Lines 41-42 swap speakers' responses | those two lines match the original exactly |
| `no-original` | Lines 37-38 omit "i anden" from psi squared | those lines are classical optics; `i anden` appears four times elsewhere |

**Where a defect exists the phrases are specific and check out.** `bueno` really does
intrude in `qwen3.6-27b/el` line 1; `האם` really is what `Camille: Hmm.` became in
`qwen3.6/he` line 23; `इतिहासमा` really does repeat **51 times** inside one line of
`bonsai2-27b/ne`, against the old column's `Severe infinite text repetition loop`.

**Line numbers are fabricated**: six citations in 44 phrases, and the three checked above
are all wrong. The prompt carries no line numbers, so the writer is counting, which is
experiment 11's own finding reproducing.

**`--no-original` is rejected.** Without the original the writer makes claims about it
anyway, and gets them wrong: `Inconsistent mixing of French and Greek phrases` for a
translation whose intruder is the Spanish `bueno`, and
`Lines where Kamille and Lyk switch roles` for one whose speakers are in order. Halving the
input is not worth it; the flag stays so the rejection can be re-run.

**Changed for run 2**: a ban on citing line numbers, with quoting the words put in its
place.

## 3. Run 2 — a ban on citing line numbers

`both` repeats run 1's configuration with the rule added. The two `focus-*` variants are
the first over `FOCUS_TARGETS`, the set weighted toward the criteria the focus sentence can
point at: `DEFAULT_TARGETS` has three such rows in eleven, which is why run 1 could not
settle anything about it.

**The rule works.** Zero numbered citations in 33 phrases, against six in run 1's 44, and
none in the 55 that followed. `line` survives only in its ordinary sense.

**The focus sentence does nothing, on the set built for it.** The focused and unfocused
variants land on the same family of defect in **all eleven rows** — omission and speaker
structure throughout, since that set is chosen for `information_completeness`. Specificity
splits both ways rather than favouring either: without the focus, `gpt-5.6-terra/es` names
the omitted sentence (`omits "Or its 'height', if you prefer."`); with it, the same row says
only `Camille's line missing "It's the square of its amplitude" context`.

Section 1 already contained the explanation. The five criteria correlate with the total at
0.88–0.99, so the weakest one is rarely a different defect; it is the same defect seen
through another criterion, and a writer reading the text arrives at it either way.

**Changed for run 3**: the focus sentence off, behind `--axis-b`.

## 4. Run 3 — the focus sentence dropped

The level alone, twice over `DEFAULT_TARGETS`.

**The phrase is stable on the defect it names.** Counted by the defect identified rather
than by the wording, `main` and `main-2` agree on eight of eleven rows. The rows that move
are level-3 rows, where the rubric says one to three lines fall short and the writer picks
one of them — `he` names the `האם` mistranslation in one run and the `מmm מm` garbling in
the other, and both are really there.

**The level-3 ban forces fabrication on a translation that has nothing to find.**
`gpt-5.6-luna/da` scores 92.2 and is level 3:

| Variant | Claim | |
|---|---|---|
| `main` | Luc's "Hvad synes du?" should be Camille's line | line 97 is `Camille:` |
| `main-2` | "differens" is wrong for diffraction | `differens` does not occur in the file |

Taking the speaker names alone and diffing them against the original, **all 99 lines
match**, so there is no swap to find, in this run or run 1's. By contrast `qwen3.6/he` at
71.2 is right in both runs, as are the `πλάτος` and missing-speaker-label claims for `el`
and `sv`.

**It is not only that row, and not only level 3.** `main` told `qwen3.6-27b/el` — level 2,
50.8 — that `Speaker names swapped to 'Luc' instead of 'Camille' at the end`, and the end
of that translation is in order. Speaker attribution is what the writer reaches for when it
has been told a defect exists and cannot find one.

The instruction is what does it. `Do not answer with a general assessment of quality: a
phrase that could have been written without reading the translation is not an answer`
closes the escape hatch, and the writer invents rather than leave the answer empty.

**Changed for run 4**: the ban replaced by permission to report soundness, with inventing a
defect forbidden in its place.

## 5. Run 4 — level 3 may report soundness

```
If you cannot locate the shortfall, say that the translation reads as sound -- that is
a valid answer. What is not an answer is a defect you did not find in the text.
```

**The permission is not taken.** `gpt-5.6-luna/da` fabricated again, in both runs:

| Variant | Claim | |
|---|---|---|
| `main` | "fortsat" should be "fortsæt" | neither string occurs in the file |
| `main-2` | Ambiguous speaker attribution for final lines | all 99 attributions match |

Four attempts at this wording across two variants, four false claims — and the rows that
have real defects are unaffected, naming the same things they named under the ban.
`gpt-oss/sv` shows the seam: the missing speaker label at line 16 is real, and the phrase
describing it, `"Luc: Ah ja." lacks Camille label`, quotes a label that is not there and
names the wrong speaker.

**So the wording is not the lever.** Permission to demur sits after an instruction that has
already asserted the shortfall exists, and the assertion wins. What would have to change is
what is asserted.

**The number to assert it from is already on hand.** Level 3 is 632 records whose weakest
criterion runs from 2.50 to 3.49, and rounding is what throws away the part that matters:

| | Weakest criterion | Jev total | Its claims |
|---|---:|---:|---|
| gpt-5.6-luna/da | **3.40** | 92.2 | fabricated, 8 of 8 across all four runs |
| gpt-oss/sv | 2.55 | 71.2 | real |
| gemini-3.7-flash/el | 2.53 | 68.0 | real |
| qwen3.6/he | 2.51 | 71.2 | real |

The level-3 band's 90th percentile is 3.28, so `da` sits in its top tenth and the three
that behave sit at its floor.

## 6. Run 5 — level 3 split by the unrounded minimum

Above `LEVEL_3_SLIGHT_MIN`, 3.3, the instruction stopped asserting one to three lines:

```
The evaluation found this translation almost entirely sound. What falls short of the
criteria is slight -- a shade of wording rather than anything necessarily visible as a
mistake -- so there may be nothing you can point at. Look for it; if you find
something, name it from the text. If you do not, say that the translation reads as
sound. Do not manufacture a defect to fill the answer.
```

Over `SLIGHT_TARGETS` — eleven of the corpus's 53 records at 3.3 or above, across eight
models and ten languages, with `gpt-5.6-luna/da` at the head because all four earlier runs
fabricated about it. The rows below the threshold were not re-run: their instruction is
unchanged from run 4.

**Soundness is never answered.** All 22 phrases name a defect. Not one says the translation
reads as sound, although the instruction offers it in as many words. Whatever is driving
the writer to produce a finding, it is not the sentence that asserts the shortfall — that
sentence is gone here and the behaviour is the same.

**The fabrication changes character.** `da` stops inventing speaker swaps and words that
are not in the file, and starts quoting real strings and arguing about them:

| Variant | Claim | |
|---|---|---|
| `main` | `"samme bølgelove" should be "samme bølgelover"` | the quoted string is really there; the correction is doubtful — `bølgelove` is the ordinary Danish plural |
| `main-2` | `"samlet sandsynlighed" should be "samlede sandsynlighed"` | inverted: the file has `samlede`, not `samlet` |

That is an improvement — a claim anchored to the text can be checked — and it is not a fix.

**One row found something real.** `union-alpha/sk` in both variants points at `jednoty
fiziky` on line 43, where Slovak wants `fyziky`, and `main-2` gives the correct form. The
phrasing is sloppy (`unity of fiziky`, `unité de fiziky`) but the finding is right and the
existing column does not have it.

**A new failure: judging the back-translation.** `ox-alpha/ru` is wrong in both variants —
`Camille misattributes Luc's final line to herself` when the last three lines match the
original, and `"psi in squares" should be "psi squared"` when line 17 reads `пси в
квадрате`, which *is* psi squared. `unity of fiziky` and `"sense of wonder" mistranslated as
"Naruhodo"` are the same move: the writer renders the target text into English and judges
the rendering. `sense of wonder` does not occur in the original at all, and `なるほど`
occurs six times perfectly well.

**Changed for run 6**: three rules, below.

## 7. Run 6 — three rules and their combinations

Ten variants, 110 phrases: eight over `SLIGHT_TARGETS` — `base`, each rule alone, each
pair, all three — and two over `DEFAULT_TARGETS`, the control and all three. Every phrase
below was checked by section 17's procedure; the speaker check was run over all eleven
slight targets at once, mapping each file's speaker labels to their first-seen order, and
**all eleven match the original on all 99 lines**, so every speaker claim made about them
in this run is false.

**One of the three rules works, and it is the one that decides the design.**

| Rule | Verdict |
|---|---|
| `--sound-rule` | Works, overwhelmingly. 0 of 22 becomes 41 of 44 |
| `--backtrans-rule` | No effect on the class it names; the rate is no better than the control's |
| `--quote-rule` | Fails, and makes quoting worse. Dropped |

### `--sound-rule` moves the 0 of 22 to 41 of 44

Across the four variants carrying it, 41 of 44 phrases answer that the translation reads as
sound. `sound-backtrans` answers it on all eleven; `sound`, `sound-quote` and `all` each
name a defect on one row. Against run 5's 0 of 22 under the permissive wording, and against
1 of 44 in this run's four variants without the rule — `base`'s `slight wording shading
rather than visible mistake` on `union-alpha/sk`, which is a demurral rather than the
answer the instruction offers.

**All three defects that survive the rule are false.** `sound` gives `gpt-5.6-luna/uk`
`Minor typos "псі" for psi and "Е" for E squared`: `псі` is the ordinary Ukrainian for psi
and line 37's `Е у квадраті` renders the original's own `E squared`. `sound-quote` and
`all` both pick `gemini-3.7-flash/ja` — a double negative that is in the English source
(line 94, `is not just a simple calculating tool`), and `プサイ二乗の法則`, which is exactly
`the law of psi squared`.

Note that the flag changes two things at once: the slight branch's wording, and the closing
line, which under the rule reads `Say in one short phrase what you found, or that it reads
as sound` instead of `WHERE the problem is and WHAT it is`. Run 5 changed only the branch
and moved nothing. Which of the two carries the effect is not separated here, and the
closing line is the likelier one: it is the last thing the writer reads, and it is the only
place in run 5's prompt that still demanded a location unconditionally.

### What it costs: the true findings in the band

`union-alpha/sk` line 43 reads `jednoty fiziky` where Slovak wants `fyziky`. It is the one
run 5 found, and **all four `sound-*` variants report the row as sound.** The three variants
without the rule keep it, though none states it cleanly — `unit of fiziky` (`backtrans`),
`unity fiziky` should be `unity fyziky` (`quote`), `"unit of physics" mistranslated as
"unity of fiziky"` (`backtrans-quote`); each half-translates the real string, so none of
the three would survive a mechanical quote check either.

> **Corrected after run 8.** This section first called `fiziky` the only true defect in the
> band and `base`'s eleven phrases false to a row. Both are wrong, and the error was mine
> rather than the writer's: I checked `ox-alpha/ru`'s pronouns by reading the lines that
> contain `ты`, and did not look for the lines that contain `Вы`. Section 13 now carries
> the check that would have caught it. Three of the eleven slight targets — `ox-alpha/ru`,
> `gemma4-31b/ru` and `gpt-5.6-luna/uk` — really do mix the two registers between the same
> two speakers, which run 8 found unanimously and which the corpus's own column never
> named:
>
> | | Formal, between the hosts | Informal, between the same two |
> | --- | --- | --- |
> | `ox-alpha/ru` | 12 `Вы хотите сказать` (Luc→Camille), 51 `Вы абсолютно правы` | 35 `с твоей областью`, 40 `Подожди`, 69 `Продолжай` |
> | `gemma4-31b/ru` | 12 `Вы имеете в виду`, 15 `если вам так удобнее` | 40 `Погоди`, 45 `Давай`, 51 `Ты совершенно прав` |
> | `gpt-5.6-luna/uk` | 51 `Ви цілком маєте рацію` | 15 `якщо хочеш`, 35 `твоєю`, 69 `Продовжуй` |
>
> So `base`'s `"твоей" should be "вашей" to match formal address` was pointing at something
> real and is not one of this run's false claims, and `backtrans`'s `Camille addresses Luc
> with "ты" instead of "вы" in one instance` is exactly right. The counts below are
> unchanged in kind but one row lighter.

So the trade on this band is one true finding lost against nine false ones removed.
Counting the control: `base` names a defect on all eleven rows and **ten of them are
false** — `"Ah, sí?" should be "Ah? Quina?"` (line 16 reads `Ah, sí.`, and the correction is
invented), `"ăă" should be "mhm"` (line 29's `ăă` renders the original's `uh`; it is a
hesitation, not a backchannel), a gender mismatch in a Russian line that marks no gender,
and a truncated, self-contradicting `"Lambda (λ) used where Greek lambda should be`.

### A failure class neither rule names: demanding notation the original spells out

Eight phrases across the three rule-bearing variants and `base` fault a translation for
writing psi squared or lambda over two in words: `"psi al quadrat" instead of "psi²"`,
`"lambda entre dos" should be "lambda/2"`, `"psi na kvadrat" misrenders psi squared as a
phrase rather than a symbol`, `"Lамбда, поділену на два" should be "лямбда/2"`. The
original writes `psi squared` and `lambda over two` in words itself, so every one of these
asks the translation to be less faithful than it is. `--quote-rule` raises the count rather
than lowering it, since the correction it puts in the writer's hand is a notation string.

This is the back-translation failure wearing another hat, which is why `--backtrans-rule`
was aimed at the wrong target.

### `--backtrans-rule` does not remove the class

Four of eleven `backtrans` phrases judge an English rendering, the same rate as run 5's
four of 22 and worse than `base`'s: `"unit of fiziky"`, `"Посылая электроны по одному"
lacks 'one' vs "one by one"` (line 20 reads `посылая электроны по одному`, which is `one by
one`), `"height", si prefieres` (the file translates it as `altura`), and
`"sandsynligheden gives of dens" should be "givet ved"` — where the writer has copied line
83's Danish `gives af` as English `of`, mid-quotation, and then corrected the correct form.
`backtrans-quote` carries three more, including `"хитроумных" instead of clever`.

### `--quote-rule` fails, and a quoted string still cannot be checked mechanically

Of 21 quoted strings in `quote`, nine occur in neither file. The rule asked for corrections
to move outside the quotation marks and they did not — `"ψ²"`, `"psi-squared"`,
`"lambda/2"`, `"unity fyziky"`, `"/2"` are all corrections still inside them. Worse, the
rule did not make the citations exact either: `"Što misite?"` for line 97's `Što mislite?`,
`"Lамбда"` with a Latin L, `"unity fiziky"` for `jednoty fiziky`, `"probability of
presence,"` as an English gloss of a Danish phrase.

So a quoted string missing from both files remains ambiguous between a fabrication and a
mangled citation, which is exactly what the rule was supposed to resolve, and the automatic
filter section 17 hoped for does not follow. The control is not worse: `base` has four of
twelve in neither file, three of them corrections.

`quote` also produced a claim that is inverted as well as misquoted — `Camille says "Što
misite?" instead of the plural form to address the audience`, where `Što mislite?` *is* the
plural form.

### The rules do not suppress a true finding

`default-all` keeps every real defect `default-base` names: the `האם` and `המהמה`
mistranslations in `qwen3.6/he`, `πλάτος` for both width and amplitude in
`gemini-3.7-flash/el`, the missing speaker labels in `gpt-oss/sv`, the Nepali repetition,
the truncated Thai, the Spanish `bueno` in `qwen3.6-27b/el`, and the three level-1 and
level-0 rows. `gpt-5.6-luna/it` at level 4 stays praise. And `gpt-5.6-luna/da` — the row
the experiment is named after, false in all ten phrases across runs 1–5 — answers `Reads as
sound`.

Two qualifications. `default-all`'s `gpt-oss/sv` phrase is *more* specific than the
control's and wrong in the added part: `Missing Camille label before "Det är amplitudens
kvadrat."` — line 15 has its `Camille:` label, and the lines actually missing one are 14 and
16, which are Luc's. Run 4 produced the same seam. And only `da` is in the slight branch,
so this variant says nothing about `--sound-rule` on the other ten rows; what it tests is
`--backtrans-rule` and `--quote-rule`, which is the right test for the two being dropped.

### The combinations do not interact; one rule dominates

`--sound-rule` decides the answer whichever of the other two accompanies it, and the other
two have nothing left to act on once the answer is `reads as sound` — there is no quotation
to regulate. Without it, the two are visible only in which false claim gets named, not in
how many: eleven false in `base`, ten in `quote`, ten in `backtrans`, ten in
`backtrans-quote`. The one interaction worth recording is a negative one: `backtrans-quote`
produced three speaker-swap claims (`da`, `ca`, `gemma4-31b/ru`) where `base` produced none,
the fabrication run 3 named returning under a pair of rules meant to suppress it.

### What run 6 settles, and what it opens

Settled: `--sound-rule` is adopted and becomes the slight branch's wording;
`--backtrans-rule` and `--quote-rule` are dropped, and stay as flags. The slight branch's
answer is now `reads as sound` in 41 of 44, and on this band that is the right answer in
ten rows of eleven.

Opened, and why this is not yet the wording to port:

1. **The rule reaches 53 records of 1,072.** `LEVEL_3_SLIGHT_MIN` is 3.3 and the level-3
   band holds 625; the branch below it still carries run 4's wording, whose behaviour is
   known only from `DEFAULT_TARGETS`' four rows.

   | Weakest criterion | Records | Instruction |
   | --- | ---: | --- |
   | 3.30–3.49 | 53 | the slight branch — `--sound-rule` |
   | 3.00–3.29 | 191 | run 4's, unchanged |
   | 2.75–2.99 | 195 | run 4's, unchanged |
   | 2.50–2.74 | 186 | run 4's, unchanged |

2. **The threshold is not shown to be in the right place.** The 3.00–3.29 band's top is
   `union-alpha/sq` at 3.29 and total 91.9, above every one of `SLIGHT_TARGETS` but
   `qwen3.8/es`, and twelve records in that band total 90.9 or better. Nothing distinguishes
   them from the slight band except a cut that was chosen from the 90th percentile of runs
   1–4's fabrications.

3. **Notation.** The class in the third subsection above is untouched by anything run so
   far, and it is not confined to the slight band: it is what the writer reaches for on any
   row whose technical vocabulary is spelled out in words.

## 8. Run 7 — the column as a characterisation, not a location

Runs 1–6 all asked for the lines that fall short and what is wrong with them, and every
failure they turned up was a failure at pointing. After run 6, the column being replaced
was measured for the first time, and it never pointed at anything:

| | Old `analysis`, 1,072 entries |
| --- | --- |
| Length | median 5 words, longest 11 |
| A quotation mark | 23 entries, always a single word |
| A line number | none |

It is `<severity> <kind of defect>` about the translation as a whole — `Minor stylistic
phrasing issues`, `Severe structural corruption and gibberish` — and the severity word
tracks the score almost monotonically:

| Opening word | Entries | Median old score | | Jev level | Entries | What the old column opened with |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| Severe | 162 | 32 | | 4 | 12 | Exceptional, Excellent |
| Pervasive | 42 | 44 | | 3 | 625 | Minor (298 of them) |
| Critical | 40 | 57 | | 2 | 335 | Severe, Pervasive, Significant, Critical |
| Significant | 28 | 65 | | 1 | 88 | Severe (58), Pervasive (11) |
| Notable | 13 | 74 | | 0 | 12 | Severe |
| Minor | 327 | 91 | | | | |
| Excellent / Exceptional | 28 | 96–97 | | | | |

So the level supplies the register and the writer supplies the kind — which is the one
thing runs 1–6 got right even where the location was invented. The genre changes, and runs
1–6 move behind `--locate`.

Six variants, 66 phrases: `char` and its repeat, `char-ex` with seven old entries shown as
the shape, and `char-word` opening the old column's single-word exception, over
`DEFAULT_TARGETS`; then `slight-char` and `slight-char-ex` over `SLIGHT_TARGETS`.

**The form lands exactly.**

| | Run 7, 66 phrases | Old column |
| --- | ---: | ---: |
| Median words | 5.0 | 5.0 |
| Mean words | 5.2 | 5.5 |
| Longest | 10 | 11 |
| Line numbers | 0 | 0 |

**And `gpt-5.6-luna/da` stops fabricating.** Not one of its four `char*` phrases claims a
speaker swap, a word that is not in the file, or a correction to correct Danish — the first
time in seven runs. What is wrong with them is new and is below.

### `--examples` is rejected: the seven become a seven-way lookup

Eight of the 22 phrases written with the examples shown are one of them, verbatim.

| Variant | Target | Phrase |
|---|---|---|
| `char-ex` | `gpt-5.6-luna/it` | `Exceptional quality, nearly perfect` |
| `char-ex` | `bonsai2-27b/ne` | `Severe machine-translation artifacts` |
| `char-ex` | `gemma4/ga` | `Severe structural corruption and gibberish` |
| `char-ex` | `gemma4-31b/ia` | `Severe machine-translation artifacts throughout` |
| `slight-char-ex` | `gpt-5.6-luna/ro` | `Minor terminology inconsistencies and anglicisms` |
| `slight-char-ex` | `union-alpha/sk`, `ox-alpha/hr`, `gemini-3.7-flash/ja` | `Minor stylistic phrasing issues` |

Three different translations answered with one string is a column that does not distinguish
them, whatever it reads like. The examples convey the shape, and the shape was already
being reached without them: `char` and `char-2` hit the old column's length distribution
with nothing shown.

### A failure the genre introduced: a quantity the prompt never gave

Eleven of 66 phrases carry a number, and where it can be checked it is wrong.

| Variant | Target | Phrase |
|---|---|---|
| `char` | `gpt-oss/sv` | `Missing speaker labels for three lines` |
| `char-2` | `gpt-oss/sv` | `Missing speaker labels for three lines` |
| `char` | `qwen3.6/he` | `minor lexical errors and noise affecting approx 1% of text` |
| `char` | `gpt-5.6-luna/da` | `Minor register shifts affecting approx three lines near the end` |
| `char-2` | `gpt-5.6-luna/da` | `Minor lexical oddities affecting approx 5% of text` |
| `char-word` | `gpt-5.6-luna/da` | `minor semantic inaccuracies affecting approximately 10 lines` |
| `slight-char` | `qwen3.8/es` | `Literal phrasing affecting ~15%` |

`gpt-oss/sv` has **eight** lines without a speaker label — 13, 14, 16, 22, 24, 25, 27 and
94 — not three, and both variants that count say three. `gpt-5.6-luna/da` gets three
different magnitudes for one translation across three variants of one wording: about three
lines, about 5%, about ten lines.

The instruction asks for it. `CHARACTER_CLOSING` says `the KIND of thing that falls short
and how far through the text it reaches`, and the second half is the extent the level has
already given — the writer converts a level into a number rather than taking it as given.
`char-ex` and `slight-char-ex` have none of this, because none of the seven examples holds
a number; that is the one thing showing them bought.

### The ban on pointing holds in part

Twelve of 66 still point: `near the end`, `final lines`, `beyond first line`, `in Luc's
lines`, `through evanescent waves section`, and the quoted words `--word-rule` permits.
`char-word` is the worst of the four at this, which is what opening the exception costs.

One of them is right. `char`'s `Repetitive garbled text through evanescent waves section`
for `bonsai2-27b/ne` names line 74, and line 72 is the evanescent-waves line, so the
location is correct even though the phrase should not have carried one.

### What checks out, and what does not

Real, and named in the right register by every variant: the missing speaker labels in
`gpt-oss/sv`, the Spanish intrusion in `qwen3.6-27b/el`, the truncation in `qwen3.8/th`,
the repetition in `bonsai2-27b/ne`, and the level-1 and level-0 collapses in `gemma4/ga`,
`gemma4-31b/ia` and `bonsai2-27b/cy`. `gemini-3.7-flash/el`'s `Terminology errors: 'width'
vs 'amplitude'` is exactly the `πλάτος` defect runs 1–6 found. `gpt-5.6-luna/it` at level 4
is praise.

False, and all of them in the specific half of a phrase rather than the general half:

| Variant | Target | Claim | |
|---|---|---|---|
| `char-word` | `bonsai2-27b/ne` | `Repetitive intruding Chinese text fragment` | the repetition is Nepali `इतिहासमा` on line 74; the file holds exactly one Chinese character, `细` on line 66 |
| `char-word` | `bonsai2-27b/cy` | `Nonsense beyond first line` | line 1 is already broken — `Hello i bobbynnau`, `podcadweddion` |
| `char-word` | `qwen3.6/he` | `terminology for 'delta' symbols` | `דלתא` occurs on line 58 alone, twice, identically |
| `slight-char` | `union-alpha/sk` | `terminological inconsistency regarding 'evanescent waves'` | line 72's `evanescentnými vlnami` is the standard Slovak term and occurs once |
| `slight-char-ex` | `gpt-5.6-luna/uk` | `terminology inconsistency for 'lambda'` | `лямбда` occurs three times in one form |
| `slight-char-ex` | `qwen3.8/es` | `Minor translation artifact "eh"` | line 29's `una razón matemática, eh...` renders the original's own `uh` |

`slight-char`'s `Inconsistent use of ты form in Luc's speech` for `gemma4-31b/ru` is
**true**, which this section first recorded as half right on the ground that the shifting
register was Camille's. Luc's is too: he says `Вы имеете в виду` on line 12 and `Погоди` on
line 40, to the same person. The correction is section 7's and the check is section 17's.

**`union-alpha/sk` line 43's `jednoty fiziky` is missed again**, by both slight variants, as
it was by all four of run 6's `sound-*`. The one real defect in that band has now escaped
six wordings.

### Most of this genre cannot be checked, and that is the point

`Minor stylistic phrasing issues` and `minor register inconsistencies throughout` are not
claims a `grep` can refute, and neither were the 1,072 entries being replaced. Section 13's
procedure applies only where specificity leaks through — a quantity, a quoted word, a
speaker, a language name — and in run 7 that is precisely where the phrases are wrong. The
generality is doing the work the pointing could not.

### Changed for run 8

1. **Drop `and how far through the text it reaches` from `CHARACTER_CLOSING`**, or forbid
   stating a magnitude outright. It asks the writer for what the level already gave, and it
   is where every invented number comes from.
2. **`--examples` is not adopted.** It buys suppression of the numbers at the price of the
   column, so the numbers have to be suppressed by the closing line instead.
3. **`--word-rule` is doubtful.** It is the old column's own 2%, but three of the four
   false phrases above are in the variant that opens it, and each one is a word the writer
   went looking for.

## 9. Run 8 — the extent, asked for twice, taken out

Run 7 asked how far the defect reaches in the two places a writer reads last, and got the
answer in numbers nobody had supplied. Both clauses go:

| | Run 7 | Run 8 |
| --- | --- | --- |
| `CHARACTER_CLOSING` | `the KIND of thing that falls short **and how far through the text it reaches**` | `the KIND of thing that falls short` |
| `NO_POINTING_RULE` | `what kind of thing is wrong **and how much of the translation it affects**` | `what kind of thing is wrong` |

`--extent-clause` restores both together. Four variants, 84 phrases, one call over
`--all-targets`: `drop` is the removal alone and `drop-2` its repeat, `no-mag` adds an
explicit ban on stating a magnitude, and `no-mag-word` carries that with the old column's
single-word exception. `--examples` was not repeated.

### The removal works, and the ban on top of it does nothing

| Variant | A quantity |
| --- | ---: |
| `drop` | 0 / 21 |
| `drop-2` | 1 / 21 |
| `no-mag` | 0 / 21 |
| `no-mag-word` | 1 / 21 |
| **Run 8** | **2 / 84** |
| Run 7 | 11 / 66 |

`drop` alone reaches zero and `no-mag` does not improve on it; the two survivors are in the
repeat and in the variant that also opens the word exception. **So `--no-magnitude` is not
adopted.** Run 4 is the precedent that made it worth trying — there, removing the sentence
that prompted a behaviour left the behaviour untouched — and it does not repeat here. The
difference is that run 4 removed a *permission* and left the assertion it sat under
standing, whereas run 8 removed the request itself.

Quoted strings fall with it, from 12 of 66 to 8 of 84, without any rule aimed at them.

### What it costs: the phrases got shorter than the column they replace

| | Run 8 | Run 7 | Old column |
| --- | ---: | ---: | ---: |
| Median words | 4.0 | 5.0 | 5.0 |
| Mean words | 4.4 | 5.2 | 5.5 |
| Longest | 9 | 10 | 11 |
| Three words or fewer | 28 / 84 (33%) | 8 / 66 (12%) | — |

`Register inconsistency`, `pronoun inconsistency`, `garbled text`, `Truncated ending`,
`Translation artifacts`. The clause was carrying half the phrase, and taking it out took the
half with it rather than only the invented numbers. Between six and nine phrases per variant
now carry no word of severity or quality at all, `bonsai2-27b/cy` at level 0 answering
`garbled text` where the old column has `Severe corruption and repetition loops`.

### It finds three things the old column never had

All confirmed against the files.

| Target | Variant | Phrase | |
|---|---|---|---|
| `gemini-3.7-flash/ja` | `no-mag` | `Inconsistent term for 'ψ'` | the file writes it `プサイ` five times and `ψ` twice |
| `qwen3.6/es` | `no-mag-word` | `inconsistent use of quotation marks` | five `« »` pairs and four `"`, against the original's `"` throughout |
| `qwen3.8/th` | `no-mag` | `Inconsistent speaker attribution labels` | lines 3–26, twenty-four consecutive lines, carry no speaker label |

The Thai row is the sharper one: the other three variants and every earlier run answered it
with the truncation at line 98, and the missing labels are the larger defect by an order of
magnitude.

**And the register mixing is found unanimously.** `ox-alpha/ru`, `gemma4-31b/ru` and
`gpt-5.6-luna/uk` each draw a phrase about inconsistent address from all four variants —
`inconsistent register shifts to informal address`, `pronoun inconsistency`, `Inconsistent
second-person pronoun usage`, `inconsistent address forms`. Section 7's correction is the
evidence; the corpus's own column names it in none of the three.

### What is false

| Variant | Target | Claim | |
|---|---|---|---|
| `no-mag` | `gpt-5.6-luna/da` | `Literal translation of 'psi i anden' for 'psi squared'` | `psi i anden` occurs four times and *is* the Danish for psi squared. Run 1's `--no-original` variant got the same string wrong |
| `drop` | `gemma4-31b/ru` | `Inconsistent speaker names (Kamil/Luc vs Kamiel/Luke)` | `Камиль` 50 times and `Люк` 49; neither Latin form occurs |
| `drop-2` | `ox-alpha/hr` | `unnecessary filler word "uh"` | line 29 renders the original's own `uh` |
| `drop-2` | `qwen3.8/es` | `unnecessary filler word "eh"` | the same line, the same error, in a second language |
| `no-mag-word` | `gpt-oss/sv` | `Missing speaker labels for two lines` | eight |

`gpt-oss/sv` is the whole run in one row. Eight lines carry no label — 13, 25 and 27 are
Camille's and 14, 16, 22, 24 and 94 are Luc's — and the four variants answer:

| Variant | Phrase | |
|---|---|---|
| `drop` | `Missing speaker names for Luc's lines` | five of the eight |
| `no-mag` | `Inconsistent character attribution for Camille's lines` | three of the eight |
| `no-mag-word` | `Missing speaker labels for two lines` | false |
| `drop-2` | `Missing speaker names in several lines` | **right** |

The vaguest of the four is the only accurate one, and it is the only one that survived the
quantity purge with a word instead of a number. Where the writer is specific it is specific
about the wrong half.

### The phrase is less stable than it was under the other genre

Counting by the kind of defect named rather than the wording, `drop` and `drop-2` agree on
**eleven of 21 rows**, against run 3's eight of eleven in the location genre. The rows that
move are level 3 and they move between characterisations that are each defensible:
`gpt-5.6-luna/ro` gets `inconsistent formatting of squared terms` and `minor register
inconsistency`, `ox-alpha/hr` gets `Minor register inconsistencies` and `unnecessary filler
word "uh"`, `union-alpha/sk` gets `minor register inconsistencies` and `Minor awkward
phrasing`.

This is the genre's own shape rather than a wording fault. A level-3 translation has several
things slightly off and the instruction asks for the kind, so any of them answers it. Under
`--locate` the writer had to name a place, which pinned it. Whether a column that names a
different true-ish aspect on a re-run is acceptable is not a wording question, and section 18
is where it has to be settled. Run 9 settles it after all.

### Changed for run 9

1. **Keep the removal; drop `--no-magnitude`.** It buys nothing over `drop`.
2. **Put the length back without putting the number back.** The instruction now asks for a
   kind and nothing else, and 33% of the answers are three words. The old column's median is
   five, and its second element is a qualifier — `Minor stylistic phrasing issues`, `Severe
   structural corruption and gibberish` — not a magnitude. Asking for the register word
   explicitly is the obvious candidate and has not been tried.
3. **`--word-rule` is still doubtful and still not settled.** It produced two of the run's
   three new true findings and one of its five false ones, which is better than run 7's
   showing and not conclusive either way.

## 10. Run 9 — the task the old column was given, on a commercial writer

Runs 7 and 8 asked the writer to characterise a translation it had just read, and that is
not how the column being replaced was made. `trtools/trend.py` hands an LLM the
`overall_comment` of three evaluation runs and asks it to summarise them: its writer never
saw the translation, and the phrase is a summary of someone else's verdict. Under Jev there
is no verdict, so the writer's own reading has to be it — which is why this is the first
section to run with thinking on. The reasoning plays the part of the `overall_comment` and
the phrase is its summary, in the same relation the old pipeline had.

The closing line and the output format are `trend.py`'s own sentences, and `SUMMARY_LEVELS`
strips the level to the extent alone, standing in for that prompt's `Trust these evaluations
as given`. The register word goes with the rest of the level's instruction: the old prompt
supplied none, its writer taking severity from the evaluations' prose. One sentence has no
equivalent — `An issue mentioned in multiple runs is more reliable than one mentioned only
once` — because there is one reading here and not three.

Three things change at once: the genre, thinking, and the model, which is `gpt-5.6-terra`
rather than the `ollama:qwen3.6` of runs 1–8. `drop` is carried over as the control — run 8's
wording on this writer — so the prompt can be told from the model. Four variants over
`--all-targets`, 84 phrases, one call.

### The form

| | Median words | Three words or fewer | Quoted strings | A quantity |
| --- | ---: | ---: | ---: | ---: |
| Run 8 `drop`, `qwen3.6` | 4.0 | 10 / 21 | 2 | 0 |
| Run 9 `drop`, `gpt-5.6-terra` | 4.0 | 7 / 21 | 0 | 0 |
| Run 9 `summary` | 5.0 | 0 / 21 | 1 | 0 |
| Run 9 `summary-2` | 5.0 | 1 / 21 | 0 | 0 |
| Run 9 `summary-free` | 6.0 | 0 / 21 | 7 | 0 |
| Old column | 5.0 | — | 23 / 1,072 | — |

**The 8-word ceiling put the length back without putting the number back.** Run 8 fixed the
invented quantities by taking the extent out of the instruction and lost a word and a half
of phrase with it, a third of its answers coming back at three words or fewer. The old
prompt's own ceiling recovers the median exactly, and no variant states a magnitude. The
model alone does not do this: `drop` on `gpt-5.6-terra` still medians at four.

### What it finds

Every specific claim below was checked against the files and **every one of them holds**.

> **Corrected after run 10.** This section read the seven as the run's achievement. They are
> not: the column being replaced quotes in 2% of its 1,072 entries and `summary-free` quotes
> in 33% of 21, so naming them at all is over-shooting what the column does. What they
> establish is narrower and still worth having — a writer that names seven strings and gets
> seven right is not fabricating, which no earlier run could say. Section 11 has the
> measurement and the variant that matches the old rate.

| Target | Variant | Phrase | Checked |
|---|---|---|---|
| `union-alpha/sk` | `summary-free` | `Minor Slovak typo: "fiziky" instead of "fyziky"` | line 43 |
| `gemini-3.7-flash/el` | `summary-2`, `summary-free` | `Mistranslates evanescent waves as evaporating waves` | line 72 reads `εξατμιζόμενα κύματα` |
| `ox-alpha/hr` | `summary-free` | `Serbian word "stubova" instead of Croatian` | line 17; Croatian is `stupova` |
| `qwen3.8/es` | `summary-free` | `Missing accent in "atenuan"` | line 74; Spanish needs `atenúan` |
| `gemini-3.7-flash/ca` | `summary-free` | `Nonstandard Catalan word choice: "bril·lança"` | line 37 |
| `gpt-5.6-luna/ro` | `summary-free` | `Minor typo: "brilanța" misspells "brilianța"` | line 37 |
| `qwen3.6/es` | `summary-free` | `Minor inconsistent formal address: "tenga" / "Siga"` | lines 68 and 69, against `tú` elsewhere |

**`union-alpha/sk`'s `fiziky` is found at last.** It is the defect that escaped runs 5
through 8 — missed by every `sound-*` variant of run 6, by both slight variants of run 7 and
named only as `Slovak term mismatch` in run 8 — and `summary-free` gives both the error and
the correction.

**`stubova` is the finding nothing else in this experiment could have produced.** Croatian
and Serbian differ here by one vowel, the word is otherwise unremarkable, and no rubric
level or focus criterion points at it. The old column for that row says `Minor terminology
issues and stylistic calques`.

The register mixing of `ox-alpha/ru`, `gemma4-31b/ru` and `gpt-5.6-luna/uk` — section 7's
correction — is named by every variant here as it was in run 8.

### What is false

One row, and the same class it has always been.

| Variant | Target | Claim | |
|---|---|---|---|
| `summary-2` | `gemini-3.7-flash/ja` | `Conflates optical power with amplitude` | line 48 reads `その出力、つまり振幅`, which is the original's own `its power, so the amplitude` |
| `summary-free` | `gemini-3.7-flash/ja` | `Minor terminology inconsistency: classical mechanics for optics` | line 37 is `古典光学` and line 93 `古典力学`, and the English shifts the same way at the same two lines |

`gpt-5.6-luna/da`'s `Awkward phrasing: "kvadratiske amplitude"` is the weakest of the seven
quotes rather than the eighth false one: the string is on line 83 and the Danish is awkward,
but the English at that line is `its square amplitude` and the translation is following it.

Faulting a translation for the original's own wording is the one failure that has survived
every genre — it was the notation demands of run 6, the back-translation judgements of run 5,
and it is these two. No rule has ever reduced it, and at two phrases in 84 it is now rarer
than it has ever been.

### The phrase is stable again

`summary` and `summary-2` name the same defect on **seventeen of 21 rows**, against run 8's
eleven of 21 under the characterisation genre and run 3's eight of eleven under the location
genre. The four that move are level 3 — `gemini-3.7-flash/ca`, `ox-alpha/ru`,
`gpt-5.6-luna/ro` and `gemini-3.7-flash/ja` — and each pair is two readings of one
translation rather than two different translations.

Section 9 left this as the open question against the characterisation genre: a column that
names a different true-ish aspect on every re-run. Asking for *the single most notable
characteristic* is what settles it. The instruction now says which of the several things to
pick, where run 8's said only what kind of thing to name.

### What it costs

For 84 phrases on `gpt-5.6-terra`, with thinking on:

| | Tokens |
| --- | ---: |
| Input | 351,974 |
| of which cached | 87,977 (25%) |
| Output | 11,700 |
| of which reasoning | 10,601 (91%) |

About 4,190 input and 139 output tokens per phrase, and the reasoning is nine tenths of the
output — which is the point, since the reasoning is what the old pipeline had an evaluator
write. Looping the targets outside the variants is what earns the 25%: the cache holds the
original and the translation across a target's four calls.

One phrase per language over the whole corpus is 1,072 calls, so roughly **4.5M input and
150k output tokens** for a full pass, against the 84-call sample here. `trtools jev` sends
the same two texts, so this is one evaluation pass in input terms and a fraction of one in
output.

[trend14.py](trend14.py) records it, on `trtools.llm.init_usage_path()`'s condition and
through `LLMClient.usage`. Every call's `Usage` is summed and the sum appended
once at the end, so a section of [batch.sh](batch.sh) leaves one row rather than 84.

### This writer is the yardstick, not the choice

**`gpt-5.6-terra` will not be the writer in production.** The input is what makes it
impossible: every phrase sends the whole original and the whole translation, 4,190 tokens of
it, and one pass over the corpus is 1,072 of those. The output is negligible beside it —
11,700 tokens against 351,974 — so nothing about shortening the phrase changes the bill, and
the 25% the cache returns does not either.

What run 9 establishes is therefore a ceiling rather than a candidate: this is what the
wording produces when the writer is strong enough for it, and `stubova`, `bril·lança` and
`fiziky` are what a column of this kind can contain. The question the remaining runs have to
answer is how much of that a local writer keeps. Runs 1–8 say `ollama:qwen3.6` under the
earlier genres kept none of it, but it has never been given this one.

### Changed for run 10

Nothing is obviously wrong with this wording, which is a first. What is not yet separated:

1. **The genre, the model and the thinking all changed together.** `drop` on this writer is
   the control for the genre and it is clearly worse — four-word phrases, none of the seven
   findings above. But nothing here separates the model from the thinking. That matters for
   the choice of writer rather than for this one: if the findings come from the reasoning,
   a local model with thinking on may reach them, and if they come from the model's own
   knowledge of Croatian and Catalan, no wording will get them out of a smaller one.
2. **`--summary-free` versus `--summary`.** Six of the seven checked findings are
   `summary-free`'s, because naming the string is what makes a claim checkable at all. The
   ban it drops was written against a writer that misquoted; this one does not. The old
   column quotes in 2% of entries and `summary-free` quotes in a third of them, which is the
   argument for keeping the ban — and the findings are the argument against.
3. **The original's half of the input has never been tested under this genre.** Dropping it
   halves the 4,190 tokens, and section 2 rejected it on run 1's
   evidence — the writer made claims about an original it had not seen and got them wrong.
   That was the location genre, which no longer exists. `--no-original` is still a flag.
4. **One writer, one corpus sample.** 21 rows of 1,072, and `gpt-5.6-terra` is one
   commercial model of several.

## 11. Run 10 — the same wording with the reasoning summary off

Meant as run 9 minus the thinking, to separate the model from the reasoning. It is not that,
and finding out why is most of what the run settled.

### `--think` does not mean the same thing on every vendor

`llm7shi.compat.generate_with_schema`'s `include_thoughts`, which is what `LLMClient(think=)`
and so `trend14.py --think` set, branches by vendor:

| Vendor | `include_thoughts=False` |
| --- | --- |
| Ollama, Gemini | stops the thinking |
| OpenRouter | stops it, via `reasoning.enabled=False` |
| llama.cpp | stops it, via `enable_thinking=False` |
| **openai** | **only skips requesting a reasoning summary; the model still reasons** |

`gpt-5.6-terra` carries no vendor prefix and does not start with `gemini`, so it takes the
openai path. The knob that would have stopped the reasoning is `reasoning_effort`, which
defaults to `"medium"` there and which `trtools.llm.LLMClient` does not expose at all.

The token counts say it plainly:

| | Calls | Reasoning tokens | Per call |
| --- | ---: | ---: | ---: |
| Run 9, `--think` | 84 | 10,601 | 126 |
| Run 10, no `--think` | 63 | 5,070 | 80 |

Not zero. **So run 10 is run 9 with the reasoning summary withheld, not with the reasoning
off**, and nothing here separates the model from the thinking. Runs 1–8 are unaffected —
they are ollama, where the flag does what it says.

Its input was almost free: 262,167 of 262,356 tokens came back cached, 99.9%, because run 9
had already sent the same 21 prefixes.

### The specificity drops, and that is the direction the column wants

| | Quoted strings | Median words |
| --- | ---: | ---: |
| Run 9 `summary` | 1 / 21 (5%) | 5.0 |
| Run 9 `summary-2` | 0 / 21 (0%) | 5.0 |
| Run 9 `summary-free` | 7 / 21 (33%) | 6.0 |
| Run 10 `summary` | 0 / 21 (0%) | 6.0 |
| Run 10 `summary-free` | 6 / 21 (29%) | 6.0 |
| Run 10 `summary-free-2` | 4 / 21 (19%) | 6.0 |
| **Old column** | **23 / 1,072 (2%)** | **5.0** |

Run 10's `summary-free` gives up some of run 9's pinpointing — `gemini-3.7-flash/ca` goes
from `Nonstandard Catalan word choice: "bril·lança"` to `Minor awkward phrasing and
terminology issues` — and that is an improvement rather than a loss, because a column of
1,072 rows is read as a table and not as a defect list. Section 10 recorded run 9's seven
checked findings as its achievement, which is the wrong way round: that they were all true
says the writer is not fabricating, which matters, but naming them at all is more than the
column does.

**By the measurement, `summary` is the match and `summary-free` is not.** The ban on
pointing puts the quote rate at 0–5% against the old column's 2%; dropping it puts it at
19–33%, an order of magnitude out. The same rows show it side by side:

| Target | `summary-free` | `summary` |
|---|---|---|
| `ox-alpha/hr` | `Contains typo: isprepleeni instead of isprepleteni` | `Minor typographical error in Croatian text` |
| `union-alpha/sk` | `Minor typo: "fiziky" instead of "fyziky"` | `Minor Slovak spelling and diacritic errors` |
| `qwen3.8/es` | `Missing accent in Spanish "atenuan"` | `Missing accent mark in a Spanish verb` |

### Stability, and where it breaks

`summary-free` and `summary-free-2` name the same defect on **sixteen of 21 rows**, close to
run 9's seventeen. The five that move — `da`, `ru`, `hr`, `gemma4-31b/ru`, `ja` — are all
rows where one of the two reached for a specific string. **Dropping the ban costs stability
in exactly the places it buys specificity**, which is a second argument for keeping it.

### What checks out, and what does not

`isprepleeni` on `ox-alpha/hr` line 88 is a real typo for `isprepleteni`, and it is a
different real defect from run 9's `stubova` on line 17 — the two runs found two, and each
named one.

Two are false, both the class that has survived every genre: faulting the translation for
the original's own wording.

| Variant | Target | Claim | |
|---|---|---|---|
| `summary-free` | `ox-alpha/ru` | `Mistranslates classical waves as classical mechanics` | line 83 is `классических волн` and line 93 `классической механике`, and the English shifts at the same two lines |
| `summary-free-2` | `gpt-5.6-luna/da` | `Nonstandard Danish term for evanescent waves` | line 72 reads `de evanescente bølger`, the standard term |

`summary-free-2`'s `Minor mistranslation: "stubova" instead of "pillars"` is mis-framed
rather than false: `stubova` does mean pillars, and what is wrong with it is that it is
Serbian, which is what run 9 said.

`summary` has no false claim, which is what a phrase that names no instance cannot have.

### Changed for run 11

The commercial writer is a yardstick and is not adopted, so what is left before the port is
how much of this a local model reaches. Run 11 is `ollama:qwen3.6` — the pinned `WRITER` —
under this wording with `--think`, which on ollama genuinely turns thinking on. Both
`summary` and `summary-free`, each twice, because the comparison is against run 10's phrases
and one draw of either would not say whether a difference is the model or the draw.

## 12. Run 11 — the same wording, on the local writer

Runs 9 and 10 are a yardstick and not a candidate, so the question left before the port is
how much of them `ollama:qwen3.6` keeps. Same wording, same 21 targets, `--think` — which on
ollama genuinely turns the thinking on, unlike the openai path section 11 found. Both
`summary` and `summary-free`, each twice, because the comparison is with run 10's phrases
and one draw of either would not say whether a difference is the model or the draw.

The answer is not that the local writer is a weaker version of the commercial one. It finds
things run 10 never reached, and it is wrong more often and less consistently while doing
it.

### The form

| | Quoted strings | Median words | Repeat agreement | False |
| --- | ---: | ---: | ---: | ---: |
| Run 9 `summary` / `summary-2` | 1 / 21 (5%), 0 (0%) | 5.0 | 17 / 21 | 1 |
| Run 10 `summary-free` / `-2` | 6 / 21 (29%), 4 (19%) | 6.0 | 16 / 21 | 2 |
| Run 11 `summary` / `summary-2` | 0 (0%), 1 / 21 (5%) | 6.0 | **14 / 21** | 3 |
| Run 11 `summary-free` / `-2` | 2 / 21 (10%), 2 (10%) | 6.0 | **13 / 21** | 4 |
| Old column | 23 / 1,072 (2%) | 5.0 | — | — |

The length holds at the old column's. What does not hold is the stability, and the rows
that move are the same band they have always been: all eight are level 3 — `da`,
`qwen3.8/es`, `ca`, `ro`, `hr`, `gemma4-31b/ru`, `ja`, `uk`, with `th` in place of `hr` on
the `summary` pair. Two of the eight are borderline and counted as agreeing: `ne`, where
`Severe machine translation errors and broken syntax` and `Severe endless repetition loops`
are two names for line 74, and `ja`, where one variant praises the filler handling and the
other faults it.

**The gap between the two wordings nearly closes here, for the wrong reason.** `summary-free`
quotes in 10% against run 10's 29%, not because the ban became unnecessary but because this
writer reaches for fewer strings. Of the two it does reach for, `'coincidence' as 'et
tilfælde'` is false and `'be careful'` is mis-framed — both are below.

### What it finds that run 10 did not

Five, each checked against the files.

| Target | Variants | Phrase | Checked |
|---|---|---|---|
| `gemini-3.7-flash/el` | `summary`, `-2`, `-free-2` | amplitude and width collapsed into one word | line 50 is `το πλάτος και το πλάτος` for `amplitude and width`; line 45 is `το πλάτος και το χωρικό πλάτος` |
| `qwen3.6/he` | all four | corrupted filler, Latin mixed into Hebrew | line 67 is `מmm מm.` for `Hmm hmm.`, the only non-technical line in the file carrying Latin script |
| `ox-alpha/hr` | `summary`, `summary-2` | wrong Croatian physics term for conservation | line 29 is `čuvanje`; the physics term is `očuvanje` |
| `qwen3.8/th` | `summary`, `-2`, `-free-2` | speaker labels missing | 24 of 99 lines carry no label. Run 10 called the same file truncated instead |
| `gpt-5.6-luna/uk` | `summary-2` | evanescent waves named imprecisely | line 72 is `затухаючими хвилями`; the term is `еванесцентні` |

**These are not the genre run 9's seven findings were.** `stubova`, `bril·lança` and
`fiziky` are one string each, found by a writer that knows the language well enough to spot
one wrong letter. `πλάτος`/`πλάτος` and the missing labels are properties of the whole
document, which is what the column is for. Run 11 lost every one of run 9's and run 10's
strings — `atenuan`, `bril·lança`, `brilanța`, `fiziky` by name, `εξατμιζόμενα κύματα`,
`isprepleeni`, `stubova` — and found this instead.

The register claims carry over unchanged and all three check out under section 17's
both-forms procedure: `ox-alpha/ru` line 35 `твоей` against lines 12 and 51 `Вы`,
`gpt-5.6-luna/uk` line 12 `Ти` against line 51 `Ви`, `gemma4-31b/ru` line 35 `твоей` against
lines 12, 15 and 68. `gpt-oss/sv`'s missing labels are real — eight of 99 — and no variant
states a number.

**Permission to report soundness is taken at last.** Runs 4 through 6 recorded it unused in
22 of 22; here `gemini-3.7-flash/ca` and `gemini-3.7-flash/ja` answer two level-3 rows with
praise alone, and `ox-alpha/hr` and `gemini-3.7-flash/ja` with praise carrying a caveat.
Two praise-only phrases in 56 level-3 phrases is under the old column's rate rather than
over it — section 16 puts that at about 10% — so nothing here needs holding back.

### What is false

Seven of 84, where runs 9 and 10 had two each. Four of the seven are one row.

| Target | Variant | Claim | |
|---|---|---|---|
| `gpt-5.6-luna/da` | `summary` | `Mistranslates coincidence to case` | line 42 is `Det er ikke et tilfælde`, the ordinary Danish for it |
| `gpt-5.6-luna/da` | `summary-free` | `Mistranslation of 'coincidence' as 'et tilfælde'` | the same |
| `gpt-5.6-luna/da` | `summary-2` | `Untranslated English word retained in the Danish text` | every word of four letters or more that the file shares with `onde-en.txt` is Danish: `have`, `stop`, `gives`, `Okay`. There is no referent |
| `gpt-5.6-luna/da` | `summary-free-2` | `Incorrect adjective form for squared amplitude` | line 83 is `dens kvadratiske amplitude`; the definite `-e` after a possessive is correct, and the English at that line is `its square amplitude` |
| `qwen3.8/es` | `summary-free` | `Unidiomatic use of implacable` | line 29 of the original is `a mathematical reason, uh... implacable` |
| `union-alpha/sk` | `summary` | `Czech lexical interference replacing Slovak terms` | no `ř`, `ě` or `ů` in the file and no Czech lexeme; `fiziky` is `fyziky` in Czech too. The defect is a typo |
| `gemma4-31b/ru` | `summary-free` | `Contextual mistranslation of 'be careful'` | line 68 is `будьте осторожны`, which is correct. What is odd at that line is the register, which three of the four variants name correctly |

Two more are unresolved rather than false: `gemini-3.7-flash/ja`'s `Mistranslation of
contextual filler 'No'` — line 43 is `ええ、違います` for `No.` agreeing with a negative, which
is defensible Japanese — and `gemini-3.7-flash/ca`'s `Literal mistranslation of
conversational idioms`, whose referent cannot be located at all.

**`gpt-5.6-luna/da` fabricates again, in all four variants.** Section 8 recorded it as the
row that stopped fabricating after seven runs; that was the commercial writer, and it does
not survive the change of writer.

**The class widened.** Runs 9 and 10 had one surviving class — faulting the translation for
the original's own wording — and two of these seven are still it (`implacable`,
`kvadratiske`). The other five are new: faulting a correct idiom by its literal gloss
(`tilfælde`, twice), a claim with no referent at all (the English word), and re-framing a
real anomaly as a different defect (`Czech interference`, `be careful`). The last is run
10's `stubova` / `pillars` again, which section 11 called mis-framed rather than false; here
the frame lands further from the truth.

### What it costs

No tokens are billed and the constraint moves to the clock. 84 phrases took
**163m58.240s**, which is 117 seconds each and puts a 1,072-phrase pass at roughly **35
hours**. The thinking is most of it: the run's console output came to 1.9 MB over 84 calls,
about 23 KB of reasoning a phrase, measured while [batch.sh](batch.sh) still teed it to a
file.

[trend14.py](trend14.py) records no usage here, by design: the condition in
`trtools.llm.init_usage_path()` is an `openai:`/`gpt-` model or `--save-usage`.

### What it settles, and what run 12 asks

`summary` is adopted. The ban on pointing holds the quote rate at 0–5% against the old
column's 2% across both writers, and run 11 removes the argument that ran against it: the
specificity `summary-free` bought on the commercial writer is not there on this one, and
both of its quotes carry a false or mis-framed claim rather than a finding.

What is not separated is the reasoning from the model. Run 10 was meant to be that
comparison and was not, because `--think` does not stop an openai model reasoning. On ollama
it does, so run 12 is this run minus `--think` and identical in everything else, the four
variants included — the wall-clock figure above is one of the things being compared, and it
is only comparable across runs of the same size. If the false phrases and the 13-of-21 come
from the reasoning, they drop; if they come from the model, the next step is another local
writer rather than another wording.

## 13. Run 12 — run 11 without the thinking

Run 11 exactly, minus `--think`: same wording, same writer, same 21 targets, the same four
variants. On ollama the flag really does turn the thinking off, so this is the comparison
run 10 was meant to be and was not.

**First, a correction to the probe.** A two-variant attempt at this section, run and
discarded before this one, came back with five invented speaker swaps, a cited line number,
a phrase written in Danish and twelve false claims in 42. **None of that reproduced.** Over
all 84 phrases here there is no speaker claim, no line number and no phrase outside English,
and the false count is 7 in 84 — run 11's exactly. Those were one bad draw of 42, which is
what insisting on the full four variants was for. The probe's phrases are not kept and its
numbers are recorded here only as the thing that did not reproduce.

### The form

| | Quoted strings | Median words | Three words or fewer | Repeat agreement | False |
| --- | ---: | ---: | ---: | ---: | ---: |
| Run 11 `summary` / `-2` | 0 (0%), 1 (5%) | 6.0 | 2, 0 | 14 / 21 | 3 |
| Run 11 `summary-free` / `-2` | 2 (10%), 2 (10%) | 6.0 | 0, 1 | 13 / 21 | 4 |
| Run 12 `summary` / `-2` | **4 (19%), 6 (29%)** | 6.0 | 1, 2 | **11 / 21** | 6 |
| Run 12 `summary-free` / `-2` | 0 (0%), 3 (14%) | 5.0, 4.0 | 2, **5** | **18 / 21** | 1 |
| Old column | 23 / 1,072 (2%) | 5.0 | — | — | — |

**The ordering of the two wordings inverts.** `summary` is the variant that forbids naming
an instance, and without the reasoning it quotes in 19% and 29% while `summary-free`, which
permits it, quotes in 0% and 14%. This is the probe's one finding that did reproduce, and
it is the important one: a rule the writer no longer has the budget to apply is not a rule.
With thinking on the ban works exactly as written — 0–5% against `summary-free`'s 10%.

**`summary-free` becomes stable by becoming empty.** 18 of 21 is the best agreement any run
has posted, above run 9's 17 on the commercial writer. It is bought with a median of five
words falling to four and five phrases of three words or fewer: `Minimal typos and errors`,
`Minor register inconsistency`, `Minor stylistic inconsistencies`, `Minor translation errors
present`. Two variants agree because neither says anything a third could disagree with. This
is run 8's failure — the phrases go short when the instruction stops holding them up —
arriving by a different road.

It also costs the two rows where a defect is documented and the phrase denies it:
`qwen3.6/es` `summary-free` is `No notable defects detected` against the `tenga`/`Siga`
register shift run 9 checked, and `qwen3.8/es` `summary-free-2` is `No obvious translation
defects detected` against `atenuan` for `atenúan`.

### What it finds

Five that no earlier run reached, each checked:

| Target | Variant | Phrase | Checked |
|---|---|---|---|
| `gpt-5.6-luna/da` | `summary-free-2` | `Inconsistent formatting of quotes (»« vs „“)` | lines 1, 15, 40, 45, 72 and 99 use `» «`; line 93 alone uses `„ “` |
| `qwen3.6/he` | `summary-free-2` | `Typo "האם" instead of "כן"` | line 23 is `קמיל: האם.` for `Camille: Hmm.` — the interrogative particle standing alone |
| `gpt-5.6-luna/uk` | `summary-2` | `Inconsistent use of "Імовірність" and "ймовірність"` | line 83 against lines 12, 13, 27, 31, 40, 93, 94 and 96 |
| `qwen3.6-27b/el` | `summary`, `-2`, `-free`, `-free-2` | the intrusion is Spanish | `bueno` on line 1. The probe called the same word Italian |
| `union-alpha/sk` | `summary` | `Minor terminology inconsistencies (fizika vs fyzika)` | line 43's `fiziky`, framed as the typo it is where run 11 called it Czech interference |

The Danish quote-style inconsistency is the kind of thing this genre is for — a property of
the whole document, one instance, invisible to a rubric level — and runs 9, 10 and 11 all
missed it.

`gemini-3.7-flash/el`'s `πλάτος` collapse, `gpt-oss/sv`'s missing labels, `qwen3.8/th`'s
truncation and the `ты`/`вы` shifts in `ox-alpha/ru` and `qwen3.6/es` all carry over and all
hold.

### What is false

Seven of 84, the same as run 11, but distributed differently: five of the seven are in
`summary-2` alone.

| Target | Variant | Claim | |
|---|---|---|---|
| `gpt-5.6-luna/da` | `summary-2` | `Minor typo: "psi i anden" instead of "psi²"` | `psi i anden` is the Danish for it, used at lines 17, 24 and 33 |
| `qwen3.8/es` | `summary-2` | `Literal translation errors ("es decir")` | `es decir` is the Spanish for `that is`, lines 48 and 58 |
| `gemini-3.7-flash/ca` | `summary` | `Minor grammatical issues with 'E squared' and 'nsom'` | line 37 reads `E al quadrat` and line 77 `el NSOM`; neither quoted string is in the file |
| `gemini-3.7-flash/ca` | `summary-free-2` | `Minor typo: "A menys" instead of "si"` | line 74's `A menys que siguis enginyós` is correct Catalan for `Unless one is clever` |
| `gpt-5.6-luna/ro` | `summary-2` | `Intrusive French term NSOM` | an English acronym, at line 77 of the original as well |
| `gemma4-31b/ru` | `summary-2` | `Inconsistent speaker name translation (Luc/Lyuk)` | the file's only two labels are `Камиль` and `Люк` |
| `gemini-3.7-flash/ja` | `summary-2` | `Inconsistent use of Katakana for "Eva" (evanescent)` | `エバネッセント波` occurs once, at line 72. There is nothing for it to be inconsistent with |

Four of the seven are the class that has survived every genre — faulting the translation for
the original's own wording or for a correct idiom — and three are a new shape: an
inconsistency asserted about a string that occurs once, or not at all.

`gemma4-31b/ru` `summary`'s `Inconsistent honorifics and pronouns (tu/vous)` is mis-framed
rather than false: the `ты`/`вы` shift is real and the phrase names it with French pronouns,
against the prompt rule that says never to confuse the language written in with the language
described.

### What it costs

**2m55.994s for 84 phrases**, against run 11's **163m58.240s** for the same 84 — 2.1 seconds
a phrase against 117, a factor of 56. A 1,072-phrase pass falls from about 35 hours to about
37 minutes. The console output that came to 1.9 MB for run 11 is 7.5 KB here, which is the
same 56× seen from the other side.

### What it settles

**The reasoning is not what keeps the writer honest — it is what makes it follow the
wording.** The false rate is the same with it and without, 7 in 84 either way, so the
argument for thinking is not accuracy. What changes is obedience: with the reasoning the ban
on pointing holds at 0–5% and the adopted variant is the stable one; without it the ban is
ignored at 19–29% and `summary` is the variant that comes apart, 11 of 21.

That is decisive for `--summary`, which is the adopted wording. It is not decisive for the
column, because run 12 also produced the most old-column-like output the experiment has
seen, in the variant nobody was measuring: `summary-free` without thinking is 18 of 21
stable, one false phrase in 42, a quote rate of 0–14% and a median of five words — and 37
minutes a pass instead of 35 hours. Its cost is that a third of its phrases say nothing
checkable and two of them deny a defect that is there. Whether that trade is the right one
for a 1,072-row table is a decision about the column and not a measurement this experiment
can make.

## 14. Run 13 — the old pipeline itself, in two stages

Runs 9–12 asked one call to be both the evaluator and the summariser: the writer's reasoning
stood in for the `overall_comment` and the phrase summarised it. Run 12 found that the
reasoning bought obedience rather than accuracy, at 56 times the wall clock. Run 13 goes back
to what produced the column being replaced and splits it into two calls, each with its own old
prompt, both without thinking:

1. **Stage 1** is `trtools/evaluate.py`'s prompt, point bands and all, with its closing
   sentence replaced. Instead of asking for five scores it hands over **Jev's** five, each a
   level times `POINTS_PER_LEVEL` — which is evaluate.py's own 0–20 scale, since Jev's
   criteria are evaluate.py's verbatim — and asks for the overall comment that accounts for
   them, in English, as plain text. Without the scores the comment would be a second,
   independent verdict and the column would not describe the score beside it, which is the
   whole reason for replacing the old column. The comment is in English because a comment
   written in the target language makes the evaluation of a Hindi translation depend on how
   well the writer writes Hindi.
2. **Stage 2** is `trtools/trend.py`'s prompt, made singular, with the Jev total in the block
   header where each run's total used to be. The sentence about issues mentioned in several
   runs is gone, there being one. It sees the comment and nothing else — the calls share no
   history, as in the old pipeline, where the summariser never saw the translation.

One wording drawn four times (`two-stage` to `two-stage-4`), so the run is run 12's size.
The comment is stored beside the phrase, so every claim can be traced to the stage that made
it.

### The form

| | Quoted strings | Median words | Three words or fewer | False |
| --- | ---: | ---: | ---: | ---: |
| Run 13, four draws | 0 in 84 | 6.0 | 0 | 2, and one of the surviving class |
| Old column | 23 / 1,072 (2%) | 5.0 | — | — |

All 84 comments are in English; the non-Latin text in them is quotation from the translation.
Their median is about 270 words.

### What it finds, and what is false

The lower rows name real defects, each checked: `πλάτος και πλάτος` and `εξατμιζόμενα
κύματα` in `gemini-3.7-flash/el`; the stray `细` on line 66 of `bonsai2-27b/ne`, which no
earlier run named; the English in `gemma4-31b/ia` (`queTook`, `whether`, `pattern`);
`qwen3.8/th`'s truncation and its 24 unlabelled lines; `gpt-oss/sv`'s eight.

| Target | Draw | Claim | |
|---|---|---|---|
| `qwen3.6-27b/el` | 1 | `Severe linguistic contamination by Spanish and French` | `bueno` on line 1 is Spanish; the "French" is `Γουάου` and `Πέψα`, Wow and Wait garbled in Greek script |
| `qwen3.6/he` | 3 | `...inconsistent speaker attribution` | the labels mapped in order of appearance match the original on all 99 lines |
| `qwen3.8/th` | 4 | `Critical truncation and untranslated jargon` | the truncation is real; the "jargon" is `delta x`, `NSOM` and `psi`, the original's own notation — the class that has survived every genre |

### The problem: the top of the scale reads as praise

On the eleven level-3 rows at 89 and over, 28 to 29 of 44 phrases are praise alone —
`Professional-grade quantum physics translation`, `Exceptionally high accuracy and
naturalness` — against the old column's 29% at 90 and over (section 16). Among them are
rows with documented defects: `ox-alpha/ru`'s `ты`/`вы`, `qwen3.8/es`'s `atenuan`,
`gpt-5.6-luna/da`'s quotation marks.

The cause is stage 1's point bands. Jev's 17–19 of 20 falls in evaluate.py's "high quality
(18-20)" and the comment reads the score on the old scale, where Jev's level 3 means one to
three lines falling short. **But every one of those 29 comments names a shortfall**, because
stage 1 is told to account for scores below full marks: the material is there and stage 2
drops it. Most of what they name is inferred rather than found — `likely stem from very
subtle stylistic preferences` — and a few are concrete.

### What it costs

**16m44.182s for 84 phrases**, 12.0 seconds each, which puts a 1,072-phrase pass at about
3.5 hours: a tenth of run 11's and six times run 12's. Run 14 puts stage 2 at 1.35 seconds, so
nearly all of it is stage 1 reading the translation and writing the comment.

## 15. Run 14 — stage 2 biased toward the shortfall

Stage 1 is not re-run: run 13's 84 comments are read back with `--comments` and stage 2 alone
is run over them, so a difference between the variants is the wording's alone. Three variants
per comment, 252 phrases, each written to a file carrying its source's suffix:

- `base` — run 13's stage 2 unchanged, drawn again, as the control.
- `short` (`--shortfall-rule`) — `If the evaluation names any shortcoming, however minor,
  state the most prominent one rather than praising the translation. Praise it only if the
  evaluation names no shortcoming at all.`
- `level` (`--shortfall-rule --jev-level`) — the same, plus `jev_criteria.LEVELS` verbatim for
  the weakest criterion's level, so that stage 2 reads the score on Jev's scale rather than
  on the point bands stage 1 used.

### The form

| | Praise alone, level 3 at 89+ | Quoted strings | Median words | Three words or fewer |
| --- | ---: | ---: | ---: | ---: |
| `base` | 32 / 44 (73%) | 0 | 5.0 | 8 |
| `short` | 6 / 44 (14%) | 0 | 5.0 | 12 |
| `level` | **3 / 44 (7%)** | 0 | 5.0 | 15 |
| Old column, 90+ / 80–90 | 29% / 12% | 2% | 5.0 | — |

`level`'s three are the counting pattern missing `Subtle nuance differences` and the like;
read by hand, no level-3 phrase in it is praise alone. The only praise is on the one level-4
row, `gpt-5.6-luna/it`, in one draw of four: `No shortcomings identified by evaluation`.
`short`'s six are all level-3 rows — `Flawless professional-grade translation`, `Accurate and
professional with no defects` — which Jev judged to fall short somewhere. `base` against run
13's 64% is stage 2's own variation.

The high rows now read as the old column did: `Slight stiffness in conversational fillers`,
`Minor literal phrasing choices`, `Occasional slightly stiff phrasing`. Mostly not checkable,
which is the old column's nature too.

### What the bias brings out

Real defects `base` had dropped: `gpt-5.6-luna/da` draw 4, `Slight inconsistencies in
typography and formatting` — six lines use `» «` and one `„ “`, run 12's finding; and
`ox-alpha/ru` draw 4, `Minor pronoun inconsistencies`.

And stage 1's errors, at the same rate:

| Target | Draw | Variants | Claim | |
|---|---|---|---|---|
| `qwen3.6/he` | 3 | `short`, `level` | speaker labels swapped | false; comment 3 says so, the labels match on all 99 lines, and `base-3` had dropped it |
| `gemma4-31b/ru` | 4 | `short`, `level` | `Gender nuance issues` | mis-framed: the `ты`/`вы` shift is real (line 12 `Вы`, line 51 `Ты`) and comment 4 calls it gender |
| `qwen3.8/th` | 4 | `short`, `level` | `untranslated segments`, `mixed English` | the original's notation, from comment 4 |
| `gemini-3.7-flash/ca` | 3 | `level` | `Fillers and interjections are direct calques` | doubtful: `Hmm` and `Ah` are the original's |

**The bias invents nothing.** Every claim in `short` and `level` is already in the comment it
summarises; what the rule changes is how often a shortfall named there reaches the phrase.
So stage 2 is not where accuracy is decided: a phrase is as right as the comment behind it.

### What it costs

**5m39.910s for 252 phrases**, 1.35 seconds each — about 24 minutes over the corpus. The
rules add nothing measurable to it, and a full pass stays at stage 1's 3.5 hours.

### What it settles

**`level` is adopted.** It is the variant that reads the score in Jev's terms at both ends:
stage 1 is handed Jev's numbers, and stage 2 is told what Jev's level means, so praise is left
to the rows Jev found nothing wrong with. Its cost against `short` is three more phrases of
three words or fewer, most of them still a finding — `Missing speaker tags`. Praise alone
falls from the old column's tenth to the twelve level-4 records, which is what the scale says.

## 16. Evidence Behind the Fixed Decisions

The decisions themselves are [README.md](README.md) section 4; what they rest on is here.

**The score column is one decimal place.** Jev compresses the corpus's top models into
roughly 20 points, so rounding to integers ties 40–48 of 67 languages per model against
8–11 at one decimal, and `render_table`'s score-descending sort degenerates into
alphabetical order.

| Model | Median | Range | Ties at 1 dp | Ties as integers |
| --- | ---: | --- | ---: | ---: |
| gpt-5.6-luna | 88.1 | 71.2–93.0 | 11 | 48 |
| union-alpha | 87.6 | 71.7–94.6 | 8 | 48 |
| gemini-3.7-flash | 82.7 | 64.8–94.5 | 11 | 40 |
| ox-alpha | 86.4 | 64.0–95.9 | 10 | 45 |

**The existing `analysis` text is not carried over.** Its severity wording is calibrated to
the old evaluator. Against the Jev scale, 560 of 1,072 records change tier under
`generate_compare_rows.py`'s 90/80/60 cuts, and the extremes read as errors:

| Model | Lang | Old | Jev | Existing `analysis` |
| --- | --- | ---: | ---: | --- |
| gpt-5.6-terra | hr | 9 | 66.7 | Mixed-language artifacts and editorial notes |
| gpt-5.6-terra | nl | 24 | 72.5 | Critical structural artifacts disrupt narrative flow |
| gemma4 | my | 34 | 79.2 | Pervasive orthographic corruption |
| gpt-oss | it | 95 | 65.6 | Inconsistent speaker attribution formatting |

**Praise is allowed.** Classifying all 632 level-3 records' existing `analysis` by whether
it names a defect:

| Jev | Records | Names a defect | Praise only |
| --- | ---: | ---: | ---: |
| under 70 | 10 | 90% | 0% |
| 70–80 | 265 | 86% | 3% |
| 80–90 | 271 | 74% | 12% |
| 90+ | 86 | 57% | **29%** |

Praise-only is 66 records of 632, about 10%, concentrated where a defect is least likely to
exist. The old column was already naming defects wherever they were findable, which is what
makes the ban in section 4 a bad trade.

---

## 17. How a Claim Is Checked

Every "false" in this file was established the same way, and a later session should not
take one on trust without redoing it. The phrases are a generative model's, and about a
fifth of them are wrong in a way that reads exactly like the four fifths that are right.
A "false" recorded here can be wrong in the other direction too: three of them were, and
section 7 carries the correction.

- **A quoted string**: `grep -n` for it in
  `examples/tr/onde/{model}/tr/onde-{lang}.txt`, and in `examples/onde-en.txt` when the
  phrase quotes the source. A string in neither is either a fabrication or a proposed
  correction, which until `--quote-rule` lands cannot be told apart by matching alone.
- **A speaker claim**: the labels are transliterated in most languages, so a plain `diff`
  of them reports all 99 lines as changed and says nothing. Map each file's labels to the
  order they first appear in and compare those: all eleven of `SLIGHT_TARGETS` match the
  original on all 99 lines, which is what makes every swap claimed about them false.
- **A register or address claim** (`ты`/`вы`, `ти`/`ви`, `tu`/`vous`): search for **both**
  forms, with word boundaries, and print the speaker of each hit. Searching only the form
  the phrase names finds only what confirms it — that is how section 7 came to call
  `ox-alpha/ru` consistent when it is not — and a Cyrillic `\b` in `grep -E` matches inside
  words, so `ты` hits `тысяч`. Imperatives and verb endings carry the register too
  (`Подожди`, `Продовжуй`, `Давай`), so a pronoun search alone under-reports it.
- **A line number**: the prompt carries none, so any citation is the writer counting.
  Three were checked in run 1 and all three were wrong; none have appeared since run 2.
- **A translation judgement** (`psi i anden`, `пси в квадрате`, `bølgelove`): read the line
  against the original. These are where the writer is most often wrong and most confident.

The corpus's own numbers come from `examples/tr/onde/{model}/jev.jsonl`, one JSONL record
per language: `scores` holds five criteria as levels 0.0–4.0, and the corpus total is their
sum times `POINTS_PER_LEVEL`, 5. The level a phrase is written under is the rounded weakest
criterion, and the unrounded value is what section 6 splits on.

## 18. When the Wording Settles

It has, and this file is closed. The trend column's port into `trtools trend --jev` is
[PORT.md](PORT.md); the rest of the migration — `trtools agg --jev`, the comparison on the
Jev scale and the switch — is [experiment 13's PORT.md](../13/PORT.md).
