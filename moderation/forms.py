from django import forms
from django.contrib.auth import get_user_model
from .models import ModerationLogMsg
from accounts.models import AbuseReport
from accounts.forms import validate_email_availability

User = get_user_model()


class InviteMemberForm(forms.Form):
    """
    Form for moderator to invite a new member.
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    def clean(self):
        """
        Make sure email is not already in the system.
        """
        cleaned_data = super(InviteMemberForm, self).clean()
        email = cleaned_data.get('email')
        validate_email_availability(email)

        return cleaned_data


class ReInviteMemberForm(forms.Form):
    """
    Form for moderators to reinvite new users.
    Asks moderator to confirm they have sent the email to the correct address.
    """
    email = forms.EmailField()
    user_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean(self):
        """
        If the moderator changes the email, make sure the new email is not already in the system.
        """
        cleaned_data = super(ReInviteMemberForm, self).clean()
        email = cleaned_data.get('email')
        user_id = cleaned_data.get('user_id')
        user = User.objects.get(id=user_id)

        # If this email is not already registered to this user
        if email != user.email:
            validate_email_availability(email)

        return cleaned_data


class RevokeMemberForm(forms.Form):
    """
    Form for moderator to revoke membership invitation.
    Requires moderator to confirm their action.
    """
    confirm = forms.BooleanField()
    user_id = forms.IntegerField(widget=forms.HiddenInput)


class ModerateApplicationForm(forms.Form):
    """
    Form for moderators to approve or reject an account application.
    """
    user_id = forms.IntegerField(widget=forms.HiddenInput)
    decision = forms.ChoiceField(choices=User.MODERATOR_CHOICES[1:],
                                 widget=forms.HiddenInput)
    comments = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder' : 'Please explain your decision. '
                        'This information will not be sent to the user, '
                        'but will be recorded in the moderation logs.',
    }))


class ReportAbuseForm(forms.Form):
    """
    Form for a user to report abusive bahaviour of another user.
    """
    def __init__(self, *args, **kwargs):
        self.logged_by = kwargs.pop('logged_by', None)
        self.logged_against = kwargs.pop('logged_against', None)
        super(ReportAbuseForm, self).__init__(*args, **kwargs)

        self.fields['logged_by'] = forms.IntegerField(
                                                initial=self.logged_by.id,
                                                widget=forms.HiddenInput)

        self.fields['logged_against'] = forms.IntegerField(
                                                initial=self.logged_against.id,
                                                widget=forms.HiddenInput)

    comments = forms.CharField(widget=forms.Textarea())


class ModerateAbuseForm(forms.Form):
    """
    Form for a moderator to:
    - Dismiss an abuse report
    - Issue a warning
    - Remove abuser
    """
    report_id = forms.IntegerField(widget=forms.HiddenInput)
    decision = forms.ChoiceField(choices=AbuseReport.ABUSE_REPORT_CHOICES,
                                 widget=forms.HiddenInput)
    comments = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder' : 'Please explain your decision. '
                        'This information will be sent to both users '
                        'and recorded in the moderation logs.',
    }))


class FilterLogsForm(forms.Form):
    """
    Form for a moderator to filter moderation logs by date, type and
    who the report has been logged against and logged by.
    """
    msg_type = forms.ChoiceField(choices=ModerationLogMsg.MSG_TYPE_CHOICES,
                                 required=False)
