from users.models import User
from .models import Wallet, Transaction
from django.db.models import QuerySet

def wallet_get_for_user(*, user: User) -> Wallet:
    return Wallet.objects.get(user=user)


def transaction_list_for_user(*, user: User) -> QuerySet[Transaction]:
    return Transaction.objects.filter(wallet__user=user).order_by("-created_at")
