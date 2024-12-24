import pytest
from decimal import Decimal
from rest_framework import status


@pytest.mark.django_db
def test_wallet_balance_retrieve(api_client, user, wallet):
    api_client.force_authenticate(user=user)
    url = f'/api/v1/wallets/{wallet.id}'

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == str(wallet.id)
    assert Decimal(response.data['balance']) == wallet.balance


@pytest.mark.django_db
def test_wallet_operation_withdraw_success(api_client, user, wallet):
    api_client.force_authenticate(user=user)
    url = f'/api/v1/wallets/{wallet.id}/operation'

    data = {
        "operationType": "withdraw",
        "amount": "50.00"
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'success'
    wallet.refresh_from_db()
    assert wallet.balance == Decimal('50.00')


@pytest.mark.django_db
def test_wallet_operation_withdraw_insufficient_funds(api_client, user, wallet):
    api_client.force_authenticate(user=user)
    url = f'/api/v1/wallets/{wallet.id}/operation'

    data = {
        "operationType": "withdraw",
        "amount": "150.00"
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['error'] == 'Insufficient funds.'
    wallet.refresh_from_db()
    assert wallet.balance == Decimal('100.00')


@pytest.mark.django_db
def test_wallet_operation_deposit_success(api_client, user, wallet):
    api_client.force_authenticate(user=user)
    url = f'/api/v1/wallets/{wallet.id}/operation'

    data = {
        "operationType": "deposit",
        "amount": "50.00"
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'success'
    wallet.refresh_from_db()
    assert wallet.balance == Decimal('150.00')


@pytest.mark.django_db
def test_wallet_operation_unauthorized(api_client, wallet):
    url = f'/api/v1/wallets/{wallet.id}/operation'

    data = {
        "operationType": "deposit",
        "amount": "50.00"
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
