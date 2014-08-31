import factory

from django.utils import timezone

from .models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    first_name = 'Standard'
    last_name = 'User'
    # Emails must be unique - so use a sequence here:
    email = factory.Sequence(lambda n: 'user.{}@test.test'.format(n))
    registration_method = CustomUser.INVITED


class ModeratorFactory(UserFactory):
    first_name = 'Moderator'
    is_moderator = True
    is_staff = True # Quick and dirty way to give moderator all permissions


class InvitedPendingFactory(factory.django.DjangoModelFactory):
    """
    User who has been invited by a moderator, but not yet
    activated their account
    """
    class Meta:
        model = CustomUser

    first_name = 'Invited Pending'
    last_name = 'User'
    email = factory.Sequence(lambda n: 'invited.pending.{}@test.test'.format(n))
    moderator = factory.SubFactory(UserFactory)


class RequestedPendingFactory(factory.django.DjangoModelFactory):
    """
    User who has requested an account, but not yet been accepted or rejected
    """
    class Meta:
        model = CustomUser

    first_name = 'Requested Pending'
    last_name = 'User'
    email = factory.Sequence(lambda n: 'requested.pending.{}@test.test'.format(n))
    registration_method = CustomUser.REQUESTED
