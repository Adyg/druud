# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('druud', '0005_auto_20160218_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertlog',
            name='alert_message',
            field=models.TextField(default=b''),
        ),
    ]
