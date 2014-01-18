import json

from django.db.models import F
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from .models import Tweet


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

def like_process(request, tweet_id):
    if not request.user.is_authenticated():
        return HttpResponseUnauthorized()
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
