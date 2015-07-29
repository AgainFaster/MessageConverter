# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiAccessSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('host', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ApiHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('setting', models.ForeignKey(to='message_converter.ApiAccessSetting')),
            ],
        ),
        migrations.CreateModel(
            name='ConvertedMessageQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('converted_message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('delivered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FtpAccessSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('host', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('path', models.TextField(null=True, blank=True)),
                ('processed_path', models.TextField(help_text='This is the path where files will be moved to after they are processed. It will be ignored if delete_processed=True.', null=True, blank=True)),
                ('delete_processed', models.BooleanField(default=False, help_text='This will delete files after they are processed rather than moving them to the processed_path.')),
            ],
        ),
        migrations.CreateModel(
            name='IncomingMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('file_name', models.CharField(null=True, max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LastDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('last_delivered', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LastPull',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('last_pulled', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MessageType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type_code', models.CharField(max_length=100)),
                ('format', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, validators=[django.core.validators.RegexValidator('^[\\w-]+$', 'Enter only alphanumeric, dash, or underscore.', 'invalid')], max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('enabled', models.BooleanField(default=True)),
                ('conversion_parameters', models.TextField(help_text='JSON parameters', null=True, blank=True)),
                ('delivery_frequency', models.IntegerField(help_text='How often to deliver converted messages (in minutes). Use 0 for immediate. Minimum is the frequency of the deliver_messages periodic task.')),
                ('delivery_message_age', models.IntegerField(default=0, help_text='How old a message has to be (in minutes) before it can be delivered. Use 0 for immediate.')),
                ('messages_per_delivery', models.IntegerField(default=0, help_text='Maximum number of messages to send in one delivery call.')),
            ],
        ),
        migrations.CreateModel(
            name='ApiProject',
            fields=[
                ('project_ptr', models.OneToOneField(parent_link=True, to='message_converter.Project', primary_key=True, auto_created=True, serialize=False)),
            ],
            bases=('message_converter.project',),
        ),
        migrations.CreateModel(
            name='PullProject',
            fields=[
                ('project_ptr', models.OneToOneField(parent_link=True, to='message_converter.Project', primary_key=True, auto_created=True, serialize=False)),
                ('pull_frequency', models.IntegerField(help_text='How often to pull new messages (in minutes). Minimum is the frequency of the pull_messages periodic task.')),
                ('check_file_size_interval', models.IntegerField(default=0, help_text="How often to check on a file size (in seconds) to determine if the file is done being written to. 0 won't check.")),
                ('max_file_size_wait_time', models.IntegerField(default=300, help_text='Max time to wait for a file to be done being written to (in seconds). Default is 5 minutes.')),
                ('pull_from_api', models.ForeignKey(help_text='Pull from an API endpoint. Leave blank if pulling from an FTP instead.', null=True, to='message_converter.ApiAccessSetting', blank=True)),
                ('pull_from_ftp', models.ForeignKey(help_text='Pull from an FTP endpoint. Leave blank if pulling from an API instead.', null=True, to='message_converter.FtpAccessSetting', blank=True)),
            ],
            bases=('message_converter.project',),
        ),
        migrations.AddField(
            model_name='project',
            name='from_type',
            field=models.ForeignKey(to='message_converter.MessageType', related_name='from_type_projects'),
        ),
        migrations.AddField(
            model_name='project',
            name='send_to_api',
            field=models.ForeignKey(help_text='An API destination to deliver the converted messages.', null=True, related_name='send_to_api_projects', to='message_converter.ApiAccessSetting', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='send_to_ftp',
            field=models.ForeignKey(help_text='An FTP destination to deliver the converted messages.', null=True, related_name='send_to_ftp_projects', to='message_converter.FtpAccessSetting', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='to_type',
            field=models.ForeignKey(to='message_converter.MessageType', related_name='to_type_projects'),
        ),
        migrations.AddField(
            model_name='lastdelivery',
            name='project',
            field=models.ForeignKey(to='message_converter.Project', unique=True),
        ),
        migrations.AddField(
            model_name='incomingmessage',
            name='project',
            field=models.ForeignKey(to='message_converter.Project'),
        ),
        migrations.AddField(
            model_name='convertedmessagequeue',
            name='original_message',
            field=models.ForeignKey(null=True, to='message_converter.IncomingMessage', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='convertedmessagequeue',
            name='project',
            field=models.ForeignKey(to='message_converter.Project'),
        ),
        migrations.AddField(
            model_name='lastpull',
            name='pull_project',
            field=models.ForeignKey(to='message_converter.PullProject', unique=True),
        ),
    ]
