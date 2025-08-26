-- Database initialization script
-- Creates the database and user if they don't exist

-- Connect to default database
\c postgres;

-- Create user if not exists
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'fastapi') THEN
        CREATE USER fastapi WITH PASSWORD 'password';
    END IF;
END
$$;

-- Create database if not exists
SELECT 'CREATE DATABASE fastapi_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'fastapi_db')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi;

-- Connect to the new database
\c fastapi_db;

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO fastapi;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fastapi;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fastapi;

-- Print success message
\echo 'Database initialization completed successfully!'