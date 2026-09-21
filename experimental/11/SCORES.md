# Experiment 11: old vs new evaluation scheme

Old scheme: 5 criteria x 0-20. New scheme: 50 items x yes/partial/no.
Combinations: old 8, new 24.

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

| Translation | gemma4-31b | gpt-oss-120b | qwen3.6 |
| --- | --- | --- | --- |
| gpt-5.6-terra / pl | 68, 69, 79 (range 11) | 95, 68, 92 (range 27) | 87, 72, 69 (range 18) |
| gpt-oss / ia | 88, 94, 93 (range 6) | 86, 91, 92 (range 6) | 80, 89, 80 (range 9) |
| qwen3.8 / ja | 87, 92, 89 (range 5) | 90, 100, 96 (range 10) | 86, 89, 84 (range 5) |
| gemini-3.5-flash-lite / kn | 80, 89, 93 (range 13) | 47, 45, 49 (range 4) | 81, 79, 95 (range 16) |
| ox-alpha / ga | 98, 96, 96 (range 2) | 97, 92, 95 (range 5) | 85, 92, 89 (range 7) |
| qwen3.6-27b / ko | 91, 79, 78 (range 13) | 94, 90, 100 (range 10) | 84, 93, 100 (range 16) |
| gemini-2.5-flash / ru | 94, 98, 98 (range 4) | 95, 96, 97 (range 2) | 96, 100, 95 (range 5) |
| gemini-3-flash / hi | 98, 98, 98 (range 0) | 74, 91, 99 (range 25) | 97, 98, 98 (range 1) |

Mean range: 9.2. Mean stdev: 3.96.

## Dependence on the evaluator model

How far the new scheme's aggregated score moves when the evaluator is swapped.

| Translation | Old (qwen3.6) | gemma4-31b | gpt-oss-120b | qwen3.6 | New spread |
| --- | ---: | ---: | ---: | ---: | ---: |
| gpt-5.6-terra / pl | 69 | 70 | 92 | 74 | 22 |
| gpt-oss / ia | 73 | 94 | 88 | 84 | 10 |
| qwen3.8 / ja | 56 | 92 | 96 | 88 | 8 |
| gemini-3.5-flash-lite / kn | 61 | 89 | 49 | 87 | 40 |
| ox-alpha / ga | 68 | 96 | 98 | 89 | 9 |
| qwen3.6-27b / ko | 77 | 84 | 94 | 94 | 10 |
| gemini-2.5-flash / ru | 85 | 98 | 98 | 97 | 1 |
| gemini-3-flash / hi | 81 | 98 | 92 | 98 | 6 |

## Where the remaining wobble sits

Combinations measured: 24

| Item | Runs disagreed | Share |
| --- | ---: | ---: |
| a01_speaker_label_present | 12 | 50% |
| a03_speaker_attribution | 12 | 50% |
| c01_propositional_content | 12 | 50% |
| a05_line_correspondence | 11 | 46% |
| b07_real_vocabulary | 10 | 42% |
| c03_no_addition | 9 | 38% |
| b02_no_source_residue | 8 | 33% |
| b05_script_consistency | 8 | 33% |
| b01_target_language | 7 | 29% |
| b03_no_third_language | 7 | 29% |
| c09_dialogue_coherence | 7 | 29% |
| d07_no_needless_coinage | 7 | 29% |
| e10_orthography | 7 | 29% |
| a02_speaker_label_consistent | 6 | 25% |
| d04_notation_convention | 6 | 25% |
| e03_syntax | 6 | 25% |
| e06_no_related_language_interference | 6 | 25% |
| a04_body_present | 5 | 21% |
| b04_no_intraword_intrusion | 5 | 21% |
| d03_borrowing_policy | 5 | 21% |
| e02_inflection_and_tense | 5 | 21% |
| e05_no_calque | 5 | 21% |
| a09_length_plausibility | 4 | 17% |
| c02_no_omission | 4 | 17% |
| c10_word_sense | 4 | 17% |
| d02_term_consistency | 4 | 17% |
| d10_speaker_name_policy | 4 | 17% |
| e04_function_words | 4 | 17% |
| e09_discourse_markers | 4 | 17% |
| a06_sentence_completion | 3 | 12% |
| a07_no_duplication | 3 | 12% |
| c06_proper_nouns | 3 | 12% |
| c07_logical_relations | 3 | 12% |
| d01_standard_terms | 3 | 12% |
| d05_variables_and_units | 3 | 12% |
| d08_concept_identification | 3 | 12% |
| d09_gloss_appropriateness | 3 | 12% |
| e07_spoken_register | 3 | 12% |
| e08_politeness_consistency | 3 | 12% |
| a10_no_inserted_matter | 2 | 8% |
| b06_encoding_integrity | 2 | 8% |
| b09_no_reasoning_trace | 2 | 8% |
| b10_no_nonlinguistic_noise | 2 | 8% |
| c04_numeric_accuracy | 2 | 8% |
| e01_agreement | 2 | 8% |
| b08_no_meta_utterance | 1 | 4% |
| c05_polarity_and_modality | 1 | 4% |
| c08_anaphora | 1 | 4% |
| d06_abbreviations | 1 | 4% |

Items that never disagreed: 1/50

## Timing (new scheme, thinking on)

Per-call duration in seconds. Files that record their own "duration_seconds" use that; older files fall back to the file-mtime difference between run n and run (n-1), for n in {2, 3} -- run 1 of each (translation, evaluator) is excluded there, since it would need the previous call's finish time, which belongs to a different translation.

| Evaluator | Calls | Median | Mean | Min | Max |
| --- | ---: | ---: | ---: | ---: | ---: |
| gemma4-31b | 24 | 557s | 798s | 393s | 2912s |
| gpt-oss-120b | 24 | 149s | 160s | 106s | 368s |
| qwen3.6 | 24 | 210s | 245s | 149s | 640s |
| all | 72 | 224s | 401s | 106s | 2912s |

## Group subtotals (new scheme)

| Translation | Evaluator | A | B | C | D | E | Total |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gemini-2.5-flash / ru | gemma4-31b | 18 | 20 | 20 | 20 | 20 | 98 |
| gemini-2.5-flash / ru | gpt-oss-120b | 19 | 19 | 20 | 20 | 20 | 98 |
| gemini-2.5-flash / ru | qwen3.6 | 17 | 20 | 20 | 20 | 20 | 97 |
| gemini-3-flash / hi | gemma4-31b | 18 | 20 | 20 | 20 | 20 | 98 |
| gemini-3-flash / hi | gpt-oss-120b | 20 | 19 | 17 | 18 | 18 | 92 |
| gemini-3-flash / hi | qwen3.6 | 18 | 20 | 20 | 20 | 20 | 98 |
| gemini-3.5-flash-lite / kn | gemma4-31b | 16 | 16 | 18 | 20 | 19 | 89 |
| gemini-3.5-flash-lite / kn | gpt-oss-120b | 13 | 17 | 5 | 9 | 5 | 49 |
| gemini-3.5-flash-lite / kn | qwen3.6 | 20 | 13 | 18 | 18 | 18 | 87 |
| gpt-5.6-terra / pl | gemma4-31b | 12 | 14 | 12 | 16 | 16 | 70 |
| gpt-5.6-terra / pl | gpt-oss-120b | 16 | 20 | 17 | 19 | 20 | 92 |
| gpt-5.6-terra / pl | qwen3.6 | 6 | 14 | 15 | 19 | 20 | 74 |
| gpt-oss / ia | gemma4-31b | 16 | 20 | 18 | 20 | 20 | 94 |
| gpt-oss / ia | gpt-oss-120b | 12 | 20 | 16 | 20 | 20 | 88 |
| gpt-oss / ia | qwen3.6 | 15 | 18 | 18 | 16 | 17 | 84 |
| ox-alpha / ga | gemma4-31b | 18 | 20 | 18 | 20 | 20 | 96 |
| ox-alpha / ga | gpt-oss-120b | 18 | 20 | 20 | 20 | 20 | 98 |
| ox-alpha / ga | qwen3.6 | 19 | 19 | 17 | 17 | 17 | 89 |
| qwen3.6-27b / ko | gemma4-31b | 20 | 12 | 18 | 19 | 15 | 84 |
| qwen3.6-27b / ko | gpt-oss-120b | 20 | 14 | 20 | 20 | 20 | 94 |
| qwen3.6-27b / ko | qwen3.6 | 20 | 14 | 20 | 20 | 20 | 94 |
| qwen3.8 / ja | gemma4-31b | 20 | 12 | 20 | 20 | 20 | 92 |
| qwen3.8 / ja | gpt-oss-120b | 20 | 16 | 20 | 20 | 20 | 96 |
| qwen3.8 / ja | qwen3.6 | 15 | 16 | 19 | 20 | 18 | 88 |
