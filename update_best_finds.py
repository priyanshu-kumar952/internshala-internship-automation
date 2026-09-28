import csv
import html
import sqlite3
import subprocess
import shutil
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from scorer import score_jobs


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = BASE_DIR / "data" / "internships.db"

CURRENT_CSV = OUTPUT_DIR / "internships.csv"
BEST_CSV = OUTPUT_DIR / "best_finds.csv"
BEST_HTML = OUTPUT_DIR / "best_finds.html"

TOP_N = 10


def read_csv(path):
    if not path.exists():
        return []

    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as f:
        return list(csv.DictReader(f))


def normalize_url(url):
    if not url:
        return ""

    try:
        parts = urlsplit(url.strip())

        return urlunsplit((
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path.rstrip("/"),
            "",
            "",
        ))
    except Exception:
        return url.strip().lower()


def identity(row):
    url = normalize_url(row.get("url", ""))

    if url:
        return f"url:{url}"

    title = row.get(
        "title",
        "",
    ).strip().lower()

    company = row.get(
        "company",
        "",
    ).strip().lower()

    return f"text:{title}|{company}"


def numeric_score(row):
    try:
        return float(
            row.get("score", 0) or 0
        )
    except (TypeError, ValueError):
        return 0


def numeric_match(row):
    try:
        return float(
            row.get(
                "requirement_match",
                0,
            ) or 0
        )
    except (TypeError, ValueError):
        return 0


# ============================================================
# CURRENT CYCLE
# ============================================================

current = read_csv(CURRENT_CSV)

# Re-run the current V4.1 scorer so all derived fields are
# definitely present.
current = score_jobs(current)

# Normalize URLs.
for row in current:
    row["url"] = normalize_url(
        row.get("url", "")
    )

# ============================================================
# PREVIOUS BEST
# ============================================================

previous = read_csv(BEST_CSV)

for row in previous:
    row["url"] = normalize_url(
        row.get("url", "")
    )

print(
    f"Previous best finds: {len(previous)}"
)

print(
    f"Current cycle results: {len(current)}"
)

# ============================================================
# MERGE
# ============================================================

merged = {}

for row in previous:
    merged[identity(row)] = row

for row in current:
    # Current cycle replaces an older duplicate.
    merged[identity(row)] = row

unique_rows = list(
    merged.values()
)

unique_rows.sort(
    key=lambda row: (
        -numeric_score(row),
        -numeric_match(row),
        row.get(
            "title",
            "",
        ).lower(),
    )
)

best_rows = unique_rows[:TOP_N]

print(
    f"Unique after merge: {len(unique_rows)}"
)

print(
    f"Keeping top {len(best_rows)}"
)


# ============================================================
# CSV
# ============================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

csv_fields = [
    "rank",
    "score",
    "requirement_match",
    "requirement_context",
    "requirement_depth",
    "requirement_count",
    "title",
    "company",
    "matched_requirements",
    "partial_requirements",
    "missing_requirements",
    "profile_relevance",
    "stipend",
    "duration",
    "work_mode",
    "employment_type",
    "posted",
    "apply_by",
    "openings",
    "url",
]

with BEST_CSV.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=csv_fields,
        extrasaction="ignore",
    )

    writer.writeheader()

    for rank, row in enumerate(
        best_rows,
        start=1,
    ):
        output_row = dict(row)
        output_row["rank"] = rank

        writer.writerow({
            field: output_row.get(
                field,
                "",
            )
            for field in csv_fields
        })


# ============================================================
# SQLITE
# ============================================================

with sqlite3.connect(DB_PATH) as con:

    con.execute(
        "DROP TABLE IF EXISTS best_finds"
    )

    con.execute("""
        CREATE TABLE best_finds (
            rank INTEGER,
            score INTEGER,
            requirement_match REAL,
            requirement_context TEXT,
            requirement_depth TEXT,
            requirement_count INTEGER,
            title TEXT,
            company TEXT,
            matched_requirements TEXT,
            partial_requirements TEXT,
            missing_requirements TEXT,
            profile_relevance INTEGER,
            stipend TEXT,
            duration TEXT,
            work_mode TEXT,
            employment_type TEXT,
            posted TEXT,
            apply_by TEXT,
            openings TEXT,
            url TEXT PRIMARY KEY
        )
    """)

    for rank, row in enumerate(
        best_rows,
        start=1,
    ):
        con.execute(
            """
            INSERT INTO best_finds (
                rank,
                score,
                requirement_match,
                requirement_context,
                requirement_depth,
                requirement_count,
                title,
                company,
                matched_requirements,
                partial_requirements,
                missing_requirements,
                profile_relevance,
                stipend,
                duration,
                work_mode,
                employment_type,
                posted,
                apply_by,
                openings,
                url
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                rank,
                int(
                    numeric_score(row)
                ),
                numeric_match(row),
                row.get(
                    "requirement_context",
                    "",
                ),
                row.get(
                    "requirement_depth",
                    "",
                ),
                int(
                    float(
                        row.get(
                            "requirement_count",
                            0,
                        ) or 0
                    )
                ),
                row.get("title", ""),
                row.get("company", ""),
                row.get(
                    "matched_requirements",
                    "",
                ),
                row.get(
                    "partial_requirements",
                    "",
                ),
                row.get(
                    "missing_requirements",
                    "",
                ),
                int(
                    float(
                        row.get(
                            "profile_relevance",
                            0,
                        ) or 0
                    )
                ),
                row.get("stipend", ""),
                row.get("duration", ""),
                row.get("work_mode", ""),
                row.get(
                    "employment_type",
                    "",
                ),
                row.get("posted", ""),
                row.get("apply_by", ""),
                row.get("openings", ""),
                normalize_url(
                    row.get("url", "")
                ),
            ),
        )


# ============================================================
# HTML VIEWER
# ============================================================

def esc(value):
    return html.escape(
        str(value or "")
    )


def score_class(value):
    value = numeric_score(value)

    if value >= 75:
        return "excellent"

    if value >= 60:
        return "good"

    if value >= 45:
        return "medium"

    return "low"


def make_tags(value):
    if not value:
        return "—"

    items = [
        x.strip()
        for x in str(value).split(",")
        if x.strip()
    ]

    if not items:
        return "—"

    return "".join(
        f"<span class='tag'>{esc(item)}</span>"
        for item in items
    )


rows_html = []

for rank, row in enumerate(
    best_rows,
    start=1,
):
    score_value = int(
        numeric_score(row)
    )

    match_value = numeric_match(row)

    url = esc(
        normalize_url(
            row.get("url", "")
        )
    )

    rows_html.append(
        f"""
        <tr>
            <td class="rank">#{rank}</td>

            <td>
                <div class="score {score_class(row)}">
                    {score_value}
                </div>
            </td>

            <td>
                <div class="title">
                    {esc(row.get("title"))}
                </div>
                <div class="company">
                    {esc(row.get("company"))}
                </div>
            </td>

            <td>
                <strong>{match_value:.1f}%</strong>
                <div class="small">
                    {esc(
                        row.get(
                            "requirement_depth"
                        )
                    )} depth
                </div>
            </td>

            <td>
                <strong>
                    {esc(
                        row.get(
                            "requirement_context"
                        )
                    )}
                </strong>
                <div class="small">
                    {esc(
                        row.get(
                            "requirement_count"
                        )
                    )} requirements
                </div>
            </td>

            <td class="requirements">
                {make_tags(
                    row.get(
                        "matched_requirements"
                    )
                )}
            </td>

            <td class="requirements missing">
                {make_tags(
                    row.get(
                        "missing_requirements"
                    )
                )}
            </td>

            <td>
                {esc(row.get("stipend"))}
                <br>
                <span class="small">
                    {esc(row.get("duration"))}
                </span>
            </td>

            <td>
                <a
                    class="open-btn"
                    href="{url}"
                    target="_blank"
                    rel="noopener"
                >
                    Open
                </a>
            </td>
        </tr>
        """
    )


best_score = (
    int(numeric_score(best_rows[0]))
    if best_rows
    else 0
)

html_content = f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Internshala Best Finds</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 30px;

    background: #f5f7fb;
    color: #172033;

    font-family:
        Inter,
        ui-sans-serif,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}}

.container {{
    max-width: 1600px;
    margin: auto;
}}

.header {{
    margin-bottom: 24px;
}}

.header h1 {{
    margin: 0;
    font-size: 32px;
}}

.header p {{
    margin-top: 8px;
    color: #667085;
}}

.summary {{
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    margin-bottom: 22px;
}}

.summary-card {{
    background: white;
    border: 1px solid #e4e7ec;
    border-radius: 12px;
    padding: 14px 18px;
    min-width: 160px;
}}

.summary-label {{
    font-size: 12px;
    color: #667085;
}}

.summary-value {{
    margin-top: 3px;
    font-size: 22px;
    font-weight: 700;
}}

.table-wrap {{
    background: white;
    border: 1px solid #e4e7ec;
    border-radius: 14px;
    overflow: auto;

    box-shadow:
        0 4px 18px rgba(
            16,
            24,
            40,
            0.05
        );
}}

table {{
    width: 100%;
    min-width: 1400px;
    border-collapse: collapse;
}}

th {{
    background: #f8fafc;
    color: #475467;
    text-align: left;

    font-size: 12px;
    padding: 13px;

    border-bottom: 1px solid #e4e7ec;

    position: sticky;
    top: 0;
    z-index: 2;
}}

td {{
    padding: 14px;
    border-bottom: 1px solid #eef1f5;

    vertical-align: top;
    font-size: 13px;
}}

tr:hover td {{
    background: #fafcff;
}}

.rank {{
    font-weight: 700;
    white-space: nowrap;
}}

.score {{
    width: 48px;
    height: 48px;

    border-radius: 12px;

    display: grid;
    place-items: center;

    font-weight: 800;
    font-size: 16px;
}}

.score.excellent {{
    background: #dcfce7;
    color: #166534;
}}

.score.good {{
    background: #dbeafe;
    color: #1d4ed8;
}}

.score.medium {{
    background: #fef3c7;
    color: #92400e;
}}

.score.low {{
    background: #fee2e2;
    color: #991b1b;
}}

.title {{
    font-weight: 700;
    font-size: 14px;
}}

.company {{
    margin-top: 4px;
    color: #667085;
}}

.small {{
    font-size: 11px;
    color: #667085;
}}

.requirements {{
    max-width: 300px;
}}

.tag {{
    display: inline-block;

    margin: 2px 3px 2px 0;
    padding: 4px 7px;

    border-radius: 999px;

    background: #eef4ff;
    color: #3155a4;

    font-size: 11px;
}}

.missing .tag {{
    background: #fff1f2;
    color: #be123c;
}}

.open-btn {{
    display: inline-block;

    background: #111827;
    color: white;

    text-decoration: none;

    padding: 8px 12px;
    border-radius: 8px;

    font-weight: 600;
}}

.open-btn:hover {{
    background: #374151;
}}

.footer {{
    margin-top: 18px;
    color: #667085;
    font-size: 12px;
}}

</style>

</head>

<body>

<div class="container">

    <div class="header">

        <h1>
            Internshala — Best Finds
        </h1>

        <p>
            Top {TOP_N} unique internships retained
            across scraping cycles.
        </p>

    </div>

    <div class="summary">

        <div class="summary-card">
            <div class="summary-label">
                Best finds
            </div>

            <div class="summary-value">
                {len(best_rows)}
            </div>
        </div>

        <div class="summary-card">
            <div class="summary-label">
                Best score
            </div>

            <div class="summary-value">
                {best_score}
            </div>
        </div>

        <div class="summary-card">
            <div class="summary-label">
                Current cycle
            </div>

            <div class="summary-value">
                {len(current)}
            </div>
        </div>

        <div class="summary-card">
            <div class="summary-label">
                Unique pool
            </div>

            <div class="summary-value">
                {len(unique_rows)}
            </div>
        </div>

    </div>

    <div class="table-wrap">

        <table>

            <thead>

                <tr>
                    <th>Rank</th>
                    <th>Score</th>
                    <th>Internship</th>
                    <th>Req. Match</th>
                    <th>Context</th>
                    <th>Matched</th>
                    <th>Missing</th>
                    <th>Stipend / Duration</th>
                    <th></th>
                </tr>

            </thead>

            <tbody>
                {''.join(rows_html)}
            </tbody>

        </table>

    </div>

    <div class="footer">
        Duplicate internships are identified primarily by
        normalized URL. A newer copy replaces the older copy.
    </div>

</div>

</body>

</html>
"""

BEST_HTML.write_text(
    html_content,
    encoding="utf-8",
)


# ============================================================
# OPEN HTML
# ============================================================

def open_file(path):
    if shutil.which("xdg-open"):
        try:
            subprocess.Popen(
                ["xdg-open", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception:
            pass

    return False


print()
print("=" * 60)
print("BEST FINDS UPDATED")
print("=" * 60)

for rank, row in enumerate(
    best_rows,
    start=1,
):
    print(
        f"{rank:>2}. "
        f"{int(numeric_score(row)):>3} | "
        f"{row.get('title', '')[:42]:42} | "
        f"{row.get('company', '')[:28]}"
    )

print()
print(f"CSV : {BEST_CSV}")
print(f"HTML: {BEST_HTML}")

if open_file(BEST_HTML):
    print("\nOpened best_finds.html automatically.")
else:
    print(
        "\nOpen manually:",
        BEST_HTML,
    )
