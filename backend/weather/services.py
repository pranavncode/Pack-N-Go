import httpx

from django.core.cache import cache
from django.utils import timezone

from .schemas import DailyWeather, WeatherResult


BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude, longitude, start_date, end_date):
    cache_key = (
        f"weather:v1:{latitude:.3f}:{longitude:.3f}:"
        f"{start_date}:{end_date}"
    )

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "timezone": "auto",
        "daily": ",".join([
            "temperature_2m_min",
            "temperature_2m_max",
            "precipitation_probability_max",
            "precipitation_sum",
            "snowfall_sum",
            "wind_speed_10m_max",
        ]),
    }

    try:
        response = httpx.get(
            BASE_URL,
            params=params,
            timeout=10.0,
        )
        response.raise_for_status()
        raw = response.json()

    except httpx.TimeoutException as exc:
        raise RuntimeError("Weather provider timed out.") from exc
    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Weather provider request failed."
        ) from exc

    daily = raw.get("daily")
    if not daily or "time" not in daily:
        raise RuntimeError("Weather data was unavailable.")

    def value_at(key, index):
        values = daily.get(key) or []
        return values[index] if index < len(values) else None

    forecast = []

    for i, day in enumerate(daily["time"]):
        forecast.append(
            DailyWeather(
                date=day,
                temperature_min_c=value_at(
                    "temperature_2m_min", i
                ),
                temperature_max_c=value_at(
                    "temperature_2m_max", i
                ),
                precipitation_probability=value_at(
                    "precipitation_probability_max", i
                ),
                precipitation_sum_mm=value_at(
                    "precipitation_sum", i
                ),
                snowfall_sum_cm=value_at(
                    "snowfall_sum", i
                ),
                wind_speed_max_kmh=value_at(
                    "wind_speed_10m_max", i
                ),
            )
        )

    result = WeatherResult(
        latitude=raw["latitude"],
        longitude=raw["longitude"],
        timezone=raw["timezone"],
        source="Open-Meteo",
        retrieved_at=timezone.now().isoformat(),
        forecast=forecast,
    ).model_dump(mode="json")

    cache.set(cache_key, result, timeout=1800)
    return result