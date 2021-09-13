# Create your views here.
from wallets.models import Wallet
from wallets.views import decrement_balance, increment_balance

from .models import Transactions


def create_transaction(wallet_id, code, trans_type, amount, new_balance, direction, description,
                       currency_code='KES', user_id=None):
    transaction = Transactions.objects.create(
        user_id=user_id,
        wallet_id=wallet_id,
        direction=direction,
        type=trans_type,
        currency=currency_code,
        code=code,
        amount=amount,
        description=description,
        wallet_balance=new_balance
    )
    return transaction


def credit(wallet_id, code, trans_type, amount, description, currency_code='KES',
           user_id=None) -> bool:
    recorded = False
    # update wallet amount
    wallet = Wallet.objects.get(id=wallet_id)
    new_balance = float(wallet.balance) - float(amount)
    # remove amount from wallet
    if decrement_balance(wallet_id, amount):
        transaction = create_transaction(wallet_id, code, trans_type, amount, new_balance, "Cr", description,
                                         currency_code, user_id)
        if transaction:
            recorded = True
        else:
            # if fails return amount
            increment_balance(wallet_id, amount)
    return recorded


def debit(wallet_id, code, trans_type, amount, description, currency_code='KES',
          user_id=None) -> bool:
    recorded = False
    # update wallet amount
    wallet = Wallet.objects.get(id=wallet_id)
    new_balance = float(wallet.balance) + float(amount)
    # remove amount from wallet
    if increment_balance(wallet_id, amount):
        transaction = create_transaction(wallet_id, code, trans_type, amount, new_balance, "Cr", description,
                                         currency_code, user_id)
        if transaction:
            recorded = True
        else:
            # if fails return amount
            decrement_balance(wallet_id, amount)
    return recorded
