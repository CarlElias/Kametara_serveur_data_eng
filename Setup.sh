#!/bin/bash
# =============================================================
# setup.sh — À exécuter UNE FOIS avant docker compose up
# Crée les dossiers locaux nécessaires à Airflow
# =============================================================

set -e

echo "🔧 Création des dossiers locaux pour les containers..."
mkdir -p volumes/{dags,plugins,logs,metabase_data}
#mkdir -p dags plugins logs metabase_data minio_data postgres_data kafka_data zookeeper_data zookeeper_log

# Permissions Airflow
chown -R 50000:0 volumes/dags volumes/logs volumes/plugins

# Permissions Metabase
chown -R 1000:1000 volumes/metabase_data

# Permissions générales
chmod -R 755 volumes/

echo "✅ Dossiers créés :"
echo "   volumes/dags/"
echo "   volumes/plugins/"
echo "   volumes/logs/"
echo "   volumes/metabase_data/"

echo ""
echo "🚀 Tu peux maintenant lancer la stack :"
echo "   docker compose up -d"