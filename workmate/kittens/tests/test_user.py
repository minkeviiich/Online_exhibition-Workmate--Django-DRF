import pytest

from django.urls import reverse

from rest_framework.test import APIClient

from kittens.models import CustomUser

@pytest.mark.django_db
def test_custom_user_factory_visitor(custom_user_factory):
    user = custom_user_factory(role='visitor')
    assert user.role == 'visitor'

@pytest.mark.django_db
def test_custom_user_factory_participant(custom_user_factory):
    user = custom_user_factory(role='participant')
    assert user.role == 'participant'

@pytest.mark.django_db
def test_create_user():
    client = APIClient()
    url = reverse('register')
    data = {
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@example.com',
        'password': 'testpassword',
        'role': 'visitor'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    user = CustomUser.objects.get(username='testuser')
    assert user.email == 'testuser@example.com'
    assert user.check_password('testpassword')
    assert user.role == 'visitor'
