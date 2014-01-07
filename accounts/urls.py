from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
            'template_name': 'accounts/login.html'
        },
        name='logout'
    ),
)
