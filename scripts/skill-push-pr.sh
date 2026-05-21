#!/bin/bash
# Cron job (03:00 daily): push hermes-skills changes as a PR
# Usage: run from within the hermes-skills git repo
#
# Behavior:
#   - If no changes → silent exit (no empty PR)
#   - If changes → create branch, commit, push, open PR to main

set -e

REPO_DIR="/opt/data/hermes-skills"
BRANCH="sync/$(date +%Y%m%d-%H%M)"
PR_TITLE="sync: skills update $(date +%Y-%m-%d)"

cd "$REPO_DIR"
git fetch origin main 2>/dev/null
git checkout main 2>/dev/null
git reset --hard origin/main 2>/dev/null

# Check for changes
if git diff --quiet && git diff --cached --quiet; then
    # Check for untracked skill files
    if [ -z "$(git ls-files --others --exclude-standard skills/)" ]; then
        echo "No changes to sync."
        exit 0
    fi
fi

git checkout -b "$BRANCH" 2>/dev/null
git add -A
git commit -m "$PR_TITLE" 2>/dev/null || { echo "Nothing to commit."; exit 0; }
git push -u origin "$BRANCH"

# Open PR via gh CLI
gh pr create \
    --base main \
    --head "$BRANCH" \
    --title "$PR_TITLE" \
    --body "自动同步 Skills 变更。请 review 后合并。" \
    --label "sync,automated"

echo "PR created: $PR_TITLE"
