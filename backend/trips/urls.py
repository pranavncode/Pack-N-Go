from django.urls import path
from .views import TripPreviewView

urlpatterns = [
    path("preview/", TripPreviewView.as_view(), name="trip-preview"),
]