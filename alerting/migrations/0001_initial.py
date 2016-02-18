# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
