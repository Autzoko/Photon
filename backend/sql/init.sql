-- current use PostgreSQL as database

-- create database for user management
CREATE DATABASE photon_user_management;

-- use `photon_user_management`
\c photon_user_management;

-- create user table

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE image (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- grant permissions for testuser
GRANT usage ON SCHEMA public TO {testuser};
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {testuser};
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {testuser};
GRANT ALL ON SCHEMA public TO {testuser};