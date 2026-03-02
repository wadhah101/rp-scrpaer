#!/bin/bash

# 1. Get the short Git SHA
export GIT_SHA_SHORT=$(git rev-parse --short HEAD)

# 2. Get the raw branch name reliably
# - GITHUB_HEAD_REF: Populated only on Pull Requests (the source branch)
# - GITHUB_REF_NAME: Populated on Push events (the branch name)
# - Fallback: Local git command when not running in CI
if [[ -n "$GITHUB_HEAD_REF" ]]; then
    export GIT_BRANCH="$GITHUB_HEAD_REF"
elif [[ -n "$GITHUB_REF_NAME" ]]; then
    export GIT_BRANCH="$GITHUB_REF_NAME"
else
    export GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
fi

# 3. Normalize the branch name
# - Translate exact match of "master" to "latest"
# - Convert all characters to lowercase
# - Replace any non-alphanumeric character with a hyphen
export GIT_BRANCH_NORM=$(echo "$GIT_BRANCH" | \
    sed 's/^master$/latest/' | \
    tr '[:upper:]' '[:lower:]' | \
    sed 's/[^a-z0-9]/-/g')
