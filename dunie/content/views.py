# views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache

def increment_counter(request):
    session_key = request.session.session_key

    # Если у пользователя нет сессионного ключа, создаем его
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    # Проверяем, есть ли пользователь в Redis
    user_key = f"user:{session_key}"
    user_in_redis = cache.get(user_key)

    if not user_in_redis:
        # Если пользователь отсутствует в Redis, увеличиваем счетчик
        cache.incr('unique_visitors_count')
        # Помечаем пользователя в Redis, чтобы избежать двойного учета
        cache.set(user_key, True, timeout=None)

    # Получаем текущее значение счетчика
    unique_visitors_count = cache.get('unique_visitors_count')

    return HttpResponse(f'Уникальных посетителей: {unique_visitors_count}')


def view_counter(request):
    unique_visitors_count = cache.get('unique_visitors_count', 0)
    return render(request, 'counter/view_counter.html', {'unique_visitors_count': unique_visitors_count})


def index(request):
    return render(request, 'index.html')
