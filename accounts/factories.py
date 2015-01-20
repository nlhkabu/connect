import factory

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.utils import timezone

from .models import (AbuseReport, CustomUser, LinkBrand,
                     Skill, Role, UserLink, UserSkill)


class GroupFactory(factory.django.DjangoModelFactory):
    """
    Creates a user group
    """
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: "Group #%s" % n)


class UserFactory(factory.django.DjangoModelFactory):
    """
    Creates a standard active user.
    """
    class Meta:
        model = CustomUser

    first_name = 'Standard'
    last_name = 'User'
    # Emails must be unique - so use a sequence here:
    email = factory.Sequence(lambda n: 'user.{}@test.test'.format(n))
    password = make_password('pass')
    registration_method = CustomUser.INVITED
    auth_token = factory.Sequence(lambda n: 'token{}'.format(n))
    auth_token_is_used = True
    is_active = True
    is_closed = False

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        """
        Where 'groups' are defined, add them to this user.
        """
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)

    @factory.post_generation
    def roles(self, create, extracted, **kwargs):
        """
        Where 'roles' are defined, add them to this user.
        """
        if not create:
            return

        if extracted:
            for role in extracted:
                self.roles.add(role)


class ModeratorFactory(UserFactory):
    """
    Creates a moderator in 'moderators' group
    """
    first_name = 'Moderator'
    is_moderator = True
    groups = Group.objects.filter(name='moderators')


class InvitedPendingFactory(factory.django.DjangoModelFactory):
    """
    Creates a user who has been invited by a moderator, but not yet
    activated their account
    """
    class Meta:
        model = CustomUser

    first_name = 'Invited Pending'
    last_name = 'User'
    email = factory.Sequence(lambda n: 'invited.pending.{}@test.test'.format(n))

    registration_method = CustomUser.INVITED
    moderator = factory.SubFactory(UserFactory) # TODO: change to moderator factory
    moderator_decision = CustomUser.PRE_APPROVED
    decision_datetime = timezone.now()
    auth_token = factory.Sequence(lambda n: 'invitedtoken{}'.format(n))
    auth_token_is_used = False
    is_active = False


class RequestedPendingFactory(factory.django.DjangoModelFactory):
    """
    Creates a user who has requested an account,
    but not yet been accepted or rejected
    """
    class Meta:
        model = CustomUser

    first_name = 'Requested Pending'
    last_name = 'User'
    email = factory.Sequence(lambda n: 'requested.pending.{}@test.test'.format(n))
    registration_method = CustomUser.REQUESTED
    application_comments = 'Please give me an account'
    is_active = False


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    name = factory.Sequence(lambda n: 'role{}'.format(n))


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Skill

    name = factory.Sequence(lambda n: 'skill{}'.format(n))


class UserSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserSkill

    user = factory.SubFactory(UserFactory)
    skill = factory.SubFactory(SkillFactory)
    proficiency = factory.Iterator([
        UserSkill.BEGINNER,
        UserSkill.INTERMEDIATE,
        UserSkill.ADVANCED,
        UserSkill.EXPERT
    ])


class AbuseReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AbuseReport

    logged_against = factory.SubFactory(UserFactory)
    logged_by = factory.SubFactory(UserFactory)


class AbuseWarningFactory(AbuseReportFactory):
    """
    Creates an abuse report where a warning has been previously issued.
    """
    moderator = factory.SubFactory(UserFactory)
    moderator_decision = AbuseReport.WARN
    moderator_comment = 'Ths is a formal warning'
    decision_datetime = timezone.now()


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
