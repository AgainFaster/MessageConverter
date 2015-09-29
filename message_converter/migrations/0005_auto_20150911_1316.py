# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_converter', '0004_auto_20150909_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='convertedmessagequeue',
            name='file_name',
            field=models.CharField(max_length=200, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='apiheader',
            name='setting',
            field=models.ForeignKey(to='message_converter.ApiAccessSetting', related_name='headers'),
        ),
    ]
