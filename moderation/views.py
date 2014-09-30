import datetime
import pytz

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import AbuseReport
from connect.utils import (generate_html_email, generate_salt,
                           hash_time, send_connect_email)
from connect import settings
from .forms import (FilterLogsForm, InviteMemberForm, ModerateApplicationForm,
                    ModerateAbuseForm, ReInviteMemberForm,
                    ReportAbuseForm, RevokeMemberForm)
from .models import ModerationLogMsg
from .utils import get_date_limits, log_moderator_event


User = get_user_model()


@login_required
@permission_required(['accounts.access_moderators_section',
                      'accounts.invite_user',
                      'accounts.uninvite_user'])
def moderation_home(request,
               invitation_form=None,
               reinvitation_form=None,
               revocation_form=None):
    """
    Show forms that allow  a moderator to:
     - Issue a membership invitation
     - Resend a membership invitation
     - Revoke a membership invitation
    """
    # Show pending invitations
    pending = User.objects.filter(moderator=request.user,
                                  registration_method=User.INVITED,
                                  auth_token_is_used=False,
                                  is_active=False)

    if not invitation_form:
        invitation_form = InviteMemberForm()

    if not reinvitation_form:
        reinvitation_form = ReInviteMemberForm()

    if not revocation_form:
        revocation_form = RevokeMemberForm()

    context = {
        'invitation_form' : invitation_form,
        'reinvitation_form' : reinvitation_form,
        'revocation_form' : revocation_form,
        'pending' : pending,
    }

    return render(request, 'moderation/invite_member.html', context)


@require_POST
@login_required
@permission_required(['accounts.access_moderators_section',
                      'accounts.invite_user'])
def invite_user(request):
    """
    Invite a new user
    """
    moderator = request.user
    site = get_current_site(request)

    invitation_form = InviteMemberForm(request.POST)

    if invitation_form.is_valid():

        # Invite user
        first_name = invitation_form.cleaned_data['first_name']
        last_name = invitation_form.cleaned_data['last_name']
        email = invitation_form.cleaned_data['email']
        new_user = moderator.invite_new_user(email, first_name, last_name)

        # Log moderation event
        msg_type = ModerationLogMsg.INVITATION
        log_comment = '{} invited {}'.format(moderator.get_full_name(),
                                             new_user.get_full_name())
        log_moderator_event(msg_type=msg_type,
                            user=new_user,
                            moderator=moderator,
                            comment=log_comment)

        # Send email
        subject = 'Welcome to {}'.format(site.name)
        template = 'moderation/emails/invite_new_user.html'
        token = new_user.auth_token
        url = request.build_absolute_uri(
                    reverse('accounts:activate-account', args=[token]))
        send_connect_email(subject=subject,
                           template=template,
                           recipient=new_user,
                           sender=moderator,
                           site=site,
                           url=url)

        # TODO: Add confirmation message here
        return redirect('moderation:moderators')

    else:
        return moderation_home(request, invitation_form=invitation_form)


@require_POST
@login_required
@permission_required(['accounts.access_moderators_section',
                      'accounts.invite_user'])
def reinvite_user(request):
    """
    Reinvite a user.
    """
    moderator = request.user
    site = get_current_site(request)

    reinvitation_form = ReInviteMemberForm(request.POST)

    if reinvitation_form.is_valid():

        user_id = reinvitation_form.cleaned_data['user_id']

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise PermissionDenied

        if not user.auth_token_is_used:

            email = reinvitation_form.cleaned_data['email']
            moderator.reinvite_user(user, email)

            # Log moderation event
            msg_type = ModerationLogMsg.REINVITATION
            log_comment = '{} resent invitation to {}'.format(moderator.get_full_name(),
                                                              user.get_full_name())
            log_moderator_event(msg_type=msg_type,
                                user=user,
                                moderator=moderator,
                                comment=log_comment)

            # Send email
            url = request.build_absolute_uri(
                        reverse('accounts:activate-account',
                                args=[user.auth_token]))

            subject = 'Activate your {} account'.format(site.name)
            template = 'moderation/emails/reinvite_user.html'

            send_connect_email(subject=subject,
                               template=template,
                               recipient=user,
                               sender=moderator,
                               site=site,
                               url=url)

        # TODO: Add confirmation message here
        return redirect('moderation:moderators')

    else:
        return moderation_home(request, reinvitation_form=reinvitation_form)



@require_POST
@login_required
@permission_required(['accounts.access_moderators_section',
                      'accounts.uninvite_user'])
def revoke_invitation(request):
    """
    Revoke a user invitation.
    """
    moderator = request.user
    site = get_current_site(request)

    revocation_form = RevokeMemberForm(request.POST)

    if revocation_form.is_valid():

        user_id = revocation_form.cleaned_data['user_id']

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise PermissionDenied

        if not user.auth_token_is_used:

            # Delete the user rather than deactivate it.
            # Removing the email address from the system altogether means
            # that the same email can later be used to create a new account
            # (e.g. if the user applies or is invited by another moderator).
            # Logs related to this user are also removed,
            # resulting in less junk to filter in that view.
            user.delete()

        # TODO: Add confirmation message here
        return redirect('moderation:moderators')

    else:
        return moderation_home(request, revocation_form=revocation_form)


@login_required
@permission_required(['accounts.access_moderators_section',
                      'accounts.approve_user_application',
                      'accounts.reject_user_application'])
def review_applications(request):
    """
    Review all pending applications.
    """
    moderator = request.user
    site = get_current_site(request)

    pending = User.objects.filter(registration_method='REQ',
                                  decision_datetime=None,
                                  is_active=False)

    form = ModerateApplicationForm()

    if request.method == 'POST':

        form = ModerateApplicationForm(request.POST)

        try:
            user = User.objects.get(id=request.POST['user_id'])
        except User.DoesNotExist:
            raise PermissionDenied

        if form.is_valid():
            decision = form.cleaned_data['decision']
            comments = form.cleaned_data['comments']

            if decision == 'APP':
                moderator.approve_user_application(user)

                # Set log and email settings
                msg_type = ModerationLogMsg.APPROVAL
                url = request.build_absolute_uri(
                                    reverse('accounts:activate-account',
                                    args=[user.auth_token]))
                subject = 'Welcome to {}'.format(site.name)
                template = 'moderation/emails/approve_user.html'

            elif decision == 'REJ':
                moderator.reject_user_application(user)

                # Set log and email settings
                msg_type = ModerationLogMsg.REJECTION
                url = ''
                subject = ('Unfortunately, your application to {} '
                           'was not successful'.format(site.name))
                template = 'moderation/emails/reject_user.html'


            # Log moderation event
            log_comment = '{}'.format(comments)
            log_moderator_event(msg_type=msg_type,
                                user=user,
                                moderator=moderator,
                                comment=log_comment)

            # Send moderation email
            send_connect_email(subject=subject,
                               template=template,
                               recipient=user,
                               sender=moderator,
                               site=site,
                               url=url)

            return redirect('moderation:review-applications')


    context = {
        'pending' : pending,
        'form' : form,
    }

    return render(request, 'moderation/review_applications.html', context)


@login_required
def report_abuse(request, user_id):
    """
    Allow any user to report another user for abusive behaviour.
    """
    site = get_current_site(request)
    logged_against = get_object_or_404(User, id=user_id)
    logged_by = request.user

    if request.POST:
        form = ReportAbuseForm(request.POST,
                               logged_by=logged_by,
                               logged_against=logged_against)

        if form.is_valid():
            logged_by = User.objects.get(id=form.cleaned_data['logged_by'])
            logged_against = User.objects.get(id=form.cleaned_data['logged_against'])
            abuse_comment = form.cleaned_data['comments']

            new_report = AbuseReport.objects.create(
                logged_by=logged_by,
                logged_against=logged_against,
                abuse_comment=abuse_comment,
            )

            # Send email(s) to moderator(s) alerting them of new report.
            # Do not nofity moderators where the report is logged against them
            moderators = (User.objects.filter(is_moderator=True,
                                              is_active=True)
                                      .exclude(id=logged_against.id))

            site = get_current_site(request)

            url = request.build_absolute_uri(
                                reverse('moderation:review-abuse'))

            subject = 'New abuse report at {}'.format(site.name)
            template = 'moderation/emails/notify_moderators_of_abuse_report.html'

            for moderator in moderators:
                send_connect_email(subject=subject,
                                   template=template,
                                   recipient=moderator,
                                   site=site,
                                   url=url)

            return redirect('moderation:abuse-report-logged')

    else:
        form = ReportAbuseForm(logged_by=logged_by,
                               logged_against=logged_against)

    context = {
        'form' : form,
        'logged_against' : logged_against,
        'logged_by' : logged_by,
        'site' : site,
    }

    return render(request, 'moderation/report_abuse.html', context)


@login_required
@permission_required(['accounts.access_moderators_section',
                      'accounts.dismiss_abuse_report',
                      'accounts.warn_user',
                      'accounts.ban_user'])
def review_abuse(request):
    """
    Show a list of abuse reports to moderators.
    Allow them to:
    - Dismiss an abuse report
    - Warn a user
    - Remove a user
    """
    site = get_current_site(request)

    # Exclude reports where:
    # - the user is not active
    # - the accused is the logged in user
    # - the accusor is the logged in user
    undecided_reports = (AbuseReport.objects.filter(decision_datetime=None)
                            .exclude(logged_against__is_active=False)
                            .exclude(logged_against=request.user)
                            .exclude(logged_by=request.user)
                            .select_related('logged_against', 'logged_by'))

    reported_users = set([report.logged_against
                          for report in undecided_reports])

    warnings = AbuseReport.objects.filter(
        logged_against__in=reported_users,
        moderator_decision='WARN'
    ).select_related('logged_against', 'logged_by', 'moderator')

    form = ModerateAbuseForm()

    for report in undecided_reports:
        accused_user = report.logged_against
        report.prior_warnings = [warning for warning in warnings
                                 if warning.logged_against == accused_user]

    if request.POST:
        try:
            abuse_report = AbuseReport.objects.get(id=request.POST['report_id'])
        except AbuseReport.DoesNotExist:
            raise PermissionDenied

        form = ModerateAbuseForm(request.POST)

        if form.is_valid():
            decision = form.cleaned_data['decision']
            comments = form.cleaned_data['comments']
            moderator = request.user
            user = abuse_report.logged_against

            abuse_report.moderator = moderator
            abuse_report.moderator_decision = decision
            abuse_report.moderator_comment = comments
            abuse_report.decision_datetime = timezone.now()
            abuse_report.save()

            logged_by = abuse_report.logged_by
            logged_against = abuse_report.logged_against


            def send_email_to_reporting_user(subject, template):
                """
                Wrapper function for sending email to the user who has made
                the abuse report.
                """
                send_connect_email(subject=subject,
                                   template=template,
                                   recipient=logged_by,
                                   logged_against=logged_against,
                                   site=site,
                                   comments=comments)


            def send_email_to_offending_user(subject, template):
                """
                Wrapper function for sending email to the user who the abuse
                report has been made against.
                """
                send_connect_email(subject=subject,
                                   template=template,
                                   recipient=logged_against,
                                   logged_against=logged_against,
                                   site=site,
                                   comments=comments)


            if decision == 'DISMISS':
                msg_type = ModerationLogMsg.DISMISSAL

                # Send email to the user who made the report
                subject = 'Your {} Abuse Report has been dismissed'.format(site.name)
                template = 'moderation/emails/abuse_report_dismissed.html'
                send_email_to_reporting_user(subject, template)


            elif decision == 'WARN':
                msg_type = ModerationLogMsg.WARNING

                # send email to the user who made the report
                subject = ('{} {} has been issued a formal '
                          'warning from {} ').format(logged_against.first_name,
                                                    logged_against.last_name,
                                                    site.name)
                template = 'moderation/emails/abuse_report_warn_other_user.html'
                send_email_to_reporting_user(subject, template)

                # send email to the user the report is logged against
                subject = 'A formal warning from {}'.format(site.name)
                template = 'moderation/emails/abuse_report_warn_this_user.html'
                send_email_to_offending_user(subject, template)


            if decision == 'BAN':
                msg_type = ModerationLogMsg.BANNING

                # send email to the user who made the report
                subject = ('{} {} has been '
                           'banned from {}').format(logged_against.first_name,
                                                    logged_against.last_name,
                                                    site.name)
                template = 'moderation/emails/abuse_report_ban_other_user.html'
                send_email_to_reporting_user(subject, template)


                # send email to the user the report is logged against
                subject = 'Your {} account has been terminated'.format(site.name)
                template = 'moderation/emails/abuse_report_ban_this_user.html'
                send_email_to_offending_user(subject, template)

                # deactivate account
                user.is_active = False
                user.save()


            # Log moderation event
            log_moderator_event(msg_type=msg_type,
                                user=user,
                                moderator=moderator,
                                comment=comments)


            return redirect('moderation:review-abuse')

    context = {
        'reports' : undecided_reports,
        'form' : form,
    }

    return render(request, 'moderation/review_abuse.html', context)


@login_required
@permission_required('accounts.access_moderators_section')
def view_logs(request):

    # Exclude logs about the logged in user (moderator)
    logs = ModerationLogMsg.objects.exclude(
        pertains_to=request.user
    ).order_by(
        '-msg_datetime'
    ).select_related(
        'pertains_to',
        'logged_by',
    )

    form = FilterLogsForm()

    # TODO: Get logged in user's timezone
    # TODO: Apply activate() to logged in user's timezone

    local_tz = timezone.get_current_timezone() # TODO: Get user's preferred timezone
    today = timezone.now().astimezone(local_tz)

    if request.method == 'GET':
        form = FilterLogsForm(request.GET)

        if form.is_valid():

            msg_type = form.cleaned_data['msg_type']
            period = form.cleaned_data['period']

            if period == 'TODAY':
                start, end = get_date_limits(start_date=today)

            elif period == 'YESTERDAY':
                yesterday = today - timezone.timedelta(days=1)
                start, end = get_date_limits(start_date=yesterday)

            elif period == 'THIS_WEEK':
                start_date = today - timezone.timedelta(days=7)
                end_date = today

                start, end = get_date_limits(start_date, end_date)

            elif period == 'CUSTOM':
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']

                start, end = get_date_limits(start_date, end_date)

            # Filter Logs
            if msg_type != 'ALL':
                logs = logs.filter(msg_type=msg_type)

            if period != 'ALL':
                logs = logs.filter(msg_datetime__gte=start,
                                   msg_datetime__lte=end)

    context = {
        'form' : form,
        'logs': logs,
    }

    return render(request, 'moderation/logs.html', context)
