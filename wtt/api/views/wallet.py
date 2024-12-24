from asgiref.sync import sync_to_async
from django.db import transaction, DatabaseError
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from tenacity import retry, stop_after_attempt, wait_fixed

from core.models import Wallet
from ..serializer import WalletSerializer, WalletSerializerForPatch
from ..permissions import IsOwner


class WalletOperationView(GenericAPIView):
    serializer_class = WalletSerializerForPatch
    permission_classes = [IsOwner]

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(0.1))
    async def handle_transaction(self, wallet_uuid: str, data: dict) -> dict:
        async with transaction.atomic():
            wallet = await Wallet.objects.select_for_update().aget(id=wallet_uuid)

            if data['operationType'] == Wallet.WITHDRAW and wallet.balance < data['amount']:
                return {"error": "Insufficient funds.", "status": status.HTTP_403_FORBIDDEN}

            await wallet.change_balance(data['amount'], data['operationType'])

            return {"status": "success", "balance": wallet.balance, "status_code": status.HTTP_200_OK}

    async def post(self, request, wallet_uuid: str) -> Response:
        serializer = await sync_to_async(self.get_serializer)(data=request.data)
        if not await sync_to_async(serializer.is_valid)():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            result = await self.handle_transaction(wallet_uuid, data)
            if "error" in result:
                return Response({"error": result["error"]}, status=result["status"])
            return Response({"status": result["status"], "balance": result["balance"]}, status=result["status_code"])
        except DatabaseError:
            return Response({"error": "Internal error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            return Response({"error": "Internal error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BalanceView(GenericAPIView, RetrieveModelMixin):
    serializer_class = WalletSerializer

    def get_object(self):
        return Wallet.objects.filter(id=self.kwargs['wallet_uuid'], owner=self.request.user).first()
