# Internshala Job Bot — V1

This version is intentionally a **job discovery + scoring tool**.
It does NOT automatically submit applications.

## 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

Windows activation:

```powershell
.venv\Scripts\activate
```

## 2. Run

```bash
python main.py
```

A Chromium window will open.

Log in manually if needed, then return to the terminal and press ENTER.

The authenticated browser state is saved locally in:

```text
auth.json
```

Treat that file as sensitive because it can contain authentication state.

## 3. Output

```text
output/internships.csv
data/internships.db
```

## 4. Current architecture

Internshala
   ↓
Playwright
   ↓
Extract listings
   ↓
Keyword scoring
   ↓
SQLite
   ↓
CSV

## Next milestones

V2:
- robust card parsing
- stipend extraction
- duration extraction
- location extraction
- posted-time extraction
- pagination
- duplicate detection across runs

V3:
- better weighted matching
- required/optional skills
- resume/profile matching
- dashboard

V4:
- open selected applications
- fill only deterministic profile fields
- stop before final submission for review

Do not put passwords, OTPs, or CAPTCHA-solving logic in the project.
