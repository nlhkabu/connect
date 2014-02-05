from django import forms

from skills.models import Skill
from .models import ConnectPreferences


class FilterMemberForm(forms.Form):
    skills = Skill.objects.all()
    selected_skills = forms.ModelMultipleChoiceField(
                        queryset=skills,
                        widget=forms.CheckboxSelectMultiple(),
                        required=False)

    preferences = ConnectPreferences.objects.all()
    selected_preferences = forms.ModelMultipleChoiceField(
                            queryset=preferences,
                            widget=forms.CheckboxSelectMultiple(),
                            required=False)



