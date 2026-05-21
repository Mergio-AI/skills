#!/bin/bash
# Cron job (04:00 daily): pull latest hermes-skills from main
# Run on all non-master agents after the PR merge window (03:30)

set -e

REPO_DIR="/opt/data/hermes-skills"

cd "$REPO_DIR"
git fetch origin main
git checkout main
git reset --hard origin/main

echo "Skills synced to $(git rev-parse --short HEAD)"
