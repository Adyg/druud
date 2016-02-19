# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('druud', '0006_alertlog_alert_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertlog',
            name='alert_status',
            field=models.CharField(default=b'P', max_length=1, null=True, blank=True, choices=[(b'P', b'Pending'), (b'S', b'Sent'), (b'F', b'Failed')]),
        ),
    ]
