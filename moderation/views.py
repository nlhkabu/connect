import crypt, time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from .forms import (ApproveApplicationForm, InviteMemberForm, ReInviteMemberForm,
                    RejectApplicationForm, RevokeMemberForm, RequestInvitationForm,)
from .models import UserRegistration, ModerationLogMsg
from .utils import generate_html_email


def hash_time():
    """
    Return a unique 30 character string based on the
    current timestamp. The returned string will consist
    of alphanumeric characters (A-Z, a-z, 0-9) only.
    """
    hashed = ''
    salt = '$1$O2xqbWD9'

    for pos in [-22, -8]:
        hashed += (crypt.crypt(str(time.time()), salt)[pos:].replace('/', '0')
                                                            .replace('.', '0'))
    return hashed


def create_token(user):
    """
    Create an authentication token for a user to activate their account.
    """
    #TODO: Generate token/invitation URL here
    # Needs to be unique (based on datetime?)
    return '123456'


def log_moderator_event(event_type, user, moderator, comment=''):
    """
    Log a moderation event.
    """
    if event_type == 'invited':
        msg_type = ModerationLogMsg.INVITATION
        comment = '{} invited {}'.format(moderator.get_full_name(),
                                         user.get_full_name())

    elif event_type == 'reinvited':
        msg_type = ModerationLogMsg.REINVITATION
        comment = '{} resent invitation to {}'.format(moderator.get_full_name(),
                                                      user.get_full_name())

    elif event_type == 'revoked':
        msg_type = ModerationLogMsg.REVOCATION
        comment = '{}'.format(comment)

    elif event_type == 'approved':
        msg_type = ModerationLogMsg.APPROVAL
        comment = '{}'.format(comment)

    elif event_type == 'rejected':
        msg_type = ModerationLogMsg.REJECTION
        comment = '{}'.format(comment)


    ModerationLogMsg.objects.create(
        msg_type=msg_type,
        comment=comment,
        pertains_to=user,
        logged_by=moderator,
    )


def send_moderation_email(email_type, user, moderator, site, token=''):
    """
    Sends an email to the user from the moderation dashboard.
    e.g. Invitation, reminder to activate their account, etc.
    """

    if email_type == 'invited':
        subject = 'Welcome to {}'.format(site.name)
        template = 'moderation/emails/invite_new_user.html'

    if email_type == 'reinvited':
        subject = 'Activate your {} account'.format(site.name)
        template = 'moderation/emails/reinvite_user.html'

    if email_type == 'approved':
        subject = 'Welcome to {}'.format(site.name)
        template = 'moderation/emails/approve_user.html'

    if email_type == 'rejected':
        subject = 'Your application to {} has been rejected'.format(site.name)
        template = 'moderation/emails/reject_user.html'

    template_vars = {
        'recipient': user,
        'site_name': site.name,
        'activation_url': token,
        'inviter': moderator,
    }

    email = generate_html_email(
        subject,
        settings.EMAIL_HOST_USER,
        [user.email],
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

                handle_invitation_form(first_name,
                                       last_name,
                                       email,
                                       moderator,
                                       site)

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
                    handle_reinvitation_form(user, moderator, site)

                    return redirect('moderation:moderators')

            elif form_type == 'revoke':
                revoke_form = RevokeMemberForm(request.POST, user=user)

                if revoke_form.is_valid():
                    comment = revoke_form.cleaned_data['comments']
                    handle_revocation_form(comment, user, moderator)

                    return redirect('moderation:moderators')

    else:
        invitation_form = InviteMemberForm()

    context = {
        'invitation_form' : invitation_form,
        'pending' : pending,
    }

    return render(request, 'moderation/invite_member.html', context)


def handle_invitation_form(first_name, last_name, email, moderator, site):
    """
    Handles InviteMemberForm.
    """
    username = hash_time()
    user_emails = [user.email for user in User.objects.all() if user.email]

    if email not in user_emails:

        # Create inactive user with unusable password
        new_user = User.objects.create_user(username, email)
        new_user.is_active = False
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        token = create_token(new_user)

        # Add user registration details
        user_registration = UserRegistration.objects.create(
            user=new_user,
            method=UserRegistration.INVITED,
            moderator=moderator,
            moderator_decision=UserRegistration.PRE_APPROVED,
            decision_datetime=now(),
            auth_token = token, # generate auth token
        )

        log_moderator_event(event_type='invited',
                            user=new_user,
                            moderator=moderator)


        send_moderation_email(email_type='invited',
                             user=new_user,
                             moderator=moderator,
                             site=site,
                             token=token)
        return new_user

    return None


def handle_reinvitation_form(user, moderator, site):
    """
    Handles ReinviteMemberForm.
    """
    if not user.userregistration.auth_token_is_used:
        # Set a new token, update approval datetime
        token = create_token(user)
        user.userregistration.auth_token = token;
        user.userregistration.decision_datetime = now()
        user.userregistration.save()

        log_moderator_event(event_type='reinvited',
                            user=user,
                            moderator=moderator)

        send_moderation_email(email_type='reinvited',
                             user=user,
                             moderator=moderator,
                             site=site,
                             token=token)

        # TODO: Add a confirmation message
        return user

    return None


def handle_revocation_form(comment, user, moderator):
    """
    Handles RevokeMemberForm.
    """
    if not user.userregistration.auth_token_is_used:
        # Remove invitation token and other registration information
        user.userregistration.delete()

        log_moderator_event(event_type='revoked',
                            user=user,
                            moderator=moderator,
                            comment=comment)
        return user

    return None


def request_invitation(request):
    """
    Allow a member of the public to request an account invitation.
    """
    if request.method == 'POST':
        form = RequestInvitationForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            comments = form.cleaned_data['comments']
            username = hash_time()

            # Create inactive user with unusable password
            new_user = User.objects.create_user(username, email)
            new_user.is_active = False
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()

            # Add user registration details
            user_registration = UserRegistration.objects.create(
                user=new_user,
                method=UserRegistration.REQUESTED,
                applied_datetime=now(),
                application_comments=comments,
            )

            # TODO: Add a confirmation message
            return redirect('moderation:request-invitation')
    else:
        form = RequestInvitationForm()

    context = {
        'form' : form,
    }

    return render(request, 'moderation/request_invitation.html', context)


@login_required
def review_applications(request):
    """
    Review all pending applications
    """
    moderator = request.user
    site = get_current_site(request)

    pending = User.objects.filter(userregistration__method='REQ',
                                  userregistration__decision_datetime=None,
                                  is_active=False)

    for user in pending:
        user.approval_form = ApproveApplicationForm(user=user)
        user.rejection_form = RejectApplicationForm(user=user)

    if request.method == 'POST':
        form_type = request.POST['form_type']

        try:
            user = pending.get(id=request.POST['user_id'])
        except User.DoesNotExist:
            raise PermissionDenied

        if form_type == 'approve':
            approval_form = ApproveApplicationForm(request.POST, user=user)

            if approval_form.is_valid():
                comments = approval_form.cleaned_data['comments']
                handle_approval_form(user, moderator, comments, site)

                return redirect('moderation:review-applications')


        if form_type == 'reject':
            rejection_form = RejectApplicationForm(request.POST, user=user)

            if rejection_form.is_valid():
                comments = rejection_form.cleaned_data['comments']
                handle_rejection_form(user, moderator, comments, site)

                return redirect('moderation:review-applications')

    context = {
        'pending' : pending,
    }

    return render(request, 'moderation/review_applications.html', context)


def handle_approval_form(user, moderator, comments, site):
    """
    Handles ApproveApplicationForm.
    """

    if not user.userregistration.auth_token_is_used:
        # Set a new token, add approval moderator and datetime
        token = create_token(user)
        user.userregistration.moderator = moderator
        user.userregistration.auth_token = token
        user.userregistration.moderator_decision=UserRegistration.APPROVED
        user.userregistration.decision_datetime = now()
        user.userregistration.save()

        log_moderator_event(event_type='approved',
                            user=user,
                            moderator=moderator,
                            comment=comments)

        send_moderation_email(email_type='approved',
                             user=user,
                             moderator=moderator,
                             site=site,
                             token=token)

        return user

    return None


def handle_rejection_form(user, moderator, comments, site):
    """
    Handles RejectApplicationForm.
    """

    if not user.userregistration.auth_token_is_used:
        # Add rejection moderator and datetime
        user.userregistration.moderator = moderator
        user.userregistration.moderator_decision=UserRegistration.REJECTED
        user.userregistration.decision_datetime = now()
        user.userregistration.save()

        log_moderator_event(event_type='rejected',
                            user=user,
                            moderator=moderator,
                            comment=comments)

        send_moderation_email(email_type='rejected',
                             user=user,
                             moderator=moderator,
                             site=site)

        return user

    return None

@login_required
def review_abuse(request):
    context = ''
    return render(request, 'moderation/review_abuse.html', context)


@login_required
def view_logs(request):

    logs = ModerationLogMsg.objects.all()

    context = {'logs': logs }
    return render(request, 'moderation/logs.html', context)
