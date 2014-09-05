# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.delivery_message_age'
        db.add_column('message_converter_project', 'delivery_message_age',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.delivery_message_age'
        db.delete_column('message_converter_project', 'delivery_message_age')


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
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['message_converter.Project']"})
        },
        'message_converter.convertedmessagequeue': {
            'Meta': {'object_name': 'ConvertedMessageQueue'},
            'converted_message': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_message': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['message_converter.IncomingMessage']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.Project']"})
        },
        'message_converter.ftpaccesssetting': {
            'Meta': {'object_name': 'FtpAccessSetting'},
            'delete_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'path': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'processed_path': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'message_converter.incomingmessage': {
            'Meta': {'object_name': 'IncomingMessage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.Project']"})
        },
        'message_converter.lastdelivery': {
            'Meta': {'object_name': 'LastDelivery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_delivered': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'to': "orm['message_converter.Project']"})
        },
        'message_converter.lastpull': {
            'Meta': {'object_name': 'LastPull'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_pulled': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'pull_project': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'to': "orm['message_converter.PullProject']"})
        },
        'message_converter.messagetype': {
            'Meta': {'object_name': 'MessageType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type_code': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'message_converter.project': {
            'Meta': {'object_name': 'Project'},
            'conversion_parameters': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'delivery_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'delivery_message_age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'from_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_type_projects'", 'to': "orm['message_converter.MessageType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'send_to_api': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'related_name': "'send_to_api_projects'", 'to': "orm['message_converter.ApiAccessSetting']"}),
            'send_to_ftp': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'related_name': "'send_to_ftp_projects'", 'to': "orm['message_converter.FtpAccessSetting']"}),
            'to_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_type_projects'", 'to': "orm['message_converter.MessageType']"})
        },
        'message_converter.pullproject': {
            'Meta': {'_ormbases': ['message_converter.Project'], 'object_name': 'PullProject'},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['message_converter.Project']"}),
            'pull_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'pull_from_api': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['message_converter.ApiAccessSetting']"}),
            'pull_from_ftp': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['message_converter.FtpAccessSetting']"})
        }
    }

    complete_apps = ['message_converter']