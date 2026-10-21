from django.shortcuts import render
from .services import wallet_credit
from .selectors import wallet_get_for_user, transaction_list_for_user
from django.contrib.auth.decorators import login_required
from decimal import Decimal


@login_required
def wallet(request):
    if request.method == "POST":
        amount = Decimal(request.POST.get("amount"))
        wallet_credit(user=request.user, amount=amount)

    wallet = wallet_get_for_user(user=request.user)
    transactions = transaction_list_for_user(user=request.user)

        
    return render(request, "money/wallet.html", {"wallet": wallet, "transactions": transactions})
