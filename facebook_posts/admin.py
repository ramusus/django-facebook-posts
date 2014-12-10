# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from facebook_api.admin import FacebookModelAdmin

from .models import Post


class PostAdmin(FacebookModelAdmin):
    list_display = ('author', 'message', 'story', 'created_time', 'application',
                    'status_type', 'type', 'likes_count', 'comments_count')
    list_display_links = ('message', 'story',)
    list_filter = ('type', 'application',)
    search_fields = ('message', 'story', 'name', 'caption', 'description')

    def get_readonly_fields(self, *args, **kwargs):
        fields = super(PostAdmin, self).get_readonly_fields(*args, **kwargs)
        return fields + ['like_users']

admin.site.register(Post, PostAdmin)

if 'facebook_comments' in settings.INSTALLED_APPS:
    from facebook_comments.admin import CommentInline
    PostAdmin.inlines = [CommentInline]
