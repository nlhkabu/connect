from django import forms
from django.contrib.auth.models import User


class InviteMemberForm(forms.Form):
    """
    Form for moderator to invite a new member.
    """
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    email = forms.EmailField()

    def clean(self):
        """
        Make sure email is not already in the system.
        """
        email = self.cleaned_data['email']
        user_emails = [user.email for user in User.objects.all() if user.email]

        if email in user_emails:
            raise forms.ValidationError("Sorry, this email address is already registered")

        return self.cleaned_data


