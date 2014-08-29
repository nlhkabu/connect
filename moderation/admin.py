from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import ModerationLogMsg

admin.site.register(Permission)
admin.site.register(ModerationLogMsg)
#~admin.site.register(ModerationLogMsg, ModerationLogMsgAdmin)
