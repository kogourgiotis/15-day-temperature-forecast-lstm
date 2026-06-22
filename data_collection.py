import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import date, timedelta, datetime

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"

# Most important variables for daily avg temp prediction
daily_vars = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min"
]

all_dataframes = []
current_year = datetime.now().year
years = list(range(current_year - 5, current_year + 1))

# Loop through years
for year in years:
    if year == current_year:
        end_date = date.today() - timedelta(days=0)
    else:
        end_date = f"{year+1}-01-01"

    params = {
        "latitude": 38.91260134888489,
        "longitude": 22.42789743600883,
        "start_date": f"{year}-01-02",
        "end_date": end_date,
        "daily": ",".join(daily_vars),
        "timezone": "auto"
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    daily = response.Daily()

    # Build DataFrame
    dates = pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        periods=daily.Variables(0).ValuesAsNumpy().size,
        freq="D"
    )

    data = {"date": dates}
    for i, var in enumerate(daily_vars):
        data[var] = daily.Variables(i).ValuesAsNumpy()

    df = pd.DataFrame(data)
    #df = df.dropna(subset=["temperature_2m_max", "temperature_2m_min"])
    #df["temperature_2m_mean"] = df["temperature_2m_mean"].fillna((df["temperature_2m_max"] + df["temperature_2m_min"]) / 2)
    all_dataframes.append(df)

# Combine and save
final_df = pd.concat(all_dataframes).reset_index(drop=True)
final_df.to_csv("dataset.csv", index=False)