from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.views import login
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.six import StringIO
from django.utils.timezone import now

User = get_user_model()


def create_superuser():
    """
    Create a superuser (with moderator privileges) to initiate tests.
    """
    temp_io = StringIO() # Avoid cluttering test output

    call_command(
        "createsuperuser",
        interactive=False,
        email="superuser@test.test",
        stdout=temp_io,
    )

    superuser = User.objects.get(email="superuser@test.test")
    superuser.is_moderator = True

    return superuser


def create_active_standard_user(moderator,
                                email='standard@test.test',
                                first_name='standard',
                                last_name='user',
                                password='default'):
    """
    Create a standard user with an already activated account.
    """
    user = moderator.invite_new_user(email, first_name, last_name)
    user.password = password
    user.is_active = True
    user.activated_datetime = now()
    user.auth_token_is_used = True

    return user


def create_active_moderator(moderator,
                           email='moderator@test.test',
                           first_name='moderator',
                           last_name='user',
                           password='default'):
    """
    Create a moderator with an already activated account.
    """
    user = moderator.invite_new_user(email, first_name, last_name)
    user.password = password
    user.promote_to_moderator()

    user.is_active = True
    user.activated_datetime = now()
    user.auth_token_is_used = True

    return user


class TestTestingUsers(TestCase):
    """
    Test that the mock users are what they should be.
    """

    def test_that_test_superuser_is_superuser(self):
        superuser = create_superuser()
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_moderator)

    def test_that_test_moderator_is_moderator(self):
        superuser = create_superuser()
        moderator = create_active_moderator(superuser)
        self.assertTrue(moderator.is_moderator)

        moderators = Group.objects.get(name='moderators')
        groups = moderator.groups.all()
        self.assertIn(moderators, groups)

    def test_that_test_standard_user_is_standard_user(self):
        superuser = create_superuser()
        standard_user = create_active_standard_user(superuser)
        self.assertFalse(standard_user.is_moderator)

        moderators = Group.objects.get(name='moderators')
        groups = standard_user.groups.all()
        self.assertNotIn(standard_user, groups)


class UserModelTest(TestCase):

    def test_standard_user_can_be_promoted_to_moderator(self):


        pass



class CreateUserTest(TestCase):

    def test_moderator_can_invite_new_user(self):
        superuser = create_superuser()
        user = superuser.invite_new_user(email='standard@test.test',
                                         first_name='standard',
                                         last_name='user')


    def test_standard_user_cannot_invite_new_user(self):
        #TODO
        pass


class LoginPageTest(TestCase):

    def test_login_page_exists(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'id_username')
        self.assertContains(response, 'id_password')
