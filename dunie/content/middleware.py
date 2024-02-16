# middleware.py
import requests
from django.db import models
from django.conf import settings
from datetime import datetime
from .models import UserVisit
class OnlineUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = self._get_client_ip(request)
        
        # Проверяем, был ли пользователь уже учтен
        if not UserVisit.objects.filter(ip_address=user_ip).exists():
            # Сохраняем информацию о пользователе в базе данных
            self._save_user_info(user_ip)

        response = self.get_response(request)
        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _save_user_info(self, user_ip):
        # Получаем информацию о геолокации
        country, city = self._get_geo_info(user_ip)
        
        # Сохраняем информацию в базе данных
        timestamp = datetime.now()  # Get the current timestamp
        user_visit = UserVisit(ip_address=user_ip, country=country, city=city, timestamp=timestamp)
        user_visit.save()

    def _get_geo_info(self, ip_address):
        url = f'http://ip-api.com/json/{ip_address}'
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'fail':
            print('Error fetching geo-location information.')
            return None, None
        else:
            country = data.get('country')
            city = data.get('city')
            return country, city