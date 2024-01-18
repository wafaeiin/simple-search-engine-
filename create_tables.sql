-- create_tables.sql
CREATE DATABASE IF NOT EXISTS search_engine_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TABLE IF NOT EXISTS public.docs (
    id integer NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    authors text[] COLLATE pg_catalog."default",
    publication_date date,
    abstract text COLLATE pg_catalog."default",
    keywords text[] COLLATE pg_catalog."default",
    CONSTRAINT docs_pkey PRIMARY KEY (id)
);
