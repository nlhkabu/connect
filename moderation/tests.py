import datetime
import factory
import pytz

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import resolve, reverse
from django.test import Client, TestCase
from django.utils import timezone

from accounts.factories import (InvitedPendingFactory, ModeratorFactory,
                                RequestedPendingFactory, UserFactory)
from accounts.models import CustomUser

from connect_config.factories import SiteFactory, SiteConfigFactory

from .models import ModerationLogMsg
from .utils import log_moderator_event, get_date_limits
from .views import moderation_home, review_applications

User = get_user_model()

# Forms.py

#~class TestFilterLogsFormValidation(TestCase):

    #~def test_validation_fails_if_custom_is_selected_but_no_start_date_is_specified(self):
    #~def test_validation_fails_if_custom_is_selected_but_no_end_date_is_specified(self):


# Utils.py

class LogMessageTest(TestCase):
    fixtures = ['group_perms']

    def test_can_log_moderation_event(self):

        msg_type = ModerationLogMsg.INVITATION
        user = UserFactory()
        moderator = ModeratorFactory()
        comment = 'This is my comment'

        log = log_moderator_event(
            msg_type=user,
            user=user,
            moderator=moderator,
            comment=comment
        )

        logs = ModerationLogMsg.objects.all()

        self.assertIn(log, logs)

    def test_date_limits_with_one_date(self):
        date = datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC)
        expected_start = datetime.datetime(2011, 8, 15, 0, 0, 0, 0, pytz.UTC)
        expected_end = datetime.datetime(2011, 8, 15, 23, 59, 59, 999999, pytz.UTC)

        start, end = get_date_limits(date)

        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    def test_date_limits_with_two_dates(self):
        day_1 = datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC)
        day_2 = datetime.datetime(2011, 9, 1, 8, 15, 12, 0, pytz.UTC)

        expected_start = datetime.datetime(2011, 8, 15, 0, 0, 0, 0, pytz.UTC)
        expected_end = datetime.datetime(2011, 9, 1, 23, 59, 59, 999999, pytz.UTC)

        start, end = get_date_limits(day_1, day_2)

        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    #~def test_date_limits_passing_non_UTC_timezone(self):



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

    #~def test_invite_user_form(self):
        #~Check that the form submits to the correct view

    #~def test_reinvite_user_form(self):
        #~# check that this form submits to the correct view

    #~def test_revoke_user_form(self):
        #~# check that this form submits to the correct view



class InviteUserTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.client = Client()

        self.moderator = ModeratorFactory(
            first_name='My',
            last_name='Moderator',
        )

        self.client.login(username=self.moderator.email, password='pass')

        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

        self.client.post(
            reverse('moderation:invite-user'),
            data = {
                'first_name' : 'Hello',
                'last_name' : 'There',
                'email' : 'invite.user@test.test',
            },
        )

    def tearDown(self):
        self.client.logout()

    def test_can_invite_new_user(self):
        user = User.objects.get(email='invite.user@test.test')

        self.assertTrue(user)
        self.assertEqual(user.first_name, 'Hello')
        self.assertEqual(user.last_name, 'There')

    def test_can_log_invitation(self):
        expected_comment = 'My Moderator invited Hello There'
        invited_user = user = User.objects.get(email='invite.user@test.test')
        log = ModerationLogMsg.objects.get(comment=expected_comment)

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.INVITATION)
        self.assertEqual(log.pertains_to, invited_user)
        self.assertEqual(log.logged_by, self.moderator)

    #~def test_can_email_invited_user(self):


class ReInviteUserTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.client = Client()

        self.moderator = ModeratorFactory(
            first_name='My',
            last_name='Moderator',
        )

        self.existing = UserFactory(
            first_name='Hello',
            last_name='There',
            email='reinviteme@test.test',
            moderator = self.moderator,
        )

        self.client.login(username=self.moderator.email, password='pass')

        site = get_current_site(self.client.request)
        site.config = SiteConfigFactory(site=site)

    def tearDown(self):
        self.client.logout()

    def test_reinvitation_resets_email(self):
        self.client.post(
            reverse('moderation:reinvite-user'),
            data = {
                'user_id' : self.existing.id,
                'email' : 'different.email@test.test',
            },
        )
        reinvited = User.objects.get(id=self.existing.id)

        self.assertEqual(reinvited.email, 'different.email@test.test')

    def test_can_log_reinvitation(self):
        self.client.post(
            reverse('moderation:reinvite-user'),
            data = {
                'user_id' : self.existing.id,
                'email' : self.existing.email,
            },
        )
        expected_comment = 'My Moderator resent invitation to Hello There'
        reinvited = User.objects.get(id=self.existing.id)
        log = ModerationLogMsg.objects.get(comment=expected_comment)

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.REINVITATION)
        self.assertEqual(log.pertains_to, reinvited)
        self.assertEqual(log.logged_by, self.moderator)

    #~def test_can_email_reinvited_user(self):


class RevokeInvitationTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.client = Client()

        self.moderator = ModeratorFactory(
            first_name='My',
            last_name='Moderator',
        )

        self.existing = UserFactory(
            first_name='Revoke',
            last_name='Me',
            email='revokeme@test.test',
            moderator = self.moderator,
        )

        self.client.login(username=self.moderator.email, password='pass')

    def tearDown(self):
        self.client.logout()

    def test_can_revoke_user_invitation(self):
        user = User.objects.get(id=self.existing.id)
        self.assertIsInstance(user, User)

        self.client.post(
            reverse('moderation:revoke-invitation'),
            data = {
                'confirm' : True,
                'user_id' : self.existing.id,
            },
        )

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.existing.id)


class ReviewApplicationTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.client = Client()
        self.standard = UserFactory()
        self.moderator = ModeratorFactory()
        self.applied = RequestedPendingFactory()

    def test_review_application_url_resolves_to_view(self):
        url = resolve('/moderation/review-applications')

        self.assertEqual(url.func, review_applications)

    def test_unauthenticated_users_cannot_access_review_application(self):
        response = self.client.get(reverse('moderation:review-applications'))

        # Unauthenticated user is redirected to login page
        self.assertEqual(response.status_code, 302)

    def test_authenticated_standard_users_cannot_access_review_application(self):
        self.client.login(username=self.standard.email, password='pass')
        response = self.client.get(reverse('moderation:review-applications'))

        # User lacking relevant permissions is redirected to login page
        self.assertEqual(response.status_code, 302)

    def test_authenticated_moderators_can_access_review_application(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:review-applications'))

        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)

    def test_pending_applications_show_in_list(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:review-applications'))

        # Check that the context includes the user we defined in Setup
        context_pending = response.context['pending'][0]

        self.assertEqual(context_pending, self.applied)

    #~def test_can_approve_application(self):
        #~self.assertFalse(self.applied.is_active)
#~
        #~self.client.login(username=self.moderator.email, password='pass')
        #~self.client.post(
            #~reverse('moderation:review-applications'),
            #~data = {
                #~'user_id' : self.applied.id,
                #~'decision' : CustomUser.APPROVED,
                #~'comments' : 'Applicant is known to the community',
            #~},
        #~)
#~
        #~self.assertTrue(self.applied.is_active)

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
    #~def test_moderators_emailed_about_new_abuse_report(self):
    #~def test_moderator_is_not_send_email_about_report_about_themself(self):


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

