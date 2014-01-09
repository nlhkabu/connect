from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def moderators(request):
    context = ''
    return render(request, 'accounts/moderators.html', context)
