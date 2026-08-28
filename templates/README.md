# Build and Deploy

For build pipeline / runtime JS / deploy design details, see [../DEPLOY.md](../DEPLOY.md).

## File layout

```
templates/
├── README.md                  # This file
├── build.py                   # Static site builder (uv run templates/build.py)
├── deploy.sh                  # Script that pushes to the gh-pages branch
├── page.html                  # Template for single-language pages
├── multi.html                 # Template for the multilingual side-by-side page
├── index.html                 # Template for the landing page
└── static/
    ├── README.md              # Implementation notes for the audio playback system
    ├── speech.js              # Shared Web Speech API utilities (ES Module)
    ├── reader.js              # JS for single-language pages
    ├── reader-multi.js        # JS for the multilingual side-by-side page
    └── reader.css             # Shared CSS
```

## Prerequisites
- `uv` (Python package manager)
- `git` (uses a worktree to push to the gh-pages branch)

## Local build

```bash
# Generate 24 HTML + index.html + assets into dist/
make build

# Check it locally with a server (localhost:8000)
make serve

# Remove build output
make clean
```

## Deploying to GitHub Pages

```bash
# Build, then push to the gh-pages branch
make deploy
```

`deploy.sh` checks out the `gh-pages` branch into `.gh-pages-worktree/` via `git worktree`, replaces its contents with `dist/`, and commits and pushes. If there's no diff, it does nothing.

## First-time setup

The `gh-pages` branch is created automatically the first time `make deploy` runs.

Steps on the GitHub UI side:

1. Open **Settings → Pages** on the GitHub repository
2. Set **Source** to `Deploy from a branch`
3. Set **Branch** to `gh-pages` / `/ (root)` and click **Save**
