from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, Permission, PermissionsMixin)
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote

from connect.utils import generate_salt, hash_time
from .utils import create_inactive_user


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

    email = models.EmailField('email address', max_length=254, unique=True)

    first_name = models.CharField('first name', max_length=30, blank=True)

    last_name = models.CharField('last name', max_length=30, blank=True)

    is_staff = models.BooleanField('staff status', default=False,
                        help_text='Designates whether the user can log '
                                  'into this admin site.')

    is_active = models.BooleanField('active', default=True,
                        help_text='Designates whether this user should be '
                                  'treated as active. Unselect this instead '
                                  'of deleting accounts.')

    is_closed = models.BooleanField('closed', default=False,
                        help_text='Designates whether the user has closed '
                                  'their own account.')

    date_joined = models.DateTimeField('date joined', default=timezone.now)

    # Custom connect fields
    bio = models.TextField(blank=True)

    roles = models.ManyToManyField('Role', null=True, blank=True)

    is_moderator = models.BooleanField(default=False)

    # Registration details
    registration_method = models.CharField(max_length=3,
                                           choices=REGISTRATION_CHOICES)

    applied_datetime = models.DateTimeField(blank=True, null=True,
                       help_text='When user applied for an account (if applicable)')

    application_comments = models.TextField(blank=True,
                           help_text='Information user supplied when applying '
                                     'for an account (if applicable)')

    moderator = models.ForeignKey('self',
                blank=True,
                null=True,
                limit_choices_to={'is_moderator': True},
                help_text='Moderator who invited, approved or rejected this user')

    moderator_decision = models.CharField(max_length=3,
                                          choices=MODERATOR_CHOICES,
                                          blank=True)

    decision_datetime = models.DateTimeField(blank=True, null=True,
                        help_text='When moderator made decision to invite, '
                                  'approve or reject this user')

    auth_token = models.CharField(max_length=40,
                                  blank=True,
                                  verbose_name='Authentication token')

    auth_token_is_used = models.BooleanField(default=False,
                                             verbose_name='Token is used')

    activated_datetime = models.DateTimeField(blank=True, null=True,
                         help_text='When user activated their account')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        permissions = (
            ("access_moderators_section", "Can see the moderators section"),
            ("invite_user", "Can issue or reissue an invitation"),
            ("uninvite_user", "Can revoke a user invitation"),
            ("approve_user_application", "Can approve a user's application"),
            ("reject_user_application", "Can reject a user's application"),
            ("dismiss_abuse_report", "Can dismiss an abuse report"),
            ("warn_user", "Can warn a user in response to an abuse report"),
            ("ban_user", "Can ban a user in response to an abuse report"),
        )


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


    def invite_new_user(self, email, first_name, last_name):
        """
        Invite an inactive user (who needs to activate their account).
        Returns none if user already exists.
        """
        User = get_user_model()

        if self.is_moderator and self.has_perm('invite_user'):
            try:
                existing_user = User.objects.get(email=email)
                return None

            except User.DoesNotExist:
                    new_user = create_inactive_user(email, first_name, last_name)
                    new_user.registration_method = new_user.INVITED
                    new_user.moderator = self
                    new_user.moderator_decision = new_user.PRE_APPROVED
                    new_user.decision_datetime = timezone.now()
                    new_user.auth_token = hash_time(generate_salt())
                    new_user.save()

                    return new_user
        else:
            raise PermissionDenied


    def reinvite_user(self, user, email):
        """
        Reinvite an already invited user.
        """
        if self.is_moderator and self.has_perm('invite_user'):
            # Reset email, set a new token and update decision datetime
            user.email = email
            user.auth_token = hash_time(generate_salt())
            user.decision_datetime = timezone.now()
            user.save()

            return user

        else:
            raise PermissionDenied


    def approve_user_application(self, user):
        """
        Approve a user's application
        """
        if self.is_moderator and self.has_perm('approve_user_application'):
            user.moderator = self
            user.moderator_decision=user.APPROVED
            user.decision_datetime = timezone.now()
            user.auth_token = hash_time(generate_salt())
            user.save()

            return user

        else:
            raise PermissionDenied


    def reject_user_application(self, user):
        """
        Reject a user's application
        """
        if self.is_moderator and self.has_perm('reject_user_application'):
            user.moderator = self
            user.moderator_decision=user.REJECTED
            user.decision_datetime = timezone.now()
            user.save()

            return user

        else:
            raise PermissionDenied


class AbuseReport(models.Model):
    """
    Record an abuse report and a moderator's response.
    """
    DISMISS = 'DISMISS'
    WARN = 'WARN'
    BAN = 'BAN'

    ABUSE_REPORT_CHOICES = (
       (DISMISS, 'Dismiss Report'),
       (WARN, 'Warn User'),
       (BAN, 'Ban User'),
    )

    logged_against = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       related_name='abuse_reports_about')

    logged_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='abuse_reports_by')

    logged_datetime = models.DateTimeField(auto_now_add=True)

    abuse_comment = models.TextField()

    moderator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='abuse_reports_moderated_by',
                                  blank=True,
                                  null=True)

    moderator_decision = models.CharField(max_length=20,
                                          choices=ABUSE_REPORT_CHOICES,
                                          blank=True)

    moderator_comment = models.TextField(blank=True)

    decision_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Abuse Report'

    def __str__(self):
        return 'Reported by {} against {}'.format(
                                            self.logged_by.get_full_name(),
                                            self.logged_against.get_full_name())


class Skill(models.Model):
    """
    Represents a skill in the community.
    """
    name = models.CharField(max_length=100, unique=True)
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserSkill')

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    """
    How proficient an individual user is at a particular skill.
    This model joins User and Skill ('through' table).
    """
    BEGINNER = 10
    INTERMEDIATE = 20
    ADVANCED = 30
    EXPERT = 40

    PROFICIENCY_CHOICES = (
        ('', '---------'),
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
        (EXPERT, 'Expert'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    skill = models.ForeignKey(Skill)
    proficiency = models.IntegerField(max_length=2,
                                      choices=PROFICIENCY_CHOICES,
                                      default=BEGINNER)

    def get_proficiency_percentage(self):
        """
        Return a user's profiency in a particular skill as a percentage,
        based on the position of the proficiency in PROFICIENCY_CHOICES.
        """
        choice_values = [choice[0] for choice in self.PROFICIENCY_CHOICES]
        if '' in choice_values:
            choice_values.remove('') # Remove the empty proficiency choice
        choice_values.sort() # Ensure values are in the correct order

        value = choice_values.index(self.proficiency) + 1
        factor = 100 / len(choice_values)
        percentage = round(value * factor)

        return percentage


    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return '{} - {}'.format(self.user, self.skill)


class Role(models.Model):
    """
    Roles that users can take when connecting with others.
    e.g. Mentor, Mentee, Coding Partner, etc.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Role"

    def __str__(self):
        return self.name


class UserLink(models.Model):
    """
    Link attached to a user's profile, e.g. github account,
    twitter account, etc.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='links')
    anchor = models.CharField(max_length=100, verbose_name='Anchor Text')
    url = models.URLField()
    icon = models.ForeignKey('LinkBrand', blank=True, null=True,
                             on_delete=models.SET_NULL)

    def get_icon(self):
        """
        If there is no icon matched - use default.
        """
        try:
            icon = self.icon.fa_icon
        except:
            icon = 'fa-globe'

        return icon

    class Meta:
        verbose_name = 'Link'
        unique_together = (('user', 'anchor'), ('user', 'url'))

    def __str__(self):
        return self.anchor

    def save(self, *args, **kwargs):
        """
        Attempt to match a user link to a recognised brand (LinkBrand).
        """
        domain = urlsplit(self.url).netloc

        try:
            self.icon = LinkBrand.objects.get(domain=domain)
        except:
            pass

        super(UserLink, self).save(*args, **kwargs)


class LinkBrand(models.Model):
    """
    Recognised third-party services.
    """
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100, unique=True,
                              help_text='Do not include scheme '
                              '(e.g. http://, https://)  or subdomain (e.g. www.) '
                              'e.g github.com, facebook.com, etc.')

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

    def save(self, *args, **kwargs):
        """
        Find any existing links to match to a new (or edited) brand
        """
        super(LinkBrand, self).save(*args, **kwargs)

        existing_links = UserLink.objects.filter(url__contains=self.domain)

        # Filter out any false positives
        for link in existing_links:
            domain = urlsplit(link.url).netloc

            if domain != self.domain:
                existing_links = existing_links.exclude(pk=link.pk)

        existing_links.update(icon=self)
