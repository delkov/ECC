--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.9
-- Dumped by pg_dump version 9.6.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: omsk; Type: SCHEMA; Schema: -; Owner: postgres
--

DROP TABLE omsk.noise;
DROP TABLE omsk.tracks;
DROP TABLE omsk.aircraft_tracks;
DROP TABLE omsk.static_points;

DROP SCHEMA omsk;

CREATE SCHEMA omsk;


ALTER SCHEMA omsk OWNER TO postgres;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: aircraft_tracks; Type: TABLE; Schema: omsk; Owner: postgres
--

CREATE TABLE omsk.aircraft_tracks (
    track bigint NOT NULL,
    icao text,
    first_time timestamp without time zone,
    last_time timestamp without time zone,
    callsign_last_time timestamp without time zone,
    altitude_last_time timestamp without time zone,
    speed_angle_last_time timestamp without time zone,
    coordinate_last_time timestamp without time zone,
    vert_speed_last_time timestamp without time zone,
    vpp_angle real,
    type_of_flight boolean
);


ALTER TABLE omsk.aircraft_tracks OWNER TO postgres;

--
-- Name: aircraft_tracks_track_seq; Type: SEQUENCE; Schema: omsk; Owner: postgres
--

CREATE SEQUENCE omsk.aircraft_tracks_track_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE omsk.aircraft_tracks_track_seq OWNER TO postgres;

--
-- Name: aircraft_tracks_track_seq; Type: SEQUENCE OWNED BY; Schema: omsk; Owner: postgres
--

ALTER SEQUENCE omsk.aircraft_tracks_track_seq OWNED BY omsk.aircraft_tracks.track;


--
-- Name: aircrafts; Type: TABLE; Schema: omsk; Owner: postgres
--

-- CREATE TABLE omsk.aircrafts (
--     icao text NOT NULL,
--     regid text,
--     mdl text,
--     type text,
--     operator text,
--     blank text
-- );


-- ALTER TABLE omsk.aircrafts OWNER TO postgres;

--
-- Name: noise; Type: TABLE; Schema: omsk; Owner: postgres
--

CREATE TABLE omsk.noise (
    id bigint NOT NULL,
    time_noise timestamp without time zone NOT NULL,
    base_name text,
    stat_1 smallint,
    stat_2 smallint,
    stat_3 smallint,
    leq real,
    slow real,
    spectrum real[],
    meteo_stat smallint,
    temperature real,
    humadity real,
    presure real,
    wind real,
    dir real,
    gps_coordinate real[],
    gps_stat smallint,
    temperature_core smallint,
    temperature_mb smallint,
    temperature_hdd smallint,
    free_hdd smallint,
    ups_stat smallint,
    ups_mode text,
    ups_time smallint,
    checked_by_sbs_join boolean,
    track bigint,
    distance integer,
    aircraft_time timestamp without time zone
);


ALTER TABLE omsk.noise OWNER TO postgres;

--
-- Name: noise_id_seq; Type: SEQUENCE; Schema: omsk; Owner: postgres
--

CREATE SEQUENCE omsk.noise_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE omsk.noise_id_seq OWNER TO postgres;

--
-- Name: noise_id_seq; Type: SEQUENCE OWNED BY; Schema: omsk; Owner: postgres
--

ALTER SEQUENCE omsk.noise_id_seq OWNED BY omsk.noise.id;


--
-- Name: routes; Type: TABLE; Schema: omsk; Owner: postgres
--

-- CREATE TABLE omsk.routes (
--     callsign text NOT NULL,
--     fromairport text,
--     toairport text,
--     blank text
-- );


-- ALTER TABLE omsk.routes OWNER TO postgres;

--
-- Name: static_points; Type: TABLE; Schema: omsk; Owner: postgres
--

CREATE TABLE omsk.static_points (
    name text,
    lon double precision,
    lat double precision,
    alt double precision,
    geom public.geometry(PointZ)
);


ALTER TABLE omsk.static_points OWNER TO postgres;

--
-- Name: tracks; Type: TABLE; Schema: omsk; Owner: postgres
--

CREATE TABLE omsk.tracks (
    id bigint NOT NULL,
    time_track timestamp without time zone NOT NULL,
    track bigint,
    callsign text,
    altitude integer,
    speed smallint,
    angle real,
    latitude double precision,
    longitude double precision,
    vertical_speed smallint,
    distance_1 integer,
    geom public.geometry(Point,4326)
);


ALTER TABLE omsk.tracks OWNER TO postgres;

--
-- Name: tracks_id_seq; Type: SEQUENCE; Schema: omsk; Owner: postgres
--

CREATE SEQUENCE omsk.tracks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE omsk.tracks_id_seq OWNER TO postgres;

--
-- Name: tracks_id_seq; Type: SEQUENCE OWNED BY; Schema: omsk; Owner: postgres
--

ALTER SEQUENCE omsk.tracks_id_seq OWNED BY omsk.tracks.id;


--
-- Name: aircraft_tracks track; Type: DEFAULT; Schema: omsk; Owner: postgres
--

ALTER TABLE ONLY omsk.aircraft_tracks ALTER COLUMN track SET DEFAULT nextval('omsk.aircraft_tracks_track_seq'::regclass);


--
-- Name: noise id; Type: DEFAULT; Schema: omsk; Owner: postgres
--

ALTER TABLE ONLY omsk.noise ALTER COLUMN id SET DEFAULT nextval('omsk.noise_id_seq'::regclass);


--
-- Name: tracks id; Type: DEFAULT; Schema: omsk; Owner: postgres
--

ALTER TABLE ONLY omsk.tracks ALTER COLUMN id SET DEFAULT nextval('omsk.tracks_id_seq'::regclass);


--
-- Name: aircraft_tracks pk_aircraft_tracks; Type: CONSTRAINT; Schema: omsk; Owner: postgres
--

ALTER TABLE ONLY omsk.aircraft_tracks
    ADD CONSTRAINT pk_aircraft_tracks PRIMARY KEY (track);


--
-- Name: aircrafts pk_aircrafts; Type: CONSTRAINT; Schema: omsk; Owner: postgres
--

-- ALTER TABLE ONLY omsk.aircrafts
--     ADD CONSTRAINT pk_aircrafts PRIMARY KEY (icao);


--
-- Name: noise pk_noise; Type: CONSTRAINT; Schema: omsk; Owner: postgres
--

ALTER TABLE ONLY omsk.noise
    ADD CONSTRAINT pk_noise PRIMARY KEY (id);


--
-- Name: tracks pk_tracks; Type: CONSTRAINT; Schema: omsk; Owner: postgres
--

ALTER TABLE ONLY omsk.tracks
    ADD CONSTRAINT pk_tracks PRIMARY KEY (id);


--
-- Name: routes pr_routes; Type: CONSTRAINT; Schema: omsk; Owner: postgres
-- --

-- ALTER TABLE ONLY omsk.routes
--     ADD CONSTRAINT pr_routes PRIMARY KEY (callsign);


--
-- Name: tracks tracks_time_track_track_key; Type: CONSTRAINT; Schema: omsk; Owner: postgres
--

ALTER TABLE ONLY omsk.tracks
    ADD CONSTRAINT tracks_time_track_track_key UNIQUE (time_track, track);


--
-- Name: idx_aircraft_tracks; Type: INDEX; Schema: omsk; Owner: postgres
--

CREATE INDEX idx_aircraft_tracks ON omsk.aircraft_tracks USING btree (icao);


--
-- Name: idx_time_track; Type: INDEX; Schema: omsk; Owner: postgres
--

CREATE INDEX idx_time_track ON omsk.tracks USING btree (time_track);


--
-- Name: idx_tracks; Type: INDEX; Schema: omsk; Owner: postgres
--

CREATE INDEX idx_tracks ON omsk.tracks USING btree (track);


--
-- Name: aircraft_tracks fk_aircraft_tracks_aircrafts; Type: FK CONSTRAINT; Schema: omsk; Owner: postgres
--

-- ALTER TABLE ONLY omsk.aircraft_tracks
    -- ADD CONSTRAINT fk_aircraft_tracks_aircrafts FOREIGN KEY (icao) REFERENCES omsk.aircrafts(icao) ON DELETE RESTRICT;


--
-- Name: tracks fk_tracks_aircraft_tracks; Type: FK CONSTRAINT; Schema: omsk; Owner: postgres
--

ALTER TABLE ONLY omsk.tracks
    ADD CONSTRAINT fk_tracks_aircraft_tracks FOREIGN KEY (track) REFERENCES omsk.aircraft_tracks(track);


--
-- PostgreSQL database dump complete
--
