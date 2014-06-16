from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from .forms import (FilterLogsForm, InviteMemberForm, ModerateApplicationForm,
                    ModerateAbuseForm, ReInviteMemberForm,
                    ReportAbuseForm, RevokeMemberForm)
from .models import AbuseReport, UserRegistration, ModerationLogMsg
from connect.utils import generate_html_email, hash_time, generate_salt


def log_moderator_event(msg_type, user, moderator, comment=''):
    """
    Log a moderation event.
    """
    ModerationLogMsg.objects.create(
        msg_type=msg_type,
        comment=comment,
        pertains_to=user,
        logged_by=moderator,
    )


def send_moderation_email(subject, template, recipient, site, moderator='',
                          token='', comments='', logged_against=''):
    """
    Sends an email to the user from the moderation dashboard.
    e.g. Invitation, reminder to activate their account, etc.
    """
    template_vars = {
        'recipient': recipient,
        'site_name': site.name,
        'activation_url': token,
        'inviter': moderator,
        'comments': comments,
        'logged_against': logged_against,
    }

    email = generate_html_email(
        subject,
        settings.EMAIL_HOST_USER,
        [recipient.email],
        template,
        template_vars,
    )

    email.send()


@login_required
def invite_member(request):
    """
    Allow a moderator to:
     - Issue a membership invitation
     - Resend a membership invitation
     - Revoke a membership invitation
    """
    moderator = request.user
    site = get_current_site(request)

    # Show pending invitations
    pending = User.objects.filter(userregistration__moderator=moderator,
                                  userregistration__method='INV',
                                  userregistration__auth_token_is_used=False,
                                  is_active=False)

    # Attach forms to each pending user
    for user in pending:
        user.reinvitation_form = ReInviteMemberForm(user=user)
        user.revocation_form = RevokeMemberForm(user=user)

    if request.method == 'POST':
        form_type = request.POST['form_type']

        if form_type == 'invite':
            invitation_form = InviteMemberForm(request.POST)

            if invitation_form.is_valid():
                first_name = invitation_form.cleaned_data['first_name']
                last_name = invitation_form.cleaned_data['last_name']
                email = invitation_form.cleaned_data['email']

                handle_invitation(request, first_name, last_name,
                                  email, moderator, site)

                return redirect('moderation:moderators')

        elif form_type == 'reinvite' or form_type == 'revoke':
            invitation_form = InviteMemberForm()

            try:
                user = pending.get(id=request.POST['user_id'])
            except User.DoesNotExist:
                raise PermissionDenied

            if form_type == 'reinvite':
                reinvitation_form = ReInviteMemberForm(request.POST, user=user)

                if reinvitation_form.is_valid():
                    email = reinvitation_form.cleaned_data['email']

                    handle_reinvitation(request, user, email, moderator, site)

                    return redirect('moderation:moderators')

            elif form_type == 'revoke':
                revoke_form = RevokeMemberForm(request.POST, user=user)

                if revoke_form.is_valid():
                    comment = revoke_form.cleaned_data['comments']
                    handle_revocation(comment, user, moderator)

                    return redirect('moderation:moderators')

    else:
        invitation_form = InviteMemberForm()

    context = {
        'invitation_form' : invitation_form,
        'pending' : pending,
    }

    return render(request, 'moderation/invite_member.html', context)


def handle_invitation(request, first_name, last_name, email, moderator, site):
    """
    Invite a new member
    """
    username = hash_time()
    user_emails = [user.email for user in User.objects.all() if user.email]

    if email not in user_emails:

        # Create inactive user
        new_user = User.objects.create_user(username, email)
        new_user.is_active = False
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        token = hash_time(generate_salt())
        token_url = request.build_absolute_uri(
                        reverse('accounts:activate-account', args=[token]))

        # Add user registration details
        user_registration = UserRegistration.objects.create(
            user=new_user,
            method=UserRegistration.INVITED,
            moderator=moderator,
            moderator_decision=UserRegistration.PRE_APPROVED,
            decision_datetime=now(),
            auth_token = token,
        )

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

        send_moderation_email(subject=subject,
                              template=template,
                              recipient=new_user,
                              moderator=moderator,
                              site=site,
                              token=token_url)
        return new_user

    return None


def handle_reinvitation(request, user, email, moderator, site):
    """
    Reinvite a member.
    """
    if not user.userregistration.auth_token_is_used:
        # Reset email
        user.email = email
        user.save()

        # Set a new token and update decision datetime
        token = hash_time(generate_salt())
        token_url = request.build_absolute_uri(
                        reverse('accounts:activate-account', args=[token]))

        user.userregistration.auth_token = token;
        user.userregistration.decision_datetime = now()
        user.userregistration.save()

        # Log moderation event
        msg_type = ModerationLogMsg.REINVITATION
        log_comment = '{} resent invitation to {}'.format(moderator.get_full_name(),
                                                          user.get_full_name())
        log_moderator_event(msg_type=msg_type,
                            user=user,
                            moderator=moderator,
                            comment=log_comment)

        # Send email
        subject = 'Activate your {} account'.format(site.name)
        template = 'moderation/emails/reinvite_user.html'

        send_moderation_email(subject=subject,
                              template=template,
                              recipient=user,
                              moderator=moderator,
                              site=site,
                              token=token_url)

        # TODO: Add a confirmation message
        return user

    return None


def handle_revocation(comment, user, moderator):
    """
    Revoke a membership invitation.
    """
    if not user.userregistration.auth_token_is_used:
        # Remove invitation token and other registration information
        user.userregistration.delete()

        # Log moderation event
        msg_type = ModerationLogMsg.REVOCATION
        log_comment = '{}'.format(comment)

        log_moderator_event(msg_type=msg_type,
                            user=user,
                            moderator=moderator,
                            comment=log_comment)

        return user

    return None


@login_required
def review_applications(request):
    """
    Review all pending applications.
    """
    moderator = request.user
    site = get_current_site(request)

    pending = User.objects.filter(userregistration__method='REQ',
                                  userregistration__decision_datetime=None,
                                  is_active=False)

    for user in pending:
        user.moderation_form = ModerateApplicationForm(user=user)

    if request.method == 'POST':
        moderation_form = ModerateApplicationForm(request.POST, user=user)

        try:
            user = pending.get(id=request.POST['user_id'])
        except User.DoesNotExist:
            raise PermissionDenied

        if moderation_form.is_valid():
            decision = moderation_form.cleaned_data['decision']
            comments = moderation_form.cleaned_data['comments']

            if decision == 'APP':
                # Create token and token URL
                token = hash_time(generate_salt())
                token_url = request.build_absolute_uri(
                        reverse('accounts:activate-account', args=[token]))
                user.userregistration.auth_token = token

                user.userregistration.moderator_decision=UserRegistration.APPROVED
                msg_type = ModerationLogMsg.APPROVAL

                # Set email settings
                subject = 'Welcome to {}'.format(site.name)
                template = 'moderation/emails/approve_user.html'

            elif decision == 'REJ':
                token_url = ''
                user.userregistration.moderator_decision=UserRegistration.REJECTED
                msg_type = ModerationLogMsg.REJECTION

                # Set email settings
                subject = 'Your application to {} has been rejected'.format(site.name)
                template = 'moderation/emails/reject_user.html'

            # Log decision against user
            user.userregistration.moderator = moderator
            user.userregistration.decision_datetime = now()
            user.userregistration.save()


            # Log moderation event
            log_comment = '{}'.format(comments)
            log_moderator_event(msg_type=msg_type,
                                user=user,
                                moderator=moderator,
                                comment=log_comment)

            # Send moderation email
            send_moderation_email(subject=subject,
                                  template=template,
                                  recipient=user,
                                  site=site,
                                  moderator=moderator,
                                  token=token_url)

            return redirect('moderation:review-applications')


    context = {
        'pending' : pending,
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
            # Do not nofity the moderator the report is logged against
            moderators = (User.objects.filter(profile__is_moderator=True,
                                              is_active=True)
                                      .exclude(id=logged_against.id))

            site = get_current_site(request)
            subject = 'New abuse report at {}'.format(site.name)
            template = 'moderation/emails/notify_moderators_of_abuse_report.html'

            for moderator in moderators:
                send_moderation_email(subject=subject,
                                      template=template,
                                      recipient=moderator,
                                      site=site)

            return redirect('moderation:abuse-report-lodged')

    else:
        form = ReportAbuseForm(logged_by=logged_by,
                               logged_against=logged_against)

    context = {
        'form' : form,
        'logged_by' : logged_by,
        'logged_against' : logged_against
    }

    return render(request, 'moderation/report_abuse.html', context)


@login_required
def abuse_report_lodged(request):
    """
    Show confirmation message for a when an abuse report has been lodged.
    """
    return render(request, 'moderation/abuse_report_lodged.html')


@login_required
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
                                        .select_related())

    reported_users = set([report.logged_against
                          for report in undecided_reports])

    warnings = AbuseReport.objects.filter(logged_against__in=reported_users,
                                          moderator_decision='WARN')

    for report in undecided_reports:
        report.moderation_form = ModerateAbuseForm(abuse_report=report)
        accused_user = report.logged_against
        report.prior_warnings = [warning for warning in warnings
                                 if warning.logged_against == accused_user]

    if request.POST:
        try:
            abuse_report = AbuseReport.objects.get(id=request.POST['report_id'])
        except AbuseReport.DoesNotExist:
            raise PermissionDenied

        form = ModerateAbuseForm(request.POST, abuse_report=report)

        if form.is_valid():
            decision = form.cleaned_data['decision']
            comments = form.cleaned_data['comments']
            moderator = request.user
            user = abuse_report.logged_against

            abuse_report.moderator = moderator
            abuse_report.moderator_decision = decision
            abuse_report.moderator_comment = comments
            abuse_report.decision_datetime = now()
            abuse_report.save()


            if decision == 'DISMISS':
                msg_type = ModerationLogMsg.DISMISSAL

                # Send email to the user who made the report
                subject = 'Your {} Abuse Report has been dismissed'.format(site.name)
                template = 'moderation/emails/abuse_report_dismissed.html'
                logged_by = abuse_report.logged_by
                logged_against = abuse_report.logged_against

                send_moderation_email(subject=subject,
                                      template=template,
                                      recipient=logged_by,
                                      logged_against=logged_against,
                                      site=site,
                                      comments=comments)

            elif decision == 'WARN':
                msg_type = ModerationLogMsg.WARNING
                logged_by = abuse_report.logged_by
                logged_against = abuse_report.logged_against

                # send email to the user the report was logged by
                subject = ('{} {} has been issued a formal '
                          'warning from {} ').format(logged_against.first_name,
                                                    logged_against.last_name,
                                                    site.name)
                template = 'moderation/emails/abuse_report_warn_other_user.html'

                send_moderation_email(subject=subject,
                                      template=template,
                                      recipient=logged_by,
                                      logged_against=logged_against,
                                      site=site,
                                      comments=comments)

                # send email to the user the report is logged against
                subject = 'A formal warning from {}'.format(site.name)
                template = 'moderation/emails/abuse_report_warn_this_user.html'

                send_moderation_email(subject=subject,
                                      template=template,
                                      recipient=logged_against,
                                      logged_against=logged_against,
                                      site=site,
                                      comments=comments)


            if decision == 'BAN':
                msg_type = ModerationLogMsg.BANNING
                logged_by = abuse_report.logged_by
                logged_against = abuse_report.logged_against

                # send email to the user the report was logged by
                subject = ('{} {} has been '
                           'banned from {}').format(logged_against.first_name,
                                                    logged_against.last_name,
                                                    site.name)
                template = 'moderation/emails/abuse_report_ban_other_user.html'

                send_moderation_email(subject=subject,
                                      template=template,
                                      recipient=logged_by,
                                      logged_against=logged_against,
                                      site=site,
                                      comments=comments)

                # send email to the user the report is logged against
                subject = 'Your {} account has been terminated'.format(site.name)
                template = 'moderation/emails/abuse_report_ban_this_user.html'

                send_moderation_email(subject=subject,
                                      template=template,
                                      recipient=logged_against,
                                      logged_against=logged_against,
                                      site=site,
                                      comments=comments)
                # deactivate account
                user.is_active = False
                user.save()


            # Log moderation event
            log_comment = '{}'.format(comments)
            log_moderator_event(msg_type=msg_type,
                                user=user,
                                moderator=moderator,
                                comment=log_comment)

            return redirect('moderation:review-abuse')

    context = {
        'reports' : undecided_reports,
    }

    return render(request, 'moderation/review_abuse.html', context)


@login_required
def view_logs(request):

    # Exclude logs about the logged in user (moderator)
    logs = ModerationLogMsg.objects.exclude(pertains_to=request.user)

    if request.method == 'POST':
        form = FilterLogsForm(request.POST)

        if form.is_valid():

            msg_type = form.cleaned_data['msg_type']

            logs = (ModerationLogMsg.objects.filter(msg_type=msg_type)
                                            .exclude(pertains_to=request.user))


    else:
        form = FilterLogsForm()

    context = {
        'form' : form,
        'logs': logs
    }

    return render(request, 'moderation/logs.html', context)
