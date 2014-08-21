from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import (AbuseReport, CustomUser, Role, LinkBrand,
                     Skill, UserLink, UserSkill)
from .forms import CustomUserChangeForm, CustomUserCreationForm


User = get_user_model()


class UserLinkInline(admin.TabularInline):
    model = UserLink

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
        ('Registration info', {'fields': ('registration_method',
                                          'application_comments',
                                          'moderator',
                                          'moderator_decision',
                                          'auth_token',
                                          'auth_token_is_used')}),
        ('Important dates', {'fields': ('applied_datetime',
                                        'decision_datetime',
                                        'activated_datetime',
                                        'last_login',)}),
        ('Permissions', {'fields': ('is_active', 'is_closed', 'is_staff',
                                    'is_superuser', 'is_moderator',
                                    'groups', 'user_permissions')}),
        ('Roles', {'fields': ('roles',)}),

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

    inlines = (UserSkillInline, UserLinkInline, UserAbuseReportInline)

admin.site.register(CustomUser, CustomUserAdmin)

# Register Preferences brands and skills
admin.site.register(Role)
admin.site.register(LinkBrand)
admin.site.register(Skill)
