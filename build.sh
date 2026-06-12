#!/usr/bin/env bash
# Script de build para Render.com

set -o errexit  # Exit on error

echo "???? Instalando depend??ncias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "??????? Inicializando banco de dados..."
python init_db.py

echo "??? Build conclu??do com sucesso!"
