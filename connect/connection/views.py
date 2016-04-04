from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


User = get_user_model()


@login_required
def connect_with_user(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    context = {
        'other_user': other_user
    }
    return render(request, 'connection/connect_with_user.html', context)
