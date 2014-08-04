# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ApiAccessSetting', fields ['host']
        db.delete_unique('message_converter_apiaccesssetting', ['host'])

        # Removing unique constraint on 'FtpAccessSetting', fields ['user']
        db.delete_unique('message_converter_ftpaccesssetting', ['user'])

        # Removing unique constraint on 'FtpAccessSetting', fields ['host']
        db.delete_unique('message_converter_ftpaccesssetting', ['host'])

        # Removing unique constraint on 'FtpAccessSetting', fields ['password']
        db.delete_unique('message_converter_ftpaccesssetting', ['password'])

        # Adding model 'ApiHeader'
        db.create_table('message_converter_apiheader', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('setting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['message_converter.ApiAccessSetting'])),
        ))
        db.send_create_signal('message_converter', ['ApiHeader'])

        # Deleting field 'ApiAccessSetting.api_key'
        db.delete_column('message_converter_apiaccesssetting', 'api_key')

        # Deleting field 'ApiAccessSetting.user'
        db.delete_column('message_converter_apiaccesssetting', 'user')


    def backwards(self, orm):
        # Deleting model 'ApiHeader'
        db.delete_table('message_converter_apiheader')

        # Adding unique constraint on 'FtpAccessSetting', fields ['password']
        db.create_unique('message_converter_ftpaccesssetting', ['password'])

        # Adding unique constraint on 'FtpAccessSetting', fields ['host']
        db.create_unique('message_converter_ftpaccesssetting', ['host'])

        # Adding unique constraint on 'FtpAccessSetting', fields ['user']
        db.create_unique('message_converter_ftpaccesssetting', ['user'])

        # Adding field 'ApiAccessSetting.api_key'
        db.add_column('message_converter_apiaccesssetting', 'api_key',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, unique=True),
                      keep_default=False)

        # Adding field 'ApiAccessSetting.user'
        db.add_column('message_converter_apiaccesssetting', 'user',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, unique=True),
                      keep_default=False)

        # Adding unique constraint on 'ApiAccessSetting', fields ['host']
        db.create_unique('message_converter_apiaccesssetting', ['host'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'ordering': "('name',)"},
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
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['message_converter.Project']", 'unique': 'True', 'primary_key': 'True'})
        },
        'message_converter.apitoken': {
            'Meta': {'object_name': 'ApiToken', 'unique_together': "(('client_id', 'key'),)"},
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'api_auth_token'", 'unique': 'True', 'to': "orm['auth.User']"})
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
            'host': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'conversion_parameters': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'delivery_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'from_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_type_projects'", 'to': "orm['message_converter.MessageType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'send_to_api': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'send_to_api_projects'", 'blank': 'True', 'to': "orm['message_converter.ApiAccessSetting']"}),
            'send_to_ftp': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'send_to_ftp_projects'", 'blank': 'True', 'to': "orm['message_converter.FtpAccessSetting']"}),
            'to_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_type_projects'", 'to': "orm['message_converter.MessageType']"})
        },
        'message_converter.pullproject': {
            'Meta': {'object_name': 'PullProject', '_ormbases': ['message_converter.Project']},
            'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['message_converter.Project']", 'unique': 'True', 'primary_key': 'True'}),
            'pull_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'pull_from_api': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['message_converter.ApiAccessSetting']"}),
            'pull_from_ftp': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['message_converter.FtpAccessSetting']"})
        }
    }

    complete_apps = ['message_converter']