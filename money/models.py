from django.db import models
from common.models import BaseModel
from django.conf import settings
from decimal import Decimal
from common.constants import TRANS_TYPE_ADD, TRANS_TYPE_PURCHASE


class Wallet(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="wallet_balance_is_non_negative",
                condition=models.Q(balance__gte=0)
            )
        ]


class Transaction(BaseModel):
    TRANS_TYPE_CHOICES = [
        (TRANS_TYPE_ADD, "Add"),
        (TRANS_TYPE_PURCHASE, "Purchase")
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    trans_type = models.CharField(max_length=1, choices=TRANS_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # a good test to implement later would be to check if the total of all transaction amounts is equal to wallet balance
    booking = models.OneToOneField("bookings.Booking", on_delete=models.PROTECT, null=True, blank=True) # you can't delete a booking if a transaction already exists - could change later if we decide to implement refund flow
    # booking has null=True because an add type transaction will ofc have no associated booking

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="transaction_amount_is_non_negative", # might be a free event too however we should count that as a transaction
                condition=models.Q(amount__gte=0)
            ),
            models.CheckConstraint( # booking is non-null only if trans_type is not 'add' and vice versa
                name="booking_is_null_when_trans_type_is_add_and_vice_versa",
                condition=(
                    ~models.Q(trans_type="A", booking__isnull=True) | models.Q(trans_type="A")
                )
            )
        ]
