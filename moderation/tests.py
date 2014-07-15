from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.utils.timezone import now

from .models import UserRegistration
from .views import invite_member, review_applications

User = get_user_model()

def create_standard_user(email='standard@test.test', password='default'):
        user = User.objects.create_user(email, password)
        return user


def invite_standard_user(moderator, email='invited@test.test', password='default'):
        user = User.objects.create_user(email, password)
        user.is_active = False

        user_registration = UserRegistration.objects.create(
            user=user,
            method=UserRegistration.INVITED,
            moderator=moderator,
            moderator_decision=UserRegistration.PRE_APPROVED,
            decision_datetime=now(),
            auth_token = '123'
        )

        return user


def create_moderator(email='moderator@test.test', password='default'):
        user = User.objects.create_user(email, password)

        codenames = ['add_abusereport',
                     'access_moderators_page',
                     'add_userregistration',
                     'change_userregistration',
                     'delete_userregistration',
                     'invite_user']
        moderator_permissions = Permission.objects.filter(codename__in=codenames)
        moderators_group = Group.objects.create(name='moderators')
        moderators_group.permissions = moderator_permissions
        user.is_moderator = True
        user.groups.add(moderators_group)

        return user


class InviteMemberPageTest(TestCase):

    def test_moderation_url_resolves_to_invite_member_view(self):
        found = resolve(reverse('moderation:moderators'))

        self.assertEqual(found.func, invite_member)

    def test_only_moderators_can_access_invite_member_view(self):
        c = self.client
        response = c.get(reverse('moderation:moderators'))
        # Unauthenticated user is redirected to login page
        self.assertEqual(response.status_code, 302)

        user = create_standard_user()
        c.login(email=user.email, password='default')

        response = c.get(reverse('moderation:moderators'))
        # User lacking relevant permissions is redirected to login page
        self.assertEqual(response.status_code, 302)
        c.logout()

        moderator = create_moderator()
        c.login(email=moderator.email, password='default')

        response = c.get(reverse('moderation:moderators'))
        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)

    def test_pending_members_show_in_list(self):
        c = self.client

        # Setup a new user who was invited by logged in moderator
        moderator = create_moderator()
        c.login(email=moderator.email, password='default')

        invited_user = invite_standard_user(moderator=moderator)

        # Check that invited user is in 'pending users' list
        response = c.get(reverse('moderation:moderators'))
        self.assertIn(invited_user, response.context['pending'])




    def test_pending_members_in_list_are_invited_by_logged_in_user(self):
        pass

    def test_invite_member_form_includes_correct_fields(self):
        pass

    def test_only_moderators_can_invite_new_members(self):
        pass





