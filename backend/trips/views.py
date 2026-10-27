from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import TripRequestSerializer


class TripPreviewView(APIView):
    def post(self, request):
        serializer = TripRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        trip = serializer.validated_data

        return Response(
            {
                "status": "success",
                "message": "Trip request validated successfully.",
                "trip": {
                    **trip,
                    "budget": str(trip["budget"]),
                    "start_date": trip["start_date"].isoformat(),
                    "end_date": trip["end_date"].isoformat(),
                },
            },
            status=status.HTTP_200_OK,
        )