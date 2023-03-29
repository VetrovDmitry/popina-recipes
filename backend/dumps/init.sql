--
-- PostgreSQL database dump
--

-- Dumped from database version 14.3
-- Dumped by pg_dump version 14.7 (Ubuntu 14.7-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: adminstatus; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.adminstatus AS ENUM (
    'ADMIN',
    'MODER'
);


ALTER TYPE public.adminstatus OWNER TO admin;

--
-- Name: devicestatus; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.devicestatus AS ENUM (
    'ENABLE',
    'DISABLE'
);


ALTER TYPE public.devicestatus OWNER TO admin;

--
-- Name: humangender; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.humangender AS ENUM (
    'MALE',
    'FEMALE'
);


ALTER TYPE public.humangender OWNER TO admin;

--
-- Name: recipecomplexity; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.recipecomplexity AS ENUM (
    'EASY',
    'MEDIUM',
    'HARD'
);


ALTER TYPE public.recipecomplexity OWNER TO admin;

--
-- Name: tokenstatus; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.tokenstatus AS ENUM (
    'ACTIVE',
    'EXPIRED'
);


ALTER TYPE public.tokenstatus OWNER TO admin;

--
-- Name: userstatus; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.userstatus AS ENUM (
    'UNCONFIRMED',
    'CONFIRMED',
    'FROZEN',
    'DELETED'
);


ALTER TYPE public.userstatus OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admins; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.admins (
    id integer NOT NULL,
    status public.adminstatus,
    time_created timestamp with time zone DEFAULT now(),
    time_updated timestamp with time zone
);


ALTER TABLE public.admins OWNER TO admin;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO admin;

--
-- Name: devices; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.devices (
    id integer NOT NULL,
    admin_id integer,
    name character varying(80) NOT NULL,
    key character varying(80) NOT NULL,
    status public.devicestatus NOT NULL,
    requests integer NOT NULL
);


ALTER TABLE public.devices OWNER TO admin;

--
-- Name: devices_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.devices_id_seq OWNER TO admin;

--
-- Name: devices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.devices_id_seq OWNED BY public.devices.id;


--
-- Name: recipes; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.recipes (
    id integer NOT NULL,
    user_id integer,
    title character varying(80) NOT NULL,
    description text NOT NULL,
    complexity public.recipecomplexity NOT NULL,
    cooking_time integer NOT NULL,
    instruction text NOT NULL,
    time_created timestamp with time zone DEFAULT now(),
    time_updated timestamp with time zone
);


ALTER TABLE public.recipes OWNER TO admin;

--
-- Name: recipes_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.recipes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_id_seq OWNER TO admin;

--
-- Name: recipes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.recipes_id_seq OWNED BY public.recipes.id;


--
-- Name: tokens; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.tokens (
    id integer NOT NULL,
    device_id integer,
    user_id integer,
    access_token text NOT NULL,
    refresh_token text NOT NULL,
    expires timestamp with time zone,
    status public.tokenstatus NOT NULL
);


ALTER TABLE public.tokens OWNER TO admin;

--
-- Name: tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tokens_id_seq OWNER TO admin;

--
-- Name: tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.tokens_id_seq OWNED BY public.tokens.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users (
    id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    username character varying(50) NOT NULL,
    sex public.humangender,
    birth_date date NOT NULL,
    email character varying(100) NOT NULL,
    hash character varying(255) NOT NULL,
    status public.userstatus,
    time_created timestamp with time zone DEFAULT now(),
    time_updated timestamp with time zone
);


ALTER TABLE public.users OWNER TO admin;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO admin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: devices id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.devices ALTER COLUMN id SET DEFAULT nextval('public.devices_id_seq'::regclass);


--
-- Name: recipes id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes ALTER COLUMN id SET DEFAULT nextval('public.recipes_id_seq'::regclass);


--
-- Name: tokens id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tokens ALTER COLUMN id SET DEFAULT nextval('public.tokens_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.admins (id, status, time_created, time_updated) FROM stdin;
1	ADMIN	2023-03-28 10:55:02.100076+00	\N
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.alembic_version (version_num) FROM stdin;
61445740c35d
\.


--
-- Data for Name: devices; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.devices (id, admin_id, name, key, status, requests) FROM stdin;
1	1	test-app	THIS-FIELD-SHOULD-BE-CHANGED	ENABLE	492
\.


--
-- Data for Name: recipes; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.recipes (id, user_id, title, description, complexity, cooking_time, instruction, time_created, time_updated) FROM stdin;
1	1	Burger	Testy burger with cucumber and chicken wings	HARD	66	set on microwave	2023-03-28 11:56:01.305112+00	2023-03-28 13:30:02.263845+00
2	1	Meet Balls	Meet balls with BBQ 	MEDIUM	22	set on cooker	2023-03-28 11:57:17.052914+00	\N
3	1	Pasta	Easy pasta with corn	EASY	45	1. Buy corn \r\n2. Buy pasta\r\n3. Mix pasta with corn and cook it together	2023-03-29 15:17:43.894406+00	\N
4	1	Doshirak	Incredibly delicious noodles	MEDIUM	15	1. Buy doshirak\r\n2. Boil water\r\n3. Pour boiling water into noodles\r\n4. Chill and relax	2023-03-29 15:53:33.757163+00	\N
\.


--
-- Data for Name: tokens; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.tokens (id, device_id, user_id, access_token, refresh_token, expires, status) FROM stdin;
2	1	2	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MDA5Njc1NSwianRpIjoiYTJhZDMwNWMtODBlMi00MTY0LWE3NjMtYWYzMTAzMDlhZjkyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InsnaWQnOiAyLCAndXNlcm5hbWUnOiAndGVzdF91c2VyJ30iLCJuYmYiOjE2ODAwOTY3NTUsImV4cCI6MTY4MDA5ODU1NX0.OODm_uAYT3XNMbqUbLruehXqB7xmALZL5k851UbFJE4	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MDA5Njc1NSwianRpIjoiNGE1MDFjODAtYzNjMS00M2ZhLTk3MzctYTMwOTA5Y2QyZTg1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJ7J2lkJzogMiwgJ2V4cGlyZXNfYXQnOiAnMjAyMy0wMy0yOVQxNjozMjozNS4yNTAxMjkrMDA6MDAnfSIsIm5iZiI6MTY4MDA5Njc1NSwiZXhwIjoxNjgwMTA3NTU1fQ.8bLV7_fwrUf2teeo3Ibp7fBDcmRbl4kaQRsZNNmXfSs	2023-03-29 14:02:35.250129+00	ACTIVE
1	1	1	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MDEwNTAyMiwianRpIjoiOWMxOWRmNjUtYTYyZi00NmRlLTkxMjEtMjlhMDdiYmEzMDU3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InsnaWQnOiAxLCAndXNlcm5hbWUnOiAncG9waW5hMDA3J30iLCJuYmYiOjE2ODAxMDUwMjIsImV4cCI6MTY4MDEwNjgyMn0.xouUwtdjpiz3bInMEMZmMfAJ92L1MJoHkX2yS2c6t9c	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MDEwNTAyMiwianRpIjoiYjNmMmMwZTAtMWU5MS00ZDUyLWI3NDMtZjY5MTM3OTY5NmI4IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJ7J2lkJzogMSwgJ2V4cGlyZXNfYXQnOiAnMjAyMy0wMy0yOVQxODo1MDoyMi43MzA3MTMrMDA6MDAnfSIsIm5iZiI6MTY4MDEwNTAyMiwiZXhwIjoxNjgwMTE1ODIyfQ.2ai4T6RGkkJSEHI6MrkGWfvnuUi7JJsoWTg8PGHoD0E	2023-03-29 16:20:22.730713+00	ACTIVE
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users (id, first_name, last_name, username, sex, birth_date, email, hash, status, time_created, time_updated) FROM stdin;
1	One	Admin	admin	FEMALE	1970-01-01	admin@mail.com	$2b$12$sjxvXLtrWSgfWsASUtGn0.k.1xj.TEGrohl/1GGIfDzMJ0zt0xY7S	CONFIRMED	2023-03-28 10:54:27.421824+00	2023-03-28 11:05:29.397452+00
2	Anastasia	Popina	popina	FEMALE	2023-03-04	nastya@popina.com	$2b$12$j1csUF68cybk/e/Nh/UtqezRJkLHmql/BAxgSoZh9EPHiI.69HNjC	CONFIRMED	2023-03-29 00:07:30.681903+00	\N
\.


--
-- Name: devices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.devices_id_seq', 1, true);


--
-- Name: recipes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.recipes_id_seq', 4, true);


--
-- Name: tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.tokens_id_seq', 2, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: devices devices_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_name_key UNIQUE (name);


--
-- Name: devices devices_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);


--
-- Name: recipes recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (id);


--
-- Name: tokens tokens_access_token_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tokens
    ADD CONSTRAINT tokens_access_token_key UNIQUE (access_token);


--
-- Name: tokens tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tokens
    ADD CONSTRAINT tokens_pkey PRIMARY KEY (id);


--
-- Name: tokens tokens_refresh_token_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tokens
    ADD CONSTRAINT tokens_refresh_token_key UNIQUE (refresh_token);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: admins admins_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- Name: devices devices_admin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES public.admins(id);


--
-- Name: recipes recipes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: tokens tokens_device_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tokens
    ADD CONSTRAINT tokens_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id);


--
-- Name: tokens tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tokens
    ADD CONSTRAINT tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

