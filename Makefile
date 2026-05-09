.PHONY: build clean serve deploy

build:
	uv run build.py

clean:
	rm -rf dist

serve:
	cd dist && uv run python -m http.server 8000

deploy: build
	bash deploy.sh
