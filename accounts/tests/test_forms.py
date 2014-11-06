from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase

from connect_config.factories import SiteConfigFactory

from accounts.factories import (InvitedPendingFactory, RoleFactory,
                                SkillFactory, UserFactory)
from accounts.forms import (ActivateAccountForm, AccountSettingsForm,
                            BaseLinkFormSet, BaseSkillFormSet,
                            CloseAccountForm, LinkForm, ProfileForm,
                            RequestInvitationForm, SkillForm,
                            validate_email_availability)
from accounts.models import UserLink, UserSkill


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
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.closed_user = UserFactory(
            email='closed.user@test.test',
            is_closed=True,
        )

    def test_closed_account_prompts_custom_validation(self):
        response = self.client.post(
            reverse('accounts:request-invitation'),
            data={
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
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.pending_user = InvitedPendingFactory()

    def test_password_validation_fails_when_passwords_are_different(self):
        response = self.client.post(
            reverse('accounts:activate-account',
                     args=(self.pending_user.auth_token,)),
            data={
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
            user=self.pending_user,
            data={
                'first_name': 'First',
                'last_name': 'Last',
                'password': 'pass1',
                'confirm_password': 'pass1',
            }
        )

        self.assertTrue(form.is_valid())


class ProfileFormTest(TestCase):
    def setUp(self):
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.standard_user = UserFactory()

        # Setup skills and roles
        self.django = SkillFactory(name='django')
        self.rails = SkillFactory(name='rails')
        self.jquery = SkillFactory(name='jquery')

        self.mentor = RoleFactory(name='mentor')
        self.mentee = RoleFactory(name='mentee')

        self.client.login(username=self.standard_user.email, password='pass')

    def test_validation_fails_if_first_name_not_provided(self):
        form = ProfileForm(
            user=self.standard_user,
            data={
                'last_name': 'Last',
                'bio': 'My bio',
                'roles': [self.mentor.id, self.mentee.id],
            }
        )

        self.assertFalse(form.is_valid())

    def test_validation_fails_if_last_name_not_provided(self):
        form = ProfileForm(
            user=self.standard_user,
            data={
                'first_name': 'First',
                'bio': 'My bio',
                'roles': [self.mentor.id, self.mentee.id],
            }
        )

        self.assertFalse(form.is_valid())


    def test_skill_formset_validation_passes_with_correct_data(self):
        form = ProfileForm(
            user=self.standard_user,
            data={
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
            user=self.standard_user,
            data={
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
            data={
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
            data={
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
            data=
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
            user=self.standard_user,
            data={
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
            user=self.standard_user,
            data={
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
            data={
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
            data={
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
            data={
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
            data={
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
            user=self.user,
            data={
                'email': 'thisemail@test.test',
                'current_password': 'wrongpass',
                'reset_password': 'newpass',
                'reset_password_confirm': 'newpass',
            }
        )

        self.assertFalse(form.is_valid())

    def test_cannot_change_password_without_current_password(self):
        form = AccountSettingsForm(
            user=self.user,
            data={
                'email': 'thisemail@test.test',
                'reset_password': 'newpass',
                'reset_password_confirm': 'newpass',
            }
        )

        self.assertFalse(form.is_valid())

    def test_cannot_change_password_without_confirming_password(self):
        form = AccountSettingsForm(
            user=self.user,
            data={
                'email': 'thisemail@test.test',
                'current_password': 'pass',
                'reset_password': 'newpass',
            }
        )

        self.assertFalse(form.is_valid())

    def test_password_validation_fails_when_new_passwords_are_different(self):
        form = AccountSettingsForm(
            user=self.user,
            data={
                'email': 'thisemail@test.test',
                'current_password': 'pass',
                'reset_password': 'newpass',
                'reset_password_confirm': 'differentpass',
            }
        )

        self.assertFalse(form.is_valid())

    def test_password_validation_passes_when_all_fields_correct(self):
        form = AccountSettingsForm(
            user=self.user,
            data={
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
            user=self.user,
            data={}
        )

        self.assertFalse(form.is_valid())

    def test_validation_fails_with_incorrect_password(self):
        form = CloseAccountForm(
            user=self.user,
            data={
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
