#!/bin/env bash

set -xe

git fetch origin main
git checkout main
git pull --rebase origin main
if ! git checkout -b typedpath; then
    git branch -D typedpath
    git checkout -b typedpath
fi
poetry run python -m requirements
if [[ $(git status --porcelain) ]]; then
    poetry update
    git \
        -c "user.name=Update requirements bot" \
        -c "user.email=none" \
        commit \
        -am "Update requirements."
    git push origin +typedpath
    gh pr create \
       --title "Update requirements" \
       --body "Automatic update of requirements." \
       --reviewer jesnie \
       || true
    gh pr merge -s --auto
fi
