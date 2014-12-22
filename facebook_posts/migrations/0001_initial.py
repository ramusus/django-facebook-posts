# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Post'
        db.create_table('facebook_posts_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('graph_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('author_json', self.gf('annoying.fields.JSONField')(null=True)),
            ('owners_json', self.gf('annoying.fields.JSONField')(null=True)),
            ('author_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='facebook_posts', null=True, to=orm['contenttypes.ContentType'])),
            ('author_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', null=True, to=orm['facebook_applications.Application'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('object_id', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('picture', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('icon', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('story', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('properties', self.gf('annoying.fields.JSONField')(null=True)),
            ('actions', self.gf('annoying.fields.JSONField')(null=True)),
            ('privacy', self.gf('annoying.fields.JSONField')(null=True)),
            ('place', self.gf('annoying.fields.JSONField')(null=True)),
            ('message_tags', self.gf('annoying.fields.JSONField')(null=True)),
            ('story_tags', self.gf('annoying.fields.JSONField')(null=True)),
            ('with_tags', self.gf('annoying.fields.JSONField')(null=True)),
            ('likes', self.gf('annoying.fields.JSONField')(null=True)),
            ('comments', self.gf('annoying.fields.JSONField')(null=True)),
            ('status_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('likes_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('comments_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('facebook_posts', ['Post'])

        # Adding model 'PostOwner'
        db.create_table('facebook_posts_postowner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owners', to=orm['facebook_posts.Post'])),
            ('owner_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='facebook_page_posts', null=True, to=orm['contenttypes.ContentType'])),
            ('owner_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal('facebook_posts', ['PostOwner'])

        # Adding unique constraint on 'PostOwner', fields ['post', 'owner_content_type', 'owner_id']
        db.create_unique('facebook_posts_postowner', ['post_id', 'owner_content_type_id', 'owner_id'])

    def backwards(self, orm):
        # Removing unique constraint on 'PostOwner', fields ['post', 'owner_content_type', 'owner_id']
        db.delete_unique('facebook_posts_postowner', ['post_id', 'owner_content_type_id', 'owner_id'])

        # Deleting model 'Post'
        db.delete_table('facebook_posts_post')

        # Deleting model 'PostOwner'
        db.delete_table('facebook_posts_postowner')

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'facebook_applications.application': {
            'Meta': {'ordering': "['name']", 'object_name': 'Application'},
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'namespace': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'facebook_posts.post': {
            'Meta': {'ordering': "['-created_time']", 'object_name': 'Post'},
            'actions': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'null': 'True', 'to': "orm['facebook_applications.Application']"}),
            'author_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'facebook_posts'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'author_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'author_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'comments': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'likes_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'message_tags': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'object_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'owners_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'picture': ('django.db.models.fields.TextField', [], {}),
            'place': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'privacy': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'properties': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'status_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'story': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'story_tags': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {}),
            'with_tags': ('annoying.fields.JSONField', [], {'null': 'True'})
        },
        'facebook_posts.postowner': {
            'Meta': {'ordering': "('post',)", 'unique_together': "(('post', 'owner_content_type', 'owner_id'),)", 'object_name': 'PostOwner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'facebook_page_posts'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'owner_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owners'", 'to': "orm['facebook_posts.Post']"})
        }
    }

    complete_apps = ['facebook_posts']