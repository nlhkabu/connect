import factory

from django.contrib.sites.models import Site

from connect.config.models import SiteConfig


class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site

    name = factory.Sequence(lambda n: "site%s" % n)
    domain = factory.Sequence(lambda n: "site%s.com" % n)


class SiteConfigFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SiteConfig

    site = factory.SubFactory(Site)
    logo = factory.django.ImageField(filename='my_log.png', format='PNG')
    email = factory.Sequence(lambda n: "site.email%s@test.test" % n)
    tagline = 'A tagline'
    email_header = factory.django.ImageField(filename='my_image.png', format='PNG')
