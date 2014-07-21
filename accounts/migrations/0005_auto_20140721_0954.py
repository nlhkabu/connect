# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_abusereport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('proficiency', models.IntegerField(max_length=2, default=10, choices=[('', '---------'), (10, 'Beginner'), (20, 'Intermediate'), (30, 'Advanced'), (40, 'Expert')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='skill',
            name='owner',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='accounts.UserSkill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userskill',
            name='skill',
            field=models.ForeignKey(to='accounts.Skill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userskill',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='userskill',
            unique_together=set([('user', 'skill')]),
        ),
    ]
