from io import StringIO
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_world_population_ranking():
    url = "https://www.worldometers.info/world-population/population-by-country/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find table by class 'datatable'
    table = soup.find("table", class_="datatable")
    if not table:
        raise ValueError("Could not find the ranking table on the page.")

    html_str = str(table)
    df = pd.read_html(StringIO(html_str), flavor='lxml')[0]

    # Debug: print column names to verify
    print("Columns found:", df.columns.tolist())

    # Select and rename exact columns based on the actual headers
    df = df[["#", "Country (or dependency)", "Population (2025)"]]
    df.columns = ["rank", "country", "population"]

    ranking = df.to_dict(orient="records")
    return ranking
