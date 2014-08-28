from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

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

    # page where user can request to reset their password
    url(r'^password/reset/$',
        'django.contrib.auth.views.password_reset',
        {
            'template_name': 'accounts/password_reset.html',
            'post_reset_redirect': '/accounts/password/reset/done/',
            'from_email': settings.EMAIL_HOST_USER,
            'current_app': 'accounts',
            'email_template_name': 'accounts/emails/password_reset_email.html',
            'html_email_template_name': 'accounts/emails/password_reset_email.html',
        },
        name="password_reset"
    ),

    # page to confirm that email has been sent
    url(r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {
            'template_name': 'accounts/password_reset_done.html',
            'current_app' : 'accounts',
        },
        name="password_reset_done"
    ),


    # page for user to change password (uses token sent in email)
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {
            'template_name': 'accounts/password_reset_confirm.html',
            'post_reset_redirect': '/accounts/password/done/',
            'current_app' : 'accounts',
        },
        name="password_reset_confirm"
    ),

    # page confirming password has been reset
    url(r'^password/done/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'accounts/password_reset_complete.html',},
        name="pasword_reset_complete"
    ),

    # Request and activate account
    url(r'^request-invitation$', 'accounts.views.request_invitation', name='request-invitation'),
    url(r'^request-invitation/done$',
        TemplateView.as_view(template_name='accounts/request_invitation_done.html'),
        name='request-invitation-done'),
    url(r'^activate/(?P<token>\w+)$', 'accounts.views.activate_account', name='activate-account'),

    # Profile settings
    url(r'^profile/$', 'accounts.views.profile_settings', name='profile-settings'),

    # Account settings
    url(r'^settings/$', 'accounts.views.account_settings', name='account-settings'),
    url(r'^settings/update$', 'accounts.views.update_account', name='update-account'),
    url(r'^close$', 'accounts.views.close_account', name='close-account'),
    url(r'^close/done$',
        TemplateView.as_view(template_name='accounts/close_account_done.html'),
        name='close-account-done'),
)
