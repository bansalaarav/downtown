from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import BaseModel
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Organisation(BaseModel):
    name = models.CharField(unique=True, max_length=100)


class OrganisationMember(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)
