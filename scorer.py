import re
import config


# ============================================================
# YOUR SKILLS
# ============================================================

YOUR_SKILLS = {
    "html",
    "html5",
    "css",
    "css3",
    "javascript",
    "react",
    "next.js",
    "nextjs",
    "typescript",

    "rest api",
    "rest apis",
    "api",
    "api design",
    "jwt",
    "authentication",
    "authorization",
    "bcrypt",

    "sql",
    "sqlite",
    "database",
    "database design",
    "transactions",
    "indexing",

    "docker",
    "aws",
    "aws ec2",
    "git",
    "github",
    "github actions",
    "ci/cd",
    "linux",
    "caddy",

    "python",
    "fastapi",
    "firebase",
    "recharts",

    "data structures",
    "object oriented programming",
    "oop",
    "system design",
    "software architecture",
}


# ============================================================
# SKILLS YOU HAVE ACTUALLY USED IN PROJECTS
# ============================================================

PROJECT_SKILLS = {
    "html",
    "css",
    "javascript",
    "react",
    "next.js",
    "sql",
    "sqlite",
    "database",
    "database design",
    "rest api",
    "api",
    "jwt",
    "authentication",
    "authorization",
    "docker",
    "aws",
    "aws ec2",
    "git",
    "github",
    "github actions",
    "ci/cd",
    "linux",
    "firebase",
    "recharts",
    "system design",
    "software architecture",
}


# ============================================================
# RELATED / PARTIAL MATCHES
# ============================================================

RELATED_SKILLS = {
    "react native": ["react"],
    "node.js": ["javascript"],
    "nodejs": ["javascript"],

    "frontend": [
        "html",
        "css",
        "javascript",
    ],

    "front end": [
        "html",
        "css",
        "javascript",
    ],

    "backend": [
        "api",
        "database",
    ],

    "back end": [
        "api",
        "database",
    ],

    "web development": [
        "html",
        "css",
        "javascript",
    ],

    "full stack": [
        "html",
        "css",
        "javascript",
        "api",
        "database",
    ],
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):
    text = text.lower().strip()

    replacements = {
        "nextjs": "next.js",
        "nodejs": "node.js",
        "fullstack": "full stack",
        "front-end": "front end",
        "back-end": "back end",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return re.sub(r"\s+", " ", text)


def contains_skill(skill, known_skills):
    skill = normalize(skill)

    return any(
        skill == normalize(known)
        for known in known_skills
    )


def partial_skill_match(skill):
    skill = normalize(skill)

    for required, alternatives in RELATED_SKILLS.items():
        if skill == normalize(required):
            for known in alternatives:
                if contains_skill(
                    known,
                    YOUR_SKILLS
                ):
                    return 0.5

    return 0


def clean_requirements(required_skills):
    skills = [
        normalize(skill)
        for skill in required_skills.split(",")
        if skill.strip()
    ]

    return list(dict.fromkeys(skills))


# ============================================================
# JOB CONTEXT
#
# We infer the domain from the REQUIREMENTS themselves.
# The title is deliberately not used.
# ============================================================

WEB_CONTEXT = {
    "html",
    "html5",
    "css",
    "css3",
    "javascript",
    "typescript",
    "react",
    "next.js",
    "frontend",
    "front end",
    "backend",
    "back end",
    "web development",
    "full stack",
    "rest api",
    "api",
    "node.js",
    "nodejs",
}

DATA_CONTEXT = {
    "data analytics",
    "data analysis",
    "data science",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "statistics",
    "data visualization",
}

AI_CONTEXT = {
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "natural language processing (nlp)",
    "nlp",
    "neural networks",
    "tensorflow",
    "pytorch",
    "computer vision",
    "generative ai",
}

MOBILE_CONTEXT = {
    "react native",
    "flutter",
    "android",
    "ios",
    "mobile development",
}


def detect_context(skills):
    counts = {
        "web": 0,
        "data": 0,
        "ai": 0,
        "mobile": 0,
    }

    for skill in skills:
        if skill in WEB_CONTEXT:
            counts["web"] += 1

        if skill in DATA_CONTEXT:
            counts["data"] += 1

        if skill in AI_CONTEXT:
            counts["ai"] += 1

        if skill in MOBILE_CONTEXT:
            counts["mobile"] += 1

    context = max(
        counts,
        key=counts.get
    )

    if counts[context] == 0:
        return "general"

    return context


# ============================================================
# REQUIREMENT WEIGHTS
# ============================================================

def requirement_weight(skill, context):
    skill = normalize(skill)

    # --------------------------------------------------------
    # Context-specific importance
    # --------------------------------------------------------

    if context == "web":
        weights = {
            "next.js": 15,
            "react": 15,
            "javascript": 15,
            "typescript": 15,
            "node.js": 13,
            "nodejs": 13,
            "rest api": 10,
            "api": 9,
            "html": 10,
            "html5": 10,
            "css": 10,
            "css3": 10,
            "sql": 8,
            "mysql": 8,
            "postgresql": 8,
            "mongodb": 7,
            "git": 6,
            "github": 5,
            "docker": 7,
            "aws": 7,
            "python": 7,
            "fastapi": 9,

            # Web-adjacent but not your main stack.
            "wordpress": 5,
            "bootstrap": 5,
            "tailwind css": 6,

            # Generic.
            "english proficiency (spoken)": 3,
            "english proficiency (written)": 3,
            "effective communication": 3,
            "communication": 3,
            "interpersonal skills": 3,
        }

        if skill in weights:
            return weights[skill]

    # --------------------------------------------------------
    # Data / analytics context
    # --------------------------------------------------------

    if context == "data":
        weights = {
            "data analytics": 15,
            "data analysis": 15,
            "data science": 15,
            "power bi": 12,
            "tableau": 12,
            "pandas": 10,
            "numpy": 9,
            "statistics": 10,
            "data visualization": 10,
            "python": 10,
            "sql": 10,
            "mysql": 8,
            "postgresql": 8,
            "machine learning": 12,

            # Web skills are not central to a data role.
            "html": 3,
            "html5": 3,
            "css": 3,
            "css3": 3,
            "javascript": 4,
            "react": 3,

            "ms-excel": 8,
            "microsoft excel": 8,

            "git": 5,
            "docker": 5,

            "english proficiency (spoken)": 3,
            "english proficiency (written)": 3,
            "effective communication": 3,
        }

        if skill in weights:
            return weights[skill]

    # --------------------------------------------------------
    # AI context
    # --------------------------------------------------------

    if context == "ai":
        weights = {
            "artificial intelligence": 15,
            "machine learning": 15,
            "deep learning": 15,
            "natural language processing (nlp)": 15,
            "nlp": 15,
            "neural networks": 15,
            "tensorflow": 12,
            "pytorch": 12,
            "computer vision": 12,
            "python": 10,
            "data science": 12,
            "data analytics": 10,
            "sql": 7,

            "html": 3,
            "css": 3,
            "javascript": 4,
            "react": 4,

            "git": 5,
            "docker": 5,

            "english proficiency (spoken)": 3,
            "english proficiency (written)": 3,
        }

        if skill in weights:
            return weights[skill]

    # --------------------------------------------------------
    # Mobile context
    # --------------------------------------------------------

    if context == "mobile":
        weights = {
            "react native": 15,
            "flutter": 15,
            "android": 15,
            "ios": 15,
            "mobile development": 15,
            "react": 10,
            "javascript": 10,
            "typescript": 10,
            "firebase": 7,
            "rest api": 7,
            "api": 7,
            "git": 5,

            "html": 3,
            "css": 3,

            "english proficiency (spoken)": 3,
            "english proficiency (written)": 3,
        }

        if skill in weights:
            return weights[skill]

    # --------------------------------------------------------
    # General fallback
    # --------------------------------------------------------

    if skill in {
        "next.js",
        "react",
        "javascript",
        "typescript",
    }:
        return 15

    if skill in {
        "html",
        "html5",
        "css",
        "css3",
        "python",
        "sql",
        "database",
        "api",
        "rest api",
        "fastapi",
    }:
        return 10

    if skill in {
        "docker",
        "aws",
        "git",
        "github",
        "jwt",
        "authentication",
        "authorization",
        "linux",
        "firebase",
        "system design",
        "software architecture",
    }:
        return 7

    if skill in {
        "english proficiency (spoken)",
        "english proficiency (written)",
        "effective communication",
        "communication",
        "interpersonal skills",
        "ms-office",
        "ms-excel",
        "ms-word",
        "problem solving",
    }:
        return 3

    return 5


# ============================================================
# REQUIREMENT DEPTH
#
# Prevents a tiny requirement list from behaving like a
# deeply specified technical role.
# ============================================================

def depth_factor(total_weight):
    if total_weight >= 60:
        return 1.00

    if total_weight >= 40:
        return 0.90

    if total_weight >= 25:
        return 0.75

    if total_weight >= 15:
        return 0.60

    return 0.45


def depth_label(total_weight):
    if total_weight >= 60:
        return "High"

    if total_weight >= 40:
        return "Medium-High"

    if total_weight >= 25:
        return "Medium"

    if total_weight >= 15:
        return "Low"

    return "Very Low"


# ============================================================
# REQUIREMENT MATCHING
# ============================================================

def calculate_requirement_match(
    required_skills
):
    skills = clean_requirements(
        required_skills
    )

    if not skills:
        return {
            "score": 0,
            "percentage": 0,
            "matched": [],
            "partial": [],
            "missing": [],
            "total_weight": 0,
            "matched_weight": 0,
            "depth_factor": 0,
            "depth_label": "None",
            "context": "general",
            "count": 0,
        }

    context = detect_context(skills)

    total_weight = 0
    matched_weight = 0

    matched = []
    partial = []
    missing = []

    for skill in skills:
        weight = requirement_weight(
            skill,
            context
        )

        total_weight += weight

        if contains_skill(
            skill,
            YOUR_SKILLS
        ):
            matched_weight += weight
            matched.append(skill)
            continue

        factor = partial_skill_match(skill)

        if factor:
            matched_weight += (
                weight * factor
            )
            partial.append(skill)
        else:
            missing.append(skill)

    coverage = (
        matched_weight / total_weight * 100
        if total_weight
        else 0
    )

    factor = depth_factor(
        total_weight
    )

    score = (
        60
        * (coverage / 100)
        * factor
    )

    return {
        "score": round(score, 2),
        "percentage": round(
            coverage,
            2
        ),
        "matched": matched,
        "partial": partial,
        "missing": missing,
        "total_weight": total_weight,
        "matched_weight": round(
            matched_weight,
            2
        ),
        "depth_factor": factor,
        "depth_label": depth_label(
            total_weight
        ),
        "context": context,
        "count": len(skills),
    }


# ============================================================
# TECHNICAL PROFILE RELEVANCE
#
# Based on matched REQUIREMENTS, never the title.
# ============================================================

def technical_profile_relevance(
    matched,
    context
):
    matched = {
        normalize(x)
        for x in matched
    }

    score = 0

    web_hits = matched & {
        "html",
        "html5",
        "css",
        "css3",
        "javascript",
        "react",
        "next.js",
        "typescript",
    }

    backend_hits = matched & {
        "api",
        "rest api",
        "sql",
        "sqlite",
        "database",
        "python",
        "fastapi",
        "jwt",
        "authentication",
        "authorization",
    }

    devops_hits = matched & {
        "docker",
        "aws",
        "git",
        "github",
        "github actions",
        "ci/cd",
        "linux",
    }

    if context == "web":
        if len(web_hits) >= 4:
            score += 5
        elif len(web_hits) >= 2:
            score += 4
        elif web_hits:
            score += 2

        if len(backend_hits) >= 2:
            score += 3
        elif backend_hits:
            score += 2

        if devops_hits:
            score += 2

    elif context == "mobile":
        # You have React/JavaScript experience, but not
        # demonstrated mobile development.
        if "react" in matched:
            score += 2
        elif "javascript" in matched:
            score += 1

    elif context == "data":
        # Python + SQL are transferable, but this is not
        # treated as proven data-specialist experience.
        if "python" in matched:
            score += 2

        if "sql" in matched:
            score += 2

    # AI gets no positive profile bonus.
    return min(score, 10)


# ============================================================
# PROJECT EVIDENCE
# ============================================================

def project_evidence(
    matched,
    partial,
    context
):
    matched = {
        normalize(x)
        for x in matched
    }

    project_hits = (
        matched & PROJECT_SKILLS
    )

    points = 0

    for _ in project_hits:
        points += 2

    # Keep unrelated/domain-transfer evidence from becoming
    # more important than the actual requirement match.
    if context in {
        "ai",
        "data",
        "mobile",
    }:
        points = min(
            points,
            5
        )

    return min(
        points,
        15
    )


# ============================================================
# STIPEND
# ============================================================

def stipend_score(stipend):
    stipend = normalize(stipend)

    if "unpaid" in stipend:
        return 0

    numbers = [
        int(x.replace(",", ""))
        for x in re.findall(
            r"\d[\d,]*",
            stipend
        )
    ]

    if not numbers:
        return 0

    highest = max(numbers)

    if highest >= 15000:
        return 5

    if highest >= 10000:
        return 4

    if highest >= 7500:
        return 3

    if highest >= 5000:
        return 2

    return 1


# ============================================================
# WORK MODE
# ============================================================

def work_mode_score(job):
    mode = normalize(
        job.get("work_mode", "")
    )

    return (
        5
        if "work from home" in mode
        else 0
    )


# ============================================================
# DURATION
# ============================================================

def duration_score(job):
    duration = normalize(
        job.get("duration", "")
    )

    match = re.search(
        r"(\d+)\s*month",
        duration
    )

    if not match:
        return 0

    months = int(match.group(1))

    if months <= config.MAX_DURATION_MONTHS:
        return 5

    if months <= 9:
        return 3

    return 1


# ============================================================
# FINAL SCORE
# ============================================================

def score_job(job):
    requirements = (
        calculate_requirement_match(
            job.get(
                "required_skills",
                ""
            )
        )
    )

    profile = (
        technical_profile_relevance(
            requirements["matched"],
            requirements["context"]
        )
    )

    project = project_evidence(
        requirements["matched"],
        requirements["partial"],
        requirements["context"]
    )

    stipend = stipend_score(
        job.get("stipend", "")
    )

    remote = work_mode_score(job)

    duration = duration_score(job)

    score = round(
        requirements["score"]
        + project
        + profile
        + stipend
        + remote
        + duration
    )

    score = max(
        0,
        min(score, 100)
    )

    job["score"] = score

    job["requirement_match"] = (
        requirements["percentage"]
    )

    job["requirement_count"] = (
        requirements["count"]
    )

    job["requirement_depth"] = (
        requirements["depth_label"]
    )

    job["requirement_context"] = (
        requirements["context"]
    )

    job["matched_requirements"] = (
        ", ".join(
            requirements["matched"]
        )
    )

    job["partial_requirements"] = (
        ", ".join(
            requirements["partial"]
        )
    )

    job["missing_requirements"] = (
        ", ".join(
            requirements["missing"]
        )
    )

    job["matched_weight"] = (
        requirements["matched_weight"]
    )

    job["total_requirement_weight"] = (
        requirements["total_weight"]
    )

    job["profile_relevance"] = profile

    job["matched_keywords"] = (
        job["matched_requirements"]
    )

    return job


def score_jobs(jobs):
    return sorted(
        (
            score_job(job)
            for job in jobs
        ),
        key=lambda job: job["score"],
        reverse=True,
    )
