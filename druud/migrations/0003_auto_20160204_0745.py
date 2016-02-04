# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import druud.models


class Migration(migrations.Migration):

    dependencies = [
        ('druud', '0002_auto_20160127_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckPayload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.TextField()),
                ('value', models.TextField(null=True, blank=True)),
                ('pfile', models.FileField(null=True, upload_to=druud.models.payload_directory, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='check',
            name='post_data',
        ),
        migrations.AlterField(
            model_name='check',
            name='check_type',
            field=models.CharField(db_index=True, max_length=1, choices=[(b'H', b'HEAD'), (b'G', b'GET'), (b'P', b'POST'), (b'U', b'PUT'), (b'D', b'DELETE'), (b'O', b'OPTIONS')]),
        ),
        migrations.AddField(
            model_name='checkpayload',
            name='related_check',
            field=models.ForeignKey(to='druud.Check'),
        ),
    ]
