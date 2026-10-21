from django.contrib import admin

from .models import Event, Slot

class SlotInline(admin.TabularInline):
    model = Slot
    fields = ["label", "starts_at", "ends_at", "price", "capacity", "booked_count"]
    readonly_fields = ["booked_count"]

class EventAdmin(admin.ModelAdmin):
    fields = ["title", "description", "organisation", "event_type", "location", "status"]
    inlines = [SlotInline]

admin.site.register(Event, EventAdmin)