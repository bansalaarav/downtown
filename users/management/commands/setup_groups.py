from django.core.management.base import BaseCommand
from django.db import transaction
from common.constants import ORG_GROUP_NAME, ONGROUND_GROUP_NAME
from django.contrib.auth.models import Group, Permission


ORG_GROUP_PERMISSIONS = ["add_event", "add_slot", "view_event", "view_booking", "change_ticket"]

ONGROUND_GROUP_PERMISSIONS = ["add_organisation", "view_event", "review_event"]
# review_event is the only custom permission (defined in the model)

class Command(BaseCommand):
    help = "Create organisation and on ground group and add permissions"

    # no need for add_arguments as we're not gonna have any arguments na

    @transaction.atomic
    def handle(self, *args, **options):
        org_group, created1 = Group.objects.get_or_create(name=ORG_GROUP_NAME)
        org_perms = [Permission.objects.get(codename=x) for x in ORG_GROUP_PERMISSIONS]
        org_group.permissions.set(org_perms)

        onground_group, created2 = Group.objects.get_or_create(name=ONGROUND_GROUP_NAME)
        onground_perms = [Permission.objects.get(codename=x) for x in ONGROUND_GROUP_PERMISSIONS]
        onground_group.permissions.set(onground_perms)
