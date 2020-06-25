#!/usr/bin/env sh
echo "--- verified commits alert ---"
env
echo ""
pwd
echo ""
ls -al
echo ""
python3 -m src.action
echo "--- verified commits alert ---"
