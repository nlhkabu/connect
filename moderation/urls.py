from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from moderation import views

urlpatterns = patterns('',
    url(r'^$', 'moderation.views.moderation_home', name='moderators'),
    url(r'^invite-user$', 'moderation.views.invite_user', name='invite-user'),
    url(r'^reinvite-user$', 'moderation.views.reinvite_user', name='reinvite-user'),
    url(r'^revoke-invitation$', 'moderation.views.revoke_invitation', name='revoke-invitation'),
    url(r'^review-applications$', 'moderation.views.review_applications', name='review-applications'),
    url(r'^review-abuse-reports$', 'moderation.views.review_abuse', name='review-abuse'),
    url(r'^logs$', 'moderation.views.view_logs', name='logs'),
    url(r'^(?P<user_id>\d+)/report-abuse$', 'moderation.views.report_abuse', name='report-abuse'),
    url(r'^abuse-report-logged$',
        TemplateView.as_view(template_name='moderation/abuse_report_logged.html'),
        name="abuse-report-logged"),
)
