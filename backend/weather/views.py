from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import WeatherRequestSerializer
from .services import get_weather


class WeatherAssessView(APIView):
    def post(self, request):
        serializer = WeatherRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            result = get_weather(
                latitude=data["latitude"],
                longitude=data["longitude"],
                start_date=data["start_date"],
                end_date=data["end_date"],
            )

        except RuntimeError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(result, status=status.HTTP_200_OK)