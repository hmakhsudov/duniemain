# middleware.py
import redis
from django.conf import settings
from datetime import datetime

class OnlineUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])

    def __call__(self, request):
        user_ip = self._get_client_ip(request)
        key = f'online_users:{user_ip}'
        
        # Проверяем, был ли пользователь уже учтен
        if not self.redis_client.exists(key):
            # Если нет, увеличиваем счетчик
            self.redis_client.incr('online_users')
            # Устанавливаем метку, что пользователь уже учтен
            self.redis_client.set(key, '1')
            # Сохраняем IP-адрес и дату в отдельный список
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            self.redis_client.lpush('user_ips', f'{timestamp} - {user_ip}')
        
        response = self.get_response(request)
        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
