from rest_framework import serializers
from users.models import Account

class AccountLinkedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Account