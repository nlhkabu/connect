import factory

from django.utils import timezone

from connect.accounts.factories import UserFactory
from connect.moderation.models import ModerationLogMsg


class LogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ModerationLogMsg

    msg_type = ModerationLogMsg.INVITATION
    comment = 'Placeholder comment'
    pertains_to = factory.SubFactory(UserFactory)
    # TODO: change to moderator factory
    logged_by = factory.SubFactory(UserFactory)
    msg_datetime = timezone.now()
