-- Adminer 4.7.9 PostgreSQL dump

-- \connect "postgres";

DROP TABLE IF EXISTS "files";
CREATE TABLE "public"."files" (
    "patientid" integer NOT NULL,
    "pathh" character varying NOT NULL,
    "fileid" integer NOT NULL,
    "type" character varying,
    "date" character varying
) WITH (oids = false);

DROP TABLE IF EXISTS "login";
CREATE TABLE "public"."login" (
    "pw" character varying NOT NULL,
    "ownerid" integer NOT NULL,
    "log" character varying NOT NULL
) WITH (oids = false);

DROP TABLE IF EXISTS "medfile";
DROP SEQUENCE IF EXISTS medfile_fileid_seq;
CREATE SEQUENCE medfile_fileid_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."medfile" (
    "fileid" integer DEFAULT nextval('medfile_fileid_seq') NOT NULL,
    "diag" text,
    "chronic" text,
    "prescr" text,
    "compl" text NOT NULL,
    "ddate" character varying NOT NULL,
    "patientid" integer NOT NULL,
    CONSTRAINT "medfile_pkey" PRIMARY KEY ("fileid")
) WITH (oids = false);

DROP TABLE IF EXISTS "patient";
DROP SEQUENCE IF EXISTS patient_patientid_seq;
CREATE SEQUENCE patient_patientid_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."patient" (
    "sname" character varying NOT NULL,
    "fname" character varying NOT NULL,
    "pname" character varying,
    "patientid" integer DEFAULT nextval('patient_patientid_seq') NOT NULL,
    "doctorid" integer NOT NULL,
    "sex" character varying NOT NULL,
    "adr" character varying NOT NULL,
    "pol" character varying NOT NULL,
    "dob" character varying NOT NULL,
    "dod" character varying,
    "sitanx" character varying,
    "persanx" character varying,
    CONSTRAINT "patient_pkey" PRIMARY KEY ("patientid")
) WITH (oids = false);

DROP TABLE IF EXISTS "pd";
DROP SEQUENCE IF EXISTS "pd_doctorID_seq";
CREATE SEQUENCE "pd_doctorID_seq" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE;

CREATE TABLE "public"."pd" (
    "fname" character varying(50) NOT NULL,
    "doctorid" integer DEFAULT nextval('"pd_doctorID_seq"') NOT NULL,
    "dob" character varying(10) NOT NULL,
    "department" text NOT NULL,
    "sname" character varying(50) NOT NULL,
    "pname" character varying(50),
    CONSTRAINT "pd_pkey" PRIMARY KEY ("doctorid")
) WITH (oids = false);

