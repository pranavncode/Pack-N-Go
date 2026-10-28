from django.db import models

# Create your models here.
from django.db import models


class Trip(models.Model):
    class Mode(models.TextChoices):
        FIXED = "fixed", "Fixed destination"
        DISCOVER = "discover", "Discover destinations"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PLANNING = "planning", "Planning"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    mode = models.CharField(max_length=10, choices=Mode.choices)
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200, blank=True)

    start_date = models.DateField()
    end_date = models.DateField()

    travellers = models.PositiveIntegerField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="INR")

    preferences = models.JSONField(default=dict, blank=True)
    transport = models.JSONField(default=dict, blank=True)
    must_visit = models.JSONField(default=list, blank=True)
    constraints = models.JSONField(default=dict, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timezone = models.CharField(max_length=50, blank=True)

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trip {self.pk}: {self.origin} -> {self.destination or 'Undecided'}"