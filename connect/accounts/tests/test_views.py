import factory

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import views as auth_views
from django.core import mail
from django.core.urlresolvers import resolve, reverse

from connect.accounts.factories import (InvitedPendingFactory, ModeratorFactory,
                                RoleFactory, SkillFactory, UserFactory)
from connect.accounts.models import UserLink, UserSkill
from connect.accounts.views import (activate_account, close_account, profile_settings,
                            request_invitation, update_email, update_password)
from connect.config.factories import SiteConfigFactory
from connect.tests import BoostedTestCase as TestCase


User = get_user_model()


class AuthenticationTest(TestCase):
    def test_login_url_and_template(self):
        self.check_url('/accounts/login/', auth_views.login)
        self.check_template('accounts:login', 'accounts/login.html')

    def test_logout_url(self):
        self.check_url('/accounts/logout/', auth_views.logout)


class ResetPasswordTest(TestCase):
    def test_password_reset_url_and_template(self):
        self.check_url('/accounts/password/reset/', auth_views.password_reset)
        self.check_template('accounts:password-reset',
                            'accounts/password_reset.html')

    def test_password_reset_done_url_and_template(self):
        self.check_url('/accounts/password/reset/done/',
                       auth_views.password_reset_done)
        self.check_template('accounts:password-reset-done',
                            'accounts/password_reset_done.html')

    def test_password_reset_confirm_url_and_template(self):
        self.check_url('/accounts/password/reset/MMMM/fjdklafjsl/',
                       auth_views.password_reset_confirm)
        response = self.client.post(reverse('accounts:password-reset-confirm',
                                             kwargs={
                                                'uidb64': 'MMM',
                                                'token': 'fsaljfkdl'
                                            }))
        self.assertTemplateUsed(response, 'accounts/password_reset_confirm.html')

    def test_password_reset_complete_url_and_template(self):
        self.check_url('/accounts/password/reset/complete/',
                       auth_views.password_reset_complete)
        self.check_template('accounts:password-reset-complete',
                            'accounts/password_reset_complete.html')


class RequestInvitationTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.site = get_current_site(self.client.request)
        self.site.config = SiteConfigFactory(site=self.site)
        self.moderator = ModeratorFactory()

    def post_data(self, first='First'):
        return self.client.post(
            reverse('accounts:request-invitation'),
            data={
                'first_name': first,
                'last_name': 'Last',
                'email': 'new_test@test.test',
                'comments': 'Please give me an account',
            },
        )

    def test_url_and_template(self):
        self.check_url('/accounts/request-invitation/', request_invitation)
        self.check_template('accounts:request-invitation',
                            'accounts/request_invitation.html')

    def test_account_registration_recorded(self):
        """
        Test that the request has been saved as a new user.
        """
        response = self.post_data()
        user = User.objects.get(email='new_test@test.test')

        self.assertEqual(user.registration_method, 'REQ')
        self.assertIsNotNone(user.applied_datetime)
        self.assertEqual(user.application_comments, 'Please give me an account')

    def test_notification_emails_sent_to_moderators(self):
        # Setup moderators to receive emails
        factory.create_batch(
            ModeratorFactory,
            3,
            moderator=self.moderator
        )

        response = self.post_data()

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

    def test_redirect(self):
        """
        Test that we redirect to the done URL if we have passed valid data.
        """
        response = self.post_data()
        self.assertRedirects(response, '/accounts/request-invitation/done/')


class ActivateAccountTest(TestCase):
    def setUp(self):
        self.invited_user = InvitedPendingFactory(
            email='validuser@test.test',
            auth_token='mytoken',
        )
        self.activated_user = InvitedPendingFactory(
            auth_token='used',
            auth_token_is_used=True,
        )

    def test_url_and_template(self):
        self.check_url('/accounts/activate/mytoken', activate_account)
        response = self.client.get(reverse('accounts:activate-account',
                                            kwargs={'token': 'mytoken'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/activate_account.html')
        # Test we see appropriate form
        expected_html = '<legend>Activate Account</legend>'
        self.assertInHTML(expected_html, response.content.decode())


    def test_invalid_token(self):
        """
        Test view raises a 404 if we try to visit the page by
        entering a random token (i.e. a token not attached to a user).
        """
        response = self.client.get('/accounts/activate/notoken')

        self.assertEqual(response.status_code, 404)


    def test_used_token(self):
        """
        Test that a user with an used token is shown a
        'token is used' message.
        """
        response = self.client.get('/accounts/activate/used')
        expected_html = '<h3 class="lined">Token is Used</h3>'

        self.assertInHTML(expected_html, response.content.decode())

    def test_account_activation(self):
        """
        Given a valid token, and valid data,
        test we see the appropriate response.
        """
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

        # And that the user is activated
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

    def test_url(self):
        self.check_url('/accounts/profile/', profile_settings)

    def test_authenticated_user_can_access_page(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('accounts:profile-settings'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_settings.html')

    def test_unauthenticated_user_cannot_access_page(self):
        response = self.client.get(reverse('accounts:profile-settings'))

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response, '/accounts/login/?next=/accounts/profile/')

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

        self.assertEqual(response.status_code, 200)

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

    def post_data(self):
        return self.client.post(
            reverse('accounts:update-email'),
            data={
                'email': 'my.new.email@test.test',
                'password': 'pass',
            },
        )

    def test_url(self):
        self.check_url('/accounts/update/email/', update_email)

    def test_unautheticated_user_cannot_update_email(self):
        response = self.post_data()

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response, '/accounts/login/?next=/accounts/update/email/')

    def test_authenticated_user_can_access_page(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('accounts:update-email'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/update_email.html')

    def test_authenticated_user_can_update_email(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.post_data()

        user = User.objects.get(id=self.standard_user.id)
        self.assertEqual(user.email, 'my.new.email@test.test')

        # Check that we see success message
        expected_message = 'email has been updated.'
        self.assertIn(expected_message, response.content.decode())


class UpdatePasswordTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

    def post_data(self):
        return self.client.post(
            reverse('accounts:update-password'),
            data={
                'new_password': 'newpass',
                'current_password': 'pass',
            },
        )

    def test_url(self):
        self.check_url('/accounts/update/password/', update_password)

    def test_unauthenticated_user_cannot_update_password(self):
        response = self.post_data()

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response, '/accounts/login/?next=/accounts/update/password/')

    def test_authenticated_user_can_access_page(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('accounts:update-password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/update_password.html')

    def test_authenticated_user_can_update_password(self):
        self.client.login(username=self.standard_user.email, password='pass')
        old_pass = self.standard_user.password
        response = self.post_data()

        user = User.objects.get(id=self.standard_user.id)
        self.assertNotEqual(user.password, old_pass)

        # Check that we see success message
        expected_message = 'password has been updated.'
        self.assertIn(expected_message, response.content.decode())


class CloseAccountTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

    def post_valid_data(self):
        return self.client.post(
            reverse('accounts:close-account'),
            data={
                'password': 'pass',
            },
        )

    def test_url(self):
        self.check_url('/accounts/close/', close_account)

    def test_unautheticated_user_cannot_close_account(self):
        response = self.post_valid_data()

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response, '/accounts/login/?next=/accounts/close/')

    def test_authenticated_user_can_access_page(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('accounts:close-account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/close_account.html')

    def test_authenticated_user_can_close_account(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.post_valid_data()

        # Sending valid data should result in this view redirecting to done
        self.assertRedirects(response, '/accounts/close/done/')
        user = User.objects.get(id=self.standard_user.id)

        self.assertFalse(user.is_active)
        self.assertTrue(user.is_closed)
