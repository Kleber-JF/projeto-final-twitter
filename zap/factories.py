import factory
from django.contrib.auth.models import User
from .models import Meep

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class MeepFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meep

    user = factory.SubFactory(UserFactory)
    body = factory.Faker('sentence')
