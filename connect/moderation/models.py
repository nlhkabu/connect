from django.conf import settings
from django.db import models
from django.template.defaultfilters import truncatewords
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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
        (INVITATION, _('Invitation')),
        (REINVITATION, _('Invitation Resent')),
        (APPROVAL, _('Application Approved')),
        (REJECTION, _('Application Rejected')),
        (DISMISSAL, _('Abuse Report Dismissed')),
        (WARNING, _('Official Warning')),
        (BANNING, _('Ban User')),
    ]

    msg_datetime = models.DateTimeField(_('date and time recorded'),
                                        default=timezone.now)
    msg_type = models.CharField(_('message type'), max_length=20,
                                choices=MSG_TYPE_CHOICES)
    comment = models.TextField(_('log comment'))
    pertains_to = models.ForeignKey(User, verbose_name=_('pertains to'),
                                    related_name='log_messages_about',
                                    help_text=_('User who moderation '
                                                'log is about'))
    logged_by = models.ForeignKey(User, verbose_name=_('logged by'),
                                  related_name='log_messages_by',
                                  help_text=_('Moderator who created the log'))

    class Meta:
        verbose_name = _('log entry')
        verbose_name_plural = _('log entries')

    def __str__(self):
        return '{}: {}'.format(self.get_msg_type_display(),
                               truncatewords(self.comment, 20))
