from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Profile, ConnectPreference, UserLink, LinkBrand
from moderation.admin import UserAbuseReportInline, UserRegistrationInline
from skills.admin import UserSkillInline


User = get_user_model()


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
               UserLinkInline, UserRegistrationInline, UserAbuseReportInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Register Preferences and Brands
admin.site.register(ConnectPreference)
admin.site.register(LinkBrand)
