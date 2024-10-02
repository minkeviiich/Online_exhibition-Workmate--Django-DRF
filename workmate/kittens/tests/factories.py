import factory
from kittens.models import CustomUser, Breed, Kitten, Rating


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    role = factory.Iterator(['visitor', 'participant'])


class BreedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Breed

    name = factory.Faker('word')


class KittenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Kitten

    color = factory.Faker('color_name')
    name = factory.Faker('first_name')
    age = factory.Faker('random_int', min=1, max=12)
    description = factory.Faker('text')
    breed = factory.SubFactory(BreedFactory)
    owner = factory.SubFactory(CustomUserFactory)


class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rating

    kitten = factory.SubFactory(KittenFactory)
    user = factory.SubFactory(CustomUserFactory)
    score = factory.Faker('random_int', min=1, max=5)
    comment = factory.Faker('text')
