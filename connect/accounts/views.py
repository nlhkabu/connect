from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from connect.utils import send_connect_email

from connect.accounts.forms import (
    ActivateAccountForm, BaseLinkFormSet, BaseSkillFormSet, CloseAccountForm,
    LinkForm, ProfileForm, RequestInvitationForm, SkillForm, UpdateEmailForm,
    UpdatePasswordForm
)
from connect.accounts.models import Role, Skill, UserLink, UserSkill

from connect.accounts.utils import create_inactive_user
from connect.accounts.view_utils import (
    match_link_to_brand, save_links, save_skills
)


User = get_user_model()


def request_invitation(request):
    """
    Allow a member of the public to request an account invitation.
    """
    site = get_current_site(request)

    if request.method == 'POST':
        form = RequestInvitationForm(request.POST, request=request)

        if form.is_valid():

            # Create inactive user
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            new_user = create_inactive_user(email, full_name)

            # Add additional details
            comments = form.cleaned_data['comments']
            new_user.registration_method = new_user.REQUESTED
            new_user.applied_datetime = now()
            new_user.application_comments = comments
            new_user.save()

            # Send email(s) to moderator(s) alerting them of new
            # account application
            moderators = User.objects.filter(is_moderator=True, is_active=True)

            url = request.build_absolute_uri(reverse(
                'moderation:review-applications'))

            subject = _('New account request at {}'.format(site.name))
            template = (
                'moderation/emails/notify_moderators_of_new_application.html'
            )

            for moderator in moderators:
                send_connect_email(subject=subject,
                                   template=template,
                                   recipient=moderator,
                                   site=site,
                                   url=url)

            return redirect('accounts:request-invitation-done')
    else:
        form = RequestInvitationForm(request=request)

    context = {
        'form': form,
    }

    return render(request, 'accounts/request_invitation.html', context)


def activate_account(request, token):
    """
    Allow a user to activate their account with the token sent to them
    by email.
    """
    user = get_object_or_404(User, auth_token=token)

    if not user.auth_token_is_used:
        if request.POST:
            form = ActivateAccountForm(request.POST, user=user)

            if form.is_valid():

                # Activate the user's account
                user.full_name = form.cleaned_data['full_name']
                user.password = make_password(form.cleaned_data['password'])
                user.is_active = True

                user.activated_datetime = now()
                user.auth_token_is_used = True
                user.save()

                email = user.email
                password = request.POST['password']
                user = authenticate(username=email, password=password)
                login(request, user)

                # Redirect to dashboard with welcome message
                request.session['show_welcome'] = True
                return redirect(reverse('dashboard'))

        else:
            form = ActivateAccountForm(user=user)

        context = {
            'user': user,
            'form': form,
        }

    else:
        token_is_used = True

        context = {
            'token_is_used': token_is_used,
        }

    return render(request, 'accounts/activate_account.html', context)


@login_required
def profile_settings(request):
    """
    Allows a user to update their own profile.
    """
    user = request.user

    has_skills = Skill.objects.count() > 0
    has_roles = Role.objects.count() > 0

    SkillFormSet = formset_factory(SkillForm, formset=BaseSkillFormSet)

    user_skills = UserSkill.objects.filter(user=user).order_by('skill__name')
    skill_data = [{'skill': s.skill, 'proficiency': s.proficiency}
                  for s in user_skills]

    LinkFormSet = formset_factory(LinkForm, formset=BaseLinkFormSet)

    user_links = UserLink.objects.filter(user=user).order_by('anchor')
    link_data = [{'anchor': l.anchor, 'url': l.url}
                 for l in user_links]

    if request.method == 'POST':
        form = ProfileForm(request.POST, user=user)
        skill_formset = SkillFormSet(request.POST, prefix='skill')
        link_formset = LinkFormSet(request.POST, prefix='link')

        forms = [form, link_formset]

        if has_skills:
            forms.append(skill_formset)

        if all([f.is_valid() for f in forms]):
            # Save user info
            user.full_name = form.cleaned_data['full_name']
            user.bio = form.cleaned_data['bio']
            user.roles = form.cleaned_data['roles']
            user.save()

            if has_skills:
                save_skills(request, user, skill_formset)

            save_links(request, user, link_formset)

            user_links = UserLink.objects.filter(user=user)
            match_link_to_brand(user_links)

            site = get_current_site(request)
            messages.success(request, _(
                'Your {} profile has been updated.'.format(site.name)))

    else:
        form = ProfileForm(user=user)
        skill_formset = SkillFormSet(initial=skill_data, prefix='skill')
        link_formset = LinkFormSet(initial=link_data, prefix='link')

    context = {
        'form': form,
        'skill_formset': skill_formset,
        'link_formset': link_formset,
        'has_skills': has_skills,
        'has_roles': has_roles,
    }

    return render(request, 'accounts/profile_settings.html', context)


@login_required
def update_email(request):
    """
    Update a user's email
    """
    user = request.user

    if request.method == 'POST':
        form = UpdateEmailForm(request.POST, user=user)

        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.save()

            site = get_current_site(request)
            messages.success(request, _(
                'Your {} email has been updated.'.format(site.name)))

    else:
        form = UpdateEmailForm(user=user)

    context = {
        'form': form,
    }

    return render(request, 'accounts/update_email.html', context)


@login_required
def update_password(request):
    """
    Update a user's password
    """
    user = request.user

    if request.method == 'POST':
        form = UpdatePasswordForm(request.POST, user=user)

        if form.is_valid():
            new_pass = make_password(form.cleaned_data['new_password'])
            user.password = new_pass
            user.save()

            site = get_current_site(request)
            messages.success(request, _(
                'Your {} password has been updated.'.format(site.name)))

    else:
        form = UpdatePasswordForm(user=user)

    context = {
        'form': form,
    }

    return render(request, 'accounts/update_password.html', context)


@login_required
def close_account(request):
    """
    Close a user's account
    """
    user = request.user

    if request.method == 'POST':
        form = CloseAccountForm(request.POST, user=user)

        if form.is_valid():

            user.is_active = False
            user.is_closed = True
            user.save()
            logout(request)

            return redirect(reverse('accounts:close-account-done'))

    else:
        form = CloseAccountForm(user=user)

    context = {
        'form': form,
    }

    return render(request, 'accounts/close_account.html', context)
