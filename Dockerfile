FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pip install --no-cache-dir pipenv && pipenv install --deploy --system

COPY . .

ENV PORT=8080
ENV DJANGO_SETTINGS_MODULE=impactreeproject.settings
ENV SQLITE_DB_PATH=/app/db.sqlite3

EXPOSE 8080

CMD bash -c '\
if [ ! -f /app/db.sqlite3 ]; then \
    python manage.py migrate --noinput; \
    python manage.py loaddata users tokens milestones impactplans charitycategories charities impactplan_charities; \
fi; \
exec gunicorn impactreeproject.wsgi:application --bind :$PORT'