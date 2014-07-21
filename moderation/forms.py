from django import forms
from django.contrib.auth import get_user_model
from .models import ModerationLogMsg
from accounts.models import AbuseReport, UserRegistration

User = get_user_model()


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


class ModerateApplicationForm(forms.Form):
    """
    Form for moderators to approve or reject an account application.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ModerateApplicationForm, self).__init__(*args, **kwargs)

        self.fields['user_id'] = forms.IntegerField(initial=self.user.id,
                                                    widget=forms.HiddenInput)

    decision = forms.ChoiceField(choices=UserRegistration.MODERATOR_CHOICES[1:])
    comments = forms.CharField(widget=forms.Textarea)


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

    comments = forms.CharField(widget=forms.Textarea)


class ModerateAbuseForm(forms.Form):
    """
    Form for a moderator to:
    - Dismiss an abuse report
    - Issue a warning
    - Remove abuser
    """
    def __init__(self, *args, **kwargs):
        self.abuse_report = kwargs.pop('abuse_report', None)
        super(ModerateAbuseForm, self).__init__(*args, **kwargs)

        self.fields['report_id'] = forms.IntegerField(initial=self.abuse_report.id,
                                                    widget=forms.HiddenInput)

    decision = forms.ChoiceField(choices=AbuseReport.ABUSE_REPORT_CHOICES)
    comments = forms.CharField(widget=forms.Textarea)


class FilterLogsForm(forms.Form):
    """
    Form for a moderator to filter moderation logs by date, type and
    who the report has been logged against and logged by.
    """

    msg_type = forms.ChoiceField(choices=ModerationLogMsg.MSG_TYPE_CHOICES,
                                 required=False)
#~
    #~preferences = ConnectPreference.objects.all()
    #~selected_preferences = forms.ModelMultipleChoiceField(
                            #~queryset=preferences,
                            #~widget=forms.CheckboxSelectMultiple(),
                            #~required=False)
