web: gunicorn django_project.wsgi:application --bind 0.0.0.0:$PORT
api: uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001
