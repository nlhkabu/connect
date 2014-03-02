from django.contrib import admin

from .models import UserRegistration, ModerationLogMsg

class UserRegistrationInline(admin.StackedInline):
    fk_name = 'user'
    model = UserRegistration
    can_delete = False
    verbose_name = 'Registration Details'
    verbose_name_plural = 'Registration Details'

from django.contrib.auth.models import Permission
admin.site.register(Permission)

admin.site.register(ModerationLogMsg)
