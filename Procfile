release: python manage.py migrate --no-input
web: daphne ZoomClone.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer -v2