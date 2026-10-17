from .models import Wallet
from users import User


def wallet_create(user: User) -> Wallet:
    wallet = Wallet(user=user)
    wallet.full_clean()
    wallet.save()

    return wallet
