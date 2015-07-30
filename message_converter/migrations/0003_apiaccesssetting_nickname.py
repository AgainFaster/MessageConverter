# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_converter', '0002_auto_20150625_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiaccesssetting',
            name='nickname',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
