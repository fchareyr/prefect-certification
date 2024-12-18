import httpx
from prefect import flow


@flow
def fetch_last_hour_windspeed(latitude: float = 14, longitude: float = 20):
    base_url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=wind_speed_10m"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "wind_speed_10m",
    }

    result = httpx.get(url=base_url, params=params)

    windspeed = result.json()["hourly"]["wind_speed_10m"][0]

    print(windspeed)

    return windspeed


if __name__ == "__main__":
    fetch_last_hour_windspeed.serve("deploy-1")
