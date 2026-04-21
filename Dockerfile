FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN SECRET_KEY=dummy-secret-key-for-build \
    DJANGO_SETTINGS_MODULE=safestorage.settings \
    DATABASE_URL=sqlite:////tmp/dummy.db \
    python manage.py collectstatic --noinput

CMD ["sh", "-c", "gunicorn safestorage.wsgi:application --bind 0.0.0.0:${PORT}"]