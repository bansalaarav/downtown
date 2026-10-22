from .models import Event, Slot, Bookmark
from django.db.models import QuerySet
from django.utils import timezone
from users.models import User


def event_list_approved() -> QuerySet[Event]:
    return Event.objects.filter(status="A").order_by("-created_at")


def slot_list_for_event(*, event: Event) -> QuerySet[Slot]:
    # we only want slots that are future dated. first we order by start time and then by label for viewing consistency
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return Slot.objects.filter(event=event, starts_at__gt=today).order_by("starts_at", "label")


def bookmark_list_for_user(*, user: User) -> QuerySet[Bookmark]:
    return Bookmark.objects.filter(user=user).order_by("-created_at")
