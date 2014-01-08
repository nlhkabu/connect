from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='homepage/image_links', blank=True)
    is_mentor = models.BooleanField(default=False, help_text='Wants to mentor others')
    is_mentee = models.BooleanField(default=False, help_text='Wants to be mentored')
    is_coding_buddy = models.BooleanField(default=False, help_text='Wants to code with others')
    is_social = models.BooleanField(default=False, help_text='Wants to form social connections')

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username
