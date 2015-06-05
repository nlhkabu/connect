from django import forms

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from connect.utils import send_connect_email, generate_unique_id


def create_inactive_user(email, full_name):
    """
    Create inactive user with basic details.
    Used when moderators invite new users and when a member of the public
    requests an account.
    """
    User = get_user_model()

    user = User.objects.create_user(email)
    user.is_active = False
    user.full_name = full_name
    user.set_unusable_password()

    return user


def invite_user_to_reactivate_account(user, request):
    """
    Send an email to a user asking them if they'd like to reactivate
    their account.
    """
    # Build and send a reactivation link for closed account
    user.auth_token = generate_unique_id()  # Reset token
    user.auth_token_is_used = False
    user.save()

    site = get_current_site(request)
    url = request.build_absolute_uri(
        reverse('accounts:activate-account',
                args=[user.auth_token]))

    # Send email
    subject = _('Reactivate your {} account'.format(site.name))
    template = 'accounts/emails/reactivate_account.html'

    send_connect_email(subject=subject,
                       template=template,
                       recipient=user,
                       site=site,
                       url=url)

    return user


def get_user(email):
    """
    Retrieve a user based on the supplied email address.
    Return None if no user has registered this email address.
    """
    User = get_user_model()

    try:
        user = User.objects.get(email=email)
        return user

    except User.DoesNotExist:
        return None


def validate_email_availability(email):
    """
    Check that the email address is not registered to an existing user.
    """
    user = get_user(email)
    if user:
        raise forms.ValidationError(
            ugettext_lazy('Sorry, this email address is already '
                          'registered to another user.'),
            code='email_already_registered'
        )
    else:
        return True
