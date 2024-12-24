from django.urls import path

from .views.wallet import WalletOperationView, BalanceView


urlpatterns = [
    path('api/v1/wallets/<uuid:wallet_uuid>/operation', WalletOperationView.as_view(), name='wallet-operation'),
    path('api/v1/wallets/<uuid:wallet_uuid>', BalanceView.as_view(), name='wallet-retrieve'),
]
