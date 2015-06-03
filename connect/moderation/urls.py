from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _

from connect.moderation import views

urlpatterns = patterns(
    '',
    url(r'^$', views.moderation_home, name='moderators'),
    url(_(r'^invite-user/$'), views.invite_user, name='invite-user'),
    url(_(r'^reinvite-user/$'), views.reinvite_user, name='reinvite-user'),
    url(_(r'^revoke-invitation/$'), views.revoke_invitation,
        name='revoke-invitation'),
    url(_(r'^review-applications/$'), views.review_applications,
        name='review-applications'),
    url(_(r'^review-abuse-reports/$'), views.review_abuse,
        name='review-abuse'),
    url(_(r'^logs/$'), views.view_logs, name='logs'),
    url(_(r'^(?P<user_id>\d+)/report-abuse/$'), views.report_abuse,
        name='report-abuse'),
    url(_(r'^abuse-report-logged/$'), TemplateView.as_view(
        template_name='moderation/abuse_report_logged.html'),
        name='abuse-report-logged'),
)
