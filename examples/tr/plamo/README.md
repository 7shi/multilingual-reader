# examples/tr/plamo/

Translates and evaluates the onde text under PLaMo 3 Translate's conditions ([PLAMO.md](../PLAMO.md)): the languages the model supports (`PLAMO_LANGS` in [../common.mk](../common.mk)) and the whole text in one request per language, with the target language's whole column of [../terms/onde-en.tsv](../terms/onde-en.tsv) as the glossary. The shared settings are in [common.mk](common.mk), and each model's `Makefile` names only its `TRANSLATOR`.

PLaMo's languages differ from the corpus's, and the one-request method differs from the line-by-line translation of [onde/](../onde/), so these results are kept apart from the comparison there and compared only with each other, on these languages.

- [plamo-3-translate-0.8b](plamo-3-translate-0.8b/) (PLaMo 3 Translate 0.8B Q4_K_M, llama.cpp)
- [plamo-3-translate-2b](plamo-3-translate-2b/) (PLaMo 3 Translate 2B Q4_K_M, llama.cpp)
- [plamo-3-translate-8b](plamo-3-translate-8b/) (PLaMo 3 Translate 8B Q4_K_M, llama.cpp)
- [plamo-3-translate-31b](plamo-3-translate-31b/) (PLaMo 3 Translate 31B Q4_K_M, llama.cpp)

Every model is evaluated by TypeSafe's Jev (`jev-1.14.0`), one run per language, as in onde/.

## Sizes of PLaMo 3 Translate

Over the 52 supported languages (Jev's total; the high quality, practical and critical columns count the languages at 90+, 80–89 and below 60):

| Model | Mean | Median | Std Dev | 90+ | 80–89 | <60 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| plamo-3-translate-31b | 78.92 | 78.50 | 8.16 | 5 | 19 | 0 |
| plamo-3-translate-8b | 75.94 | 77.00 | 10.01 | 2 | 16 | 3 |
| plamo-3-translate-2b | 73.36 | 73.75 | 9.60 | 2 | 12 | 6 |
| plamo-3-translate-0.8b | 61.06 | 62.40 | 10.96 | 0 | 0 | 23 |

Each size is above the next smaller one (Wilcoxon signed-rank, paired by language): 2B over 0.8B in 46 of 52 languages (p < 0.001), 8B over 2B in 31 (p = 0.022), and 31B over 8B in 32 (p = 0.024). The largest step is from 0.8B to 2B; above that the gain is a few points per size, and not every language follows it (the 31B is below the 2B in Swahili, Slovene and Lithuanian). The 31B reaches high quality in French, Spanish, both Chinese scripts and Japanese, and its floor is Telugu, Burmese and Basque.

## Skipped, Repeated, and Runaway Passages

The model is given the whole text in one request rather than line by line, so nothing holds its output to the source's lines, and in some languages it loses its place. These are kept as they are, as part of its performance under its intended use; each model's README lists them.

- **Skipped stretches**: most often it skips part of the dialogue and goes on to a natural ending, so the line count falls short with no visible break. The 0.8B does so in Burmese, and the 2B and 8B skip 17 to 43 lines in nine languages between them, Telugu at 2B the most.
- **Loops**: otherwise it falls into a loop until the output stops. The 0.8B repeats one phrase in Telugu and Sinhala and three lines of the closing passage in Gujarati; the 2B repeats one word in Khmer at the summary; the 8B's Japanese goes back from line 53 to line 40 and runs through the same stretch again before jumping ahead.
- **By size**: larger sizes lose their place less often, though not steadily: the 2B does in eight languages and the 8B in five, while the 31B only joins two lines into one in Kazakh and Burmese.
