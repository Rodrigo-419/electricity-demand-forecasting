import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("EIA_API_KEY")
if not api_key:
    raise SystemExit("Falta EIA_API_KEY en el archivo .env")

url = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
params = {
    "api_key": api_key,
    "frequency": "hourly",
    "data[0]": "value",
    "facets[respondent][]": "ERCO",
    "facets[type][]": "D",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "length": 5,
}

response = requests.get(url, params=params, timeout=30)
print("Código de respuesta:", response.status_code)
response.raise_for_status()

df = pd.DataFrame(response.json()["response"]["data"])
print(df)