#!/bin/sh

echo "Esperando a la base de datos en $MYSQL_HOST:$MYSQL_PORT..."
until nc -z -v -w30 $MYSQL_HOST $MYSQL_PORT; do
  echo "Esperando..."
  sleep 5
done

echo "Base de datos disponible, ejecutando migraciones..."
python manage.py migrate --noinput

echo "Arrancando Gunicorn..."
gunicorn genomics.wsgi:application --bind 0.0.0.0:8000
