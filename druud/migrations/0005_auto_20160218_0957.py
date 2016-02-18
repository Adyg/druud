# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerting', '0001_initial'),
        ('druud', '0004_auto_20160218_0726'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='check',
            name='contact',
            field=models.ManyToManyField(to='alerting.Contact'),
        ),
        migrations.AddField(
            model_name='alertlog',
            name='related_check',
            field=models.ForeignKey(to='druud.Check'),
        ),
        migrations.AddField(
            model_name='alertlog',
            name='related_contact',
            field=models.ForeignKey(to='alerting.Contact'),
        ),
    ]
