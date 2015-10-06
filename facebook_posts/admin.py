# -*- coding: utf-8 -*-
'''
Copyright 2011-2015 ramusus
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
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
