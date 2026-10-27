from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Trip
from .serializers import TripSerializer


class TripCreateView(APIView):
    def post(self, request):
        serializer = TripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        trip = serializer.save()

        return Response(
            TripSerializer(trip).data,
            status=status.HTTP_201_CREATED,
        )


class TripDetailView(generics.RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    lookup_field = "pk"