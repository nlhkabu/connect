from django.conf import settings

User = settings.AUTH_USER_MODEL

def create_inactive_user(email, first_name, last_name):
    """
    Create inactive user with basic details
    """
    user = User.objects.create_user(email)
    user.is_active = False
    user.first_name = first_name
    user.last_name = last_name

    return user
