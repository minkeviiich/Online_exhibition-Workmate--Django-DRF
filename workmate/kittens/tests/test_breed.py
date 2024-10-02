import pytest

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .factories import BreedFactory, CustomUserFactory
from kittens.models import Breed

@pytest.mark.django_db
class TestBreedViewSet:
    """Тесты для BreedViewSet."""

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return CustomUserFactory(role='participant')

    @pytest.fixture
    def auth_client(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client

    def test_list_breeds(self, auth_client):
        """Проверяет, запрос на получение списка пород."""

        BreedFactory.create_batch(3)
        url = reverse('breed-list')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_breed(self, auth_client):
        """Проверяет, что порода успешно создается."""

        url = reverse('breed-list')
        data = {'name': 'Siamese'}
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Breed.objects.count() == 1
        assert Breed.objects.get().name == 'Siamese'

    def test_retrieve_breed(self, auth_client):
        """
        Проверяет, что запрос на получение конкретной породы 
        возвращает статус 200.
        """

        breed = BreedFactory()
        url = reverse('breed-detail', args=[breed.id])
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == breed.name

    def test_update_breed(self, auth_client):
        """Проверяет, что порода успешно обновляется."""

        breed = BreedFactory()
        url = reverse('breed-detail', args=[breed.id])
        data = {'name': 'Updated Breed'}
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        breed.refresh_from_db()
        assert breed.name == 'Updated Breed'

    def test_delete_breed(self, auth_client):
        """Проверяет, что порода успешно удаляется."""

        breed = BreedFactory()
        url = reverse('breed-detail', args=[breed.id])
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Breed.objects.count() == 0
