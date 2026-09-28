# Personal preferences. Edit these as you learn what you want.
BASE_URL = "https://internshala.com/internships/matching-preferences/stipend-10000"

MIN_STIPEND = 10000
MAX_DURATION_MONTHS = 6
REMOTE_ONLY = True

KEYWORDS = {
    "python": 10,
    "ai": 10,
    "machine learning": 10,
    "ml": 8,
    "django": 6,
    "fastapi": 6,
    "flask": 5,
    "data science": 8,
    "web development": 6,
    "javascript": 4,
    "react": 5,
    "next.js": 5,
    "sql": 3,
}

NEGATIVE_KEYWORDS = {
    "sales": 10,
    "telecalling": 10,
    "business development": 8,
    "content writing": 6,
}

DB_PATH = "data/internships.db"
CSV_PATH = "output/internships.csv"
AUTH_FILE = "auth.json"
