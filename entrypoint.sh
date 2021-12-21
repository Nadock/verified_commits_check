#!/usr/bin/env sh
#
# This entrypoint script is used to work around the way GitHub Actions runs Docker
# based actions. Specifically, they set a custom WORKDIR which overrides the
# container's configured WORKDIR.
#
# e: Exit immediately on fail
# u: Treat unset variables as errors
# x: Print each instruction to stderr before executing
set -eux

cd /opt/action
python3 -m src.action
