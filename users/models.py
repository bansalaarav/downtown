from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import BaseModel
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)


# kind of useless but in the future it'll come in useful
# if onground members get additional fields
class OngroundMember(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Organisation(BaseModel):
    name = models.CharField(unique=True, max_length=100)


# profile model so that user doesn't need to have a null organisation field
# also useful if like in the future we need to add some organisation member specific fields
class OrganisationMember(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)
