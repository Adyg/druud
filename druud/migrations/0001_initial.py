# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.TextField()),
                ('address', models.TextField()),
                ('check_type', models.CharField(db_index=True, max_length=1, choices=[(b'H', b'Head')])),
                ('check_frequency', models.CharField(db_index=True, max_length=3, choices=[(b'5', b'5min'), (b'10', b'10min')])),
                ('check_status', models.CharField(default=b'P', max_length=1, db_index=True, choices=[(b'P', b'Pending'), (b'R', b'Running')])),
                ('next_check', models.DateTimeField(default=django.utils.timezone.now)),
                ('port', models.IntegerField(null=True, blank=True)),
                ('http_auth_username', models.TextField(null=True, blank=True)),
                ('http_auth_password', models.TextField(null=True, blank=True)),
                ('post_data', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CheckLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result', models.IntegerField()),
                ('status', models.TextField()),
                ('elapsed', models.IntegerField()),
                ('check_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('error', models.TextField(null=True, blank=True)),
                ('error_message', models.TextField(null=True, blank=True)),
                ('related_check', models.ForeignKey(to='druud.Check')),
            ],
        ),
        migrations.CreateModel(
            name='CheckRequestHeader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('header_key', models.TextField()),
                ('header_value', models.TextField(null=True, blank=True)),
                ('related_check', models.ForeignKey(to='druud.Check')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='check',
            name='project',
            field=models.ForeignKey(to='druud.Project'),
        ),
    ]
