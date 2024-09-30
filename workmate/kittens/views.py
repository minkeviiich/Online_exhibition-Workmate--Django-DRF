from rest_framework import viewsets, permissions, generics
from .models import Kitten, Breed, Rating, CustomUser
from .serializers import KittenSerializer, BreedSerializer, RatingSerializer, CustomUserSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsParticipant(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'participant'


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class KittenViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [IsAuthenticated, IsParticipant]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.role == 'participant':
            return Kitten.objects.filter(owner=self.request.user)
        return Kitten.objects.all()


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)