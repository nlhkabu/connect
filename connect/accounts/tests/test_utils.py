from django.contrib.auth.models import Group
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.test import TestCase, RequestFactory

from connect.config.factories import SiteConfigFactory

from connect.accounts.factories import UserFactory
from connect.accounts.utils import (
    create_inactive_user, get_user, invite_user_to_reactivate_account,
    validate_email_availability
)


class AccountUtilsTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.standard_user = UserFactory(email='my.user@test.test')
        self.factory = RequestFactory()
        self.site = get_current_site(self.client.request)
        self.site.config = SiteConfigFactory(site=self.site)
        self.closed_user = UserFactory(
            full_name='Closed',
            email='closed.user@test.test',
            is_closed=True,
        )

    def test_create_inactive_user(self):
        user = create_inactive_user('test@test.test', 'first last')
        moderators = Group.objects.get(name='moderators')

        self.assertEqual(user.email, 'test@test.test')
        self.assertEqual(user.full_name, 'first last')
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.is_moderator, False)
        self.assertNotIn(moderators, user.groups.all())

    def test_reactivated_account_token_is_reset(self):
        """
        Test that when a closed account is reactivated, their auth token
        is reset.
        """
        initial_token = self.standard_user.auth_token
        request = self.factory.get(reverse('accounts:request-invitation'))
        user = invite_user_to_reactivate_account(self.standard_user, request)

        self.assertNotEqual(initial_token, user.auth_token)
        self.assertFalse(user.auth_token_is_used)

    def test_reactivation_email_sent_to_user(self):
        """
        Test that when a closed account is reactivated, they are sent an
        activation email.
        """
        request = self.factory.get('/')
        invite_user_to_reactivate_account(self.closed_user, request)

        expected_subject = 'Reactivate your {} account'.format(self.site.name)
        expected_intro = 'Hi {},'.format(self.closed_user.full_name)
        expected_content = '{} using this email address.'.format(
            self.site.name)
        expected_url = 'http://testserver/accounts/activate/{}'.format(
            self.closed_user.auth_token
        )
        email = mail.outbox[0]

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(email.subject, expected_subject)
        self.assertIn(expected_intro, email.body)
        self.assertIn(expected_content, email.body)
        self.assertIn(expected_url, email.body)

    def test_get_user(self):
        user = get_user('my.user@test.test')

        self.assertEqual(user, self.standard_user)

    def test_unregistered_email(self):
        """
        Test that an email not registered to another user is returned as True.
        i.e. It is available for another user to use.
        """
        unregistered = validate_email_availability(
            'unregistered.user@test.test')
        self.assertTrue(unregistered)

    def test_registered_email(self):
        """
        Test that an email registered to another user is returned as False.
        i.e. It is NOT available for another user to use.
        """
        with self.assertRaises(ValidationError):
            validate_email_availability('my.user@test.test')
