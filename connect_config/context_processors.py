from django.contrib.sites.shortcuts import get_current_site
from .models import SiteConfig


def site_processor(request):
    """
    Make site details available to all templates.
    """
    site = get_current_site(request)

    try:
        site_config = SiteConfig.objects.get(site=site)
        site.logo = site_config.logo
        site.tagline = site_config.tagline
        site.email = site_config.email
        site.email_header = site_config.email_header
    except:
        pass

    return {'site': site }


