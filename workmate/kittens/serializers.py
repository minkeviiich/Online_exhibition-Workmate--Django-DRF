from .models import Breed, CustomUser, Kitten, Rating
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
import django_filters


class CustomUserSerializer(ModelSerializer):
    """ Сериализатор для модели CustomUser."""

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'role'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Метод создает и возвращает нового пользователя с валидированными данными."""
        
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user


class BreedSerializer(ModelSerializer):
    """Сериализатор для модели Breed"""


    class Meta:
        model = Breed
        fields = '__all__'


class KittenSerializer(ModelSerializer):
    """Сериализатор для модели Kitten."""


    class Meta:
        model = Kitten
        fields = '__all__'
        read_only_fields = ['owner']


class KittinFilter(django_filters.FilterSet):
    class Meta:
        model = Kitten
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    """Сериализатор для модели Rating."""


    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['user']


    def validate_score(self, value):
        """Метод проверяет, что значение оценки находится в диапазоне от 1 до 5."""

        if not (1 <= value <= 5):
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )
        return value
