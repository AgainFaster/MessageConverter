# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.conversion_parameters'
        db.add_column('message_converter_project', 'conversion_parameters',
                      self.gf('django.db.models.fields.TextField')(blank=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.conversion_parameters'
        db.delete_column('message_converter_project', 'conversion_parameters')


    models = {
        'message_converter.apiaccesssetting': {
            'Meta': {'object_name': 'ApiAccessSetting'},
            'api_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'host': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'message_converter.apiproject': {
            'Meta': {'object_name': 'ApiProject', '_ormbases': ['message_converter.Project']},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['message_converter.Project']", 'primary_key': 'True'})
        },
        'message_converter.convertedmessagequeue': {
            'Meta': {'object_name': 'ConvertedMessageQueue'},
            'converted_message': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_message': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['message_converter.IncomingMessage']", 'on_delete': 'models.SET_NULL'}),
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
            'project': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'to': "orm['message_converter.Project']"})
        },
        'message_converter.messagetype': {
            'Meta': {'object_name': 'MessageType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'message_converter.project': {
            'Meta': {'object_name': 'Project'},
            'conversion_parameters': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'delivery_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'from_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.MessageType']", 'related_name': "'from_type_projects'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'send_to_api': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'send_to_api_projects'", 'blank': 'True', 'to': "orm['message_converter.ApiAccessSetting']"}),
            'send_to_ftp': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'send_to_ftp_projects'", 'blank': 'True', 'to': "orm['message_converter.FtpAccessSetting']"}),
            'to_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.MessageType']", 'related_name': "'to_type_projects'"})
        },
        'message_converter.pullproject': {
            'Meta': {'object_name': 'PullProject', '_ormbases': ['message_converter.Project']},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['message_converter.Project']", 'primary_key': 'True'}),
            'pull_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'pull_from_api': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['message_converter.ApiAccessSetting']"}),
            'pull_from_ftp': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['message_converter.FtpAccessSetting']"})
        }
    }

    complete_apps = ['message_converter']