#!/usr/bin/env bash
# multilingual-reader を GitHub Pages (gh-pages ブランチ) へデプロイする。
# 実行は `bash deploy.sh` 経由。chmod +x は不要。
# 前提: `make build` 済みで dist/ に静的サイトが揃っていること。

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$REPO_ROOT/dist"
WORKTREE_DIR="$REPO_ROOT/.gh-pages-worktree"
BRANCH="gh-pages"

if [ ! -d "$DIST_DIR" ]; then
    echo "Error: $DIST_DIR not found. Run 'make build' first." >&2
    exit 1
fi

cd "$REPO_ROOT"
COMMIT_SHA="$(git rev-parse --short HEAD)"

# 既存の worktree を掃除（前回失敗時の残骸対策）
if [ -d "$WORKTREE_DIR" ]; then
    git worktree remove --force "$WORKTREE_DIR" 2>/dev/null || rm -rf "$WORKTREE_DIR"
fi

# gh-pages ブランチを worktree として用意（未存在なら新規作成）
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
    git worktree add "$WORKTREE_DIR" "$BRANCH"
elif git ls-remote --heads origin "$BRANCH" | grep -q "$BRANCH"; then
    git worktree add -B "$BRANCH" "$WORKTREE_DIR" "origin/$BRANCH"
else
    git worktree add --orphan -b "$BRANCH" "$WORKTREE_DIR"
fi

# worktree 内の既存ファイルを削除（.git は worktree なので影響なし）
find "$WORKTREE_DIR" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

# dist の中身を worktree へコピー
cp -r "$DIST_DIR"/. "$WORKTREE_DIR"/

# Jekyll 処理を抑止
touch "$WORKTREE_DIR/.nojekyll"

# コミット & push
cd "$WORKTREE_DIR"
git add -A
if git diff --cached --quiet; then
    echo "No changes to deploy."
else
    git commit -m "Deploy from $COMMIT_SHA"
    git push origin "$BRANCH"
fi

# 後片付け
cd "$REPO_ROOT"
git worktree remove --force "$WORKTREE_DIR"

echo "Deployed to $BRANCH branch."
