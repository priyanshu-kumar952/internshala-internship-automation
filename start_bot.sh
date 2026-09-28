#!/usr/bin/env bash

set -e

PROJECT_DIR="$HOME/.Disk_C/expetriment"
CHROME_PROFILE="$HOME/internshala-chrome-profile"
DEBUG_PORT="9222"
RESULTS_URL="https://internshala.com/internships/work-from-home-internships/"

cd "$PROJECT_DIR"

echo
echo "=============================================="
echo "       INTERNSHALA AUTOMATION BOT"
echo "=============================================="
echo


# ============================================================
# OPTIONAL CLEAN RESET
# ============================================================

if [[ "${1:-}" == "--reset" ]]; then

    echo "[RESET] Removing previous database..."

    rm -f \
        data/internships.db \
        output/internships.csv \
        output/best_finds.csv \
        output/best_finds.html

    echo "[RESET] Clean slate created."
    echo

fi


# ============================================================
# PYTHON ENVIRONMENT
# ============================================================

echo "[1/6] Activating Python environment..."

source .venv/bin/activate

export PYTHONUNBUFFERED=1

echo "Python:"
which python

echo


# ============================================================
# CHROME
# ============================================================

echo "[2/6] Checking Chrome..."

if curl -fsS \
    "http://127.0.0.1:${DEBUG_PORT}/json/version" \
    >/dev/null 2>&1
then

    echo "Chrome debugging is already running."

else

    if command -v google-chrome >/dev/null 2>&1; then
        CHROME_BIN="google-chrome"
    elif command -v google-chrome-stable >/dev/null 2>&1; then
        CHROME_BIN="google-chrome-stable"
    else
        echo
        echo "Google Chrome was not found."
        exit 1
    fi

    echo "Starting Chrome..."

    "$CHROME_BIN" \
        --remote-debugging-port="${DEBUG_PORT}" \
        --remote-debugging-address=127.0.0.1 \
        --user-data-dir="${CHROME_PROFILE}" \
        --new-window \
        --no-first-run \
        --no-default-browser-check \
        "${RESULTS_URL}" \
        >/tmp/internshala-chrome.log 2>&1 &

    CHROME_PID=$!

    echo "Chrome PID: ${CHROME_PID}"

    echo "Waiting for remote debugging..."

    READY=0

    for i in $(seq 1 60); do

        if curl -fsS \
            "http://127.0.0.1:${DEBUG_PORT}/json/version" \
            >/dev/null 2>&1
        then
            READY=1
            break
        fi

        sleep 1

    done

    if [[ "$READY" != "1" ]]; then

        echo
        echo "Chrome did not start correctly."
        echo
        echo "Chrome log:"
        tail -30 /tmp/internshala-chrome.log || true
        exit 1

    fi

    echo "Chrome is ready."

fi

echo


# ============================================================
# WAIT FOR INTERN SHALA RESULTS
# ============================================================

echo "[3/6] Waiting for Internshala..."

python - <<'PY'
import time
import config
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.connect_over_cdp(
        "http://127.0.0.1:9222"
    )

    context = browser.contexts[0]

    page = None

    # Prefer an existing results page.
    for candidate in context.pages:

        url = candidate.url.lower()

        if (
            "internshala.com/internships/"
            in url
            and "/internship/detail/"
            not in url
        ):
            page = candidate
            break

    # Otherwise open one.
    if page is None:

        page = context.new_page()

        page.goto(
            config.BASE_URL,
            wait_until="domcontentloaded",
            timeout=30000,
        )

    print(
        "\nInternshala page:",
        page.url,
    )

    print(
        "\nIf Internshala asks you to log in,"
    )
    print(
        "log in manually in the Chrome window."
    )
    print(
        "The script will wait for the internship results."
    )

    deadline = time.time() + 300

    while time.time() < deadline:

        try:

            count = page.locator(
                "div.individual_internship"
            ).count()

            if count > 0:

                print(
                    f"\nInternshala results ready: "
                    f"{count} cards."
                )

                break

        except Exception:
            pass

        print(
            "Waiting for results...",
            flush=True,
        )

        time.sleep(3)

    else:

        raise RuntimeError(
            "Timed out waiting for Internshala results."
        )

PY

echo


# ============================================================
# SCRAPE
# ============================================================

echo "[4/6] Scraping internships..."

# main.py asks for one ENTER.
# Feed it automatically because the preflight above
# already confirmed that results are available.

printf '\n' | python main.py

echo


# ============================================================
# BEST FINDS
# ============================================================

echo "[5/6] Updating best finds..."

python update_best_finds.py

echo


# ============================================================
# FINISHED
# ============================================================

echo "[6/6] Finished."

echo
echo "=============================================="
echo "                 COMPLETE"
echo "=============================================="
echo
echo "Database:"
echo "  ${PROJECT_DIR}/data/internships.db"
echo
echo "Best finds CSV:"
echo "  ${PROJECT_DIR}/output/best_finds.csv"
echo
echo "Best finds viewer:"
echo "  ${PROJECT_DIR}/output/best_finds.html"
echo
echo "Chrome stays open."
echo
