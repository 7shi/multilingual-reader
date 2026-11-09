# examples/tr/plamo/

Translates and evaluates the onde text under PLaMo 3 Translate's conditions ([PLAN.md](PLAN.md)): the languages the model supports (`PLAMO_LANGS` in [../common.mk](../common.mk)) and the whole text in one request per language, with the target language's whole column of [../terms/onde-en.tsv](../terms/onde-en.tsv) as the glossary. The shared settings are in [common.mk](common.mk), and each model's `Makefile` names only its `TRANSLATOR`, with a general model's `OPTIONS` as in onde/. See [ADD_PLAMO.md](../ADD_PLAMO.md) for adding a model.

PLaMo's languages differ from the corpus's, and the one-request method differs from the line-by-line translation of [onde/](../onde/), so these results are kept apart from the comparison there and compared only with each other, on these languages.

- [plamo-3-translate-0.8b](plamo-3-translate-0.8b/) (PLaMo 3 Translate 0.8B Q4_K_M, llama.cpp)
- [plamo-3-translate-2b](plamo-3-translate-2b/) (PLaMo 3 Translate 2B Q4_K_M, llama.cpp)
- [plamo-3-translate-8b](plamo-3-translate-8b/) (PLaMo 3 Translate 8B Q4_K_M, llama.cpp)
- [plamo-3-translate-31b](plamo-3-translate-31b/) (PLaMo 3 Translate 31B Q4_K_M, llama.cpp)
- [gpt-6-luna](gpt-6-luna/) (a general model, `trtools whole`; its line-by-line counterpart is [onde/gpt-6-luna](../onde/gpt-6-luna/))
- [gemma4-e2b](gemma4-e2b/) (Gemma 4 E2B, Ollama, `trtools whole`; its line-by-line counterpart is [onde/gemma4-e2b](../onde/gemma4-e2b/))
- [gemma4-e4b](gemma4-e4b/) (Gemma 4 E4B, Ollama, `trtools whole`; its line-by-line counterpart is [onde/gemma4-e4b](../onde/gemma4-e4b/))
- [gemma4-12b](gemma4-12b/) (Gemma 4 12B, Ollama, `trtools whole`; its line-by-line counterpart is [onde/gemma4-12b](../onde/gemma4-12b/))
- [gemma4-26b](gemma4-26b/) (Gemma 4 26B-A4B QAT, MoE, Ollama, `trtools whole`; its line-by-line counterpart is [onde/gemma4](../onde/gemma4/), not QAT)
- [gemma4-31b](gemma4-31b/) (Gemma 4 31B, Ollama, `trtools whole`; its line-by-line counterpart is [onde/gemma4-31b](../onde/gemma4-31b/))

Every model is evaluated by TypeSafe's Jev (`jev-1.14.0`), one run per language, as in onde/.

## Sizes of PLaMo 3 Translate

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical flaws (below 60)

Mean and standard deviation are computed from each model's `SCORES-jev.txt` by `uv run generate_compare_rows.py plamo --jev --sync` in examples/tr/ (Notes are entered manually).

| Model | Mean | Median | Stdev | Notes |
| --- | ---: | ---: | ---: | --- |
| gpt-6-luna | 87.48 | 88.30 | 4.16 | A general model given the same request (`trtools whole`), for reference. Above the 31B in 51 of 52 languages, all but Korean, and keeps all 99 lines in every language; only Telugu, Cebuano, Tagalog, and Gujarati fall below 80 |
| gemma4-31b | 76.90 | 78.75 | 12.35 | Not distinguishable from PLaMo's 31B (above in 23 of 52, p = 0.36), but differs by language: 16 points higher in Burmese and 12 to 15 in Telugu and Gujarati, 26 to 29 lower in Khmer, Georgian, and Estonian. Seven languages reach high quality, and all keep their 99 lines |
| plamo-3-translate-31b | 78.92 | 78.50 | 8.08 | High quality on French, Spanish, both Chinese scripts, and Japanese, and no language below 60; Telugu, Burmese, and Basque are its floor. Keeps its place in all but two languages, each two lines short |
| plamo-3-translate-8b | 75.94 | 77.00 | 9.92 | French and Spanish reach high quality, but Japanese falls to 60.0 when the request loops back over a stretch of the dialogue, and Burmese, Sinhala, and Malayalam each skip 20 to 33 lines |
| plamo-3-translate-2b | 73.36 | 73.75 | 9.51 | Above the 0.8B in 46 of 52 languages; Italian and Dutch reach high quality. Loses its place most often of the four sizes: six languages skip 17 to 43 lines, Khmer stops in a loop, and Vietnamese adds a line |
| gemma4-e4b | 72.25 | 73.75 | 13.39 | Above the E2B in 40 of 52 languages and not distinguishable from PLaMo's 2B or 8B; keeps all 99 lines in every language. Basque, Latvian, Belarusian, Estonian, and Lithuanian fall below 50 |
| gemma4-26b | 65.38 | 71.10 | 22.63 | The MoE (QAT build). Leaves 3 languages in another language (Catalan and German in French, Malay copied in English), all scoring 0, and Khmer breaks off at line 20; Japanese, Urdu, and Estonian lose a line or two. On the other 48 not distinguishable from the E4B |
| gemma4-e2b | 68.12 | 70.40 | 15.36 | A general model given the same request, for reference against PLaMo's small sizes. Above the 0.8B in 38 of 52 languages and not distinguishable from the 2B; French and Spanish reach high quality, but 13 languages fall below 60, Basque, Estonian, Latvian, Belarusian, and Lithuanian under 40. Loses its place only in Uzbek and Thai, by one or two lines |
| plamo-3-translate-0.8b | 61.06 | 62.40 | 10.86 | No language reaches the practical range (Italian, Vietnamese, Spanish, and Hungarian are its best, 76.5–78.5), and 23 fall below 60, with Burmese skipping a stretch and Telugu, Sinhala, and Gujarati ending in loops |
| gemma4-12b | 61.96 | 61.95 | 15.94 | Below the E4B in 47 of 52 languages, at the level of PLaMo's 0.8B: words in other scripts (Chinese, Hangul, Cyrillic, Arabic) break into 27 languages, as in its line-by-line run. Keeps all 99 lines in every language |

Each size is above the next smaller one (Wilcoxon signed-rank, paired by language): 2B over 0.8B in 46 of 52 languages (p < 0.001), 8B over 2B in 31 (p = 0.022), and 31B over 8B in 32 (p = 0.024). The largest step is from 0.8B to 2B; above that the gain is a few points per size, and not every language follows it (the 31B is below the 2B in Swahili, Slovene, and Lithuanian).

gpt-6-luna, a general model given what PLaMo's template carries and nothing more, is above the 31B in 51 of 52 languages (p < 0.001), by 8.6 points on average, and keeps the source's 99 lines in every language without being asked to. Losing one's place is therefore not a cost of the whole-text request itself. On the 45 corpus languages it is also above its own line-by-line translation in [onde/gpt-6-luna](../onde/gpt-6-luna/) (mean 88.0 against 86.0; above in 33, one tie, p = 0.002). The largest gains are in Latvian, Hungarian, Basque, and Thai, where the line-by-line run lost points to typos, a missing speaker label, and grammatical fragments; the largest loss is Persian (7.0 points lower).

gemma4-e2b, the smallest Gemma 4, given the same request, is above the 0.8B in 38 of 52 languages (p = 0.002, 7.0 points on average), not distinguishable from the 2B (above in 22, p = 0.10), and below the 8B (above in 18, p = 0.002). It keeps its place better than PLaMo's small sizes: only Uzbek, which folds one line into another and drops a short reply, and Thai, which leaves out the closing line, fall short, by two lines and one. Against its own line-by-line translation in [onde/gemma4-e2b](../onde/gemma4-e2b/), it is above in 39 of the 45 corpus languages (p < 0.001, mean 67.9 against 59.4).

The larger Gemma 4 sizes do not line up by size. The E4B is above the E2B in 40 of 52 languages (p < 0.001) and not distinguishable from PLaMo's 2B (p = 0.94) or 8B (p = 0.12). The 12B falls below the E4B in 47 (p < 0.001), to the level of the 0.8B (p = 0.52), as words in other scripts break into the middle of its sentences in 27 languages; its line-by-line run in onde/ has them as well (31 languages), so this comes with the model rather than with the request. The 31B is the best of them and not distinguishable from PLaMo's 31B (above in 23 of 52, p = 0.36), with the gap running both ways by language: it is 16 points higher in Burmese and 12 to 15 in Telugu and Gujarati, PLaMo's floor, and 26 to 29 lower in Khmer, Georgian, and Estonian. Across the sizes, Gemma's weakest languages are the same: Basque, Latvian, Estonian, Lithuanian, Belarusian, and Hungarian.

The dense sizes keep their place: only the E2B loses it, in Uzbek and Thai by a line or two, and the E4B, 12B, and 31B keep the source's 99 lines in every language. Skipping and looping over stretches of the dialogue, as PLaMo's 0.8B to 8B do, is therefore not what any small model does with the whole text in one request. The MoE, run in its QAT build (`gemma4:26b-a4b-it-qat`), behaves otherwise: it leaves Catalan and German in French and Malay in English (scoring 0), breaks off Khmer at line 20 after mixing in other scripts, and loses a line or two in Japanese, Urdu, and Estonian. On the 48 languages it translates it is not distinguishable from the E4B (p = 0.40), so it does not perform as its total size would suggest.

Against each size's line-by-line translation in onde/ on the 45 corpus languages, the whole-text request helps the smallest sizes and not the larger ones: the E2B is above in 39 (p < 0.001, 67.9 against 59.4) and the E4B in 32 (p = 0.005, 72.4 against 69.5), while the 12B is below in 34 (p < 0.001, 62.4 against 65.8) and the 31B is not distinguishable (above in 22, p = 0.27, 76.8 against 77.8). The 26B is below [onde/gemma4](../onde/gemma4/) in 35 (p < 0.001, 64.5 against 77.7), and still in 31 of the 41 left once its 4 failed languages are set aside (p < 0.001); since onde/gemma4 ran the Q4_K_M build (`gemma4:26b`), this mixes the method with the quantization.

| Language | 0.8B | 2B | 8B | 31B | gpt-6-luna | gemma4-e2b | gemma4-e4b | gemma4-12b | gemma4-26b | gemma4-31b |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| French | 73.2 | 83.7 | 91.9 | 93.6 | 94.2 | 93.4 | 78.5 | 90.8 | 92.3 | 93.9 |
| Spanish | 77.0 | 78.1 | 90.9 | 92.0 | 94.7 | 91.6 | 91.7 | 91.2 | 91.3 | 93.8 |
| Chinese (Traditional) | 70.5 | 87.3 | 89.0 | 90.8 | 91.7 | 83.0 | 81.7 | 68.2 | 88.9 | 90.5 |
| Chinese | 67.5 | 87.0 | 89.4 | 90.7 | 90.8 | 77.7 | 77.7 | 77.3 | 87.8 | 89.4 |
| Japanese | 70.1 | 76.5 | 60.0 | 90.3 | 91.3 | 77.2 | 87.0 | 70.5 | 89.7 | 90.0 |
| Korean | 67.4 | 85.5 | 79.1 | 88.8 | 88.4 | 86.0 | 84.2 | 87.0 | 78.8 | 88.0 |
| Vietnamese | 77.2 | 73.6 | 87.8 | 88.1 | 90.2 | 84.5 | 87.0 | 76.7 | 86.6 | 89.7 |
| Arabic | 69.0 | 85.9 | 84.2 | 88.0 | 91.5 | 78.5 | 82.3 | 83.0 | 84.8 | 87.5 |
| Catalan | 66.6 | 80.2 | 87.1 | 88.0 | 93.8 | 59.8 | 67.4 | 56.5 | 0.0 | 79.5 |
| Dutch | 71.8 | 90.1 | 88.0 | 87.8 | 92.8 | 83.8 | 87.5 | 76.6 | 88.0 | 84.2 |
| German | 65.5 | 81.1 | 85.2 | 87.7 | 90.5 | 80.7 | 88.1 | 71.2 | 0.0 | 92.3 |
| Indonesian | 74.3 | 73.9 | 77.5 | 87.6 | 91.1 | 80.8 | 87.9 | 87.4 | 88.6 | 89.0 |
| Malay | 73.1 | 76.8 | 84.7 | 86.2 | 89.7 | 84.7 | 86.4 | 75.7 | 0.0 | 84.0 |
| Italian | 78.5 | 90.5 | 85.5 | 86.0 | 88.1 | 88.9 | 89.7 | 75.1 | 88.7 | 91.0 |
| Polish | 65.4 | 74.2 | 88.8 | 85.9 | 90.0 | 83.6 | 82.2 | 86.9 | 83.4 | 89.0 |
| Russian | 56.8 | 80.3 | 71.7 | 84.5 | 92.2 | 79.5 | 87.7 | 74.0 | 79.7 | 92.3 |
| Croatian | 67.7 | 78.4 | 77.2 | 83.2 | 90.5 | 70.0 | 73.3 | 64.2 | 72.8 | 84.1 |
| Thai | 68.6 | 79.5 | 82.5 | 82.2 | 90.5 | 74.3 | 87.7 | 83.7 | 83.7 | 87.0 |
| Hindi | 64.5 | 72.3 | 70.9 | 81.8 | 87.0 | 74.5 | 74.0 | 73.8 | 85.1 | 77.4 |
| Serbian | 66.5 | 82.0 | 76.8 | 81.6 | 89.7 | 73.1 | 73.9 | 77.2 | 71.1 | 78.7 |
| Uzbek | 59.2 | 81.6 | 76.5 | 81.6 | 87.3 | 62.4 | 73.6 | 62.3 | 68.7 | 82.2 |
| Javanese | 75.9 | 68.2 | 78.4 | 81.5 | 84.2 | 74.2 | 66.1 | 61.6 | 76.2 | 81.6 |
| Marathi | 60.1 | 59.3 | 75.6 | 81.5 | 87.8 | 69.4 | 77.0 | 55.0 | 74.7 | 78.3 |
| Estonian | 51.0 | 77.8 | 83.7 | 81.1 | 88.6 | 35.6 | 43.3 | 38.1 | 40.9 | 55.5 |
| Nepali | 62.8 | 73.0 | 76.7 | 79.0 | 85.2 | 74.2 | 78.5 | 69.7 | 76.6 | 75.2 |
| Khmer | 63.8 | 54.4 | 62.1 | 78.8 | 82.8 | 68.0 | 65.8 | 58.7 | 27.9 | 50.0 |
| Persian | 50.6 | 76.2 | 66.4 | 78.2 | 81.7 | 75.0 | 79.5 | 65.9 | 83.5 | 89.1 |
| Hungarian | 76.5 | 67.4 | 84.7 | 77.9 | 90.2 | 46.7 | 59.2 | 38.2 | 51.3 | 58.7 |
| Azerbaijani | 57.5 | 66.3 | 78.0 | 77.5 | 88.2 | 56.8 | 72.9 | 55.8 | 67.2 | 78.6 |
| Punjabi | 62.0 | 63.3 | 57.0 | 77.5 | 83.8 | 60.7 | 63.9 | 53.9 | 69.5 | 65.3 |
| Bengali | 57.1 | 69.0 | 61.2 | 77.0 | 84.1 | 74.9 | 75.1 | 56.6 | 77.9 | 81.2 |
| Belarusian | 51.8 | 72.5 | 74.9 | 76.7 | 90.0 | 37.8 | 42.9 | 35.2 | 54.2 | 64.6 |
| Georgian | 71.7 | 81.2 | 81.2 | 76.6 | 89.5 | 56.2 | 67.2 | 36.5 | 46.1 | 50.2 |
| Cebuano | 64.3 | 69.4 | 75.0 | 75.6 | 78.8 | 64.6 | 70.5 | 55.8 | 71.5 | 71.3 |
| Slovak | 55.1 | 58.4 | 74.8 | 74.8 | 90.9 | 58.7 | 63.5 | 45.0 | 62.3 | 72.7 |
| Hebrew | 57.0 | 68.4 | 76.5 | 74.5 | 84.7 | 68.6 | 73.2 | 55.5 | 62.7 | 80.0 |
| Kazakh | 53.2 | 73.0 | 67.3 | 74.2 | 83.9 | 62.9 | 67.8 | 50.9 | 55.4 | 67.3 |
| Bulgarian | 56.6 | 72.7 | 79.4 | 73.9 | 89.0 | 54.2 | 71.3 | 59.9 | 71.1 | 73.8 |
| Gujarati | 38.7 | 68.8 | 67.4 | 73.0 | 79.5 | 79.8 | 76.9 | 59.1 | 68.5 | 85.5 |
| Urdu | 59.2 | 76.4 | 80.4 | 72.7 | 83.1 | 70.8 | 75.2 | 60.3 | 78.2 | 77.3 |
| Malayalam | 40.1 | 53.4 | 64.7 | 72.0 | 84.4 | 66.6 | 72.1 | 50.8 | 51.9 | 60.6 |
| Armenian | 53.4 | 72.0 | 77.2 | 71.9 | 86.4 | 53.7 | 67.2 | 41.7 | 46.7 | 70.7 |
| Tagalog | 52.0 | 63.5 | 72.3 | 71.2 | 79.0 | 74.2 | 68.7 | 64.5 | 74.3 | 67.8 |
| Slovene | 60.8 | 82.3 | 81.1 | 70.3 | 88.4 | 47.9 | 62.5 | 45.9 | 60.0 | 68.0 |
| Lithuanian | 51.9 | 76.3 | 76.2 | 69.2 | 88.2 | 38.0 | 46.3 | 32.0 | 43.8 | 58.8 |
| Sinhala | 33.4 | 66.7 | 50.8 | 68.6 | 82.3 | 68.3 | 71.4 | 52.9 | 42.6 | 75.0 |
| Latvian | 54.1 | 68.2 | 73.1 | 68.2 | 91.3 | 36.2 | 37.6 | 36.0 | 44.9 | 53.4 |
| Tamil | 53.8 | 71.9 | 70.8 | 68.0 | 85.5 | 65.2 | 58.6 | 52.0 | 72.8 | 73.1 |
| Swahili | 69.7 | 78.8 | 79.2 | 67.3 | 83.4 | 69.2 | 76.8 | 66.6 | 62.4 | 79.1 |
| Basque | 51.5 | 65.2 | 65.7 | 64.6 | 87.9 | 22.9 | 30.4 | 29.1 | 37.3 | 47.5 |
| Burmese | 40.7 | 51.4 | 49.8 | 62.6 | 83.7 | 78.0 | 74.2 | 63.0 | 69.2 | 78.8 |
| Telugu | 38.4 | 50.6 | 62.5 | 61.4 | 76.7 | 64.7 | 71.7 | 66.2 | 68.1 | 76.2 |

- **Skipped, repeated, and runaway passages**: with the whole text in one request, nothing holds the output to the source's lines, and in some languages the model loses its place. Most often it skips part of the dialogue and goes on to a natural ending, so the line count falls short with no visible break: the 0.8B does so in Burmese, and the 2B and 8B skip 17 to 43 lines in nine languages between them, Telugu at 2B the most. Otherwise it falls into a loop until the output stops: the 0.8B repeats one phrase in Telugu and Sinhala (`වර්ගයේ වර්ගයේ ...`) and three lines of the closing passage in Gujarati, the 2B one word in Khmer at the summary, and the 8B's Japanese goes back from line 53 to line 40 and runs through the same stretch again before jumping ahead. Larger sizes lose their place less often, though not steadily: the 2B does in eight languages and the 8B in five, while the 31B only joins two lines into one in Kazakh and Burmese. These are kept as they are, as part of its performance under its intended use; each size's README lists them.
