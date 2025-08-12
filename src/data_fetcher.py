import requests
import pandas as pd

# FRED API endpoint and series IDs
FRED_API_ENDPOINT = "https://api.stlouisfed.org/fred/series/observations"
# WTI Crude Oil: DCOILWTICO
# Henry Hub Natural Gas: DHHNGSP
SERIES_IDS = {
    "WTI": "DCOILWTICO",
    "Henry Hub": "DHHNGSP"
}

def fetch_data(api_key, series_id):
    """Fetches historical data for a given series from FRED.

    Args:
        api_key (str): Your FRED API key.
        series_id (str): The ID of the series to fetch.

    Returns:
        pd.DataFrame: A DataFrame with the historical data.
    """
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json"
    }
    response = requests.get(FRED_API_ENDPOINT, params=params)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()["observations"]
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    df = df[["value"]]
    df["value"] = pd.to_numeric(df["value"], errors='coerce')
    df["value"] = df["value"].ffill()
    df = df.dropna()
    df.columns = [series_id]
    return df
