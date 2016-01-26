# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('druud', '0003_auto_20160126_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('results', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='check',
            name='id',
        ),
        migrations.AddField(
            model_name='check',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='checklog',
            name='related_check',
            field=models.ForeignKey(to='druud.Check'),
        ),
    ]
