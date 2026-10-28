from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Trip
from .serializers import TripSerializer
from places.services import search_destinations

class TripDetailView(generics.RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    lookup_field = "pk"


class TripCreateView(APIView):
    def post(self, request):
        serializer = TripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        place = data["destination"]
        state = data["state"]

        # Step 1: Resolve the destination before saving the trip.
        try:
            results = search_destinations(
                place=place,
                state=state,
            )
        except RuntimeError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # Step 2: Do not save trips with unresolved coordinates.
        if not results:
            return Response(
                {"error": "No matching destination found in India."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(results) != 1:
            return Response(
                {
                    "error": "Destination is ambiguous. Select a specific location.",
                    "results": results,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        selected = results[0]

        # Step 3: Save the trip with the resolved coordinates.
        trip = serializer.save(
            latitude=selected["latitude"],
            longitude=selected["longitude"],
            timezone=selected.get("timezone") or "",
        )

        # Step 4: Return the saved trip.
        return Response(
            TripSerializer(trip).data,
            status=status.HTTP_201_CREATED,
        )
