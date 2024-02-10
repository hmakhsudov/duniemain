# middleware.py
import redis
from django.conf import settings

class OnlineUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])
    def __call__(self, request):
        user_id = request.session.session_key or self._create_session_key(request)
        key = f'online_users:{user_id}'
        # Проверяем, был ли пользователь уже учтен
        if not self.redis_client.exists(key):
            # Если нет, увеличиваем счетчик и устанавливаем TTL
            self.redis_client.incr('online_users')
            self.redis_client.setex(key, 60 * 5, 1)  # Устанавливаем TTL в 5 минут
        response = self.get_response(request)
        return response

    def _create_session_key(self, request):
        # Создаем уникальный идентификатор сессии, если его нет
        request.session.create()
        return request.session.session_key