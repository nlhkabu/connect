from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import truncatewords


class UserRegistration(models.Model):
    """
    Log the method and details of the user's registration.
    """
    INVITED = 'INV'
    REQUESTED = 'REQ'

    REGISTRATION_CHOICES = (
        (INVITED, 'Invited'),
        (REQUESTED, 'Requested'),
    )

    PRE_APPROVED = 'PRE'
    APPROVED = 'APP'
    REJECTED = 'REJ'

    MODERATOR_CHOICES = (
        (PRE_APPROVED, 'Pre-approved'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    )

    user = models.OneToOneField(User)
    method = models.CharField(max_length=20, choices=REGISTRATION_CHOICES)
    moderator = models.ForeignKey(User,
                blank=True,
                null=True,
                related_name='inviter',
                limit_choices_to={'profile__is_moderator': True},
                help_text='Moderator who invited, approved or rejected this user')

    applied_datetime = models.DateTimeField(blank=True, null=True)
    application_comments = models.TextField(blank=True)

    moderator_decision = models.CharField(max_length=20,
                                          choices=MODERATOR_CHOICES,
                                          blank=True)
    decision_datetime = models.DateTimeField(blank=True, null=True)

    auth_token = models.CharField(max_length=40,
                                  blank=True,
                                  verbose_name='Authetication token')
    activated_datetime = models.DateTimeField(blank=True, null=True)
    auth_token_is_used = models.BooleanField(default=False,
                                             verbose_name='Token is used')


    class Meta:
        permissions = (
            ("invite_user", "Can invite a new user"),
            ("access_moderators_page", "Can see the moderators page"),
        )

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ModerationLogMsg(models.Model):
    """
    Log a moderation event, e.g. when a new user is invited, approved, etc.
    Or when an abuse report is dealt with
    """
    INVITATION = 'INVITATION'
    REINVITATION = 'REINVITATION'
    REVOCATION = 'REVOCATION'
    APPROVAL = 'APPROVAL'
    REJECTION = 'REJECTION'
    DISMISSAL = 'DISMISSAL'
    WARNING = 'WARNING'
    BANNING = 'BANNING'


    MSG_TYPE_CHOICES = (
        (INVITATION, 'Invitation'),
        (REINVITATION, 'Invitation Resent'),
        (REVOCATION, 'Invitation Revoked'),
        (APPROVAL, 'Application Approved'),
        (REJECTION, 'Application Rejected'),
        (DISMISSAL, 'Abuse Report Dismissed'),
        (WARNING, 'Official Warning'),
        (BANNING, 'Ban User'),

    )

    msg_datetime = models.DateTimeField(auto_now_add=True)
    msg_type = models.CharField(max_length=20, choices=MSG_TYPE_CHOICES)
    comment = models.TextField()
    pertains_to = models.ForeignKey(User, related_name='log_messages_about')
    logged_by = models.ForeignKey(User, related_name='log_messages_by')

    class Meta:
        verbose_name = 'Log Entry'
        verbose_name_plural = 'Log Entries'

    def __str__(self):
        return '{}: {}'.format(self.get_msg_type_display(),
                               truncatewords(self.comment, 20))


class AbuseReport(models.Model):
    """
    Record an abuse report and a moderator's response.
    """
    DISMISS = 'DISMISS'
    WARN = 'WARN'
    BAN = 'BAN'

    ABUSE_REPORT_CHOICES = (
       (DISMISS, 'Dismiss Report'),
       (WARN, 'Warn Abuser'),
       (BAN, 'Ban Abuser'),
    )

    logged_against = models.ForeignKey(User, related_name='abuse_reports_about')
    logged_by = models.ForeignKey(User, related_name='abuse_reports_by')
    logged_datetime = models.DateTimeField(auto_now_add=True)
    abuse_comment = models.TextField()
    moderator = models.ForeignKey(User,
                                  related_name='abuse_reports_moderatored_by',
                                  blank=True,
                                  null=True)
    moderator_decision = models.CharField(max_length=20,
                                          choices=ABUSE_REPORT_CHOICES,
                                          blank=True)
    moderator_comment = models.TextField(blank=True)
    decision_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Abuse Report'

    def __str__(self):
        return 'Reported by {}'.format(self.logged_by.get_full_name())


#~class AbuseWarning(models.Model):
    #~"""
    #~Record a warning against a user.
    #~"""
    #~report = models.ForeignKey(AbuseReport)
#~
    #~class Meta:
        #~verbose_name = 'Abuse Warning'
#~
    #~def __str__(self):
        #~return 'Warned by {} on {}'.format(self.report.moderator,
                                           #~self.report.decision_datetime)
