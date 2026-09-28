import csv
import sqlite3
from pathlib import Path


FIELDS = {
    "url": "TEXT PRIMARY KEY",
    "title": "TEXT",
    "company": "TEXT",
    "stipend": "TEXT",
    "duration": "TEXT",
    "location": "TEXT",
    "work_mode": "TEXT",
    "skills": "TEXT",
    "required_skills": "TEXT",
    "description": "TEXT",
    "detail_description": "TEXT",
    "who_can_apply": "TEXT",
    "apply_by": "TEXT",
    "openings": "TEXT",
    "posted": "TEXT",
    "employment_type": "TEXT",

    # Scoring
    "score": "INTEGER",
    "requirement_match": "REAL",
    "matched_requirements": "TEXT",
    "partial_requirements": "TEXT",
    "missing_requirements": "TEXT",
    "matched_weight": "REAL",
    "total_requirement_weight": "REAL",
    "profile_relevance": "INTEGER",
    "matched_keywords": "TEXT",
}


def connect(path):
    return sqlite3.connect(path)


def ensure_table(con):
    columns_sql = []

    for name, column_type in FIELDS.items():
        columns_sql.append(
            f"{name} {column_type}"
        )

    # Create table if it does not exist.
    con.execute(
        f"""
        CREATE TABLE IF NOT EXISTS internships (
            {", ".join(columns_sql)}
        )
        """
    )

    # Add any columns missing from an older database.
    existing = {
        row[1]
        for row in con.execute(
            "PRAGMA table_info(internships)"
        ).fetchall()
    }

    for name, column_type in FIELDS.items():
        if name not in existing:
            con.execute(
                f"""
                ALTER TABLE internships
                ADD COLUMN {name} {column_type}
                """
            )


def save_jobs(jobs, path):
    Path(path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with connect(path) as con:
        ensure_table(con)

        columns = list(FIELDS.keys())

        placeholders = ", ".join(
            "?" for _ in columns
        )

        update_columns = [
            column
            for column in columns
            if column != "url"
        ]

        update_sql = ", ".join(
            f"{column}=excluded.{column}"
            for column in update_columns
        )

        sql = f"""
            INSERT INTO internships (
                {", ".join(columns)}
            )
            VALUES (
                {placeholders}
            )
            ON CONFLICT(url) DO UPDATE SET
                {update_sql}
        """

        for job in jobs:
            values = [
                job.get(column, "")
                for column in columns
            ]

            con.execute(sql, values)


def export_csv(jobs, path):
    Path(path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fields = [
        "score",
        "requirement_match",
        "profile_relevance",
        "title",
        "company",
        "required_skills",
        "matched_requirements",
        "partial_requirements",
        "missing_requirements",
        "matched_weight",
        "total_requirement_weight",
        "stipend",
        "duration",
        "work_mode",
        "employment_type",
        "skills",
        "posted",
        "apply_by",
        "openings",
        "url",
        "description",
        "detail_description",
        "who_can_apply",
    ]

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fields,
            extrasaction="ignore"
        )

        writer.writeheader()
        writer.writerows(jobs)
