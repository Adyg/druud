# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('druud', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='check_status',
            field=models.CharField(default=b'P', max_length=1, db_index=True, choices=[(b'P', b'Pending'), (b'R', b'Running')]),
        ),
    ]
