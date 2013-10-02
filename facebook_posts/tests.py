# -*- coding: utf-8 -*-
from django.test import TestCase
from facebook_pages.factories import PageFactory
from facebook_applications.models import Application
from facebook_users.models import User
from models import Post, PostOwner, Comment, Page
from datetime import datetime, timedelta

PAGE_ID = '19292868552'
POST1_ID = '19292868552_10150189643478553'
POST2_ID = '40796308305_10151982794203306'
COMMENT1_ID = '19292868552_10150189643478553_16210808'

class FacebookPostsTest(TestCase):

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
        self.assertEqual(post.status_type, 'app_created_story')
        self.assertEqual(post.created_time, datetime(2011,5,10,22,35,38))
        self.assertTrue('We continue to make Platform more secure for users' in post.description)
        self.assertTrue(len(post.icon) > 0)
        self.assertTrue(len(post.picture) > 20)

    def test_fetch_post_application(self):

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

    def test_fetch_post_authors_owners(self):

        # post on the page by page
        Post.remote.fetch(POST1_ID)
        post = Post.objects.all()[0]
        page = Page.objects.all()[0]

        author = {
            "name": "Facebook Developers",
            "category": "Product/service",
            "id": "19292868552"
        }

        self.assertEqual(page.graph_id, author['id'])
        self.assertEqual(page.name, author['name'])
        self.assertEqual(page.category, author['category'])

        self.assertEqual(post.author_json, author)
        self.assertEqual(post.author, page)

        # post on the page by user
        Post.remote.fetch(POST2_ID)
        post = Post.objects.all()[0]
        user = User.objects.all()[0]
        postowner = PostOwner.objects.all()[0]

        author = {
            "name": "Calum Gaterr",
            "id": "100001882194092"
        }
        owners = [{
            "name": "Coca-Cola",
            "category": "Food/beverages",
            "id": "40796308305"
        }]

        self.assertEqual(post.author, user)
        self.assertEqual(post.owners.all()[0], postowner)
        # self.assertEqual(post.owners_json, owners) # TODO: fix saving json as string
        self.assertDictEqual(post.author_json, author)

        self.assertEqual(user.graph_id, author['id'])
        self.assertEqual(user.name, author['name'])

        self.assertEqual(postowner.owner.name, owners[0]['name'])
        self.assertEqual(postowner.owner.graph_id, owners[0]['id'])
        self.assertEqual(postowner.owner.category, owners[0]['category'])

    def test_fetch_post_comments(self):

        Post.remote.fetch(POST1_ID)
        post = Post.objects.all()[0]

        self.assertEqual(Comment.objects.count(), 0)
        comments = post.fetch_comments(limit=100)
        self.assertTrue(Comment.objects.count() == comments.count() == 100)

        comments = post.fetch_comments(all=True)
        self.assertTrue(Comment.objects.count() > 100)
        self.assertTrue(Comment.objects.count() == comments.count() == post.comments_real_count)

        comment = comments.get(graph_id=COMMENT1_ID)
        user = User.objects.get(graph_id='100001650376589')

        self.assertEqual(user.name, 'Whdtabbasiwahd Abbas')

        self.assertEqual(comment.post, post)
        self.assertEqual(comment.author, user)
        self.assertEqual(comment.message, 'ok')
        self.assertEqual(comment.can_remove, False)
        self.assertEqual(comment.user_likes, False)
        self.assertEqual(comment.created_time, datetime(2011,5,10,22,36,29))
        self.assertTrue(comment.likes_count > 400)

#        self.assertEqual(post.comments.count(), post.comments_count) # TODO: fix strange ammount of real comments
#        self.assertEqual(post.comments_real_count, post.comments_count)

    def test_fetch_post_likes(self):

        Post.remote.fetch(POST1_ID)
        post = Post.objects.all()[0]

        self.assertEqual(post.like_users.count(), 0)
        post.fetch_likes()
        self.assertEqual(post.likes_real_count, User.objects.count())
#        self.assertEqual(post.like_users.count(), post.likes_count) # TODO: fix strange ammount of real likes
#        self.assertEqual(post.likes_real_count, post.likes_count)

    def test_fetch_comment_likes(self):

        post = Post.remote.fetch(POST1_ID)
        comment = Comment.remote.fetch(COMMENT1_ID, extra_fields={'post_id': post.id})

        self.assertEqual(comment.like_users.count(), 0)
        comment.fetch_likes()
        self.assertEqual(comment.likes_real_count, User.objects.count())
#        self.assertEqual(comment.like_users.count(), comment.likes_count) # TODO: fix strange ammount of real likes
#        self.assertEqual(comment.likes_real_count, comment.likes_count)

    def test_fetch_posts_of_page(self):

        page = PageFactory.create(graph_id=PAGE_ID)

        self.assertEqual(Post.objects.count(), 0)

        posts = page.fetch_posts(limit=100)
        posts_count = Post.objects.count()

        self.assertEqual(posts_count, 100)
        self.assertEqual(posts_count, len(posts))

        Post.objects.all().delete()
        posts = page.fetch_posts(since=datetime.now() - timedelta(10))
        posts_count1 = Post.objects.count()

        self.assertTrue(posts_count1 < posts_count)
        self.assertEqual(posts_count1, len(posts))