from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from connect.accounts.models import (
    AbuseReport, CustomUser, Role, LinkBrand,
    Skill, UserLink, UserSkill
)
from connect.accounts.forms import CustomUserChangeForm, CustomUserCreationForm


User = get_user_model()


class UserLinkInline(admin.TabularInline):
    model = UserLink


class UserAbuseReportInline(admin.StackedInline):
    fk_name = 'logged_against'
    model = AbuseReport
    extra = 0
    verbose_name = _('Abuse Report')


class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 1


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Registration info'), {'fields': ('registration_method',
                                             'application_comments',
                                             'moderator',
                                             'moderator_decision',
                                             'auth_token',
                                             'auth_token_is_used')}),
        (_('Important dates'), {'fields': ('applied_datetime',
                                           'decision_datetime',
                                           'activated_datetime',
                                           'last_login',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_closed', 'is_staff',
                                       'is_superuser', 'is_moderator',
                                       'groups', 'user_permissions')}),
        (_('Roles'), {'fields': ('roles',)}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'full_name', 'is_staff')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    inlines = (UserSkillInline, UserLinkInline, UserAbuseReportInline)

admin.site.register(CustomUser, CustomUserAdmin)

# Register Preferences brands and skills
admin.site.register(Role)
admin.site.register(LinkBrand)
admin.site.register(Skill)
