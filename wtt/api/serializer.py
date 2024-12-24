from random import choice

from rest_framework import serializers

from core.models import Wallet


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['id', 'balance']
        read_only_fields = ['id', 'balance']


class WalletSerializerForPatch(serializers.ModelSerializer):
    operationType = serializers.ChoiceField(source='operation_type', choices=Wallet.OPERATION_TYPE_CHOICES, required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Wallet
        fields = ['operationType', 'amount']
        read_only_fields = ['operationType']
