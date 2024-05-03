CREATE EXTENSION postgis;

SET maintenance_work_mem = '16GB';
SET max_parallel_maintenance_workers = 80;


\set ON_ERROR_STOP on

BEGIN;
CREATE TABLE urls (
    id_urls BIGSERIAL PRIMARY KEY,
    url TEXT UNIQUE
);

CREATE TABLE users (
    id_users BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    age INTEGER
);

CREATE table tweets (
    id_tweets BIGSERIAL primary key,
    id_users integer not null REFERENCES users(id_users),
    text TEXT not null,
    created_at timestamp not null default current_timestamp,
    id_urls INTEGER REFERENCES urls(id_urls)
);
