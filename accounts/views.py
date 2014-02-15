from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django_gravatar.helpers import get_gravatar_url, has_gravatar

from .forms import ProfileForm


@login_required
def profile_settings(request):

    request.user.gravatar_exists = has_gravatar(request.user.email)

    # if you are submitting the form
    if request.method == 'POST':
        form = ProfileForm(request.POST, user=request.user)

        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.profile.bio = form.cleaned_data['bio']
            request.user.profile.connect_preferences = form.cleaned_data['preferences']

            request.user.save()
            request.user.profile.save()

    else:
        form = ProfileForm(user=request.user)


    context = {
        'form' : form
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
