import crypt, time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from .forms import InviteMemberForm, ReInviteMemberForm, RevokeMemberForm
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

    ModerationLogMsg.objects.create(
        msg_type=msg_type,
        comment=comment,
        pertains_to=user,
        logged_by=moderator,
    )


def send_moderator_email(email_type, user, moderator, site, token=''):
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

    subject = subject

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
            handle_invitation_form(invitation_form, moderator, site)

        elif form_type == 'reinvite' or form_type == 'revoke':
            invitation_form = InviteMemberForm()

            try:
                user = pending.get(id=request.POST['user_id'])
            except User.DoesNotExist:
                raise PermissionDenied

            if form_type == 'reinvite':
                reinvitation_form = ReInviteMemberForm(request.POST, user=user)
                handle_reinvitation_form(reinvitation_form, user, moderator, site)

            if form_type == 'revoke':
                revoke_form = RevokeMemberForm(request.POST, user=user)
                form_is_valid = handle_revocation_form(revoke_form, user, moderator)



    else:
        invitation_form = InviteMemberForm()

    context = {
        'invitation_form' : invitation_form,
        'pending' : pending,
    }

    return render(request, 'moderation/invite_member.html', context)


def handle_invitation_form(form, moderator, site):
    """
    Handles InviteMemberForm.
    """
    if form.is_valid():

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        username = hash_time()
        user_emails = [user.email for user in User.objects.all() if user.email]

        if email not in user_emails:

            # Create inactive user with unusable password
            new_user = User.objects.create_user(username, email)
            new_user.is_active = False
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()

            # Add user registration details
            user_registration = UserRegistration.objects.create(
                user=new_user,
                method=UserRegistration.INVITED,
                moderator=moderator,
                approved_datetime=now(),
                auth_token = create_token(new_user), # generate auth token
            )

            log_moderator_event(event_type='invited',
                                user=new_user,
                                moderator=moderator)


            send_moderator_email(email_type='invited',
                                 user=new_user,
                                 moderator=moderator,
                                 site=site,
                                 token='user_registration.auth_token')

            return redirect('moderation:moderators')

    return False


def handle_reinvitation_form(form, user, moderator, site):
    """
    Handles ReinviteMemberForm.
    """
    if form.is_valid():

        if not user.userregistration.auth_token_is_used:
            # Set a new token, update approval datetime
            token = create_token(user)
            user.userregistration.auth_token = token;
            user.userregistration.approved_datetime = now()
            user.save()

            log_moderator_event(event_type='reinvited',
                                user=user,
                                moderator=moderator)

            send_moderator_email(email_type='reinvited',
                                 user=user,
                                 moderator=moderator,
                                 site=site,
                                 token=token)

            return redirect('moderation:moderators')

    return False


def handle_revocation_form(form, user, moderator):
    """
    Handles RevokeMemberForm.
    """
    if form.is_valid():

        moderator_comment = form.cleaned_data['comments']

        if not user.userregistration.auth_token_is_used:
            # Remove invitation token and other information
            user.userregistration.delete()

            log_moderator_event(event_type='revoked',
                                user=user,
                                moderator=moderator,
                                comment=moderator_comment)

            return redirect('moderation:moderators')

    return False















@login_required
def review_applications(request):
    context = ''
    return render(request, 'moderation/review_applications.html', context)


@login_required
def review_abuse(request):
    context = ''
    return render(request, 'moderation/review_abuse.html', context)


@login_required
def view_logs(request):

    logs = ModerationLogMsg.objects.all()

    context = {'logs': logs }
    return render(request, 'moderation/logs.html', context)
