from django.shortcuts import render
from .selectors import event_list_approved


def index(request):
    # keeping it simple as on ground team and organisation accounts should also be able to see what a customer could see right?
    events = event_list_approved()
    return render(request, "events/index.html", {"events": events})
