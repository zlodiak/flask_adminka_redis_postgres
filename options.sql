--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.19
-- Dumped by pg_dump version 9.5.19

-- Started on 2019-12-06 15:04:44 MSK

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 182 (class 1259 OID 16458)
-- Name: options; Type: TABLE; Schema: public; Owner: flask_admin
--

CREATE TABLE public.options (
    id integer NOT NULL,
    firstname text,
    lastname text,
    notepad text,
    user_id integer NOT NULL
);


ALTER TABLE public.options OWNER TO flask_admin;

--
-- TOC entry 2140 (class 0 OID 16458)
-- Dependencies: 182
-- Data for Name: options; Type: TABLE DATA; Schema: public; Owner: flask_admin
--

COPY public.options (id, firstname, lastname, notepad, user_id) FROM stdin;
2	dd	22d	zxzvxcvx	2
1	ggg	hhh2	saasdsdf	1
0	222	1	rr	0
\.


--
-- TOC entry 2024 (class 2606 OID 16465)
-- Name: options_pkey; Type: CONSTRAINT; Schema: public; Owner: flask_admin
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_pkey PRIMARY KEY (id);


--
-- TOC entry 2025 (class 2606 OID 16522)
-- Name: user_id; Type: FK CONSTRAINT; Schema: public; Owner: flask_admin
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


-- Completed on 2019-12-06 15:04:44 MSK

--
-- PostgreSQL database dump complete
--

