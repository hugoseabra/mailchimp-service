#!/usr/bin/env bash

source /app_conf/services/scripts.sh
touch /code/.env

run_python_script "Coletando arquivos estáticos" "manage.py collectstatic --noinput --verbosity 0"
run_python_script_with_output "Atualizando Site ID" "manage.py loaddata 000_site"
run_python_script_with_output "Making migrations" "manage.py makemigrations"
run_python_script_with_output "Migrating" "manage.py migrate"

echo " > Iniciando SERVER"
echo ;
echo "########################################################################"
echo ;
gunicorn project.wsgi:application --bind 0.0.0.0:8000
