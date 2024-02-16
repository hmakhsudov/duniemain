# views.py
from django.shortcuts import render
from .models import UserVisit

def user_count(request):
    # Получаем общее количество записей в базе данных
    total_users = UserVisit.objects.count()

    # Получаем информацию о посещениях пользователей из базы данных
    user_visits = UserVisit.objects.all()

    # Форматируем данные для передачи в шаблон
    user_entries = format_user_entries(user_visits)
    print(user_entries)
    return render(request, 'user_count.html', {'total_users': total_users, 'user_entries': user_entries})

def format_user_entries(user_visits):
    user_entries = []

    for visit in user_visits:
        timestamp = visit.timestamp
        date_str = timestamp.strftime("%d.%m.%Y")
        hour_str = timestamp.strftime("%H:00-%H:59")

        # Find or create the user entry for the current date and hourly period
        user_entry = next((entry for entry in user_entries if entry['date'] == date_str and entry['hour'] == hour_str), None)

        if user_entry is None:
            # If the user entry doesn't exist, create a new one
            user_entry = {'date': date_str, 'hour': hour_str, 'user_details': []}
            user_entries.append(user_entry)

        # Add user details to the current user entry
        user_entry['user_details'].append({
            'ip': visit.ip_address,
            'timestamp': timestamp.strftime("%H:%M:%S"),
            'country': visit.country,
            'city': visit.city,
        })

    # Sort user entries by the maximum timestamp across all user details in reverse order (newest first)
    user_entries.sort(key=lambda x: max(entry['timestamp'] for entry in x['user_details']), reverse=True)

    return user_entries

def index(request):
    return render(request, 'index.html')