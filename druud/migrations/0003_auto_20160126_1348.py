# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('druud', '0002_check_check_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check',
            name='last_check',
        ),
        migrations.AddField(
            model_name='check',
            name='next_check',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='check',
            name='check_frequency',
            field=models.CharField(db_index=True, max_length=3, choices=[(b'5', b'5min'), (b'10', b'10min')]),
        ),
    ]
