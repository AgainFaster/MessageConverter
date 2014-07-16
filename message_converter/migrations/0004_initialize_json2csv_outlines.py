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

        project = orm.ApiProject.objects.get(name='order-message')
        project.conversion_parameters = """
            {
                    "outlines": [
                        {"first_record": ["record_type", "HDR"], "map": [["billing_address_city", "order.billing_address.city"], ["billing_address_firstname", "order.billing_address.firstname"]]},
                        {"collection": "order.line_items", "first_record": ["record_type", "DTL"], "map": [["line_item_name", "name"], ["line_item_quantity", "quantity"]]}
                    ]
            }"""

        project.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'message_converter.apiaccesssetting': {
            'Meta': {'object_name': 'ApiAccessSetting'},
            'api_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'host': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'message_converter.apiproject': {
            'Meta': {'_ormbases': ['message_converter.Project'], 'object_name': 'ApiProject'},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['message_converter.Project']", 'primary_key': 'True', 'unique': 'True'})
        },
        'message_converter.convertedmessagequeue': {
            'Meta': {'object_name': 'ConvertedMessageQueue'},
            'converted_message': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_message': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'null': 'True', 'to': "orm['message_converter.IncomingMessage']"}),
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
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.Project']"})
        },
        'message_converter.lastdelivery': {
            'Meta': {'object_name': 'LastDelivery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_delivered': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
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
            'conversion_parameters': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'delivery_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'from_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.MessageType']", 'related_name': "'from_type_projects'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'send_to_api': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['message_converter.ApiAccessSetting']", 'related_name': "'send_to_api_projects'"}),
            'send_to_ftp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['message_converter.FtpAccessSetting']", 'related_name': "'send_to_ftp_projects'"}),
            'to_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.MessageType']", 'related_name': "'to_type_projects'"})
        },
        'message_converter.pullproject': {
            'Meta': {'_ormbases': ['message_converter.Project'], 'object_name': 'PullProject'},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['message_converter.Project']", 'primary_key': 'True', 'unique': 'True'}),
            'pull_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'pull_from_api': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['message_converter.ApiAccessSetting']"}),
            'pull_from_ftp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['message_converter.FtpAccessSetting']"})
        }
    }

    complete_apps = ['message_converter']
    symmetrical = True
