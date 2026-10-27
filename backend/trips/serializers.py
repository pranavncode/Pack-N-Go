from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = [
            "id",
            "mode",
            "origin",
            "destination",
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

        if mode == Trip.Mode.FIXED and not destination.strip():
            raise serializers.ValidationError({
                "destination": "Required for fixed-destination trips."
            })

        return attrs