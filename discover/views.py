from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render

from django_gravatar.helpers import get_gravatar_url, has_gravatar

from .forms import FilterMemberForm
from accounts.models import UserSkill


User = get_user_model()


@login_required
def dashboard(request):
    """
    Shows all members as a list - with the capacity to filter by
    member skills and roles.

    Session containing 'show_welcome' displays custom message for our
    user's first visit.
    """
    show_welcome = request.session.get('show_welcome')

    if show_welcome is not None:
        del request.session['show_welcome']

    # Get additional profile data
    user = request.user

    # Display members
    listed_users = User.objects.filter(
        is_active=True
    ).order_by(
        'first_name'
    ).prefetch_related(
        'userskill_set',
        'userskill_set__skill',
        'roles',
        'links',
        'links__icon'
    )

    if request.method == 'GET':
        form = FilterMemberForm(request.GET)
        if form.is_valid():
            skills = form.cleaned_data['skills']
            roles = form.cleaned_data['roles']

            if skills:
                listed_users = listed_users.filter(
                    skill__in=skills
                ).distinct()
            if roles:
                listed_users = listed_users.filter(
                    roles__in=roles
                ).distinct()
    else:
        form = FilterMemberForm()

    context = {
        'logged_in_user': user,
        'listed_users': listed_users,
        'form': form,
        'show_welcome': show_welcome,
    }

    return render(request, 'discover/list.html', context)


@login_required
def member_map(request):
    """
    Shows all members on a world map.
    """
    return render(request, 'discover/map.html')


