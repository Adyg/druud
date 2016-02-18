# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('druud', '0003_auto_20160204_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='check_type',
            field=models.CharField(db_index=True, max_length=1, choices=[(b'H', b'HEAD'), (b'G', b'GET'), (b'P', b'POST')]),
        ),
    ]
