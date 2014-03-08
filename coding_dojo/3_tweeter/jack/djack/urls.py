# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('djack',
    url(r'^create/$', 'views.create'),
    url(r'^$', 'views.list_tweets'),
    url(r'^(?P<tweet_id>\d+)/?$', 'views.detail_tweet'),
    url(r'^like/(?P<tweet_id>\d+)/?', 'views.like_process'),
    url(r'^bye/', 'views.bye_user'),
    url(r'^likers/(?P<tweet_id>\d+)/?', 'views.likers'),
    url(r'^(?P<tweet_id>\d+)/comment/new/?', 'views.create_comment'),
    url(r'^(?P<tweet_id>\d+)/comment/?', 'views.comment_list'),
    url(r'^follow/(?P<user_id>\d+)/?', 'views.follow'),
    url(r'^unfollow/(?P<user_id>\d+)/?', 'views.unfollow'),
    url(r'^block/(?P<stalker_id>\d+)/?', 'views.block'),
)
