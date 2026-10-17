from django.db import transaction
from django.contrib.auth.models import Group

from money.services import wallet_create
from .models import User, Organisation, OrganisationMember, OngroundMember
from common.constants import ORG_GROUP_NAME, ONGROUND_GROUP_NAME


@transaction.atomic # since this is a multistep addition, if wallet creating fails for some reason, user should also not be created
def user_create(*, username: str, email: str, password: str) -> User: # * is to force keyword parameters only
    user = User(username=username, email=email)
    user.set_password(password)
    user.full_clean()
    user.save()

    wallet_create(user=user) # we're creating wallets for org_members too then but we'll just not use them ig

    return user


@transaction.atomic
def onground_member_create(*, user:User) -> OngroundMember:
    onground_member = OngroundMember(user=user)

    Group.objects.get(name=ONGROUND_GROUP_NAME).user_set.add(user)

    return onground_member


@transaction.atomic
def onground_member_onboard(*, username: str, email: str, password: str) -> OngroundMember:
    user = user_create(username=username, email=email, password=password)
    return onground_member_create(user=user)


@transaction.atomic
def org_member_create(*, user: User, organisation: Organisation) -> OrganisationMember:
    org_member = OrganisationMember(user=user, organisation=organisation)
    org_member.full_clean()
    org_member.save()

    Group.objects.get(name=ORG_GROUP_NAME).user_set.add(user)
    
    return org_member


@transaction.atomic
def org_member_onboard(*, username: str, email: str, password: str, organisation: Organisation) -> OrganisationMember:
    user = user_create(username=username, email=email, password=password)
    return org_member_create(user=user, organisation=organisation)


def org_create(*, name: str) -> Organisation:
    org = Organisation(name=name)
    org.full_clean()
    org.save()

    return org
