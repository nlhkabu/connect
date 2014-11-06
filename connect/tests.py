from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.test import Client, TestCase

from accounts.factories import UserFactory
from connect_config.factories import SiteConfigFactory
from .utils import (generate_salt, generate_html_email, hash_time,
                    send_connect_email)

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

    def test_can_send_html_email(self):
        subject = 'Test email'
        from_address = 'from@test.test'
        recipients = ['to@test.test']
        site_name = 'My Site'
        html_template='emails/email_base.html'
        template_vars={
            'site_name': site_name,
        }

        email = generate_html_email(subject, from_address, recipients,
                                    html_template, template_vars)

        expected_string = 'you are a registered user at My Site.'

        self.assertEqual(email.subject, subject)
        self.assertEqual(email.from_email, from_address)
        self.assertEqual(email.to, recipients)
        self.assertIn(expected_string, email.body)
        self.assertIn('<html>', email.alternatives[0][0])


    def test_can_send_connect_email(self):
        subject = 'Test email'
        template = 'emails/email_base.html'
        recipient = UserFactory(email='recipient@test.test')
        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)
        # Sender != from email, but rather the user who has sent the message
        sender = UserFactory(email='sender@test.test')
        url = 'http://testurl.com'
        comments = 'comment',
        logged_against = UserFactory(email='accused@test.test')

        email = send_connect_email(subject, template, recipient, site, sender,
                                   url, comments, logged_against)

        self.assertEqual(email.subject, subject)
        self.assertEqual(email.to[0], recipient.email)
