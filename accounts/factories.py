import factory

from django.utils import timezone

from .models import (AbuseReport, CustomUser, LinkBrand, Role,
                    UserLink, UserSkill)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    first_name = 'Standard'
    last_name = 'User'
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())
    registration_method = CustomUser.INVITED


class ModeratorFactory(UserFactory):
    first_name = 'Moderator'
    is_moderator = True
    is_staff = True # Quick and dirty method to give moderator all permissions

