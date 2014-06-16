from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django_gravatar.helpers import get_gravatar_url, has_gravatar
from django.utils.timezone import now

from moderation.models import UserRegistration
from moderation.views import send_moderation_email
from connect.utils import generate_html_email, hash_time
from skills.models import UserSkill

from .forms import (AccountSettingsForm, ActivateAccountForm,
                    BaseLinkFormSet, BaseSkillFormSet, LinkForm,
                    ProfileForm, RequestInvitationForm, SkillForm)
from .models import UserLink


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

            # Create inactive user
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

            # Send email(s) to moderator(s) alerting them of new account application
            moderators = User.objects.filter(profile__is_moderator=True,
                                                    is_active=True)

            site = get_current_site(request)
            subject = 'New account request at {}'.format(site.name)
            template = 'moderation/emails/notify_moderators_of_new_application.html'

            for moderator in moderators:
                send_moderation_email(subject=subject,
                                      template=template,
                                      recipient=moderator,
                                      site=site)

            # TODO: Add a confirmation message
            return redirect('accounts:request-invitation')
    else:
        form = RequestInvitationForm()

    context = {
        'form' : form,
    }

    return render(request, 'accounts/request_invitation.html', context)


def activate_account(request, token):
    """
    Allow a user to activate their account with the token sent to them
    by email.
    """
    user = get_object_or_404(User, userregistration__auth_token=token)

    if not user.userregistration.auth_token_is_used:
        if request.POST:
            # TODO: Check url token = user's token

            form = ActivateAccountForm(request.POST, user=user)

            if form.is_valid():

                # Activate the user's account
                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.password = make_password(form.cleaned_data['password'])
                user.is_active = True
                user.save()

                user.userregistration.activated_datetime = now()
                user.userregistration.auth_token_is_used = True
                user.userregistration.save()

                # TODO: create user.profile

                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                login(request, user)

                # TODO: redirect to welcome page instead of standard dashboard
                return redirect(reverse('dashboard'))

        else:
            form = ActivateAccountForm(user=user)

        context = {
            'user' : user,
            'form' : form,
        }

    else:
        # TODO: Redirect to another view
        is_used = True

        context = {
            'is_used' : is_used,
        }

    return render(request, 'accounts/activate_account.html', context)


@login_required
def profile_settings(request):
    """
    Allows a user to update their own profile.
    """
    user = request.user

    SkillFormSet = formset_factory(SkillForm, extra=1, max_num=None,
                                                       formset=BaseSkillFormSet)

    user_skills = UserSkill.objects.filter(user=user).order_by('skill__name')
    skill_data = [{'skill': s.skill, 'proficiency': s.proficiency}
                    for s in user_skills]

    LinkFormSet = formset_factory(LinkForm, extra=1, max_num=None,
                                                     formset=BaseLinkFormSet)

    user_links = UserLink.objects.filter(user=user).order_by('anchor')
    link_data = [{'anchor': l.anchor, 'url': l.url}
                    for l in user_links]

    if request.method == 'POST':
        form = ProfileForm(request.POST, user=user)
        skill_formset = SkillFormSet(request.POST, prefix='skill')
        link_formset = LinkFormSet(request.POST, prefix='link')

        if form.is_valid() and skill_formset.is_valid() and link_formset.is_valid():
            # Save user info
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.profile.bio = form.cleaned_data['bio']
            user.profile.connect_preferences = form.cleaned_data['preferences']

            user.save()
            user.profile.save()

            #Handle skills formset
            user_skills = []

            for form in skill_formset:
                skill = form.cleaned_data.get('skill', None)
                proficiency = form.cleaned_data.get('proficiency', None)

                if skill and proficiency:
                    user_skills.append(UserSkill(user=user,
                                                 skill=skill,
                                                 proficiency=proficiency))


            # Replace old skills with new
            UserSkill.objects.filter(user=user).delete()
            UserSkill.objects.bulk_create(user_skills)


            # Handle links formset
            user_links = []

            for form in link_formset:
                anchor = form.cleaned_data.get('anchor', None)
                url = form.cleaned_data.get('url', None)

                if (anchor and url):
                    user_links.append(UserLink(user=user,
                                                 anchor=anchor,
                                                 url=url))

            # Replace old skills with new
            UserLink.objects.filter(user=user).delete()
            UserLink.objects.bulk_create(user_links)


            return redirect(reverse('accounts:profile-settings'))

    else:
        form = ProfileForm(user=user)
        skill_formset = SkillFormSet(initial=skill_data, prefix='skill')
        link_formset = LinkFormSet(initial=link_data, prefix='link')


    context = {
        'form' : form,
        'skill_formset' : skill_formset,
        'link_formset' : link_formset,
    }

    return render(request, 'accounts/profile_settings.html', context)


@login_required
def account_settings(request):
    """
    Allows a user to update their own accounts settings.
    """
    user = request.user

    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, user=user)

        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']

            if form.cleaned_data['reset_password']:
                new_pass = make_password(form.cleaned_data['reset_password'])
                user.password = new_pass

            user.save()

            return redirect(reverse('accounts:account-settings'))

    else:
        form = AccountSettingsForm(user=user)


    context = {
        'form' : form,
    }

    return render(request, 'accounts/account_settings.html', context)
