from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'accounts/login.html',
            'extra_context': {'next': '/'}
        },
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
    url(r'^moderators/$', 'accounts.views.moderators', name='moderators'),
)
