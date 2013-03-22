# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comment'
        db.create_table('facebook_posts_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('graph_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['facebook_posts.Post'])),
            ('author_json', self.gf('annoying.fields.JSONField')(null=True)),
            ('author_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='facebook_comments', null=True, to=orm['contenttypes.ContentType'])),
            ('author_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('likes_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('can_remove', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_likes', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('facebook_posts', ['Comment'])

        # Deleting field 'Post.likes'
        db.delete_column('facebook_posts_post', 'likes')

        # Deleting field 'Post.comments'
        db.delete_column('facebook_posts_post', 'comments')

        # Adding field 'Post.likes_json'
        db.add_column('facebook_posts_post', 'likes_json',
                      self.gf('annoying.fields.JSONField')(null=True),
                      keep_default=False)

        # Adding field 'Post.comments_json'
        db.add_column('facebook_posts_post', 'comments_json',
                      self.gf('annoying.fields.JSONField')(null=True),
                      keep_default=False)

        # Adding field 'Post.likes_real_count'
        db.add_column('facebook_posts_post', 'likes_real_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Post.comments_real_count'
        db.add_column('facebook_posts_post', 'comments_real_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding M2M table for field likes on 'Post'
        db.create_table('facebook_posts_post_likes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['facebook_posts.post'], null=False)),
            ('user', models.ForeignKey(orm['facebook_users.user'], null=False))
        ))
        db.create_unique('facebook_posts_post_likes', ['post_id', 'user_id'])

    def backwards(self, orm):
        # Deleting model 'Comment'
        db.delete_table('facebook_posts_comment')

        # Adding field 'Post.likes'
        db.add_column('facebook_posts_post', 'likes',
                      self.gf('annoying.fields.JSONField')(null=True),
                      keep_default=False)

        # Adding field 'Post.comments'
        db.add_column('facebook_posts_post', 'comments',
                      self.gf('annoying.fields.JSONField')(null=True),
                      keep_default=False)

        # Deleting field 'Post.likes_json'
        db.delete_column('facebook_posts_post', 'likes_json')

        # Deleting field 'Post.comments_json'
        db.delete_column('facebook_posts_post', 'comments_json')

        # Deleting field 'Post.likes_real_count'
        db.delete_column('facebook_posts_post', 'likes_real_count')

        # Deleting field 'Post.comments_real_count'
        db.delete_column('facebook_posts_post', 'comments_real_count')

        # Removing M2M table for field likes on 'Post'
        db.delete_table('facebook_posts_post_likes')

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
        'facebook_posts.comment': {
            'Meta': {'ordering': "['-created_time']", 'object_name': 'Comment'},
            'author_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'facebook_comments'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'author_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'author_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'can_remove': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {}),
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['facebook_posts.Post']"}),
            'user_likes': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'facebook_posts.post': {
            'Meta': {'ordering': "['-created_time']", 'object_name': 'Post'},
            'actions': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'null': 'True', 'to': "orm['facebook_applications.Application']"}),
            'author_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'facebook_posts'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'author_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'author_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comments_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'comments_real_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['facebook_users.User']", 'symmetrical': 'False'}),
            'likes_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'likes_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'likes_real_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
        },
        'facebook_users.user': {
            'Meta': {'ordering': "['name']", 'object_name': 'User'},
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['facebook_posts']