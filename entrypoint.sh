
#!/bin/sh
set -e

CPU_COUNT=$(nproc)

# Gunicorn
GUNICORN_WORKERS=$((CPU_COUNT * 2 + 1))
GUNICORN_THREADS=2

# Celery
CELERY_CONCURRENCY=$CPU_COUNT

echo "🧠 CPUs detectadas: $CPU_COUNT"
echo "🌐 Gunicorn workers: $GUNICORN_WORKERS"
echo "🌱 Celery concurrency: $CELERY_CONCURRENCY"

echo "🟥 Iniciando Redis..."
redis-server --daemonize yes

echo "🌱 Iniciando Celery worker..."
celery -A config worker \
    --loglevel=info \
    --concurrency=$CELERY_CONCURRENCY &

# Se quiser o beat:
# celery -A config beat -l info &

echo "🚀 Iniciando Django (Gunicorn)..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers $GUNICORN_WORKERS \
    --threads $GUNICORN_THREADS \
    --timeout 60
