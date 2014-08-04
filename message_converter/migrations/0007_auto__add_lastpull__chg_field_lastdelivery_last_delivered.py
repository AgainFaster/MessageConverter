# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LastPull'
        db.create_table('message_converter_lastpull', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pull_project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['message_converter.PullProject'], unique=True)),
            ('last_pulled', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('message_converter', ['LastPull'])


        # Changing field 'LastDelivery.last_delivered'
        db.alter_column('message_converter_lastdelivery', 'last_delivered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):
        # Deleting model 'LastPull'
        db.delete_table('message_converter_lastpull')


        # Changing field 'LastDelivery.last_delivered'
        db.alter_column('message_converter_lastdelivery', 'last_delivered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'Meta': {'object_name': 'ApiProject', '_ormbases': ['message_converter.Project']},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['message_converter.Project']", 'unique': 'True'})
        },
        'message_converter.apitoken': {
            'Meta': {'unique_together': "(('client_id', 'key'),)", 'object_name': 'ApiToken'},
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'related_name': "'api_auth_token'", 'unique': 'True'})
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
            'host': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'path': ('django.db.models.fields.TextField', [], {}),
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
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'message_converter.project': {
            'Meta': {'object_name': 'Project'},
            'conversion_parameters': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'delivery_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'from_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.MessageType']", 'related_name': "'from_type_projects'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'send_to_api': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['message_converter.ApiAccessSetting']", 'related_name': "'send_to_api_projects'", 'blank': 'True'}),
            'send_to_ftp': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['message_converter.FtpAccessSetting']", 'related_name': "'send_to_ftp_projects'", 'blank': 'True'}),
            'to_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.MessageType']", 'related_name': "'to_type_projects'"})
        },
        'message_converter.pullproject': {
            'Meta': {'object_name': 'PullProject', '_ormbases': ['message_converter.Project']},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['message_converter.Project']", 'unique': 'True'}),
            'pull_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'pull_from_api': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['message_converter.ApiAccessSetting']", 'blank': 'True'}),
            'pull_from_ftp': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['message_converter.FtpAccessSetting']", 'blank': 'True'})
        }
    }

    complete_apps = ['message_converter']