from django.contrib import admin

from .models import AbuseReport, UserRegistration, ModerationLogMsg

class UserRegistrationInline(admin.StackedInline):
    fk_name = 'user'
    model = UserRegistration
    can_delete = False
    verbose_name = 'Registration Details'
    verbose_name_plural = 'Registration Details'

class UserAbuseReportInline(admin.StackedInline):
    fk_name = 'logged_against'
    model = AbuseReport
    can_delete = False
    extra = 0
    verbose_name = 'Abuse Report'
    verbose_name_plural = 'Abuse Reports'

from django.contrib.auth.models import Permission
admin.site.register(Permission)

admin.site.register(ModerationLogMsg)
