from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.test import TestCase

from connect.accounts.factories import UserFactory
from connect.config.factories import SiteFactory, SiteConfigFactory
from connect.utils import generate_unique_id, send_connect_email


class UtilsTest(TestCase):

    def test_generate_unique_id(self):
        uid = generate_unique_id()
        self.assertEqual(len(uid), 30)
        self.assertRegexpMatches(uid, '^\w+$')


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
