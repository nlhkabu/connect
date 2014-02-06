from django import forms

from skills.models import Skill
from accounts.models import ConnectPreference


class FilterMemberForm(forms.Form):
    skills = Skill.objects.all()
    selected_skills = forms.ModelMultipleChoiceField(
                        queryset=skills,
                        widget=forms.CheckboxSelectMultiple(),
                        required=False)

    preferences = ConnectPreference.objects.all()
    selected_preferences = forms.ModelMultipleChoiceField(
                            queryset=preferences,
                            widget=forms.CheckboxSelectMultiple(),
                            required=False)



