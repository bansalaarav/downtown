from django.shortcuts import render, redirect
from .selectors import event_list_approved, slot_list_for_event, bookmark_list_for_user
from .services import bookmark_create
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def index(request):
    # keeping it simple as on ground team and organisation accounts should also be able to see what a customer could see right?
    events = event_list_approved()
    bookmarked_event_ids = []
    if request.user.is_authenticated:
        bookmarks = bookmark_list_for_user(user=request.user)
        bookmarked_event_ids = [b.event.pk for b in bookmarks]
    return render(request, "events/index.html", {"events": events, "bookmarked_event_ids": bookmarked_event_ids})


def detail(request, event_pk):
    # though we can access slots in the  itself we need specific info so we use a selector
    event = get_object_or_404(event_list_approved(), pk=event_pk)
    slots = slot_list_for_event(event=event)
    return render(request, "events/detail.html", {"event": event, "slots": slots})


@login_required
def bookmark_list_view(request):
    bookmarks = bookmark_list_for_user(user=request.user)
    return render(request, "events/bookmarks.html", {"bookmarks": bookmarks})


@login_required
def bookmark_delete_view(request, event_pk):
    if request.method == "POST":
        bookmark = get_object_or_404(bookmark_list_for_user(user=request.user), event__pk=event_pk)
        bookmark.delete()
    return redirect("events:index")


@login_required
def bookmark_create_view(request, event_pk):
    if request.method == "POST":
        event = get_object_or_404(event_list_approved(), pk=event_pk)
        bookmark_create(user=request.user, event=event)
    return redirect("events:index")
