from urllib.parse import urlsplit

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from skills.models import UserSkill


User = settings.AUTH_USER_MODEL


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField('email address', max_length=254, unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin '
                    'site.')
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    # Custom connect fields
    bio = models.TextField(blank=True)
    connect_preferences = models.ManyToManyField('ConnectPreference',
                                                  null=True,
                                                  blank=True)
    is_moderator = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_skills(self):
        skills = self.skill_set.all()

        for skill in skills:
            userskill = UserSkill.objects.get(user=self.user, skill=skill)
            skill.proficiency = userskill.get_proficiency_display()
            skill.percentage = userskill.get_proficiency_percentage()

        return skills


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
        unique_together = (('user', 'anchor'), ('user', 'url'))

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

