#!/bin/bash
# =============================================================
# setup.sh — À exécuter UNE FOIS avant docker compose up
# =============================================================

set -e

echo "🔧 Création des dossiers locaux pour les containers..."
mkdir -p volumes/{dags,plugins,logs,metabase_data,minio_data,postgres_data,kafka_data,zookeeper_data,zookeeper_log,pgadmin_data}

# ── Airflow (user 50000, group 0) ──────────────────────────
chown -R 50000:0   volumes/dags volumes/logs volumes/plugins
chmod -R 775       volumes/dags volumes/plugins
chmod -R 777       volumes/logs   # Airflow crée des sous-dossiers en runtime (scheduler/, dag_processor_manager/)

# ── PostgreSQL (user 999 dans le container) ────────────────
chown -R 999:999   volumes/postgres_data
chmod -R 777       volumes/postgres_data

# ── pgAdmin (user 5050 dans le container) ─────────────────
chown -R 5050:5050 volumes/pgadmin_data
chmod -R 755       volumes/pgadmin_data

# ── Kafka + Zookeeper (user 1000) ─────────────────────────
chown -R 1000:1000 volumes/kafka_data volumes/zookeeper_data volumes/zookeeper_log
chmod -R 755       volumes/kafka_data volumes/zookeeper_data volumes/zookeeper_log

# ── MinIO (user 1000) ─────────────────────────────────────
chown -R 1000:1000 volumes/minio_data
chmod -R 755       volumes/minio_data

# ── Metabase (user 2000 dans le container) ────────────────
chown -R 2000:2000 volumes/metabase_data
chmod -R 755       volumes/metabase_data

echo ""

#apt install python3.14-venv

echo "✅ Dossiers créés :"
echo "   volumes/dags/"
echo "   volumes/plugins/"
echo "   volumes/logs/"
echo "   volumes/metabase_data/"
echo "   volumes/minio_data/"
echo "   volumes/postgres_data/"
echo "   volumes/kafka_data/"
echo "   volumes/zookeeper_data/"
echo "   volumes/zookeeper_log/"
echo "   volumes/pgadmin_data/"
echo ""
echo "🚀 Installation de la stack :"
docker compose up -d

#python3 -m venv venv
#source venv/bin/activate
#pip install -r requirements.txt