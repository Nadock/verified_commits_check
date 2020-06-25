#!/usr/bin/env sh
# e: Exit immediately on fail
# u: Treat unset variables as errors
# x: Print each instruction to stderr before executing
# o pipefail: Exit status of pipe is non-zero if any step in pipe fails
set -euxo pipefail

echo "--- verified commits alert ---"

env
pwd
cd /opt/action
echo ""
ls -al
echo ""
cat $GITHUB_EVENT_PATH
echo ""
python3 -m src.action
echo "--- verified commits alert ---"
