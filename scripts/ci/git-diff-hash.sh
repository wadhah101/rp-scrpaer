#!/bin/bash

export GIT_DIFF_HASH=$(git diff HEAD | sha1sum | awk '{print $1}')


