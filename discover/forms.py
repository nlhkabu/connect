from django import forms

from accounts.models import Role, Skill


class FilterMemberForm(forms.Form):
    """
    Form for searching for members by their skills and roles.
    """
    skills = Skill.objects.all()
    selected_skills = forms.ModelMultipleChoiceField(
                        queryset=skills,
                        widget=forms.CheckboxSelectMultiple(),
                        required=False)

    roles = Role.objects.all()
    selected_roles = forms.ModelMultipleChoiceField(
                        queryset=roles,
                        widget=forms.CheckboxSelectMultiple(),
                        required=False)



