from django.contrib.auth import get_user_model

def create_inactive_user(email, first_name, last_name):
    """
    Create inactive user with basic details
    """
    User = get_user_model()

    user = User.objects.create_user(email)
    user.is_active = False
    user.first_name = first_name
    user.last_name = last_name
    user.set_unusable_password()

    return user
