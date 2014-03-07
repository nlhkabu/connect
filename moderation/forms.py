from django import forms
from django.contrib.auth.models import User


class InviteMemberForm(forms.Form):
    """
    Form for moderator to invite a new member.
    """
    form_type = forms.CharField(initial='invite', widget=forms.HiddenInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    def clean(self):
        """
        Make sure email is not already in the system.
        """
        cleaned_data = super(InviteMemberForm, self).clean()
        email = cleaned_data.get('email')
        user_emails = [user.email for user in User.objects.all() if user.email]

        if email in user_emails:
            raise forms.ValidationError("Sorry, this email address is already registered")

        return cleaned_data


class ReInviteMemberForm(forms.Form):
    """
    Form for moderators to reinvite new users.
    Asks moderator to confirm they have sent the email to the correct address.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReInviteMemberForm, self).__init__(*args, **kwargs)

        self.fields['email'] = forms.CharField(max_length=30,
                                               initial = self.user.email)

        self.fields['user_id'] = forms.IntegerField(initial=self.user.id,
                                                 widget=forms.HiddenInput)

    form_type = forms.CharField(initial='reinvite', widget=forms.HiddenInput)


class RevokeMemberForm(forms.Form):
    """
    Form for moderator to revoke membership invitation.
    Requires moderator to make a comment.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RevokeMemberForm, self).__init__(*args, **kwargs)

        self.fields['user_id'] = forms.IntegerField(initial=self.user.id,
                                                 widget=forms.HiddenInput)

    form_type = forms.CharField(initial='revoke', widget=forms.HiddenInput)
    comments = forms.CharField(widget=forms.Textarea)


class RequestInvitationForm(forms.Form):
    """
    Form for member of the public to request an invitation.
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder' : 'Please explain why you would like to join this site',
    }))

    def clean(self):
        """
        Make sure email is not already in the system.
        """
        cleaned_data = super(RequestInvitationForm, self).clean()
        email = cleaned_data.get('email')
        user_emails = [user.email for user in User.objects.all() if user.email]

        if email in user_emails:
            raise forms.ValidationError("Sorry, this email address is already registered")

        return cleaned_data


class ApproveApplicationForm(forms.Form):
    """
    Form for moderators to approve an account application.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ApproveApplicationForm, self).__init__(*args, **kwargs)

        self.fields['user_id'] = forms.IntegerField(initial=self.user.id,
                                                 widget=forms.HiddenInput)

    form_type = forms.CharField(initial='approve', widget=forms.HiddenInput)
    comments = forms.CharField(widget=forms.Textarea)

