from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from django_gravatar.helpers import get_gravatar_url, has_gravatar

from .models import Profile
from skills.models import UserSkill


@login_required
def dashboard(request):

    # Get additional profile data
    user = request.user

    user.gravatar_exists = has_gravatar(user.email)

    # Display other members

    listed_members = User.objects.exclude(id=request.user.id)

    #~for member in listed_members:
        #~skills = member.get_skills()

    extra_context = {
        'listed_members': listed_members,
    }

    return render(request, 'profiles/dashboard.html', extra_context)


