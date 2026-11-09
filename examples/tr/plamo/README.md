# examples/tr/plamo/

Translates and evaluates the onde text under PLaMo 3 Translate's conditions ([PLAN.md](PLAN.md)): the languages the model supports (`PLAMO_LANGS` in [../common.mk](../common.mk)) and the whole text in one request per language, with the target language's whole column of [../terms/onde-en.tsv](../terms/onde-en.tsv) as the glossary. The shared settings are in [common.mk](common.mk), and each model's `Makefile` names only its `TRANSLATOR`, with a general model's `OPTIONS` as in onde/. See [ADD_PLAMO.md](../ADD_PLAMO.md) for adding a model.

PLaMo's languages differ from the corpus's, and the one-request method differs from the line-by-line translation of [onde/](../onde/), so these results are kept apart from the comparison there and compared only with each other, on these languages.

- [plamo-3-translate-0.8b](plamo-3-translate-0.8b/) (PLaMo 3 Translate 0.8B Q4_K_M, llama.cpp)
- [plamo-3-translate-2b](plamo-3-translate-2b/) (PLaMo 3 Translate 2B Q4_K_M, llama.cpp)
- [plamo-3-translate-8b](plamo-3-translate-8b/) (PLaMo 3 Translate 8B Q4_K_M, llama.cpp)
- [plamo-3-translate-31b](plamo-3-translate-31b/) (PLaMo 3 Translate 31B Q4_K_M, llama.cpp)
- [gpt-6-luna](gpt-6-luna/) (a general model, `trtools whole`; its line-by-line counterpart is [onde/gpt-6-luna](../onde/gpt-6-luna/))
- [gpt-6-astra](gpt-6-astra/) (a general model, `trtools whole`; its line-by-line counterpart is [onde/gpt-6-astra](../onde/gpt-6-astra/))
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
| gpt-6-astra | 87.16 | 87.85 | 4.22 | A second general model from the API, beside gpt-6-luna. Not distinguishable from it (above in 16 of 52, p = 0.15) and above the 31B in 50; keeps all 99 lines in every language. Only Cebuano and Telugu fall below 80 |
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

gpt-6-astra, given the same request, is not distinguishable from gpt-6-luna (above in 16 of 52, two ties, p = 0.15; mean 87.16 against 87.48) and is above the 31B in 50 (p < 0.001), keeping the source's 99 lines in every language as well. On the 45 corpus languages it is not distinguishable from its own line-by-line translation in [onde/gpt-6-astra](../onde/gpt-6-astra/) either (mean 87.6 against 87.3; above in 26, two ties, p = 0.056): for both API models the whole-text request costs nothing, and gives gpt-6-luna a little.

gemma4-e2b, the smallest Gemma 4, given the same request, is above the 0.8B in 38 of 52 languages (p = 0.002, 7.0 points on average), not distinguishable from the 2B (above in 22, p = 0.10), and below the 8B (above in 18, p = 0.002). It keeps its place better than PLaMo's small sizes: only Uzbek, which folds one line into another and drops a short reply, and Thai, which leaves out the closing line, fall short, by two lines and one. Against its own line-by-line translation in [onde/gemma4-e2b](../onde/gemma4-e2b/), it is above in 39 of the 45 corpus languages (p < 0.001, mean 67.9 against 59.4).

The larger Gemma 4 sizes do not line up by size. The E4B is above the E2B in 40 of 52 languages (p < 0.001) and not distinguishable from PLaMo's 2B (p = 0.94) or 8B (p = 0.12). The 12B falls below the E4B in 47 (p < 0.001), to the level of the 0.8B (p = 0.52), as words in other scripts break into the middle of its sentences in 27 languages; its line-by-line run in onde/ has them as well (31 languages), so this comes with the model rather than with the request. The 31B is the best of them and not distinguishable from PLaMo's 31B (above in 23 of 52, p = 0.36), with the gap running both ways by language: it is 16 points higher in Burmese and 12 to 15 in Telugu and Gujarati, PLaMo's floor, and 26 to 29 lower in Khmer, Georgian, and Estonian. Across the sizes, Gemma's weakest languages are the same: Basque, Latvian, Estonian, Lithuanian, Belarusian, and Hungarian.

The dense sizes keep their place: only the E2B loses it, in Uzbek and Thai by a line or two, and the E4B, 12B, and 31B keep the source's 99 lines in every language. Skipping and looping over stretches of the dialogue, as PLaMo's 0.8B to 8B do, is therefore not what any small model does with the whole text in one request. The MoE, run in its QAT build (`gemma4:26b-a4b-it-qat`), behaves otherwise: it leaves Catalan and German in French and Malay in English (scoring 0), breaks off Khmer at line 20 after mixing in other scripts, and loses a line or two in Japanese, Urdu, and Estonian. On the 48 languages it translates it is not distinguishable from the E4B (p = 0.40), so it does not perform as its total size would suggest.

Against each size's line-by-line translation in onde/ on the 45 corpus languages, the whole-text request helps the smallest sizes and not the larger ones: the E2B is above in 39 (p < 0.001, 67.9 against 59.4) and the E4B in 32 (p = 0.005, 72.4 against 69.5), while the 12B is below in 34 (p < 0.001, 62.4 against 65.8) and the 31B is not distinguishable (above in 22, p = 0.27, 76.8 against 77.8). The 26B is below [onde/gemma4](../onde/gemma4/) in 35 (p < 0.001, 64.5 against 77.7), and still in 31 of the 41 left once its 4 failed languages are set aside (p < 0.001); since onde/gemma4 ran the Q4_K_M build (`gemma4:26b`), this mixes the method with the quantization.

| Language | 0.8B | 2B | 8B | 31B |
| --- | ---: | ---: | ---: | ---: |
| Arabic | 69.0 | 85.9 | 84.2 | 88.0 |
| Armenian | 53.4 | 72.0 | 77.2 | 71.9 |
| Azerbaijani | 57.5 | 66.3 | 78.0 | 77.5 |
| Basque | 51.5 | 65.2 | 65.7 | 64.6 |
| Belarusian | 51.8 | 72.5 | 74.9 | 76.7 |
| Bengali | 57.1 | 69.0 | 61.2 | 77.0 |
| Bulgarian | 56.6 | 72.7 | 79.4 | 73.9 |
| Burmese | 40.7 | 51.4 | 49.8 | 62.6 |
| Catalan | 66.6 | 80.2 | 87.1 | 88.0 |
| Cebuano | 64.3 | 69.4 | 75.0 | 75.6 |
| Chinese | 67.5 | 87.0 | 89.4 | 90.7 |
| Chinese (Traditional) | 70.5 | 87.3 | 89.0 | 90.8 |
| Croatian | 67.7 | 78.4 | 77.2 | 83.2 |
| Dutch | 71.8 | 90.1 | 88.0 | 87.8 |
| Estonian | 51.0 | 77.8 | 83.7 | 81.1 |
| French | 73.2 | 83.7 | 91.9 | 93.6 |
| Georgian | 71.7 | 81.2 | 81.2 | 76.6 |
| German | 65.5 | 81.1 | 85.2 | 87.7 |
| Gujarati | 38.7 | 68.8 | 67.4 | 73.0 |
| Hebrew | 57.0 | 68.4 | 76.5 | 74.5 |
| Hindi | 64.5 | 72.3 | 70.9 | 81.8 |
| Hungarian | 76.5 | 67.4 | 84.7 | 77.9 |
| Indonesian | 74.3 | 73.9 | 77.5 | 87.6 |
| Italian | 78.5 | 90.5 | 85.5 | 86.0 |
| Japanese | 70.1 | 76.5 | 60.0 | 90.3 |
| Javanese | 75.9 | 68.2 | 78.4 | 81.5 |
| Kazakh | 53.2 | 73.0 | 67.3 | 74.2 |
| Khmer | 63.8 | 54.4 | 62.1 | 78.8 |
| Korean | 67.4 | 85.5 | 79.1 | 88.8 |
| Latvian | 54.1 | 68.2 | 73.1 | 68.2 |
| Lithuanian | 51.9 | 76.3 | 76.2 | 69.2 |
| Malay | 73.1 | 76.8 | 84.7 | 86.2 |
| Malayalam | 40.1 | 53.4 | 64.7 | 72.0 |
| Marathi | 60.1 | 59.3 | 75.6 | 81.5 |
| Nepali | 62.8 | 73.0 | 76.7 | 79.0 |
| Persian | 50.6 | 76.2 | 66.4 | 78.2 |
| Polish | 65.4 | 74.2 | 88.8 | 85.9 |
| Punjabi | 62.0 | 63.3 | 57.0 | 77.5 |
| Russian | 56.8 | 80.3 | 71.7 | 84.5 |
| Serbian | 66.5 | 82.0 | 76.8 | 81.6 |
| Sinhala | 33.4 | 66.7 | 50.8 | 68.6 |
| Slovak | 55.1 | 58.4 | 74.8 | 74.8 |
| Slovene | 60.8 | 82.3 | 81.1 | 70.3 |
| Spanish | 77.0 | 78.1 | 90.9 | 92.0 |
| Swahili | 69.7 | 78.8 | 79.2 | 67.3 |
| Tagalog | 52.0 | 63.5 | 72.3 | 71.2 |
| Tamil | 53.8 | 71.9 | 70.8 | 68.0 |
| Telugu | 38.4 | 50.6 | 62.5 | 61.4 |
| Thai | 68.6 | 79.5 | 82.5 | 82.2 |
| Urdu | 59.2 | 76.4 | 80.4 | 72.7 |
| Uzbek | 59.2 | 81.6 | 76.5 | 81.6 |
| Vietnamese | 77.2 | 73.6 | 87.8 | 88.1 |

- **Skipped, repeated, and runaway passages**: with the whole text in one request, nothing holds the output to the source's lines, and in some languages the model loses its place. Most often it skips part of the dialogue and goes on to a natural ending, so the line count falls short with no visible break: the 0.8B does so in Burmese, and the 2B and 8B skip 17 to 43 lines in nine languages between them, Telugu at 2B the most. Otherwise it falls into a loop until the output stops: the 0.8B repeats one phrase in Telugu and Sinhala (`වර්ගයේ වර්ගයේ ...`) and three lines of the closing passage in Gujarati, the 2B one word in Khmer at the summary, and the 8B's Japanese goes back from line 53 to line 40 and runs through the same stretch again before jumping ahead. Larger sizes lose their place less often, though not steadily: the 2B does in eight languages and the 8B in five, while the 31B only joins two lines into one in Kazakh and Burmese. These are kept as they are, as part of its performance under its intended use; each size's README lists them.

## Reliability of the Evaluation and the Choice of API Model

Every comparison here rests on Jev's scores, so what it can tell apart bounds what these results show. Two findings suggest that it tells apart differences of a few points, in the middle of the scale and near its top:

- **Middle of the scale**: PLaMo's four sizes, one model at different sizes, come out in order of size, each above the next smaller one (p < 0.001, 0.022, and 0.024). In the 60–80 range, the scores follow a difference known in advance.
- **Near the top**: gpt-6-luna's whole-text translation is above its line-by-line one by two points (88.0 against 86.0, p = 0.002), and the languages where the line-by-line run lost points show concrete defects in the text: typos, a missing speaker label, and grammatical fragments. Around 85–90, a gap of a few points still matches flaws that can be read in the translation.

So the lack of a difference between gpt-6-astra and gpt-6-luna (p = 0.15 on PLaMo's 52 languages) is better read as the two translating about equally well than as the evaluator running out of resolution. gpt-6-astra, the top model, costs about ten times as much as gpt-6-luna; for translation, at least as far as these evaluations can see, it gains nothing, and gpt-6-luna is enough as the API reference.
