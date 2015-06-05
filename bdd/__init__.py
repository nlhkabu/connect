from django.test import TestCase
from django.core.urlresolvers import resolve, reverse

class BoostedTestCase(TestCase):
    """
    Custom test case that adds helpful utilities to Django's built in
    functionality.
    """
    def check_url(self, url, view):
        url = resolve(url)
        self.assertEqual(url.func, view)

    def check_template(self, url, template):
        response = self.client.get(reverse(url))
        self.assertTemplateUsed(response, template)
