import uuid
from django.db import models
# Create your models here.
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel


class PaymentMethods(SafeDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey('users.Account', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        db_table = 'tbl_payment_methods'
        ordering = ['created_at', ]


class Payments(SafeDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.Account', on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    payment_receipt_no = models.CharField(max_length=50, blank=True, null=True)
    payment_reference_id = models.UUIDField(max_length=100,null=True, blank=True)
    transaction_status = models.CharField(blank=True, null=True, max_length=100)
    completed_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        db_table = 'tbl_payments'
        ordering = ['created_at', 'amount']


class MpesaPayments(SafeDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.Account', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    phone_no = models.CharField(max_length=50)
    merchant_request_id = models.CharField(max_length=200, blank=True, null=True)
    conversation_id = models.CharField(max_length=200, blank=True, null=True)
    originator_conversation_id = models.CharField(max_length=200, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=200, blank=True, null=True)
    transaction_time = models.DateTimeField(auto_now_add=True)
    mpesa_code = models.CharField(max_length=50, blank=True, null=True)
    response_code = models.CharField(max_length=50, blank=True, null=True)
    order_id = models.UUIDField(max_length=200, null=True, blank=True)
    transaction_status = models.CharField(blank=True, null=True, max_length=100)
    completed_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(blank=True, null=True, max_length=100)
    response_description = models.CharField(blank=True, null=True, max_length=100)
    transaction_type = models.CharField(blank=True, null=True, max_length=50)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        db_table = 'tbl_mpesa_payments'
        ordering = ['created_at', 'amount']
