from django.conf.urls import patterns, include, url

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
)
