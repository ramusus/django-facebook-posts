from facebook_users.factories import UserFactory
from facebook_pages.factories import PageFactory
from models import Post, Comment, PostOwner
from datetime import datetime
import factory
import random

class PostOwnerFactory(factory.Factory):
    FACTORY_FOR = PostOwner

class PostFactory(factory.Factory):
    FACTORY_FOR = Post

    created_time = datetime.now()

#    owners = factory.SubFactory(UserFactory)
    author = factory.SubFactory(UserFactory)
    graph_id = factory.Sequence(lambda n: n)

class CommentFactory(factory.Factory):
    FACTORY_FOR = Comment

    created_time = datetime.now()

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    graph_id = factory.LazyAttributeSequence(lambda o, n: '%s_%s' % (o.post.graph_id, n))
