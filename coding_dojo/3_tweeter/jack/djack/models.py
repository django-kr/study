# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tweet(models.Model):
    writer = models.ForeignKey(User)
    text = models.CharField(max_length=140)