# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import re
import time

import dateutil.parser
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from facebook_api import fields
from facebook_api.decorators import fetch_all, atomic
from facebook_api.mixins import OwnerableModelMixin, AuthorableModelMixin, LikableModelMixin, ShareableModelMixin
from facebook_api.models import FacebookGraphIDModel, FacebookGraphManager, MASTER_DATABASE
from facebook_api.utils import graph, get_or_create_from_small_resource, UnknownResourceType, get_improperly_configured_field
from facebook_applications.models import Application
from facebook_pages.models import Page
from facebook_users.models import User
from m2m_history.fields import ManyToManyHistoryField


log = logging.getLogger('facebook_posts')

if 'facebook_comments' in settings.INSTALLED_APPS:
    from facebook_comments.models import Comment
    from facebook_comments.mixins import CommentableModelMixin
    wall_comments = generic.GenericRelation(
        Comment, content_type_field='owner_content_type', object_id_field='owner_id', verbose_name=u'Comments')
else:
    wall_comments = get_improperly_configured_field('facebook_comments', True)

    class CommentableModelMixin(models.Model):
        comments_count = None
        fetch_comments = get_improperly_configured_field('facebook_comments')


class PostRemoteManager(FacebookGraphManager):

    def update_count_and_get_posts(self, instances, page, *args, **kwargs):
        page.posts_count = page.wall_posts.count()
        page.save()
        return instances

    @atomic
    @fetch_all(return_all=update_count_and_get_posts, always_all=True, paging_next_arg_name='until')
    def fetch_page(self, page, limit=250, offset=0, until=None, since=None, edge='posts', **kwargs):
        '''
        Arguments:
         * until|since - timestamp or datetime
        '''
        kwargs.update({
            'limit': int(limit),
            'offset': int(offset),
        })
        for field in ['until', 'since']:
            value = locals()[field]
            if isinstance(value, datetime):
                kwargs[field] = int(time.mktime(value.timetuple()))
            elif value is not None:
                try:
                    kwargs[field] = int(value)
                except TypeError:
                    raise ValueError('Wrong type of argument %s: %s' % (field, type(value)))

        response = graph('%s/%s' % (page.graph_id, edge), **kwargs)
        ids = []
        if response:
            log.debug('response objects count - %s' % len(response.data))

            page_ct = ContentType.objects.get_for_model(page)
            if response:
                log.debug('response objects count=%s, limit=%s, after=%s' %
                          (len(response.data), limit, kwargs.get('after')))
                for resource in response.data:
                    instance = Post.remote.get_or_create_from_resource(resource)

                    if instance.owners.using(MASTER_DATABASE).count() == 0:
                        post_owner = PostOwner.objects.get_or_create(
                            post=instance, owner_content_type=page_ct, owner_id=page.pk)[0]
                        instance.owners.add(post_owner)

                    ids += [instance.pk]

        return Post.objects.filter(pk__in=ids), response


class Post(AuthorableModelMixin, LikableModelMixin, CommentableModelMixin, ShareableModelMixin, FacebookGraphIDModel):

    # Contains in data an array of objects, each with the name and Facebook id of the user
    owners_json = fields.JSONField(null=True, help_text='Profiles mentioned or targeted in this post')

    application = models.ForeignKey(
        Application, null=True, help_text='Application this post came from', related_name='posts')

    message = models.TextField(help_text='The message')

    object_id = models.BigIntegerField(null=True, help_text='The Facebook object id for an uploaded photo or video')

    created_time = models.DateTimeField(help_text='The time the post was initially published', db_index=True)
    updated_time = models.DateTimeField(null=True, help_text='The time of the last comment on this post')

    picture = models.TextField(help_text='If available, a link to the picture included with this post')
    source = models.TextField(help_text='A URL to a Flash movie or video file to be embedded within the post')
    link = models.URLField(max_length=1000, help_text='The link attached to this post')
    icon = models.URLField(max_length=500, help_text='A link to an icon representing the type of this post')

    name = models.TextField(help_text='The name of the link')
    type = models.CharField(
        max_length=100, help_text='A string indicating the type for this post (including link, photo, video)')

    caption = models.TextField(help_text='The caption of the link (appears beneath the link name)')
    description = models.TextField(help_text='A description of the link (appears beneath the link caption)')
    story = models.TextField(
        help_text='Text of stories not intentionally generatd by users, such as those generated when two users become friends; you must have the "Include recent activity stories" migration enabled in your app to retrieve these stories')

    properties = fields.JSONField(
        null=True, help_text='A list of properties for an uploaded video, for example, the length of the video')
    actions = fields.JSONField(
        null=True, help_text='A list of available actions on the post (including commenting, liking, and an optional app-specified action)')
    # object containing the value field and optional friends, networks, allow, deny and description fields.
    privacy = fields.JSONField(null=True, help_text='The privacy settings of the Post')
    # object containing id and name of Page associated with this location, and
    # a location field containing geographic information such as latitude,
    # longitude, country, and other fields (fields will vary based on
    # geography and availability of information)
    place = fields.JSONField(null=True, help_text='Location associated with a Post, if any')
    # object containing fields whose names are the indexes to where objects
    # are mentioned in the message field; each field in turn is an array
    # containing an object with id, name, offset, and length fields, where
    # length is the length, within the message field, of the object mentioned
    message_tags = fields.JSONField(null=True, help_text='Objects tagged in the message (Users, Pages, etc)')
    # object containing fields whose names are the indexes to where objects
    # are mentioned in the message field; each field in turn is an array
    # containing an object with id, name, offset, and length fields, where
    # length is the length, within the message field, of the object mentioned
    story_tags = fields.JSONField(
        null=True, help_text='Objects (Users, Pages, etc) tagged in a non-intentional story; you must have the "Include recent activity stories" migration enabled in your app to retrieve these tags')
    # objects containing id and name fields, encapsulated in a data[] array
    with_tags = fields.JSONField(
        null=True, help_text='Objects (Users, Pages, etc) tagged as being with the publisher of the post ("Who are you with?" on Facebook)')

    # Structure containing a data object and the count of total likes, with
    # data containing an array of objects, each with the name and Facebook id
    # of the user who liked the post
    likes_json = fields.JSONField(null=True, help_text='Likes for this post')
    # Structure containing a data object containing an array of objects, each
    # with the id, from, message, and created_time for each comment
    comments_json = fields.JSONField(null=True, help_text='Comments for this post')
    # Just only get count here, maybe the detail only for manager?
    shares_json = fields.JSONField(null=True, help_text='Shares for this post')

    # not in API
    status_type = models.CharField(max_length=100)
    expanded_height = models.IntegerField(null=True)
    expanded_width = models.IntegerField(null=True)

#    like_users = ManyToManyHistoryField(User, related_name='like_posts')

    comments = wall_comments

    objects = models.Manager()
    remote = PostRemoteManager()

    class Meta:
        verbose_name = 'Facebook post'
        verbose_name_plural = 'Facebook posts'

    def __unicode__(self):
        return '%s: %s' % (unicode(self.author), self.message or self.story)

    def parse(self, response):

        # shared_stories has `object_id` not int, but like 252974534827155_1073741878
        if 'object_id' in response and '_' in response['object_id']:
            del response['object_id']

        if 'from' in response:
            response['author_json'] = response.pop('from')
        if 'to' in response and len(response['to']['data']):
            response['owners_json'] = response.pop('to')['data']

        for field in ['likes', 'comments', 'shares']:
            if field in response:
                if 'count' in response[field]:
                    response['%s_count' % field] = response[field]['count']
                response['%s_json' % field] = response.pop(field)

        super(Post, self).parse(response)

        if self.author is None and self.author_json:
            self.author = get_or_create_from_small_resource(self.author_json)

        if self.owners.count() == 0 and self.owners_json:
            self._external_links_to_add['owners'] = []
            for owner_json in self.owners_json:
                try:
                    owner = get_or_create_from_small_resource(owner_json)
                except UnknownResourceType:
                    continue
                if owner:
                    self._external_links_to_add['owners'] += [PostOwner(post=self, owner=owner)]

    def save(self, *args, **kwargs):
        # set exactly Page or User contentTypes, not a child
        for field_name in ['author']:
            for allowed_model in [Page, User]:
                if isinstance(getattr(self, field_name), allowed_model):
                    setattr(self, '%s_content_type' % field_name, ContentType.objects.get_for_model(allowed_model))
                    break

        # check is generic fields has correct content_type
        if self.author_content_type:
            allowed_ct_ids = [ct.pk for ct in ContentType.objects.get_for_models(Page, User).values()]
            if self.author_content_type.pk not in allowed_ct_ids:
                raise ValueError("'author' field should be Page or User instance")

        return super(Post, self).save(*args, **kwargs)

    @property
    def slug(self):
        return self.username or self.graph_id

    @property
    def owner_slug(self):
        try:
            owner = self.owners.all()[0].owner
            return owner.username or owner.graph_id
        except IndexError:
            return''

    @property
    def slug(self):
        return '%s/posts/%s' % (self.owner_slug, self.graph_id.split('_')[1])


class PostOwner(models.Model):

    '''
    Connection model for keeping multiple owners of single post
    '''
    class Meta:
        unique_together = ('post', 'owner_content_type', 'owner_id')

    post = models.ForeignKey(Post, related_name='owners')

    owner_content_type = models.ForeignKey(ContentType, null=True, related_name='facebook_page_posts')
    owner_id = models.PositiveIntegerField(null=True, db_index=True)
    owner = generic.GenericForeignKey('owner_content_type', 'owner_id')

    def save(self, *args, **kwargs):
        # set exactly right Page or User contentTypes, not a child
        for field_name in ['owner']:
            for allowed_model in [Page, User]:
                if isinstance(getattr(self, field_name), allowed_model):
                    setattr(self, '%s_content_type' % field_name, ContentType.objects.get_for_model(allowed_model))
                    break

        # check if generic fields has correct content_type
        if self.owner_content_type:
            allowed_ct_ids = [ct.pk for ct in ContentType.objects.get_for_models(Page, User, Application).values()]
            if self.owner_content_type.pk not in allowed_ct_ids:
                raise ValueError("'owner' field should be Page or User instance, not %s" % type(self.owner))

        return super(PostOwner, self).save(*args, **kwargs)
