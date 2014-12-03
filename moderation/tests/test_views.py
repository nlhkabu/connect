import datetime
import factory
import pytz

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.utils import timezone

from accounts.factories import (AbuseReportFactory, AbuseWarningFactory,
                                InvitedPendingFactory, ModeratorFactory,
                                RequestedPendingFactory, UserFactory)

from accounts.models import AbuseReport, CustomUser

from connect_config.factories import SiteFactory, SiteConfigFactory

from moderation.factories import LogFactory
from moderation.forms import FilterLogsForm
from moderation.models import ModerationLogMsg
from moderation.views import (moderation_home, report_abuse,
                              review_abuse, review_applications, view_logs)


User = get_user_model()


class ModerationHomeTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.standard_user = UserFactory()
        self.moderator = ModeratorFactory()

    def test_moderation_url_resolves_to_moderation_home(self):
        url = resolve('/moderation/')

        self.assertEqual(url.func, moderation_home)

    def test_unauthenticated_users_cannot_access_moderation_home(self):
        response = self.client.get(reverse('moderation:moderators'))

        # Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/',
            status_code=302
        )

    def test_authenticated_standard_users_cannot_access_moderation_home(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('moderation:moderators'))

        # User lacking relevant permissions is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/',
            status_code=302
        )

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
        self.response = self.client.post(
            reverse('moderation:invite-user'),
            data={
                'first_name': 'Hello',
                'last_name': 'There',
                'email': 'invite.user@test.test',
            },
            follow=True,
        )

        self.invited_user = user = User.objects.get(
            email='invite.user@test.test'
        )

    def test_can_invite_new_user(self):
        user = User.objects.get(email='invite.user@test.test')

        self.assertTrue(user)
        self.assertEqual(user.first_name, 'Hello')
        self.assertEqual(user.last_name, 'There')

    def test_can_log_invitation(self):
        expected_comment = 'My Moderator invited Hello There'

        log = ModerationLogMsg.objects.get(comment=expected_comment)

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.INVITATION)
        self.assertEqual(log.pertains_to, self.invited_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_email_invited_user(self):
        expected_subject = 'Welcome to {}'.format(self.site.name)
        expected_recipient = 'invite.user@test.test'
        expected_intro = 'Hi {},'.format('Hello')
        expected_content = 'created for you at {}'.format(
            self.site.name
        )
        expected_url = 'http://testserver/accounts/activate/{}'.format(
            self.invited_user.auth_token
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
        messages = list(self.response.context['messages'])

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

        self.existing = UserFactory(
            first_name='Hello',
            last_name='There',
            email='reinviteme@test.test',
            moderator=self.moderator,
        )

        self.client.login(username=self.moderator.email, password='pass')

    def test_reinvitation_resets_email(self):
        self.client.post(
            reverse('moderation:reinvite-user'),
            data={
                'user_id': self.existing.id,
                'email': 'different.email@test.test',
            },
        )
        reinvited_user = User.objects.get(id=self.existing.id)

        self.assertEqual(reinvited_user.email, 'different.email@test.test')

    def test_can_log_reinvitation(self):
        self.client.post(
            reverse('moderation:reinvite-user'),
            data={
                'user_id': self.existing.id,
                'email': self.existing.email,
            },
        )
        expected_comment = 'My Moderator resent invitation to Hello There'
        reinvited_user = User.objects.get(id=self.existing.id)
        log = ModerationLogMsg.objects.get(comment=expected_comment)

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.REINVITATION)
        self.assertEqual(log.pertains_to, reinvited_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_email_reinvited_user(self):
        self.client.post(
            reverse('moderation:reinvite-user'),
            data={
                'user_id': self.existing.id,
                'email': self.existing.email,
            },
        )

        expected_subject = 'Activate your {} account'.format(self.site.name)
        expected_recipient = 'invite.user@test.test'
        expected_intro = 'Hi {},'.format('Hello')
        expected_content = 'created for you at {}'.format(
            self.site.name
        )
        expected_url = 'http://testserver/accounts/activate/{}'.format(
            self.existing.auth_token
        )
        expected_footer = 'My Moderator registered a new {} account'.format(
            self.site.name
        )

        email = mail.outbox[0]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(email.subject, expected_subject)
        self.assertEqual(email.to[0], self.existing.email)
        self.assertIn(expected_intro, email.body)
        self.assertIn(expected_content, email.body)
        self.assertIn(expected_url, email.alternatives[0][0])
        self.assertIn(expected_footer, email.body)

    def test_confirmation_message(self):
        response = self.client.post(
            reverse('moderation:reinvite-user'),
            data={
                'user_id': self.existing.id,
                'email': self.existing.email,
            },
            follow=True,
        )

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

        self.existing_user = UserFactory(
            first_name='Revoke',
            last_name='Me',
            email='revokeme@test.test',
            moderator=self.moderator,
        )

        self.client.login(username=self.moderator.email, password='pass')

    def test_can_revoke_user_invitation(self):
        user = User.objects.get(id=self.existing_user.id)
        self.assertIsInstance(user, User)

        response = self.client.post(
            reverse('moderation:revoke-invitation'),
            data={
                'confirm': True,
                'user_id': self.existing_user.id,
            },
            follow=True,
        )

        messages = list(response.context['messages'])

        self.assertEqual(len(messages), 1)
        self.assertIn('has been uninvited from', str(messages[0]))

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.existing_user.id)


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

    def test_review_application_url_resolves_to_view(self):
        url = resolve('/moderation/review-applications/')

        self.assertEqual(url.func, review_applications)

    def test_unauthenticated_users_cannot_access_review_application(self):
        response = self.client.get(reverse('moderation:review-applications'))

        # Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/review-applications/',
            status_code=302
        )

    def test_authenticated_standard_users_cannot_access_review_application(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('moderation:review-applications'))

        # User lacking relevant permissions is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/review-applications/',
            status_code=302
        )

    def test_authenticated_moderators_can_access_review_application(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:review-applications'))

        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)

    def test_pending_applications_show_in_list(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:review-applications'))

        # Check that the context includes the user we defined in Setup
        context_pending = response.context['pending']

        self.assertIn(self.applied_user, context_pending)
        self.assertEqual(len(context_pending), 1)

    def test_can_approve_application(self):
        self.assertFalse(self.applied_user.moderator)
        self.assertFalse(self.applied_user.moderator_decision)
        self.assertFalse(self.applied_user.auth_token)

        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-applications'),
            data={
                'user_id': self.applied_user.id,
                'decision': CustomUser.APPROVED,
                'comments': 'Applicant is known to the community',
            },
        )

        user = User.objects.get(id=self.applied_user.id)

        self.assertEqual(user.moderator, self.moderator)
        self.assertEqual(user.moderator_decision, CustomUser.APPROVED)
        self.assertTrue(user.auth_token)

    def test_can_log_approval(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-applications'),
            data={
                'user_id': self.applied_user.id,
                'decision': CustomUser.APPROVED,
                'comments': 'Applicant is known to the community',
            },
        )

        log = ModerationLogMsg.objects.get(
            comment='Applicant is known to the community'
        )

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.APPROVAL)
        self.assertEqual(log.pertains_to, self.applied_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_email_approved_user(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-applications'),
            data={
                'user_id': self.applied_user.id,
                'decision': CustomUser.APPROVED,
                'comments': 'Applicant is known to the community',
            },
        )

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
        response = self.client.post(
            reverse('moderation:review-applications'),
            data={
                'user_id': self.applied_user.id,
                'decision': CustomUser.REJECTED,
                'comments': 'Spam Application',
            },
        )

        user = User.objects.get(id=self.applied_user.id)

        self.assertEqual(user.moderator, self.moderator)
        self.assertEqual(user.moderator_decision, CustomUser.REJECTED)

    def test_can_log_rejection(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-applications'),
            data={
                'user_id': self.applied_user.id,
                'decision': CustomUser.REJECTED,
                'comments': 'Spam Application',
            },
        )

        log = ModerationLogMsg.objects.get(comment='Spam Application')

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.REJECTION)
        self.assertEqual(log.pertains_to, self.applied_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_email_rejected_user(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-applications'),
            data={
                'user_id': self.applied_user.id,
                'decision': CustomUser.REJECTED,
                'comments': 'Spam Application',
            },
        )

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

    def test_report_abuse_url_resolves_to_report_abuse_view(self):
        url = resolve(
            '/moderation/{}/report-abuse/'.format(self.accused_user.id)
        )

        self.assertEqual(url.func, report_abuse)

    def test_unauthenticated_users_cannot_report_abuse(self):
        response = self.client.get(reverse(
            'moderation:report-abuse',
            kwargs={'user_id': self.accused_user.id}
        ))

        # Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/{}/report-abuse/'.format(
                self.accused_user.id
            ),
            status_code=302
        )

    def test_authenticated_users_can_report_abuse(self):
        self.client.login(username=self.reporting_user.email, password='pass')

        response = self.client.get(reverse(
            'moderation:report-abuse',
            kwargs={'user_id': self.accused_user.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_report_abuse_form_called_in_view(self):
        self.client.login(username=self.reporting_user.email, password='pass')

        response = self.client.get(reverse(
            'moderation:report-abuse',
            kwargs={'user_id': self.accused_user.id}
        ))

        expected_html = ('<legend>Log an abuse report '
                         'against {}</legend>'.format(
                         self.accused_user.get_full_name()
                        ))

        self.assertInHTML(expected_html, response.content.decode())

    def test_can_report_abuse(self):
        self.client.login(username=self.reporting_user.email, password='pass')

        response = self.client.post(
            reverse(
                'moderation:report-abuse',
                kwargs={'user_id': self.accused_user.id},
            ),
            data={
                'logged_by': self.reporting_user.id,
                'logged_against': self.accused_user.id,
                'comments': 'User is a spam account',
            },
        )

        report = AbuseReport.objects.get(logged_against=self.accused_user)

        self.assertIsInstance(report, AbuseReport)
        self.assertEqual(report.logged_by, self.reporting_user)
        self.assertEqual(report.logged_against, self.accused_user)
        self.assertEqual(report.abuse_comment, 'User is a spam account')

    def test_moderators_emailed_about_new_abuse_report(self):
        self.client.login(username=self.reporting_user.email, password='pass')

        response = self.client.post(
            reverse(
                'moderation:report-abuse',
                kwargs={'user_id': self.accused_user.id},
            ),
            data={
                'logged_by': self.reporting_user.id,
                'logged_against': self.accused_user.id,
                'comments': 'User is a spam account',
            },
        )

        expected_subject = 'New abuse report at {}'.format(self.site.name)
        expected_intro = 'Hi {},'.format('Hello')
        expected_url = ('href="http://testserver/moderation/review-'
                       'abuse-reports/">review')
        expected_footer = 'you are a moderator at {}'.format(self.site.name)
        email = mail.outbox[0]
        recipients = [message.to[0] for message in mail.outbox]

        self.assertEqual(len(mail.outbox), 11)
        self.assertEqual(email.subject, expected_subject)
        self.assertIn(self.moderator.email, recipients)
        self.assertIn(expected_url, email.alternatives[0][0])
        self.assertIn(expected_footer, email.body)

    def test_moderator_not_sent_email_regarding_report_about_themself(self):
        self.client.login(username=self.reporting_user.email, password='pass')

        response = self.client.post(
            reverse(
                'moderation:report-abuse',
                kwargs={'user_id': self.accused_user.id},
            ),
            data={
                'logged_by': self.reporting_user.id,
                'logged_against': self.moderator.id,
                'comments': 'This moderator is not nice',
            },
        )

        recipients = []

        for email in mail.outbox:
            recipients.append(email.to[0])

        self.assertEqual(len(mail.outbox), 10)
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

    def test_review_abuse_url_resolves_to_view(self):
        url = resolve('/moderation/review-abuse-reports/')

        self.assertEqual(url.func, review_abuse)

    def test_unauthenticated_users_cannot_access_review_abuse_reports(self):
        response = self.client.get(reverse('moderation:review-abuse'))

        # Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/review-abuse-reports/',
            status_code=302
        )

    def test_authenticated_standard_users_cannot_review_abuse_reports(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('moderation:review-abuse'))

        # User lacking relevant permissions is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/review-abuse-reports/',
            status_code=302
        )

    def test_authenticated_moderators_can_access_review_application(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:review-abuse'))

        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)

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

    def test_can_dismiss_abuse_report(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-abuse'),
            data={
                'report_id': self.abuse_report.id,
                'decision': AbuseReport.DISMISS,
                'comments': 'Spam Report',
            },
        )

        report = AbuseReport.objects.get(id=self.abuse_report.id)

        self.assertEqual(report.moderator, self.moderator)
        self.assertEqual(report.moderator_decision, AbuseReport.DISMISS)
        self.assertEqual(report.moderator_comment, 'Spam Report')
        self.assertTrue(report.decision_datetime)

    def test_can_log_dismissal(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-abuse'),
            data={
                'report_id': self.abuse_report.id,
                'decision': AbuseReport.DISMISS,
                'comments': 'Spam Report',
            },
        )

        log = ModerationLogMsg.objects.get(comment='Spam Report')

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.DISMISSAL)
        self.assertEqual(log.pertains_to, self.accused_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_send_dismissal_email_to_reporting_user(self):
        self.client.login(username=self.moderator.email, password='pass')
        comments = 'Spam Report'
        response = self.client.post(
            reverse('moderation:review-abuse'),
            data={
                'report_id': self.abuse_report.id,
                'decision': AbuseReport.DISMISS,
                'comments': comments,
            },
        )

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
        self.assertIn(comments, email.body)
        self.assertIn(expected_email, email.body)
        self.assertIn(expected_footer, email.body)

    def test_can_issue_warning(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-abuse'),
            data={
                'report_id': self.abuse_report.id,
                'decision': AbuseReport.WARN,
                'comments': 'This is a warning',
            },
        )
        report = AbuseReport.objects.get(id=self.abuse_report.id)

        self.assertEqual(report.moderator, self.moderator)
        self.assertEqual(report.moderator_decision, AbuseReport.WARN)
        self.assertEqual(report.moderator_comment, 'This is a warning')
        self.assertTrue(report.decision_datetime)

    def test_can_log_warning(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-abuse'),
            data={
                'report_id': self.abuse_report.id,
                'decision': AbuseReport.WARN,
                'comments': 'This is a warning',
            },
        )

        log = ModerationLogMsg.objects.get(comment='This is a warning')

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.WARNING)
        self.assertEqual(log.pertains_to, self.accused_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_send_warning_emails(self):
        self.client.login(username=self.moderator.email, password='pass')
        comments = 'This is a warning'
        response = self.client.post(
            reverse('moderation:review-abuse'),
            data={
                'report_id': self.abuse_report.id,
                'decision': AbuseReport.WARN,
                'comments': comments,
            },
        )

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
        self.assertIn(comments, email.body)
        self.assertIn(offending_url, email.body)
        self.assertIn(offending_footer, email.body)

    def test_can_ban_user(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-abuse'),
            data={
                'report_id': self.abuse_report.id,
                'decision': AbuseReport.BAN,
                'comments': 'You are banned',
            },
        )

        report = AbuseReport.objects.get(id=self.abuse_report.id)
        user = report.logged_against

        self.assertEqual(report.moderator, self.moderator)
        self.assertEqual(report.moderator_decision, AbuseReport.BAN)
        self.assertEqual(report.moderator_comment, 'You are banned')
        self.assertTrue(report.decision_datetime)
        self.assertFalse(user.is_active)

    def test_can_log_ban(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-abuse'),
            data={
                'report_id': self.abuse_report.id,
                'decision': AbuseReport.BAN,
                'comments': 'You are banned',
            },
        )

        log = ModerationLogMsg.objects.get(comment='You are banned')

        self.assertIsInstance(log, ModerationLogMsg)
        self.assertEqual(log.msg_type, ModerationLogMsg.BANNING)
        self.assertEqual(log.pertains_to, self.accused_user)
        self.assertEqual(log.logged_by, self.moderator)

    def test_can_send_ban_emails(self):
        comments = 'You are banned'
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.post(
            reverse('moderation:review-abuse'),
            data={
                'report_id': self.abuse_report.id,
                'decision': AbuseReport.BAN,
                'comments': comments,
            },
        )

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
        self.assertIn(comments, email.body)
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
        self.assertIn(comments, email.body)
        self.assertIn(offending_url, email.body)
        self.assertIn(offending_footer, email.body)


class ViewLogsTest(TestCase):
    fixtures = ['group_perms']

    def setUp(self):
        self.standard_user = UserFactory()
        self.moderator = ModeratorFactory()

    def test_logs_url_resolves_to_view_logs(self):
        url = resolve('/moderation/logs/')

        self.assertEqual(url.func, view_logs)

    def test_unauthenticated_users_cannot_view_logs(self):
        response = self.client.get(reverse('moderation:logs'))

        # Unauthenticated user is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/logs/',
            status_code=302
        )

    def test_authenticated_standard_users_cannot_view_logs(self):
        self.client.login(username=self.standard_user.email, password='pass')
        response = self.client.get(reverse('moderation:logs'))

        # User lacking relevant permissions is redirected to login page
        self.assertRedirects(
            response,
            '/accounts/login/?next=/moderation/logs/',
            status_code=302
        )

    def test_authenticated_moderators_can_view_logs(self):
        self.client.login(username=self.moderator.email, password='pass')
        response = self.client.get(reverse('moderation:logs'))

        # User in moderation group can view the page
        self.assertEqual(response.status_code, 200)

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
        response = self.client.get(
            reverse('moderation:logs'),
            data={
                'msg_type': ModerationLogMsg.INVITATION,
                'period': FilterLogsForm.ALL
            },
        )

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
        response = self.client.get(
            reverse('moderation:logs'),
            data={
                'msg_type': 'ALL',
                'period': FilterLogsForm.TODAY
            },
        )

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
        response = self.client.get(
            reverse('moderation:logs'),
            data={
                'msg_type': 'ALL',
                'period': FilterLogsForm.YESTERDAY
            },
        )

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
        response = self.client.get(
            reverse('moderation:logs'),
            data={
                'msg_type': 'ALL',
                'period': FilterLogsForm.THIS_WEEK
            },
        )

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
        response = self.client.get(
            reverse('moderation:logs'),
            data={
                'msg_type': ModerationLogMsg.INVITATION,
                'period': FilterLogsForm.CUSTOM,
                'start_date': '1/2/2014',
                'end_date': '30/3/2014',
            },
        )

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
        response = self.client.get(
            reverse('moderation:logs'),
            data={
                'msg_type': ModerationLogMsg.INVITATION,
                'period': FilterLogsForm.TODAY
            },
        )

        context_logs = response.context['logs']

        self.assertEqual(len(context_logs), 1)
        self.assertIn(today_invitation_log, context_logs)
        self.assertNotIn(today_reinvitation_log, context_logs)
        self.assertNotIn(yesterday_invitation_log, context_logs)

