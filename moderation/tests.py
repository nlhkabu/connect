from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import resolve
from django.test import TestCase

from .views import invite_member, review_applications

User = get_user_model()

class InviteMemberPageTest(TestCase):

    def test_moderators_url_resolves_to_invite_member_view(self):
        found = resolve('/moderation/')

        self.assertEqual(found.func, invite_member)

    def test_only_moderators_can_access_invite_member_view(self):
        c = self.client
        response = c.get('/moderation/')
        # Unauthenticated user is redirected to login page
        self.assertEqual(response.status_code, 302)

        email = 'john@test.test'
        password = 'johnpass'

        user = User.objects.create_user(email, password)
        c.login(username=email, password=password)

        response = c.get('/moderation/')
        # User lacking relevant permissions is redirected to login page
        self.assertEqual(response.status_code, 302)

        permissions = Permission.objects.filter(codename__in=['add_abusereport', 'access_moderators_page'])
        moderators_group = Group.objects.create()
        moderators_group.permissions = permissions
        user.is_moderator = True
        user.groups.add(moderators_group)

        response = c.get('/moderation/')
        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)

    def test_pending_members_show_in_list(self):
        pass

    def test_pending_members_in_list_are_invited_by_logged_in_user(self):
        pass

    def test_invite_member_form_includes_correct_fields(self):
        pass





