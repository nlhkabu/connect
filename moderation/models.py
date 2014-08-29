from django.conf import settings
from django.db import models
from django.template.defaultfilters import truncatewords


User = settings.AUTH_USER_MODEL


class ModerationLogMsg(models.Model):
    """
    Log a moderation event, e.g. when a new user is invited, approved, etc.
    Or when an abuse report is dealt with
    """
    INVITATION = 'INVITATION'
    REINVITATION = 'REINVITATION'
    APPROVAL = 'APPROVAL'
    REJECTION = 'REJECTION'
    DISMISSAL = 'DISMISSAL'
    WARNING = 'WARNING'
    BANNING = 'BANNING'


    MSG_TYPE_CHOICES = [
        (INVITATION, 'Invitation'),
        (REINVITATION, 'Invitation Resent'),
        (APPROVAL, 'Application Approved'),
        (REJECTION, 'Application Rejected'),
        (DISMISSAL, 'Abuse Report Dismissed'),
        (WARNING, 'Official Warning'),
        (BANNING, 'Ban User'),
    ]

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
