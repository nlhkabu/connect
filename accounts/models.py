from urllib.parse import urlsplit

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
    Link attached to a user's profile, e.g. github account,
    twitter account, etc.
    """

    user = models.ForeignKey(User)
    anchor = models.CharField(max_length=100, verbose_name='Anchor Text')
    url = models.URLField()

    def get_icon(self):
        """
        Attempt to match a user link to a recognised brand (LinkBrand).
        """
        domain = urlsplit(self.url).netloc
        icon = 'fa-globe'

        try:
            brand = LinkBrand.objects.get(domain=domain)
            icon = brand.fa_icon

        except LinkBrand.DoesNotExist:
            pass # Keep the default icon

        return icon


    class Meta:
        verbose_name = 'Link'

    def __str__(self):
        return self.anchor


class LinkBrand(models.Model):
    """
    Recognised third-party services.
    """
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100, unique=True)
    fa_icon = models.CharField(
        max_length=100,
        verbose_name='Font Awesome Icon',
        help_text='Choose an icon name from '
                  '<a href="http://fontawesome.io/icons/">Font Awesome</a> '
                  '(v4.0.3)')

    class Meta:
        verbose_name = 'Brand'

    def __str__(self):
        return self.name

