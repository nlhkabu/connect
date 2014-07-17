from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.utils.timezone import now

from .models import UserRegistration
from .views import invite_standard_user, invite_moderator

User = get_user_model()

def create_active_standard_user(moderator,
                                email='standard@test.test',
                                first_name='standard',
                                last_name='user'):
    """
    For testing purposes only.
    Create a standard user with an already activated account.
    """
    user = invite_standard_user(email, first_name, last_name, moderator)
    user.is_active = True
    user.userregistration.activated_datetime = now()
    user.userregistration.auth_token_is_used = True

    return user


def create_active_moderator(moderator,
                           email='moderator@test.test',
                           first_name='moderator',
                           last_name='user'):
    """
    For testing purposes only.
    Create a moderator with an already activated account.
    """
    user = invite_moderator(email, first_name, last_name, moderator)
    user.is_active = True
    user.userregistration.activated_datetime = now()
    user.userregistration.auth_token_is_used = True

    return user


class CreateUserTest(TestCase):

    def can_create_standard_user(self):


        pass

    def can_create_another_moderator(self):
        pass


class InviteMemberPageTest(TestCase):

    def test_moderation_url_resolves_to_invite_member_view(self):
        found = resolve(reverse('moderation:moderators'))

        self.assertEqual(found.func, invite_member)

    def test_only_moderators_can_access_invite_member_view(self):
        c = self.client
        response = c.get(reverse('moderation:moderators'))
        # Unauthenticated user is redirected to login page
        self.assertEqual(response.status_code, 302)

        user = create_active_standard_user()
        c.login(email=user.email, password='default')

        response = c.get(reverse('moderation:moderators'))
        # User lacking relevant permissions is redirected to login page
        self.assertEqual(response.status_code, 302)
        c.logout()

        moderator = create_active_moderator()
        c.login(email=moderator.email, password='default')

        response = c.get(reverse('moderation:moderators'))
        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)

#~
    #~def test_pending_members_show_in_list(self):
        #~c = self.client
#~
        #~moderator = create_moderator()
        #~c.login(email=moderator.email, password='default')
#~
        #~# Setup a new user who was invited by logged in moderator
        #~invited_user = invite_standard_user(moderator=moderator)
#~
        #~# Check that invited user is in 'pending users' list
        #~response = c.get(reverse('moderation:moderators'))
        #~self.assertIn(invited_user, response.context['pending'])




    def test_pending_members_in_list_are_invited_by_logged_in_user(self):
        pass

    def test_invite_member_form_includes_correct_fields(self):
        pass

    def test_only_moderators_can_invite_new_members(self):
        pass





