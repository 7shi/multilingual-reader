all:

split:
	python split_podcast_data.py -o examples/onde onde.js
	python split_podcast_data.py -o examples/momentum momentum.js
