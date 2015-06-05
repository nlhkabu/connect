from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext as _

from connect.config.factories import SiteConfigFactory

from connect.accounts.factories import (
    InvitedPendingFactory, RoleFactory, SkillFactory, UserFactory
)
from connect.accounts.forms import (
    ActivateAccountForm, CloseAccountForm,
    CustomUserCreationForm, CustomUserChangeForm,
    CustomPasswordResetForm, ProfileForm, UpdateEmailForm,
    UpdatePasswordForm
)
from connect.accounts.models import UserSkill


class CustomCustomPasswordResetFormTest(TestCase):
    """
    Test our cutomised reset password form.
    These tests are a modified version of those found at
    django.contrib.auth.tests.testforms
    """
    def setUp(self):
        self.user = UserFactory(email='test@test.test')

    def test_invalid_email(self):
        form = CustomPasswordResetForm({'email': 'not valid'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form['email'].errors,
                         [_('Please enter a valid email address.')])

    def test_nonexistent_email(self):
        """
        Test nonexistent email address. This should not fail because it would
        expose information about registered users.
        """
        form = CustomPasswordResetForm({'email': 'foo@bar.com'})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(mail.outbox), 0)

    def test_cleaned_data(self):
        form = CustomPasswordResetForm({'email': self.user.email})
        self.assertTrue(form.is_valid())
        form.save(domain_override='example.com')
        self.assertEqual(form.cleaned_data['email'], self.user.email)
        self.assertEqual(len(mail.outbox), 1)

    def test_custom_email_subject(self):
        data = {'email': 'test@test.test'}
        form = CustomPasswordResetForm(data)
        self.assertTrue(form.is_valid())
        # Since we're not providing a request object, we must provide a
        # domain_override to prevent the save operation from failing in the
        # potential case where contrib.sites is not installed. Refs #16412.
        form.save(domain_override='example.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         'Reset your example.com password')

    def test_inactive_user(self):
        """
        Test that inactive user cannot receive password reset email.
        """
        self.user.is_active = False
        self.user.save()
        form = CustomPasswordResetForm({'email': self.user.email})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(len(mail.outbox), 0)

    def test_unusable_password(self):
        data = {"email": "test@example.com"}
        form = CustomPasswordResetForm(data)
        self.assertTrue(form.is_valid())
        self.user.set_unusable_password()
        self.user.save()
        form = CustomPasswordResetForm(data)
        # The form itself is valid, but no email is sent
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(len(mail.outbox), 0)


class CustomUserAdminTest(TestCase):
    def test_user_creation_form(self):
        """
        Test that user creation form does not include a username.
        """
        form = CustomUserCreationForm()
        self.assertNotIn('username', form.fields)

    def test_user_change_form(self):
        """
        Test that user change form does not include a username
        """
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

    def post_data(self, email):
        return self.client.post(
            reverse('accounts:request-invitation'),
            data={
                'full_name': 'First Last',
                'email': email,
                'comments': 'Comments',
            }
        )

    def test_closed_account(self):
        """
        Test that an email address attached to a closed account prompts a
        custom validation message.
        """
        response = self.post_data(email='closed.user@test.test')

        self.assertFormError(
            response,
            form='form',
            field='email',
            errors='This email address is already registered to another '
            '(closed) account. To reactivate this account, '
            'please check your email inbox. To register a new '
            'account, please use a different email address.'
        )

    def test_registered_email(self):
        """
        Test that an email address registered to another user
        prompts an error.
        """
        response = self.post_data(email='existing.user@test.test')

        self.assertFormError(
            response,
            form='form',
            field='email',
            errors=('Sorry, this email address is already '
                    'registered to another user.')
        )


class ActivateAccountFormTest(TestCase):
    def setUp(self):
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.pending_user = InvitedPendingFactory()

    def test_unmatched_passwords(self):
        response = self.client.post(
            reverse('accounts:activate-account',
                    args=(self.pending_user.auth_token,)),
            data={
                'full_name': 'First Last',
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

    def test_matching_passwords(self):
        form = ActivateAccountForm(
            user=self.pending_user,
            data={
                'full_name': 'First Last',
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

    def form_data(self, name):
        return ProfileForm(
            user=self.standard_user,
            data={
                'full_name': name,
                'bio': 'My bio',
                'roles': [self.mentor.id, self.mentee.id],
            }
        )

    def test_valid_data(self):
        form = self.form_data('First Last')

        self.assertTrue(form.is_valid())

    def test_missing_full_name(self):
        form = self.form_data('')
        errors = form['full_name'].errors.as_data()

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

    def form_data(self, skill, proficiency):
        return ProfileForm(
            user=self.standard_user,
            data={
                'full_name': 'First Last',
                'link-TOTAL_FORMS': 0,
                'link-INITIAL_FORMS': 0,
                'skill-TOTAL_FORMS': 1,
                'skill-INITIAL_FORMS': 0,
                'skill-0-skill': skill,
                'skill-0-proficiency': proficiency,
            }
        )

    def post_data(self, skill1, proficiency1, skill2='', proficiency2=''):
        return self.client.post(
            reverse('accounts:profile-settings'),
            data={
                'link-TOTAL_FORMS': 0,
                'link-INITIAL_FORMS': 0,
                'skill-TOTAL_FORMS': 2,
                'skill-INITIAL_FORMS': 0,
                'skill-0-skill': skill1,
                'skill-0-proficiency': proficiency1,
                'skill-1-skill': skill2,
                'skill-1-proficiency': proficiency2,
            }
        )

    def raise_formset_error(self, response, error):
        return self.assertFormsetError(
            response,
            formset='skill_formset',
            form_index=None,
            field=None,
            errors=error
        )

    def test_valid_data(self):
        form = self.form_data(self.django.id, UserSkill.BEGINNER)

        self.assertTrue(form.is_valid())

    def test_empty_fields(self):
        """
        Test validation passes when no data is provided
        (data is not required).
        """
        form = self.form_data('', '')

        self.assertTrue(form.is_valid())

    def test_duplicate_skills(self):
        """
        Test validation fails when skill is listed more than once.
        """
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.post_data(self.django.id, UserSkill.BEGINNER,
                                  self.django.id, UserSkill.INTERMEDIATE)

        self.raise_formset_error(response,
                                 'Each skill can only be entered once.')

    def test_skill_without_proficiency(self):
        """
        Test validation fails when a skill is passed without a proficiency.
        """
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.post_data(self.django.id, '')

        self.raise_formset_error(response,
                                 'All skills must have a proficiency.')

    def test_proficiency_without_skill_name(self):
        """
        Test validation fails when a proficiency is passed without being
        attached to a skill.
        """
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.post_data('', UserSkill.BEGINNER)

        self.raise_formset_error(response,
                                 'All skills must have a skill name.')


class LinkFormsetTest(TestCase):
    def setUp(self):
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.standard_user = UserFactory()
        self.client.login(username=self.standard_user.email, password='pass')

    def form_data(self, anchor, url):
        return ProfileForm(
            user=self.standard_user,
            data={
                'full_name': 'First Last',
                'link-TOTAL_FORMS': 1,
                'link-INITIAL_FORMS': 0,
                'skill-TOTAL_FORMS': 0,
                'skill-INITIAL_FORMS': 0,
                'link-0-anchor': anchor,
                'link-0-url': url,
            }
        )

    def post_data(self, anchor1, url1, anchor2='', url2=''):
        return self.client.post(
            reverse('accounts:profile-settings'),
            data={
                'link-TOTAL_FORMS': 2,
                'link-INITIAL_FORMS': 0,
                'skill-TOTAL_FORMS': 0,
                'skill-INITIAL_FORMS': 0,
                'link-0-anchor': anchor1,
                'link-0-url': url1,
                'link-1-anchor': anchor2,
                'link-1-url': url2,
            }
        )

    def raise_formset_error(self, response, error):
        self.assertFormsetError(
            response,
            formset='link_formset',
            form_index=None,
            field=None,
            errors=error
        )

    def test_valid_data(self):
        form = self.form_data('My Link', 'http://mylink.com')

        self.assertTrue(form.is_valid())

    def test_empty_fields(self):
        """
        Test validation passes when no data is provided
        (data is not required).
        """
        form = self.form_data('', '')

        self.assertTrue(form.is_valid())

    def test_duplicate_anchors(self):
        """
        Test validation fails when an anchor is submitted more than once.
        """
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.post_data('My Link', 'http://mylink.com',
                                  'My Link', 'http://mylink2.com')

        self.raise_formset_error(response,
                                 'Links must have unique anchors and URLs.')

    def test_duplicate_url(self):
        """
        Test validation fails when a URL is submitted more than once.
        """
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.post_data('My Link', 'http://mylink.com',
                                  'My Link2', 'http://mylink.com')

        self.raise_formset_error(response,
                                 'Links must have unique anchors and URLs.')

    def test_anchor_without_url(self):
        """
        Test validation fails when a link is submitted without a URL.
        """
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.post_data('My Link', '')

        self.raise_formset_error(response, 'All links must have a URL.')

    def test_url_without_anchor(self):
        """
        Test validation fails when a link is submitted without an anchor.
        """
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.post_data('', 'http://mylink.com')

        self.raise_formset_error(response, 'All links must have an anchor.')


class UpdateEmailFormTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory(email='standard.user@test.test')
        self.existing_user = UserFactory(email='existing.email@test.test')

    def form_data(self, email='new.email@test.test', password='pass'):
        return UpdateEmailForm(
            user=self.standard_user,
            data={
                'email': email,
                'password': password,
            }
        )

    def test_valid_data(self):
        form = self.form_data()

        self.assertTrue(form.is_valid())

    def test_incorrect_password(self):
        form = self.form_data(password='wrongpass')
        errors = form['password'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'incorrect_pass')

    def test_registered_email(self):
        """
        Test validation fails if the submitted email is already registered
        to another user.
        """
        form = self.form_data('existing.email@test.test')
        errors = form['email'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'email_already_registered')


class UpdatePasswordFormTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory(email='standard.user@test.test')

    def form_data(self, new='newpass', current='pass'):
        return UpdatePasswordForm(
            user=self.standard_user,
            data={
                'new_password': new,
                'current_password': current,
            }
        )

    def test_valid_data(self):
        form = self.form_data()

        self.assertTrue(form.is_valid())

    def test_missing_new_password(self):
        form = self.form_data('')
        errors = form['new_password'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'required')

    def test_incorrect_current_password(self):
        form = self.form_data(current='wrongpass')

        errors = form['current_password'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'incorrect_pass')


class CloseAccountFormTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

    def form_data(self, password='pass'):
        return CloseAccountForm(
            user=self.standard_user,
            data={'password': password}
        )

    def test_valid_data(self):
        form = self.form_data()

        self.assertTrue(form.is_valid())

    def test_no_password(self):
        form = self.form_data('')
        errors = form['password'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'required')

    def test_incorrect_password(self):
        form = self.form_data('wrongpass')
        errors = form['password'].errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'incorrect_pass')
