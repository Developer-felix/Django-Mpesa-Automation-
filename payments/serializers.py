from rest_framework import serializers
from users.models import Account
from users.serializer import AccountLinkedSerializer

from .models import Payments, PaymentMethods


class PaymentMethodSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Account, read_only=False)
    user = AccountLinkedSerializer(required=False, read_only=True)

    class Meta:
        model = PaymentMethods
        fields = (
            "id",
            "name",
            "user",
            "created_at",
            "updated_at",
        )


class OrderPaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Account, read_only=False)
    user = AccountLinkedSerializer(required=False, read_only=True)
    payment_method = serializers.PrimaryKeyRelatedField(queryset=Payments, read_only=False)
    payment_method = PaymentMethodSerializer(required=False, read_only=True)

    class Meta:
        model = Payments
        fields = (
            "id",
            "user",
            "amount",
            "payment_method",
            "payment_receipt_no",
            "payment_reference_id",
            "transaction_status",
            "completed_time",
        )


