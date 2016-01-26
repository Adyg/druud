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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.TextField()),
                ('check_type', models.CharField(db_index=True, max_length=1, choices=[(b'A', b'Alive')])),
                ('check_frequency', models.CharField(db_index=True, max_length=1, choices=[(b'A', b'5min'), (b'B', b'10min')])),
                ('last_check', models.DateTimeField(default=django.utils.timezone.now)),
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
