'''
follow(from_user, to_user)
unfollow(from_user, to_user)
block(from_user, to_user)

follow-list(self)
follower-list(self)
block-list(self)
'''

import json
import unittest

from django.test import TestCase

from . import TestHelper

class FollowTest(TestCase, TestHelper):
    @unittest.skip('Not yet implemented')
    def test_follow(self):
        user1 = self.create_user('user1')
        user2 = self.create_user('user2')
        self.client.login(**user1.credential)
        resp = self.client.post('/jack/follow/%d' % user2.id)
        self.assertEqual(resp.status_code, 200)
        
        self.assertTrue(list(user1.following.values_list('id', flat=True)), [user2.id])
        self.assertTrue(list(user2.follower.values_list('id', flat=True)), [user1.id])
        #! follow user1 -> user2 (API)
        #self.assertEqual(...) # model
        pass
