import factory

from django.core.urlresolvers import resolve, reverse
from django.test import RequestFactory

from connect.accounts.factories import (RoleFactory, SkillFactory, UserFactory,
                                UserSkillFactory)
from connect.discover.views import dashboard, member_map
from connect.tests import BoostedTestCase as TestCase


class DashboardTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

        # Setup users with skills
        self.django = SkillFactory(name='django')
        self.rails = SkillFactory(name='rails')
        self.jquery = SkillFactory(name='jquery')

        self.mentor = RoleFactory(name='mentor')
        self.mentee = RoleFactory(name='mentee')

        self.user_1 = UserFactory(roles=[self.mentor,])
        UserSkillFactory(user=self.user_1, skill=self.django)

        self.user_2 = UserFactory(roles=[self.mentee,])
        UserSkillFactory(user=self.user_2, skill=self.django)
        UserSkillFactory(user=self.user_2, skill=self.rails)

        self.user_3 = UserFactory(roles=[self.mentor, self.mentee])
        UserSkillFactory(user=self.user_3, skill=self.rails)
        UserSkillFactory(user=self.user_3, skill=self.jquery)

    def get_dashboard(self, skills=[], roles=[]):
        return self.client.get(
            reverse('dashboard'),
            data={
                'skills': skills,
                'roles': roles,
            },
        )

    def test_dashboard_url(self):
        self.check_url('/', dashboard)

    def test_unauthenticated_user_cannot_view_dashboard(self):
        response = self.get_dashboard()
        # Unauthenticated user is redirected to login page
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_authenticated_user_can_view_dashboard(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.get_dashboard()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discover/list.html')

    def test_requesting_view_with_POST_returns_dashboard(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.post(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)

    def test_can_filter_users_by_skill(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.get_dashboard([self.django.id])
        context_users = response.context['listed_users']

        self.assertIn(self.user_1, context_users)
        self.assertIn(self.user_2, context_users)
        self.assertEqual(len(context_users), 2)

    def test_can_filter_users_by_two_skills(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.get_dashboard([self.django.id, self.rails.id])
        context_users = response.context['listed_users']

        self.assertIn(self.user_1, context_users)
        self.assertIn(self.user_2, context_users)
        self.assertIn(self.user_3, context_users)
        self.assertNotIn(self.standard_user, context_users) #User has no skills
        self.assertEqual(len(context_users), 3)

    def test_can_filter_users_by_role(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.get_dashboard(roles=[self.mentor.id])
        context_users = response.context['listed_users']

        self.assertIn(self.user_1, context_users)
        self.assertIn(self.user_3, context_users)
        self.assertEqual(len(context_users), 2)

    def test_can_filter_users_by_two_roles(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.get_dashboard(roles=[self.mentor.id, self.mentee.id])
        context_users = response.context['listed_users']

        self.assertIn(self.user_1, context_users)
        self.assertIn(self.user_2, context_users)
        self.assertIn(self.user_3, context_users)
        self.assertNotIn(self.standard_user, context_users) #User has no roles
        self.assertEqual(len(context_users), 3)

    def test_can_filter_users_by_skill_and_role(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.get_dashboard(skills=[self.django.id],
                                      roles=[self.mentor.id])
        context_users = response.context['listed_users']

        self.assertIn(self.user_1, context_users)
        self.assertEqual(len(context_users), 1)

    def test_can_filter_users_by_multiple_skills_and_role(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.get_dashboard([self.django.id, self.rails.id],
                                      [self.mentor.id])
        context_users = response.context['listed_users']

        self.assertIn(self.user_1, context_users)
        self.assertIn(self.user_3, context_users)
        self.assertEqual(len(context_users), 2)

    def test_welcome_message_for_first_session(self):
        self.client.login(username=self.standard_user.email, password='pass')
        session = self.client.session
        session['show_welcome'] = True
        session.save()
        response = self.get_dashboard()

        self.assertTrue(response.context['show_welcome'])


class MapTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

    def test_map_url(self):
        self.check_url('/dashboard/map/', member_map)

    def test_unauthenticated_user_cannot_view_map(self):
        response = self.client.get(reverse('discover:map'))

        # Unauthenticated user is redirected to login page
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/map/')

    def test_authenticated_user_can_view_map(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('discover:map'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discover/map.html')
