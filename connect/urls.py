from django.conf.urls import patterns, include, url

#TODO: Remove for production
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(
        r'^$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'accounts/login.html',
            'extra_context': {'next': '/dashboard'}
        },
        name='login'
    ),

    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^dashboard/', include('profiles.urls', namespace='profile')),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #TODO: Remove for production
