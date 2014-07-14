# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MessageType'
        db.create_table('message_converter_messagetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('message_converter', ['MessageType'])

        # Adding model 'ApiAccessSetting'
        db.create_table('message_converter_apiaccesssetting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('user', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('api_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('message_converter', ['ApiAccessSetting'])

        # Adding model 'FtpAccessSetting'
        db.create_table('message_converter_ftpaccesssetting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('user', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('password', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('path', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('message_converter', ['FtpAccessSetting'])

        # Adding model 'Project'
        db.create_table('message_converter_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('from_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_type_projects', to=orm['message_converter.MessageType'])),
            ('to_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_type_projects', to=orm['message_converter.MessageType'])),
            ('send_to_ftp', self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='send_to_ftp_projects', to=orm['message_converter.FtpAccessSetting'], blank=True)),
            ('send_to_api', self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='send_to_api_projects', to=orm['message_converter.ApiAccessSetting'], blank=True)),
            ('delivery_frequency', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('message_converter', ['Project'])

        # Adding model 'ApiProject'
        db.create_table('message_converter_apiproject', (
            ('project_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['message_converter.Project'])),
        ))
        db.send_create_signal('message_converter', ['ApiProject'])

        # Adding model 'PullProject'
        db.create_table('message_converter_pullproject', (
            ('project_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['message_converter.Project'])),
            ('pull_from_ftp', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['message_converter.FtpAccessSetting'], blank=True)),
            ('pull_from_api', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['message_converter.ApiAccessSetting'], blank=True)),
            ('pull_frequency', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('message_converter', ['PullProject'])

        # Adding model 'IncomingMessage'
        db.create_table('message_converter_incomingmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['message_converter.Project'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('message_converter', ['IncomingMessage'])

        # Adding model 'ConvertedMessageQueue'
        db.create_table('message_converter_convertedmessagequeue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_message', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.SET_NULL, null=True, to=orm['message_converter.IncomingMessage'])),
            ('converted_message', self.gf('django.db.models.fields.TextField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['message_converter.Project'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('delivered', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('message_converter', ['ConvertedMessageQueue'])

        # Adding model 'LastDelivery'
        db.create_table('message_converter_lastdelivery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['message_converter.Project'])),
            ('last_delivered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('message_converter', ['LastDelivery'])


    def backwards(self, orm):
        # Deleting model 'MessageType'
        db.delete_table('message_converter_messagetype')

        # Deleting model 'ApiAccessSetting'
        db.delete_table('message_converter_apiaccesssetting')

        # Deleting model 'FtpAccessSetting'
        db.delete_table('message_converter_ftpaccesssetting')

        # Deleting model 'Project'
        db.delete_table('message_converter_project')

        # Deleting model 'ApiProject'
        db.delete_table('message_converter_apiproject')

        # Deleting model 'PullProject'
        db.delete_table('message_converter_pullproject')

        # Deleting model 'IncomingMessage'
        db.delete_table('message_converter_incomingmessage')

        # Deleting model 'ConvertedMessageQueue'
        db.delete_table('message_converter_convertedmessagequeue')

        # Deleting model 'LastDelivery'
        db.delete_table('message_converter_lastdelivery')


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
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['message_converter.Project']"})
        },
        'message_converter.convertedmessagequeue': {
            'Meta': {'object_name': 'ConvertedMessageQueue'},
            'converted_message': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'message_converter.project': {
            'Meta': {'object_name': 'Project'},
            'delivery_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'from_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_type_projects'", 'to': "orm['message_converter.MessageType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'send_to_api': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'send_to_api_projects'", 'to': "orm['message_converter.ApiAccessSetting']", 'blank': 'True'}),
            'send_to_ftp': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'send_to_ftp_projects'", 'to': "orm['message_converter.FtpAccessSetting']", 'blank': 'True'}),
            'to_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_type_projects'", 'to': "orm['message_converter.MessageType']"})
        },
        'message_converter.pullproject': {
            'Meta': {'object_name': 'PullProject', '_ormbases': ['message_converter.Project']},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['message_converter.Project']"}),
            'pull_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'pull_from_api': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['message_converter.ApiAccessSetting']", 'blank': 'True'}),
            'pull_from_ftp': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['message_converter.FtpAccessSetting']", 'blank': 'True'})
        }
    }

    complete_apps = ['message_converter']