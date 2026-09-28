# Internshala Internship Automation

A Python + Playwright automation tool for discovering, scraping, analyzing, scoring, and ranking Internshala internships against a personal technical profile.

The project is focused on **internship discovery and requirement matching**. It does **not** automatically submit internship applications.

---

## What the Automation Does

The complete workflow is:

```text
Internshala
    ↓
Dedicated Chrome Profile
    ↓
Playwright connects through Chrome CDP
    ↓
Internship result cards are scraped
    ↓
Individual internship detail pages are opened
    ↓
Detailed requirements are extracted
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
Top 10 internships are retained
    ↓
best_finds.html is generated
    ↓
The results page is opened in the browser
````

The important part is that the system does not simply look at internship titles.

It analyzes the **actual requirements of each internship** and compares them with the skills and technical background of the target profile.

---

# Main Features

* Internshala internship discovery
* Playwright-based scraping
* Chrome CDP connection
* Dedicated Chrome profile
* Detailed internship-page extraction
* Requirement-based matching
* Weighted requirement scoring
* Matched / partial / missing requirement analysis
* Requirement depth tracking
* Web-context detection
* SQLite database storage
* CSV export
* Accumulated Best Finds
* URL-based duplicate detection
* Top 10 ranking
* HTML results dashboard
* One-command startup through `start_bot.sh`

---

# 1. Chrome Session

The automation uses a dedicated Chrome profile for Internshala.

Playwright does not create a completely isolated browser session for scraping.

Instead, it attaches to the running Chrome instance through the **Chrome DevTools Protocol (CDP)**.

This is important because the Internshala login/session is maintained by the dedicated Chrome profile.

The normal workflow is:

```text
Chrome
  ↓
Dedicated Internshala profile
  ↓
Logged-in session
  ↓
Chrome remote debugging
  ↓
Playwright attaches to Chrome
```

The bot therefore does not need to store the normal Internshala browser session inside the project itself.

---

# 2. Dedicated Chrome Profile

The Chrome profile used by the automation is:

```text
~/internshala-chrome-profile
```

This profile is separate from the normal Chrome profile.

The first time the automation is used, Internshala should be logged in through this dedicated profile.

After that, future runs can reuse the same browser session as long as the session remains valid.

---

# 3. Internship Scraping

The scraper first reads the internship result cards from the current Internshala results page.

It collects information such as:

* Internship title
* Company
* Stipend
* Duration
* Location
* Work mode
* Skills shown on the card
* Description
* Posted information
* Employment type
* Internship URL

The scraper then opens the individual internship detail page.

The detail page provides more information that is important for matching.

Additional information can include:

* Required skills
* Full description
* Who can apply
* Application deadline
* Number of openings

This gives the scorer much more information than the internship card alone.

---

# 4. Requirement Extraction

The important part of the scraper is extracting the actual requirements from the internship detail page.

For example, an internship might contain requirements such as:

```text
HTML
CSS
JavaScript
React
Python
REST API
SQL
Git
```

The system treats these as individual requirements rather than treating the whole internship as one generic keyword match.

This makes the matching system more useful for technical internships.

---

# 5. Matching System

The scorer evaluates the actual internship requirements against the target technical profile.

The main target is:

```text
Web Development
Frontend Development
Backend Development
Full-Stack Development
Software Engineering
```

The matching system does not give the same importance to every requirement.

Different requirements receive different weights depending on their importance.

The general weighting model is:

| Requirement type                | Typical weight |
| ------------------------------- | -------------: |
| Core technical requirement      |            ~15 |
| Important technical requirement |            ~10 |
| Supporting technical skill      |             ~7 |
| Adjacent skill                  |             ~5 |
| Generic requirement             |             ~3 |

These values are used as relative importance rather than as a simple keyword count.

---

# 6. Why Weighted Matching Is Used

A simple keyword system can produce misleading results.

For example:

```text
Internship A
1 requirement
HTML
```

and:

```text
Internship B
10 requirements
HTML
CSS
JavaScript
React
Python
REST API
SQL
Git
Docker
Next.js
```

A simple "matched percentage" can make a very small requirement set look artificially strong.

The scoring system therefore considers:

* How many requirements were matched
* How important those requirements are
* How many requirements the internship contains
* How deeply the internship requirements match the profile
* The context of the internship

This gives more information than title-based ranking.

---

# 7. Requirement Match

The system tracks several requirement-level values.

### Matched requirements

Requirements that are directly supported by the profile.

Example:

```text
HTML
CSS
JavaScript
React
Python
```

### Partial requirements

Requirements where the profile has related or overlapping experience but not an exact direct match.

### Missing requirements

Requirements for which there is no strong evidence in the current profile.

Example:

```text
PHP
Laravel
Angular
MongoDB
Flutter
```

The final result therefore shows not only a score, but also what is contributing to the score and what is missing.

---

# 8. Requirement Match Percentage

The system calculates a weighted requirement match.

Conceptually:

```text
Matched Requirement Weight
-------------------------------- × 100
Total Requirement Weight
```

This is different from:

```text
Number of matched keywords
-------------------------- × 100
Number of keywords
```

because important technical requirements contribute more to the result.

---

# 9. Requirement Depth

Requirement depth is tracked separately.

This matters because:

```text
5 requirements
```

and:

```text
19 requirements
```

should not be interpreted in exactly the same way.

An internship can technically have a very high percentage match while still having a shallow requirement set.

The output therefore tracks information such as:

* Requirement count
* Requirement match
* Requirement depth
* Requirement context

Example:

```text
89.7%
High depth
5 requirements
```

or:

```text
68.9%
High depth
19 requirements
```

This makes it easier to understand how much evidence is behind a score.

---

# 10. Context Detection

The scorer also considers the general context of the internship.

Examples include:

```text
web
data
AI
mobile
general
```

The current target profile is primarily web/software oriented.

This helps prevent unrelated technical categories from being treated the same way as directly relevant web-development requirements.

---

# 11. Current Technical Profile

The current profile contains experience and skills in areas such as:

## Languages

```text
Python
C++
JavaScript
```

## Frontend / Web

```text
HTML5
CSS3
JavaScript
React
Next.js
```

## Backend / APIs

```text
REST APIs
Next.js Route Handlers
JWT
bcrypt
Authentication
Authorization
API Design
```

## Database

```text
SQLite
SQL
Database Design
Transactions
Indexing
WAL
Migrations
```

## DevOps / Infrastructure

```text
Docker
AWS EC2
GitHub Actions
Linux
Caddy
Git
GitHub
```

## Other Technical Concepts

```text
DSA
OOP
Software Architecture
System Design
Firebase
Recharts
```

AI/ML is not treated as the primary target career category.

---

# 12. Main Project Used as Evidence

## Mithila Medico

The strongest real-world project used as evidence for the profile is **Mithila Medico**.

It is a full-stack pharmacy e-commerce and management platform.

The project contains functionality such as:

* Customer workflows
* Staff workflows
* Admin workflows
* Medicine search
* Batch inventory management
* Stock tracking
* Expiry tracking
* Billing
* Analytics
* Audit logging
* REST-style APIs
* JWT authentication
* Database transactions
* SQLite
* Database indexing
* WAL
* Database migrations
* Docker
* AWS EC2
* GitHub Actions CI/CD

This project provides practical evidence for requirements related to:

```text
Frontend
Backend
Full Stack
APIs
Authentication
Databases
Software Engineering
Deployment
DevOps
System Design
```

---

# 13. Database Storage

Internship data is stored locally in SQLite.

The main database is:

```text
data/internships.db
```

The database stores information about scraped internships, including data such as:

```text
URL
Title
Company
Stipend
Duration
Location
Work mode
Skills
Required skills
Description
Detailed description
Who can apply
Apply by
Openings
Posted information
Employment type
Score
Requirement match
Matched requirements
Partial requirements
Missing requirements
Matched weight
Total requirement weight
Profile relevance
Matched keywords
```

SQLite gives the automation persistent local storage between scraping cycles.

---

# 14. CSV Output

The current scraping cycle is also exported to:

```text
output/internships.csv
```

This provides a simple tabular representation of the current results.

The CSV is useful for inspecting the raw/processed internship dataset outside the HTML interface.

---

# 15. Accumulated Best Finds

One of the important features of the automation is that the Top 10 list is not limited to a single scraping cycle.

The system maintains an accumulated pool.

Example:

```text
Cycle 1
50 internships
        ↓
Current results

Cycle 2
50 more internships
        ↓
Merge with previous results

Cycle 3
Another 50 internships
        ↓
Merge again
```

The system then:

```text
Merge
  ↓
Normalize URLs
  ↓
Remove duplicates
  ↓
Re-score
  ↓
Sort by score / requirement match
  ↓
Keep Top 10
```

This means an internship discovered during an earlier run can remain in the Best Finds list even when it is no longer present in the current scraping cycle.

---

# 16. Duplicate Detection

Duplicate internships should not occupy multiple positions in the Best Finds list.

The system primarily uses the internship URL for deduplication.

Tracking parameters can be removed before comparison so that different tracking versions of the same internship are treated as the same listing.

There is also a fallback based on internship title + company when necessary.

---

# 17. Best Finds Output

The final accumulated result is written to:

```text
output/best_finds.csv
```

and:

```text
output/best_finds.html
```

The HTML file is the main visual interface for reviewing the results.

---

# 18. Best Finds Dashboard

The generated HTML page contains information such as:

* Rank
* Score
* Internship
* Company
* Requirement match
* Requirement depth
* Requirement context
* Requirement count
* Matched skills
* Missing skills
* Stipend
* Duration
* Open button

Example layout:

![Best Finds preview](docs/best-finds-preview.png)

The dashboard is generated locally after each automation cycle.

---

# 19. Example Result

A result can look conceptually like:

```text
#1
Score: 82

Front End Development
Company: Example Company

Requirement Match: 89.7%
Depth: High
Context: web
Requirements: 5

Matched:
CSS
HTML
JavaScript
React

Missing:
None

Stipend:
₹8,000 - ₹20,000 / month

Duration:
2 Months
```

Another internship may have:

```text
Score: 81

Full Stack Development

Requirement Match: 68.9%
Depth: High
Context: web
Requirements: 19

Matched:
CSS
Docker
FastAPI
Git
GitHub
HTML
JavaScript
Python
React
REST API
SQL

Missing:
Django
Flask
MySQL
PostgreSQL
Vue.js
UI/UX Design
etc.
```

The purpose of the interface is to make the score explainable rather than presenting a score with no context.

---

# 20. Project Structure

```text
internshala-internship-automation/
│
├── main.py
├── scraper.py
├── scorer.py
├── database.py
├── update_best_finds.py
├── config.py
│
├── start_bot.sh
├── run_bot.sh
│
├── requirements.txt
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
```

---

# 21. What Each Python File Does

## `main.py`

Controls the main scraping workflow.

It:

1. Connects to the running Chrome instance
2. Finds the Internshala results page
3. Runs the scraper
4. Sends internships to the scorer
5. Saves the results
6. Exports the CSV
7. Displays summary information

---

## `scraper.py`

Responsible for extracting internship information from Internshala.

It handles:

* Result cards
* Internship detail pages
* Required skills
* Descriptions
* Eligibility
* Application deadlines
* Openings
* Other internship metadata

---

## `scorer.py`

Responsible for:

* Requirement normalization
* Requirement matching
* Partial matching
* Missing requirements
* Requirement weights
* Requirement context
* Requirement depth
* Final scoring

This is the main matching engine.

---

## `database.py`

Responsible for:

* SQLite database creation
* Database migrations
* Internship storage
* CSV export
* Persistent local data

---

## `update_best_finds.py`

Responsible for the accumulated Best Finds system.

It:

1. Reads the latest results
2. Re-applies the current scoring system
3. Reads previous Best Finds
4. Merges old and new results
5. Removes duplicates
6. Sorts the combined pool
7. Keeps the Top 10
8. Writes `best_finds.csv`
9. Updates the SQLite Best Finds table
10. Generates `best_finds.html`
11. Opens the HTML results page

---

## `config.py`

Contains configuration values used by the scraper and scoring workflow.

This includes things such as:

* Internshala URL
* Search configuration
* Profile keywords
* Negative keywords
* Database path
* CSV path
* Other scraper settings

---

## `start_bot.sh`

This is the main launcher.

It is designed to handle the complete local workflow instead of requiring several commands manually.

The script can:

```text
Start / connect to Chrome
        ↓
Prepare the browser session
        ↓
Run the scraper
        ↓
Run the scoring system
        ↓
Update Best Finds
        ↓
Generate HTML
        ↓
Open the results
```

---

# 22. How to Run the Automation

The main startup command is:

```bash
cd /path/to/internshala-internship-automation && ./start_bot.sh
```

Replace:

```text
/path/to/internshala-internship-automation
```

with the actual location of the repository on your laptop.

For example:

```bash
cd ~/internshala-internship-automation && ./start_bot.sh
```

Or:

```bash
cd /home/username/projects/internshala-internship-automation && ./start_bot.sh
```

The important point is that the command can be copied directly into the terminal after replacing the repository path.

---

# 23. First-Time Setup

Clone the repository:

```bash
git clone https://github.com/priyanshu-kumar952/internshala-internship-automation.git
```

Enter the project:

```bash
cd internshala-internship-automation
```

Create the Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the required Playwright browser:

```bash
python -m playwright install chromium
```

Make the launcher executable:

```bash
chmod +x start_bot.sh
```

After setup, the normal workflow is simply:

```bash
cd /path/to/internshala-internship-automation && ./start_bot.sh
```

---

# 24. Normal Run Workflow

Every time the automation is run:

```text
1. Start the launcher
        ↓
2. Chrome session is prepared
        ↓
3. Playwright connects through CDP
        ↓
4. Internshala results are located
        ↓
5. Internship cards are scraped
        ↓
6. Detail pages are inspected
        ↓
7. Requirements are extracted
        ↓
8. Requirements are matched against the profile
        ↓
9. Scores are calculated
        ↓
10. Current results are saved
        ↓
11. Previous Best Finds are merged
        ↓
12. Duplicate internships are removed
        ↓
13. Top 10 are retained
        ↓
14. HTML dashboard is generated
        ↓
15. Best Finds page is opened
```

---

# 25. Resetting Local Results

The normal run preserves the accumulated Best Finds history.

A reset can be used when starting from a clean local state.

```bash
./start_bot.sh --reset
```

The reset is intended for local cleanup/testing and should not be used casually if the accumulated Best Finds history is important.

---

# 26. Output Files

## Current scraping cycle

```text
output/internships.csv
```

Contains the internships discovered during the current scrape.

## Persistent database

```text
data/internships.db
```

Contains the local SQLite data.

## Accumulated Best Finds

```text
output/best_finds.csv
```

Contains the current accumulated Top 10.

## HTML dashboard

```text
output/best_finds.html
```

Contains the visual Best Finds interface.

---

# 27. Privacy and Sensitive Data

The project uses a dedicated browser profile for the Internshala session.

The browser session itself should not be committed to Git.

Sensitive information such as:

```text
Passwords
OTP codes
Authentication tokens
Browser session data
Cookies
Personal credentials
```

should never be committed to the repository.

The repository `.gitignore` is used to keep local/generated files outside Git where appropriate.

---

# 28. Application Submission

This project does **not** automatically submit internship applications.

The automation stops at:

```text
Discovery
        ↓
Scraping
        ↓
Analysis
        ↓
Scoring
        ↓
Ranking
        ↓
Review
```

The final application decision remains manual.

There is intentionally no password automation, OTP automation, or CAPTCHA-solving logic in the project.

---

# 29. GitHub Repository

Repository:

[https://github.com/priyanshu-kumar952/internshala-internship-automation](https://github.com/priyanshu-kumar952/internshala-internship-automation)

The repository contains the source code required to reproduce the automation.

Generated local files such as databases, scraped output, browser sessions, and other local state should remain outside the repository.

---

# 30. Current Architecture

```text
                     ┌────────────────────┐
                     │    Internshala     │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │ Dedicated Chrome   │
                     │     Profile        │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │   Chrome CDP       │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │     Playwright     │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │      Scraper       │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │   Requirement     │
                     │    Extraction      │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │      Scorer        │
                     └─────────┬──────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │        SQLite + CSV          │
                └──────────────┬───────────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │  Best Finds Merge  │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │ Deduplicate + Top 10│
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │ best_finds.html    │
                     └────────────────────┘
```

---

# 31. Design Goals

The project is designed around several principles:

### Real requirements over internship titles

The title alone is not considered sufficient evidence for matching.

### Weighted matching over raw keyword counts

More important technical requirements contribute more to the score.

### Explainable results

The dashboard shows what was matched and what is missing.

### Persistent Best Finds

Good internships discovered in earlier cycles can remain in the Top 10.

### Local-first operation

Scraped data and generated output remain local.

### Manual application control

The automation discovers and analyzes opportunities but does not submit applications automatically.

---

# 32. Current Scope

The current system focuses on:

```text
Internship Discovery
        +
Requirement Extraction
        +
Profile Matching
        +
Weighted Scoring
        +
Persistent Best Finds
        +
Top 10 Visualization
```

The main goal is to make internship discovery more efficient by reducing the amount of manual searching and manually comparing technical requirements.

---

# 33. Future Improvements

Possible future development areas include:

* More robust pagination
* More advanced requirement normalization
* Improved synonym handling
* Better partial-match detection
* More detailed profile evidence
* Better handling of optional vs required skills
* Improved duplicate detection
* More detailed analytics
* Better historical tracking
* Improved result filtering
* More detailed dashboards

Automatic application submission is deliberately not the current objective.

---

# 34. Project Philosophy

The goal of this project is not to blindly automate applications.

The goal is:

```text
Find more opportunities
        ↓
Understand their requirements
        ↓
Compare them with the actual profile
        ↓
Reduce irrelevant listings
        ↓
Surface the most relevant opportunities
        ↓
Let the user make the final decision
```

The automation handles the repetitive discovery and comparison work while keeping the final application decision manual.

---

## License

This project is currently maintained as a personal automation project.

---

## Repository

GitHub:

[https://github.com/priyanshu-kumar952/internshala-internship-automation](https://github.com/priyanshu-kumar952/internshala-internship-automation)

````

After pasting that into GitHub's `README.md` editor, make sure the screenshot is committed at:

```text
docs/best-finds-preview.png
````

so this line displays correctly:

```markdown
![Best Finds preview](docs/best-finds-preview.png)
```

And the **actual one-line command you'll document/use to start it** remains:

```bash
cd /path/to/internshala-internship-automation && ./start_bot.sh
```
