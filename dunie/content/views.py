# views.py
from django.shortcuts import render
import redis
from django.conf import settings
from datetime import datetime

def user_count(request):
    redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])
    online_users = redis_client.get('online_users')

    user_ips = redis_client.lrange('user_ips', 0, -1)
    user_entries = format_user_entries(user_ips)

    return render(request, 'user_count.html', {'online_users': online_users.decode('utf-8') if online_users else '0', 'user_entries': user_entries})

def format_user_entries(user_ips):
    user_entries = []
    current_date = None
    hourly_entries = []

    for entry in user_ips:
        entry_parts = entry.decode('utf-8').split(' - ')
        timestamp_str = entry_parts[0]
        user_ip_str = entry_parts[1]
        try:
            country = entry_parts[2]
            city = entry_parts[3]
        except IndexError:
            country = city = "N/A"  # Или любое другое значение по умолчанию, которое вы хотите использовать.

        timestamp = datetime.strptime(timestamp_str, "%d.%m.%Y %H:%M:%S")
        date_str = timestamp.strftime("%d.%m.%Y")
        hour_str = timestamp.strftime("%H:00-%H:59")

        if date_str != current_date:
            if current_date is not None:
                user_entries.append({'date': current_date, 'hourly_entries': hourly_entries})

            hourly_entries = [{'hour': hour_str, 'ip': user_ip_str, 'timestamp': timestamp_str, 'country': country, 'city': city}]
            current_date = date_str
        else:
            hourly_entries.append({'hour': hour_str, 'ip': user_ip_str, 'timestamp': timestamp_str, 'country': country, 'city': city})

    if current_date is not None:
        user_entries.append({'date': current_date, 'hourly_entries': hourly_entries})

    return user_entries

def index(request):
    return render(request, 'index.html')
