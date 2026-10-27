
from django.urls import path
from .views import DestinationSearchView

urlpatterns = [
    path("search/", DestinationSearchView.as_view()),
]
