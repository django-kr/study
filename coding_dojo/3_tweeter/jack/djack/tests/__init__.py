import string
import random

from djack.models import JackUser as User

from ..models import Tweet

class TestHelper(object):
    entire_tweet_list_url = '/jack/'
    tweet_create_url = '/jack/create/'
    like_url_fmt = '/jack/like/%d'
    like_list_url_fmt = '/jack/likers/%d'
    detail_url_fmt = '/jack/%d'
    comment_url_fmt = '/jack/%d/comment/new'
    comment_list_url_fmt = '/jack/%d/comment'
    bye_url = '/jack/bye/'

    def _make_tweet(self, user, text='default text'):
        return Tweet.objects.create(writer=user, text=text)

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

