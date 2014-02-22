import json

from djack.models import JackUser as User
from django.test import TestCase

from ..models import Tweet, Comment
from . import TestHelper, refresh


class LikeTest(TestCase, TestHelper):
    def setUp(self):
        self.a_user = User.objects.create_user('test1', 'test1@test.com', 'password')
        self.other_user = User.objects.create_user('test2', 'test2@test.com', 'password')

    def test_detail_tweet__no_like_initially0(self):
        user1_tweet = self._make_tweet(self.a_user)
        response = self.client.get(self.detail_url_fmt % user1_tweet.id)
        tweet_dict = json.loads(response.content)
        self.assertEqual(tweet_dict['like'], 0)

    def test_like_count_increased_when_do_like(self):
        user1_tweet = self._make_tweet(self.a_user)
        response = self.client.post(self.like_url_fmt % user1_tweet.id)
        self.assertEqual(response.status_code, 401)
        self.client.login(username=self.a_user.username, password='password')
        response = self.client.post(self.like_url_fmt % user1_tweet.id)
        tweet = refresh(user1_tweet)
        self.assertEqual(tweet.like, 1)
        self.client.login(username=self.other_user.username, password='password')
        response = self.client.post(self.like_url_fmt % user1_tweet.id)
        tweet = refresh(user1_tweet)
        self.assertEqual(tweet.like, 2)

    def test_prevent_duplicated_like(self):
        user1_tweet = self._make_tweet(self.a_user)
        self.client.login(username=self.a_user.username, password='password')
        response = self.client.post(self.like_url_fmt % user1_tweet.id)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.like_url_fmt % user1_tweet.id)
        self.assertEqual(response.status_code, 400)
        tweet = refresh(user1_tweet)
        self.assertEqual(tweet.like, 1)

    def test_like_cancel(self):
        user1_tweet = self._make_tweet(self.a_user)
        self.client.login(username=self.a_user.username, password='password')
        response = self.client.post(self.like_url_fmt % user1_tweet.id)
        tweet = refresh(user1_tweet)
        self.assertEqual(tweet.like, 1)
        response = self.client.post(self.like_url_fmt % user1_tweet.id, {'delete': '1'})
        tweet = refresh(user1_tweet)
        self.assertEqual(tweet.like, 0)

    def test_remove_all_like_from_deleted_user(self):
        tweet1 = self._make_tweet(self.a_user)
        tweet2 = self._make_tweet(self.a_user)
        tweet3 = self._make_tweet(self.a_user)

        self.client.login(username=self.a_user.username, password='password')
        self.client.post(self.like_url_fmt % tweet1.id)
        self.client.post(self.like_url_fmt % tweet2.id)

        self.client.login(username=self.other_user.username, password='password')
        self.client.post(self.like_url_fmt % tweet2.id)
        self.client.post(self.like_url_fmt % tweet3.id)

        #    T1 T2 T3
        # U1  v  v
        # U2     v  v

        response = self.client.post(self.bye_url)
        for tweet in Tweet.objects.filter(id__in=[tweet1.id, tweet2.id]):
            self.assertEqual(tweet.like, 1)
        for tweet in Tweet.objects.filter(id__in=[tweet3.id]):
            self.assertEqual(tweet.like, 0)

    def test_likers_list(self):
        tweet1 = self._make_tweet(self.a_user)
        response = self.client.get(self.like_list_url_fmt % tweet1.id)
        self.assertEqual(json.loads(response.content), [])

        self.client.login(username=self.a_user.username, password='password')
        self.client.post(self.like_url_fmt % tweet1.id)
        response = self.client.get(self.like_list_url_fmt % tweet1.id)
        self.assertEqual(json.loads(response.content), [{'username':self.a_user.username,
                                                         'user_id':self.a_user.id}])

        self.client.login(username=self.other_user.username, password='password')
        self.client.post(self.like_url_fmt % tweet1.id)
        response = self.client.get(self.like_list_url_fmt % tweet1.id)
        self.assertEqual(sorted(json.loads(response.content), key=lambda u: u['user_id']), [
            {'username':self.a_user.username,
             'user_id':self.a_user.id},
            {'username':self.other_user.username,
             'user_id':self.other_user.id},
        ])

    # * comment list
    def test_comment_to_tweet(self):
        # * comment
        tweet1 = self._make_tweet(self.a_user)
        response = self.client.post(self.comment_url_fmt % tweet1.id, {'text': 'test comment'})
        self.assertEqual(Comment.objects.all().exists(), False)


        self.client.login(username=self.a_user, password='password')
        response = self.client.post(self.comment_url_fmt % tweet1.id, {'text': 'test comment'})
        comment = tweet1.comment_set.get()
        self.assertEqual(comment.text, 'test comment')

    def test_comment_list_of_tweet(self):
        # * comment list
        tweet1 = self._make_tweet(self.a_user)
        Comment.objects.create(tweet=tweet1, writer=self.a_user, text='test comment1')
        Comment.objects.create(tweet=tweet1, writer=self.a_user, text='test comment2')
        response = self.client.get(self.comment_list_url_fmt % tweet1.id)
        result = json.loads(response.content)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['text'], 'test comment1')
        self.assertEqual(result[1]['text'], 'test comment2')

