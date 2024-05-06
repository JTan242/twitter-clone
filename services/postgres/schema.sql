SET maintenance_work_mem = '16GB';
SET max_parallel_maintenance_workers = 80;
CREATE EXTENSION postgis;

\set ON_ERROR_STOP on
create extension RUM;
CREATE TABLE urls (
    id_urls BIGSERIAL PRIMARY KEY,
    url TEXT UNIQUE
);

CREATE TABLE users (
    id_users BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE tweets (
    id_tweets BIGSERIAL PRIMARY KEY,
    id_users INTEGER NOT NULL REFERENCES users(id_users) ON DELETE CASCADE,
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    id_urls INTEGER REFERENCES urls(id_urls)
);
CREATE INDEX ON tweets USING rum(to_tsvector('english', text));
