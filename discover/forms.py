from django import forms

from accounts.models import ConnectPreference, Skill


class FilterMemberForm(forms.Form):
    """
    Form for searching for members by their skills and connect preferences.
    """
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



