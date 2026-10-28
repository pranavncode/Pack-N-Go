from django.urls import path
from .views import TripCreateView, TripDetailView
from .weather_views import TripWeatherView

urlpatterns = [
    path("", TripCreateView.as_view(), name="trip-create"),
    path("<int:pk>/", TripDetailView.as_view(), name="trip-detail"),
    path("<int:pk>/weather/", TripWeatherView.as_view())
]