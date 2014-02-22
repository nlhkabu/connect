from django.contrib.auth.models import User
from django.db import models




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
