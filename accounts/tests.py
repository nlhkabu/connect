from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.test import TestCase

class LoginPageTest(TestCase):

    def test_login_page_exists(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'id_username')
        self.assertContains(response, 'id_password')
