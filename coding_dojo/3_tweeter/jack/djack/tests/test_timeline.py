# coding: utf-8
'''
o following users post list
. following users like post list
'''
import json

from django.test import TestCase

from . import TestHelper

class TimeLineTest(TestCase, TestHelper):
    def test_following_users_post_list(self):
        follower = self.create_user('user1')
        following = self.create_user('user2')
        unfollowing = self.create_user('user3')
        
        follower.following.add(following)
        
        tweet = self._make_tweet(following)
        self._make_tweet(unfollowing)
        
        result_data = self._get_timeline(follower)
        # [ {'id': tweet.id, 'writer_id': following.id, 'text': tweet.text} ]
        self._assert_tweets_equal(result_data, [tweet])

    def test_timeline_should_contains_my_own_posts(self):
        me = self.create_user('user1')
        tweet = self._make_tweet(me)

        self.client.login(**me.credential)
        result_data = self._get_timeline(me)

        self._assert_tweets_equal(result_data, [tweet])

    def test_timeline_should_contains_followings_liked_posts(self):
        #     
        #   u1->u2 u3 u4 u5
        # t         o  o
        #        L->    <-L
        u1 = self.create_user('u1')
        u2 = self.create_user('u2')
        u3 = self.create_user('u3')
        u4 = self.create_user('u4')
        u5 = self.create_user('u5')

        u1.following.add(u2)

        u3_tweet = self._make_tweet(u3)
        u3_tweet.likers.add(u2)

        u4_tweet = self._make_tweet(u4)
        u4_tweet.likers.add(u5)
        
        result_data = self._get_timeline(u1)
        self._assert_tweets_equal(result_data, [u3_tweet])

        u1.following.add(u5)
        result_data = self._get_timeline(u1)
        self._assert_tweets_equal(result_data, [u4_tweet, u3_tweet])

        result_data = self._get_timeline(u2)
        self._assert_tweets_equal(result_data, [u3_tweet])


    def test_timeline_should_contain_my_commented_tweet(self):
        # 1. 자신이 코멘트한 트윗
        #    u1 u2
        #  t     o
        #     c->

        u1 = self.create_user('u1')
        u2 = self.create_user('u2')
        u2_tweet = self._make_tweet(u2)
        result_data = self._get_timeline(u1)
        self.assertEqual(result_data, [])
        
        u1_comment = self._make_comment(u2_tweet, u1)
        result_data = self._get_timeline(u1)

        self._assert_tweets_equal(result_data, [u2_tweet])

    def test_timeline_should_contain_my_followings_commented_tweet(self):
        # 1. 팔로우한 사람이 코멘트한 트윗

        #    u1->u2  u3
        #  t          x

        u1 = self.create_user('u1')
        u2 = self.create_user('u2')
        u3 = self.create_user('u3')
        u1.following.add(u2)
        u3_tweet = self._make_tweet(u3)

        result_data = self._get_timeline(u1)
        self.assertEqual(len(result_data), 0)

        #    u1->u2  u3
        #  t      c-> o
        u2_comment = self._make_comment(u3_tweet, u2)
        result_data = self._get_timeline(u1)
        self._assert_tweets_equal(result_data, [u3_tweet])
