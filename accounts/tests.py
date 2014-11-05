import factory

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.views import login
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.urlresolvers import resolve, reverse
from django.forms.formsets import formset_factory
from django.test import Client, TestCase, RequestFactory

from connect_config.factories import SiteConfigFactory

from .factories import (BrandFactory, InvitedPendingFactory, ModeratorFactory,
                        RequestedPendingFactory, RoleFactory, SkillFactory,
                        UserFactory, UserLinkFactory, UserSkillFactory)

from .forms import (ActivateAccountForm, AccountSettingsForm,
                    BaseLinkFormSet, BaseSkillFormSet,
                    CloseAccountForm, LinkForm, ProfileForm,
                    RequestInvitationForm, SkillForm,
                    validate_email_availability)

from .models import CustomUser, UserLink, UserSkill
from .utils import (create_inactive_user, get_user,
                    invite_user_to_reactivate_account)
from .views import (account_settings, activate_account, close_account,
                    profile_settings, request_invitation, update_account)

from .view_utils import match_link_to_brand, save_links, save_skills


User = get_user_model()


# Models.py

class UserModelTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.moderator = ModeratorFactory()
        self.standard_user = UserFactory()
        self.invited_pending = InvitedPendingFactory()
        self.requested_pending = RequestedPendingFactory()

    def test_moderator_can_invite_new_user(self):
        user = self.moderator.invite_new_user(email='standard_user@test.test',
                                              first_name='standard_user',
                                              last_name='user')

        self.assertEqual(user.email,'standard_user@test.test')
        self.assertEqual(user.first_name, 'standard_user')
        self.assertEqual(user.last_name, 'user')
        self.assertEqual(user.registration_method, CustomUser.INVITED)
        self.assertEqual(user.moderator, self.moderator)
        self.assertEqual(user.moderator_decision, CustomUser.PRE_APPROVED)
        self.assertIsNotNone(user.decision_datetime)
        self.assertIsNotNone(user.auth_token)

    def test_standard_user_user_cannot_invite_new_user(self):
        with self.assertRaises(PermissionDenied):
            user = self.standard_user.invite_new_user(email='standard_user@test.test',
                                                 first_name='standard_user',
                                                 last_name='user')
            self.assertIsNone(user)

    def test_moderator_can_reinvite_user(self):

        decision_datetime = self.invited_pending.decision_datetime
        auth_token = self.invited_pending.auth_token

        self.moderator.reinvite_user(user=self.invited_pending,
                                     email='reset_email@test.test')

        self.assertEqual(self.invited_pending.email, 'reset_email@test.test')
        self.assertNotEqual(self.invited_pending.decision_datetime, decision_datetime)
        self.assertNotEqual(self.invited_pending.auth_token, auth_token)

    def test_standard_user_user_cannot_reinvite_user(self):

        decision_datetime = self.invited_pending.decision_datetime
        auth_token = self.invited_pending.auth_token

        with self.assertRaises(PermissionDenied):
            self.standard_user.reinvite_user(user=self.invited_pending,
                                        email='reset_email@test.test')

            self.assertNotEqual(self.invited_pending.email, 'reset_email@test.test')
            self.assertEqual(self.invited_pending.decision_datetime, decision_datetime)
            self.assertEqual(self.invited_pending.auth_token, auth_token)

    def test_moderator_can_approve_user_application(self):
        self.moderator.approve_user_application(self.requested_pending)

        self.assertEqual(self.requested_pending.moderator, self.moderator)
        self.assertEqual(self.requested_pending.moderator_decision, CustomUser.APPROVED)
        self.assertIsNotNone(self.requested_pending.decision_datetime)
        self.assertIsNotNone(self.requested_pending.auth_token)

    def test_standard_user_user_cannot_approve_user_application(self):
        with self.assertRaises(PermissionDenied):
            self.standard_user.approve_user_application(self.requested_pending)

            self.assertIsNone(self.requested_pending.moderator)
            self.assertFalse(self.requested_pending.moderator_decision)
            self.assertIsNone(self.requested_pending.decision_datetime)
            self.assertFalse(self.requested_pending.auth_token)

    def test_moderator_can_reject_user_application(self):
        self.moderator.reject_user_application(self.requested_pending)

        self.assertEqual(self.requested_pending.moderator, self.moderator)
        self.assertEqual(self.requested_pending.moderator_decision, CustomUser.REJECTED)
        self.assertIsNotNone(self.requested_pending.decision_datetime)
        self.assertIsNotNone(self.requested_pending.auth_token)

    def test_standard_user_user_cannot_reject_user_application(self):
        with self.assertRaises(PermissionDenied):
            self.standard_user.reject_user_application(self.requested_pending)

            self.assertIsNone(self.requested_pending.moderator)
            self.assertFalse(self.requested_pending.moderator_decision)
            self.assertIsNone(self.requested_pending.decision_datetime)
            self.assertFalse(self.requested_pending.auth_token)


class UserSkillTest(TestCase):
    def test_proficiency_percentage_calculates_correctly(self):
        user_skill = UserSkillFactory(proficiency=UserSkill.INTERMEDIATE)
        percentage = user_skill.get_proficiency_percentage()

        self.assertEquals(percentage, 50)


class UserLinkTest(TestCase):
    def setUp(self):
        self.github = BrandFactory() # Github is default brand.

    def test_custom_save_method_finds_registered_brand(self):
        user_link = UserLinkFactory(url='http://github.com/nlh-kabu')

        self.assertEqual(user_link.icon, self.github)

    def test_custom_save_method_cannot_find_unregistered_brand(self):
        user_link = UserLinkFactory(url='http://blahblah.com/nlh-kabu')

        self.assertIsNone(user_link.icon)

    def test_get_icon_method_gets_correct_icon(self):
        user_link = UserLinkFactory(url='http://github.com/nlh-kabu')
        icon = user_link.get_icon()

        self.assertEqual(icon, 'fa-github')

    def test_get_icon_method_gets_default_icon(self):
        user_link = UserLinkFactory(url='http://noiconurl.com')
        icon = user_link.get_icon()

        self.assertEqual(icon, 'fa-globe')


class LinkBrandTest(TestCase):
    def test_custom_save_method_applies_new_brand_to_existing_userlinks(self):
        UserLinkFactory(url='http://facebook.com/myusername')

        new_brand = BrandFactory(name='Facebook',
                                 domain='facebook.com',
                                 fa_icon='fa-facebook')

        # Retreive the link to check that it has the new brand
        link = UserLink.objects.get(url='http://facebook.com/myusername')

        self.assertEqual(link.icon, new_brand)


# Forms.py

class FormValidationTest(TestCase):
    def setUp(self):
        existing_user = UserFactory(email='existing.user@test.test')

    def test_email_is_unique(self):
        unique = validate_email_availability('unique_user@test.test')
        self.assertTrue(unique)

    def test_email_is_duplicate(self):
        with self.assertRaises(ValidationError):
            validate_email_availability('existing.user@test.test')


class RequestInvitationFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.closed_user = UserFactory(
            email='closed.user@test.test',
            is_closed=True,
        )

    def test_closed_account_prompts_custom_validation(self):
        response = self.client.post(
            reverse('accounts:request-invitation'),
            data = {
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'closed.user@test.test',
                'comments': 'I would like an account',
            }
        )

        self.assertFormError(
            response,
            form='form',
            field='email',
            errors='This email address is already registered to another '
            '(closed) account. To reactivate this account, '
            'please check your email inbox. To register a new '
            'account, please use a different email address.'
        )


class ActivateAccountFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.pending_user = InvitedPendingFactory()

    def test_password_validation_fails_when_passwords_are_different(self):
        response = self.client.post(
            reverse('accounts:activate-account', args=(self.pending_user.auth_token,)),
            data = {
                'first_name': 'First',
                'last_name': 'Last',
                'password': 'pass1',
                'confirm_password': 'pass2',
            }
        )

        self.assertFormError(
            response,
            'form',
            field=None,
            errors='Your passwords do not match. Please try again.'
        )

    def test_password_validation_passes_when_passwords_are_same(self):
        form = ActivateAccountForm(
            user = self.pending_user,
            data = {
                'first_name': 'First',
                'last_name': 'Last',
                'password': 'pass1',
                'confirm_password': 'pass1',
            }
        )

        self.assertTrue(form.is_valid())


class ProfileFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.standard_user = UserFactory()

        # Setup skills and roles
        self.django = SkillFactory(name='django')
        self.rails = SkillFactory(name='rails')
        self.jquery = SkillFactory(name='jquery')

        self.mentor = RoleFactory(name='mentor')
        self.mentee = RoleFactory(name='mentee')

        client = Client()
        client.login(username=self.standard_user.email, password='pass')

    def test_validation_fails_if_first_name_not_provided(self):
        form = ProfileForm(
            user = self.standard_user,
            data = {
                'last_name': 'Last',
                'bio': 'My bio',
                'roles': [self.mentor.id, self.mentee.id],
            }
        )

        self.assertFalse(form.is_valid())

    def test_validation_fails_if_last_name_not_provided(self):
        form = ProfileForm(
            user = self.standard_user,
            data = {
                'first_name': 'First',
                'bio': 'My bio',
                'roles': [self.mentor.id, self.mentee.id],
            }
        )

        self.assertFalse(form.is_valid())


    def test_skill_formset_validation_passes_with_correct_data(self):
        form = ProfileForm(
            user = self.standard_user,
            data = {
                'first_name': 'First',
                'last_name': 'Last',
                'link-TOTAL_FORMS': 0,
                'link-INITIAL_FORMS': 0,
                'skill-TOTAL_FORMS': 1,
                'skill-INITIAL_FORMS': 0,
                'skill-0-skill': self.django.id,
                'skill-0-proficiency': UserSkill.BEGINNER,
            }
        )

        self.assertTrue(form.is_valid())

    def test_skill_formset_validation_passes_with_empty_fields(self):
        form = ProfileForm(
            user = self.standard_user,
            data = {
                'first_name': 'First',
                'last_name': 'Last',
                'link-TOTAL_FORMS': 0,
                'link-INITIAL_FORMS': 0,
                'skill-TOTAL_FORMS': 1,
                'skill-INITIAL_FORMS': 0,
                'skill-0-skill': '',
                'skill-0-proficiency': '',
            }
        )

        self.assertTrue(form.is_valid())

    def test_validation_fails_when_skill_is_listed_more_than_once(self):
        self.client.login(username=self.standard_user.email, password='pass')

        response = self.client.post(
            reverse('accounts:profile-settings'),
            data = {
                'link-TOTAL_FORMS': 0,
                'link-INITIAL_FORMS': 0,
                'skill-TOTAL_FORMS': 2,
                'skill-INITIAL_FORMS': 0,
                'skill-0-skill': self.django.id,
                'skill-0-proficiency': UserSkill.BEGINNER,
                'skill-1-skill': self.django.id,
                'skill-1-proficiency': UserSkill.INTERMEDIATE,
            }
        )

        self.assertFormsetError(
            response,
            formset='skill_formset',
            form_index=None,
            field=None,
            errors='Each skill can only be entered once.'
        )

    def test_validation_fails_when_userskill_has_skill_but_no_proficiency(self):
        self.client.login(username=self.standard_user.email, password='pass')

        response = self.client.post(
            reverse('accounts:profile-settings'),
            data = {
                'link-TOTAL_FORMS': 0,
                'link-INITIAL_FORMS': 0,
                'skill-TOTAL_FORMS': 1,
                'skill-INITIAL_FORMS': 0,
                'skill-0-skill': self.django.id,
                'skill-0-proficiency': '',
            }
        )
        self.assertFormsetError(
            response,
            formset='skill_formset',
            form_index=None,
            field=None,
            errors='All skills must have a proficiency.'
        )

    def test_validation_fails_when_userskill_has_proficicency_but_no_skill(self):
        self.client.login(username=self.standard_user.email, password='pass')

        response = self.client.post(
            reverse('accounts:profile-settings'),
            data = {
                'link-TOTAL_FORMS': 0,
                'link-INITIAL_FORMS': 0,
                'skill-TOTAL_FORMS': 1,
                'skill-INITIAL_FORMS': 0,
                'skill-0-skill': '',
                'skill-0-proficiency': UserSkill.BEGINNER,
            }
        )
        self.assertFormsetError(
            response,
            formset='skill_formset',
            form_index=None,
            field=None,
            errors='All profiencies must be attached to a skill.'
        )

    def test_link_formset_validation_passes_with_correct_data(self):
        form = ProfileForm(
            user = self.standard_user,
            data = {
                'first_name': 'First',
                'last_name': 'Last',
                'link-TOTAL_FORMS': 1,
                'link-INITIAL_FORMS': 0,
                'link-0-anchor': 'My Link',
                'link-0-url': 'http://mylink.com',
                'skill-TOTAL_FORMS': 0,
                'skill-INITIAL_FORMS': 0,
            }
        )

        self.assertTrue(form.is_valid())

    def test_link_formset_validation_passes_with_empty_fields(self):
        form = ProfileForm(
            user = self.standard_user,
            data = {
                'first_name': 'First',
                'last_name': 'Last',
                'link-TOTAL_FORMS': 1,
                'link-INITIAL_FORMS': 0,
                'link-0-anchor': '',
                'link-0-url': '',
                'skill-TOTAL_FORMS': 0,
                'skill-INITIAL_FORMS': 0,
            }
        )

        self.assertTrue(form.is_valid())

    def test_validation_fails_when_link_anchor_is_listed_more_than_once(self):
        self.client.login(username=self.standard_user.email, password='pass')

        response = self.client.post(
            reverse('accounts:profile-settings'),
            data = {
                'link-TOTAL_FORMS': 2,
                'link-INITIAL_FORMS': 0,
                'link-0-anchor': 'My Link',
                'link-0-url': 'http://mylink.com',
                'link-1-anchor': 'My Link',
                'link-1-url': 'http://mylink2.com',
                'skill-TOTAL_FORMS': 0,
                'skill-INITIAL_FORMS': 0,
            }
        )

        self.assertFormsetError(
            response,
            formset='link_formset',
            form_index=None,
            field=None,
            errors='Links must have unique anchors and URLs.'
        )

    def test_validation_fails_when_link_url_is_listed_more_than_once(self):
        self.client.login(username=self.standard_user.email, password='pass')

        response = self.client.post(
            reverse('accounts:profile-settings'),
            data = {
                'link-TOTAL_FORMS': 2,
                'link-INITIAL_FORMS': 0,
                'link-0-anchor': 'My Link',
                'link-0-url': 'http://mylink.com',
                'link-1-anchor': 'My Link 2',
                'link-1-url': 'http://mylink.com',
                'skill-TOTAL_FORMS': 0,
                'skill-INITIAL_FORMS': 0,
            }
        )

        self.assertFormsetError(
            response,
            formset='link_formset',
            form_index=None,
            field=None,
            errors='Links must have unique anchors and URLs.'
        )

    def test_validation_fails_when_link_has_anchor_but_no_url(self):
        self.client.login(username=self.standard_user.email, password='pass')

        response = self.client.post(
            reverse('accounts:profile-settings'),
            data = {
                'link-TOTAL_FORMS': 1,
                'link-INITIAL_FORMS': 0,
                'link-0-anchor': 'My Link',
                'link-0-url': '',
                'skill-TOTAL_FORMS': 0,
                'skill-INITIAL_FORMS': 0,
            }
        )

        self.assertFormsetError(
            response,
            formset='link_formset',
            form_index=None,
            field=None,
            errors='All links must have a URL.'
        )

    def test_validation_fails_when_link_has_url_but_no_anchor(self):
        self.client.login(username=self.standard_user.email, password='pass')

        response = self.client.post(
            reverse('accounts:profile-settings'),
            data = {
                'link-TOTAL_FORMS': 1,
                'link-INITIAL_FORMS': 0,
                'link-0-anchor': '',
                'link-0-url': 'http://mylink.com',
                'skill-TOTAL_FORMS': 0,
                'skill-INITIAL_FORMS': 0,
            }
        )

        self.assertFormsetError(
            response,
            formset='link_formset',
            form_index=None,
            field=None,
            errors='All links must have an anchor.'
        )


class AccountSettingsFormTest(TestCase):
    def setUp(self):
        self.user = UserFactory(email='thisemail@test.test')

    def test_validation_fails_if_users_submits_incorrect_current_password(self):
        form = AccountSettingsForm(
            user = self.user,
            data = {
                'email': 'thisemail@test.test',
                'current_password': 'wrongpass',
                'reset_password': 'newpass',
                'reset_password_confirm': 'newpass',
            }
        )

        self.assertFalse(form.is_valid())

    def test_validation_fails_if_user_tries_to_change_password_without_current_password(self):
        form = AccountSettingsForm(
            user = self.user,
            data = {
                'email': 'thisemail@test.test',
                'reset_password': 'newpass',
                'reset_password_confirm': 'newpass',
            }
        )

        self.assertFalse(form.is_valid())

    def test_validation_fails_if_user_tries_to_change_password_without_confirming_password(self):
        form = AccountSettingsForm(
            user = self.user,
            data = {
                'email': 'thisemail@test.test',
                'current_password': 'pass',
                'reset_password': 'newpass',
            }
        )

        self.assertFalse(form.is_valid())

    def test_password_validation_fails_when_new_passwords_are_different(self):
        form = AccountSettingsForm(
            user = self.user,
            data = {
                'email': 'thisemail@test.test',
                'current_password': 'pass',
                'reset_password': 'newpass',
                'reset_password_confirm': 'differentpass',
            }
        )

        self.assertFalse(form.is_valid())

    def test_password_validation_passes_when_all_fields_correct(self):
        form = AccountSettingsForm(
            user = self.user,
            data = {
                'email': 'thisemail@test.test',
                'current_password': 'pass',
                'reset_password': 'newpass',
                'reset_password_confirm': 'newpass',
            }
        )

        self.assertTrue(form.is_valid())


class CloseAccountFormTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_validation_fails_with_no_password(self):
        form = CloseAccountForm(
            user = self.user,
            data = {}
        )

        self.assertFalse(form.is_valid())

    def test_validation_fails_with_incorrect_password(self):
        form = CloseAccountForm(
            user = self.user,
            data = {
                'password': 'wrongpass',
            }
        )

        self.assertFalse(form.is_valid())

    def test_validation_passes_with_correct_password(self):
        form = CloseAccountForm(
            user = self.user,
            data = {
                'password': 'pass',
            }
        )

        self.assertTrue(form.is_valid())


# Utils.py

class AccountUtilsTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.standard_user = UserFactory(email='myuser@test.test')
        self.factory = RequestFactory()
        self.site = get_current_site(self.client.request)
        self.site.config = SiteConfigFactory(site=self.site)
        self.closed_user = UserFactory(
            email='closed.user@test.test',
            is_closed=True,
        )

    def test_create_inactive_user(self):
        user = create_inactive_user('test@test.test', 'first', 'last')
        moderators = Group.objects.get(name='moderators')

        self.assertEqual(user.email, 'test@test.test')
        self.assertEqual(user.first_name, 'first')
        self.assertEqual(user.last_name, 'last')
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.is_moderator, False)
        self.assertNotIn(moderators, user.groups.all())

    def test_reactivated_account_token_is_reset(self):
        initial_token = self.standard_user.auth_token
        request = self.factory.get(reverse('accounts:request-invitation'))
        user = invite_user_to_reactivate_account(self.standard_user, request)

        self.assertNotEqual(initial_token, user.auth_token)
        self.assertFalse(user.auth_token_is_used)

    def test_reactivation_email_sent_to_user(self):
        request = self.factory.get('/')
        invite_user_to_reactivate_account(self.closed_user, request)

        expected_subject = 'Reactivate your {} account'.format(self.site.name)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, expected_subject)

    def test_get_user(self):
        user = get_user('myuser@test.test')

        self.assertEqual(user, self.standard_user)


# Urls.py and views.py

class RequestInvitationTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.client = Client()
        self.site = get_current_site(self.client.request)
        self.site.config = SiteConfigFactory(site=self.site)
        self.moderator = ModeratorFactory()

    def test_request_invitation_url_resolves_to_request_invitation_view(self):
        url = resolve('/accounts/request-invitation')

        self.assertEqual(url.func, request_invitation)

    def test_requested_account_registration_recorded(self):
        response = self.client.post(
            reverse('accounts:request-invitation'),
            data = {
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
            data = {
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'new_test@test.test',
                'comments': 'Please give me an account',
            },
        )

        expected_subject = 'New account request at {}'.format(self.site.name)

        self.assertEqual(len(mail.outbox), 4) # 3 created as batch, plus original.
        self.assertEqual(mail.outbox[0].subject, expected_subject)

    def test_request_invitation_redirect(self):
        response = self.client.post(
            reverse('accounts:request-invitation'),
            data = {
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'new_test@test.test',
                'comments': 'Please give me an account',
            },
        )

        self.assertRedirects(response, '/accounts/request-invitation/done')


class ActivateAccountTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.invited_user = InvitedPendingFactory(
            email='validuser@test.test',
            auth_token='mytoken',
        )
        self.invalid_invited_user = InvitedPendingFactory(
            auth_token = 'invalid',
            auth_token_is_used = True,
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
            data = {
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
        self.client = Client()

    def test_profile_url_resolves_to_profile_settings_view(self):
        url = resolve('/accounts/profile')

        self.assertEqual(url.func, profile_settings)

    def test_profile_is_not_available_to_unauthenticated_users(self):
        response = self.client.get(reverse('accounts:profile-settings'))

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/accounts/profile',
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
            data = {
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


class AccountSettingsTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()
        self.client = Client()

    def test_account_settings_url_resolves_to_account_settings_view(self):
        url = resolve('/accounts/settings')

        self.assertEqual(url.func, account_settings)

    def test_account_settings_is_not_available_to_unauthenticated_users(self):
        response = self.client.get(reverse('accounts:account-settings'))

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/accounts/settings',
            status_code=302
        )

    def test_account_settings_is_available_to_authenticated_users(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('accounts:account-settings'))

        self.assertEqual(response.status_code, 200)

    def test_account_settings_form_is_rendered_to_page(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('accounts:account-settings'))
        expected_html = '<legend>Account Settings</legend>'

        self.assertInHTML(expected_html, response.content.decode())

    def test_close_account_form_is_rendered_to_page(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('accounts:account-settings'))
        expected_html = '<legend>Close Account</legend>'

        self.assertInHTML(expected_html, response.content.decode())

    def test_update_account_url_resolves_to_update_account_view(self):
        url = resolve('/accounts/settings/update')

        self.assertEqual(url.func, update_account)

    def test_update_account_not_available_to_unautheticated_users(self):
        response = self.client.post(
            reverse('accounts:update-account'),
            data = {
                'email': 'mynewemail@test.test',
            },
        )

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/accounts/settings/update',
            status_code=302
        )

    def test_update_account_not_available_without_POST_data(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('accounts:update-account'))

        self.assertEqual(response.status_code, 405)

    def test_update_account_is_available_to_authenticated_users_with_POST_data(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.post(
            reverse('accounts:update-account'),
            data = {
                'email': 'mynewemail@test.test',
            },
        )

        # Sending valid data should result in this view redirecting back
        # to account settings
        self.assertRedirects(
            response,
            '/accounts/settings',
            status_code=302
        )

    def test_can_update_email(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.post(
            reverse('accounts:update-account'),
            data = {
                'email': 'mynewemail@test.test',
            },
        )

        user = User.objects.get(id=self.standard_user.id)

        self.assertEqual(user.email, 'mynewemail@test.test')

    def test_can_update_password(self):
        self.client.login(username=self.standard_user.email, password='pass')
        old_pass = self.standard_user.password
        response = self.client.post(
            reverse('accounts:update-account'),
            data = {
                'email': self.standard_user.email,
                'current_password': 'pass',
                'reset_password': 'new',
                'reset_password_confirm': 'new',
            },
        )

        user = User.objects.get(id=self.standard_user.id)
        self.assertNotEqual(user.password, old_pass)

    def test_close_account_url_resolves_to_close_account_view(self):
        url = resolve('/accounts/close')

        self.assertEqual(url.func, close_account)


    def test_close_account_not_available_to_unautheticated_users(self):
        response = self.client.post(
            reverse('accounts:close-account'),
            data = {
                'password': 'pass',
            },
        )

        #Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/accounts/close',
            status_code=302
        )

    def test_close_account_not_available_without_POST_data(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('accounts:close-account'))

        self.assertEqual(response.status_code, 405)

    def test_close_account_is_available_to_authenticated_users_with_POST_data(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.post(
            reverse('accounts:close-account'),
            data = {
                'password': 'pass',
            },
        )

        # Sending valid data should result in this view redirecting to done
        self.assertRedirects(
            response,
            '/accounts/close/done',
            status_code=302
        )

    def test_can_close_account(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.post(
            reverse('accounts:close-account'),
            data = {
                'password': 'pass',
            },
        )

        user = User.objects.get(id=self.standard_user.id)

        self.assertFalse(user.is_active)
        self.assertTrue(user.is_closed)


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
            data = {
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
            data = {
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
            url='http://github.com/myaccount',
        )
        userlinks = [link,]

        match_link_to_brand(userlinks)
        link = UserLink.objects.get(user=link_user)

        self.assertEqual(link.icon, github)
