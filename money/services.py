from .models import Wallet, Transaction
from users.models import User
from decimal import Decimal
from bookings.models import Booking
from django.db import transaction
from django.core.exceptions import ValidationError
from common.constants import TRANS_TYPE_ADD, TRANS_TYPE_PURCHASE


def wallet_create(*, user: User) -> Wallet:
    wallet = Wallet(user=user)
    wallet.full_clean()
    wallet.save()

    return wallet


@transaction.atomic
def wallet_debit(*, user: User, amount: Decimal, booking: Booking) -> Transaction:
    wallet = Wallet.objects.select_for_update().get(user=user)
    if wallet.balance < amount: # our model constraint checks this too just in case
        raise ValidationError("Insufficient balance")
    wallet.balance -= amount
    wallet.full_clean()
    wallet.save()
    
    trans = Transaction(wallet=wallet, trans_type=TRANS_TYPE_PURCHASE, amount=amount, booking=booking)
    trans.full_clean()
    trans.save()

    return trans


@transaction.atomic
def wallet_credit(*, user: User, amount: Decimal) -> Transaction:
    wallet = Wallet.objects.select_for_update().get(user=user)
    wallet.balance += amount
    wallet.full_clean()
    wallet.save()
    
    trans = Transaction(wallet=wallet, trans_type=TRANS_TYPE_ADD, amount=amount)
    trans.full_clean()
    trans.save()

    return trans
