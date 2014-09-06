from django import forms

from django.contrib.auth import get_user_model
from django.forms.formsets import BaseFormSet
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from .models import CustomUser, Role, Skill, UserSkill
from .utils import get_user, invite_user_to_reactivate_account

User = get_user_model()

def validate_email_availability(email):
    """
    Check that the email address is not registered to an existing user.
    """
    user = get_user(email)
    if user:
        raise forms.ValidationError(
            _('Sorry, this email address is already '
                'registered to another user'),

            code='email_already_registered'
        )


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
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
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)


class RequestInvitationForm(forms.Form):
    """
    Form for member of the public to request an invitation.
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RequestInvitationForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder' : 'Please explain why you would like to join this site',
    }))

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
                        'registered to another user'),

                    code='email_already_registered'
                )

        return email


class ActivateAccountForm(forms.Form):
    """
    Form for a user to activate their account
    (after clicking on invitation link)
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ActivateAccountForm, self).__init__(*args, **kwargs)

        self.fields['first_name'] = forms.CharField(initial=self.user.first_name)
        self.fields['last_name'] = forms.CharField(initial=self.user.last_name)

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        """
        Adds validation to:
        - Ensure password and reset confirm password are the same.
        """
        cleaned_data = super(ActivateAccountForm, self).clean()

        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError('Your passwords do not match. '
                                        'Please try again.')

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
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                skill = form.cleaned_data['skill']
                proficiency = form.cleaned_data['proficiency']

                # Check that no two skills are the same
                if skill and proficiency:
                    if skill in skills:
                        raise forms.ValidationError(
                          'Each skill can only be entered once.')
                    skills.append(skill)

                # Check that all skills have both a name and proficiency
                if skill and not proficiency:
                    raise forms.ValidationError(
                          'All skills must have a proficiency.')
                elif proficiency and not skill:
                    raise forms.ValidationError(
                          'All profiencies must be attached to a skill.')


class SkillForm(forms.Form):
    """
    Form for individual user skills
    """
    skills = Skill.objects.all()
    skill = forms.ModelChoiceField(
                        queryset=skills,
                        required=False)

    proficiency = forms.ChoiceField(
                        choices=UserSkill.PROFICIENCY_CHOICES,
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
                          'Links must have unique anchors and URLs.')

                # Check that all links have both an anchor and URL
                if url and not anchor:
                    raise forms.ValidationError(
                          'All links must have an anchor.')
                elif anchor and not url:
                    raise forms.ValidationError(
                          'All links must have a URL.')


class LinkForm(forms.Form):
    """
    Form for individual user links

    """
    anchor = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Link Name / Anchor Text',
                    }),
                    required=False)

    url = forms.URLField(
                    widget=forms.URLInput(attrs={
                        'placeholder': 'URL',
                    }),
                    required=False)


class RoleModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        label = "<strong>{}</strong> ({})".format(obj.name, obj.description)
        return mark_safe(label)


class ProfileForm(forms.Form):
    """
    Form for user to update their own profile details
    (excluding skills and links which are handled by separate formsets)
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)


        self.fields['first_name'] = forms.CharField(
                                        max_length=30,
                                        initial = self.user.first_name,
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'First Name',
                                        }))

        self.fields['last_name'] = forms.CharField(
                                        max_length=30,
                                        initial = self.user.last_name,
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'Last Name',
                                        }))

        self.fields['bio'] = forms.CharField(
                        initial = self.user.bio,
                        widget=forms.Textarea(attrs={
                            'class': 'bio',
                            'placeholder': 'Add some details about yourself...',
                            'rows': 'auto',
                        }),
                        required=False)

        roles = Role.objects.all()
        self.fields['roles'] = RoleModelMultipleChoiceField(
                                   initial = self.user.roles.all(),
                                   queryset=roles,
                                   widget=forms.CheckboxSelectMultiple(),
                                   required=False)


class AccountSettingsForm(forms.Form):
    """
    Form for user to update their not publically viewable settings
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AccountSettingsForm, self).__init__(*args, **kwargs)

        self.fields['email'] = forms.EmailField(
                                        initial = self.user.email,
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'Email Address',
                                        }))

        self.fields['current_password'] = forms.CharField(
                                        widget=forms.PasswordInput(attrs={
                                            'placeholder' : 'Current Password'
                                        }),
                                        required=False)

        self.fields['reset_password'] = forms.CharField(
                                        widget=forms.PasswordInput(attrs={
                                            'class' : 'pw',
                                            'placeholder' : 'New Password'
                                        }),
                                        required=False)

        self.fields['reset_password_confirm'] = forms.CharField(
                                        widget=forms.PasswordInput(attrs={
                                            'placeholder' : 'Confirm Password'
                                        }),
                                        required=False)

    def clean(self):
        """
        Adds validation to:
        - Check that the email address is not registerd with another user.
        - Ensure current password matches the user's password.
        - Ensure reset password and reset password confirm are the same.
        """
        cleaned_data = super(AccountSettingsForm, self).clean()

        currentpass = cleaned_data.get('current_password')
        password1 = cleaned_data.get('reset_password')
        password2 = cleaned_data.get('reset_password_confirm')

        if currentpass:
            if not self.user.check_password(currentpass):
                raise forms.ValidationError({
                'current_password': ['Incorrect Password.  Please try again.',]})

        if password1:
            if not currentpass:
                raise forms.ValidationError("Please provide your current password")
            if not password2:
                raise forms.ValidationError("Please confirm your password")
            if password1 != password2:
                raise forms.ValidationError("Your passwords do not match. Please try again.")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']

        if email != self.user.email:
            validate_email_availability(email)

        return email


class CloseAccountForm(forms.Form):
    """
    Form for user to close their account
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CloseAccountForm, self).__init__(*args, **kwargs)

        self.fields['password'] = forms.CharField(
                                        widget=forms.PasswordInput(attrs={
                                            'placeholder' : 'Password'
                                        }))

    def clean(self):
        """
        Adds validation to:
        - Ensure current password matches the user's password.
        """
        cleaned_data = super(CloseAccountForm, self).clean()

        password = cleaned_data.get('password')

        if not self.user.check_password(password):
            raise forms.ValidationError({
            'password': ['Incorrect Password.  Please try again.',]})

        return cleaned_data
