#!/usr/bin/env bash
# Deploy multilingual-reader to GitHub Pages (the gh-pages branch).
# Run via `bash templates/deploy.sh`. No need for chmod +x.
# Prerequisite: `make build` has been run and dist/ has the static site.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$REPO_ROOT/dist"
WORKTREE_DIR="$REPO_ROOT/.gh-pages-worktree"
BRANCH="gh-pages"

if [ ! -d "$DIST_DIR" ]; then
    echo "Error: $DIST_DIR not found. Run 'make build' first." >&2
    exit 1
fi

cd "$REPO_ROOT"
COMMIT_SHA="$(git rev-parse --short HEAD)"

# Clean up any existing worktree (leftovers from a previous failed run)
if [ -d "$WORKTREE_DIR" ]; then
    git worktree remove --force "$WORKTREE_DIR" 2>/dev/null || rm -rf "$WORKTREE_DIR"
fi

# Set up the gh-pages branch as a worktree (create it if it doesn't exist)
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
    git worktree add "$WORKTREE_DIR" "$BRANCH"
elif git ls-remote --heads origin "$BRANCH" | grep -q "$BRANCH"; then
    git worktree add -B "$BRANCH" "$WORKTREE_DIR" "origin/$BRANCH"
else
    git worktree add --orphan -b "$BRANCH" "$WORKTREE_DIR"
fi

# Remove existing files inside the worktree (.git is unaffected since it's a worktree)
find "$WORKTREE_DIR" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

# Copy dist's contents into the worktree
cp -r "$DIST_DIR"/. "$WORKTREE_DIR"/

# Suppress Jekyll processing
touch "$WORKTREE_DIR/.nojekyll"

# Commit & push
cd "$WORKTREE_DIR"
git add -A
if git diff --cached --quiet; then
    echo "No changes to deploy."
else
    git commit -m "Deploy from $COMMIT_SHA"
    git push origin "$BRANCH"
fi

# Clean up
cd "$REPO_ROOT"
git worktree remove --force "$WORKTREE_DIR"

echo "Deployed to $BRANCH branch."
