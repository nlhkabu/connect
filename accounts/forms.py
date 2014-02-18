from django import forms
from django.forms.formsets import BaseFormSet

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


class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        """
        Check that no two links have the same anchor or URL
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
                          'Links must have unique anchors and URLs')

                # Check that all links have both an anchor and URL.
                if url and not anchor:
                    raise forms.ValidationError(
                          'All links must specify an anchor')
                elif anchor and not url:
                    raise forms.ValidationError(
                          'All links must specify a URL')



class LinkForm(forms.Form):

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
                                        }),
                                        required=False)

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
