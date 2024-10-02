from rest_framework import generics, status, viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from django.db.models import Sum, Count

from .models import Breed, CustomUser, Kitten, Rating
from .serializers import BreedSerializer, CustomUserSerializer, KittenSerializer, RatingSerializer


class IsParticipant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'participant'


class IsVisitor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'visitor'


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAuthenticated, IsParticipant]


class KittenViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['breed']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'participant':
            return Response(
                {'detail': 'You do not have permission to add kittens.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response(
                {'detail': 'You do not have permission to modify this kitten.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response(
                {'detail': 'You do not have permission to delete this kitten.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        kitten = serializer.validated_data.get('kitten')
        if Rating.objects.filter(user=user, kitten=kitten).exists():
            raise ValidationError('You have already rated this kitten.')
        serializer.save(user=user)
    
    @action(detail=False, methods=['get'], url_path='kitten-stats/(?P<kitten_id>[^/.]+)')
    def kitten_stats(self, request, kitten_id=None):
        try:
            kitten = Kitten.objects.get(id=kitten_id)
        except Kitten.DoesNotExist:
            return Response({'error': 'Kitten not found'}, status=status.HTTP_404_NOT_FOUND)

        stats = Rating.objects.filter(kitten=kitten).aggregate(
            total_score=Sum('score'),
            rating_count=Count('id')
        )
        return Response(stats)
