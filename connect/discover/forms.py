from django import forms

from connect.accounts.models import Role, Skill


class FilterMemberForm(forms.Form):
    """
    Form for searching for members by their skills and roles.
    """
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False)

    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False)
