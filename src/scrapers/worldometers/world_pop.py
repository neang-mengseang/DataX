from playwright.sync_api import sync_playwright

def extract_number(span_element):
    # Join all nested number parts and remove commas
    return int("".join(span_element.inner_text().split(",")).strip())


def scrape_world_population():
    url = "https://www.worldometers.info/world-population/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_selector(".rts-counter", timeout=15000)

            # Scrape main population
            population_span = page.query_selector('span[rel="current_population"]')
            current_population = extract_number(population_span)

            # Scrape today's data
            births_today = extract_number(page.query_selector('span[rel="births_today"]'))
            deaths_today = extract_number(page.query_selector('span[rel="dth1s_today"]'))
            growth_today = extract_number(page.query_selector('span[rel="absolute_growth"]'))

            # Scrape this year's data
            births_year = extract_number(page.query_selector('span[rel="births_this_year"]'))
            deaths_year = extract_number(page.query_selector('span[rel="dth1s_this_year"]'))
            growth_year = extract_number(page.query_selector('span[rel="absolute_growth_year"]'))

            return {
                "current_population": current_population,
                "today": {
                    "births": births_today,
                    "deaths": deaths_today,
                    "growth": growth_today
                },
                "this_year": {
                    "births": births_year,
                    "deaths": deaths_year,
                    "growth": growth_year
                }
            }
        finally:
            browser.close()

