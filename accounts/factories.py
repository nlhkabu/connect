import factory

from django.contrib.auth.models import Group
from django.utils import timezone

from .models import CustomUser, LinkBrand, Skill, UserLink, UserSkill


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: "Group #%s" % n)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    first_name = 'Standard'
    last_name = 'User'
    # Emails must be unique - so use a sequence here:
    email = factory.Sequence(lambda n: 'user.{}@test.test'.format(n))
    registration_method = CustomUser.INVITED

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)


class ModeratorFactory(UserFactory):
    first_name = 'Moderator'
    is_moderator = True
    groups = Group.objects.filter(name='moderators')


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

    registration_method = CustomUser.INVITED
    moderator = factory.SubFactory(ModeratorFactory)
    moderator_decision = CustomUser.PRE_APPROVED
    decision_datetime = timezone.now()
    auth_token = 'abc'


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


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Skill


class UserSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserSkill

    user = factory.SubFactory(UserFactory)
    skill = factory.SubFactory(SkillFactory)
    proficiency = UserSkill.BEGINNER


class UserLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserLink

    user = factory.SubFactory(UserFactory)
    anchor = factory.Sequence(lambda n: 'linkname{}'.format(n))
    url = factory.Sequence(lambda n: 'url{}.test'.format(n))


class BrandFactory(factory.django.DjangoModelFactory):
    """
    Use github as a default for all LinkBrand objects
    """
    class Meta:
        model = LinkBrand

    name = 'Github'
    domain = 'github.com'
    fa_icon = 'fa-github'
