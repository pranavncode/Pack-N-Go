
from rest_framework import serializers


class DestinationSearchSerializer(serializers.Serializer):
    place = serializers.CharField(max_length=100, trim_whitespace=True)
    state = serializers.CharField(max_length=100, trim_whitespace=True)
    country = serializers.CharField(
        max_length=50,
        default="India",
        required=False,
    )

    def validate(self, attrs):
        if attrs["country"].strip().casefold() != "india":
            raise serializers.ValidationError({
                "country": "Currently, only destinations in India are supported."
            })

        attrs["country"] = "India"
        return attrs
