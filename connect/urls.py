from django.conf.urls import patterns, include, url

#TODO: Remove for production
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'discover.views.dashboard', name='dashboard'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^moderation/', include('moderation.urls', namespace='moderation')),
    url(r'^dashboard/', include('discover.urls', namespace='discover')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #TODO: Remove for production
