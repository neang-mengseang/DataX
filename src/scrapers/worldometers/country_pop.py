from playwright.sync_api import sync_playwright
from scrapers.worldometers.scrape import normalize_header, clean_value

def normalize_header(h):
    h = h.strip()
    if 'Density' in h:
        h = 'Density (P/Km²)'
    h = h.replace(' %', '%').replace('% ', '%')
    h = h.replace('Pop %', 'Urban Pop %')
    h = h.replace('\u00b2', '')
    h = h.replace("Country'sShare ofWorld Pop", "Country's Share of World Pop")
    h = h.replace("Country's Share of WorldPop", "Country's Share of World Pop")
    h = h.replace("CambodiaGlobalRank", "Cambodia Global Rank")
    h = h.replace("Cambodia GlobalRank", "Cambodia Global Rank")
    h = h.replace('Yearly%Change', 'Yearly % Change')
    h = h.replace('Yearly Change ', 'Yearly Change')
    h = h.replace('YearlyChange', 'Yearly Change')
    h = h.replace('Migrants(net)', 'Migrants (net)')
    h = h.replace('UrbanPopulation', 'Urban Population')
    h = h.replace('UrbanPop%', 'Urban Pop %')
    h = h.replace('WorldPopulation', 'World Population')
    h = h.replace('FertilityRate', 'Fertility Rate')
    h = h.replace('MedianAge', 'Median Age')
    h = ' '.join(h.split())
    return h

def clean_value(value):
    if not isinstance(value, str):
        return value

    value = value.replace('\u2212', '-').strip()  # Unicode minus to ASCII minus
    no_commas = value.replace(',', '')

    if '%' in no_commas:
        try:
            return float(no_commas.strip('%')) / 100
        except ValueError:
            return value

    try:
        if '.' in no_commas:
            return float(no_commas)
        else:
            return int(no_commas)
    except ValueError:
        return value

def scrape_country_population(country: str):
    url = f"https://www.worldometers.info/world-population/{country}-population/"
    print(f"[INFO] Starting scraping for country: {country}")
    print(f"[INFO] Target URL: {url}")

    with sync_playwright() as p:
        print("[INFO] Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("[INFO] Navigating to page...")
        page.goto(url, wait_until="load", timeout=60000)
        print("[SUCCESS] Page loaded.")

        try:
            print("[INFO] Waiting for population selector...")
            page.wait_for_selector('span.rts-counter[rel*="population"]', timeout=10000)
            print("[SUCCESS] Population selector found.")
        except Exception as e:
            browser.close()
            raise ValueError(f"Could not find the population data element for '{country}': {e}")

        table_selector = 'table.datatable'
        try:
            page.wait_for_selector(table_selector, timeout=10000)
            tables = page.query_selector_all(table_selector)
            if len(tables) < 2:
                raise ValueError("Expected at least 2 tables: historical and forecast.")
            print("[SUCCESS] Found population data tables.")
        except Exception as e:
            browser.close()
            raise ValueError(f"Could not find population data tables for '{country}': {e}")

        def extract_table_data(table):
            headers = table.eval_on_selector_all(
                'thead tr th',
                'ths => ths.map(th => th.textContent.trim().replace(/\\n/g, " ").replace(/\\s+/g, " "))'
            )
            rows = table.eval_on_selector_all(
                'tbody tr',
                '''rows => rows.map(row => {
                    const cells = Array.from(row.querySelectorAll('td'));
                    return cells.map(cell => cell.textContent.trim());
                })'''
            )
            return headers, rows

        # Extract historical data
        hist_headers, hist_rows = extract_table_data(tables[0])
        # Extract forecast data
        fore_headers, fore_rows = extract_table_data(tables[1])

        # Normalize headers
        hist_headers = [normalize_header(h) for h in hist_headers]
        fore_headers = [normalize_header(h) for h in fore_headers]

        # Convert rows to dicts and clean values
        historical_data = [{hist_headers[i]: clean_value(row[i]) for i in range(min(len(hist_headers), len(row)))} for row in hist_rows]
        forecast_data = [{fore_headers[i]: clean_value(row[i]) for i in range(min(len(fore_headers), len(row)))} for row in fore_rows]
        print(f"[INFO]  Historical data: {len(historical_data)}")
        print(f"[INFO]  Forecast data: {len(forecast_data)}")
        # Get live population
        live_population = page.eval_on_selector(
            'span.rts-counter[rel*="population"]',
            'el => el.textContent.trim()'
        )
        live_population = live_population.replace(',', '')
        try:
            live_population = int(live_population)
        except ValueError:
            live_population = 0
        print("[DEBUG] Live population container text:", live_population)

        # Extract key statistics
        stat_labels = [
            "Fertility Rate", "Median Age", "Urban Population",
            "World Population Share", "Global Rank"
        ]
        print("[INFO] Extracting key statistics...")
        stat_elements = page.query_selector_all("div.col-md-6 div strong")
        stats = {}
        for i, label in enumerate(stat_labels):
            if i < len(stat_elements):
                value = stat_elements[i].text_content().strip()
                stats[label] = value
                print(f"[DATA] {label}: {value}")

        browser.close()
        print("[INFO] Browser closed.")
        print("[SUCCESS] Scraping completed.\n")

        return {
            "country": country,
            "live_population": live_population,
            "stats": stats,
            "historical_population": historical_data,
            "forecast_population": forecast_data,
        }

