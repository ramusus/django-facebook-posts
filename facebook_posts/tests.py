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
from datetime import datetime, timedelta

from django.db.models import Min
from django.test import TestCase
from django.utils import timezone
from facebook_api.api import FacebookError
from facebook_applications.models import Application
from facebook_comments.factories import CommentFactory
from facebook_pages.factories import PageFactory
from facebook_users.models import User

from .factories import PostFactory
from .models import Post, PostOwner, Comment, Page

PAGE_ID = '19292868552'
POST1_ID = '19292868552_10150189643478553'
POST2_ID_OLD = '100001341687090_632170373504346'
POST2_ID_NEW = '816815785039803_632170373504346'
COMMENT1_ID = '19292868552_10150475844632302_20258978'

PAGE1_ID = '1411299469098495'
GROUP_CLOSED_ID = '167276666692692'

POST_WITH_MANY_LIKES_ID = '19292868552_10151516882688553'
POST_WITH_MANY_COMMENTS_ID = '19292868552_10150475844632302'
POST_WITH_MANY_NEW_COMMENTS_ID = '147863265269488_588392457883231'
COMMENT_NEW_ID = '147863265269488:588392457883231:10101338186056211_10106024381073883'


class FacebookPostsTest(TestCase):

    # def test_app_scoped_posts_graph_id(self):
    #
    #     post_old = PostFactory(graph_id=POST2_ID_OLD)
    #     post_new = Post.remote.fetch(POST2_ID_OLD)
    #
    #     self.assertEqual(post_new.graph_id, POST2_ID_NEW)
    #     self.assertEqual(post_old.graph_id, POST2_ID_NEW)
    #     self.assertEqual(Post.objects.count(), 1)

    def test_fetch_post(self):
        self.assertEqual(Post.objects.count(), 0)
        Post.remote.fetch(POST1_ID)
        Post.remote.fetch(POST1_ID)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.all()[0]

        self.assertEqual(post.graph_id, POST1_ID)
        self.assertEqual(post.link, u'http://developers.facebook.com/blog/post/497')
        self.assertEqual(post.name, u'Developer Roadmap Update: Moving to OAuth 2.0 + HTTPS')
        self.assertEqual(post.type, 'link')
        self.assertEqual(post.status_type, 'published_story')
        self.assertIsInstance(post.created_time, datetime)
        self.assertTrue('We continue to make Platform more secure for users' in post.description)
        self.assertGreater(len(post.icon), 0)
        self.assertGreater(len(post.picture), 20)

    def test_post_fetch_application(self):
        Post.remote.fetch(POST1_ID)
        post = Post.objects.all()[0]
        application = Application.objects.all()[0]

        application_json = {
            "name": "NetworkedBlogs",
            "namespace": "blognetworks",
            "id": "9953271133"
        }
        self.assertEqual(post.application, application)
        self.assertEqual(post.application.graph_id, application_json['id'])
        self.assertEqual(post.application.name, application_json['name'])
        self.assertEqual(post.application.namespace, application_json['namespace'])

    def test_post_fetch_authors_owners(self):
        # post on the page by page
        author = {
            "name": "Facebook Developers",
            "category": "Product/service",
            "id": "19292868552"
        }
        Post.remote.fetch(POST1_ID)
        post = Post.objects.get(graph_id=POST1_ID)
        page = Page.objects.get(graph_id=author['id'])

        self.assertEqual(page.graph_id, author['id'])
        self.assertEqual(page.name, author['name'])
        self.assertEqual(page.category, author['category'])

        self.assertEqual(post.author_json, author)
        self.assertEqual(post.author, page)

        # post on the page by user
        owners = [{
                      "id": "816815785039803",
                      "name": "Rainbow Gathering"
                  }]

        Post.remote.fetch(POST2_ID_NEW)
        post = Post.objects.get(graph_id=POST2_ID_NEW)

        # self.assertEqual(post.owners_json, owners) # TODO: fix saving json as string
        self.assertEqual(post.author.name, "Danny Reitzloff")
        self.assertEqual(post.author_json["name"], "Danny Reitzloff")

        postowner = PostOwner.objects.all()[0]
        self.assertEqual(post.owners.all()[0], postowner)
        self.assertEqual(postowner.owner.name, owners[0]['name'])
        self.assertEqual(postowner.owner.graph_id, owners[0]['id'])

    def test_post_fetch_comments(self):
        post = PostFactory(graph_id=POST_WITH_MANY_COMMENTS_ID)

        self.assertEqual(Comment.objects.count(), 0)

        comments = post.fetch_comments(limit=100)
        self.assertEqual(comments.count(), 100)
        self.assertEqual(comments.count(), Comment.objects.count())
        self.assertEqual(comments.count(), post.comments.count())

        comments = post.fetch_comments(all=True)
        self.assertGreater(post.comments_count, 1000)
        self.assertEqual(post.comments_count, Comment.objects.count())
        self.assertEqual(post.comments_count, comments.count())
        self.assertEqual(post.comments_count, post.comments.count())

        comment = comments.get(graph_id=COMMENT1_ID)
        self.assertEqual(comment.owner, post)
        self.assertEqual(comment.author.name, 'Jordan Alvarez')
        self.assertEqual(comment.message, 'PLAYDOM? bahhhhhhhhh ZYNGA RULES!')
        self.assertEqual(comment.can_remove, False)
        self.assertEqual(comment.user_likes, False)
        self.assertIsInstance(comment.created_time, datetime)
        self.assertGreater(comment.likes_count, 5)

    def test_post_fetch_comments_new_ids(self):
        post = PostFactory(graph_id=POST_WITH_MANY_NEW_COMMENTS_ID)

        self.assertEqual(Comment.objects.count(), 0)
        comments = post.fetch_comments(limit=100)
        comments.get(graph_id=COMMENT_NEW_ID)

    def test_post_fetch_comments_parse_author(self):
        post = PostFactory(graph_id='125405167513286_764679973585799')

        self.assertEqual(Comment.objects.count(), 0)
        comments = post.fetch_comments(all=True)

        self.assertGreater(comments.count(), 100)

    def test_post_fetch_likes(self):
        post = PostFactory(graph_id=POST_WITH_MANY_LIKES_ID)

        self.assertEqual(post.likes_users.count(), 0)
        self.assertEqual(User.objects.count(), 1)

        users = post.fetch_likes(all=True)
        self.assertGreater(users.count(), 1000)
        self.assertEqual(post.likes_count, users.count())
        self.assertEqual(post.likes_count, User.objects.count() - 1)
        self.assertEqual(post.likes_count, post.likes_users.count())

    def test_comment_fetch_likes(self):
        post = PostFactory(graph_id=POST1_ID)
        comment = CommentFactory(graph_id=COMMENT1_ID, owner=post)

        self.assertEqual(comment.likes_users.count(), 0)
        self.assertEqual(User.objects.count(), 2)

        users = comment.fetch_likes(all=True)
        self.assertGreater(users.count(), 7)
        self.assertEqual(comment.likes_count, users.count())
        self.assertEqual(comment.likes_count, User.objects.count() - 2)
        self.assertEqual(comment.likes_count, comment.likes_users.count())

    def test_post_fetch_shares(self):
        post = PostFactory(graph_id=POST_WITH_MANY_LIKES_ID)

        self.assertEqual(post.shares_users.count(), 0)
        self.assertEqual(User.objects.count(), 1)

        users = post.fetch_shares(all=True)
        self.assertGreaterEqual(users.count(), 40)
        self.assertEqual(post.shares_count, users.count())
        self.assertEqual(post.shares_count, User.objects.count() - 1)
        self.assertEqual(post.shares_count, post.shares_users.count())

        post = PostFactory(graph_id='1411299469098495_1534163126812128')
        users = post.fetch_shares(all=True)
        self.assertGreaterEqual(users.count(), 7)

        count = users.count()

        users = post.fetch_shares(all=True)
        self.assertEqual(users.count(), count)

    def test_post_fetch_shares_status_raise(self):
        post = PostFactory(graph_id='918051514883799')

        with self.assertRaises(FacebookError):
            post.fetch_shares(all=True)

        try:
            post.fetch_shares(all=True)
        except Exception, e:
            self.assertEqual(e.code, 12)

        post = PostFactory(graph_id='129107667156177_918051514883799')
        post.fetch_shares(all=True)

    # def test_page_fetch_posts_with_strange_object_id(self):
    #     instance = PageFactory(graph_id=252974534827155)
    #     posts = instance.fetch_posts(all=True, since=datetime(2014, 9, 1).replace(tzinfo=timezone.utc))
    #
    #     self.assertEqual(posts.filter(graph_id='252974534827155_323648421093099')[0].object_id, None)

    def test_page_fetch_posts(self):
        page = PageFactory(graph_id=PAGE_ID)

        self.assertEqual(Post.objects.count(), 0)

        posts = page.fetch_posts(limit=25)

        self.assertEqual(posts.count(), 25)
        self.assertEqual(posts.count(), Post.objects.count())

        earliest = posts.aggregate(Min('created_time'))['created_time__min'] - timedelta(30)
        posts = page.fetch_posts(all=True, since=earliest)

        self.assertGreater(posts.count(), 25)
        self.assertEqual(posts.count(), Post.objects.count())

        earliest1 = posts.aggregate(Min('created_time'))['created_time__min']
        self.assertTrue(earliest <= earliest1)

        # posts = page.fetch_posts(all=True, limit=95)
        # posts_count = Post.objects.count()
        #
        # self.assertGreaterEqual(posts.count(), 95)
        # self.assertEqual(posts.count(), posts_count)

        Post.objects.all().delete()
        posts = page.fetch_posts(all=True, since=timezone.now() - timedelta(10))

        self.assertEqual(posts.count(), Post.objects.count())
        self.assertLess(posts.count(), 25)

        # def test_group_closed_fetch_posts(self):
        # page = PageFactory(graph_id=GROUP_CLOSED_ID)
        #
        #     self.assertEqual(Post.objects.count(), 0)
        #
        #             posts = page.fetch_posts(all=True)
        #
        #     self.assertTrue(len(posts) > 0) # ensure user has access to closed group

    def test_page_fetch_many_posts(self):
        page = PageFactory(graph_id=PAGE1_ID)

        self.assertEqual(Post.objects.count(), 0)

        posts = page.fetch_posts(all=True, since=datetime(2014, 1, 1).replace(tzinfo=timezone.utc))

        self.assertGreater(posts.count(), 250)
        self.assertEqual(posts.count(), Post.objects.count())
        self.assertTrue(posts.filter(created_time__lte=datetime(2014, 1, 7).replace(tzinfo=timezone.utc)).count(), 1)
