
raw
Readme · MD
# 📈 Pipeline de Données Boursières en Temps Réel
 
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?logo=apachekafka&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?logo=apacheairflow&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?logo=dbt&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-C72E49?logo=minio&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Metabase](https://img.shields.io/badge/Metabase-509EE3?logo=metabase&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
 
---
 
## 📌 Vue d'ensemble du projet
 
Ce projet met en œuvre un **pipeline de données end-to-end en temps réel** basé sur le **Modern Data Stack**.  
Il capture des **données boursières en direct** depuis une API externe, les diffuse via Kafka, les stocke dans MinIO, orchestre les transformations avec Airflow et dbt, et expose les résultats dans Metabase — le tout conteneurisé avec Docker.
 
```
Finnhub API → Kafka → MinIO (S3) → Airflow + dbt → PostgreSQL → Metabase
```
 
---
 
## ⚡ Stack Technique
 
| Composant | Rôle |
|---|---|
| **Apache Kafka** | Streaming de données en temps réel |
| **MinIO** | Stockage objet S3-compatible (Data Lake) |
| **Apache Airflow** | Orchestration des workflows ETL |
| **dbt** | Transformations SQL (Bronze → Silver → Gold) |
| **PostgreSQL** | Base de données centrale (Airflow + Metabase) |
| **Metabase** | Visualisation et dashboards analytiques |
| **Python** | Producteur et consommateur Kafka |
| **Docker Compose** | Conteneurisation de l'ensemble des services |
 
---
 
## 🏗️ Architecture
 
```
┌─────────────────┐     ┌────────────────┐     ┌─────────────────┐
│   Finnhub API   │────▶│  Kafka Producer │────▶│  Apache Kafka   │
│  (données live) │     │   (Python)      │     │  stocks-topic   │
└─────────────────┘     └────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │  Kafka Consumer  │
                                               │    (Python)      │
                                               └────────┬────────┘
                                                        │
                                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                        MinIO (S3)                                │
│              Couche Bronze — données brutes JSON                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Apache Airflow (DAG)                          │
│         MinIO → PostgreSQL  |  Déclenchement dbt                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  dbt — Transformations SQL                        │
│  Bronze (brut) → Silver (nettoyé) → Gold (agrégé / analytique)  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌──────────────┐      ┌──────────────────────────────────────────┐
│  PostgreSQL  │◀─────│         Tables Gold analytiques          │
│  (warehouse) │      │  Candlestick | KPI | Treechart           │
└──────┬───────┘      └──────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│  Metabase   │
│  Dashboard  │
└─────────────┘
```
 
---
 
## 📂 Structure du dépôt
 
```text
real-time-stocks-pipeline/
├── producer/
│   └── producer.py                    # Producteur Kafka (API Finnhub)
├── consumer/
│   └── consumer.py                    # Consommateur Kafka → MinIO
├── dbt_stocks/
│   └── models/
│       ├── bronze/
│       │   ├── bronze_stg_stock_quotes.sql
│       │   └── sources.yml
│       ├── silver/
│       │   └── silver_clean_stock_quotes.sql
│       └── gold/
│           ├── gold_candlestick.sql
│           ├── gold_kpi.sql
│           └── gold_treechart.sql
├── dags/
│   └── minio_to_postgres.py           # DAG Airflow principal
├── init-db/                           # Scripts SQL d'initialisation PostgreSQL
├── docker-compose.yml                 # Tous les services conteneurisés
├── requirements.txt
└── README.md
```
 
---
 
## 🚀 Démarrage rapide
 
### Prérequis
 
- [Docker](https://www.docker.com/) et Docker Compose installés
- Clé API [Finnhub](https://finnhub.io/) (compte gratuit)
- Python 3.11+
### 1. Cloner le dépôt
 
```bash
git clone https://github.com/<votre-username>/real-time-stocks-pipeline.git
cd real-time-stocks-pipeline
```
 
### 2. Configurer les variables d'environnement
 
```bash
cp .env.example .env
# Renseigner votre clé API Finnhub dans .env
FINNHUB_API_KEY=votre_cle_api
```
 
### 3. Lancer les services Docker
 
```bash
docker compose up -d
```
 
Les services suivants démarrent automatiquement :
 
| Service | URL |
|---|---|
| Apache Airflow | http://localhost:8080 |
| MinIO Console | http://localhost:9001 |
| Kafdrop (Kafka UI) | http://localhost:9000 |
| Metabase | http://localhost:3000 |
| PostgreSQL | localhost:5432 |
 
> **Identifiants par défaut** — Airflow : `admin / password123` · MinIO : `admin / password123`
 
### 4. Lancer le producteur Kafka
 
```bash
pip install -r requirements.txt
python producer/producer.py
```
 
### 5. Lancer le consommateur Kafka
 
```bash
python consumer/consumer.py
```
 
### 6. Activer le DAG Airflow
 
Se connecter à Airflow (http://localhost:8080) et activer le DAG `minio_to_postgres`.
 
---
 
## ⚙️ Détail des composants
 
### Producteur Kafka (`producer/producer.py`)
- Interroge l'**API Finnhub** pour récupérer les cours boursiers en temps réel.
- Sérialise les données en **JSON** et les publie dans le topic Kafka `stocks-topic`.
### Consommateur Kafka (`consumer/consumer.py`)
- Consomme les messages depuis Kafka.
- Persiste les données brutes dans des **buckets MinIO** (couche Bronze).
### DAG Airflow (`dags/minio_to_postgres.py`)
- Charge les fichiers JSON depuis MinIO vers les **tables de staging PostgreSQL**.
- Déclenche les modèles **dbt** pour appliquer les transformations.
- Planification : toutes les **1 minute**.
### Transformations dbt
 
| Couche | Modèle | Description |
|---|---|---|
| **Bronze** | `bronze_stg_stock_quotes` | Données brutes structurées depuis MinIO |
| **Silver** | `silver_clean_stock_quotes` | Données nettoyées et validées |
| **Gold** | `gold_candlestick` | Données OHLCV pour graphiques en chandeliers |
| **Gold** | `gold_kpi` | Indicateurs clés de performance |
| **Gold** | `gold_treechart` | Agrégats pour visualisation en treemap |
 
### Metabase
- Connecté à la couche **Gold** de PostgreSQL.
- Dashboards disponibles :
  - **Graphique en chandeliers** — patterns de marché
  - **Treemap** — tendances par action
  - **KPIs** — volumes, prix, variations en temps réel
---
 
## 🐳 Services Docker Compose
 
| Conteneur | Image | Port(s) |
|---|---|---|
| `postgres_sn` | postgres:latest | 5432 |
| `zookeeper_sn` | confluentinc/cp-zookeeper:7.4.0 | 2181 |
| `kafka_sn` | confluentinc/cp-kafka:7.4.0 | 9092, 29092 |
| `kafdrop` | obsidiandynamics/kafdrop | 9000 |
| `minio` | minio/minio:latest | 9001, 9002 |
| `airflow-webserver-sn` | apache/airflow:2.8.0-python3.11 | 8080 |
| `airflow-scheduler-sn` | apache/airflow:2.8.0-python3.11 | — |
| `metabase_sn` | metabase/metabase:latest | 3000 |
 
---
 
## 📊 Livrables finaux
 
- ✅ Pipeline de données automatisé en temps réel
- ✅ Data Lake structuré dans MinIO (couche Bronze)
- ✅ Tables PostgreSQL transformées (Bronze → Silver → Gold)
- ✅ Modèles analytiques dbt (Candlestick, KPI, Treechart)
- ✅ DAGs Airflow orchestrés et planifiés
- ✅ Dashboard Metabase avec insights en quasi-temps réel
---
 

 