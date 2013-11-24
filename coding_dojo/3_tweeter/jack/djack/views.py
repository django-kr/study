import json

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
