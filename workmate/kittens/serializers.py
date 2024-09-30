from rest_framework import serializers
from .models import Kitten, Breed, Rating, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'

class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = '__all__'
        read_only_fields = ['owner']

    def validate(self, data):
        description = data.get('description')
        if Kitten.objects.filter(description=description).exists():
            raise serializers.ValidationError("A kitten with this description already exists.")
        return data
        

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['user']

    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        kitten = data['kitten']
        
        # Проверка, существует ли уже рейтинг от этого пользователя для данного котенка
        if Rating.objects.filter(user=user, kitten=kitten).exists():
            raise serializers.ValidationError("You have already rated this kitten.")
        
        return data
