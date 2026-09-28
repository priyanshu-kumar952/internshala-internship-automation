# Internshala Internship Automation

A Python + Playwright tool that scrapes Internshala internships, extracts their real requirements, scores them against your technical profile, and keeps a ranked **Top 10** list.

> It does **not** submit applications. Discovery, analysis, and ranking are automated. The final decision stays with you.

![Best Finds preview](docs/best-finds-preview.png)

## Features

- Scrapes result cards **and** each internship's detail page (skills, description, eligibility, deadline, openings)
- Weighted requirement matching, so core skills count more than generic ones
- Matched / partial / missing skills shown for every result, so scores are explainable
- Requirement depth and context detection (web, data, AI, mobile)
- Best Finds accumulate across runs, with URL-based duplicate removal
- Local storage in SQLite, with CSV and HTML dashboard output
- One-command start with `start_bot.sh`

## How It Works

```text
Dedicated Chrome profile (logged in to Internshala)
  → Playwright attaches via Chrome CDP
  → Scrape cards + detail pages
  → Extract requirements
  → Weighted scoring against your profile
  → Save to SQLite + CSV
  → Merge with previous Best Finds, dedupe, keep Top 10
  → Generate and open best_finds.html
```

## Scoring

Each requirement is weighted by importance, and the match is `matched weight / total weight × 100`.

| Requirement type | Weight |
| --- | ---: |
| Core technical | ~15 |
| Important technical | ~10 |
| Supporting skill | ~7 |
| Adjacent skill | ~5 |
| Generic | ~3 |

Requirement count and depth are shown alongside the score, so a 90% match on 2 requirements isn't mistaken for a 90% match on 20.

## Setup

```bash
git clone https://github.com/priyanshu-kumar952/internshala-internship-automation.git
cd internshala-internship-automation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
chmod +x start_bot.sh
```

On first run, log in to Internshala in the dedicated Chrome profile (`~/internshala-chrome-profile`). The session is reused afterwards.

## Usage

```bash
./start_bot.sh            # run the full workflow
./start_bot.sh --reset    # clear local results and Best Finds history
```

## Project Structure

```text
├── main.py               # scraping workflow
├── scraper.py            # card + detail page extraction
├── scorer.py             # requirement matching and scoring
├── database.py           # SQLite, migrations, CSV export
├── update_best_finds.py  # merge, dedupe, Top 10, HTML
├── config.py             # URLs, profile keywords, paths
├── start_bot.sh          # main launcher
├── data/internships.db
└── output/
    ├── internships.csv   # current cycle
    ├── best_finds.csv    # accumulated Top 10
    └── best_finds.html   # results dashboard
```

## Privacy

Never commit passwords, cookies, tokens, or browser session data. `.gitignore` excludes the database, output files, and local state. There is no password, OTP, or CAPTCHA automation.

## Roadmap

- More robust pagination
- Better synonym and partial-match handling
- Required vs. optional skill detection
- Historical tracking and analytics

##command for me, "cd "$HOME/.Disk_C/expetriment" && ./start_bot.sh"

## License

Personal project. Add a `LICENSE` file (e.g. MIT) if you want others to reuse it.
