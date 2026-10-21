"""
Seed test organisations, events and slots.

Run from the project root (PowerShell or any shell):
    uv run python manage.py shell -c "exec(open('scripts/seed_events.py', encoding='utf-8').read())"

Safe to run more than once: organisations and events are matched by name/title,
and slots are only created for events that did not exist before.
"""
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from users.models import User, Organisation
from events.models import Event, Slot


def at(days_from_today, hour, minute=0):
    """A timezone-aware datetime N days from today at HH:MM local time."""
    day = timezone.localdate() + timedelta(days=days_from_today)
    return timezone.make_aware(datetime.combine(day, time(hour, minute)))


def slots(days, start_times, duration_minutes, price, capacity, label=""):
    """Build slot specs for every combination of day and start time."""
    specs = []
    for day in days:
        for hour, minute in start_times:
            starts = at(day, hour, minute)
            specs.append({
                "label": label,
                "starts_at": starts,
                "ends_at": starts + timedelta(minutes=duration_minutes),
                "price": Decimal(price),
                "capacity": capacity,
            })
    return specs


def hours(*hs):
    return [(h, 0) for h in hs]


EVENTS = [
    # ---- Slot-based --------------------------------------------------------
    {
        "org": "Smash Sports Arena",
        "title": "Badminton court booking",
        "event_type": "SBE",
        "status": "A",
        "location": "Indiranagar, Bengaluru",
        "description": "Indoor synthetic courts with lighting. Rackets available on request.",
        "slots": (
            slots(range(1, 4), hours(6, 7, 8, 18, 19, 20), 60, "400", 1, label="Court 1")
            + slots(range(1, 4), hours(6, 7, 8, 18, 19, 20), 60, "400", 1, label="Court 2")
        ),
    },
    {
        "org": "Goalpost Turf",
        "title": "5-a-side football turf",
        "event_type": "SBE",
        "status": "A",
        "location": "Jubilee Hills, Hyderabad",
        "description": "Floodlit FIFA-grade artificial turf for 5-a-side games. Bibs provided.",
        "slots": slots(range(1, 4), hours(17, 18, 19, 20, 21), 60, "1200", 1),
    },
    {
        "org": "Cue Club",
        "title": "Pool table booking",
        "event_type": "SBE",
        "status": "A",
        "location": "Sector 29, Gurugram",
        "description": "Three full-size tables. Book a table for an hour, cues and chalk included.",
        "slots": slots(range(1, 3), hours(14, 15, 16, 17, 18, 19, 20, 21), 60, "250", 3),
    },
    {
        "org": "Goalpost Turf",
        "title": "Cricket practice nets",
        "event_type": "SBE",
        "status": "P",  # pending: should NOT appear on the public page
        "location": "Jubilee Hills, Hyderabad",
        "description": "Two bowling-machine nets with coaching on weekends.",
        "slots": slots(range(2, 4), hours(7, 8, 9), 60, "600", 2),
    },

    # ---- Ticket-based ------------------------------------------------------
    {
        "org": "The Loft Collective",
        "title": "Indie Nights: acoustic live set",
        "event_type": "TBE",
        "status": "A",
        "location": "Bandra West, Mumbai",
        "description": "An evening of acoustic sets from three independent artists.",
        "slots": (
            slots([7], [(19, 0)], 180, "799", 200, label="General admission")
            + slots([7], [(19, 0)], 180, "1499", 40, label="Front row")
        ),
    },
    {
        "org": "Laugh Lane Comedy Club",
        "title": "Stand-up comedy open mic",
        "event_type": "TBE",
        "status": "A",
        "location": "Park Street, Kolkata",
        "description": "Ten new comics, five minutes each. Two-drink minimum not included.",
        "slots": slots([3, 10], [(20, 0)], 120, "299", 120),
    },
    {
        "org": "Starlight Cinemas",
        "title": "The Lighthouse Keeper",
        "event_type": "TBE",
        "status": "A",
        "location": "Koramangala, Bengaluru",
        "description": "A slow-burn mystery set on a remote island. 2 hr 20 min.",
        "slots": slots(range(1, 3), [(13, 0), (16, 30), (20, 0)], 150, "250", 150),
    },
    {
        "org": "The Loft Collective",
        "title": "Jazz brunch session",
        "event_type": "TBE",
        "status": "P",  # pending
        "location": "Bandra West, Mumbai",
        "description": "Live jazz trio over a late-morning set.",
        "slots": slots([14], [(11, 0)], 150, "999", 80),
    },
    {
        "org": "Laugh Lane Comedy Club",
        "title": "Roast battle night",
        "event_type": "TBE",
        "status": "R",  # rejected
        "location": "Park Street, Kolkata",
        "description": "Comics roast each other head to head.",
        "slots": slots([12], [(21, 0)], 120, "399", 100),
    },

    # ---- Reservation-based -------------------------------------------------
    {
        "org": "The Courtyard Kitchen",
        "title": "Sunday brunch",
        "event_type": "RBE",
        "status": "A",
        "location": "Koregaon Park, Pune",
        "description": "Garden-side brunch. Reserve a table; pay at the venue.",
        "slots": slots(range(1, 5), [(11, 0), (13, 0)], 90, "0", 40),
    },
    {
        "org": "Skyline Terrace",
        "title": "Rooftop dinner",
        "event_type": "RBE",
        "status": "A",
        "location": "Anna Nagar, Chennai",
        "description": "Set menu on the rooftop. Price is a per-person deposit.",
        "slots": slots(range(1, 6), [(19, 0), (20, 30)], 90, "1500", 30),
    },
]


with transaction.atomic():
    reviewer = User.objects.filter(is_superuser=True).first()
    now = timezone.now()

    created_events = 0
    created_slots = 0

    for spec in EVENTS:
        org, _ = Organisation.objects.get_or_create(name=spec["org"])

        event = Event.objects.filter(organisation=org, title=spec["title"]).first()
        if event is not None:
            continue  # already seeded

        reviewed = spec["status"] in ("A", "R")
        event = Event(
            organisation=org,
            title=spec["title"],
            description=spec["description"],
            event_type=spec["event_type"],
            location=spec["location"],
            status=spec["status"],
            reviewed_by=reviewer if reviewed else None,
            reviewed_at=now if reviewed else None,
        )
        event.full_clean()
        event.save()
        created_events += 1

        for slot_spec in spec["slots"]:
            slot = Slot(event=event, **slot_spec)
            slot.full_clean()
            slot.save()
            created_slots += 1

print(f"Created {created_events} events and {created_slots} slots.")
print(f"Approved events now in the database: {Event.objects.filter(status='A').count()}")