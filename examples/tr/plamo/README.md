# examples/tr/plamo/

Translates and evaluates the onde text under PLaMo 3 Translate's conditions ([PLAN.md](PLAN.md)): the languages the model supports (`PLAMO_LANGS` in [../common.mk](../common.mk)) and the whole text in one request per language, with the target language's whole column of [../terms/onde-en.tsv](../terms/onde-en.tsv) as the glossary. The shared settings are in [common.mk](common.mk), and each model's `Makefile` names only its `TRANSLATOR`, with a general model's `OPTIONS` as in onde/. See [ADD_PLAMO.md](../ADD_PLAMO.md) for adding a model.

PLaMo's languages differ from the corpus's, and the one-request method differs from the line-by-line translation of [onde/](../onde/), so these results are kept apart from the comparison there and compared only with each other, on these languages.

- [plamo-3-translate-0.8b](plamo-3-translate-0.8b/) (PLaMo 3 Translate 0.8B Q4_K_M, llama.cpp)
- [plamo-3-translate-2b](plamo-3-translate-2b/) (PLaMo 3 Translate 2B Q4_K_M, llama.cpp)
- [plamo-3-translate-8b](plamo-3-translate-8b/) (PLaMo 3 Translate 8B Q4_K_M, llama.cpp)
- [plamo-3-translate-31b](plamo-3-translate-31b/) (PLaMo 3 Translate 31B Q4_K_M, llama.cpp)
- [gpt-6-luna](gpt-6-luna/) (a general model, `trtools whole`; its line-by-line counterpart is [onde/gpt-6-luna](../onde/gpt-6-luna/))
- [gemma4-e2b](gemma4-e2b/) (Gemma 4 E2B, Ollama, `trtools whole`; its line-by-line counterpart is [onde/gemma4-e2b](../onde/gemma4-e2b/))

Every model is evaluated by TypeSafe's Jev (`jev-1.14.0`), one run per language, as in onde/.

## Sizes of PLaMo 3 Translate

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical flaws (below 60)

Mean and standard deviation are computed from each model's `SCORES-jev.txt` by `uv run generate_compare_rows.py plamo --jev --sync` in examples/tr/ (Notes are entered manually).

| Model | Mean | Median | Stdev | Notes |
| --- | ---: | ---: | ---: | --- |
| gpt-6-luna | 87.48 | 88.30 | 4.16 | A general model given the same request (`trtools whole`), for reference. Above the 31B in 51 of 52 languages, all but Korean, and keeps all 99 lines in every language; only Telugu, Cebuano, Tagalog, and Gujarati fall below 80 |
| plamo-3-translate-31b | 78.92 | 78.50 | 8.08 | High quality on French, Spanish, both Chinese scripts, and Japanese, and no language below 60; Telugu, Burmese, and Basque are its floor. Keeps its place in all but two languages, each two lines short |
| plamo-3-translate-8b | 75.94 | 77.00 | 9.92 | French and Spanish reach high quality, but Japanese falls to 60.0 when the request loops back over a stretch of the dialogue, and Burmese, Sinhala, and Malayalam each skip 20 to 33 lines |
| plamo-3-translate-2b | 73.36 | 73.75 | 9.51 | Above the 0.8B in 46 of 52 languages; Italian and Dutch reach high quality. Loses its place most often of the four sizes: six languages skip 17 to 43 lines, Khmer stops in a loop, and Vietnamese adds a line |
| gemma4-e2b | 68.12 | 70.40 | 15.36 | A general model given the same request, for reference against PLaMo's small sizes. Above the 0.8B in 38 of 52 languages and not distinguishable from the 2B; French and Spanish reach high quality, but 13 languages fall below 60, Basque, Estonian, Latvian, Belarusian, and Lithuanian under 40. Loses its place only in Uzbek and Thai, by one or two lines |
| plamo-3-translate-0.8b | 61.06 | 62.40 | 10.86 | No language reaches the practical range (Italian, Vietnamese, Spanish, and Hungarian are its best, 76.5–78.5), and 23 fall below 60, with Burmese skipping a stretch and Telugu, Sinhala, and Gujarati ending in loops |

Each size is above the next smaller one (Wilcoxon signed-rank, paired by language): 2B over 0.8B in 46 of 52 languages (p < 0.001), 8B over 2B in 31 (p = 0.022), and 31B over 8B in 32 (p = 0.024). The largest step is from 0.8B to 2B; above that the gain is a few points per size, and not every language follows it (the 31B is below the 2B in Swahili, Slovene, and Lithuanian).

gpt-6-luna, a general model given what PLaMo's template carries and nothing more, is above the 31B in 51 of 52 languages (p < 0.001), by 8.6 points on average, and keeps the source's 99 lines in every language without being asked to. Losing one's place is therefore not a cost of the whole-text request itself. On the 45 corpus languages it is also above its own line-by-line translation in [onde/gpt-6-luna](../onde/gpt-6-luna/) (mean 88.0 against 86.0; above in 33, one tie, p = 0.002). The largest gains are in Latvian, Hungarian, Basque, and Thai, where the line-by-line run lost points to typos, a missing speaker label, and grammatical fragments; the largest loss is Persian (7.0 points lower).

gemma4-e2b, the smallest Gemma 4, given the same request, is above the 0.8B in 38 of 52 languages (p = 0.002, 7.0 points on average), not distinguishable from the 2B (above in 22, p = 0.10), and below the 8B (above in 18, p = 0.002). It keeps its place better than PLaMo's small sizes: only Uzbek, which folds one line into another and drops a short reply, and Thai, which leaves out the closing line, fall short, by two lines and one. Against its own line-by-line translation in [onde/gemma4-e2b](../onde/gemma4-e2b/), it is above in 39 of the 45 corpus languages (p < 0.001, mean 67.9 against 59.4).

| Language | 0.8B | 2B | 8B | 31B | gpt-6-luna | gemma4-e2b |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| French | 73.2 | 83.7 | 91.9 | 93.6 | 94.2 | 93.4 |
| Spanish | 77.0 | 78.1 | 90.9 | 92.0 | 94.7 | 91.6 |
| Chinese (Traditional) | 70.5 | 87.3 | 89.0 | 90.8 | 91.7 | 83.0 |
| Chinese | 67.5 | 87.0 | 89.4 | 90.7 | 90.8 | 77.7 |
| Japanese | 70.1 | 76.5 | 60.0 | 90.3 | 91.3 | 77.2 |
| Korean | 67.4 | 85.5 | 79.1 | 88.8 | 88.4 | 86.0 |
| Vietnamese | 77.2 | 73.6 | 87.8 | 88.1 | 90.2 | 84.5 |
| Arabic | 69.0 | 85.9 | 84.2 | 88.0 | 91.5 | 78.5 |
| Catalan | 66.6 | 80.2 | 87.1 | 88.0 | 93.8 | 59.8 |
| Dutch | 71.8 | 90.1 | 88.0 | 87.8 | 92.8 | 83.8 |
| German | 65.5 | 81.1 | 85.2 | 87.7 | 90.5 | 80.7 |
| Indonesian | 74.3 | 73.9 | 77.5 | 87.6 | 91.1 | 80.8 |
| Malay | 73.1 | 76.8 | 84.7 | 86.2 | 89.7 | 84.7 |
| Italian | 78.5 | 90.5 | 85.5 | 86.0 | 88.1 | 88.9 |
| Polish | 65.4 | 74.2 | 88.8 | 85.9 | 90.0 | 83.6 |
| Russian | 56.8 | 80.3 | 71.7 | 84.5 | 92.2 | 79.5 |
| Croatian | 67.7 | 78.4 | 77.2 | 83.2 | 90.5 | 70.0 |
| Thai | 68.6 | 79.5 | 82.5 | 82.2 | 90.5 | 74.3 |
| Hindi | 64.5 | 72.3 | 70.9 | 81.8 | 87.0 | 74.5 |
| Serbian | 66.5 | 82.0 | 76.8 | 81.6 | 89.7 | 73.1 |
| Uzbek | 59.2 | 81.6 | 76.5 | 81.6 | 87.3 | 62.4 |
| Javanese | 75.9 | 68.2 | 78.4 | 81.5 | 84.2 | 74.2 |
| Marathi | 60.1 | 59.3 | 75.6 | 81.5 | 87.8 | 69.4 |
| Estonian | 51.0 | 77.8 | 83.7 | 81.1 | 88.6 | 35.6 |
| Nepali | 62.8 | 73.0 | 76.7 | 79.0 | 85.2 | 74.2 |
| Khmer | 63.8 | 54.4 | 62.1 | 78.8 | 82.8 | 68.0 |
| Persian | 50.6 | 76.2 | 66.4 | 78.2 | 81.7 | 75.0 |
| Hungarian | 76.5 | 67.4 | 84.7 | 77.9 | 90.2 | 46.7 |
| Azerbaijani | 57.5 | 66.3 | 78.0 | 77.5 | 88.2 | 56.8 |
| Punjabi | 62.0 | 63.3 | 57.0 | 77.5 | 83.8 | 60.7 |
| Bengali | 57.1 | 69.0 | 61.2 | 77.0 | 84.1 | 74.9 |
| Belarusian | 51.8 | 72.5 | 74.9 | 76.7 | 90.0 | 37.8 |
| Georgian | 71.7 | 81.2 | 81.2 | 76.6 | 89.5 | 56.2 |
| Cebuano | 64.3 | 69.4 | 75.0 | 75.6 | 78.8 | 64.6 |
| Slovak | 55.1 | 58.4 | 74.8 | 74.8 | 90.9 | 58.7 |
| Hebrew | 57.0 | 68.4 | 76.5 | 74.5 | 84.7 | 68.6 |
| Kazakh | 53.2 | 73.0 | 67.3 | 74.2 | 83.9 | 62.9 |
| Bulgarian | 56.6 | 72.7 | 79.4 | 73.9 | 89.0 | 54.2 |
| Gujarati | 38.7 | 68.8 | 67.4 | 73.0 | 79.5 | 79.8 |
| Urdu | 59.2 | 76.4 | 80.4 | 72.7 | 83.1 | 70.8 |
| Malayalam | 40.1 | 53.4 | 64.7 | 72.0 | 84.4 | 66.6 |
| Armenian | 53.4 | 72.0 | 77.2 | 71.9 | 86.4 | 53.7 |
| Tagalog | 52.0 | 63.5 | 72.3 | 71.2 | 79.0 | 74.2 |
| Slovene | 60.8 | 82.3 | 81.1 | 70.3 | 88.4 | 47.9 |
| Lithuanian | 51.9 | 76.3 | 76.2 | 69.2 | 88.2 | 38.0 |
| Sinhala | 33.4 | 66.7 | 50.8 | 68.6 | 82.3 | 68.3 |
| Latvian | 54.1 | 68.2 | 73.1 | 68.2 | 91.3 | 36.2 |
| Tamil | 53.8 | 71.9 | 70.8 | 68.0 | 85.5 | 65.2 |
| Swahili | 69.7 | 78.8 | 79.2 | 67.3 | 83.4 | 69.2 |
| Basque | 51.5 | 65.2 | 65.7 | 64.6 | 87.9 | 22.9 |
| Burmese | 40.7 | 51.4 | 49.8 | 62.6 | 83.7 | 78.0 |
| Telugu | 38.4 | 50.6 | 62.5 | 61.4 | 76.7 | 64.7 |

- **Skipped, repeated, and runaway passages**: with the whole text in one request, nothing holds the output to the source's lines, and in some languages the model loses its place. Most often it skips part of the dialogue and goes on to a natural ending, so the line count falls short with no visible break: the 0.8B does so in Burmese, and the 2B and 8B skip 17 to 43 lines in nine languages between them, Telugu at 2B the most. Otherwise it falls into a loop until the output stops: the 0.8B repeats one phrase in Telugu and Sinhala (`වර්ගයේ වර්ගයේ ...`) and three lines of the closing passage in Gujarati, the 2B one word in Khmer at the summary, and the 8B's Japanese goes back from line 53 to line 40 and runs through the same stretch again before jumping ahead. Larger sizes lose their place less often, though not steadily: the 2B does in eight languages and the 8B in five, while the 31B only joins two lines into one in Kazakh and Burmese. These are kept as they are, as part of its performance under its intended use; each size's README lists them.
