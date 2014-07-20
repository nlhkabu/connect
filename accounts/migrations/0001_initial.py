# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(verbose_name='email address', unique=True, max_length=254)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('bio', models.TextField(blank=True)),
                ('is_moderator', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(verbose_name='groups', to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', blank=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'permissions': (('access_moderators_section', 'Can see the moderators section'), ('invite_user', 'Can issue or reissue an invitation'), ('uninvite_user', 'Can revoke a user invitation'), ('approve_user_application', "Can approve a user's application"), ('reject_user_application', "Can reject a user's application"), ('dismiss_abuse_report', 'Can dismiss an abuse report'), ('warn_user', 'Can warn a user in response to an abuse report'), ('ban_user', 'Can ban a user in response to an abuse report')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConnectPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Preference',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='customuser',
            name='connect_preferences',
            field=models.ManyToManyField(null=True, to='accounts.ConnectPreference', blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='LinkBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=100)),
                ('domain', models.CharField(unique=True, max_length=100)),
                ('fa_icon', models.CharField(verbose_name='Font Awesome Icon', max_length=100, help_text='Choose an icon name from <a href="http://fontawesome.io/icons/">Font Awesome</a> (v4.0.3)')),
            ],
            options={
                'verbose_name': 'Brand',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anchor', models.CharField(max_length=100, verbose_name='Anchor Text')),
                ('url', models.URLField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Link',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='userlink',
            unique_together=set([('user', 'anchor'), ('user', 'url')]),
        ),
    ]
