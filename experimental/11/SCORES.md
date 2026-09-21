# Experiment 11: old vs new evaluation scheme

Old scheme: 5 criteria x 0-20. New scheme: 50 items x yes/partial/no.
Combinations: old 8, new 40.

## Run-to-run wobble under the reference evaluator (qwen3.6)

How far the total score moves across runs on the same translation.

| Translation | Old runs | Old range | New runs | New range | Change |
| --- | --- | ---: | --- | ---: | ---: |
| gpt-5.6-terra / pl | 69, 81, 15 | 66 | 87, 72, 69 | 18 | -48 |
| gpt-oss / ia | 89, 73, 34 | 55 | 80, 89, 80 | 9 | -46 |
| qwen3.8 / ja | 56, 78, 25 | 53 | 86, 89, 84 | 5 | -48 |
| gemini-3.5-flash-lite / kn | 29, 61, 80 | 51 | 81, 79, 95 | 16 | -35 |
| ox-alpha / ga | 38, 68, 89 | 51 | 85, 92, 89 | 7 | -44 |
| qwen3.6-27b / ko | 92, 42, 77 | 50 | 84, 93, 100 | 16 | -34 |
| gemini-2.5-flash / ru | 91, 44, 86 | 47 | 96, 100, 95 | 5 | -42 |
| gemini-3-flash / hi | 91, 81, 45 | 46 | 97, 98, 98 | 1 | -45 |

Mean range: old 52.4, new 9.6.
Mean stdev: old 22.16, new 4.17.

## Run-to-run wobble of the new scheme, by evaluator

| Translation | gemma4-31b | gpt-5.6-luna | gpt-5.6-terra | gpt-oss-120b | qwen3.6 |
| --- | --- | --- | --- | --- | --- |
| gpt-5.6-terra / pl | 68, 69, 79 (range 11) | 75, 77, 80 (range 5) | 80, 67, 79 (range 13) | 95, 68, 92 (range 27) | 87, 72, 69 (range 18) |
| gpt-oss / ia | 88, 94, 93 (range 6) | 57, 59, 50 (range 9) | 54, 46, 51 (range 8) | 86, 91, 92 (range 6) | 80, 89, 80 (range 9) |
| qwen3.8 / ja | 87, 92, 89 (range 5) | 74, 63, 71 (range 11) | 71, 67, 71 (range 4) | 90, 100, 96 (range 10) | 86, 89, 84 (range 5) |
| gemini-3.5-flash-lite / kn | 80, 89, 93 (range 13) | 68, 65, 59 (range 9) | 73, 73, 62 (range 11) | 47, 45, 49 (range 4) | 81, 79, 95 (range 16) |
| ox-alpha / ga | 98, 96, 96 (range 2) | 63, 53, 65 (range 12) | 63, 64, 61 (range 3) | 97, 92, 95 (range 5) | 85, 92, 89 (range 7) |
| qwen3.6-27b / ko | 91, 79, 78 (range 13) | 81, 79, 73 (range 8) | 69, 77, 68 (range 9) | 94, 90, 100 (range 10) | 84, 93, 100 (range 16) |
| gemini-2.5-flash / ru | 94, 98, 98 (range 4) | 92, 90, 92 (range 2) | 92, 88, 93 (range 5) | 95, 96, 97 (range 2) | 96, 100, 95 (range 5) |
| gemini-3-flash / hi | 98, 98, 98 (range 0) | 82, 90, 92 (range 10) | 80, 80, 84 (range 4) | 74, 91, 99 (range 25) | 97, 98, 98 (range 1) |

Mean range: 8.6. Mean stdev: 3.72.

## Dependence on the evaluator model

How far the new scheme's aggregated score moves when the evaluator is swapped.

| Translation | Old (qwen3.6) | gemma4-31b | gpt-5.6-luna | gpt-5.6-terra | gpt-oss-120b | qwen3.6 | New spread |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt-5.6-terra / pl | 69 | 70 | 78 | 79 | 92 | 74 | 22 |
| gpt-oss / ia | 73 | 94 | 56 | 50 | 88 | 84 | 44 |
| qwen3.8 / ja | 56 | 92 | 70 | 69 | 96 | 88 | 27 |
| gemini-3.5-flash-lite / kn | 61 | 89 | 65 | 71 | 49 | 87 | 40 |
| ox-alpha / ga | 68 | 96 | 64 | 61 | 98 | 89 | 37 |
| qwen3.6-27b / ko | 77 | 84 | 81 | 69 | 94 | 94 | 25 |
| gemini-2.5-flash / ru | 85 | 98 | 93 | 93 | 98 | 97 | 5 |
| gemini-3-flash / hi | 81 | 98 | 92 | 81 | 92 | 98 | 17 |

### qwen3.6 vs gpt-oss:120b, new scheme, in the old table's terms

README's "It moves when the evaluator changes" quotes the old scheme's qwen3.6-vs-gpt-oss:120b gap (mean 49.6 vs 69.5, mean absolute difference 21.6) on a different set of translations (examples/tr/onde/qwen3.6/*, all translated by qwen3.6). The same two evaluators on the new scheme, over targets.tsv's 8 translations:

Mean 88.9 against 88.4, with a mean absolute difference of 10.5 points.

## Where the remaining wobble sits

Combinations measured: 40

| Item | Runs disagreed | Share |
| --- | ---: | ---: |
| a03_speaker_attribution | 17 | 42% |
| a05_line_correspondence | 17 | 42% |
| c01_propositional_content | 17 | 42% |
| b02_no_source_residue | 16 | 40% |
| b07_real_vocabulary | 16 | 40% |
| c03_no_addition | 16 | 40% |
| d07_no_needless_coinage | 16 | 40% |
| e03_syntax | 16 | 40% |
| b05_script_consistency | 15 | 38% |
| a01_speaker_label_present | 14 | 35% |
| b01_target_language | 14 | 35% |
| c02_no_omission | 13 | 32% |
| c09_dialogue_coherence | 13 | 32% |
| d03_borrowing_policy | 13 | 32% |
| d04_notation_convention | 13 | 32% |
| e10_orthography | 13 | 32% |
| b03_no_third_language | 12 | 30% |
| b04_no_intraword_intrusion | 12 | 30% |
| a09_length_plausibility | 11 | 28% |
| d01_standard_terms | 10 | 25% |
| e02_inflection_and_tense | 10 | 25% |
| e05_no_calque | 10 | 25% |
| a02_speaker_label_consistent | 9 | 22% |
| c10_word_sense | 9 | 22% |
| d02_term_consistency | 9 | 22% |
| d09_gloss_appropriateness | 9 | 22% |
| a04_body_present | 8 | 20% |
| e06_no_related_language_interference | 8 | 20% |
| e01_agreement | 7 | 18% |
| e04_function_words | 7 | 18% |
| c06_proper_nouns | 6 | 15% |
| e07_spoken_register | 6 | 15% |
| e08_politeness_consistency | 6 | 15% |
| e09_discourse_markers | 6 | 15% |
| a06_sentence_completion | 5 | 12% |
| a10_no_inserted_matter | 5 | 12% |
| c04_numeric_accuracy | 5 | 12% |
| c07_logical_relations | 5 | 12% |
| c08_anaphora | 5 | 12% |
| d05_variables_and_units | 5 | 12% |
| d08_concept_identification | 5 | 12% |
| d10_speaker_name_policy | 5 | 12% |
| a07_no_duplication | 4 | 10% |
| b06_encoding_integrity | 4 | 10% |
| b09_no_reasoning_trace | 4 | 10% |
| b10_no_nonlinguistic_noise | 4 | 10% |
| c05_polarity_and_modality | 4 | 10% |
| b08_no_meta_utterance | 2 | 5% |
| d06_abbreviations | 2 | 5% |

Items that never disagreed: 1/50

## Timing (new scheme, thinking on)

Per-call duration in seconds. Files that record their own "duration_seconds" use that; older files fall back to the file-mtime difference between run n and run (n-1), for n in {2, 3} -- run 1 of each (translation, evaluator) is excluded there, since it would need the previous call's finish time, which belongs to a different translation.

| Evaluator | Calls | Median | Mean | Min | Max |
| --- | ---: | ---: | ---: | ---: | ---: |
| gemma4-31b | 24 | 557s | 798s | 393s | 2912s |
| gpt-5.6-luna | 24 | 31s | 42s | 22s | 91s |
| gpt-5.6-terra | 24 | 42s | 43s | 23s | 70s |
| gpt-oss-120b | 24 | 149s | 160s | 106s | 368s |
| qwen3.6 | 24 | 210s | 245s | 149s | 640s |
| all | 120 | 149s | 258s | 22s | 2912s |

## Timing (new scheme, no-think)

| Evaluator | Calls | Median | Mean | Min | Max |
| --- | ---: | ---: | ---: | ---: | ---: |
| gemma4-31b | 24 | 104s | 110s | 93s | 149s |
| gpt-5.6-luna | 24 | 42s | 43s | 16s | 82s |
| gpt-5.6-terra | 24 | 39s | 39s | 24s | 65s |
| gpt-oss-120b | 24 | 155s | 160s | 95s | 272s |
| qwen3.6 | 24 | 19s | 23s | 17s | 44s |
| all | 120 | 48s | 75s | 16s | 272s |

## Timing (new scheme, thinking on, no evidence)

| Evaluator | Calls | Median | Mean | Min | Max |
| --- | ---: | ---: | ---: | ---: | ---: |
| gemma4-31b | 24 | 376s | 382s | 260s | 584s |
| gpt-5.6-luna | 24 | 38s | 39s | 14s | 78s |
| gpt-5.6-terra | 24 | 33s | 34s | 17s | 51s |
| gpt-oss-120b | 24 | 118s | 124s | 94s | 246s |
| qwen3.6 | 24 | 155s | 156s | 122s | 198s |
| all | 120 | 118s | 147s | 14s | 584s |

## Thinking on vs off

Same 50-item scheme, same targets and evaluators, run with `--no-think --no-evidence`. Score is the median-of-runs total; time is the mean call duration from "duration_seconds". gpt-oss:120b ignores `--no-think`, so its rows are thinking-on/evidence-off, not no-think.

| Translation | Evaluator | Think score | No-think score | Diff | Think time | No-think time |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| gpt-5.6-terra / pl | gemma4-31b | 70 | 76 | +6 | 767s | 119s |
| gpt-5.6-terra / pl | gpt-5.6-luna | 78 | 70 | -8 | 26s | 44s |
| gpt-5.6-terra / pl | gpt-5.6-terra | 79 | 77 | -2 | 41s | 49s |
| gpt-5.6-terra / pl | gpt-oss-120b | 92 | 96 | +4 | 162s | 157s |
| gpt-5.6-terra / pl | qwen3.6 | 74 | 74 | +0 | 246s | 18s |
| gpt-oss / ia | gemma4-31b | 94 | 87 | -7 | 1366s | 113s |
| gpt-oss / ia | gpt-5.6-luna | 56 | 64 | +8 | 33s | 48s |
| gpt-oss / ia | gpt-5.6-terra | 50 | 51 | +1 | 58s | 42s |
| gpt-oss / ia | gpt-oss-120b | 88 | 88 | +0 | 163s | 143s |
| gpt-oss / ia | qwen3.6 | 84 | 75 | -9 | 349s | 25s |
| qwen3.8 / ja | gemma4-31b | 92 | 95 | +3 | 929s | 109s |
| qwen3.8 / ja | gpt-5.6-luna | 70 | 77 | +7 | 28s | 43s |
| qwen3.8 / ja | gpt-5.6-terra | 69 | 71 | +2 | 37s | 34s |
| qwen3.8 / ja | gpt-oss-120b | 96 | 95 | -1 | 130s | 157s |
| qwen3.8 / ja | qwen3.6 | 88 | 78 | -10 | 231s | 20s |
| gemini-3.5-flash-lite / kn | gemma4-31b | 89 | 90 | +1 | 444s | 113s |
| gemini-3.5-flash-lite / kn | gpt-5.6-luna | 65 | 57 | -8 | 33s | 34s |
| gemini-3.5-flash-lite / kn | gpt-5.6-terra | 71 | 66 | -5 | 43s | 35s |
| gemini-3.5-flash-lite / kn | gpt-oss-120b | 49 | 52 | +3 | 141s | 145s |
| gemini-3.5-flash-lite / kn | qwen3.6 | 87 | 56 | -31 | 208s | 25s |
| ox-alpha / ga | gemma4-31b | 96 | 93 | -3 | 701s | 104s |
| ox-alpha / ga | gpt-5.6-luna | 64 | 64 | +0 | 49s | 49s |
| ox-alpha / ga | gpt-5.6-terra | 61 | 61 | +0 | 46s | 31s |
| ox-alpha / ga | gpt-oss-120b | 98 | 91 | -7 | 246s | 200s |
| ox-alpha / ga | qwen3.6 | 89 | 57 | -32 | 252s | 20s |
| qwen3.6-27b / ko | gemma4-31b | 84 | 92 | +8 | 1098s | 110s |
| qwen3.6-27b / ko | gpt-5.6-luna | 81 | 72 | -9 | 55s | 30s |
| qwen3.6-27b / ko | gpt-5.6-terra | 69 | 74 | +5 | 30s | 34s |
| qwen3.6-27b / ko | gpt-oss-120b | 94 | 90 | -4 | 128s | 154s |
| qwen3.6-27b / ko | qwen3.6 | 94 | 80 | -14 | 190s | 20s |
| gemini-2.5-flash / ru | gemma4-31b | 98 | 97 | -1 | 494s | 102s |
| gemini-2.5-flash / ru | gpt-5.6-luna | 93 | 95 | +2 | 52s | 42s |
| gemini-2.5-flash / ru | gpt-5.6-terra | 93 | 90 | -3 | 36s | 39s |
| gemini-2.5-flash / ru | gpt-oss-120b | 98 | 100 | +2 | 156s | 148s |
| gemini-2.5-flash / ru | qwen3.6 | 97 | 85 | -12 | 273s | 27s |
| gemini-3-flash / hi | gemma4-31b | 98 | 88 | -10 | 589s | 108s |
| gemini-3-flash / hi | gpt-5.6-luna | 92 | 86 | -6 | 61s | 56s |
| gemini-3-flash / hi | gpt-5.6-terra | 81 | 82 | +1 | 52s | 51s |
| gemini-3-flash / hi | gpt-oss-120b | 92 | 91 | -1 | 152s | 177s |
| gemini-3-flash / hi | qwen3.6 | 98 | 87 | -11 | 209s | 26s |

## Evidence on vs off (thinking on)

Same 50-item scheme with `--no-evidence` only, which separates the per-item evidence field from the thinking change `evals-nt` makes at the same time.

| Translation | Evaluator | Evidence score | No-evidence score | Diff | Evidence time | No-evidence time |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| gpt-5.6-terra / pl | gemma4-31b | 70 | 90 | +20 | 767s | 413s |
| gpt-5.6-terra / pl | gpt-5.6-luna | 78 | 81 | +3 | 26s | 39s |
| gpt-5.6-terra / pl | gpt-5.6-terra | 79 | 72 | -7 | 41s | 30s |
| gpt-5.6-terra / pl | gpt-oss-120b | 92 | 83 | -9 | 162s | 150s |
| gpt-5.6-terra / pl | qwen3.6 | 74 | 80 | +6 | 246s | 158s |
| gpt-oss / ia | gemma4-31b | 94 | 95 | +1 | 1366s | 447s |
| gpt-oss / ia | gpt-5.6-luna | 56 | 63 | +7 | 33s | 40s |
| gpt-oss / ia | gpt-5.6-terra | 50 | 50 | +0 | 58s | 36s |
| gpt-oss / ia | gpt-oss-120b | 88 | 89 | +1 | 163s | 115s |
| gpt-oss / ia | qwen3.6 | 84 | 92 | +8 | 349s | 175s |
| qwen3.8 / ja | gemma4-31b | 92 | 96 | +4 | 929s | 330s |
| qwen3.8 / ja | gpt-5.6-luna | 70 | 76 | +6 | 28s | 35s |
| qwen3.8 / ja | gpt-5.6-terra | 69 | 75 | +6 | 37s | 38s |
| qwen3.8 / ja | gpt-oss-120b | 96 | 99 | +3 | 130s | 120s |
| qwen3.8 / ja | qwen3.6 | 88 | 87 | -1 | 231s | 152s |
| gemini-3.5-flash-lite / kn | gemma4-31b | 89 | 96 | +7 | 444s | 332s |
| gemini-3.5-flash-lite / kn | gpt-5.6-luna | 65 | 55 | -10 | 33s | 31s |
| gemini-3.5-flash-lite / kn | gpt-5.6-terra | 71 | 64 | -7 | 43s | 41s |
| gemini-3.5-flash-lite / kn | gpt-oss-120b | 49 | 37 | -12 | 141s | 113s |
| gemini-3.5-flash-lite / kn | qwen3.6 | 87 | 82 | -5 | 208s | 149s |
| ox-alpha / ga | gemma4-31b | 96 | 95 | -1 | 701s | 376s |
| ox-alpha / ga | gpt-5.6-luna | 64 | 62 | -2 | 49s | 44s |
| ox-alpha / ga | gpt-5.6-terra | 61 | 61 | +0 | 46s | 32s |
| ox-alpha / ga | gpt-oss-120b | 98 | 97 | -1 | 246s | 110s |
| ox-alpha / ga | qwen3.6 | 89 | 89 | +0 | 252s | 173s |
| qwen3.6-27b / ko | gemma4-31b | 84 | 94 | +10 | 1098s | 282s |
| qwen3.6-27b / ko | gpt-5.6-luna | 81 | 74 | -7 | 55s | 30s |
| qwen3.6-27b / ko | gpt-5.6-terra | 69 | 78 | +9 | 30s | 33s |
| qwen3.6-27b / ko | gpt-oss-120b | 94 | 93 | -1 | 128s | 114s |
| qwen3.6-27b / ko | qwen3.6 | 94 | 97 | +3 | 190s | 146s |
| gemini-2.5-flash / ru | gemma4-31b | 98 | 97 | -1 | 494s | 399s |
| gemini-2.5-flash / ru | gpt-5.6-luna | 93 | 92 | -1 | 52s | 39s |
| gemini-2.5-flash / ru | gpt-5.6-terra | 93 | 90 | -3 | 36s | 34s |
| gemini-2.5-flash / ru | gpt-oss-120b | 98 | 100 | +2 | 156s | 122s |
| gemini-2.5-flash / ru | qwen3.6 | 97 | 98 | +1 | 273s | 146s |
| gemini-3-flash / hi | gemma4-31b | 98 | 93 | -5 | 589s | 476s |
| gemini-3-flash / hi | gpt-5.6-luna | 92 | 84 | -8 | 61s | 51s |
| gemini-3-flash / hi | gpt-5.6-terra | 81 | 68 | -13 | 52s | 28s |
| gemini-3-flash / hi | gpt-oss-120b | 92 | 100 | +8 | 152s | 144s |
| gemini-3-flash / hi | qwen3.6 | 98 | 96 | -2 | 209s | 145s |

### Which item verdicts move when evidence is dropped

Per-item median verdicts compared against `evals/` on the same (translation, evaluator). A variant can leave the total untouched while individual verdicts move in both directions, so the totals above do not answer this on their own.

| Evaluator | Combinations | Items moved (mean of 50) | Max |
| --- | ---: | ---: | ---: |
| gemma4-31b | 8 | 4.6 | 14 |
| gpt-5.6-luna | 8 | 8.8 | 11 |
| gpt-5.6-terra | 8 | 8.4 | 15 |
| gpt-oss-120b | 8 | 5.8 | 14 |
| qwen3.6 | 8 | 7.0 | 15 |

Items that moved in at least one of the 40 combinations: 48/50.

| Item | Combinations moved | Share |
| --- | ---: | ---: |
| b07_real_vocabulary | 15 | 38% |
| b01_target_language | 11 | 28% |
| e10_orthography | 11 | 28% |
| b05_script_consistency | 10 | 25% |
| c09_dialogue_coherence | 10 | 25% |
| a03_speaker_attribution | 9 | 22% |
| b02_no_source_residue | 9 | 22% |
| b03_no_third_language | 9 | 22% |
| c03_no_addition | 9 | 22% |
| e03_syntax | 9 | 22% |
| e06_no_related_language_interference | 9 | 22% |
| b04_no_intraword_intrusion | 8 | 20% |
| c01_propositional_content | 8 | 20% |
| c02_no_omission | 8 | 20% |
| d07_no_needless_coinage | 8 | 20% |
| e01_agreement | 8 | 20% |
| a01_speaker_label_present | 7 | 18% |
| a10_no_inserted_matter | 7 | 18% |
| d02_term_consistency | 7 | 18% |
| a04_body_present | 6 | 15% |
| a05_line_correspondence | 6 | 15% |
| c10_word_sense | 6 | 15% |
| d01_standard_terms | 6 | 15% |
| d03_borrowing_policy | 6 | 15% |
| e02_inflection_and_tense | 6 | 15% |
| d04_notation_convention | 5 | 12% |
| e05_no_calque | 5 | 12% |
| e07_spoken_register | 5 | 12% |
| e08_politeness_consistency | 5 | 12% |
| e09_discourse_markers | 5 | 12% |
| a09_length_plausibility | 4 | 10% |
| c06_proper_nouns | 4 | 10% |
| d09_gloss_appropriateness | 4 | 10% |
| a02_speaker_label_consistent | 3 | 8% |
| a06_sentence_completion | 3 | 8% |
| c04_numeric_accuracy | 3 | 8% |
| c05_polarity_and_modality | 3 | 8% |
| c07_logical_relations | 3 | 8% |
| d08_concept_identification | 3 | 8% |
| a07_no_duplication | 2 | 5% |
| b08_no_meta_utterance | 2 | 5% |
| b10_no_nonlinguistic_noise | 2 | 5% |
| c08_anaphora | 2 | 5% |
| b06_encoding_integrity | 1 | 2% |
| b09_no_reasoning_trace | 1 | 2% |
| d05_variables_and_units | 1 | 2% |
| d10_speaker_name_policy | 1 | 2% |
| e04_function_words | 1 | 2% |

## Group subtotals (new scheme)

| Translation | Evaluator | A | B | C | D | E | Total |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gemini-2.5-flash / ru | gemma4-31b | 18 | 20 | 20 | 20 | 20 | 98 |
| gemini-2.5-flash / ru | gpt-5.6-luna | 14 | 20 | 19 | 20 | 20 | 93 |
| gemini-2.5-flash / ru | gpt-5.6-terra | 16 | 20 | 18 | 20 | 19 | 93 |
| gemini-2.5-flash / ru | gpt-oss-120b | 19 | 19 | 20 | 20 | 20 | 98 |
| gemini-2.5-flash / ru | qwen3.6 | 17 | 20 | 20 | 20 | 20 | 97 |
| gemini-3-flash / hi | gemma4-31b | 18 | 20 | 20 | 20 | 20 | 98 |
| gemini-3-flash / hi | gpt-5.6-luna | 16 | 19 | 20 | 20 | 17 | 92 |
| gemini-3-flash / hi | gpt-5.6-terra | 16 | 14 | 17 | 17 | 17 | 81 |
| gemini-3-flash / hi | gpt-oss-120b | 20 | 19 | 17 | 18 | 18 | 92 |
| gemini-3-flash / hi | qwen3.6 | 18 | 20 | 20 | 20 | 20 | 98 |
| gemini-3.5-flash-lite / kn | gemma4-31b | 16 | 16 | 18 | 20 | 19 | 89 |
| gemini-3.5-flash-lite / kn | gpt-5.6-luna | 18 | 11 | 13 | 11 | 12 | 65 |
| gemini-3.5-flash-lite / kn | gpt-5.6-terra | 18 | 10 | 14 | 13 | 16 | 71 |
| gemini-3.5-flash-lite / kn | gpt-oss-120b | 13 | 17 | 5 | 9 | 5 | 49 |
| gemini-3.5-flash-lite / kn | qwen3.6 | 20 | 13 | 18 | 18 | 18 | 87 |
| gpt-5.6-terra / pl | gemma4-31b | 12 | 14 | 12 | 16 | 16 | 70 |
| gpt-5.6-terra / pl | gpt-5.6-luna | 11 | 17 | 14 | 18 | 18 | 78 |
| gpt-5.6-terra / pl | gpt-5.6-terra | 13 | 14 | 15 | 19 | 18 | 79 |
| gpt-5.6-terra / pl | gpt-oss-120b | 16 | 20 | 17 | 19 | 20 | 92 |
| gpt-5.6-terra / pl | qwen3.6 | 6 | 14 | 15 | 19 | 20 | 74 |
| gpt-oss / ia | gemma4-31b | 16 | 20 | 18 | 20 | 20 | 94 |
| gpt-oss / ia | gpt-5.6-luna | 11 | 16 | 12 | 13 | 4 | 56 |
| gpt-oss / ia | gpt-5.6-terra | 11 | 12 | 12 | 11 | 4 | 50 |
| gpt-oss / ia | gpt-oss-120b | 12 | 20 | 16 | 20 | 20 | 88 |
| gpt-oss / ia | qwen3.6 | 15 | 18 | 18 | 16 | 17 | 84 |
| ox-alpha / ga | gemma4-31b | 18 | 20 | 18 | 20 | 20 | 96 |
| ox-alpha / ga | gpt-5.6-luna | 17 | 16 | 13 | 11 | 7 | 64 |
| ox-alpha / ga | gpt-5.6-terra | 18 | 15 | 11 | 11 | 6 | 61 |
| ox-alpha / ga | gpt-oss-120b | 18 | 20 | 20 | 20 | 20 | 98 |
| ox-alpha / ga | qwen3.6 | 19 | 19 | 17 | 17 | 17 | 89 |
| qwen3.6-27b / ko | gemma4-31b | 20 | 12 | 18 | 19 | 15 | 84 |
| qwen3.6-27b / ko | gpt-5.6-luna | 20 | 15 | 15 | 19 | 12 | 81 |
| qwen3.6-27b / ko | gpt-5.6-terra | 20 | 11 | 12 | 18 | 8 | 69 |
| qwen3.6-27b / ko | gpt-oss-120b | 20 | 14 | 20 | 20 | 20 | 94 |
| qwen3.6-27b / ko | qwen3.6 | 20 | 14 | 20 | 20 | 20 | 94 |
| qwen3.8 / ja | gemma4-31b | 20 | 12 | 20 | 20 | 20 | 92 |
| qwen3.8 / ja | gpt-5.6-luna | 20 | 10 | 15 | 16 | 9 | 70 |
| qwen3.8 / ja | gpt-5.6-terra | 20 | 10 | 13 | 16 | 10 | 69 |
| qwen3.8 / ja | gpt-oss-120b | 20 | 16 | 20 | 20 | 20 | 96 |
| qwen3.8 / ja | qwen3.6 | 15 | 16 | 19 | 20 | 18 | 88 |
