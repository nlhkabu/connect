from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# TODO: Move this view to a more relevant app
@login_required
def dashboard(request):
    extra_context = {}
    return render(request, 'accounts/dashboard.html', extra_context)
