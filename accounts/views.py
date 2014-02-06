from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django_gravatar.helpers import get_gravatar_url, has_gravatar


@login_required
def profile_settings(request):

    user = request.user
    user.gravatar_exists = has_gravatar(user.email)

    return render(request, 'accounts/profile_settings.html')


@login_required
def account_settings(request):
    user = request.user
    return render(request, 'accounts/account_settings.html')


@login_required
def moderators(request):
    context = ''
    return render(request, 'accounts/moderators.html', context)
