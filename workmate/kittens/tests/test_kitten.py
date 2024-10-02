import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .factories import BreedFactory, CustomUserFactory, KittenFactory
from kittens.models import Kitten

@pytest.mark.django_db
class TestKittenViewSet:
    """Тесты для KittenViewSet."""

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

    def test_list_kittens(self, auth_client):
        """
        Проверяет, что запрос на получение списка котят 
        возвращает статус 200.
        """

        KittenFactory.create_batch(3)
        url = reverse('kitten-list')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_kitten(self, auth_client):
        """ Проверяет, что котенок успешно создается."""

        breed = BreedFactory()
        url = reverse('kitten-list')
        data = {
            'color': 'Black',
            'name': 'Whiskers',
            'age': 2,
            'description': 'A playful kitten',
            'breed': breed.id
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Kitten.objects.count() == 1
        assert Kitten.objects.get().name == 'Whiskers'

    def test_create_kitten_unauthorized(self, api_client):
        """
        Проверяет, что неавторизованный пользователь не может 
        создать котенка.
        """

        breed = BreedFactory()
        url = reverse('kitten-list')
        data = {
            'color': 'Black',
            'name': 'Whiskers',
            'age': 2,
            'description': 'A playful kitten',
            'breed': breed.id
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_kitten(self, auth_client):
        """
        Проверяет, что запрос на получение конкретного котенка 
        возвращает статус 200.
        """

        kitten = KittenFactory()
        url = reverse('kitten-detail', args=[kitten.id])
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == kitten.name

    def test_update_kitten(self, auth_client):
        """Проверяет, что владелец котенка может его обновить."""

        kitten = KittenFactory(owner=auth_client.handler._force_user)
        url = reverse('kitten-detail', args=[kitten.id])
        data = {
            'color': kitten.color,
            'name': 'Updated Kitten',
            'age': kitten.age,
            'description': kitten.description,
            'breed': kitten.breed.id
        }
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        kitten.refresh_from_db()
        assert kitten.name == 'Updated Kitten'

    def test_update_kitten_unauthorized(self, auth_client):
        """
        Проверяет, что пользователь, не являющийся владельцем котенка,
        не может его обновить.
        """

        kitten = KittenFactory()
        url = reverse('kitten-detail', args=[kitten.id])
        data = {'name': 'Updated Kitten'}
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_kitten(self, auth_client):
        """Проверяет, что владелец котенка может его удалить."""

        kitten = KittenFactory(owner=auth_client.handler._force_user)
        url = reverse('kitten-detail', args=[kitten.id])
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Kitten.objects.count() == 0

    def test_delete_kitten_unauthorized(self, auth_client):
        
        """Проверяет, что пользователь, не являющийся владельцем котенка,
        не может его удалить.
        """

        kitten = KittenFactory()
        url = reverse('kitten-detail', args=[kitten.id])
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
