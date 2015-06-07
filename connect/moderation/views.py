from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST

from connect.accounts.models import AbuseReport
from connect.utils import send_connect_email
from connect.moderation.forms import (
    FilterLogsForm, InviteMemberForm, ModerateApplicationForm,
    ModerateAbuseForm, ReInviteMemberForm,
    ReportAbuseForm, RevokeInvitationForm
)
from connect.moderation.models import ModerationLogMsg
from connect.moderation.utils import get_date_limits, log_moderator_event


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
        reinvitation_form = ReInviteMemberForm(moderator=request.user)

    if not revocation_form:
        revocation_form = RevokeInvitationForm()

    context = {
        'invitation_form': invitation_form,
        'reinvitation_form': reinvitation_form,
        'revocation_form': revocation_form,
        'pending': pending,
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
        full_name = invitation_form.cleaned_data['full_name']
        email = invitation_form.cleaned_data['email']
        new_user = moderator.invite_new_user(email, full_name)

        # Log moderation event
        msg_type = ModerationLogMsg.INVITATION
        log_comment = _('{} invited {}'.format(moderator.get_full_name(),
                                               new_user.get_full_name()))
        log_moderator_event(msg_type=msg_type,
                            user=new_user,
                            moderator=moderator,
                            comment=log_comment)

        # Send email
        subject = _('Welcome to {}'.format(site.name))
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

        messages.success(request, _('{} has been invited to {}.'.format(
                         new_user.get_full_name(), site.name)))

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

    reinvitation_form = ReInviteMemberForm(request.POST,
                                           moderator=request.user)

    if reinvitation_form.is_valid():

        user_id = reinvitation_form.cleaned_data['user_id']
        user = User.objects.get(id=user_id)
        # We don't need to get_object_or_404 here as we've already checked
        # this in our form's clean method.

        if not user.auth_token_is_used:

            email = reinvitation_form.cleaned_data['email']
            moderator.reinvite_user(user, email)

            # Log moderation event
            msg_type = ModerationLogMsg.REINVITATION
            log_comment = _('{} resent invitation to {}'.format(
                moderator.get_full_name(),
                user.get_full_name()))
            log_moderator_event(msg_type=msg_type,
                                user=user,
                                moderator=moderator,
                                comment=log_comment)

            # Send email
            url = request.build_absolute_uri(
                reverse('accounts:activate-account',
                        args=[user.auth_token]))

            subject = _('Activate your {} account'.format(site.name))
            template = 'moderation/emails/reinvite_user.html'

            send_connect_email(subject=subject,
                               template=template,
                               recipient=user,
                               sender=moderator,
                               site=site,
                               url=url)

        messages.success(request, _('{} has been reinvited to {}.'.format(
                         user.get_full_name().title(), site.name)))

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
    site = get_current_site(request)

    revocation_form = RevokeInvitationForm(request.POST)

    if revocation_form.is_valid():

        user_id = revocation_form.cleaned_data['user_id']
        user = get_object_or_404(User, id=user_id)

        if user.is_invited_pending_activation \
           and user.moderator == request.user:
            messages.success(request, _(
                '{} has been uninvited from {}.'.format(
                    user.get_full_name(), site.name)))

            # Delete the user rather than deactivate it.
            # Removing the email address from the system altogether means
            # that the same email can later be used to create a new account
            # (e.g. if the user applies or is invited by another moderator).
            # Logs related to this user are also removed,
            # resulting in less junk to filter in that view.
            user.delete()
        else:
            raise PermissionDenied

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
        user = get_object_or_404(User, id=request.POST['user_id'])

        if form.is_valid():
            decision = form.cleaned_data['decision']
            comments = form.cleaned_data['comments']

            if decision == 'APP':
                confirmation_message = _("{}'s account application "
                                         "has been approved.".format(
                                             user.get_full_name().title()))

                moderator.approve_user_application(user)

                # Set log and email settings
                msg_type = ModerationLogMsg.APPROVAL
                url = request.build_absolute_uri(
                    reverse('accounts:activate-account',
                            args=[user.auth_token]))
                subject = _('Welcome to {}'.format(site.name))
                template = 'moderation/emails/approve_user.html'

            elif decision == 'REJ':
                confirmation_message = _("{}'s account application "
                                         "has been rejected.".format(
                                             user.get_full_name().title()))

                moderator.reject_user_application(user)

                # Set log and email settings
                msg_type = ModerationLogMsg.REJECTION
                url = ''
                subject = _(('Unfortunately, your application to {} '
                             'was not successful').format(site.name))
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

            messages.success(request, confirmation_message)

            return redirect('moderation:review-applications')

    context = {
        'pending': pending,
        'form': form,
    }

    return render(request, 'moderation/review_applications.html', context)


@login_required
def report_abuse(request, user_id):
    """
    Allow any user to report another user for abusive behaviour.
    """
    logged_against = get_object_or_404(User, id=user_id)
    logged_by = request.user

    if request.POST:
        form = ReportAbuseForm(request.POST)
        if form.is_valid():
            abuse_comment = form.cleaned_data['comments']

            AbuseReport.objects.create(
                logged_by=logged_by,
                logged_against=logged_against,
                abuse_comment=abuse_comment,
            )

            # Send email(s) to moderator(s) alerting them of new report.
            # Do not nofity moderators where the report is logged against them
            # or when they have made the complaint
            moderators = (User.objects.filter(is_moderator=True, is_active=True)
                                      .exclude(id=logged_against.id)
                                      .exclude(id=logged_by.id))

            site = get_current_site(request)

            url = request.build_absolute_uri(
                reverse('moderation:review-abuse'))

            subject = _('New abuse report at {}'.format(site.name))
            template = (
                'moderation/emails/notify_moderators_of_abuse_report.html'
            )

            for moderator in moderators:
                send_connect_email(subject=subject,
                                   template=template,
                                   recipient=moderator,
                                   site=site,
                                   url=url)

            return redirect('moderation:abuse-report-logged')

    else:
        form = ReportAbuseForm()

    context = {
        'form': form,
        'logged_against': logged_against,
        'logged_by': logged_by,
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

        abuse_report = get_object_or_404(AbuseReport,
                                         id=request.POST['report_id'])
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
                confirmation_message = _("The report against {} "
                                         "has been dismissed.".format(
                                             user.get_full_name().title()))

                # Send email to the user who made the report
                subject = _('Your {} Abuse Report has been dismissed'.format(
                    site.name))
                template = 'moderation/emails/abuse_report_dismissed.html'
                send_email_to_reporting_user(subject, template)

            elif decision == 'WARN':
                msg_type = ModerationLogMsg.WARNING
                confirmation_message = _(
                    "{} has been issued a formal warning.".format(
                        user.get_full_name().title()))

                # send email to the user who made the report
                subject = _(
                    '{} has been issued a formal warning from {}'.format(
                        logged_against.get_full_name(), site.name))
                template = (
                    'moderation/emails/abuse_report_warn_other_user.html'
                )
                send_email_to_reporting_user(subject, template)

                # send email to the user the report is logged against
                subject = _('A formal warning from {}'.format(site.name))
                template = 'moderation/emails/abuse_report_warn_this_user.html'
                send_email_to_offending_user(subject, template)

            if decision == 'BAN':
                msg_type = ModerationLogMsg.BANNING
                confirmation_message = _("{} has been banned from {}.".format(
                    user.get_full_name().title(), site.name))

                # send email to the user who made the report
                subject = _('{} has been banned from {}'.format(
                    logged_against.get_full_name(),
                    site.name))
                template = 'moderation/emails/abuse_report_ban_other_user.html'
                send_email_to_reporting_user(subject, template)

                # send email to the user the report is logged against
                subject = _(('Your {} account has been terminated').format(
                    site.name))
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

            messages.success(request, confirmation_message)
            return redirect('moderation:review-abuse')

    context = {
        'reports': undecided_reports,
        'form': form,
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
    # TODO: Get user's preferred timezone

    local_tz = timezone.get_current_timezone()
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
        'form': form,
        'logs': logs,
    }

    return render(request, 'moderation/logs.html', context)
