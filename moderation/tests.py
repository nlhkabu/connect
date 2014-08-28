from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.utils.timezone import now

from accounts.tests import (create_active_moderator, create_superuser,
                            create_active_standard_user)
from .views import invite_member

User = get_user_model()

# Utils.py

#~class LogMessageTest(TestCase):
    #~
    #~def test_can_log_moderation_event(self):


# Urls.py and views.py

class ModerationHomeTest(TestCase):

    def test_moderation_url_resolves_to_moderation_home(self):
        found = resolve(reverse('moderation:moderators'))

        self.assertEqual(found.func, invite_member)

    def test_only_authenticated_users_can_access_moderation_home(self):
        c = self.client
        response = c.get(reverse('moderation:moderators'))
        # Unauthenticated user is redirected to login page
        self.assertEqual(response.status_code, 302)

    def test_standard_users_cannot_access_moderation_home(self):
        c = self.client
        user = create_active_standard_user()
        c.login(username=user.email, password='default')

        response = c.get(reverse('moderation:moderators'))
        # User lacking relevant permissions is redirected to login page
        self.assertEqual(response.status_code, 302)

    def test_moderators_can_access_moderation_home(self):
        c = self.client
        moderator = create_active_moderator()
        c.login(username=moderator.email, password='default')

        response = c.get(reverse('moderation:moderators'))
        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)


    #~def test_pending_users_show_in_list(self):
    #~def test_pending_users_are_invited_by_logged_in_moderator(self):
    #~def test_pending_users_are_not_invited_by_other_moderators(self):
    #~def test_invite_user_form_is_rendered_to_page(self):


#~class InviteUserTest(TestCase):
#~
    #~def test_can_log_invitation(self):
    #~def test_can_email_invited_user(self):


#~class ReInviteUserTest(TestCase):
#~
    #~def test_can_log_reinvitation(self):
    #~def test_can_email_reinvited_user(self):


#~class RevokeInvitationTest(TestCase):
#~
    #~def test_can_revoke_user_invitation(self):

#~class ReviewApplicationTest(TestCase):
#~
    #~def test_review_application_url_resolves_to_view(self):
    #~def test_only_authenticated_users_can_access_review_application_view(self):
    #~def test_standard_users_cannot_access_review_application_view(self):
    #~def test_moderators_can_access_review_application_view(self):
    #~def test_pending_applications_render_on_page(self):
#~
    #~def test_can_approve_application(self):
    #~def test_can_log_approval(self):
    #~def test_can_email_approved_user(self):

    #~def test_can_reject_application(self):
    #~def test_can_log_rejection(self):
    #~def test_can_email_rejected_user(self):


#~class ReportAbuseTest(TestCase):

    #~def test_report_abuse_url_resolves_to_view(self):
    #~def test_only_authenticated_users_can_report_abuse(self):
    #~def test_report_abuse_form_renders_on_page(self):
    #~def test_can_report_abuse(self):
    #~def test_can_email_moderators_alert_of_new_abuse_report(self):
    #~def test_moderator_does_not_recieve_email_about_report_regarding_themself(self):


#~class ReviewAbuseTest(TestCase):

    #~def test_review_abuse_url_resolves_to_view(self):
    #~def test_only_authenticated_users_can_access_review_abuse_view(self):
    #~def test_standard_users_cannot_access_review_abuse_view(self):
    #~def test_moderators_can_access_review_abuse_view(self):
    #~def test_abuse_reports_render_on_page(self):
    #~def test_previous_warnings_are_attached_to_accused_user(self):
    #~def test_moderator_cannot_see_abuse_reports_about_themself(self):
    #~def test_can_resolve_abuse_report(self):
    #~def test_can_log_dismissal(self):
    #~def test_can_log_warning(self):
    #~def test_can_log_ban(self):
    #~def test_can_send_email_to_reporting_user(self):
    #~def test_can_send_email_to_offending_user(self):


#~class ViewLogsTest(TestCase):

    #~def test_view_logs_url_resolves_to_view(self):
    #~def test_only_authenticated_users_can_access_view_logs_view(self):
    #~def test_standard_users_cannot_access_view_logs_view(self):
    #~def test_moderators_can_access_view_logs_view(self):
    #~def test_logs_render_on_page(self):
    #~def test_moderator_cannot_see_logs_about_themself(self):
    #~def test_can_filter_logs_by_type(self):

