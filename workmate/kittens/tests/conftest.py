from pytest_factoryboy import register
from .factories import CustomUserFactory, BreedFactory, KittenFactory, RatingFactory

register(CustomUserFactory) 
register(BreedFactory)
register(KittenFactory)
register(RatingFactory)
   