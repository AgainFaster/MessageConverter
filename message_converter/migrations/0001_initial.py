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

        # Adding model 'IncomingMessage'
        db.create_table('message_converter_incomingmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['message_converter.MessageType'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('message_converter', ['IncomingMessage'])

        # Adding model 'ConvertedMessageQueue'
        db.create_table('message_converter_convertedmessagequeue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_message', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.SET_NULL, to=orm['message_converter.IncomingMessage'], null=True)),
            ('converted_message', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['message_converter.MessageType'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('message_converter', ['ConvertedMessageQueue'])


    def backwards(self, orm):
        # Deleting model 'MessageType'
        db.delete_table('message_converter_messagetype')

        # Deleting model 'IncomingMessage'
        db.delete_table('message_converter_incomingmessage')

        # Deleting model 'ConvertedMessageQueue'
        db.delete_table('message_converter_convertedmessagequeue')


    models = {
        'message_converter.convertedmessagequeue': {
            'Meta': {'object_name': 'ConvertedMessageQueue'},
            'converted_message': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_message': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'to': "orm['message_converter.IncomingMessage']", 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.MessageType']"})
        },
        'message_converter.incomingmessage': {
            'Meta': {'object_name': 'IncomingMessage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message_converter.MessageType']"})
        },
        'message_converter.messagetype': {
            'Meta': {'object_name': 'MessageType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['message_converter']