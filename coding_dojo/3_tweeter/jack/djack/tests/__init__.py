import string
import random
import json

from django.contrib.auth import get_user_model

from ..models import Tweet, Comment


User = get_user_model()


class TestHelper(object):
    entire_tweet_list_url = '/jack/'
    tweet_create_url = '/jack/create/'
    like_url_fmt = '/jack/like/%d'
    like_list_url_fmt = '/jack/likers/%d'
    detail_url_fmt = '/jack/%d'
    comment_url_fmt = '/jack/%d/comment/new'
    comment_list_url_fmt = '/jack/%d/comment'
    bye_url = '/jack/bye/'
    follow_url_fmt = '/jack/follow/%d'
    unfollow_url_fmt = '/jack/unfollow/%d'
    block_url_fmt = '/jack/block/%d'
    unblock_url_fmt = '/jack/unblock/%d'
    following_list_url_fmt = '/jack/following/%d'
    follower_list_url_fmt = '/jack/follower/%d'
    block_list_url = '/jack/blocked/'
    timeline_url_fmt = '/jack/timeline/%d'

    def _make_tweet(self, user, text='default text'):
        return Tweet.objects.create(writer=user, text=text)

    def _make_comment(self, parent_tweet, user, text='default text'):
        return Comment.objects.create(writer=user, tweet=parent_tweet, text=text)

    def _get_timeline(self, user):
        resp = self.client.get(self.timeline_url_fmt % user.id)
        return json.loads(resp.content)

    def _assert_tweet_equal(self, tweet_dict, tweet):
        self.assertEqual(tweet_dict['id'], tweet.id)
        self.assertEqual(tweet_dict['writer_id'], tweet.writer.id)
        self.assertEqual(tweet_dict['text'], tweet.text)

    def _assert_tweets_equal(self, tweet_dicts, tweets):
        self.assertEqual(len(tweet_dicts), len(tweets))
        for tweet_dict, tweet in zip(tweet_dicts, tweets):
            self._assert_tweet_equal(tweet_dict, tweet)

    @staticmethod
    def create_user(username=None):
        '''
        create user
        
        return: credential dictionary for use in self.client.login

        >>> self.create_user('tester')
        {'username': 'tester', 'password': '....'}
        '''
        if not username:
            username = ''.join(random.sample(string.ascii_lowercase, 10))
        password = ''.join(random.sample(string.ascii_lowercase, 10))
        user = User.objects.create_user(username=username, password=password)
        user.credential = {'username': username, 'password': password}
        return user

def refresh(model_instance):
    cls = type(model_instance)
    return cls.objects.get(pk=model_instance.pk)


