#!/bin/sh
set -e
cd "$(dirname "$0")/.."
python3 src/main.py --vfs default.vfs --script startup.txt
