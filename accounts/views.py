from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render

from django_gravatar.helpers import get_gravatar_url, has_gravatar

from .forms import LinkForm, ProfileForm, SkillForm
from .models import UserLink
from skills.models import UserSkill


@login_required
def profile_settings(request):

    user = request.user

    user.gravatar_exists = has_gravatar(user.email)

    SkillFormSet = formset_factory(SkillForm, extra=1, max_num=None)
    user_skills = UserSkill.objects.filter(user=user)
    skill_data = [{'skill': s.skill, 'proficiency': s.proficiency}
                    for s in user_skills]

    LinkFormSet = formset_factory(LinkForm, extra=1, max_num=None)
    user_links = UserLink.objects.filter(user=user)
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
    user = request.user
    return render(request, 'accounts/account_settings.html')


@login_required
def moderators(request):
    context = ''
    return render(request, 'accounts/moderators.html', context)
