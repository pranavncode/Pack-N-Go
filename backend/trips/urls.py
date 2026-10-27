from django.urls import path
from .views import TripCreateView, TripDetailView

urlpatterns = [
    path("", TripCreateView.as_view(), name="trip-create"),
    path("<int:pk>/", TripDetailView.as_view(), name="trip-detail"),
]