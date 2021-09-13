import uuid

from django.db import models
# Create your models here.
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel

directIon_choice = (
    ("dr", "Dr"),
    ("cr", "Cr")
)
transaction_type = (
    ('withdrawal', "WITHDRAW"),
    ('wallet_deposit', "WALLET_DEPOSIT"),
    ('wallet_withdraw', "WALLET_WITHDRAW"),
    ("reversal", "REVERSAL")
)


class Transactions(SafeDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.Account', on_delete=models.CASCADE)
    wallet = models.ForeignKey('wallets.Wallet', on_delete=models.CASCADE)
    direction = models.CharField(max_length=10, choices=directIon_choice)
    type = models.CharField(max_length=30, choices=transaction_type)
    currency_code = models.CharField(max_length=10)
    code = models.CharField(max_length=20, null=True, blank=True)
    wallet_balance = models.DecimalField(decimal_places=2, max_digits=20)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        db_table = 'tbl_transactions'
        ordering = ['created_at', 'amount']

