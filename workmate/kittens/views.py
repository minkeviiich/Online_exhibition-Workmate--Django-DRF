from rest_framework import viewsets, permissions, generics
from .models import Kitten, Breed, Rating, CustomUser
from .serializers import KittenSerializer, BreedSerializer, RatingSerializer, CustomUserSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'participant':
            return Response({'detail': 'You do not have permission to add kittens.'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({'detail': 'You do not have permission to modify this kitten.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({'detail': 'You do not have permission to delete this kitten.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        return Kitten.objects.all()

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('breed', openapi.IN_QUERY, description="ID породы", type=openapi.TYPE_INTEGER)
    ])
    @action(detail=False, methods=['get'], url_path='by-breed')
    def list_by_breed(self, request):
        breed_id = request.query_params.get('breed')
        if breed_id:
            kittens = Kitten.objects.filter(breed_id=breed_id)
        else:
            return Response({'detail': 'Breed ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(kittens, many=True)
        return Response(serializer.data)
    

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
