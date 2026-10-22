from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.index, name="index"),
    path("events/<int:event_pk>/", views.detail, name="detail"),
    path("bookmarks/", views.bookmark_list_view, name="bookmarks"),
    path("events/<int:event_pk>/bookmark", views.bookmark_create_view, name="bookmark_create"),
    path("events/<int:event_pk>/unbookmark", views.bookmark_delete_view, name="bookmark_delete")
]