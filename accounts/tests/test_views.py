import factory

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.urlresolvers import resolve, reverse
from django.forms.formsets import formset_factory
from django.test import TestCase

from connect_config.factories import SiteConfigFactory

from accounts.factories import (BrandFactory, InvitedPendingFactory,
                                ModeratorFactory, UserLinkFactory,
                                UserFactory, RoleFactory, SkillFactory)
from accounts.forms import (BaseLinkFormSet, BaseSkillFormSet,
                            LinkForm, SkillForm)
from accounts.models import UserLink, UserSkill
from accounts.views import (activate_account, close_account, profile_settings,
                            request_invitation, update_email, update_password)
from accounts.view_utils import match_link_to_brand, save_links, save_skills


User = get_user_model()

#TODO: Write unit tests for django.auth views

class RequestInvitationTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.site = get_current_site(self.client.request)
        self.site.config = SiteConfigFactory(site=self.site)
        self.moderator = ModeratorFactory()

    def test_request_invitation_url_resolves_to_request_invitation_view(self):
        url = resolve('/accounts/request-invitation/')

        self.assertEqual(url.func, request_invitation)

    def test_requested_account_registration_recorded(self):
        response = self.client.post(
            reverse('accounts:request-invitation'),
            data={
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'new_test@test.test',
                'comments': 'Please give me an account',
            },
        )

        user = User.objects.get(email='new_test@test.test')

        self.assertEqual(user.registration_method, 'REQ')
        self.assertIsNotNone(user.applied_datetime)
        self.assertEqual(user.application_comments, 'Please give me an account')

    def test_notification_emails_are_sent_to_moderators(self):
        # Setup moderators to receive emails
        factory.create_batch(
            ModeratorFactory,
            3,
            moderator=self.moderator
        )

        response = self.client.post(
            reverse('accounts:request-invitation'),
            data={
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'new_test@test.test',
                'comments': 'Please give me an account',
            },
        )

        expected_subject = 'New account request at {}'.format(self.site.name)
        expected_intro = 'Hi {},'.format('Moderator')
        expected_content = 'new account application has be registered at {}'.format(
            self.site.name
        )

        expected_url = ('href="http://testserver/moderation/review-applications/"')
        email = mail.outbox[0]

        self.assertEqual(len(mail.outbox), 4) # 3 created as batch, plus original.
        self.assertEqual(email.subject, expected_subject)
        self.assertIn(expected_intro, email.body)
        self.assertIn(expected_content, email.body)
        self.assertIn(expected_url, email.alternatives[0][0])

    def test_request_invitation_redirect(self):
        response = self.client.post(
            reverse('accounts:request-invitation'),
            data={
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'new_test@test.test',
                'comments': 'Please give me an account',
            },
        )

        self.assertRedirects(response, '/accounts/request-invitation/done/')


class ActivateAccountTest(TestCase):
    def setUp(self):
        self.invited_user = InvitedPendingFactory(
            email='validuser@test.test',
            auth_token='mytoken',
        )
        self.invalid_invited_user = InvitedPendingFactory(
            auth_token='invalid',
            auth_token_is_used=True,
        )

    def test_activate_account_url_resolves_to_activate_account_view(self):
        url = resolve('/accounts/activate/mytoken')

        self.assertEqual(url.func, activate_account)

    def test_activate_account_view_with_valid_token(self):
        response = self.client.get('/accounts/activate/mytoken')

        self.assertEqual(response.status_code, 200)


    def test_raises_404_if_given_token_not_attached_to_a_user(self):
        response = self.client.get('/accounts/activate/notoken')

        self.assertEqual(response.status_code, 404)

    def test_form_shows_if_token_is_valid(self):
        response = self.client.get('/accounts/activate/mytoken')
        expected_html = '<legend>Activate Account</legend>'
        self.assertInHTML(expected_html, response.content.decode())

    def test_error_shows_if_token_is_invalid(self):
        response = self.client.get('/accounts/activate/invalid')
        expected_html = '<h3 class="lined">Token is Used</h3>'

        self.assertInHTML(expected_html, response.content.decode())

    def test_account_activation(self):
        user = User.objects.get(email='validuser@test.test')
        old_pass = user.password

        response = self.client.post(
            '/accounts/activate/mytoken',
            data={
                'first_name': 'Hello',
                'last_name': 'There',
                'password': 'abc',
                'confirm_password': 'abc',
            },
        )

        user = User.objects.get(email='validuser@test.test')

        self.assertEqual(user.first_name, 'Hello')
        self.assertEqual(user.last_name, 'There')
        self.assertNotEqual(user.password, old_pass)
        self.assertTrue(user.is_active)
        self.assertTrue(user.auth_token_is_used)

        self.assertTrue(self.client.session['show_welcome'])
        self.assertRedirects(response, '/')


class ProfileSettingsTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

    def test_profile_url_resolves_to_profile_settings_view(self):
        url = resolve('/accounts/profile/')

        self.assertEqual(url.func, profile_settings)

    def test_profile_is_not_available_to_unauthenticated_users(self):
        response = self.client.get(reverse('accounts:profile-settings'))

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/accounts/profile/',
            status_code=302
        )

    def test_profile_is_available_to_authenticated_users(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('accounts:profile-settings'))

        self.assertEqual(response.status_code, 200)

    def test_can_update_profile(self):
        # Setup skills and roles
        django = SkillFactory(name='django')
        mentor = RoleFactory(name='mentor')

        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.post(
            reverse('accounts:profile-settings'),
            data={
                'first_name': 'New First Name',
                'last_name': 'New Last Name',
                'bio': 'New bio',
                'roles': [mentor.id],
                'link-TOTAL_FORMS': 1,
                'link-INITIAL_FORMS': 0,
                'link-0-anchor': 'My Link',
                'link-0-url': 'http://mylink.com',
                'skill-TOTAL_FORMS': 1,
                'skill-INITIAL_FORMS': 0,
                'skill-0-skill': django.id,
                'skill-0-proficiency': UserSkill.INTERMEDIATE,
            },
        )

        user = User.objects.get(id=self.standard_user.id)
        user_link = UserLink.objects.get(user=user)
        user_skill = UserSkill.objects.get(user=user)

        self.assertEqual(user.first_name, 'New First Name')
        self.assertEqual(user.last_name, 'New Last Name')
        self.assertEqual(user.bio, 'New bio')
        self.assertEqual(user.roles.count(), 1)
        self.assertEqual(user.roles.first(), mentor)
        self.assertEqual(user_link.anchor, 'My Link')
        self.assertEqual(user_link.url, 'http://mylink.com/')
        self.assertEqual(user_skill.skill, django)
        self.assertEqual(user_skill.proficiency, UserSkill.INTERMEDIATE)

        # Check that we see success message
        expected_message = 'profile has been updated.'
        self.assertIn(expected_message, response.content.decode())


class UpdateEmailTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

    def test_update_email_url_resolves_to_update_email_view(self):
        url = resolve('/accounts/update/email/')

        self.assertEqual(url.func, update_email)

    def test_authenticated_users_can_update_email_with_POST_data(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.post(
            reverse('accounts:update-email'),
            data={
                'email': 'my.new.email@test.test',
                'password': 'pass',
            },
        )

        user = User.objects.get(id=self.standard_user.id)
        self.assertEqual(user.email, 'my.new.email@test.test')

        # Check that we see success message
        expected_message = 'email has been updated.'
        self.assertIn(expected_message, response.content.decode())

    def test_update_email_not_available_to_unautheticated_users(self):
        response = self.client.post(
            reverse('accounts:update-email'),
            data={
                'email': 'my.new.email@test.test',
                'password': 'pass',
            },
        )

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/accounts/update/email/',
            status_code=302
        )


class UpdatePasswordTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

    def test_update_password_url_resolves_to_update_password_view(self):
        url = resolve('/accounts/update/password/')

        self.assertEqual(url.func, update_password)

    def test_authenticated_users_can_update_password(self):
        self.client.login(username=self.standard_user.email, password='pass')
        old_pass = self.standard_user.password

        response = self.client.post(
            reverse('accounts:update-password'),
            data={
                'new_password': 'newpass',
                'current_password': 'pass',
            },
        )

        user = User.objects.get(id=self.standard_user.id)
        self.assertNotEqual(user.password, old_pass)

        # Check that we see success message
        expected_message = 'password has been updated.'
        self.assertIn(expected_message, response.content.decode())

    def test_update_password_not_available_to_unautheticated_users(self):
        response = self.client.post(
            reverse('accounts:update-password'),
            data={
                'new_password': 'newpass',
                'current_password': 'pass',
            },
        )

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/accounts/update/password/',
            status_code=302
        )


class CloseAccountTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

    def test_close_account_url_resolves_to_close_account_view(self):
        url = resolve('/accounts/close/')

        self.assertEqual(url.func, close_account)

    def test_authenticated_users_can_close_account(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.post(
            reverse('accounts:close-account'),
            data={
                'password': 'pass',
            },
        )

        # Sending valid data should result in this view redirecting to done
        self.assertRedirects(
            response,
            '/accounts/close/done/',
            status_code=302
        )
        user = User.objects.get(id=self.standard_user.id)

        self.assertFalse(user.is_active)
        self.assertTrue(user.is_closed)

    def test_close_account_not_available_to_unautheticated_users(self):
        response = self.client.post(
            reverse('accounts:close-account'),
            data={
                'password': 'pass',
            },
        )

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/accounts/close/',
            status_code=302
        )


# View_utils.py

class ViewUtilsTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

    def test_can_save_skills(self):
        django = SkillFactory(name='django')
        python = SkillFactory(name='python')

        SkillFormSet = formset_factory(SkillForm, max_num=None,
                                       formset=BaseSkillFormSet)

        formset = SkillFormSet(
            data={
                'form-TOTAL_FORMS': 2,
                'form-INITIAL_FORMS': 0,
                'form-0-skill': django.id,
                'form-0-proficiency': UserSkill.BEGINNER,
                'form-1-skill': python.id,
                'form-1-proficiency': UserSkill.INTERMEDIATE,
            }
        )

        save_skills(self.standard_user, formset)

        user = User.objects.get(id=self.standard_user.id)
        user_skills = UserSkill.objects.filter(user=user)

        skill_names = [skill.skill for skill in user_skills]
        skill_proficencies = [skill.proficiency for skill in user_skills]

        self.assertEqual(len(user_skills), 2)
        self.assertIn(django, skill_names)
        self.assertIn(python, skill_names)
        self.assertIn(UserSkill.BEGINNER, skill_proficencies)
        self.assertIn(UserSkill.INTERMEDIATE, skill_proficencies)

    def test_can_save_links(self):
        LinkFormSet = formset_factory(LinkForm, max_num=None,
                                      formset=BaseLinkFormSet)

        formset = LinkFormSet(
            data={
                'form-TOTAL_FORMS': 2,
                'form-INITIAL_FORMS': 0,
                'form-0-anchor': 'Anchor 1',
                'form-0-url': 'http://link1.com',
                'form-1-anchor': 'Anchor 2',
                'form-1-url': 'http://link2.com',
            }
        )

        save_links(self.standard_user, formset)

        user = User.objects.get(id=self.standard_user.id)
        user_links = UserLink.objects.filter(user=user)

        link_anchors = [link.anchor for link in user_links]
        link_urls = [link.url for link in user_links]

        self.assertEqual(len(user_links), 2)
        self.assertIn('Anchor 1', link_anchors)
        self.assertIn('Anchor 2', link_anchors)
        self.assertIn('http://link1.com/', link_urls)
        self.assertIn('http://link2.com/', link_urls)

    def test_can_match_link_to_brand(self):
        github = BrandFactory()
        link_user = UserFactory()
        link = UserLinkFactory(
            user=link_user,
            anchor='Github',
            url='http://github.com/myaccount/',
        )
        userlinks = [link,]

        match_link_to_brand(userlinks)
        link = UserLink.objects.get(user=link_user)

        self.assertEqual(link.icon, github)
