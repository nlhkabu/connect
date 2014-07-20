from django.contrib.auth import get_user_model
from django.contrib.auth.views import login
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.six import StringIO
from django.utils.timezone import now

from moderation.models import UserRegistration

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

    #TODO: test that is is actually a superuser

    return superuser


def create_active_standard_user(moderator,
                                email='standard@test.test',
                                first_name='standard',
                                last_name='user'):
    """
    Create a standard user with an already activated account.
    """
    user = moderator.invite_new_user(email, first_name, last_name)
    user.is_active = True
    user.userregistration.activated_datetime = now()
    user.userregistration.auth_token_is_used = True

    #TODO: test that is is actually a standard user

    return user


def create_active_moderator(moderator,
                           email='moderator@test.test',
                           first_name='moderator',
                           last_name='user'):
    """
    Create a moderator with an already activated account.
    """
    user = moderator.invite_new_user(email, first_name, last_name)
    user.promote_to_moderator()

    user.is_active = True
    user.userregistration.activated_datetime = now()
    user.userregistration.auth_token_is_used = True

    #TODO: test that is is actually a moderator

    return user


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
