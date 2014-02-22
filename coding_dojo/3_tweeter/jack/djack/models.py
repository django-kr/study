# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, AbstractUser

# TODO: need to be implemented base on AbstractUser
# set AUTH_USER_MODEL value to JackUser after that change
JackUser = User

# Create your models here.
class Post(models.Model):
    writer = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    like = models.IntegerField(default=0)
    likers = None

    class Meta:
        abstract = True


class Tweet(Post):
    likers = models.ManyToManyField(User, related_name='my_likes')


class Comment(Post):
    likers = models.ManyToManyField(User, related_name='my_comments')
    tweet = models.ForeignKey(Tweet)

