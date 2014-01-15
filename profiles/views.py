from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django_gravatar.helpers import get_gravatar_url, has_gravatar

from .models import Profile
from skills.models import UserSkill

@login_required
def dashboard(request):
    user = request.user
    profile = user.profile
    gravatar_exists = has_gravatar(user.email)

    my_skills = user.skill_set.all()

    for skill in my_skills:
        userskill = UserSkill.objects.get(user=user, skill=skill)
        skill.proficiency = userskill.get_proficiency_display()

    extra_context = {
        'profile': profile,
        'my_skills': my_skills,
        'gravatar_exists': gravatar_exists,
    }

    return render(request, 'profiles/dashboard.html', extra_context)
