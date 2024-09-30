from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    ROLE_CHOICES = (
        ('participant', 'Участник'),
        ('visitor', 'Посетитель'),
    )
    role = models.CharField(max_length=11, choices=ROLE_CHOICES, default='visitor')


class Breed(models.Model):
    name = models.CharField(max_length=100)


class Kitten(models.Model):
    color = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField()
    breed = models.ForeignKey(Breed, related_name='kittens', on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='kittens', on_delete=models.CASCADE)


class Rating(models.Model):
    kitten = models.ForeignKey(Kitten, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='ratings', on_delete=models.CASCADE)
    score = models.IntegerField()