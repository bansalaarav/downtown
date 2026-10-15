from django.db import models
from common.models import BaseModel
from django.conf import settings
import uuid


class Booking(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    slot = models.ForeignKey("events.Slot", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="unit_price_non_negative",
                condition=models.Q(unit_price__gte=0)
            ),
            models.CheckConstraint(
                name="total_amount_non_negative",
                condition=models.Q(total_amount__gte=0)
            ),
            models.CheckConstraint(
                name="quantity_non_zero", # positive integer field could be zero too which doesn't make sense for quantity field
                condition=models.Q(quantity__gt=0)
            )
        ]
  

class Ticket(BaseModel):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    unique_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    consumed_at = models.DateTimeField(null=True, blank=True)
