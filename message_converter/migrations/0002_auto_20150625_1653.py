# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_converter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastdelivery',
            name='project',
            field=models.OneToOneField(to='message_converter.Project'),
        ),
        migrations.AlterField(
            model_name='lastpull',
            name='pull_project',
            field=models.OneToOneField(to='message_converter.PullProject'),
        ),
    ]
