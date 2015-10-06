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
import logging

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from facebook_api import fields
from facebook_api.decorators import atomic, fetch_all
from facebook_api.mixins import AuthorableModelMixin, LikableModelMixin, ShareableModelMixin
from facebook_api.models import MASTER_DATABASE, FacebookGraphIDModel, FacebookGraphTimelineManager
from facebook_api.utils import UnknownResourceType, get_improperly_configured_field, get_or_create_from_small_resource
from facebook_applications.models import Application
from facebook_pages.models import Page
from facebook_users.models import User

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


class PostRemoteManager(FacebookGraphTimelineManager):

    timeline_cut_fieldname = 'created_time'

    def update_count_and_get_posts(self, instances, page, *args, **kwargs):
        page.posts_count = page.wall_posts.count()
        page.save()
        return instances

    @atomic
    @fetch_all(return_all=update_count_and_get_posts, paging_next_arg_name='until')
    def fetch_page(self, page, limit=250, offset=0, edge='posts', **kwargs):
        """
        Arguments:
         * until|since - timestamp or datetime
        """
        kwargs.update({
            'limit': int(limit),
            'offset': int(offset),
        })

        instances = self.get('%s/%s' % (page.graph_id, edge), **kwargs)

        ids = []
        log.debug('response objects count=%s, limit=%s, after=%s' % (len(instances), limit, kwargs.get('since')))
        page_ct = ContentType.objects.get_for_model(page)
        for instance in instances:
            instance = Post.remote.get_or_create_from_instance(instance)

            if instance.owners.using(MASTER_DATABASE).count() == 0:
                post_owner = PostOwner.objects.get_or_create(
                    post=instance, owner_content_type=page_ct, owner_id=page.pk)[0]
                instance.owners.add(post_owner)

            ids += [instance.pk]

        return Post.objects.filter(pk__in=ids), self.response


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
    link = models.URLField(max_length=1500, help_text='The link attached to this post')
    icon = models.URLField(max_length=500, help_text='A link to an icon representing the type of this post')

    name = models.TextField(help_text='The name of the link')
    type = models.CharField(max_length=10, db_index=True,
                            help_text='A string indicating the type for this post (including link, photo, video)')

    caption = models.TextField(help_text='The caption of the link (appears beneath the link name)')
    description = models.TextField(help_text='A description of the link (appears beneath the link caption)')
    story = models.TextField(help_text='Text of stories not intentionally generatd by users, such as those '
                                       'generated when two users become friends; you must have the "Include recent '
                                       'activity stories" migration enabled in your app to retrieve these stories')

    properties = fields.JSONField(null=True, help_text='A list of properties for an uploaded video, for example, '
                                                       'the length of the video')
    actions = fields.JSONField(null=True, help_text='A list of available actions on the post (including commenting, '
                                                    'liking, and an optional app-specified action)')
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
    story_tags = fields.JSONField(null=True,
                                  help_text='Objects (Users, Pages, etc) tagged in a non-intentional story; '
                                            'you must have the "Include recent activity stories" migration enabled '
                                            'in your app to retrieve these tags')
    # objects containing id and name fields, encapsulated in a data[] array
    with_tags = fields.JSONField(null=True, help_text='Objects (Users, Pages, etc) tagged as being with the publisher '
                                                      'of the post ("Who are you with?" on Facebook)')

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

    # like_users = ManyToManyHistoryField(User, related_name='like_posts')

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
        return self.graph_id

    @property
    def owner_slug(self):
        try:
            owner = self.owners.all()[0].owner
            return owner.username if getattr(owner, 'username', None) else owner.graph_id
        except (IndexError, KeyError, AttributeError):
            return ''

    @property
    def slug(self):
        return '%s/posts/%s' % (self.owner_slug, self.graph_id.split('_')[1])


class PostOwner(models.Model):
    """
    Connection model for keeping multiple owners of single post
    """
    post = models.ForeignKey(Post, related_name='owners')

    owner_content_type = models.ForeignKey(ContentType, null=True, related_name='facebook_page_posts')
    owner_id = models.PositiveIntegerField(null=True, db_index=True)
    owner = generic.GenericForeignKey('owner_content_type', 'owner_id')

    class Meta:
        unique_together = ('post', 'owner_content_type', 'owner_id')

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
