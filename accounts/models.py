from django.contrib.auth.models import User
from django.db import models

from skills.models import UserSkill

class Profile(models.Model):
    """
    Member profile.
    """
    user = models.OneToOneField(User)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='homepage/image_links', blank=True)
    connect_preferences = models.ManyToManyField('ConnectPreference')

    def get_skills(self):
        skills = self.user.skill_set.all()

        for skill in skills:
            userskill = UserSkill.objects.get(user=self.user, skill=skill)
            skill.proficiency = userskill.get_proficiency_display()
            skill.percentage = userskill.get_proficiency_percentage()

        return skills


    class Meta:
        permissions = (
            ("access_moderators_page", "Can see the moderators page"),
        )

    def __str__(self):
        return self.user.get_full_name() or self.user.username



class ConnectPreference(models.Model):
    """
    Member preferences for how they want to connect with others.
    e.g. Mentor, Mentee, Coding Partner, etc.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Preference"

    def __str__(self):
        return self.name


class UserLink(models.Model):
    """
    Link attached to a user's profile, e.g. github account, twitter account, etc·
    """

    user = models.ForeignKey(User)
    anchor = models.CharField(max_length=100, verbose_name='Anchor Text')
    url = models.URLField()

    class Meta:
        verbose_name = 'Link'

    def __str__(self):
        return self.anchor
