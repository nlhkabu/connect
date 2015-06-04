from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from connect.utils import generate_unique_id
from connect.accounts.utils import create_inactive_user


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
        (INVITED, _('Invited')),
        (REQUESTED, _('Requested')),
    )

    PRE_APPROVED = 'PRE'
    APPROVED = 'APP'
    REJECTED = 'REJ'

    MODERATOR_CHOICES = (
        (PRE_APPROVED, _('Pre-approved')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
    )

    email = models.EmailField(_('email address'), max_length=254, unique=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)

    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log '
                    'into this admin site.'))

    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be '
                    'treated as active. Unselect this instead '
                    'of deleting accounts.'))

    is_closed = models.BooleanField(
        _('closed'), default=False,
        help_text=_('Designates whether the user has closed '
                    'their own account.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # Custom connect fields
    bio = models.TextField(_('biography'), blank=True)

    roles = models.ManyToManyField('Role', verbose_name=_('role'),
                                   null=True, blank=True)

    is_moderator = models.BooleanField(
        _('moderator status'), default=False,
        help_text=_('Designates whether the user has '
                    'moderator privileges.'))

    # Registration details
    registration_method = models.CharField(_('registration method'),
                                           max_length=3,
                                           choices=REGISTRATION_CHOICES)

    applied_datetime = models.DateTimeField(
        _('date applied'),
        blank=True, null=True,
        help_text=_('When user applied for an account (if applicable)'))

    application_comments = models.TextField(
        _('application comments'),
        blank=True,
        help_text='Information user supplied when applying '
        'for an account (if applicable)')

    moderator = models.ForeignKey(
        'self', verbose_name=_('moderator'),
        blank=True, null=True,
        limit_choices_to={'is_moderator': True},
        help_text=_('Moderator who invited, '
                    'approved or rejected this user'))

    moderator_decision = models.CharField(_('moderator decision'),
                                          max_length=3,
                                          choices=MODERATOR_CHOICES,
                                          blank=True)

    decision_datetime = models.DateTimeField(
        _('decision datetime'),
        blank=True,
        null=True,
        help_text=_('When moderator made their decision to invite, approve'
                    ' or reject this user'))

    auth_token = models.CharField(
        _('authentication token'),
        max_length=40,
        blank=True,
        help_text=_('Token for user to activate their account'))

    auth_token_is_used = models.BooleanField(_('token is used'),
                                             default=False)

    activated_datetime = models.DateTimeField(
        _('date account activated'),
        blank=True,
        null=True,
        help_text=_('Date and time when user activated their account'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
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

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user - required for admin.
        """
        return self.first_name

    def is_pending_activation(self):
        """
        Checks whether the user has activated their account.
        """
        if (self.auth_token_is_used and self.is_active):
            return False
        else:
            return True

    def is_invited_pending_activation(self):
        """
        Checks whether the user is an invited user who has not yet activated
        their account.
        """
        if self.registration_method == self.INVITED \
           and self.is_pending_activation():
            return True
        else:
            return False

    def is_pending_approval(self):
        """
        Checks whether the user has requested an account and is
        awaiting a decision.
        """
        if self.registration_method == self.REQUESTED \
           and self.is_pending_activation():
            return True
        else:
            return False

    def invite_new_user(self, email, first_name, last_name):
        """
        Invite an inactive user (who needs to activate their account).
        Returns none if user already exists.
        """
        User = get_user_model()

        if self.is_moderator and self.has_perm('accounts.invite_user'):
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                new_user = create_inactive_user(email, first_name, last_name)
                new_user.registration_method = new_user.INVITED
                new_user.moderator = self
                new_user.moderator_decision = new_user.PRE_APPROVED
                new_user.decision_datetime = timezone.now()
                new_user.auth_token = generate_unique_id()
                new_user.save()
                return new_user
            else:
                return None
        else:
            raise PermissionDenied

    def reinvite_user(self, user, email):
        """
        Reinvite an already invited user.
        """
        if self.is_moderator and self.has_perm('accounts.invite_user'):
            # Reset email, set a new token and update decision datetime
            user.email = email
            user.auth_token = generate_unique_id()
            user.decision_datetime = timezone.now()
            user.save()

            return user

        else:
            raise PermissionDenied

    def approve_user_application(self, user):
        """
        Approve a user's application
        """
        if self.is_moderator and \
           self.has_perm('accounts.approve_user_application'):
            user.moderator = self
            user.moderator_decision = user.APPROVED
            user.decision_datetime = timezone.now()
            user.auth_token = generate_unique_id()
            user.save()

            return user

        else:
            raise PermissionDenied

    def reject_user_application(self, user):
        """
        Reject a user's application
        """
        if self.is_moderator \
           and self.has_perm('accounts.reject_user_application'):
            user.moderator = self
            user.moderator_decision = user.REJECTED
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
        (DISMISS, _('Dismiss Report')),
        (WARN, _('Warn User')),
        (BAN, _('Ban User')),
    )

    logged_against = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('logged against'),
        related_name='abuse_reports_about',
        help_text=_('User who is subject of abuse report'))

    logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('logged by'),
        related_name='abuse_reports_by',
        help_text=_('User who logged the abuse report'))

    logged_datetime = models.DateTimeField(_('date and time logged'),
                                           default=timezone.now)

    abuse_comment = models.TextField(_('abuse comment'),
                                     help_text=_('Content of abuse report'))

    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='abuse_reports_moderated_by',
        verbose_name=_('moderator'),
        blank=True,
        null=True,
        help_text=_('Moderator who has decided on report'))

    moderator_decision = models.CharField(_('moderator decision'),
                                          max_length=20,
                                          choices=ABUSE_REPORT_CHOICES,
                                          blank=True)

    moderator_comment = models.TextField(_('moderator comment'), blank=True)

    decision_datetime = models.DateTimeField(
        _('decision datetime'),
        blank=True, null=True,
        help_text=_('Time and date when moderator made a decision on the '
                    'report'))

    class Meta:
        verbose_name = _('abuse report')
        verbose_name_plural = _('abuse reports')

    def __str__(self):
        return 'Reported by {} against {}'.format(
            self.logged_by.get_full_name(),
            self.logged_against.get_full_name())


class Skill(models.Model):
    """
    Represents a skill in the community.
    """
    name = models.CharField(_('name'), max_length=100, unique=True)
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   through='UserSkill',
                                   verbose_name=_('owner'))

    class Meta:
        verbose_name = _('skill')
        verbose_name_plural = _('skills')

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
        (BEGINNER, _('Beginner')),
        (INTERMEDIATE, _('Intermediate')),
        (ADVANCED, _('Advanced')),
        (EXPERT, _('Expert')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))
    skill = models.ForeignKey(Skill, verbose_name=_('skill'))
    proficiency = models.IntegerField(_('proficiency'),
                                      max_length=2,
                                      choices=PROFICIENCY_CHOICES,
                                      default=BEGINNER)

    def get_proficiency_percentage(self):
        """
        Return a user's profiency in a particular skill as a percentage,
        based on the position of the proficiency in PROFICIENCY_CHOICES.
        """
        choice_values = [choice[0] for choice in self.PROFICIENCY_CHOICES]
        if '' in choice_values:
            choice_values.remove('')  # Remove the empty proficiency choice
        choice_values.sort()  # Ensure values are in the correct order

        value = choice_values.index(self.proficiency) + 1
        factor = 100 / len(choice_values)
        percentage = round(value * factor)

        return percentage

    class Meta:
        verbose_name = _('user skill')
        verbose_name_plural = _('user skills')
        unique_together = ('user', 'skill')

    def __str__(self):
        return '{} - {}'.format(self.user.get_full_name(), self.skill.name)


class Role(models.Model):
    """
    Roles that users can take when connecting with others.
    e.g. Mentor, Mentee, Coding Partner, etc.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __str__(self):
        return self.name


class UserLink(models.Model):
    """
    Link attached to a user's profile, e.g. github account,
    twitter account, etc.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'),
                             related_name='links')
    anchor = models.CharField(_('anchor text'), max_length=100)
    url = models.URLField(_('url'))
    icon = models.ForeignKey('LinkBrand', blank=True, null=True,
                             on_delete=models.SET_NULL,
                             verbose_name=_('icon'))

    def get_icon(self):
        """
        If there is no icon matched - use default.
        """
        try:
            icon = self.icon.fa_icon
        except AttributeError:
            icon = 'fa-globe'

        return icon

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')
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
        except ObjectDoesNotExist:
            pass

        super(UserLink, self).save(*args, **kwargs)


class LinkBrand(models.Model):
    """
    Recognised third-party services.
    """
    name = models.CharField(_('brand name'), max_length=100, unique=True)
    domain = models.CharField(
        _('domain'), max_length=100, unique=True, help_text=_(
            'Do not include scheme '
            '(e.g. http://, https://)  or subdomain (e.g. www.).'
            ' Valid examples include "github.com", "facebook.com", etc.'))

    fa_icon = models.CharField(
        max_length=100,
        verbose_name=_('font awesome icon'),
        help_text=_('Choose an icon name from '
                    '<a href="http://fontawesome.io/icons/">Font Awesome</a> '
                    '(v4.2.0)'))

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')

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
