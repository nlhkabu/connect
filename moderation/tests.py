import factory

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.test import Client, TestCase
from django.utils.timezone import now

from accounts.factories import InvitedPendingFactory, ModeratorFactory, UserFactory
from accounts.models import CustomUser

from .views import moderation_home

User = get_user_model()

# Forms.py

#~class TestFilterLogsFormValidation(TestCase):

    #~def test_validation_fails_if_custom_is_selected_but_no_start_date_is_specified(self):
    #~def test_validation_fails_if_custom_is_selected_but_no_end_date_is_specified(self):


# Utils.py

#~class LogMessageTest(TestCase):
    #~
    #~def test_can_log_moderation_event(self):


# Urls.py and views.py

class ModerationHomeTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.client = Client()
        self.standard = UserFactory()
        self.moderator = ModeratorFactory()

    def test_moderation_url_resolves_to_moderation_home(self):
        url = resolve('/moderation/')

        self.assertEqual(url.func, moderation_home)

    def test_unauthenticated_users_cannot_access_moderation_home(self):
        response = self.client.get(reverse('moderation:moderators'))

        # Unauthenticated user is redirected to login page
        self.assertEqual(response.status_code, 302)

    def test_authenticated_standard_users_cannot_access_moderation_home(self):
        self.client.login(username=self.standard.email, password='pass')
        response = self.client.get(reverse('moderation:moderators'))

        # User lacking relevant permissions is redirected to login page
        self.assertEqual(response.status_code, 302)

    def test_authenticated_moderators_can_access_moderation_home(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:moderators'))

        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)

    def test_pending_users_show_in_list(self):
        pending = factory.create_batch(
            InvitedPendingFactory,
            10,
            moderator=self.moderator,
        )

        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:moderators'))

        context_pending = list(response.context['pending'])

        self.assertCountEqual(context_pending, pending)

    def test_pending_users_are_not_invited_by_other_moderators(self):
        other_moderator = ModeratorFactory()
        pending = factory.create_batch(
            InvitedPendingFactory,
            10,
            moderator=other_moderator,
        )

        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:moderators'))
        # Should be empty...
        context_pending = list(response.context['pending'])

        self.assertFalse(context_pending)

    def test_invite_user_form_is_rendered_to_page(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:moderators'))
        expected_html = '<legend>Invite a New Member</legend>'

        self.assertInHTML(expected_html, response.content.decode())

    #~def test_submit_invite_user_form(self):
        #~self.client.login(username=self.moderator.email, password='pass')
        #~response = self.client.get(reverse('moderation:moderators'))
#~
        #~Check that the form submits to the correct view




#~class InviteUserTest(TestCase):
    #~fixtures = ['group_perms']
#~
    #~def setUp(self):
        #~self.client = Client()
        #~self.moderator = ModeratorFactory()
#~
        #~self.client.login(username=self.moderator.email, password='pass')
        #~self.client.post(
            #~reverse('moderation:invite-user'),
            #~data = {
                #~'first_name' : 'Hello',
                #~'last_name' : 'There',
                #~'email' : 'invite.user@test.test',
            #~},
        #~)
#~
    #~def tearDown(self):
        #~self.client.logout()
#~
    #~def test_can_invite_new_user(self):
        #~user = User.objects.get(email='invite.user@test.test')
#~
        #~pass
        #~assertTrue(user)
        #~assertEqual(user.first_name, 'Hello')
        #~assertEqual(user.last_name, 'There')

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
    #~def test_can_filter_logs_by_type_and_date(self):
    #~def test_can_filter_logs_by_today(self):
    #~def test_can_filter_logs_by_yesterday(self):
    #~def test_can_filter_logs_by_last_seven_days(self):
    #~def test_can_filter_logs_by_custom_date_range(self):

