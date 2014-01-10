from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from profiles.models import Profile, ConnectPreferences
from skills.admin import UserSkillInline

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'Profile'
    verbose_name_plural = 'Profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, UserSkillInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(ConnectPreferences)
