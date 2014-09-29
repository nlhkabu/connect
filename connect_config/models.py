from django.contrib.sites.models import Site
from django.db import models


class SiteConfig(models.Model):
    """
    Site specific settings.
    """
    site = models.OneToOneField(Site, related_name='config')
    logo = models.ImageField(help_text='Must be no larger than 80px by 160px')
    tagline = models.CharField(max_length=200)
    email = models.EmailField(help_text='Email for receiving site-wide enquiries')
    email_header = models.ImageField(help_text='Header image on site generated emails.'
                                               'Must be 600px wide.'
                                               'Keep the file size as small as possible!')
    class Meta:
        verbose_name = 'Site Configuration'

    def __str__(self):
        return 'Config for {}'.format(self.site.name, self.tagline)





