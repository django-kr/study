# -*- coding: utf-8 -*-
import datetime
import hashlib
import uuid

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib import admin
from django.utils.timezone import now
from django.conf import settings


class JackUser(AbstractUser):
    following = models.ManyToManyField('JackUser', related_name='follower')
    stalkers = models.ManyToManyField('JackUser', related_name='victim')

User = JackUser

class SignupVerification(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=40,
            default=lambda: hashlib.sha1(str(uuid.uuid4())).hexdigest())
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return now() < self.created_at + settings.ACTIVATION_EXPIRE

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
