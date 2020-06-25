#!/usr/bin/env sh
set +x
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
