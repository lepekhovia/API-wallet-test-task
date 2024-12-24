import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from core.models import Wallet


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='testuser', password='password')


@pytest.fixture
def wallet(user):
    return Wallet.objects.create(owner=user, balance=Decimal('100.00'))