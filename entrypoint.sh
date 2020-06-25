#!/usr/bin/env sh
# e: Exit immediately on fail
# E: Inherit ERR trap so it works correctly if something fails and we exit because of -e
# u: Treat unset variables as errors
# x: Print each instruction to stderr before executing
# o pipefail: Exit status of pipe is non-zero if any step in pipe fails
set -Eeuxo pipefail

echo "--- verified commits alert ---"
env
echo ""
pwd
cd /opt/action
echo ""
ls -al
echo ""
python3 -m src.action
echo "--- verified commits alert ---"
