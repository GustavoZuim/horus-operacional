#!/usr/bin/env bash
# Script de build para Render.com

set -o errexit  # Exit on error

echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build concluido com sucesso!"
