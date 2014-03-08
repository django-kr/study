'''
o follow(to_user)
o unfollow(to_user)
. block(stalker)
. unblock(stalker)

. follow-list(self)
. follower-list(self)
. block-list(self)
'''

import json
import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase

from . import TestHelper


User = get_user_model()


class FollowTest(TestCase, TestHelper):
    def test_follow(self):
        user1 = self.create_user('user1')
        user2 = self.create_user('user2')
        self.client.login(**user1.credential)
        resp = self.client.post(self.follow_url_fmt % user2.id)
        
        self.assertEqual(list(user1.following.values_list('id', flat=True)), [user2.id])
        self.assertEqual(list(user2.follower.values_list('id', flat=True)), [user1.id])

    def test_unfollow(self):
        user1 = self.create_user('user1')
        user2 = self.create_user('user2')
        user3 = self.create_user('user3')
        user1.following.add(user2)
        user1.following.add(user3)

        self.client.login(**user1.credential)
        resp = self.client.post(self.unfollow_url_fmt % user2.id)
        
        self.assertEqual(list(user1.following.values_list('id', flat=True)), [user3.id])
        self.assertEqual(list(user2.follower.values_list('id', flat=True)), [])
        self.assertEqual(list(user3.follower.values_list('id', flat=True)), [user1.id])
        
    def test_block_stranger(self):
        user1 = self.create_user('user1')
        user2 = self.create_user('user2')

        self.client.login(**user1.credential)
        resp = self.client.post(self.block_url_fmt % user2.id)

        self.assertIn(user2, user1.stalkers.all())
    
    def test_block_follower(self):
        user1 = self.create_user('user1')
        user2 = self.create_user('user2')
        user1.following.add(user2)
        user2.following.add(user1)

        self.client.login(**user1.credential)
        resp = self.client.post(self.block_url_fmt % user2.id)
        self.assertNotIn(user1, user2.following.all())
        self.assertNotIn(user2, user1.following.all())
    
    def test_blocked_user_cannot_follow(self):
        user1 = self.create_user('user1')
        user2 = self.create_user('user2')
        user2.stalkers.add(user1)

        self.client.login(**user1.credential)
        resp = self.client.post(self.follow_url_fmt % user2.id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content)['result'], 'Blocked')

        self.assertNotIn(user2, user1.following.all())

    def test_blocker_cannot_follow_to_blocked_user(self):
        pass
