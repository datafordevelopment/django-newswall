# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Source.ordering'
        db.delete_column('newswall_source', 'ordering')


    def backwards(self, orm):
        
        # Adding field 'Source.ordering'
        db.add_column('newswall_source', 'ordering', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    models = {
        'newswall.source': {
            'Meta': {'ordering': "['priority', 'name']", 'object_name': 'Source'},
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'priority': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'newswall.story': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Story'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'object_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': "orm['newswall.Source']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['newswall']
