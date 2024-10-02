import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from kittens.models import Rating
from .factories  import RatingFactory, KittenFactory, CustomUserFactory

@pytest.mark.django_db
class TestRatingViewSet:
    """Тесты для RatingViewSet."""

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

    def test_list_ratings(self, auth_client):
        """
        Проверяет, что запрос на получение списка рейтингов
        возвращает статус 200.
        """

        RatingFactory.create_batch(3)
        url = reverse('rating-list')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_rating(self, auth_client):
        """Проверяет, что рейтинг успешно создается."""

        kitten = KittenFactory()
        url = reverse('rating-list')
        data = {
            'score': 5,
            'comment': 'Great kitten!',
            'kitten': kitten.id
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Rating.objects.count() == 1
        assert Rating.objects.get().score == 5

    def test_create_rating_unauthorized(self, api_client):
        """
        Проверяет, что неавторизованный пользователь не может
        создать рейтинг.
        """

        kitten = KittenFactory()
        url = reverse('rating-list')
        data = {
            'score': 5,
            'comment': 'Great kitten!',
            'kitten': kitten.id
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
 
    def test_retrieve_rating(self, auth_client):
        """
        Проверяет, что запрос на получение конкретного рейтинга
        возвращает статус 200
        """

        rating = RatingFactory()
        url = reverse('rating-detail', args=[rating.id])
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['score'] == rating.score

    def test_update_rating(self, auth_client):
        """Проверяет, что владелец рейтинга может его обновить."""

        rating = RatingFactory(user=auth_client.handler._force_user)
        url = reverse('rating-detail', args=[rating.id])
        data = {
            'score': 4,
            'comment': 'Updated comment',
            'kitten': rating.kitten.id
        }
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        rating.refresh_from_db()
        assert rating.score == 4
        assert rating.comment == 'Updated comment'

    def test_update_rating_unauthorized(self, auth_client):
        """
        Проверяет, что пользователь, не являющийся владельцем рейтинга,
        не может его обновить.
        """

        rating = RatingFactory()
        url = reverse('rating-detail', args=[rating.id])
        data = {
            'score': 4,
            'comment': 'Updated comment',
            'kitten': rating.kitten.id
        }
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_rating(self, auth_client):
        """Проверяет, что владелец рейтинга может его удалить."""

        rating = RatingFactory(user=auth_client.handler._force_user)
        url = reverse('rating-detail', args=[rating.id])
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Rating.objects.count() == 0

    def test_delete_rating_unauthorized(self, auth_client):
        """
        Проверяет, что пользователь, не являющийся владельцем рейтинга,
        не может его удалить
        """

        rating = RatingFactory()
        url = reverse('rating-detail', args=[rating.id])
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_cannot_rate_kitten_multiple_times(self, auth_client):
        """
        Проверяет, что пользователь не может оставить несколько оценок для
        одного котенка
        """
        kitten = KittenFactory()
        url = reverse('rating-list')
        data = {
            'score': 5,
            'comment': 'Great kitten!',
            'kitten': kitten.id
        }

        # Создаем первую оценку
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Rating.objects.count() == 1

        # Пытаемся создать вторую оценку для того же котенка
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert any('You have already rated this kitten.' in str(error) for error in response.data)
        assert Rating.objects.count() == 1
