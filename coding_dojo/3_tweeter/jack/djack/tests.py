# -*- coding: utf-8 -*-
import json
from unittest import skip

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Tweet

'''
개별사용자 기능
list
v post (140)
retweet
favorite
follow
'''

# Create your tests here.
class JackTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'password')
        self.client.login(username='test', password='password')

    def test_post_tweet(self):
        response = self.client.post('/jack/create/', {"text": "test tweet"})
        self.assertEqual(response.status_code, 200)
        tweets = Tweet.objects.all()
        self.assertEqual(list(tweets.values_list('text', 'writer__username')),
                         [(u"test tweet", u'test')])
        # self.assertEqual(list(tweets.values_list('writer__username', flat=True)),
                        #[u"test"])

    def test_post_length_limit(self):
        char_141 = 'c' * 141
        response = self.client.post('/jack/create/', {"text": char_141})
        self.assertEqual(response.status_code, 400)
        char_140 = 'c' * 140
        response = self.client.post('/jack/create/', {"text": char_140})
        self.assertEqual(response.status_code, 200)

    def test_list_empty(self):
        response = self.client.get('/jack/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_list_tweets(self):
        Tweet.objects.create(writer=self.user, text='test tweet 1')
        Tweet.objects.create(writer=self.user, text='test tweet 2')
        response = self.client.get('/jack/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [
            {u'writer': self.user.username, u'text': 'test tweet 1'},
            {u'writer': self.user.username, u'text': 'test tweet 2'},
        ])
