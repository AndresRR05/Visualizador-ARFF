#!/usr/bin/env bash
# Exit on error
set -o errexit

# Añadimos esta línea para forzar la instalación
pip install -r requirements.txt

# Comandos de Django
python manage.py collectstatic --no-input
python manage.py migrate