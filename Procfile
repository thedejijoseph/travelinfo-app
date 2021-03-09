release: python manage.py migrate
web: gunicorn travelinfo_app.wsgi --bind=0.0.0.0:$PORT
