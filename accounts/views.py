from django.contrib.auth import authenticate, login
from django.shortcuts import render

#TODO: Move this view to it's relevant app
def dashboard(request):
    context = 'my dashboard'
    return render(request, 'accounts/dashboard.html', context)
