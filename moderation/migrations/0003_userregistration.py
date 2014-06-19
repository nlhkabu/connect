# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0002_moderationlogmsg'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('user', models.OneToOneField(to_field='id', to=settings.AUTH_USER_MODEL)),
                ('method', models.CharField(choices=[('INV', 'Invited'), ('REQ', 'Requested')], max_length=20)),
                ('moderator', models.ForeignKey(null=True, to_field='id', blank=True, to=settings.AUTH_USER_MODEL, help_text='Moderator who invited, approved or rejected this user')),
                ('applied_datetime', models.DateTimeField(null=True, blank=True)),
                ('application_comments', models.TextField(blank=True)),
                ('moderator_decision', models.CharField(choices=[('PRE', 'Pre-approved'), ('APP', 'Approved'), ('REJ', 'Rejected')], max_length=20, blank=True)),
                ('decision_datetime', models.DateTimeField(null=True, blank=True)),
                ('auth_token', models.CharField(verbose_name='Authetication token', max_length=40, blank=True)),
                ('activated_datetime', models.DateTimeField(null=True, blank=True)),
                ('auth_token_is_used', models.BooleanField(verbose_name='Token is used', default=False)),
            ],
            options={
                'permissions': (('invite_user', 'Can invite a new user'), ('access_moderators_page', 'Can see the moderators page')),
            },
            bases=(models.Model,),
        ),
    ]
