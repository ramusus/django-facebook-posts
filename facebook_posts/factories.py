from facebook_users.factories import UserFactory
#from facebook_pages.factories import PageFactory
from models import Post, Comment, PostOwner
from datetime import datetime
import factory
import random

class PostOwnerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PostOwner

class PostFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Post

    created_time = datetime.now()

#    owners = factory.SubFactory(UserFactory)
    author = factory.SubFactory(UserFactory)
    graph_id = factory.LazyAttributeSequence(lambda o, n: '%s_%s' % (n, n))

class CommentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Comment

    created_time = datetime.now()

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    graph_id = factory.LazyAttributeSequence(lambda o, n: '%s_%s' % (o.post.graph_id, n))
