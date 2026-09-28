#!/usr/bin/env bash

set -e

PROJECT_DIR="$HOME/expetriment"

cd "$PROJECT_DIR"

echo "=========================================="
echo "      INTERN SHALA JOB BOT"
echo "=========================================="
echo

echo "[1/4] Activating virtual environment..."
source .venv/bin/activate

echo "[2/4] Checking Chrome..."

if ! curl -fsS \
    http://127.0.0.1:9222/json/version \
    >/dev/null 2>&1
then
    echo
    echo "Chrome remote debugging is NOT running."
    echo
    echo 'Start Chrome with:'
    echo
    echo 'google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/internshala-chrome-profile"'
    echo
    exit 1
fi

echo "Chrome connection OK."
echo

echo "[3/4] Running internship scraper..."
echo

python main.py

echo
echo "[4/4] Merging previous best finds with this cycle..."
echo

python update_best_finds.py

echo
echo "=========================================="
echo "DONE"
echo "=========================================="
echo
echo "Database:"
echo "  $PROJECT_DIR/data/internships.db"
echo
echo "Top 10 CSV:"
echo "  $PROJECT_DIR/output/best_finds.csv"
echo
echo "Visual viewer:"
echo "  $PROJECT_DIR/output/best_finds.html"
echo
