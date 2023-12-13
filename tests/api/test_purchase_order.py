import pytest
from django.urls import reverse
import datetime
from home.models import PurchaseOrder


# test for Successfull Creation of Purchase Order
@pytest.mark.django_db
def test_create_purchase_order_success(authenticated_user_client, create_vendor):
    client, get_token = authenticated_user_client
    vendor = create_vendor
    payload = {
        "vendor": "OM",
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

    url = reverse("purchase_orders")
    response = client.post(url, payload, format="json")

    data = response.data['data']

    assert response.status_code == 201
    assert data['po_number'] == 1


# test for Failed Creation of Purchase Order
@pytest.mark.django_db
def test_create_purchase_order_fail(authenticated_user_client):
    client, get_token = authenticated_user_client
    payload = {}

    url = reverse("purchase_orders")
    response = client.post(url, payload, format="json")

    assert response.status_code == 400


# test for Retriving all Purchase Order
@pytest.mark.django_db
def test_view_purchase_order(authenticated_user_client, create_purchase_order):
    client, get_token = authenticated_user_client
    purchase_order = create_purchase_order

    url = reverse("purchase_orders")
    response = client.get(url, format="json")

    assert response.status_code == 200


# test for Retriving Specific Purchase Order Successfully
@pytest.mark.django_db
def test_view_specific_purchase_order_success(authenticated_user_client, create_purchase_order):
    client, get_token = authenticated_user_client
    purchase_order = create_purchase_order

    url = reverse("specific_purchase_order", kwargs={'po_id': 1})
    response = client.get(url, format="json")

    assert response.status_code == 200


# test for Retriving Specific Purchase Order Fail
@pytest.mark.django_db
def test_view_specific_purchase_order_fail(authenticated_user_client, create_purchase_order):
    client, get_token = authenticated_user_client
    purchase_order = create_purchase_order

    url = reverse("specific_purchase_order", kwargs={'po_id': 2})
    response = client.get(url, format="json")

    assert response.status_code == 404


# test for Update Specific Purchase Order Success
@pytest.mark.django_db
def test_update_specific_purchase_order_success(authenticated_user_client, create_purchase_order):
    client, get_token = authenticated_user_client
    purchase_order = create_purchase_order

    payload = {
        "status": "completed",
        "quality_rating": 4,
        "issue_date": datetime.datetime.now(datetime.timezone.utc)
    }

    url = reverse("specific_purchase_order", kwargs={
                  'po_id': purchase_order.po_number})
    response = client.put(url, payload, format="json")
    data = response.data['data']

    assert response.status_code == 202
    assert data['status'] == 'completed'
    assert data['quality_rating'] == 4.0
    assert data['issue_date'] != None


# test for Update Specific Purchase Order Fail - Wrong ID
@pytest.mark.django_db
def test_update_specific_purchase_order_fail_1(authenticated_user_client, create_purchase_order):
    client, get_token = authenticated_user_client
    purchase_order = create_purchase_order

    payload = {
        "status": "completed",
        "quality_rating": 4
    }

    url = reverse("specific_purchase_order", kwargs={'po_id': 2})
    response = client.put(url, payload, format="json")

    assert response.status_code == 404


# test for Update Specific Purchase Order Fail - Invalid Data
@pytest.mark.django_db
def test_update_specific_purchase_order_fail_2(authenticated_user_client, create_purchase_order):
    client, get_token = authenticated_user_client
    purchase_order = create_purchase_order
    payload = {}

    url = reverse("specific_purchase_order", kwargs={
                  'po_id': purchase_order.po_number})
    response = client.put(url, payload, format="json")

    assert response.status_code == 400


# test for Delete Specific Purchase Order
@pytest.mark.django_db
def test_delete_specific_purchase_order(authenticated_user_client, create_purchase_order):
    client, get_token = authenticated_user_client
    purchase_order = create_purchase_order

    url = reverse("specific_purchase_order", kwargs={
                  'po_id': purchase_order.po_number})
    response = client.delete(url, format="json")
    check_existance = PurchaseOrder.objects.filter(
        po_number=purchase_order.po_number).first()

    assert response.status_code == 200
    assert check_existance == None


# test for Acknowledge Specific Purchase Order Success
@pytest.mark.django_db
def test_acknowledge_specific_purchase_order_success(authenticated_user_client, updated_purchase_order):
    client, get_token = authenticated_user_client
    purchase_order = updated_purchase_order

    url = reverse("acknowledge_purchase_order", kwargs={
                  'po_id': purchase_order.po_number})
    response = client.post(url, format="json")

    data = response.data['data']

    assert response.status_code == 202
    assert data['acknowledgment_date'] != None


# test for History Performance of Specific Vendor
@pytest.mark.django_db
def test_history_performance_specific_vendor(authenticated_user_client, acknowledged_purchase_order):
    client, get_token = authenticated_user_client
    purchase_order = acknowledged_purchase_order

    url = reverse("vendor_performance", kwargs={'vendor_id': 1})
    response = client.get(url, format="json")

    data = response.data
    print(data)
    print(data['fulfillment_rate'])

    assert response.status_code == 200
    assert data['on_time_delivery_rate'] != None
    assert data['quality_rating_avg'] != None
    assert data['average_response_time'] != None
    assert data['fulfillment_rate'] != None
