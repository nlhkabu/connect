import crypt, time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.timezone import now

from .forms import InviteMemberForm
from .models import UserRegistration
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


@login_required
def invite_member(request):
    """
    Allows a moderator to invite a new member to the system.
    """
    moderator = request.user
    site = get_current_site(request)

    if request.method == 'POST':
        form = InviteMemberForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            username = hash_time()
            user_emails = [user.email for user in User.objects.all() if user.email]

            if email not in user_emails:

                # Create user with unusable password
                user = User.objects.create_user(username, email)

                user.is_active = False
                user.save()

                # Log invitation details against user

                user_registration = UserRegistration.objects.create(
                    user=user,
                    method=UserRegistration.INVITED,
                    moderator=moderator,
                    approved_datetime=now()
                )

                # Send invitation email to new user

                # Render HTML email:
                subject = 'Welcome to '+ site.name
                recipient = user

                template_vars = {
                    'recipient': recipient,
                    'site_name': site.name,
                    'activation_url': 'url here', #TODO: create key
                    'inviter': request.user,
                }

                email = generate_html_email(
                    subject,
                    settings.EMAIL_HOST_USER,
                    [recipient.email],
                    'moderation/emails/invite_new_user.html',
                    template_vars,
                )

                email.send()

            return redirect(reverse('moderators:moderators'))

    else:
        form = InviteMemberForm()

    # Show pending invitations
    # i.e if users are not active AND have not set their passwords
    pending = User.objects.filter(userregistration__moderator=moderator,
                                  is_active=False)

    pending = [user for user in pending if not user.has_usable_password()]

    context = {
        'form' : form,
        'pending' : pending,
    }

    return render(request, 'moderation/invite_member.html', context)


@login_required
def review_applications(request):
    context = ''
    return render(request, 'moderation/review_applications.html', context)


@login_required
def review_abuse(request):
    context = ''
    return render(request, 'moderation/review_abuse.html', context)


@login_required
def logs(request):
    context = ''
    return render(request, 'moderation/logs.html', context)
