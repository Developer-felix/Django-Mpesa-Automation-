from .models import Wallet


def increment_balance(wallet_id, amount) -> bool:
    wallet = Wallet.objects.get(id=wallet_id)
    wallet.balance += float(amount)
    return wallet.save()


def decrement_balance(wallet_id, amount) -> bool:
    wallet = Wallet.objects.get(id=wallet_id)
    wallet.balance -= float(amount)
    return wallet.save()
