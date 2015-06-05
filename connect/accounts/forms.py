from parsley.decorators import parsleyfy

from django import forms
from django.contrib.auth import get_user_model
from django.forms.formsets import BaseFormSet
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from connect.accounts.models import CustomUser, Role, Skill, UserSkill
from connect.accounts.utils import (
    get_user, invite_user_to_reactivate_account, validate_email_availability
)


User = get_user_model()


@parsleyfy
class CustomPasswordResetForm(forms.Form):
    """
    Customised form based on django.contrib.auth.PasswordResetForm.
    Passes additional parameters to attach an email header and link color to
    html template.
    """
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        error_messages={
            'required': _('Please enter your email address.'),
            'invalid': _('Please enter a valid email address.')
        })

    def save(self, domain_override=None,
             subject_template_name='accounts/emails/password_reset_subject.txt',  # NoQA
             email_template_name='accounts/emails/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        email = self.cleaned_data["email"]
        active_users = User._default_manager.filter(
            email__iexact=email, is_active=True)

        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                site = get_current_site(request)
                domain = site.domain
            else:
                site = Site(name=domain_override,
                            domain=domain_override)
                domain = site.domain

            context = {
                'email': user.email,
                'domain': domain,
                'site': site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                # TODO: dynamically retrieve color from CSS
                'link_color': 'e51e41'
            }

            subject = loader.render_to_string(subject_template_name, context)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())

            email = loader.render_to_string(email_template_name, context)

            if html_email_template_name:
                html_email = loader.render_to_string(html_email_template_name,
                                                     context)
            else:
                html_email = None

            send_mail(subject, email, from_email,
                      [user.email], html_message=html_email)


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        if 'username' in self.fields:  # Django 1.7 support
            del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        if 'username' in self.fields:  # Django 1.7 support
            del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)


@parsleyfy
class RequestInvitationForm(forms.Form):
    """
    Form for member of the public to request an invitation.
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RequestInvitationForm, self).__init__(*args, **kwargs)

    full_name = forms.CharField(
        max_length=30,
        error_messages={'required': _('Please enter your full name.')}
    )

    email = forms.EmailField(
        error_messages={
            'required': _('Please enter your email address.'),
            'invalid': _('Please enter a valid email address.')
        })

    comments = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': _('Please explain why you '
                                                      'would like to join '
                                                      'this site')}),
        error_messages={
            'required': _('Please describe why you would like '
                          'to create an account.')
        }
    )

    def clean_email(self):
        """
        Check whether the email is in the system.  If it is registered
        to a closed account, send the user a reactivation link.
        """
        email = self.cleaned_data['email']

        user = get_user(email)
        if user:
            if user.is_closed:
                invite_user_to_reactivate_account(user, request=self.request)
                raise forms.ValidationError(
                    _('This email address is already registered to another '
                      '(closed) account. To reactivate this account, '
                      'please check your email inbox. To register a new '
                      'account, please use a different email address.'),

                    code='email_registered_to_closed_account'
                )

            else:
                raise forms.ValidationError(
                    _('Sorry, this email address is already '
                        'registered to another user.'),

                    code='email_already_registered'
                )

        return email


@parsleyfy
class ActivateAccountForm(forms.Form):
    """
    Form for a user to activate their account
    (after clicking on invitation link)
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ActivateAccountForm, self).__init__(*args, **kwargs)

        self.fields['full_name'] = forms.CharField(
            initial=self.user.full_name,
            error_messages={
                'required': _('Please enter your full name.')
            })

    password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please select a password.')
        })

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please confirm your password.')
        })

    def clean(self):
        """
        Adds validation to:
        - Ensure password and reset confirm password are the same.
        """
        cleaned_data = super(ActivateAccountForm, self).clean()

        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError(_('Your passwords do not match. '
                                          'Please try again.'),
                                        code='unmatched_passwords')

        return cleaned_data


class BaseSkillFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no skill is listed twice
        and that all skills have both a name and proficiency.
        """
        if any(self.errors):
            return

        skills = []

        for form in self.forms:
            if form.cleaned_data:
                skill = form.cleaned_data['skill']
                proficiency = form.cleaned_data['proficiency']

                # Check that no two skills are the same
                if skill and proficiency:
                    if skill in skills:
                        raise forms.ValidationError(
                            _('Each skill can only be entered once.'),
                            code='duplicate_skill'
                        )

                    skills.append(skill)

                # Check that all skills have both a name and proficiency
                if skill and not proficiency:

                    raise forms.ValidationError(
                        _('All skills must have a proficiency.'),
                        code='missing_proficiency'
                    )

                elif proficiency and not skill:
                    raise forms.ValidationError(
                        _('All skills must have a skill name.'),
                        code='missing_skill_name'
                    )


@parsleyfy
class SkillForm(forms.Form):
    """
    Form for individual user skills
    """
    skills = Skill.objects.all()
    skill = forms.ModelChoiceField(queryset=skills, required=False)

    proficiency = forms.ChoiceField(choices=UserSkill.PROFICIENCY_CHOICES,
                                    required=False)


class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        anchors = []
        urls = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                anchor = form.cleaned_data['anchor']
                url = form.cleaned_data['url']

                # Check that no two links have the same anchor or URL
                if anchor and url:
                    if anchor in anchors:
                        duplicates = True
                    anchors.append(anchor)

                    if url in urls:
                        duplicates = True
                    urls.append(url)

                if duplicates:
                    raise forms.ValidationError(
                        _('Links must have unique anchors and URLs.'),
                        code='duplicate_links'
                    )

                # Check that all links have both an anchor and URL
                if url and not anchor:
                    raise forms.ValidationError(
                        _('All links must have an anchor.'),
                        code='missing_anchor'
                    )
                elif anchor and not url:
                    raise forms.ValidationError(
                        _('All links must have a URL.'),
                        code='missing_URL'
                    )


@parsleyfy
class LinkForm(forms.Form):
    """
    Form for individual user links

    """
    anchor = forms.CharField(max_length=100,
                             widget=forms.TextInput(attrs={
                                 'placeholder': _('Link Name / Anchor Text'),
                             }),
                             required=False)

    url = forms.URLField(
        widget=forms.URLInput(attrs={'placeholder': _('URL')}),
        error_messages={'invalid': _('Please enter a valid URL.')},
        required=False)


class RoleModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        label = "<strong>{}</strong> ({})".format(obj.name, obj.description)
        return mark_safe(label)


@parsleyfy
class ProfileForm(forms.Form):
    """
    Form for user to update their own profile details
    (excluding skills and links which are handled by separate formsets)
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['full_name'] = forms.CharField(
            max_length=30,
            initial=self.user.full_name,
            widget=forms.TextInput(attrs={
                'placeholder': _('Name'),
            }),
            error_messages={
                'required': _('Please enter your full name.')
            })

        self.fields['bio'] = forms.CharField(
            initial=self.user.bio,
            widget=forms.Textarea(attrs={
                'class': 'bio',
                'placeholder': _('Add some details about yourself...'),
                'rows': 'auto',
            }),
            required=False)

        roles = Role.objects.all()
        self.fields['roles'] = RoleModelMultipleChoiceField(
            initial=self.user.roles.all(),
            queryset=roles,
            widget=forms.CheckboxSelectMultiple(),
            required=False)


@parsleyfy
class UpdateEmailForm(forms.Form):
    """
    Form for user to update their password.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateEmailForm, self).__init__(*args, **kwargs)

        self.fields['email'] = forms.EmailField(
            initial=self.user.email,
            widget=forms.EmailInput(attrs={
                'placeholder': _('Email')
            }),
            error_messages={
                'required': _('Please enter your new email address.'),
                'invalid': _('Please enter a valid email address.')
            })

        self.fields['password'] = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'placeholder': _('Password')
            }),
            error_messages={
                'required': _('Please enter your password.'),
            })

    def clean_email(self):
        email = self.cleaned_data['email']

        if email != self.user.email:
            validate_email_availability(email)

        return email

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user.check_password(password):
            raise forms.ValidationError(
                _('Incorrect password. Please try again.'),
                code='incorrect_pass'
            )
        else:
            pass


@parsleyfy
class UpdatePasswordForm(forms.Form):
    """
    Form for user to update their password
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password'] = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'placeholder': _('New Password')
            }),
            error_messages={
                'required': _('Please enter your new password.')
            })

        self.fields['current_password'] = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'placeholder': _('Current Password')
            }),
            error_messages={
                'required': _('Please enter your current password.')
            })

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']

        if not self.user.check_password(current_password):
            raise forms.ValidationError(
                _('Incorrect password. Please try again.'),
                code='incorrect_pass'
            )
        else:
            pass


@parsleyfy
class CloseAccountForm(forms.Form):
    """
    Form for user to close their account
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CloseAccountForm, self).__init__(*args, **kwargs)

        self.fields['password'] = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'placeholder': _('Password')
            }),
            error_messages={
                'required': _('Please enter your password.')
            })

    def clean_password(self):
        """
        Adds validation to:
        - Ensure current password matches the user's password.
        """
        password = self.cleaned_data.get('password')

        if not self.user.check_password(password):
            raise forms.ValidationError(
                _('Incorrect password. Please try again.'),
                code='incorrect_pass'
            )
        else:
            pass
