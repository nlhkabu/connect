from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, ConnectPreference, UserLink, LinkBrand
from moderation.admin import UserRegistrationInline
from skills.admin import UserSkillInline


# Add Profile, Links and Skills to user page in admin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'Profile'
    verbose_name_plural = 'Profile'

class UserLinkInline(admin.TabularInline):
    model = UserLink

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, UserSkillInline,
               UserLinkInline, UserRegistrationInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Register Preferences and Brands
admin.site.register(ConnectPreference)
admin.site.register(LinkBrand)
