'''
o follow(to_user)
o unfollow(to_user)
o block(stalker)
o unblock(stalker)

o follow-list(user)
. follower-list(user)
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
        user1 = self.create_user('user1')
        user2 = self.create_user('user2')
        user2.stalkers.add(user1)

        self.client.login(**user2.credential)
        resp = self.client.post(self.follow_url_fmt % user1.id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content)['result'], 'Blocked')

        self.assertNotIn(user1, user2.following.all())

    def test_unblock_blocked_user(self):
        stalker = self.create_user('user1')
        blocker = self.create_user('user2')
        self.client.login(**blocker.credential)
        resp = self.client.post(self.block_url_fmt % stalker.id)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(stalker, blocker.stalkers.all())
        resp = self.client.post(self.unblock_url_fmt % stalker.id)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(stalker, blocker.stalkers.all())

    def test_following_list(self):
        follower = self.create_user('user1')
        following1 = self.create_user('user2')
        following2 = self.create_user('user3')
        
        self.client.login(**follower.credential)
        resp = self.client.post(self.follow_url_fmt % following1.id)
        resp = self.client.post(self.follow_url_fmt % following2.id)
        
        resp = self.client.get(self.following_list_url_fmt % follower.id)
        self.assertEqual(resp.status_code, 200)

        result_data = json.loads(resp.content)
        # [ {'id': following1.id, ...}, {'id': following2.id, ... } ]
        result_ids = sorted(map(lambda x: x['id'], result_data))
        expect_ids = sorted([following1.id, following2.id])
        self.assertEqual(result_ids, expect_ids)

    def test_follower_list(self):
        following = self.create_user('user1')
        follower1 = self.create_user('user2')
        follower2 = self.create_user('user3')
        
        self.client.login(**follower1.credential)
        resp = self.client.post(self.follow_url_fmt % following.id)

        self.client.login(**follower2.credential)
        resp = self.client.post(self.follow_url_fmt % following.id)
        
        resp = self.client.get(self.follower_list_url_fmt % following.id)

        self.assertEqual(resp.status_code, 200)

        result_data = json.loads(resp.content)
        # [ {'id': following1.id, ...}, {'id': following2.id, ... } ]
        result_ids = sorted(map(lambda x: x['id'], result_data))
        expect_ids = sorted([follower1.id, follower2.id])
        self.assertEqual(result_ids, expect_ids)

    def test_block_list(self):
        blocker = self.create_user('user1')
        stalker1 = self.create_user('user2')
        stalker2 = self.create_user('user3')

        self.client.login(**blocker.credential)
        self.client.post(self.block_url_fmt % stalker1.id)
        self.client.post(self.block_url_fmt % stalker2.id)

        resp = self.client.get(self.block_list_url)

        result_data = json.loads(resp.content)
        # [ {'id': following1.id, ...}, {'id': following2.id, ... } ]
        result_ids = sorted(map(lambda x: x['id'], result_data))
        expect_ids = sorted([stalker1.id, stalker2.id])
        self.assertEqual(result_ids, expect_ids)




        


            



