import pytest
from django.urls import reverse
from home.models import Vendor

# Test when the Vendor is created Successfully


@pytest.mark.django_db
def test_create_vendor_success(authenticated_user_client):
    client, get_token = authenticated_user_client

    url = reverse('vendor_view')
    payload = {
        "name": "OldMug",
        "vendor_code": "OM",
        "contact_details": "123-456-7890",
        "address": "Trivandrum, Kerala, India"
    }
    response = client.post(url, payload, format="json")
    data = response.data

    assert response.status_code == 201
    assert data['data'] == {
        'vendor_id': 1,
        "name": "OldMug",
        "vendor_code": "OM",
        "contact_details": "123-456-7890",
        "address": "Trivandrum, Kerala, India"
    }


# Test when the Vendor data is not provided
@pytest.mark.django_db
def test_create_vendor_fail(authenticated_user_client):
    client, get_token = authenticated_user_client

    url = reverse('vendor_view')
    payload = {}
    response = client.post(url, payload)

    assert response.status_code == 400


# Test for Viewing all Vendors
@pytest.mark.django_db
def test_view_vendor_success(authenticated_user_client, create_vendor):
    client, get_token = authenticated_user_client
    vendor = create_vendor

    url = reverse('vendor_view')
    response = client.get(url)
    data = response.data[0]

    assert response.status_code == 200
    assert data['vendor_id'] == vendor.vendor_id
    assert data['name'] == vendor.name


# Test for Viewing a specific Vendor
@pytest.mark.django_db
def test_view_specific_vendor_success(authenticated_user_client, create_vendor):
    client, get_token = authenticated_user_client
    vendor = create_vendor

    url = reverse('specific_vendor_view', kwargs={
                  'vendor_id': vendor.vendor_id})
    response = client.get(url)
    data = response.data

    assert response.status_code == 200
    assert data['vendor_id'] == vendor.vendor_id
    assert data['name'] == vendor.name


@pytest.mark.django_db
def test_view_specific_vendor_fail(authenticated_user_client):
    client, get_token = authenticated_user_client

    url = reverse('specific_vendor_view', kwargs={
                  'vendor_id': 2})
    response = client.get(url)

    assert response.status_code == 404


# Test for Editing a specific Vendor Success
@pytest.mark.django_db
def test_edit_specific_vendor_success(authenticated_user_client, create_vendor):
    client, get_token = authenticated_user_client
    vendor = create_vendor
    payload = {
        "contact_details": 'oldmug@123.com'
    }
    url = reverse('specific_vendor_view', kwargs={
                  'vendor_id': vendor.vendor_id})
    response = client.put(url, payload, format='json')
    data = response.data['data']

    assert response.status_code == 202
    assert data['vendor_id'] == vendor.vendor_id
    assert data['contact_details'] == payload['contact_details']


# Test for Editing a specific Vendor Fail - Wrong ID
@pytest.mark.django_db
def test_edit_specific_vendor_fail_1(authenticated_user_client):
    client, get_token = authenticated_user_client
    payload = {
        "contact_details": 'oldmug@123.com'
    }
    url = reverse('specific_vendor_view', kwargs={
                  'vendor_id': 2})
    response = client.put(url, payload, format='json')

    assert response.status_code == 404


# Test for Editing a specific Vendor Fail - Invaild Data
@pytest.mark.django_db
def test_edit_specific_vendor_fail_2(authenticated_user_client, create_vendor):
    client, get_token = authenticated_user_client
    vendor = create_vendor
    payload = {}
    url = reverse('specific_vendor_view', kwargs={
                  'vendor_id': vendor.vendor_id})
    response = client.put(url, payload, format='json')

    assert response.status_code == 400


# Test for Deleting a specific Vendor
@pytest.mark.django_db
def test_delete_vendor_success(authenticated_user_client, create_vendor):
    client, get_token = authenticated_user_client
    vendor = create_vendor

    url = reverse('specific_vendor_view', kwargs={
                  'vendor_id': vendor.vendor_id})
    response = client.delete(url, format='json')
    check_existance = Vendor.objects.filter(vendor_id=vendor.vendor_id).first()

    assert response.status_code == 200
    assert check_existance == None
