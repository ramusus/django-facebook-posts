from datetime import datetime
import random

from facebook_users.factories import UserFactory
import factory

import models


class PostOwnerFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.PostOwner


class PostFactory(factory.DjangoModelFactory):

    created_time = datetime.now()

#    owners = factory.SubFactory(UserFactory)
    author = factory.SubFactory(UserFactory)
    graph_id = factory.LazyAttributeSequence(lambda o, n: '%s_%s' % (n, n))

    class Meta:
        model = models.Post
