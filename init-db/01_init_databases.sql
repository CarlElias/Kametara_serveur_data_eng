-- Script exécuté automatiquement au 1er démarrage du container postgres
-- Crée les databases et utilisateurs nécessaires pour Airflow et Metabase

-- Créer l'utilisateur airflow (si non existant)
DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'airflow') THEN
      CREATE ROLE airflow WITH LOGIN PASSWORD 'airflow';
   END IF;
END
$do$;

-- Donner les droits à l'utilisateur airflow
ALTER ROLE airflow WITH CREATEDB CREATEROLE;

-- Créer les bases de données
CREATE DATABASE airflow OWNER airflow;
CREATE DATABASE metabase OWNER airflow;

-- Donner les droits à l'utilisateur postgres (optionnel)
GRANT ALL PRIVILEGES ON DATABASE airflow TO postgres;
GRANT ALL PRIVILEGES ON DATABASE metabase TO postgres;