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
        WAREHOUSEORDERSTATUS, created = orm.MessageType.objects.get_or_create(type_code='WAREHOUSEORDERSTATUS', name='Warehouse Order Status', format='CSV')
        WOFORDERSTATUS, created = orm.MessageType.objects.get_or_create(type_code='WOFORDERSTATUS', name='WOF Order Status', format='JSON')

    def backwards(self, orm):
        #orm.MessageType.objects.filter(type_code__in=['WOFORDERSTATUS', 'WAREHOUSEORDERSTATUS']).delete()
        pass

    models = {
        'message_converter.apiaccesssetting': {
            'Meta': {'object_name': 'ApiAccessSetting'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'message_converter.apiheader': {
            'Meta': {'object_name': 'ApiHeader'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'setting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.ApiAccessSetting']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'message_converter.apiproject': {
            'Meta': {'_ormbases': ['message_converter.Project'], 'object_name': 'ApiProject'},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['message_converter.Project']", 'primary_key': 'True', 'unique': 'True'})
        },
        'message_converter.convertedmessagequeue': {
            'Meta': {'object_name': 'ConvertedMessageQueue'},
            'converted_message': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_message': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'to': "orm['message_converter.IncomingMessage']", 'null': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.Project']"})
        },
        'message_converter.ftpaccesssetting': {
            'Meta': {'object_name': 'FtpAccessSetting'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'path': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'processed_path': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'last_delivered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.Project']", 'unique': 'True'})
        },
        'message_converter.lastpull': {
            'Meta': {'object_name': 'LastPull'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_pulled': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pull_project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.PullProject']", 'unique': 'True'})
        },
        'message_converter.messagetype': {
            'Meta': {'object_name': 'MessageType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type_code': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'message_converter.project': {
            'Meta': {'object_name': 'Project'},
            'conversion_parameters': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'delivery_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'from_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_type_projects'", 'to': "orm['message_converter.MessageType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'send_to_api': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'send_to_api_projects'", 'to': "orm['message_converter.ApiAccessSetting']", 'blank': 'True', 'null': 'True'}),
            'send_to_ftp': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'send_to_ftp_projects'", 'to': "orm['message_converter.FtpAccessSetting']", 'blank': 'True', 'null': 'True'}),
            'to_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_type_projects'", 'to': "orm['message_converter.MessageType']"})
        },
        'message_converter.pullproject': {
            'Meta': {'_ormbases': ['message_converter.Project'], 'object_name': 'PullProject'},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['message_converter.Project']", 'primary_key': 'True', 'unique': 'True'}),
            'pull_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'pull_from_api': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.ApiAccessSetting']", 'blank': 'True', 'null': 'True'}),
            'pull_from_ftp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.FtpAccessSetting']", 'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['message_converter']
    symmetrical = True
