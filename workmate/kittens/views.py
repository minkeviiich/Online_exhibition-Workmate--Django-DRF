from rest_framework import generics, status, viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.decorators import action
from django.db.models import Sum, Count

from .models import Breed, CustomUser, Kitten, Rating
from .serializers import BreedSerializer, CustomUserSerializer, KittenSerializer, RatingSerializer


class IsParticipant(BasePermission):
    """
    Проверяет, что пользователь аутентифицирован и имеет роль 'participant'.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'participant'


class IsVisitor(BasePermission):
    """
    Проверяет, что пользователь аутентифицирован и имеет роль 'visitor'.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'visitor'


class RegisterView(generics.CreateAPIView):
    """
    Представление для регистрации новых пользователей.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class BreedViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для управления породами
    Доступен только аутентифицированным пользователям с ролью 'participant'.
    """

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAuthenticated, IsParticipant]


class KittenViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для управления котятами.
    Доступен только аутентифицированным пользователям.
    """

    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['breed']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Создает нового котенка, если пользователь имеет роль 'participant'.
        """

        if self.request.user.role != 'participant':
            return Response(
                {'detail': 'You do not have permission to add kittens.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Обновляет информацию о котенке, если пользователь является его владельцем.
        """

        instance = self.get_object()
        if instance.owner != request.user:
            return Response(
                {'detail': 'You do not have permission to modify this kitten.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет котенка, если пользователь является его владельцем.
        """

        instance = self.get_object()
        if instance.owner != request.user:
            return Response(
                {'detail': 'You do not have permission to delete this kitten.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class RatingViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для управления оценками.
    Доступен только аутентифицированным пользователям.
    """

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Создает новую оценку, если пользователь еще не оценивал данного котенка.
        """

        user = self.request.user
        kitten = serializer.validated_data.get('kitten')
        if Rating.objects.filter(user=user, kitten=kitten).exists():
            raise ValidationError('You have already rated this kitten.')
        serializer.save(user=user)
    
    def update(self, request, *args, **kwargs):
        """
        Обновляет оценку, если пользователь является ее автором.
        """

        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {'detail': 'You do not have permission to modify this reting.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет оценку, если пользователь является ее автором.
        """

        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {'detail': 'You do not have permission to delete this rating.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='kitten-stats/(?P<kitten_id>[^/.]+)')
    def kitten_stats(self, request, kitten_id=None):
        """
        Возвращает статистику оценок для указанного котенка.
        """

        try:
            kitten = Kitten.objects.get(id=kitten_id)
        except Kitten.DoesNotExist:
            return Response({'error': 'Kitten not found'}, status=status.HTTP_404_NOT_FOUND)

        stats = Rating.objects.filter(kitten=kitten).aggregate(
            total_score=Sum('score'),
            rating_count=Count('id')
        )
        return Response(stats)
