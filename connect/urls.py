from django.conf.urls import patterns, include, url
from django.contrib.flatpages import urls as flatpages_urls
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from connect.accounts import urls as accounts_urls
from connect.moderation import urls as moderation_urls
from connect.connection import urls as connect_urls
from connect.discover import urls as discover_urls
from connect.discover.views import dashboard


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(_(r'^admin/'), include(admin.site.urls)),
    url(r'^$', dashboard, name='dashboard'),
    url(_(r'^accounts/'), include(accounts_urls, namespace='accounts')),
    url(_(r'^moderation/'), include(moderation_urls, namespace='moderation')),
    url(_(r'^connections/'), include(connect_urls, namespace='connections')),
    url(_(r'^dashboard/'), include(discover_urls, namespace='discover')),
    url(_(r'^pages/'), include(flatpages_urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
