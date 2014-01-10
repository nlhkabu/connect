from django.contrib import admin

from skills.models import Skill, UserSkill

admin.site.register(Skill)
admin.site.register(UserSkill)
