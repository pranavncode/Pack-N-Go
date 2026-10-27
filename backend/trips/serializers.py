from rest_framework import serializers

class TripRequestSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(
        choices=["fixed", "discover"]
    )
    origin = serializers.CharField(max_length=200)

    destination = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        default="",
    )

    start_date = serializers.DateField()
    end_date = serializers.DateField()

    travellers = serializers.IntegerField(min_value=1)
    budget = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
    )

    currency = serializers.ChoiceField(
        choices=["INR"],
        default="INR",
    )

    preferences = serializers.DictField(
        required=False,
        default=dict,
    )

    def validate(self, attrs):
        if attrs["end_date"] < attrs["start_date"]:
            raise serializers.ValidationError(
                {"end_date": "End date must be on or after start date."}
            )

        if attrs["mode"] == "fixed" and not attrs.get("destination"):
            raise serializers.ValidationError(
                {"destination": "Required for fixed-destination trips."}
            )

        return attrs