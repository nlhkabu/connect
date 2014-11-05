from django.test import TestCase

from .utils import generate_salt, hash_time


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

    #~def test_can_send_html_email(self):
    #~def test_can_send_plaintext_email(self):
    #~def test_can_send_connect_email(self):
