from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, OrganisationMember, Organisation


# note that we're using UserAdmin as that's what it says to use in the django docs for custom users
class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ["email"]}),)


admin.site.register(User, CustomUserAdmin)
admin.site.register(OrganisationMember)
admin.site.register(Organisation)
