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
        
        resp = self.client.get(self.timeline_url_fmt % follower.id)
        
        result_data = json.loads(resp.content)
        # [ {'id': tweet.id, 'writer_id': following.id, 'text': tweet.text} ]
        self.assertEqual(len(result_data), 1)
        self._assert_tweet_equal(result_data[0], tweet)

    def test_timeline_should_contains_my_own_posts(self):
        me = self.create_user('user1')
        tweet = self._make_tweet(me)

        self.client.login(**me.credential)
        resp = self.client.get(self.timeline_url_fmt % me.id)
        result_data = json.loads(resp.content)

        self.assertEqual(len(result_data), 1)
        self._assert_tweet_equal(result_data[0], tweet)

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
        
        resp = self.client.get(self.timeline_url_fmt % u1.id)
        result_data = json.loads(resp.content)
        self.assertEqual(len(result_data), 1)
        self._assert_tweet_equal(result_data[0], u3_tweet)

        u1.following.add(u5)
        resp = self.client.get(self.timeline_url_fmt % u1.id)
        result_data = json.loads(resp.content)
        self.assertEqual(len(result_data), 2)

        resp = self.client.get(self.timeline_url_fmt % u2.id)
        result_data = json.loads(resp.content)
        self.assertEqual(len(result_data), 1)
        self._assert_tweet_equal(result_data[0], u3_tweet)


    def test_timeline_should_contain_me_and_my_followings_commented_tweet(self):
        # TODO
        # 1. 자신이 코멘트한 트윗
        # 1. 팔로우한 사람이 코멘트한 트윗
        # 1. 팔로우한 사람이 코멘트에 좋아요한 트윗 (X)
        pass

    def _assert_tweet_equal(self, tweet_dict, tweet):
        self.assertEqual(tweet_dict['id'], tweet.id)
        self.assertEqual(tweet_dict['writer_id'], tweet.writer.id)
        self.assertEqual(tweet_dict['text'], tweet.text)
