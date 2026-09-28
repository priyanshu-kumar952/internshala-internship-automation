import re
from urllib.parse import urljoin


BASE = "https://internshala.com"


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def get_text(card, selector):
    try:
        return clean(
            card.locator(selector).first.inner_text(timeout=2000)
        )
    except Exception:
        return ""


def scrape_detail_page(detail):
    """
    Extract information that is only available on the
    internship detail page.
    """

    required_skills = []

    try:
        skills = detail.locator(
            "h3.skills_heading + div.round_tabs_container span.round_tabs"
        )

        for i in range(skills.count()):
            skill = clean(
                skills.nth(i).inner_text(timeout=1000)
            )

            if skill:
                required_skills.append(skill)

    except Exception:
        pass

    # Full description
    description = ""

    try:
        about_heading = detail.locator(
            "h2.about_heading"
        )

        if about_heading.count():
            description = clean(
                about_heading
                .locator("xpath=following-sibling::div[1]")
                .inner_text(timeout=3000)
            )
    except Exception:
        pass

    # Who can apply
    who_can_apply = ""

    try:
        section = detail.locator(
            ".who_can_apply"
        )

        if section.count():
            who_can_apply = clean(
                section.inner_text(timeout=2000)
            )
    except Exception:
        pass

    # Apply-by date
    apply_by = ""

    try:
        item = detail.locator(
            ".apply_by .item_body"
        )

        if item.count():
            apply_by = clean(
                item.inner_text(timeout=1000)
            )
    except Exception:
        pass

    # Number of openings
    openings = ""

    try:
        heading = detail.get_by_text(
            "Number of openings",
            exact=True
        )

        if heading.count():
            value = heading.locator(
                "xpath=following-sibling::div[1]"
            )

            if value.count():
                openings = clean(
                    value.inner_text(timeout=1000)
                )
    except Exception:
        pass

    return {
        "required_skills": ", ".join(required_skills),
        "detail_description": description,
        "who_can_apply": who_can_apply,
        "apply_by": apply_by,
        "openings": openings,
    }


def scrape_current_page(page):
    jobs = []
    seen = set()

    cards = page.locator(
        "div.individual_internship"
    )

    count = cards.count()

    print(f"Found {count} internship cards.")

    # One reusable detail tab.
    detail = page.context.new_page()

    try:
        for i in range(count):
            card = cards.nth(i)

            try:
                # ------------------------------------------------
                # URL
                # ------------------------------------------------

                link = card.locator(
                    "a.job-title-href"
                ).first

                url = link.get_attribute(
                    "href",
                    timeout=2000
                )

                if not url:
                    continue

                url = urljoin(BASE, url)

                if url in seen:
                    continue

                seen.add(url)

                # ------------------------------------------------
                # CARD DATA
                # ------------------------------------------------

                title = get_text(
                    card,
                    "a.job-title-href"
                )

                company = get_text(
                    card,
                    "p.company-name"
                )

                location = get_text(
                    card,
                    ".locations"
                )

                stipend = get_text(
                    card,
                    ".stipend"
                )

                duration = ""

                try:
                    row_items = card.locator(
                        ".detail-row-1 .row-1-item"
                    )

                    if row_items.count() >= 3:
                        duration = clean(
                            row_items.nth(2).inner_text(
                                timeout=2000
                            )
                        )
                except Exception:
                    pass

                description = get_text(
                    card,
                    ".about_job .text"
                )

                skills = []

                skill_elements = card.locator(
                    ".job_skill"
                )

                for j in range(
                    skill_elements.count()
                ):
                    skill = clean(
                        skill_elements.nth(j).inner_text(
                            timeout=1000
                        )
                    )

                    if skill:
                        skills.append(skill)

                posted = get_text(
                    card,
                    ".status-success"
                )

                employment_type = get_text(
                    card,
                    ".status-li"
                )

                # ------------------------------------------------
                # DETAIL PAGE
                # ------------------------------------------------

                print(
                    f"[{i + 1}/{count}] "
                    f"Opening detail: {title}"
                )

                detail.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=30000
                )

                # Give dynamic content a small chance to load.
                detail.wait_for_timeout(500)

                detail_data = scrape_detail_page(
                    detail
                )

                jobs.append({
                    "title": title,
                    "company": company,
                    "stipend": stipend,
                    "duration": duration,
                    "location": location,
                    "work_mode": (
                        "Work from home"
                        if "work from home"
                        in location.lower()
                        else location
                    ),
                    "skills": ", ".join(skills),
                    "required_skills":
                        detail_data[
                            "required_skills"
                        ],
                    "description": description,
                    "detail_description":
                        detail_data[
                            "detail_description"
                        ],
                    "who_can_apply":
                        detail_data[
                            "who_can_apply"
                        ],
                    "apply_by":
                        detail_data[
                            "apply_by"
                        ],
                    "openings":
                        detail_data[
                            "openings"
                        ],
                    "posted": posted,
                    "employment_type":
                        employment_type,
                    "url": url,
                })

            except Exception as e:
                print(
                    f"Skipping card {i}: "
                    f"{type(e).__name__}: {e}"
                )

    finally:
        detail.close()

    print(
        f"Successfully extracted "
        f"{len(jobs)} internships."
    )

    return jobs
