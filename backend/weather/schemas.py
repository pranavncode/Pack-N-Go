from datetime import date
from pydantic import BaseModel


class WeatherRequest(BaseModel):
    latitude: float
    longitude: float
    start_date: date
    end_date: date


class DailyWeather(BaseModel):
    date: date
    temperature_min_c: float | None
    temperature_max_c: float | None
    precipitation_probability: float | None
    precipitation_sum_mm: float | None
    snowfall_sum_cm: float | None
    wind_speed_max_kmh: float | None


class WeatherResult(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    source: str
    retrieved_at: str
    forecast: list[DailyWeather]