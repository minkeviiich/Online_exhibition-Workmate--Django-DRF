from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя, расширяющая стандартную модель AbstractUser."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password',
    ]

    ROLE_CHOICES = (
        ('participant', 'Участник'),
        ('visitor', 'Посетитель'),
    )
    role = models.CharField(
        max_length=11,
        choices=ROLE_CHOICES,
        default='visitor',
    )


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)


class Breed(models.Model):
    """Модель породы котят."""

    name = models.CharField(
        verbose_name='Название породы',
        max_length=100,
    )


    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'
        ordering = ('id',)


class Kitten(models.Model):
    """ Модель котят."""

    color = models.CharField(
        verbose_name='Цвет',
        max_length=100,
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=100,
    )
    age = models.IntegerField(
        verbose_name='Возраст',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        unique=True,
    )
    breed = models.ForeignKey(
        Breed,
        related_name='kittens',
        on_delete=models.CASCADE,
        verbose_name='Порода',
    )
    owner = models.ForeignKey(
        CustomUser,
        related_name='kittens',
        on_delete=models.CASCADE,
        verbose_name='Владелец',
    )


    class Meta:
        verbose_name = 'Котенок'
        verbose_name_plural = 'Котята'
        ordering = ('id',)


class Rating(models.Model):
    """Модель рейтинга котенка."""

    kitten = models.ForeignKey(
        Kitten,
        related_name='ratings',
        on_delete=models.CASCADE,
        verbose_name='Котенок',
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='ratings',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
    )


    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        ordering = ('id',)
