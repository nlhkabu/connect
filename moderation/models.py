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
    """

    INVITATION = 'INVITATION'
    REINVITATION = 'REINVITATION'
    REVOCATION = 'REVOCATION'
    APPROVAL = 'APPROVAL'
    REJECTION = 'REJECTION'


    MSG_TYPE_CHOICES = (
        (INVITATION, 'Invitation'),
        (REINVITATION, 'Invitation Resent'),
        (REVOCATION, 'Invitation Revoked'),
        (APPROVAL, 'Application Approved'),
        (REJECTION, 'Application Rejected'),
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
