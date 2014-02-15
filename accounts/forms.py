from django import forms
from django.forms.formsets import formset_factory

from .models import Profile, ConnectPreference


class ProfileForm(forms.Form):

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

