from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, ConnectPreference, UserLink, LinkBrand
from .forms import CustomUserChangeForm, CustomUserCreationForm
from moderation.admin import UserAbuseReportInline, UserRegistrationInline
from skills.admin import UserSkillInline


User = get_user_model()


class UserLinkInline(admin.TabularInline):
    model = UserLink

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    inlines = (UserSkillInline, UserLinkInline,
               UserRegistrationInline, UserAbuseReportInline)

admin.site.register(CustomUser, CustomUserAdmin)

# Register Preferences and Brands
admin.site.register(ConnectPreference)
admin.site.register(LinkBrand)
