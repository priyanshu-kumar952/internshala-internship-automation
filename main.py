from pathlib import Path

from playwright.sync_api import sync_playwright

from scraper import scrape_current_page
from scorer import score_jobs
from database import save_jobs, export_csv
import config


def find_results_page(context):
    """
    Find an existing Internshala internship-results tab.
    Ignore individual internship detail pages.
    """

    for page in context.pages:
        url = page.url.lower()

        if (
            "internshala.com/internships/" in url
            and "/internship/detail/" not in url
        ):
            return page

    return None


def main():
    Path("data").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)

    with sync_playwright() as p:
        print("Connecting to existing Chrome...")

        browser = p.chromium.connect_over_cdp(
            "http://127.0.0.1:9222"
        )

        if not browser.contexts:
            raise RuntimeError(
                "No Chrome browser context found."
            )

        context = browser.contexts[0]

        page = find_results_page(context)

        if page is None:
            print(
                "\nNo internship results tab found."
            )
            print(
                "Opening the configured Internshala URL..."
            )

            page = context.new_page()

            page.goto(
                config.BASE_URL,
                wait_until="domcontentloaded",
                timeout=30000
            )

        print("Connected to Chrome.")
        print("Results page:", page.url)

        # Make sure result cards are present.
        try:
            page.locator(
                "div.individual_internship"
            ).first.wait_for(
                state="visible",
                timeout=10000
            )
        except Exception:
            print(
                "\nCould not find internship result cards."
            )
            print(
                "Open an Internshala internship-results "
                "page manually and run again."
            )
            return

        input(
            "\nPress ENTER to start scraping... "
        )

        jobs = scrape_current_page(page)

        # Current scorer is still temporary.
        # We will replace it with requirement matching next.
        jobs = score_jobs(jobs)

        save_jobs(
            jobs,
            config.DB_PATH
        )

        export_csv(
            jobs,
            config.CSV_PATH
        )

        print(
            f"\nCollected: {len(jobs)} internships"
        )

        for job in jobs[:10]:
            print(
                f"{job['score']:>3} | "
                f"{job['title'][:45]:45} | "
                f"{job['company'][:25]}"
            )

        print(
            f"\nCSV: {config.CSV_PATH}"
        )
        print(
            f"Database: {config.DB_PATH}"
        )


if __name__ == "__main__":
    main()
