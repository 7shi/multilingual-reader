# Shared definitions for each model directory under plamo/: the onde text, translated
# under PLaMo 3 Translate's conditions (PLAN.md). Each Makefile defines only its
# TRANSLATOR and includes this.

include ../../onde/common.mk

# Set after the include, which would otherwise reset them. PLaMo's supported languages,
# the whole text in one request per language with the glossary as a template variable:
# trtools translate's instructions, glossary and summary messages do not fit the model's
# chat template.
LANGS = $(PLAMO_LANGS)
TRANSLATE_CMD = uv run trtools plamo $(DIR)/onde-en.txt \
	--terms-dir ../../terms \
	--langs $(LANGS) \
	-m $(TRANSLATOR)
