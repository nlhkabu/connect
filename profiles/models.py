from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField()


    def __unicode__(self):
        return self.user.username
