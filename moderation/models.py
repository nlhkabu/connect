from django.contrib.auth.models import User
from django.db import models


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

    user = models.OneToOneField(User)
    method = models.CharField(max_length=20, choices=REGISTRATION_CHOICES)
    moderator = models.ForeignKey(User,
                related_name='inviter',
                limit_choices_to={'profile__is_moderator': True},
                help_text='Moderator who has invited or approved this user')
    approved_datetime = models.DateTimeField()
    auth_token = models.CharField(max_length=40,
                                  verbose_name='Authetication token')
    auth_token_is_used = models.BooleanField(default=False,
                                             verbose_name='Token is used')

    class Meta:
        permissions = (
            ("invite_user", "Can invite a new user"),
            ("access_moderators_page", "Can see the moderators page"),
        )

    def __str__(self):
        return self.user.get_full_name() or self.user.username


#~class ModerationLogMsg(models.Model):
    #~"""
    #~Log of a moderation event, e.g. when a new user is invited, approved, etc.
    #~"""
    #~MSG_TYPE_CHOICES = (
        #~('INVITED', 'Invited'),
        #~('APPROVED', 'Approved'),
        #~('REJECTED', 'Rejected'),
    #~)
#~
    #~msg_datetime = models.DateTimeField()
    #~msg_type = models.CharField(max_length=20, choices=MSG_TYPE_CHOICES)
    #~comment = models.TextField()
    #~pertains_to = models.ForeignKey(User, related_name='log_messages_about')
    #~logged_by = models.ForeignKey(User, related_name='log_messages_by')
