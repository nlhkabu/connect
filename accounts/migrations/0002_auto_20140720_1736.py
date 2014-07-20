# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Group, Permission
from django.db import models, migrations

def create_moderator_group(apps, schema_editor):
    """
    Creates a moderator group with moderation permissions
    """
    codenames = ['access_moderators_section',
                 'invite_user',
                 'uninvite_user',
                 'approve_user_application',
                 'reject_user_application',
                 'dismiss_abuse_report',
                 'warn_user',
                 'ban_user',
                 'add_userregistration',
                 'change_userregistration',
                 'add_abusereport',
                 'add_moderationlogmsg']

    moderator_permissions = Permission.objects.filter(codename__in=codenames)
    moderators_group = Group.objects.create(name='moderators')
    moderators_group.permissions = moderator_permissions


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_moderator_group),
    ]

