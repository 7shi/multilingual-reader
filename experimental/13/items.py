"""The 50 evaluation items for Experiment 11.

A copy, frozen at the revision this experiment was run on. Experiment 11 is a finished
record rather than a library, and the items are what it tested; sharing the file would let
an edit there silently change what the results in evals50/ claim to mean. Diff the two
before assuming they agree.

Each item is a property the translation should satisfy, phrased positively so that
"yes" always means good. The wording deliberately avoids anything specific to the
source material, so the same item set works for any dialogue script.

The items were derived from the deduction vocabulary that actually appears in the
existing evaluations under examples/tr/onde/*/evals/.
"""

GROUPS = {
    "a": "Structural integrity",
    "b": "Language purity",
    "c": "Semantic fidelity",
    "d": "Terminology",
    "e": "Fluency and naturalness",
}

# (id, criterion shown to the evaluator)
ITEMS = [
    # A. Structural integrity
    ("a01_speaker_label_present", "Every line carries a speaker label."),
    ("a02_speaker_label_consistent", "The same speaker is always written with the same label."),
    ("a03_speaker_attribution", "The speaker of each line matches the speaker of the same line in the original."),
    ("a04_body_present", "No line consists of a speaker label with the body text missing."),
    ("a05_line_correspondence", "Each line renders the content of the line at the same position in the original, with no shifting, merging or reordering."),
    ("a06_sentence_completion", "No sentence or clause is cut off partway."),
    ("a07_no_duplication", "No sentence or line is repeated where the original does not repeat it."),
    ("a08_no_degenerate_loop", "No passage repeats the same character or phrase abnormally many times."),
    ("a09_length_plausibility", "Each line's length is plausible for the corresponding original line, with no extreme inflation or truncation."),
    ("a10_no_inserted_matter", "No headings, numbering, notes or separators have been added that the original does not have."),

    # B. Language purity
    ("b01_target_language", "The entire body text is written in the target language."),
    ("b02_no_source_residue", "No words or sentences of the source language remain untranslated."),
    ("b03_no_third_language", "No words or phrases appear from a language that is neither the source nor the target language."),
    ("b04_no_intraword_intrusion", "No word has a fragment of another language grafted inside it."),
    ("b05_script_consistency", "Only the writing system that the target language's orthography uses appears in the text."),
    ("b06_encoding_integrity", "There is no mojibake, malformed combining sequence or replacement character."),
    ("b07_real_vocabulary", "There are no invented words or misspelled forms that do not exist in the target language."),
    ("b08_no_meta_utterance", "No translation instruction, self-reference or annotation is left in the body text."),
    ("b09_no_reasoning_trace", "No fragment of reasoning or of a system prompt has leaked into the text."),
    ("b10_no_nonlinguistic_noise", "No JSON, HTML tags, placeholders or other non-prose strings appear in the text."),

    # C. Semantic fidelity
    ("c01_propositional_content", "What each line asserts matches the original."),
    ("c02_no_omission", "No information present in the original has been dropped."),
    ("c03_no_addition", "No information absent from the original has been added."),
    ("c04_numeric_accuracy", "Numbers, formulas and quantitative relations are rendered correctly."),
    ("c05_polarity_and_modality", "Negation, condition, supposition and emphasis are preserved in presence and direction."),
    ("c06_proper_nouns", "Personal names and technical designations are carried over correctly."),
    ("c07_logical_relations", "Causal, adversative and coordinating relations between statements are preserved."),
    ("c08_anaphora", "Pronouns and demonstratives refer to the correct antecedents."),
    ("c09_dialogue_coherence", "Each reply or backchannel fits the utterance it responds to."),
    ("c10_word_sense", "No polysemous word or false friend has been taken in the wrong sense."),

    # D. Terminology
    ("d01_standard_terms", "Technical terms use the established equivalents of the target language."),
    ("d02_term_consistency", "The same concept is rendered by the same term throughout."),
    ("d03_borrowing_policy", "The choice between transliteration, loanword and native coinage is applied consistently."),
    ("d04_notation_convention", "Symbols and formulas are written according to the target language's conventions."),
    ("d05_variables_and_units", "Variable symbols and units are preserved as in the original."),
    ("d06_abbreviations", "Abbreviations are expanded, kept or translated appropriately."),
    ("d07_no_needless_coinage", "No unnecessary literal coinage is invented where an established term exists."),
    ("d08_concept_identification", "No term has been applied to the wrong concept."),
    ("d09_gloss_appropriateness", "Explanatory additions the reader needs are present, and no more than needed."),
    ("d10_speaker_name_policy", "Speaker names follow a consistent policy of translation or transliteration."),

    # E. Fluency and naturalness
    ("e01_agreement", "Gender, number and case agreement are correct."),
    ("e02_inflection_and_tense", "Verb inflection, tense and aspect are correct."),
    ("e03_syntax", "Word order and dependency structure read naturally in the target language."),
    ("e04_function_words", "Prepositions, particles and articles are used appropriately."),
    ("e05_no_calque", "There are no unnatural turns of phrase that trace the source language's syntax."),
    ("e06_no_related_language_interference", "No vocabulary or spelling from a closely related language has crept in."),
    ("e07_spoken_register", "The register suits a spoken dialogue."),
    ("e08_politeness_consistency", "Honorific and politeness levels stay consistent for each speaker."),
    ("e09_discourse_markers", "Backchannels, fillers and interjections are handled naturally."),
    ("e10_orthography", "Spelling, diacritics, punctuation and quotation marks are correct."),
]

ITEM_IDS = [item_id for item_id, _ in ITEMS]
CRITERIA = dict(ITEMS)

assert len(ITEMS) == 50, f"expected 50 items, got {len(ITEMS)}"
assert len(set(ITEM_IDS)) == 50, "item ids must be unique"
for _group in GROUPS:
    _n = sum(1 for i in ITEM_IDS if i[0] == _group)
    assert _n == 10, f"group {_group} has {_n} items, expected 10"
