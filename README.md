
````markdown
# Population Data Scraper & API

This project scrapes world and country population data from [Worldometers](https://www.worldometers.info/) using Playwright and BeautifulSoup, and exposes REST API endpoints via Flask for easy consumption.

---

## Features

- Scrape current world population and statistics (births, deaths, growth)
- Scrape population rankings by country
- Scrape country-specific population data
- RESTful API endpoints to access scraped data
- Robust scraping with headless browsers (Playwright)
- Error handling and logging

---

## Requirements

- Python 3.8+
- Virtual environment (recommended)
- Internet connection (for scraping)
- Playwright dependencies (browsers)

---

## Setup & Installation

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
````

2. **Create and activate a virtual environment**

On Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers**

Playwright requires installing browser binaries separately:

```bash
playwright install
```

This installs Chromium, Firefox, and WebKit browsers needed for scraping.

---

## Running the Application

Start the Flask server:

```bash
python src/app.py
```

You should see output indicating the server is running, e.g.:

```
 * Running on http://127.0.0.1:5000/
```

---

## API Endpoints

| Endpoint                         | Method | Description                        |
| -------------------------------- | ------ | ---------------------------------- |
| `/api/population/world`          | GET    | Get current world population stats |
| `/api/population/world/ranking`  | GET    | Get population rankings by country |
| `/api/population/country/<name>` | GET    | Get population data for a country  |

---

## Example Request

```bash
curl http://127.0.0.1:5000/api/population/world
```

Sample response:

```json
{
  "data": {
    "current_population": 8233067913,
    "births_today": 333974,
    "deaths_today": 157370,
    "population_growth_today": 176604,
    "births_this_year": 67807155,
    "deaths_this_year": 31951049,
    "population_growth_this_year": 35856106
  }
}
```

---

## Troubleshooting

* If you get errors about missing Playwright browsers, run:

  ```bash
  playwright install
  ```

* For issues with dependencies, verify you installed all from `requirements.txt`.

* If the scraper stops working, the source site structure may have changed. Inspect selectors and update scraping logic.

---

## Development

* Scrapers are located under `src/scrapers/worldometers/`.
* API routes are in `src/routes/population.py`.
* Use Playwright for dynamic content scraping.
* Logging is enabled for debugging errors.

---

## Contributing

Feel free to open issues or pull requests to improve the scraper or API functionality.

---

## License

MIT License

---

## Resources

* [Playwright Python Documentation](https://playwright.dev/python/docs/intro)
* [Flask Documentation](https://flask.palletsprojects.com/)
* [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

*Made with ❤️ by Twilight*

```

