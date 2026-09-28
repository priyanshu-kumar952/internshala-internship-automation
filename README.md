Internshala Internship Automation

A Python + Playwright automation tool for discovering, scraping, analyzing, scoring, and ranking Internshala internships against a personal technical profile.

The project is intentionally focused on internship discovery and matching. It does not automatically submit internship applications.

What the automation does

The complete workflow is:

Internshala
    ↓
Dedicated Chrome profile
    ↓
Playwright connects through Chrome CDP
    ↓
Internship result cards are scraped
    ↓
Detail pages are opened and requirements are extracted
    ↓
Requirements are matched against the technical profile
    ↓
Weighted score is calculated
    ↓
Results are stored in SQLite + CSV
    ↓
Previous best finds are merged with the new cycle
    ↓
Duplicates are removed
    ↓
Top 10 are retained
    ↓
best_finds.html is generated and opened

1. Chrome session

The bot uses a dedicated Chrome profile for Internshala. Playwright does not create an isolated login session for scraping; it attaches to the running Chrome instance through the Chrome DevTools Protocol (CDP).

This keeps the Internshala login/session in the dedicated browser profile rather than inside the project files.

2. Internship scraping

The scraper reads internship cards from the current Internshala results page and then opens internship detail pages to collect more complete information.

The data collected includes fields such as:

Internship title

Company

Stipend

Duration

Location

Work mode

Skills shown on the listing

Required skills from the detail page

Description

Who can apply / eligibility information

Application deadline

Number of openings

Posted information

Employment type

Internship URL

3. Requirement extraction

The detail page is important because the scoring system does not rely only on the internship title.

The bot extracts the actual required skills and uses those requirements as the main basis for matching.

4. Profile matching

The current profile is primarily focused on:

Web Development

Frontend Development

Backend Development

Full-Stack Development

Software Engineering

Relevant technical skills include:

Languages

Python

C++

JavaScript

Web

HTML5

CSS3

React

Next.js

REST APIs

Next.js Route Handlers

Backend / Database

JWT

bcrypt

SQLite

SQL

Database design

DevOps / Infrastructure

Docker

AWS EC2

GitHub Actions

Linux

Caddy

Git / GitHub

Other engineering concepts

Firebase

Recharts

DSA

OOP

Authentication

Authorization

API design

Software architecture

System design

AI/ML is not treated as the primary job target.

Scoring system

The scorer is designed around requirements, not just job titles.

Each requirement receives a different importance weight. A technically important requirement contributes more to the score than a generic or weakly related requirement.

The matching system tracks:

Matched requirements

Partial requirements

Missing requirements

Matched requirement weight

Total requirement weight

Requirement match percentage

Requirement context

Requirement depth

Requirement count

Overall profile relevance

This matters because a listing with only one easy requirement can otherwise appear artificially strong. Requirement depth is therefore kept alongside coverage.

Example

A listing requiring:

HTML
CSS
JavaScript
React

can produce a strong match because several core web requirements are covered.

A listing requiring:

HTML

may show very high requirement coverage, but it has much lower requirement depth because the listing itself is technically shallow.

Best Finds system

The bot does not throw away previous results after every scrape cycle.

Each cycle produces a new set of internships. Those results are merged with the existing best-finds pool.

The system then:

Normalizes internship URLs.

Removes duplicate internships.

Merges current results with previously retained results.

Recalculates the current ranking.

Retains the top 10 unique internships.

Saves those results to CSV and SQLite.

Regenerates the HTML results page.

This means the best_finds list acts as an accumulated pool across scraping cycles rather than representing only the latest page scrape.

Example result page

The generated best_finds.html provides a visual summary of the current Top 10.



The page includes information such as:

Rank

Score

Internship title

Company

Requirement match

Requirement depth

Requirement context

Number of requirements

Matched skills

Missing skills

Stipend

Duration

Link to the internship

The screenshot above is an example of the current output format.

Output files

Raw scraped results

output/internships.csv

Contains the internship records collected during the scraping cycle.

SQLite database

data/internships.db

Stores the scraped internship data and the best-finds data locally.

Accumulated Top 10

output/best_finds.csv

Contains the currently retained Top 10 unique internships.

Human-readable results

output/best_finds.html

A browser-friendly page containing the ranked results.

Project structure

internshala-internship-automation/
│
├── main.py                 # Main scraper/scoring workflow
├── scraper.py              # Internshala page + detail extraction
├── scorer.py               # Requirement matching and scoring
├── database.py             # SQLite storage + CSV export
├── update_best_finds.py    # Merge, deduplicate and build Top 10
├── config.py               # Runtime/search configuration
│
├── start_bot.sh            # Main one-command launcher
├── run_bot.sh              # Supporting runner
│
├── requirements.txt        # Python dependencies
├── README.md
├── .gitignore
│
├── data/
│   └── internships.db
│
└── output/
    ├── internships.csv
    ├── best_finds.csv
    └── best_finds.html

Run the automation

The project is already configured to run locally through start_bot.sh.

Use this command from a terminal:

cd /path/to/internshala-internship-automation && ./start_bot.sh

Replace /path/to/internshala-internship-automation with the actual path of the repository on your laptop.

This is the single command used to start the automation.

The launcher handles the full workflow rather than requiring the individual Python scripts to be run manually.

Reset the local result history

The launcher also supports a reset mode for starting with a clean local result database/output set:

cd /path/to/internshala-internship-automation && ./start_bot.sh --reset

Use this only when the accumulated local results need to be cleared.

First-time setup

Clone the repository:

git clone https://github.com/priyanshu-kumar952/internshala-internship-automation.git
cd internshala-internship-automation

Create the Python environment and install dependencies:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium

The bot also requires Google Chrome/Chromium with remote-debugging support.

Dedicated Chrome profile

The automation uses a separate Chrome profile for the Internshala session.

~/internshala-chrome-profile

The profile keeps the browser session separate from the user's normal Chrome profile.

For the first run, log in to Internshala in that dedicated profile. Later runs can reuse the existing authenticated session as long as it remains valid.

Why CDP is used

Google authentication may restrict automated browser contexts. The project therefore uses a normal Chrome session and connects Playwright to that running browser through CDP.

Conceptually:

Normal Chrome session
        │
        │ CDP :9222
        ▼
Playwright
        ▼
Internshala scraper

The project does not attempt to bypass Google security checks or CAPTCHA systems.

Current application scope

The automation is intentionally limited to:

Internship discovery

Data extraction

Requirement analysis

Technical profile matching

Weighted scoring

Deduplication

Ranking

Local result storage

Human-readable result generation

It does not automatically submit applications.

The final application decision remains manual.

Security and sensitive data

Do not commit or place the following in the repository:

Passwords

OTPs

CAPTCHA-solving code

Authentication tokens

Browser session secrets

Personal generated databases or scraped result files

Local session/data/output files are excluded through .gitignore.

Repository

GitHub:

https://github.com/priyanshu-kumar952/internshala-internship-automation

Current development direction

The project can continue evolving around:

More accurate requirement extraction

Better partial-match detection

More robust duplicate handling

Better pagination coverage

Improved scoring calibration

Better result presentation

Additional internship-source support

The central goal remains the same: find technically relevant internships efficiently and make the matching process transparent enough to inspect before applying.
