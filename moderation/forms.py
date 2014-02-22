from django import forms


class InviteMemberForm(forms.Form):
    """
    Form for moderator to invite a new member
    """
    #first_name = forms.CharField()
    email = forms.EmailField()
