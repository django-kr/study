# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('djack',
    url(r'^create/$', 'views.create'),
    url(r'^$', 'views.list_tweets'),
)
