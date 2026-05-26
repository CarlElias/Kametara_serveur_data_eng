-- =============================================================
-- Script exécuté automatiquement au 1er démarrage du container
-- Crée les databases airflow et metabase avec le compte postgres
-- UN SEUL COMPTE : postgres / postgres gère tout
-- =============================================================
 
-- Créer la base de données pour Airflow
CREATE DATABASE airflow;
 
-- Créer la base de données pour Metabase
CREATE DATABASE metabase;
 
-- Donner tous les droits à postgres sur les deux bases
GRANT ALL PRIVILEGES ON DATABASE airflow TO postgres;
GRANT ALL PRIVILEGES ON DATABASE metabase TO postgres;