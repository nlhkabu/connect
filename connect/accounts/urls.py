from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _

from connect.accounts.forms import CustomPasswordResetForm
from connect.accounts import views


reset_email_template = 'accounts/emails/password_reset_email.html'

urlpatterns = patterns(
    '',
    # Auth
    url(_(r'^login/$'), auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='login'),
    url(_(r'^logout/$'), auth_views.logout,
        {
            'next_page': '/',
            'template_name': 'accounts/login.html'
        },
        name='logout'),

    # page where user can request to reset their password
    url(_(r'^password/reset/$'), auth_views.password_reset,
        {'template_name': 'accounts/password_reset.html',
         'post_reset_redirect': '/accounts/password/reset/done/',
         'from_email': settings.EMAIL_HOST_USER,
         'current_app': 'accounts',
         'email_template_name': 'accounts/emails/password_reset_email.html',
         'html_email_template_name': reset_email_template,
         'subject_template_name': 'accounts/emails/password_reset_subject.txt',
         'password_reset_form': CustomPasswordResetForm},
        name="password-reset"),

    # page to confirm that email has been sent
    url(_(r'^password/reset/done/$'), auth_views.password_reset_done,
        {
            'template_name': 'accounts/password_reset_done.html',
            'current_app': 'accounts',
        },
        name="password-reset-done"),


    # page for user to change password (uses token sent in email)
    url(_(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$'),
        auth_views.password_reset_confirm,
        {
            'template_name': 'accounts/password_reset_confirm.html',
            'post_reset_redirect': '/accounts/password/done/',
            'current_app': 'accounts',
        },
        name="password-reset-confirm"),

    # page confirming password has been reset
    url(_(r'^password/reset/complete/$'),
        auth_views.password_reset_complete,
        {'template_name': 'accounts/password_reset_complete.html'},
        name="password-reset-complete"),

    # Request and activate account
    url(_(r'^request-invitation/$'), views.request_invitation,
        name='request-invitation'),
    url(_(r'^request-invitation/done/$'), TemplateView.as_view(
        template_name='accounts/request_invitation_done.html'),
        name='request-invitation-done'),
    url(_(r'^activate/(?P<token>\w+)$'), views.activate_account,
        name='activate-account'),

    # Profile settings
    url(_(r'^profile/$'), views.profile_settings, name='profile-settings'),

    # Account settings
    url(_(r'^update/email/$'), views.update_email, name='update-email'),
    url(_(r'^update/password/$'), views.update_password,
        name='update-password'),
    url(_(r'^close/$'), views.close_account, name='close-account'),
    url(_(r'^close/done/$'),
        TemplateView.as_view(template_name='accounts/close_account_done.html'),
        name='close-account-done'),
)
