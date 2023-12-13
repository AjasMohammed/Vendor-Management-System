import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from home.models import CustomUser, Vendor, PurchaseOrder


@pytest.fixture
def authenticated_user_client():
    client = APIClient()

    # Create a user for testing
    user = CustomUser.objects.create_user(
        email='testuser@123.com', password='testpassword')

    # Get JWT token for the created user
    access_token = AccessToken.for_user(user)
    token = str(access_token)

    def _get_token():
        return token

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    yield client, _get_token

    # Clean up after the test
    user.delete()


@pytest.fixture
def create_vendor():
    data = {
        "name": "OldMug",
        "vendor_code": "OM",
        "contact_details": "123-456-7890",
        "address": "Trivandrum, Kerala, India"
    }
    vendor = Vendor.objects.create(**data)

    return vendor


@pytest.fixture
def create_purchase_order(create_vendor):
    vendor = create_vendor
    data = {
        "vendor": vendor,
        "delivery_date": "2024-01-20T00:00:00Z",
        "items": [
            {
                "item_name": "Cap",
                "quantity": 4,
                "unit_price": 2400
            },
            {
                "item_name": "T-Shirt",
                "quantity": 5,
                "unit_price": 400
            }
        ],
        "quantity": 9
    }
    purchase_order = PurchaseOrder.objects.create(**data)

    return purchase_order


@pytest.fixture
def updated_purchase_order(create_purchase_order):
    purchase_order = create_purchase_order
    purchase_order.status = 'completed'
    purchase_order.quality_rating = 5.0
    purchase_order.issue_date = "2023-12-30T14:42:34Z"
    purchase_order.save()

    return purchase_order


@pytest.fixture
def acknowledged_purchase_order(updated_purchase_order):
    purchase_order = updated_purchase_order
    purchase_order.acknowledgment_date = "2023-12-31T14:42:34Z"
    purchase_order.save()

    return purchase_order