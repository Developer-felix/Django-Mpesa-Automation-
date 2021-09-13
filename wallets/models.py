from django.db import models


import uuid

from django.db import models
# Create your models here.
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel


class Wallet(SafeDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.Account', on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=20)
    type = models.CharField(max_length=20)
    status = models.IntegerField(default=1)
    currency_code = models.IntegerField(default="KES")
    created_at = models.DateTimeField(auto_now=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        db_table = "tbl_wallets"
        ordering = ['created_at']
