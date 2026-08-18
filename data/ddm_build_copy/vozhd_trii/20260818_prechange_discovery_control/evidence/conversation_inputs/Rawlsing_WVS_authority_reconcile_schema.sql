--
-- PostgreSQL database dump
--

\restrict a0H8XXMuQT9ORHjtUpfcLYMpS0ehYz7ABj3wEcmOOviqlTOexK7OETQvIurSBnZ

-- Dumped from database version 15.4
-- Dumped by pg_dump version 15.14 (Homebrew)

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
-- Name: rawlsing_authority_reconcile_ar_20260719t213835z; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA rawlsing_authority_reconcile_ar_20260719t213835z;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: canonical_question_registry; Type: TABLE; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

CREATE TABLE rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry (
    canonical_source text NOT NULL,
    canonical_wave text NOT NULL,
    canonical_var_code text NOT NULL,
    normalized_var_key text NOT NULL,
    question_id text NOT NULL,
    question_text text,
    disposition text,
    module_guess text,
    response_topology text,
    current_directional_atom_eligible boolean,
    future_topology_evidence_eligible boolean,
    allowed_as_v551_relation_evidence boolean,
    directional_certification_status text,
    authority_semantic_role text,
    authority_source_path text,
    authority_row_identity text
);


--
-- Name: cq_staging; Type: TABLE; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

CREATE TABLE rawlsing_authority_reconcile_ar_20260719t213835z.cq_staging (
    canonical_source text,
    canonical_wave text,
    canonical_var_code text,
    normalized_var_key text,
    question_id text,
    question_text text,
    disposition text,
    module_guess text,
    response_topology text,
    current_directional_atom_eligible text,
    future_topology_evidence_eligible text,
    allowed_as_v551_relation_evidence text,
    directional_certification_status text,
    authority_semantic_role text,
    authority_source_path text,
    authority_row_identity text
);


--
-- Name: question_structural_mapping_provenance; Type: TABLE; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

CREATE TABLE rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_provenance (
    raw_source text NOT NULL,
    raw_wave text NOT NULL,
    raw_var_code text NOT NULL,
    canonical_source text NOT NULL,
    canonical_wave text NOT NULL,
    canonical_var_code text NOT NULL,
    identity_match_type text NOT NULL,
    authority_source_path text,
    authority_row_identity text,
    migration_run_id text NOT NULL
);


--
-- Name: question_structural_mapping_raw; Type: TABLE; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

CREATE TABLE rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_raw (
    source text NOT NULL,
    wave text DEFAULT ''::text NOT NULL,
    question_id text NOT NULL,
    var_code text NOT NULL,
    display_text text,
    legacy_final_driver_id text,
    final_driver_label text,
    final_driver_scope text,
    final_driver_origin text,
    driver_id text,
    driver_facet_id text,
    question_block_id text,
    structural_domain_id text,
    relation_axis_id text,
    target_entity_id text,
    mapping_status text,
    evidence_kind text,
    strata_relevance text,
    channel_affordances text,
    forbidden_inference text,
    does_not_measure text,
    review_notes text,
    loaded_at timestamp with time zone DEFAULT now() NOT NULL,
    source_structure_classification text,
    question_type text,
    handling_rule text,
    source_structure_fields_joined boolean DEFAULT true
);


--
-- Name: question_variable_alias; Type: TABLE; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

CREATE TABLE rawlsing_authority_reconcile_ar_20260719t213835z.question_variable_alias (
    canonical_source text NOT NULL,
    canonical_wave text NOT NULL,
    raw_var_code text NOT NULL,
    normalized_raw_var_key text NOT NULL,
    canonical_var_code text NOT NULL,
    alias_type text NOT NULL,
    alias_basis text NOT NULL
);


--
-- Name: survey_wave_alias; Type: TABLE; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

CREATE TABLE rawlsing_authority_reconcile_ar_20260719t213835z.survey_wave_alias (
    raw_source text NOT NULL,
    raw_wave text NOT NULL,
    canonical_source text NOT NULL,
    canonical_wave text NOT NULL,
    normalized_raw_source text NOT NULL,
    normalized_raw_wave text NOT NULL,
    alias_basis text NOT NULL
);


--
-- Name: v_question_structural_mapping_canonical; Type: VIEW; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

CREATE VIEW rawlsing_authority_reconcile_ar_20260719t213835z.v_question_structural_mapping_canonical AS
 SELECT qsm.source,
    qsm.wave,
    qsm.question_id,
    qsm.var_code,
    qsm.display_text,
    qsm.legacy_final_driver_id,
    qsm.final_driver_label,
    qsm.final_driver_scope,
    qsm.final_driver_origin,
    qsm.driver_id,
    qsm.driver_facet_id,
    qsm.question_block_id,
    qsm.structural_domain_id,
    qsm.relation_axis_id,
    qsm.target_entity_id,
    qsm.mapping_status,
    qsm.evidence_kind,
    qsm.strata_relevance,
    qsm.channel_affordances,
    qsm.forbidden_inference,
    qsm.does_not_measure,
    qsm.review_notes,
    qsm.loaded_at,
    qsm.source_structure_classification,
    qsm.question_type,
    qsm.handling_rule,
    qsm.source_structure_fields_joined,
    cqr.canonical_var_code AS authority_var_code,
    cqr.question_id AS authority_question_id,
    cqr.disposition AS authority_disposition,
    cqr.authority_semantic_role,
    cqr.allowed_as_v551_relation_evidence
   FROM (rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_raw qsm
     JOIN rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry cqr ON (((qsm.source = cqr.canonical_source) AND (qsm.wave = cqr.canonical_wave) AND ((qsm.var_code = cqr.canonical_var_code) OR ((NOT (EXISTS ( SELECT 1
           FROM rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry cqr2
          WHERE ((cqr2.canonical_source = qsm.source) AND (cqr2.canonical_wave = qsm.wave) AND (cqr2.canonical_var_code = qsm.var_code))))) AND (EXISTS ( SELECT 1
           FROM rawlsing_authority_reconcile_ar_20260719t213835z.question_variable_alias qva
          WHERE ((qva.canonical_source = cqr.canonical_source) AND (qva.canonical_wave = cqr.canonical_wave) AND (qva.normalized_raw_var_key = lower(COALESCE(qsm.var_code, ''::text))) AND (qva.canonical_var_code = cqr.canonical_var_code) AND (qva.alias_type <> 'exact_identity'::text)))))))));


--
-- Name: canonical_question_registry canonical_question_registry_pkey; Type: CONSTRAINT; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

ALTER TABLE ONLY rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry
    ADD CONSTRAINT canonical_question_registry_pkey PRIMARY KEY (canonical_source, canonical_wave, canonical_var_code);


--
-- Name: question_structural_mapping_provenance question_structural_mapping_provenance_pkey; Type: CONSTRAINT; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

ALTER TABLE ONLY rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_provenance
    ADD CONSTRAINT question_structural_mapping_provenance_pkey PRIMARY KEY (raw_source, raw_wave, raw_var_code);


--
-- Name: question_structural_mapping_raw question_structural_mapping_raw_pkey; Type: CONSTRAINT; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

ALTER TABLE ONLY rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_raw
    ADD CONSTRAINT question_structural_mapping_raw_pkey PRIMARY KEY (source, wave, var_code);


--
-- Name: question_variable_alias question_variable_alias_pkey; Type: CONSTRAINT; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

ALTER TABLE ONLY rawlsing_authority_reconcile_ar_20260719t213835z.question_variable_alias
    ADD CONSTRAINT question_variable_alias_pkey PRIMARY KEY (canonical_source, canonical_wave, raw_var_code);


--
-- Name: survey_wave_alias survey_wave_alias_pkey; Type: CONSTRAINT; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

ALTER TABLE ONLY rawlsing_authority_reconcile_ar_20260719t213835z.survey_wave_alias
    ADD CONSTRAINT survey_wave_alias_pkey PRIMARY KEY (normalized_raw_source, normalized_raw_wave);


--
-- Name: question_structural_mapping_r_question_block_id_driver_face_idx; Type: INDEX; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

CREATE INDEX question_structural_mapping_r_question_block_id_driver_face_idx ON rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_raw USING btree (question_block_id, driver_facet_id);


--
-- Name: question_structural_mapping_raw_source_wave_var_code_idx; Type: INDEX; Schema: rawlsing_authority_reconcile_ar_20260719t213835z; Owner: -
--

CREATE INDEX question_structural_mapping_raw_source_wave_var_code_idx ON rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_raw USING btree (source, wave, var_code);


--
-- PostgreSQL database dump complete
--

\unrestrict a0H8XXMuQT9ORHjtUpfcLYMpS0ehYz7ABj3wEcmOOviqlTOexK7OETQvIurSBnZ
