#!/usr/bin/env sh
# e: Exit immediately on fail
# u: Treat unset variables as errors
# x: Print each instruction to stderr before executing
set -eux

cd /opt/action
python3 -m src.action
