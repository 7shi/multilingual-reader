# Shared definitions for each model directory under plamo/: the onde text, translated
# under PLaMo 3 Translate's conditions (PLAN.md). Each Makefile defines only its
# TRANSLATOR (and OPTIONS, as its onde/ counterpart does) and includes this.

include ../../onde/common.mk

# Set after the include, which would otherwise reset it: PLaMo's supported languages.
LANGS = $(PLAMO_LANGS)

# The whole text in one request per language, with the target language's whole glossary
# column. PLaMo 3 Translate takes the glossary and languages as chat-template variables,
# since trtools translate's instructions, glossary and summary messages do not fit its
# template; a general model gets the same as a system message (trtools whole).
PLAMO_TRANSLATE = uv run trtools plamo $(DIR)/onde-en.txt \
	--terms-dir ../../terms \
	--langs $(LANGS) \
	-m $(TRANSLATOR)
WHOLE_TRANSLATE = uv run trtools whole $(DIR)/onde-en.txt \
	--terms-dir ../../terms \
	--langs $(LANGS) \
	$(OPTIONS) \
	-m $(TRANSLATOR)

# A PLaMo size's Makefile sets TRANSLATE_CMD = $(PLAMO_TRANSLATE) after the include.
TRANSLATE_CMD = $(WHOLE_TRANSLATE)
