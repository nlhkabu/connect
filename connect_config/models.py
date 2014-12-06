from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SiteConfig(models.Model):
    """
    Site specific settings.
    """
    site = models.OneToOneField(Site, verbose_name=_('site'),
                                related_name='config')
    logo = models.ImageField(_('logo'),
                             help_text=_('Must be no larger than 80px by 160px'))
    tagline = models.CharField(_('site tagline'), max_length=200)
    email = models.EmailField(_('email'), help_text=_('Email for receiving '
                                                      'site-wide enquiries'))
    email_header = models.ImageField(_('email header'),
                                     help_text=_('Header image on site generated '
                                                 'emails. Must be 600px wide. '
                                                 'Keep the file size as '
                                                 'small as possible!'))
    class Meta:
        verbose_name = _('site configuration')
        verbose_name_plural = _('site configurations')

    def __str__(self):
        return _('Site configuration for {}'.format(self.site.name, self.tagline))





