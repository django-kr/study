# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib import admin

class JackUser(AbstractUser):
    following = models.ManyToManyField('JackUser', related_name='follower')
    stalkers = models.ManyToManyField('JackUser', related_name='victim')

User = JackUser

# Create your models here.
class Post(models.Model):
    writer = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    like = models.IntegerField(default=0)
    likers = None
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Tweet(Post):
    likers = models.ManyToManyField(User, null=True, blank=True, related_name='my_likes')


class Comment(Post):
    likers = models.ManyToManyField(User, related_name='my_comments')
    tweet = models.ForeignKey(Tweet)

admin.site.register(Tweet)
