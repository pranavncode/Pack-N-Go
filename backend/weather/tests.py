from django.test import TestCase

# Create your tests here.
from datetime import date
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from .services import get_weather


class WeatherTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_rejects_invalid_coordinates(self):
        response = self.client.post(
            "/api/v1/weather/assess/",
            {
                "latitude": 120,
                "longitude": 79,
                "start_date": "2026-10-28",
                "end_date": "2026-10-29",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_rejects_invalid_date_range(self):
        response = self.client.post(
            "/api/v1/weather/assess/",
            {
                "latitude": 30,
                "longitude": 79,
                "start_date": "2026-11-02",
                "end_date": "2026-10-28",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    @patch("weather.services.httpx.get")
    def test_normalizes_provider_response(self, mock_get):
        mock_get.return_value.json.return_value = {
            "latitude": 30,
            "longitude": 79,
            "timezone": "Asia/Kolkata",
            "daily": {
                "time": ["2026-10-28"],
                "temperature_2m_min": [12.0],
                "temperature_2m_max": [22.0],
                "precipitation_probability_max": [10],
                "precipitation_sum": [0.0],
                "snowfall_sum": [0.0],
                "wind_speed_10m_max": [15.0],
            },
        }
        mock_get.return_value.raise_for_status.return_value = None

        result = get_weather(
            30, 79, date(2026, 10, 28), date(2026, 10, 28)
        )

        self.assertEqual(result["source"], "Open-Meteo")
        self.assertEqual(
            result["forecast"][0]["temperature_max_c"], 22.0
        )