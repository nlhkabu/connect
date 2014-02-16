from django import forms

from .models import Profile, ConnectPreference
from skills.models import Skill, UserSkill


class SkillForm(forms.Form):

    skills = Skill.objects.all()
    skill = forms.ModelChoiceField(
                        queryset=skills,
                        required=True)

    proficiency = forms.ChoiceField(
                        choices=UserSkill.PROFICIENCY_CHOICES,
                        required=True)


class LinkForm(forms.Form):

    anchor = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Link Name / Anchor Text',
                    }))

    url = forms.URLField(
                    widget=forms.URLInput(attrs={
                        'placeholder': 'URL',
                    }))


class ProfileForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['first_name'] = forms.CharField(
                                        max_length=30,
                                        initial = self.user.first_name,
                                        widget=forms.TextInput(attrs={
                                            'class' : 'name inactive',
                                            'placeholder': 'First Name',
                                        }))

        self.fields['last_name'] = forms.CharField(
                                        max_length=30,
                                        initial = self.user.last_name,
                                        widget=forms.TextInput(attrs={
                                            'class' : 'name inactive',
                                            'placeholder': 'Last Name',
                                        }))

        self.fields['bio'] = forms.CharField(
                                initial = self.user.profile.bio,
                                widget=forms.Textarea(attrs={
                                    'class': 'bio inactive',
                                    'placeholder': 'Add some details about yourself...',
                                    'rows': 'auto',
                                }))

        preferences = ConnectPreference.objects.all()
        self.fields['preferences'] = forms.ModelMultipleChoiceField(
                                initial = self.user.profile.connect_preferences.all(),
                                queryset=preferences,
                                widget=forms.CheckboxSelectMultiple(),
                                required=False)
