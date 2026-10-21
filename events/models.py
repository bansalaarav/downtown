from django.db import models
from common.models import BaseModel
from django.conf import settings
from common.constants import EVENT_STATUS_A, EVENT_STATUS_P, EVENT_STATUS_R


class Event(BaseModel):
    EVENT_TYPE_CHOICES = [
        ("SBE", "Slot-based"),
        ("TBE", "Ticket-based"),
        ("RBE", "Reservation-based")
    ]

    STATUS_CHOICES = [
        (EVENT_STATUS_P, "Pending"),
        (EVENT_STATUS_A, "Approved"),
        (EVENT_STATUS_R, "Rejected")
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    organisation = models.ForeignKey("users.Organisation", on_delete=models.PROTECT)
    event_type = models.CharField(max_length=3, choices=EVENT_TYPE_CHOICES)
    location = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=EVENT_STATUS_P)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True) # to show on on-ground team's dashboard
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ("review_event", "Can review events by changing the status field")
        ]


class Slot(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, blank=True) # for eg there could be a VIP tier for concert ticket. however blank=True because no such thing for like court booking
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    booked_count = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="slot_starts_at_before_ends_at",
                condition=models.Q(starts_at__lt=models.F("ends_at"))
            ),
            models.CheckConstraint(
                name="slot_booked_count_lte_capacity",
                condition=models.Q(booked_count__lte=models.F("capacity"))
            ),
            models.CheckConstraint(
                name="slot_price_is_non_negative",
                condition=models.Q(price__gte=0)
            )
        ]


class Bookmark(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint( # same user cannot bookmark the event more than once
                name="bookmark_unique_user_event",
                fields=["user", "event"]
            )
        ]
