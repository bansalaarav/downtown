from .models import Event

def event_list_approved():
    return Event.objects.filter(status="A")
