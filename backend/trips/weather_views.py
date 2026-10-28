
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Trip
from weather.services import get_weather


class TripWeatherView(APIView):
    def get(self, request, pk):
        try:
            trip = Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            return Response(
                {"error": "Trip not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if trip.latitude is None or trip.longitude is None:
            return Response(
                {"error": "Trip destination coordinates are missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            weather = get_weather(
                latitude=trip.latitude,
                longitude=trip.longitude,
                start_date=trip.start_date,
                end_date=trip.end_date,
            )
        except RuntimeError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({
            "trip_id": trip.id,
            "destination": trip.destination,
            "state": getattr(trip, "state", None),
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "weather": weather,
        }, status=status.HTTP_200_OK)
