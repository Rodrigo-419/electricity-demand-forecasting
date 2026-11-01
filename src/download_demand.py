import os
import time

import pandas as pd
import requests
from dotenv import load_dotenv

URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
PAGE_SIZE = 5000


def fetch_demand(region, start, end):
    load_dotenv()
    api_key = os.getenv("EIA_API_KEY")
    if not api_key:
        raise SystemExit("Falta EIA_API_KEY en el archivo .env")

    rows = []
    offset = 0
    while True:
        params = {
            "api_key": api_key,
            "frequency": "hourly",
            "data[0]": "value",
            "facets[respondent][]": region,
            "facets[type][]": "D",
            "start": start,
            "end": end,
            "sort[0][column]": "period",
            "sort[0][direction]": "asc",
            "offset": offset,
            "length": PAGE_SIZE,
        }
        response = requests.get(URL, params=params, timeout=60)
        response.raise_for_status()
        page = response.json()["response"]["data"]

        if not page:
            break
        rows.extend(page)
        print(f"Descargadas {len(rows)} filas")
        if len(page) < PAGE_SIZE:
            break

        offset += PAGE_SIZE
        time.sleep(1)

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = fetch_demand("ERCO", "2025-01-01T00", "2025-12-31T23")
    print(df.shape)
    print(df.head())
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/erco_demand_2025.csv", index=False)