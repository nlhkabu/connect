from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
    # Auth
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'},
        name='login'
    ),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
            'template_name': 'accounts/login.html'
        },
        name='logout'
    ),
    url(r'^activate/(?P<token>\w+)$', 'accounts.views.activate_account', name='activate-account'),
    # Account settings
    url(r'^settings/$', 'accounts.views.account_settings', name='account-settings'),
    url(r'^profile/$', 'accounts.views.profile_settings', name='profile-settings'),
)
