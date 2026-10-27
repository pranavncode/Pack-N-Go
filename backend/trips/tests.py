from django.test import TestCase

# Create your tests here.
from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Trip


class TripAPITests(APITestCase):
    def setUp(self):
        self.payload = {
            "mode": "discover",
            "origin": "Dehradun, India",
            "destination": "",
            "start_date": "2026-12-10",
            "end_date": "2026-12-13",
            "travellers": 2,
            "budget": "8000.00",
            "currency": "INR",
            "preferences": {"snow": 0.9},
            "transport": {"personal_vehicle": False},
            "must_visit": [],
            "constraints": {},
        }

    def test_create_trip(self):
        response = self.client.post(
            reverse("trip-create"),
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trip.objects.count(), 1)
        self.assertEqual(response.data["status"], "draft")

    def test_reject_invalid_dates(self):
        self.payload["end_date"] = "2026-12-01"

        response = self.client.post(
            reverse("trip-create"),
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Trip.objects.count(), 0)

    def test_retrieve_trip(self):
        trip = Trip.objects.create(
            mode="discover",
            origin="Dehradun, India",
            start_date=date(2026, 12, 10),
            end_date=date(2026, 12, 13),
            travellers=2,
            budget="8000.00",
        )

        response = self.client.get(
            reverse("trip-detail", kwargs={"pk": trip.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], trip.pk)