# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ModerationLogMsg',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('msg_datetime', models.DateTimeField(auto_now_add=True)),
                ('msg_type', models.CharField(choices=[('INVITATION', 'Invitation'), ('REINVITATION', 'Invitation Resent'), ('REVOCATION', 'Invitation Revoked'), ('APPROVAL', 'Application Approved'), ('REJECTION', 'Application Rejected'), ('DISMISSAL', 'Abuse Report Dismissed'), ('WARNING', 'Official Warning'), ('BANNING', 'Ban User')], max_length=20)),
                ('comment', models.TextField()),
                ('pertains_to', models.ForeignKey(to_field='id', to=settings.AUTH_USER_MODEL)),
                ('logged_by', models.ForeignKey(to_field='id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Log Entry',
                'verbose_name_plural': 'Log Entries',
            },
            bases=(models.Model,),
        ),
    ]
