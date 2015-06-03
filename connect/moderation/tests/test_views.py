import datetime
import factory
import pytz

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve, reverse
from django.http import Http404
from django.utils import timezone

from connect.accounts.factories import (AbuseReportFactory, AbuseWarningFactory,
                                InvitedPendingFactory, ModeratorFactory,
                                RequestedPendingFactory, UserFactory)
from connect.accounts.models import AbuseReport, CustomUser
from connect.config.factories import SiteFactory, SiteConfigFactory
from connect.tests import BoostedTestCase as TestCase
from connect.moderation.factories import LogFactory
from connect.moderation.forms import FilterLogsForm
from connect.moderation.models import ModerationLogMsg
from connect.moderation.views import (moderation_home, report_abuse,
                              review_abuse, review_applications, view_logs)


User = get_user_model()


class ModerationHomeTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.standard_user = UserFactory()
        self.moderator = ModeratorFactory()

    def test_moderation_url(self):
        self.check_url('/moderation/', moderation_home)

    def test_unauthenticated_users_cannot_access_page(self):
        response = self.client.get(reverse('moderation:moderators'))

        # Unauthenticated user is redirected to login page
        self.assertRedirects(response, '/accounts/login/?next=/moderation/')

    def test_authenticated_standard_users_cannot_access_page(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('moderation:moderators'))

        # User lacking relevant permissions is redirected to login page
        self.assertRedirects(response, '/accounts/login/?next=/moderation/')

    def test_authenticated_moderators_can_access_page(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:moderators'))

        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderation/invite_member.html')

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
        """
        Test that we only see users who this particular moderator has invited.
        """
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


class InviteUserTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.site = get_current_site(self.client.request)
        self.site.config = SiteConfigFactory(site=self.site)

        self.moderator = ModeratorFactory(
            first_name='My',
            last_name='Moderator',
        )

        self.client.login(username=self.moderator.email, password='pass')

    def post_data(self):
        return self.client.post(
            reverse('moderation:invite-user'),
            data={
                'first_name': 'Hello',
                'last_name': 'There',
                'email': 'invite.user@test.test',
            },
            follow=True,
        )

    def test_invalid_data_returns_to_moderation_home(self):
        response = self.client.post(reverse('moderation:invite-user'),
            data={
                'first_name': 'Hello',
                'last_name': 'There',
                'email': 'invalid',
            },
            follow=True
        )

        first_name_val = 'value="Hello"'
        last_name_val = 'value="There"'

        self.assertIn(first_name_val, response.content.decode())
        self.assertIn(last_name_val, response.content.decode())

    def test_can_invite_new_user(self):
        self.post_data()
        user = User.objects.get(email='invite.user@test.test')

        self.assertTrue(user)
        self.assertEqual(user.first_name, 'Hello')
        self.assertEqual(user.last_name, 'There')

    def test_can_log_invitation(self):
        self.post_data()
        invited_user = User.objects.get(email='invite.user@test.test')
        expected_comment = 'My Moderator invited Hello There'
        log = ModerationLogMsg.objects.get(comment=expected_comment)

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.INVITATION)
        self.assertEqual(log.pertains_to, invited_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_email_invited_user(self):
        self.post_data()
        invited_user = User.objects.get(email='invite.user@test.test')
        expected_subject = 'Welcome to {}'.format(self.site.name)
        expected_recipient = 'invite.user@test.test'
        expected_intro = 'Hi {},'.format('Hello')
        expected_content = 'created for you at {}'.format(
            self.site.name
        )
        expected_url = 'http://testserver/accounts/activate/{}"'.format(
            invited_user.auth_token
        )
        expected_footer = 'My Moderator registered a new {} account'.format(
            self.site.name
        )

        email = mail.outbox[0]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(email.subject, expected_subject)
        self.assertEqual(email.to[0], expected_recipient)
        self.assertIn(expected_intro, email.body)
        self.assertIn(expected_content, email.body)
        self.assertIn(expected_url, email.alternatives[0][0])
        self.assertIn(expected_footer, email.body)

    def test_confirmation_message(self):
        response = self.post_data()
        messages = list(response.context['messages'])

        self.assertEqual(len(messages), 1)
        self.assertIn('has been invited to', str(messages[0]))


class ReInviteUserTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.site = get_current_site(self.client.request)
        self.site.config = SiteConfigFactory(site=self.site)

        self.moderator = ModeratorFactory(
            first_name='My',
            last_name='Moderator',
        )

        self.invited_user = InvitedPendingFactory(
            first_name='Hello',
            last_name='There',
            email='reinviteme@test.test',
            moderator=self.moderator,
            auth_token='myauthtoken',
        )

        self.client.login(username=self.moderator.email, password='pass')

    def post_data(self, user_id='', email=''):
        if not user_id:
            user_id = self.invited_user.id

        if not email:
            email = self.invited_user.email

        return self.client.post(
            reverse('moderation:reinvite-user'),
            data={
                'user_id': user_id,
                'email': email,
            },
            follow=True,
        )

    def test_invalid_email_returns_to_moderation_home(self):
        response = self.post_data(email='invalid')

        self.assertEqual(response.status_code, 200)
        self.assertIn('<legend>Invite a New Member</legend>',
                      response.content.decode())

    def test_reinvitation_reset_auth_token(self):
        response = self.post_data()
        reinvited_user = User.objects.get(id=self.invited_user.id)

        self.assertNotEqual(reinvited_user.auth_token, 'myauthtoken')

    def test_reinvitation_resets_email(self):
        """
        Test that when we reinvite a user using  a different email address,
        the new email is saved to the user's profile.
        """
        response = self.post_data(email='different.email@test.test')
        reinvited_user = User.objects.get(id=self.invited_user.id)

        self.assertEqual(reinvited_user.email, 'different.email@test.test')

    def test_can_log_reinvitation(self):
        response = self.post_data()
        expected_comment = 'My Moderator resent invitation to Hello There'
        reinvited_user = User.objects.get(id=self.invited_user.id)
        log = ModerationLogMsg.objects.get(comment=expected_comment)

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.REINVITATION)
        self.assertEqual(log.pertains_to, reinvited_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_email_reinvited_user(self):
        response = self.post_data()
        expected_subject = 'Activate your {} account'.format(self.site.name)
        expected_recipient = 'invite.user@test.test'
        expected_intro = 'Hi {},'.format('Hello')
        expected_content = 'you have not yet activated your'
        expected_footer = 'My Moderator registered a new {} account'.format(
            self.site.name
        )

        email = mail.outbox[0]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(email.subject, expected_subject)
        self.assertEqual(email.to[0], self.invited_user.email)
        self.assertIn(expected_intro, email.body)
        self.assertIn(expected_content, email.body)
        self.assertIn(expected_footer, email.body)

    def test_confirmation_message(self):
        response = self.post_data()
        messages = list(response.context['messages'])

        self.assertEqual(len(messages), 1)
        self.assertIn('has been reinvited to', str(messages[0]))


class RevokeInvitationTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.moderator = ModeratorFactory(
            first_name='My',
            last_name='Moderator',
        )

        self.other_moderator = ModeratorFactory()

        self.invited_user = InvitedPendingFactory(
            first_name='Revoke',
            last_name='Me',
            email='revokeme@test.test',
            moderator=self.moderator,
        )

        self.requested_user = RequestedPendingFactory()

        self.user_invited_by_another_moderator = InvitedPendingFactory(
            moderator=self.other_moderator,
        )

        self.client.login(username=self.moderator.email, password='pass')

    def post_data(self, confirm=True, user_id=''):
        if not user_id:
            user_id = self.invited_user.id

        return self.client.post(
            reverse('moderation:revoke-invitation'),
            data={
                'confirm': confirm,
                'user_id': user_id,
            },
            follow=True,
        )

    def test_missing_confirmation_returns_to_moderation_home(self):
        """
        Check that posting the form without confirmation is not valid.
        """
        response = self.post_data(confirm=False)

        self.assertEqual(response.status_code, 200)
        self.assertIn('<legend>Invite a New Member</legend>',
                      response.content.decode())

    def test_invalid_user_id_raises_404(self):
        """
        If we post to this view with an invalid (non-existatant) user ID, we
        should raise a 404.
        """
        response = self.post_data(user_id='999999')
        self.assertEqual(response.status_code, 404)

    def test_user_who_has_not_been_invited_raises_PermissionDenied(self):
        """
        If we try to revoke an invitation from a user that has not been invited
        (i.e. they have requested an account), we should raise a 403.
        """
        response = self.post_data(user_id=self.requested_user.id)
        self.assertEqual(response.status_code, 403)

    def test_user_id_invited_by_another_moderator_raises_PermissionDenied(self):
        """
        If we try to revoke an invitation that ANOTHER moderator has sent,
        i.e. by manually overriding the user_id, we should raise a 403.
        """
        response = self.post_data(user_id=self.user_invited_by_another_moderator.id)
        self.assertEqual(response.status_code, 403)

    def test_can_revoke_user_invitation(self):
        user = User.objects.get(id=self.invited_user.id)
        self.assertIsInstance(user, User)

        response = self.post_data()
        messages = list(response.context['messages'])

        self.assertEqual(len(messages), 1)
        self.assertIn('has been uninvited from', str(messages[0]))

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user.id)


class ReviewApplicationTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.site = get_current_site(self.client.request)
        self.site.config = SiteConfigFactory(site=self.site)

        self.standard_user = UserFactory()
        self.applied_user = RequestedPendingFactory()
        self.moderator = ModeratorFactory(
            first_name='My',
            last_name='Moderator',
        )

    def post_data(self, decision, comments, user_id=''):
        if not user_id:
            user_id = self.applied_user.id

        return self.client.post(
            reverse('moderation:review-applications'),
            data={
                'user_id': user_id,
                'decision': decision,
                'comments': comments,
            },
        )

    def approve_application(self):
        return self.post_data(CustomUser.APPROVED, 'Approved')

    def reject_application(self):
        return self.post_data(CustomUser.REJECTED, 'Spam Application')

    def test_review_application_url_resolves_to_view(self):
        url = resolve('/moderation/review-applications/')

        self.assertEqual(url.func, review_applications)

    def test_unauthenticated_users_cannot_see_page(self):
        response = self.client.get(reverse('moderation:review-applications'))

        # Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/review-applications/',
            status_code=302
        )

    def test_authenticated_standard_users_cannot_see_page(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('moderation:review-applications'))

        # User lacking relevant permissions is redirected to login page
        self.assertRedirects(
            response, '/accounts/login/?next=/moderation/review-applications/')

    def test_authenticated_moderators_can_review_application(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:review-applications'))

        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderation/review_applications.html')

    def test_pending_applications_show_in_list(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:review-applications'))

        # Check that the context includes the user we defined in Setup
        context_pending = response.context['pending']

        self.assertIn(self.applied_user, context_pending)
        self.assertEqual(len(context_pending), 1)

    def test_invalid_user_id_raises_404(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.post_data(user_id='12312312',
                                  decision=User.APPROVED,
                                  comments='comment')

        self.assertEqual(response.status_code, 404)

    def test_can_approve_application(self):
        self.assertFalse(self.applied_user.moderator)
        self.assertFalse(self.applied_user.moderator_decision)
        self.assertFalse(self.applied_user.auth_token)

        self.client.login(username=self.moderator.email, password='pass')
        response = self.approve_application()
        user = User.objects.get(id=self.applied_user.id)

        self.assertEqual(user.moderator, self.moderator)
        self.assertEqual(user.moderator_decision, CustomUser.APPROVED)
        self.assertTrue(user.auth_token)

    def test_can_log_approval(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.approve_application()
        log = ModerationLogMsg.objects.get(comment='Approved')

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.APPROVAL)
        self.assertEqual(log.pertains_to, self.applied_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_email_approved_user(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.approve_application()

        expected_subject = 'Welcome to {}'.format(self.site.name)
        expected_intro = 'Hi {},'.format('Hello')
        expected_content = 'created for you at {}'.format(
            self.site.name
        )
        expected_url = 'http://testserver/accounts/activate/{}'.format(
            self.applied_user.auth_token
        )
        expected_footer = 'My Moderator has approved your application'
        email = mail.outbox[0]

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(email.subject, expected_subject)
        self.assertEqual(email.to[0], self.applied_user.email)
        self.assertIn(expected_content, email.body)
        self.assertIn(expected_url, email.alternatives[0][0])
        self.assertIn(expected_footer, email.body)

    def test_can_reject_application(self):
        self.assertFalse(self.applied_user.moderator)
        self.assertFalse(self.applied_user.moderator_decision)

        self.client.login(username=self.moderator.email, password='pass')
        response = self.reject_application()
        user = User.objects.get(id=self.applied_user.id)

        self.assertEqual(user.moderator, self.moderator)
        self.assertEqual(user.moderator_decision, CustomUser.REJECTED)

    def test_can_log_rejection(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.reject_application()
        log = ModerationLogMsg.objects.get(comment='Spam Application')

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.REJECTION)
        self.assertEqual(log.pertains_to, self.applied_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_email_rejected_user(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.reject_application()
        expected_subject = ('Unfortunately, your application to {} '
                           'was not successful'.format(self.site.name))
        expected_intro = 'Hi {},'.format('Hello')
        expected_email = self.site.config.email
        expected_footer = 'you applied for a {} account'.format(self.site.name)
        email = mail.outbox[0]

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(email.subject, expected_subject)
        self.assertEqual(email.to[0], self.applied_user.email)
        self.assertIn(expected_email, email.body)
        self.assertIn(expected_footer, email.body)


class ReportAbuseTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.site = get_current_site(self.client.request)
        self.site.config = SiteConfigFactory(site=self.site)

        self.reporting_user = UserFactory()
        self.accused_user = UserFactory()
        self.moderator = ModeratorFactory()
        factory.create_batch(
            ModeratorFactory,
            10,
            moderator=self.moderator,
        )

    def get_page(self):
        return self.client.get(reverse(
            'moderation:report-abuse',
            kwargs={'user_id': self.accused_user.id}
        ))

    def post_data(self, logged_against, comments):
        return self.client.post(
            reverse(
                'moderation:report-abuse',
                kwargs={'user_id': logged_against},
            ),
            data={
                'logged_by': self.reporting_user.id,
                'logged_against': logged_against,
                'comments': comments,
            },
        )

    def report_standard_user(self):
        return self.post_data(self.accused_user.id, 'User is a spam account')

    def test_url(self):
        url = '/moderation/{}/report-abuse/'.format(self.accused_user.id)
        self.check_url(url, report_abuse)

    def test_unauthenticated_users_cannot_report_abuse(self):
        response = self.get_page()

        # Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/{}/report-abuse/'.format(
                self.accused_user.id
            ))

    def test_authenticated_users_can_report_abuse(self):
        self.client.login(username=self.reporting_user.email, password='pass')
        response = self.get_page()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderation/report_abuse.html')

    def test_report_abuse_form_called_in_view(self):
        self.client.login(username=self.reporting_user.email, password='pass')
        response = self.get_page()
        expected_html = ('<legend>Log an abuse report '
                         'against {}</legend>'.format(
                         self.accused_user.get_full_name()
                        ))

        self.assertInHTML(expected_html, response.content.decode())

    def test_can_report_abuse(self):
        self.client.login(username=self.reporting_user.email, password='pass')
        response = self.report_standard_user()
        report = AbuseReport.objects.get(logged_against=self.accused_user)

        self.assertIsInstance(report, AbuseReport)
        self.assertEqual(report.logged_by, self.reporting_user)
        self.assertEqual(report.logged_against, self.accused_user)
        self.assertEqual(report.abuse_comment, 'User is a spam account')

    def test_moderators_emailed_about_new_abuse_report(self):
        self.client.login(username=self.reporting_user.email, password='pass')
        response = self.report_standard_user()
        expected_subject = 'New abuse report at {}'.format(self.site.name)
        expected_intro = 'Hi {},'.format('Hello')
        expected_url = ('href="http://testserver/moderation/review-'
                       'abuse-reports/"')
        expected_footer = 'you are a moderator at {}'.format(self.site.name)
        email = mail.outbox[0]
        recipients = [message.to[0] for message in mail.outbox]

        self.assertEqual(len(mail.outbox), 11)
        self.assertEqual(email.subject, expected_subject)
        self.assertIn(self.moderator.email, recipients)
        self.assertIn(expected_url, email.alternatives[0][0])
        self.assertIn(expected_footer, email.body)

    def test_moderator_not_sent_email_regarding_report_about_themself(self):
        """
        Test that a moderator cannot receive an email regarding a report
        made against themself.
        """
        self.client.login(username=self.reporting_user.email, password='pass')
        response = self.post_data(self.moderator.id, 'This moderator is nasty')
        recipients = []

        for email in mail.outbox:
            recipients.append(email.to[0])

        self.assertEqual(len(mail.outbox), 10) # There are 10 other moderators
        self.assertNotIn(self.moderator.email, recipients)


class ReviewAbuseTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.site = get_current_site(self.client.request)
        self.site.config = SiteConfigFactory(site=self.site)

        self.standard_user = UserFactory()
        self.reporting_user = UserFactory()
        self.accused_user = UserFactory()
        self.moderator = ModeratorFactory()

        self.abuse_report = AbuseReportFactory(
            logged_against=self.accused_user,
            logged_by=self.reporting_user
        )
        self.abuse_warning = AbuseWarningFactory(
            logged_against=self.accused_user
        )

    def post_data(self, decision, comments, report_id=''):
        if not report_id:
            report_id = self.abuse_report.id

        return self.client.post(
            reverse('moderation:review-abuse'),
            data={
                'report_id': report_id,
                'decision': decision,
                'comments': comments,
            },
        )

    def dismiss_report(self):
        return self.post_data(AbuseReport.DISMISS, 'Spam Report')

    def warn_user(self):
        return self.post_data(AbuseReport.WARN, 'This is a warning')

    def ban_user(self):
        return self.post_data(AbuseReport.BAN, 'You are banned')

    def test_review_abuse_url(self):
        self.check_url('/moderation/review-abuse-reports/', review_abuse)

    def test_unauthenticated_users_cannot_access_reports(self):
        response = self.client.get(reverse('moderation:review-abuse'))

        # Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/review-abuse-reports/',
            status_code=302
        )

    def test_authenticated_standard_users_cannot_access_reports(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('moderation:review-abuse'))

        # User lacking relevant permissions is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/review-abuse-reports/')

    def test_authenticated_moderators_can_access_reports(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:review-abuse'))

        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderation/review_abuse.html')

    def test_only_undecided_abuse_reports_in_response(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:review-abuse'))
        context_reports = response.context['reports']

        self.assertEqual(len(context_reports), 1)
        self.assertIn(self.abuse_report, context_reports)

    def test_previous_warnings_are_attached_to_abuse_report(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:review-abuse'))

        context_reports = response.context['reports']
        self.assertEqual(len(context_reports), 1)

        context_report = context_reports[0]
        self.assertEqual(len(context_report.prior_warnings), 1)
        self.assertIn(self.abuse_warning, context_report.prior_warnings)

    def test_moderator_cannot_see_abuse_reports_about_themself(self):
        moderator_abuse_report = AbuseReportFactory(
            logged_against=self.moderator
        )

        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:review-abuse'))

        # We should only see self.abuse_report - as this is the only undecided
        # abuse report that is not about the logged in moderator
        context_reports = response.context['reports']

        self.assertEqual(len(context_reports), 1)
        self.assertIn(self.abuse_report, context_reports)

    def test_invalid_report_id_raises_404(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.post_data(AbuseReport.BAN, 'comment',
                                  report_id='7777777')

        self.assertEqual(response.status_code, 404)

    def test_can_dismiss_abuse_report(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.dismiss_report()
        report = AbuseReport.objects.get(id=self.abuse_report.id)

        self.assertEqual(report.moderator, self.moderator)
        self.assertEqual(report.moderator_decision, AbuseReport.DISMISS)
        self.assertEqual(report.moderator_comment, 'Spam Report')
        self.assertTrue(report.decision_datetime)

    def test_can_log_dismissal(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.dismiss_report()
        log = ModerationLogMsg.objects.get(comment='Spam Report')

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.DISMISSAL)
        self.assertEqual(log.pertains_to, self.accused_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_send_dismissal_email_to_reporting_user(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.dismiss_report()
        expected_subject = ('Your {} Abuse Report has'
                            ' been dismissed'.format(self.site.name))
        expected_intro = 'Hi {},'.format('Hello')
        expected_content = 'against {} at {}'.format(
            self.accused_user.get_full_name(),
            self.site.name
        )
        expected_email = self.site.config.email
        expected_footer = 'logged an abuse report at {}'.format(self.site.name)
        email = mail.outbox[0]

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(email.subject, expected_subject)
        self.assertEqual(email.to[0], self.reporting_user.email)
        self.assertIn(expected_content, email.body)
        self.assertIn('Spam Report', email.body)
        self.assertIn(expected_email, email.body)
        self.assertIn(expected_footer, email.body)

    def test_can_issue_warning(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.warn_user()
        report = AbuseReport.objects.get(id=self.abuse_report.id)

        self.assertEqual(report.moderator, self.moderator)
        self.assertEqual(report.moderator_decision, AbuseReport.WARN)
        self.assertEqual(report.moderator_comment, 'This is a warning')
        self.assertTrue(report.decision_datetime)

    def test_can_log_warning(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.warn_user()
        log = ModerationLogMsg.objects.get(comment='This is a warning')

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.WARNING)
        self.assertEqual(log.pertains_to, self.accused_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_send_warning_emails(self):
        """
        Test that both the accused user and user who made the report receive
        an email.
        """
        self.client.login(username=self.moderator.email, password='pass')
        response = self.warn_user()
        self.assertEqual(len(mail.outbox), 2)

        # Reporting user's email
        reporting_subject = ('{} has been issued a formal '
                             'warning from {}'.format(
                              self.accused_user.get_full_name(),
                              self.site.name,
                            ))

        reporting_intro = 'Hi {},'.format(
            self.reporting_user.first_name,
        )
        reporting_content = 'against {} at {}'.format(
            self.accused_user.get_full_name(),
            self.site.name
        )
        reporting_content_2 = "{}'s profile and will be flagged".format(
            self.accused_user.get_full_name()
        )
        reporting_footer = 'an abuse report at {}'.format(self.site.name)
        email = mail.outbox[0]

        self.assertEqual(email.subject, reporting_subject)
        self.assertEqual(email.to[0], self.reporting_user.email)
        self.assertIn(reporting_content, email.body)
        self.assertIn(reporting_content_2, email.body)
        self.assertIn(reporting_footer, email.body)

        # Offending user's email
        offending_subject = 'A formal warning from {}'.format(self.site.name)
        offending_intro = 'Hi {},'.format(
            self.accused_user.first_name,
        )
        offending_content = 'against you at {}'.format(self.site.name)
        offending_url = self.site.config.email
        offending_footer = 'logged against you at {}'.format(self.site.name)
        email = mail.outbox[1]

        self.assertEqual(email.subject, offending_subject)
        self.assertEqual(email.to[0], self.accused_user.email)
        self.assertIn(offending_content, email.body)
        self.assertIn('This is a warning', email.body)
        self.assertIn(offending_url, email.body)
        self.assertIn(offending_footer, email.body)

    def test_can_ban_user(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.ban_user()
        report = AbuseReport.objects.get(id=self.abuse_report.id)
        user = report.logged_against

        self.assertEqual(report.moderator, self.moderator)
        self.assertEqual(report.moderator_decision, AbuseReport.BAN)
        self.assertEqual(report.moderator_comment, 'You are banned')
        self.assertTrue(report.decision_datetime)
        self.assertFalse(user.is_active)

    def test_can_log_ban(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.ban_user()
        log = ModerationLogMsg.objects.get(comment='You are banned')

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.BANNING)
        self.assertEqual(log.pertains_to, self.accused_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_send_ban_emails(self):
        """
        Test that both the accused user and user who made the report receive
        an email.
        """
        self.client.login(username=self.moderator.email, password='pass')
        response = self.ban_user()
        self.assertEqual(len(mail.outbox), 2)

        # Reporting user's email
        reporting_subject = '{} has been banned from {}'.format(
            self.accused_user.get_full_name(),
            self.site.name
        )
        reporting_intro = 'Hi {},'.format(
            self.reporting_user.first_name,
        )
        reporting_content = 'against {} at {}'.format(
            self.accused_user.get_full_name(),
            self.site.name
        )
        reporting_content_2 = "decision to ban {}".format(
            self.accused_user.get_full_name()
        )
        reporting_footer = 'an abuse report at {}'.format(self.site.name)
        email = mail.outbox[0]

        self.assertEqual(email.subject, reporting_subject)
        self.assertEqual(email.to[0], self.reporting_user.email)
        self.assertIn(reporting_content, email.body)
        self.assertIn(reporting_content_2, email.body)
        self.assertIn('You are banned', email.body)
        self.assertIn(reporting_footer, email.body)

        # Offending user's email
        offending_subject = ('Your {} account has been terminated'
                            .format(self.site.name))
        offending_intro = 'Hi {},'.format(
            self.accused_user.first_name,
        )
        offending_content = 'against you at {}'.format(self.site.name)
        offending_content_2 = "ban you from future use of {}".format(
            self.site.name
        )
        offending_url = self.site.config.email
        offending_footer = 'logged against you at {}'.format(self.site.name)
        email = mail.outbox[1]

        self.assertEqual(email.subject, offending_subject)
        self.assertEqual(email.to[0], self.accused_user.email)
        self.assertIn(offending_content, email.body)
        self.assertIn(offending_content_2, email.body)
        self.assertIn('You are banned', email.body)
        self.assertIn(offending_url, email.body)
        self.assertIn(offending_footer, email.body)


class ViewLogsTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.standard_user = UserFactory()
        self.moderator = ModeratorFactory()

    def test_logs_url(self):
        self.check_url('/moderation/logs/', view_logs)

    def get_data(self, msg_type='ALL', period='ALL', start='', end=''):
        return self.client.get(
            reverse('moderation:logs'),
            data={
                'msg_type': msg_type,
                'period': period,
                'start_date': start,
                'end_date': end,
            },
        )

    def test_unauthenticated_users_cannot_view_logs(self):
        response = self.client.get(reverse('moderation:logs'))

        # Unauthenticated user is redirected to login page
        self.assertRedirects(
            response, '/accounts/login/?next=/moderation/logs/',
        )

    def test_authenticated_standard_users_cannot_view_logs(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('moderation:logs'))

        # User lacking relevant permissions is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/logs/')

    def test_authenticated_moderators_can_view_logs(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:logs'))

        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderation/logs.html')

    def test_logs_in_response(self):
        invitation_log = LogFactory()
        log_about_moderator = LogFactory(
            msg_type=ModerationLogMsg.DISMISSAL,
            pertains_to=self.moderator
        )

        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:logs'))
        context_logs = response.context['logs']

        self.assertEqual(len(context_logs), 1)
        self.assertIn(invitation_log, context_logs)

        # Check that the response does not include logs about the
        # logged in moderator
        self.assertNotIn(log_about_moderator, context_logs)

    def test_can_filter_logs_by_type(self):
        invitation_log = LogFactory()
        reinvitation_log = LogFactory(
            msg_type=ModerationLogMsg.REINVITATION
        )

        self.client.login(username=self.moderator.email, password='pass')
        response = self.get_data(ModerationLogMsg.INVITATION)
        context_logs = response.context['logs']

        self.assertEqual(len(context_logs), 1)
        self.assertIn(invitation_log, context_logs)
        self.assertNotIn(reinvitation_log, context_logs)

    def test_can_filter_logs_by_today(self):
        today_log = LogFactory()
        yesterday_log = LogFactory(
            msg_datetime=timezone.now() - timezone.timedelta(days=1)
        )

        self.client.login(username=self.moderator.email, password='pass')
        response = self.get_data(period=FilterLogsForm.TODAY)
        context_logs = response.context['logs']

        self.assertEqual(len(context_logs), 1)
        self.assertIn(today_log, context_logs)
        self.assertNotIn(yesterday_log, context_logs)

    def test_can_filter_logs_by_yesterday(self):
        today_log = LogFactory()
        yesterday_log = LogFactory(
            msg_datetime=timezone.now() - timezone.timedelta(days=1)
        )

        self.client.login(username=self.moderator.email, password='pass')
        response = self.get_data(period=FilterLogsForm.YESTERDAY)
        context_logs = response.context['logs']

        self.assertEqual(len(context_logs), 1)
        self.assertIn(yesterday_log, context_logs)
        self.assertNotIn(today_log, context_logs)

    def test_can_filter_logs_by_last_seven_days(self):
        today_log = LogFactory()
        this_week_log = LogFactory(
            msg_datetime=timezone.now() - timezone.timedelta(days=7)
        )
        last_month_log = LogFactory(
            msg_datetime=timezone.now() - timezone.timedelta(days=60)
        )

        self.client.login(username=self.moderator.email, password='pass')
        response = self.get_data(period=FilterLogsForm.THIS_WEEK)
        context_logs = response.context['logs']

        self.assertEqual(len(context_logs), 2)
        self.assertIn(today_log, context_logs)
        self.assertIn(this_week_log, context_logs)
        self.assertNotIn(last_month_log, context_logs)

    def test_can_filter_logs_by_custom_date_range(self):
        first_of_feb_log = LogFactory(
            msg_datetime=datetime.datetime(2014, 2, 1, 1, 1, 1, 1, pytz.UTC)
        )
        first_of_mar_log = LogFactory(
            msg_datetime=datetime.datetime(2014, 3, 1, 1, 1, 1, 1, pytz.UTC)
        )
        first_of_apr_log = LogFactory(
            msg_datetime=datetime.datetime(2014, 4, 1, 1, 1, 1, 1, pytz.UTC)
        )

        self.client.login(username=self.moderator.email, password='pass')
        response = self.get_data(ModerationLogMsg.INVITATION,
                                 FilterLogsForm.CUSTOM,
                                 '1/2/2014', '30/3/2014')
        context_logs = response.context['logs']

        self.assertEqual(len(context_logs), 2)
        self.assertIn(first_of_feb_log, context_logs)
        self.assertIn(first_of_feb_log, context_logs)
        self.assertNotIn(first_of_apr_log, context_logs)

    def test_can_filter_logs_by_type_and_date(self):
        today_invitation_log = LogFactory()
        today_reinvitation_log = LogFactory(
            msg_type=ModerationLogMsg.REINVITATION
        )
        yesterday_invitation_log = LogFactory(
            msg_datetime=timezone.now() - timezone.timedelta(days=1)
        )

        self.client.login(username=self.moderator.email, password='pass')
        response = self.get_data(ModerationLogMsg.INVITATION,
                                 FilterLogsForm.TODAY)
        context_logs = response.context['logs']

        self.assertEqual(len(context_logs), 1)
        self.assertIn(today_invitation_log, context_logs)
        self.assertNotIn(today_reinvitation_log, context_logs)
        self.assertNotIn(yesterday_invitation_log, context_logs)

