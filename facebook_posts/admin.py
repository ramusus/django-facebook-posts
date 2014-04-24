# -*- coding: utf-8 -*-
from django.contrib import admin
from facebook_api.admin import FacebookModelAdmin
from models import Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('created_time','author','message','likes_count','like_users')
    readonly_fields = fields
    extra = False
    can_delete = False

class PostAdmin(FacebookModelAdmin):
    list_display = ('author','message','story','created_time','application','status_type','type','likes_count','comments_count')
    list_display_links = ('message','story',)
    list_filter = ('type','application',)
    search_fields = ('message','story','name','caption','description')
    inlines = [CommentInline]

    def get_readonly_fields(self, *args, **kwargs):
        fields = super(PostAdmin, self).get_readonly_fields(*args, **kwargs)
        return fields + ['like_users']

class CommentAdmin(FacebookModelAdmin):
    list_display = ('author','created_time','message','likes_count')
    list_display_links = ('message',)
    search_fields = ('message',)

    def get_readonly_fields(self, *args, **kwargs):
        fields = super(CommentAdmin, self).get_readonly_fields(*args, **kwargs)
        return fields + ['like_users']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)