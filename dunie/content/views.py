# views.py
from django.shortcuts import render
import redis
from django.conf import settings

def user_count(request):
    redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])
    online_users = redis_client.get('online_users')
    return render(request, 'user_count.html', {'online_users': online_users.decode('utf-8') if online_users else '0'})

def index(request):

    return render(request, 'index.html')
