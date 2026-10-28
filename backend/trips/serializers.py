
from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    state = serializers.CharField(
        max_length=100,
        write_only=True,
        required=False,
        allow_blank=True,
        default="",
    )

    class Meta:
        model = Trip
        fields = [
            "id",
            "mode",
            "origin",
            "destination",
            "state",
            "start_date",
            "end_date",
            "travellers",
            "budget",
            "currency",
            "preferences",
            "transport",
            "must_visit",
            "constraints",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        validated_data.pop("state", None)
        return super().create(validated_data)

    def validate(self, attrs):
        start = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None),
        )
        end = attrs.get(
            "end_date",
            getattr(self.instance, "end_date", None),
        )

        if start and end and end < start:
            raise serializers.ValidationError({
                "end_date": "End date must be on or after start date."
            })

        mode = attrs.get(
            "mode",
            getattr(self.instance, "mode", None),
        )
        destination = attrs.get(
            "destination",
            getattr(self.instance, "destination", ""),
        )
        state = attrs.get(
            "state",
            "",
        )

        if mode == Trip.Mode.FIXED:
            if not destination.strip():
                raise serializers.ValidationError({
                    "destination": "Required for fixed-destination trips."
                })

            if not state.strip():
                raise serializers.ValidationError({
                    "state": "State is required for Indian destinations."
                })

        return attrs
