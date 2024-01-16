# Apply migrations and collect static files
python manage.py migrate --no-input
python manage.py collectstatic --no-input

# Check if the superuser already exists
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'admin') if not User.objects.filter(username='admin').exists() else None"

# Start Gunicorn
gunicorn dunie.wsgi:application --bind 0.0.0.0:8000
