from django import forms
from django.contrib.auth import get_user_model
from django.forms.formsets import BaseFormSet
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Profile, ConnectPreference
from skills.models import Skill, UserSkill


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)


class RequestInvitationForm(forms.Form):
    """
    Form for member of the public to request an invitation.
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder' : 'Please explain why you would like to join this site',
    }))

    def clean(self):
        """
        Make sure email is not already in the system.
        """
        cleaned_data = super(RequestInvitationForm, self).clean()
        email = cleaned_data.get('email')
        user_emails = [user.email for user in User.objects.all() if user.email]

        if email in user_emails:
            raise forms.ValidationError("Sorry, this email address is already registered")

        return cleaned_data


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
            raise forms.ValidationError("Your passwords do not match. Please try again.")

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
                                            'class' : 'account-input inactive',
                                            'placeholder': 'First Name',
                                        }))

        self.fields['last_name'] = forms.CharField(
                                        max_length=30,
                                        initial = self.user.last_name,
                                        widget=forms.TextInput(attrs={
                                            'class' : 'account-input inactive',
                                            'placeholder': 'Last Name',
                                        }))

        self.fields['bio'] = forms.CharField(
                                initial = self.user.profile.bio,
                                widget=forms.Textarea(attrs={
                                    'class': 'bio inactive',
                                    'placeholder': 'Add some details about yourself...',
                                    'rows': 'auto',
                                }),
                                required=False)

        preferences = ConnectPreference.objects.all()
        self.fields['preferences'] = forms.ModelMultipleChoiceField(
                                initial = self.user.profile.connect_preferences.all(),
                                queryset=preferences,
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
                                            'class' : 'account-input inactive',
                                            'placeholder': 'Email Address',
                                        }))

        self.fields['reset_password'] = forms.CharField(
                                        widget=forms.PasswordInput(attrs={
                                            'class' : 'account-input inactive pw',
                                            'placeholder' : 'New Password'
                                        }),
                                        required=False)

        self.fields['reset_password_confirm'] = forms.CharField(
                                        widget=forms.PasswordInput(attrs={
                                            'class' : 'account-input inactive',
                                            'placeholder' : 'Confirm Password'
                                        }),
                                        required=False)


    def clean(self):
        """
        Adds validation to:
        - Ensure reset password and reset password confirm are the same.
        """
        cleaned_data = super(AccountSettingsForm, self).clean()

        password1 = cleaned_data.get('reset_password')
        password2 = cleaned_data.get('reset_password_confirm')

        if password1:
            if not password2:
                raise forms.ValidationError("Please confirm your password")
            if password1 != password2:
                raise forms.ValidationError("Your passwords do not match. Please try again.")

        email = cleaned_data.get('email')
        user_emails = [user.email for user in User.objects.exclude(id=self.user.id) if user.email]

        if email in user_emails:
            raise forms.ValidationError("Sorry, this email address is already registered")

        return cleaned_data
