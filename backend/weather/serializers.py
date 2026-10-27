from rest_framework import serializers


class WeatherRequestSerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, attrs):
        if attrs["end_date"] < attrs["start_date"]:
            raise serializers.ValidationError({
                "end_date": "End date must be on or after start date."
            })

        if (attrs["end_date"] - attrs["start_date"]).days > 15:
            raise serializers.ValidationError({
                "end_date": "Maximum requested range is 16 calendar days."
            })

        return attrs
    