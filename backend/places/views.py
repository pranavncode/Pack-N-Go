
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import DestinationSearchSerializer
from .services import search_destinations


class DestinationSearchView(APIView):
    def post(self, request):
        serializer = DestinationSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            results = search_destinations(
                place=data["place"],
                state=data["state"],
            )
        except RuntimeError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {
                "query": {
                    "place": data["place"],
                    "state": data["state"],
                    "country": "India",
                },
                "results": results,
            },
            status=status.HTTP_200_OK,
        )
