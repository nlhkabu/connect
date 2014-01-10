from django.contrib import admin

from skills.models import Skill, UserSkill

admin.site.register(Skill)
#admin.site.register(UserSkill)

class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 1
