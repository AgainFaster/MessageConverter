# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_converter', '0003_apiaccesssetting_nickname'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apiaccesssetting',
            options={'verbose_name': 'API Connection'},
        ),
        migrations.AlterModelOptions(
            name='apiheader',
            options={'verbose_name': 'API Header'},
        ),
        migrations.AlterModelOptions(
            name='apiproject',
            options={'verbose_name': 'API Project'},
        ),
        migrations.AlterModelOptions(
            name='convertedmessagequeue',
            options={'verbose_name': 'Converted Message'},
        ),
        migrations.AlterModelOptions(
            name='ftpaccesssetting',
            options={'verbose_name': 'FTP Connection'},
        ),
        migrations.AlterModelOptions(
            name='incomingmessage',
            options={'verbose_name': 'Incoming Message'},
        ),
        migrations.AlterModelOptions(
            name='messagetype',
            options={'verbose_name': 'Message Type'},
        ),
        migrations.AlterModelOptions(
            name='pullproject',
            options={'verbose_name': 'Pull Project'},
        ),
        migrations.AddField(
            model_name='ftpaccesssetting',
            name='organize_archive',
            field=models.BooleanField(help_text='Attempt to organize the Processed Path by Year/Month.', default=True),
        ),
    ]
