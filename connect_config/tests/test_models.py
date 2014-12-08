from django.test import TestCase

from connect_config.factories import SiteConfigFactory, SiteFactory

class SiteConfigTest(TestCase):
    def test_string_method(self):
        site = SiteFactory(name='MySite')
        config = SiteConfigFactory(site=site)

        self.assertEqual(config.__str__(), 'Site configuration for MySite')
