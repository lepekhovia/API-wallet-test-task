from asgiref.sync import sync_to_async
from django.db import transaction
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from core.models import Wallet
from ..serializer import WalletSerializer, WalletSerializerForPatch
from ..permissions import IsOwner


class WalletOperationView(GenericAPIView):
    serializer_class = WalletSerializer
    serializer_class_for_patch = WalletSerializerForPatch
    permission_classes = [IsOwner]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return self.serializer_class_for_patch
        return self.serializer_class

    async def post(self, request, wallet_uuid: str):
        serializer = await sync_to_async(self.get_serializer)(data=request.data)
        if not await sync_to_async(serializer.is_valid)():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            with transaction.atomic():
                try:
                    wallet = await Wallet.objects.select_for_update().aget(id=wallet_uuid)
                except Wallet.DoesNotExist:
                    transaction.rollback()
                    return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)
                if data['operationType'] == Wallet.WITHDRAW and wallet.balance < data['amount']:
                    transaction.rollback()
                    return Response({"error": "Insufficient funds."}, status=status.HTTP_403_FORBIDDEN)
                await wallet.change_balance(data['amount'], data['operationType'])

        except Exception:
            # TODO: подключить редис и отправлять сообщение в очередь
            return Response({"error": "Error processing transaction."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "success", "balance": wallet.balance}, status=status.HTTP_200_OK)


class BalanceView(GenericAPIView, RetrieveModelMixin):
    serializer_class = WalletSerializer

    def get_object(self):
        return Wallet.objects.filter(id=self.kwargs['wallet_uuid'], owner=self.request.user).first()
