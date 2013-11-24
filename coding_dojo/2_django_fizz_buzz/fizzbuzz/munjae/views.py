from django.shortcuts import render
from django.http import HttpResponse
import json

def fizz_buzz(request):
    max_range = int(request.GET.get('range'))
    listed_range = range(1, max_range+1)
    if max_range >= 3:
        listed_range[3-1] = 'fizz'
    if max_range >= 5:
        listed_range[5-1] = 'buzz'
    return HttpResponse(json.dumps(listed_range))
