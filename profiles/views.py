from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from profiles.models import Profile

@login_required
def dashboard(request):
    profile = request.user.profile
    extra_context = {'profile': profile}
    return render(request, 'profiles/dashboard.html', extra_context)
