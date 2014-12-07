from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.test import TestCase

from connect_config.factories import SiteConfigFactory

from accounts.factories import (InvitedPendingFactory, RoleFactory,
                                SkillFactory, UserFactory)
from accounts.forms import (ActivateAccountForm, BaseLinkFormSet,
                            BaseSkillFormSet, CloseAccountForm,
                            CustomUserCreationForm, CustomUserChangeForm,
                            LinkForm, ProfileForm, RequestInvitationForm,
                            SkillForm, UpdateEmailForm, UpdatePasswordForm)
from accounts.models import UserLink, UserSkill


#TODO: CustomPasswordResetForm(TestCase):

class CustomUserAdminTest(TestCase):
    def test_user_creation_form_does_not_contain_username_field(self):
        form = CustomUserCreationForm()
        self.assertNotIn('username', form.fields)

    def test_user_change_form_does_not_contain_username_field(self):
        form = CustomUserChangeForm()
        self.assertNotIn('username', form.fields)


class RequestInvitationFormTest(TestCase):
    def setUp(self):
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.closed_user = UserFactory(
            email='closed.user@test.test',
            is_closed=True,
        )
        self.existing_user = UserFactory(
            email='existing.user@test.test',
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

    def test_registered_email_prompts_custom_validation(self):
        response = self.client.post(
            reverse('accounts:request-invitation'),
            data={
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'existing.user@test.test',
                'comments': 'I would like an account',
            }
        )

        self.assertFormError(
            response,
            form='form',
            field='email',
            errors=('Sorry, this email address is already '
                    'registered to another user')
        )

class ActivateAccountFormTest(TestCase):
    def setUp(self):
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.pending_user = InvitedPendingFactory()

    def test_password_validation_fails_when_passwords_do_not_match(self):
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

    def test_password_validation_passes_when_passwords_match(self):
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
        # Setup Roles
        self.mentor = RoleFactory(name='mentor')
        self.mentee = RoleFactory(name='mentee')

        self.standard_user = UserFactory()
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

        errors = form['first_name'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'required')

    def test_validation_fails_if_last_name_not_provided(self):
        form = ProfileForm(
            user=self.standard_user,
            data={
                'first_name': 'First',
                'bio': 'My bio',
                'roles': [self.mentor.id, self.mentee.id],
            }
        )

        errors = form['last_name'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'required')


class SkillFormsetTest(TestCase):
    def setUp(self):
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.standard_user = UserFactory()

        # Setup skills
        self.django = SkillFactory(name='django')
        self.rails = SkillFactory(name='rails')
        self.jquery = SkillFactory(name='jquery')

        self.client.login(username=self.standard_user.email, password='pass')

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

    def test_validation_fails_when_skill_submitted_without_proficiency(self):
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

    def test_validation_fails_when_skill_is_submitted_without_skill_name(self):
        self.client.login(username=self.standard_user.email, password='pass')

        response = self.client.post(
            reverse('accounts:profile-settings'),
            data={
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
            errors='All skills must have a skill name.'
        )


class LinkFormsetTest(TestCase):
    def setUp(self):
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.standard_user = UserFactory()
        self.client.login(username=self.standard_user.email, password='pass')

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

    def test_validation_fails_when_anchor_is_submitted_more_than_once(self):
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

    def test_validation_fails_when_url_is_submitted_more_than_once(self):
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


class UpdateEmailFormTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory(email='standard.user@test.test')
        self.existing_user = UserFactory(email='existing.email@test.test')

    def test_validation_passes_if_all_data_is_valid(self):
        form = UpdateEmailForm(
            user=self.standard_user,
            data={
                'email': 'new.email@test.test',
                'password': 'pass',
            }
        )

        self.assertTrue(form.is_valid())

    def test_validation_fails_if_user_submits_incorrect_password(self):
        form = UpdateEmailForm(
            user=self.standard_user,
            data={
                'email': 'new.email@test.test',
                'password': 'wrongpass',
            }
        )

        errors = form['password'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'incorrect_pass')

    def test_validation_fails_if_email_is_already_registered_to_another_user(self):
        form = UpdateEmailForm(
            user=self.standard_user,
            data={
                'email': 'existing.email@test.test',
                'password': 'pass',
            }
        )

        errors = form['email'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'email_already_registered')


class UpdatePasswordFormTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory(email='standard.user@test.test')

    def test_validation_passes_if_all_data_is_valid(self):
        form = UpdatePasswordForm(
            user=self.standard_user,
            data={
                'new_password': 'newpass',
                'current_password': 'pass',
            }
        )

        self.assertTrue(form.is_valid())

    def test_validation_fails_with_no_new_password(self):
        form = UpdatePasswordForm(
            user=self.standard_user,
            data={}
        )

        errors = form['new_password'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'required')

    def test_validation_fails_if_user_submits_incorrect_current_password(self):
        form = UpdatePasswordForm(
            user=self.standard_user,
            data={
                'new_password': 'newpass',
                'current_password': 'wrongpass',
            }
        )

        errors = form['current_password'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'incorrect_pass')


class CloseAccountFormTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

    def test_validation_fails_with_no_password(self):
        form = CloseAccountForm(
            user=self.standard_user,
            data={}
        )

        errors = form['password'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'required')

    def test_validation_fails_with_incorrect_password(self):
        form = CloseAccountForm(
            user=self.standard_user,
            data={
                'password': 'wrongpass',
            }
        )

        errors = form['password'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'incorrect_pass')

    def test_validation_passes_with_correct_password(self):
        form = CloseAccountForm(
            user = self.standard_user,
            data = {
                'password': 'pass',
            }
        )

        self.assertTrue(form.is_valid())
