# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        from_type, created = orm.MessageType.objects.get_or_create(type='JSON')
        to_type, created = orm.MessageType.objects.get_or_create(type='CSV')

        orm.ApiProject.objects.get_or_create(name="order-message", from_type=from_type, to_type=to_type, delivery_frequency=15)

        interval, created = orm['djcelery.IntervalSchedule'].objects.get_or_create(period='minutes', every=5)
        orm['djcelery.PeriodicTask'].objects.get_or_create(interval=interval, name='Deliver Messages',
                                                    task='message_converter.tasks.deliver_messages')

        orm['djcelery.PeriodicTask'].objects.get_or_create(interval=interval, name='Pull Messages',
                                            task='message_converter.tasks.pull_messages')

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'djcelery.crontabschedule': {
            'Meta': {'ordering': "['month_of_year', 'day_of_month', 'day_of_week', 'hour', 'minute']", 'object_name': 'CrontabSchedule'},
            'day_of_month': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'*'"}),
            'day_of_week': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'*'"}),
            'hour': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'*'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minute': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'*'"}),
            'month_of_year': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': "'*'"})
        },
        'djcelery.intervalschedule': {
            'Meta': {'ordering': "['period', 'every']", 'object_name': 'IntervalSchedule'},
            'every': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.CharField', [], {'max_length': '24'})
        },
        'djcelery.periodictask': {
            'Meta': {'object_name': 'PeriodicTask'},
            'args': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "'[]'"}),
            'crontab': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['djcelery.CrontabSchedule']"}),
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'exchange': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200', 'null': 'True', 'default': 'None'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['djcelery.IntervalSchedule']"}),
            'kwargs': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "'{}'"}),
            'last_run_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'queue': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200', 'null': 'True', 'default': 'None'}),
            'routing_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200', 'null': 'True', 'default': 'None'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'total_run_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'djcelery.periodictasks': {
            'Meta': {'object_name': 'PeriodicTasks'},
            'ident': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True', 'unique': 'True', 'default': '1'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {})
        },
        'djcelery.taskmeta': {
            'Meta': {'db_table': "'celery_taskmeta'", 'object_name': 'TaskMeta'},
            'date_done': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('djcelery.picklefield.PickledObjectField', [], {'null': 'True', 'default': 'None'}),
            'result': ('djcelery.picklefield.PickledObjectField', [], {'null': 'True', 'default': 'None'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'PENDING'"}),
            'task_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'traceback': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'})
        },
        'djcelery.tasksetmeta': {
            'Meta': {'db_table': "'celery_tasksetmeta'", 'object_name': 'TaskSetMeta'},
            'date_done': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('djcelery.picklefield.PickledObjectField', [], {}),
            'taskset_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'djcelery.taskstate': {
            'Meta': {'ordering': "['-tstamp']", 'object_name': 'TaskState'},
            'args': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'eta': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwargs': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'retries': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'runtime': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64'}),
            'task_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'traceback': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'tstamp': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djcelery.WorkerState']", 'null': 'True'})
        },
        'djcelery.workerstate': {
            'Meta': {'ordering': "['-last_heartbeat']", 'object_name': 'WorkerState'},
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_heartbeat': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True'})
        },
        'message_converter.apiaccesssetting': {
            'Meta': {'object_name': 'ApiAccessSetting'},
            'api_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'host': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'message_converter.apiproject': {
            'Meta': {'_ormbases': ['message_converter.Project'], 'object_name': 'ApiProject'},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['message_converter.Project']", 'unique': 'True'})
        },
        'message_converter.convertedmessagequeue': {
            'Meta': {'object_name': 'ConvertedMessageQueue'},
            'converted_message': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.IncomingMessage']", 'on_delete': 'models.SET_NULL', 'null': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.Project']"})
        },
        'message_converter.ftpaccesssetting': {
            'Meta': {'object_name': 'FtpAccessSetting'},
            'host': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'message_converter.incomingmessage': {
            'Meta': {'object_name': 'IncomingMessage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.Project']"})
        },
        'message_converter.lastdelivery': {
            'Meta': {'object_name': 'LastDelivery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_delivered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.Project']", 'unique': 'True'})
        },
        'message_converter.messagetype': {
            'Meta': {'object_name': 'MessageType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'message_converter.project': {
            'Meta': {'object_name': 'Project'},
            'delivery_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'from_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.MessageType']", 'related_name': "'from_type_projects'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'send_to_api': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'send_to_api_projects'", 'null': 'True', 'to': "orm['message_converter.ApiAccessSetting']"}),
            'send_to_ftp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'send_to_ftp_projects'", 'null': 'True', 'to': "orm['message_converter.FtpAccessSetting']"}),
            'to_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.MessageType']", 'related_name': "'to_type_projects'"})
        },
        'message_converter.pullproject': {
            'Meta': {'_ormbases': ['message_converter.Project'], 'object_name': 'PullProject'},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['message_converter.Project']", 'unique': 'True'}),
            'pull_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'pull_from_api': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['message_converter.ApiAccessSetting']"}),
            'pull_from_ftp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['message_converter.FtpAccessSetting']"})
        }
    }

    complete_apps = ['djcelery', 'message_converter']
    symmetrical = True
