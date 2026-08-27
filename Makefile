.PHONY: help build clean serve deploy

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  build    build site into dist/"
	@echo "  clean    remove dist/"
	@echo "  serve    serve dist/ on localhost:8000"
	@echo "  deploy   build + deploy"

build:
	uv run build.py

clean:
	rm -rf dist

serve:
	cd dist && uv run python -m http.server 8000

deploy: build
	bash deploy.sh
