#!/usr/bin/env bash

source /app_conf/services/scripts.sh
touch /code/.env

# Define settings
export DJANGO_SETTINGS_MODULE=project.settings

#run_python_script "Configurando SETTINGS" /deploy/setup/configure-settings.py
run_python_script_with_output "Atualizando Site ID" "manage.py loaddata 000_site"

echo " > Iniciando CELERY"
echo ;
echo "########################################################################"
echo ;
celery -E --loglevel=INFO -A project worker -B -l INFO --scheduler django -s /tmp/beat-scheduler --logfile="/tmp/celery-logs/celery.log"