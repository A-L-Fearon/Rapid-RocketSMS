# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Beneficiary'
        db.create_table(u'pathapp_beneficiary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('message_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('authenticated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('authen_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'pathapp', ['Beneficiary'])

        # Adding model 'Path'
        db.create_table(u'pathapp_path', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beneficiary_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pathapp.Beneficiary'], null=True)),
            ('balance', self.gf('django.db.models.fields.FloatField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'pathapp', ['Path'])

        # Adding model 'History'
        db.create_table(u'pathapp_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('confirmation_code', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'pathapp', ['History'])

        # Adding model 'Survey'
        db.create_table(u'pathapp_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('question_one', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('question_two', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('question_three', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('answer_one', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('answer_two', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('answer_three', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'pathapp', ['Survey'])


    def backwards(self, orm):
        # Deleting model 'Beneficiary'
        db.delete_table(u'pathapp_beneficiary')

        # Deleting model 'Path'
        db.delete_table(u'pathapp_path')

        # Deleting model 'History'
        db.delete_table(u'pathapp_history')

        # Deleting model 'Survey'
        db.delete_table(u'pathapp_survey')


    models = {
        u'pathapp.beneficiary': {
            'Meta': {'object_name': 'Beneficiary'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'authen_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'authenticated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pathapp.history': {
            'Meta': {'object_name': 'History'},
            'confirmation_code': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'message': ('django.db.models.fields.TextField', [], {})
        },
        u'pathapp.path': {
            'Meta': {'object_name': 'Path'},
            'balance': ('django.db.models.fields.FloatField', [], {}),
            'beneficiary_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pathapp.Beneficiary']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pathapp.survey': {
            'Meta': {'object_name': 'Survey'},
            'answer_one': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'answer_three': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'answer_two': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'question_one': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question_three': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question_two': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['pathapp']