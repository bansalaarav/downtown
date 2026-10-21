from .models import Event, Slot
from users.models import User, Organisation
from common.constants import EVENT_STATUS_A, EVENT_STATUS_P, EVENT_STATUS_R
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils import timezone
from django.db import transaction


def event_create(*, title: str, description: str, organisation: Organisation, event_type: str, location: str) -> Event:
    event = Event(title=title, description=description, organisation=organisation, event_type=event_type, location=location, status=EVENT_STATUS_P)
    event.full_clean()
    event.save()

    return event


@transaction.atomic
def event_review(*, event: Event, reviewer: User, approve: bool) -> Event:
    if reviewer.has_perm("events.review_event"):
        event = Event.objects.select_for_update().get(pk=event.pk)
        # so that db is locked during this review

        if event.status != EVENT_STATUS_P:
            raise ValidationError("This event has already been reviewed.")

        if approve:
            event.status = EVENT_STATUS_A
        else:
            event.status = EVENT_STATUS_R

        event.reviewed_by = reviewer
        event.reviewed_at = timezone.now()
        event.full_clean()
        event.save()

        return event

    else:
        raise PermissionDenied("You don't have permission to review events.")



# TODO: when i start phase 2

def slot_create():
    pass


def bookmark_toggle():
    pass
