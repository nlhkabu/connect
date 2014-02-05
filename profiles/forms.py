from django import forms

from skills.models import Skill


class FilterMemberForm(forms.Form):
    skills = Skill.objects.all()
    selected_skills = forms.ModelMultipleChoiceField(
                        queryset=skills,
                        widget=forms.CheckboxSelectMultiple())



