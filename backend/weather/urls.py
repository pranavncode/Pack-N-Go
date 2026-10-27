
from django.urls import path
from .views import WeatherAssessView

urlpatterns = [
    path("assess/", WeatherAssessView.as_view(), name="weather-assess"),
]