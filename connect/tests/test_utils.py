from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.test import TestCase

from accounts.factories import UserFactory
from connect_config.factories import SiteFactory, SiteConfigFactory
from connect.settings import MEDIA_ROOT
from connect.utils import generate_salt, hash_time, send_connect_email


class UtilsTest(TestCase):
    def test_can_generate_standard_salt(self):
        salt = generate_salt()

        self.assertEqual(len(salt), 8)
        self.assertRegexpMatches(salt, '\w')

    def test_can_generate_longer_salt(self):
        salt = generate_salt(10)

        self.assertEqual(len(salt), 10)
        self.assertRegexpMatches(salt, '\w')

    def test_can_create_unique_hash(self):
        hash_1 = hash_time()
        hash_2 = hash_time()

        self.assertEqual(len(hash_1), 30)
        self.assertRegexpMatches(hash_1, '\w')
        self.assertNotEqual(hash_1, hash_2)

    def test_can_send_connect_email(self):
        subject = 'Test email'
        template = 'emails/email_base.html'
        recipient = UserFactory(email='recipient@test.test')
        site = SiteFactory(domain='mydomain.com')
        site.config = SiteConfigFactory(site=site)

        # Sender != from email, but rather the user who has sent the message
        sender = UserFactory(email='sender@test.test')
        url = 'http://testurl.com'
        comments = 'comment',
        logged_against = UserFactory(email='accused@test.test')

        email = send_connect_email(subject, template, recipient, site, sender,
                                   url, comments, logged_against)

        self.assertEqual(email, 1) # send_email returns no. of emails sent
