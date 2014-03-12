from django.conf.urls import patterns, url
from moderation import views

urlpatterns = patterns('',
    url(r'^$', 'moderation.views.invite_member', name='moderators'),
    url(r'^review-membership-applications$', 'moderation.views.review_applications', name='review-applications'),
    url(r'^review-abuse-reports$', 'moderation.views.review_abuse', name='review-abuse'),
    url(r'^logs$', 'moderation.views.view_logs', name='logs'),
    url(r'^request-invitation$', 'moderation.views.request_invitation', name='request-invitation'),
    url(r'^(?P<user_id>\d+)/report-abuse$', 'moderation.views.report_abuse', name='report-abuse'),
)
