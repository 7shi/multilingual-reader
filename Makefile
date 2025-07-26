DATASETS = transformer finetuning onde momentum

all:

split:
	for ds in $(DATASETS); do uv run split_podcast_data.py -o examples/$$ds $$ds.js; done

merge:
	for ds in $(DATASETS); do uv run merge_podcast_data.py -o $$ds.js examples/$$ds-{fr,en,ja}.txt; done
