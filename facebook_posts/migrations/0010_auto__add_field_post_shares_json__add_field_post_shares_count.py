# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.shares_json'
        db.add_column('facebook_posts_post', 'shares_json',
                      self.gf('annoying.fields.JSONField')(null=True),
                      keep_default=False)

        # Adding field 'Post.shares_count'
        db.add_column('facebook_posts_post', 'shares_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Post.shares_json'
        db.delete_column('facebook_posts_post', 'shares_json')

        # Deleting field 'Post.shares_count'
        db.delete_column('facebook_posts_post', 'shares_count')


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
            'like_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'like_comments'", 'symmetrical': 'False', 'to': "orm['facebook_users.User']"}),
            'likes_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'likes_real_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'caption': ('django.db.models.fields.TextField', [], {}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comments_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'comments_real_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expanded_height': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'expanded_width': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'like_posts'", 'symmetrical': 'False', 'to': "orm['facebook_users.User']"}),
            'likes_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'likes_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'likes_real_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'message_tags': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'owners_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'picture': ('django.db.models.fields.TextField', [], {}),
            'place': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'privacy': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'properties': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'shares_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shares_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.TextField', [], {}),
            'status_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'story': ('django.db.models.fields.TextField', [], {}),
            'story_tags': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
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
            'Meta': {'ordering': "['graph_id']", 'object_name': 'User'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birthday': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'cover': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'currency': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'devices': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'education': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'favorite_athletes': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'favorite_teams': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'hometown': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installed': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'interested_in': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'languages': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'location': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'payment_pricepoints': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'political': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quotes': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'relationship_status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'security_settings': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'significant_other': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'third_party_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'timezone': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video_upload_limits': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'work': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'})
        }
    }

    complete_apps = ['facebook_posts']