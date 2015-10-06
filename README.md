Django Facebook Graph API Posts
===============================

[![PyPI version](https://badge.fury.io/py/django-facebook-posts.png)](http://badge.fury.io/py/django-facebook-posts) [![Build Status](https://travis-ci.org/ramusus/django-facebook-posts.png?branch=master)](https://travis-ci.org/ramusus/django-facebook-posts) [![Coverage Status](https://coveralls.io/repos/ramusus/django-facebook-posts/badge.png?branch=master)](https://coveralls.io/r/ramusus/django-facebook-posts)

Application for interacting with Facebook Graph API Posts objects using Django model interface

Installation
------------

    pip install django-facebook-posts

Add into `settings.py` lines:

    INSTALLED_APPS = (
        ...
        'oauth_tokens',
        'facebook_api',
        'facebook_applications',
        'facebook_pages',
        'facebook_users',
        'facebook_posts',
    )

    # oauth-tokens settings
    OAUTH_TOKENS_HISTORY = True                                        # to keep in DB expired access tokens
    OAUTH_TOKENS_FACEBOOK_CLIENT_ID = ''                               # application ID
    OAUTH_TOKENS_FACEBOOK_CLIENT_SECRET = ''                           # application secret key
    OAUTH_TOKENS_FACEBOOK_SCOPE = ['offline_access']                   # application scopes
    OAUTH_TOKENS_FACEBOOK_USERNAME = ''                                # user login
    OAUTH_TOKENS_FACEBOOK_PASSWORD = ''                                # user password

Usage examples
--------------

### Fetch post by Graph ID

    >>> from facebook_posts.models import Post
    >>> post = Post.remote.fetch('19292868552_10150189643478553')
    >>> post
    <Post: Facebook Developers: >
    >>> post.__dict__
    {'_application_cache': <Application: NetworkedBlogs>,
     '_author_cache': <Page: Facebook Developers>,
     '_author_content_type_cache': <ContentType: Facebook page>,
     '_external_links_post_save': [],
     '_external_links_to_add': [],
     '_foreignkeys_post_save': [],
     '_state': <django.db.models.base.ModelState at 0xbd7e7ec>,
     'actions': [{'link': 'http://www.facebook.com/19292868552/posts/10150189643478553',
       'name': 'Comment'},
      {'link': 'http://www.facebook.com/19292868552/posts/10150189643478553',
       'name': 'Like'},
      {'link': 'http://networkedblogs.com/hGWk3?a=share', 'name': 'Share'}],
     'application_id': 18,
     'author_content_type_id': 82,
     'author_id': 9,
     'author_json': {'category': 'Product/service',
      'id': '19292868552',
      'name': 'Facebook Developers'},
     'caption': '',
     'comments_count': 753,
     'comments_json': {'count': 753,
      'data': [{'created_time': '2012-12-30T17:07:19+0000',
        'from': {'id': '100004288712236', 'name': 'Jian Liu'},
        'id': '19292868552_10150189643478553_24586753',
        'likes': 1,
        'message': 'dsa'}, ...]},
     'comments_real_count': 594,
     'created_time': datetime.datetime(2011, 5, 10, 18, 35, 38, tzinfo=tzutc()),
     'description': u'\nWe continue to make Platform more secure for users. Earlier this year, we introduced the ability for users to browse Facebook over HTTPS. As a result, we provided \u201cSecure Canvas URL\u201d and \u201cSecure Tab URL\u201d fields in the Developer App for developers to serve their apps through an H',
     'expanded_height': None,
     'expanded_width': None,
     'graph_id': '19292868552_10150189643478553',
     'icon': 'http://m.ak.fbcdn.net/photos-b.ak/photos-ak-snc7/v85006/169/9953271133/app_2_9953271133_841622721.gif',
     'id': 4364,
     'likes_count': 8270,
     'likes_json': {'count': 8270,
      'data': [{'id': '100000499350811', 'name': u'Nguy\u1ec5n V\u0103n Linh'},
       {'id': '670265477', 'name': 'Soonsang Hong'},
       {'id': '100005341900488', 'name': 'Aloha Sanjay'},
       {'id': '527488241', 'name': 'Princess Grace Dimaculangan'}]},
     'likes_real_count': 0,
     'link': 'http://developers.facebook.com/blog/post/497',
     'message': '',
     'message_tags': None,
     'name': 'Developer Roadmap Update: Moving to OAuth 2.0 + HTTPS',
     'object_id': None,
     'owners_json': None,
     'picture': 'http://m.ak.fbcdn.net/platform.ak/www/app_full_proxy.php?app=9953271133&v=3&size=z&cksum=e15ac22d55f6a9501d3b3ac64c5fb763&src=http%3A%2F%2Fimg.bitpixels.com%2Fgetthumbnail%3Fcode%3D78793%26size%3D120%26url%3Dhttp%3A%2F%2Fdevelopers.facebook.com%2Fblog%2F',
     'place': None,
     'privacy': {'value': ''},
     'properties': [{'href': 'http://apps.facebook.com/blognetworks/blog/official_facebook_developer_blog',
       'name': 'source',
       'text': 'Official Facebook Developer Blog'},
      {'href': 'http://developers.facebook.com/blog/post/497',
       'name': 'link',
       'text': 'Full Article...'}],
     'source': '',
     'status_type': 'app_created_story',
     'story': '',
     'story_tags': None,
     'type': 'link',
     'updated_time': datetime.datetime(2013, 3, 15, 1, 24, 46, tzinfo=tzutc()),
     'with_tags': None}

### Fetch post comments

    >>> from facebook_posts.models import Post
    >>> post = Post.remote.fetch('19292868552_10150189643478553')
    >>> post.fetch_comments()
    [<Comment: Comment object>, <Comment: Comment object>, <Comment: Comment object>, '...(remaining elements truncated)...']
    >>> post.comments.count()
    82
    >>> post.comments.all()[0].__dict__
    Out[53]:
    {'_external_links_post_save': [],
     '_external_links_to_add': [],
     '_foreignkeys_post_save': [],
     '_state': <django.db.models.base.ModelState at 0xbfc51cc>,
     'author_content_type_id': 87,
     'author_id': 6447,
     'author_json': {u'id': u'767515690', u'name': u'Tim McKnight'},
     'can_remove': False,
     'created_time': datetime.datetime(2013, 3, 15, 5, 24, 46),
     'graph_id': u'19292868552_10150189643478553_25321001',
     'id': 3605,
     'likes_count': 0,
     'likes_real_count': 0,
     'message': u'test',
     'post_id': 4364,
     'user_likes': False}

Fetch all comments of post

    >>> post.fetch_comments(all=True)
    [<Comment: Comment object>, <Comment: Comment object>, <Comment: Comment object>, '...(remaining elements truncated)...']
    >>> page.wall_comments.count()
    610

### Fetch post likes

    >>> from facebook_posts.models import Post
    >>> post = Post.remote.fetch('19292868552_10150189643478553')
    >>> post.likes_count # field with likes ammount transfered via API
    8270
    >>> post.likes_real_count # field with ammount of real likes connections
    0
    >>> post.fetch_likes()
    [<User: Cosmos Pham>, <User: Ismail Yanık>, '...(remaining elements truncated)...']
    >>> post.like_users.count()
    4316
    >>> post.likes_real_count # strange, but real ammount of likes often less than value of likes_count field
    4316

### Fetch comment likes

    >>> from facebook_posts.models import Post, Comment
    >>> post = Post.remote.fetch('19292868552_10150189643478553')
    >>> comment = Comment.remote.fetch('19292868552_10150189643478553_16210808')
    >>> comment.likes_count # field with likes ammount transfered via API
    480
    >>> comment.likes_real_count # field with ammount of real likes connections
    0
    >>> comment.fetch_likes()
    [<User: Blondi Gjini>, <User: Kerem Aydoğan>, '...(remaining elements truncated)...']
    >>> comment.like_users.count()
    480
    >>> comment.likes_real_count
    480

Licensing
---------

This library uses the [Apache License, version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).
Please see the library's individual files for more information.
