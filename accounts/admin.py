from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import (AbuseReport, CustomUser, ConnectPreference, LinkBrand,
                     Skill, UserLink, UserRegistration, UserSkill)
from .forms import CustomUserChangeForm, CustomUserCreationForm


User = get_user_model()


class UserLinkInline(admin.TabularInline):
    model = UserLink

class UserRegistrationInline(admin.StackedInline):
    fk_name = 'user'
    model = UserRegistration
    can_delete = False
    verbose_name = 'Registration Details'
    verbose_name_plural = 'Registration Details'

class UserAbuseReportInline(admin.StackedInline):
    fk_name = 'logged_against'
    model = AbuseReport
    #can_delete = False
    extra = 0
    verbose_name = 'Abuse Report'
    verbose_name_plural = 'Abuse Reports'

class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 1

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'is_moderator', 'groups', 'user_permissions')}),
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

    inlines = (UserRegistrationInline, UserSkillInline, UserLinkInline,
               UserAbuseReportInline)

admin.site.register(CustomUser, CustomUserAdmin)

# Register Preferences brands and skills
admin.site.register(ConnectPreference)
admin.site.register(LinkBrand)
admin.site.register(Skill)
