import functools
import json

from django.contrib.auth import get_user_model
from django.db.models import F
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from .models import Tweet, Comment


User = get_user_model()


def authorize(view):
    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseUnauthorized()
        return view(request, *args, **kwargs)
    return wrapper



# Create your views here.
def create(request):
    if len(request.POST.get('text')) > 140:
        return HttpResponseBadRequest("Fail")
    Tweet.objects.create(writer=request.user, text=request.POST.get('text'))
    return HttpResponse("OK")

def list_tweets(request):
    tweets = [
        {'writer': writer, 'text': text}
        for writer, text in Tweet.objects.all().values_list('writer__username', 'text')
    ]

    #tweets = list(Tweet.objects.all().values('writer__username', 'text'))
    #for i in tweets:
    #    i['writer'] = i.pop('writer__username')
    return HttpResponse(json.dumps(tweets))

def detail_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    detail_dict = {
        f.name: getattr(tweet, f.name) for f in tweet._meta.fields
        if not f.rel
    }
    return HttpResponse(json.dumps(detail_dict))

class HttpResponseUnauthorized(HttpResponse):
    def __init__(self):
        super(HttpResponseUnauthorized, self).__init__()
        self.status_code = 401

@authorize
def like_process(request, tweet_id):
    tweet = Tweet.objects.select_for_update().get(id=tweet_id)
    if request.POST.get('delete'):
        return _like_delete(request.user, tweet)
    else:
        return _like(request.user, tweet)

def _like(user, tweet):
    if tweet.likers.filter(id=user.id).exists():
        return HttpResponseBadRequest()
    tweet.likers.add(user)
    tweet.like += 1
    tweet.save()
    return HttpResponse()

def _like_delete(user, tweet):
    tweet.likers.filter(id=user.id).delete()
    tweet.like -= 1
    tweet.save() # XXX update_fields=.. causes error. dunno why.
    return HttpResponse()

def bye_user(request):
    request.user.is_active = False
    request.user.save()
    Tweet.objects.filter(likers=request.user).update(like=F('like') - 1)
    return HttpResponse('Bye')

def likers(request, tweet_id):
    likers = User.objects.filter(my_likes=tweet_id)
    likers = [{'username': user.username, 'user_id': user.id} for user in likers]
    return HttpResponse(json.dumps(likers))

@authorize
def create_comment(request, tweet_id):
    Comment.objects.create(tweet_id=tweet_id, writer=request.user, text=request.POST['text'])
    return HttpResponse('')

def comment_list(request, tweet_id):
    comments = Comment.objects.filter(tweet_id=tweet_id).order_by('id').values()
    return HttpResponse(json.dumps(list(comments)))

@authorize
def follow(request, user_id):
    target = User.objects.get(pk=user_id)
    me = request.user
    if ( target.stalkers.filter(id=me.id).exists() or
         me.stalkers.filter(id=target.id).exists() ):
        return HttpResponse(json.dumps({"result": "Blocked"}))
    request.user.following.add(target)
    return HttpResponse(json.dumps({"result": "OK"}))

@authorize
def unfollow(request, user_id):
    request.user.following.remove(User.objects.get(pk=user_id))
    return HttpResponse('OK')

@authorize
def block(request, stalker_id):
    stalker = User.objects.get(pk=stalker_id)
    request.user.stalkers.add(stalker)
    request.user.following.remove(stalker)
    request.user.follower.remove(stalker)
    return HttpResponse("BLOCK")

@authorize
def unblock(request, stalker_id):
    stalker = User.objects.get(pk=stalker_id)
    request.user.stalkers.remove(stalker)
    return HttpResponse("UNBLOCK")


#TODO : should be refactored below code blocks
def following(request, user_id):
    follower = User.objects.get(pk=user_id)
    followings = follower.following.all().values('id','username')
    followings = json.dumps(list(followings))
    return HttpResponse(followings)

def follower(request, user_id):
    following = User.objects.get(pk=user_id)
    followers = following.follower.all().values('id','username')
    followers = json.dumps(list(followers))
    return HttpResponse(followers)

@authorize
def blocked(request):
    blocker = request.user
    stalkers = blocker.stalkers.all().values('id','username')
    stalkers = json.dumps(list(stalkers))
    return HttpResponse(stalkers)
