from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import InviteMemberForm

@login_required
def invite_member(request):
    """
    Allows a moderator to invite a new member to the system.
    """
    moderator = request.user

    if request.method == 'POST':
        form = InviteMemberForm(request.POST)

        if form.is_valid():
            new_member_first_name = form.cleaned_data['first_name']
            new_member_email = form.cleaned_data['email']

            return redirect(reverse('moderators:moderators'))

    else:
        form = InviteMemberForm()

    context = {
        'form' : form,
    }

    return render(request, 'moderation/invite_member.html', context)


@login_required
def review_applications(request):
    context = ''
    return render(request, 'moderation/review_applications.html', context)


@login_required
def review_abuse(request):
    context = ''
    return render(request, 'moderation/review_abuse.html', context)


@login_required
def logs(request):
    context = ''
    return render(request, 'moderation/logs.html', context)
