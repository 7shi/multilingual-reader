all:

split:
	uv run split_podcast_data.py -o examples/transformer transformer.js
	uv run split_podcast_data.py -o examples/onde onde.js
	uv run split_podcast_data.py -o examples/momentum momentum.js

merge:
	uv run merge_podcast_data.py -o transformer.js examples/transformer-{fr,en,ja}.txt
	uv run merge_podcast_data.py -o onde.js examples/onde-{fr,en,ja}.txt
	uv run merge_podcast_data.py -o momentum.js examples/momentum-{fr,en,ja}.txt
