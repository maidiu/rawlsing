--
-- PostgreSQL database dump
--

\restrict LtCdHEzHHRfhHLI7UYmcCFQmhW1AtE6DMMfcmiNWU7dFUNLjerG7Zc5jjZSj6qF

-- Dumped from database version 15.14 (Homebrew)
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
-- Name: p3a_v27_shadow; Type: SCHEMA; Schema: -; Owner: rawlsing_p3a_owner
--

CREATE SCHEMA p3a_v27_shadow;


ALTER SCHEMA p3a_v27_shadow OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_assert_adjudication_member_partition(text); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_assert_adjudication_member_partition(p_adjudication text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE v_revision TEXT; v_missing INTEGER; v_extra INTEGER;
BEGIN
  SELECT candidate_revision_id INTO v_revision FROM p3_adjudication_decision WHERE adjudication_id=p_adjudication;
  IF NOT FOUND THEN RAISE EXCEPTION 'unknown adjudication %',p_adjudication; END IF;
  SELECT COUNT(*) INTO v_missing FROM (SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=v_revision AND membership_role='PROPOSED_MEMBER' EXCEPT SELECT member_object_id FROM p3_adjudication_member WHERE adjudication_id=p_adjudication) q;
  SELECT COUNT(*) INTO v_extra FROM (SELECT member_object_id FROM p3_adjudication_member WHERE adjudication_id=p_adjudication EXCEPT SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=v_revision AND membership_role='PROPOSED_MEMBER') q;
  IF v_missing<>0 OR v_extra<>0 THEN RAISE EXCEPTION 'adjudication member partition mismatch: missing %, extra %',v_missing,v_extra; END IF;
END $$;


ALTER FUNCTION p3a_v27_shadow.p3_assert_adjudication_member_partition(p_adjudication text) OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_assert_candidate_origin(text); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_assert_candidate_origin(p_revision text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE v_origin TEXT; v_components INTEGER; v_attachments INTEGER; v_missing INTEGER; v_extra INTEGER;
BEGIN
  SELECT candidate_origin_type INTO v_origin FROM p3_candidate_revision WHERE candidate_revision_id=p_revision;
  IF NOT FOUND THEN RAISE EXCEPTION 'unknown candidate revision %',p_revision; END IF;
  SELECT COUNT(*) INTO v_components FROM p3_candidate_component_link WHERE candidate_revision_id=p_revision;
  SELECT COUNT(*) INTO v_attachments FROM p3_candidate_attachment_projection WHERE candidate_revision_id=p_revision;
  IF v_origin IN ('STRICT_RESPONSE_COMPONENT','PROPOSITION_ONLY_SEED') THEN
    IF v_components<>1 OR v_attachments<>0 THEN RAISE EXCEPTION 'base candidate % requires exactly one component and no attachment projection: components %, attachments %', p_revision, v_components, v_attachments; END IF;
    SELECT COUNT(*) INTO v_missing FROM (
      SELECT cm.member_object_id FROM p3_component_membership cm JOIN p3_candidate_component_link cl USING(component_id) WHERE cl.candidate_revision_id=p_revision
      EXCEPT SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=p_revision AND membership_role='PROPOSED_MEMBER') q;
    SELECT COUNT(*) INTO v_extra FROM (
      SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=p_revision AND membership_role='PROPOSED_MEMBER'
      EXCEPT SELECT cm.member_object_id FROM p3_component_membership cm JOIN p3_candidate_component_link cl USING(component_id) WHERE cl.candidate_revision_id=p_revision) q;
  ELSIF v_origin='ATTACHMENT_REVIEW' THEN
    IF v_attachments<1 THEN RAISE EXCEPTION 'attachment review requires at least one attachment projection'; END IF;
    WITH expected AS (
      SELECT cm.member_object_id FROM p3_component_membership cm JOIN p3_candidate_component_link cl USING(component_id) WHERE cl.candidate_revision_id=p_revision
      UNION SELECT pp.left_subject_id FROM p3_pair_projection pp JOIN p3_candidate_attachment_projection ap USING(projection_id) WHERE ap.candidate_revision_id=p_revision
      UNION SELECT pp.right_subject_id FROM p3_pair_projection pp JOIN p3_candidate_attachment_projection ap USING(projection_id) WHERE ap.candidate_revision_id=p_revision)
    SELECT COUNT(*) INTO v_missing FROM (SELECT member_object_id FROM expected EXCEPT SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=p_revision AND membership_role='PROPOSED_MEMBER') q;
    WITH expected AS (
      SELECT cm.member_object_id FROM p3_component_membership cm JOIN p3_candidate_component_link cl USING(component_id) WHERE cl.candidate_revision_id=p_revision
      UNION SELECT pp.left_subject_id FROM p3_pair_projection pp JOIN p3_candidate_attachment_projection ap USING(projection_id) WHERE ap.candidate_revision_id=p_revision
      UNION SELECT pp.right_subject_id FROM p3_pair_projection pp JOIN p3_candidate_attachment_projection ap USING(projection_id) WHERE ap.candidate_revision_id=p_revision)
    SELECT COUNT(*) INTO v_extra FROM (SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=p_revision AND membership_role='PROPOSED_MEMBER' EXCEPT SELECT member_object_id FROM expected) q;
  ELSIF v_origin='NONCONNECTIVE_DIAGNOSTIC_CASE' THEN
    IF v_components<>0 OR v_attachments<>0 THEN RAISE EXCEPTION 'diagnostic candidate cannot borrow graph connectivity'; END IF;
    v_missing:=0;v_extra:=0;
  ELSE RAISE EXCEPTION 'unknown candidate origin %',v_origin;
  END IF;
  IF COALESCE(v_missing,0)<>0 OR COALESCE(v_extra,0)<>0 THEN RAISE EXCEPTION 'candidate origin membership mismatch: missing %, extra %',v_missing,v_extra; END IF;
END $$;


ALTER FUNCTION p3a_v27_shadow.p3_assert_candidate_origin(p_revision text) OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_assert_canonical_promotion_closure(text); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_assert_canonical_promotion_closure(p_adjudication text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE v_status TEXT; v_family TEXT; v_revision TEXT; v_missing INTEGER; v_extra INTEGER;
BEGIN
  SELECT decision_status,canonical_family_id INTO v_status,v_family FROM p3_adjudication_decision WHERE adjudication_id=p_adjudication;
  IF v_status NOT IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') THEN RETURN; END IF;
  SELECT family_revision_id INTO v_revision FROM p3_canonical_family_revision WHERE created_by_adjudication_id=p_adjudication;
  IF NOT FOUND THEN RAISE EXCEPTION 'accepted adjudication lacks canonical family revision'; END IF;
  SELECT COUNT(*) INTO v_missing FROM (SELECT member_object_id FROM p3_adjudication_member WHERE adjudication_id=p_adjudication AND member_disposition='ACCEPT' EXCEPT SELECT member_object_id FROM p3_canonical_family_membership WHERE family_revision_id=v_revision) q;
  SELECT COUNT(*) INTO v_extra FROM (SELECT member_object_id FROM p3_canonical_family_membership WHERE family_revision_id=v_revision EXCEPT SELECT member_object_id FROM p3_adjudication_member WHERE adjudication_id=p_adjudication AND member_disposition='ACCEPT') q;
  IF v_missing<>0 OR v_extra<>0 THEN RAISE EXCEPTION 'canonical membership does not equal accepted adjudication membership'; END IF;
  IF v_status='ACCEPTED_WITH_VARIANTS' AND EXISTS (SELECT 1 FROM p3_canonical_family_membership m WHERE m.family_revision_id=v_revision AND m.variant_revision_id IS NULL) THEN RAISE EXCEPTION 'accepted-with-variants member lacks canonical variant assignment'; END IF;
  IF EXISTS (SELECT 1 FROM p3_adjudication_member a WHERE a.adjudication_id=p_adjudication AND a.member_disposition='EXCLUDE' AND NOT EXISTS (SELECT 1 FROM p3_exclusion_promotion ep JOIN p3_excluded_object eo ON eo.exclusion_id=ep.canonical_exclusion_id WHERE ep.adjudication_id=p_adjudication AND eo.excluded_object_id=a.member_object_id)) THEN RAISE EXCEPTION 'excluded member lacks canonical named-exclusion promotion'; END IF;
END $$;


ALTER FUNCTION p3a_v27_shadow.p3_assert_canonical_promotion_closure(p_adjudication text) OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_assert_split_result_partition(text); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_assert_split_result_partition(p_adjudication text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE v_status TEXT; v_results INTEGER; v_missing INTEGER; v_extra INTEGER; v_duplicates INTEGER;
BEGIN
  SELECT decision_status INTO v_status FROM p3_adjudication_decision WHERE adjudication_id=p_adjudication;
  IF v_status<>'SPLIT_REQUIRED' THEN RETURN; END IF;
  SELECT COUNT(*) INTO v_results FROM p3_adjudication_split_result WHERE adjudication_id=p_adjudication;
  IF v_results<2 THEN RAISE EXCEPTION 'split decision requires at least two successor groups'; END IF;
  SELECT COUNT(*) INTO v_duplicates FROM (SELECT member_object_id FROM p3_adjudication_split_result_member WHERE adjudication_id=p_adjudication GROUP BY member_object_id HAVING COUNT(*)<>1) q;
  SELECT COUNT(*) INTO v_missing FROM (SELECT cm.member_object_id FROM p3_candidate_membership cm JOIN p3_adjudication_decision d ON d.candidate_revision_id=cm.candidate_revision_id WHERE d.adjudication_id=p_adjudication AND cm.membership_role='PROPOSED_MEMBER' EXCEPT SELECT member_object_id FROM p3_adjudication_split_result_member WHERE adjudication_id=p_adjudication) q;
  SELECT COUNT(*) INTO v_extra FROM (SELECT member_object_id FROM p3_adjudication_split_result_member WHERE adjudication_id=p_adjudication EXCEPT SELECT cm.member_object_id FROM p3_candidate_membership cm JOIN p3_adjudication_decision d ON d.candidate_revision_id=cm.candidate_revision_id WHERE d.adjudication_id=p_adjudication AND cm.membership_role='PROPOSED_MEMBER') q;
  IF v_duplicates<>0 OR v_missing<>0 OR v_extra<>0 THEN RAISE EXCEPTION 'split successor partition invalid'; END IF;
END $$;


ALTER FUNCTION p3a_v27_shadow.p3_assert_split_result_partition(p_adjudication text) OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_enforce_identity_contract(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_enforce_identity_contract() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
DECLARE c RECORD; suffix TEXT;
BEGIN
    SELECT * INTO c FROM p3_identity_key_contract WHERE object_type=NEW.object_type AND authority_release_id=NEW.allocation_release_id;
    IF c.object_type IS NULL THEN RAISE EXCEPTION 'Missing identity contract for % release %',NEW.object_type,NEW.allocation_release_id; END IF;
    IF NEW.identity_strategy<>c.identity_strategy THEN RAISE EXCEPTION 'Identity strategy mismatch for %',NEW.object_id; END IF;
    IF c.id_pattern='UPSTREAM_EXACT' THEN
        IF NEW.object_id<>NEW.idempotency_key THEN RAISE EXCEPTION 'Inherited object ID must equal exact upstream idempotency key'; END IF;
    ELSE
        IF NEW.object_id !~ ('^'||c.id_pattern||'$') THEN RAISE EXCEPTION 'Object ID % violates %',NEW.object_id,c.id_pattern; END IF;
        IF NEW.identity_strategy='CONTENT_ADDRESSED_DERIVED_ID' THEN
            IF NEW.content_hash IS NULL THEN RAISE EXCEPTION 'Content-addressed object requires full content_hash'; END IF;
            suffix:=split_part(NEW.object_id,'-',2);
            IF suffix<>substr(NEW.content_hash,1,16) THEN RAISE EXCEPTION 'Content ID prefix does not match full hash'; END IF;
        END IF;
    END IF;
    RETURN NEW;
END; $_$;


ALTER FUNCTION p3a_v27_shadow.p3_enforce_identity_contract() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_enforce_object_reference_type(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE v_column TEXT := TG_ARGV[0]; v_allowed TEXT[] := string_to_array(TG_ARGV[1], '|'); v_object_id TEXT; v_actual TEXT;
BEGIN
    v_object_id := to_jsonb(NEW) ->> v_column;
    IF v_object_id IS NULL THEN RETURN NEW; END IF;
    SELECT object_type INTO v_actual FROM p3_object_registry WHERE object_id=v_object_id;
    IF v_actual IS NULL OR NOT (v_actual = ANY(v_allowed)) THEN
        RAISE EXCEPTION 'Invalid P3 object type %.%=% actual=% allowed=%', TG_TABLE_NAME, v_column, v_object_id, v_actual, v_allowed;
    END IF;
    RETURN NEW;
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_enforce_vocab_code(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE v_domain TEXT := TG_ARGV[0]; v_column TEXT := TG_ARGV[1]; v_value TEXT;
BEGIN
    v_value := to_jsonb(NEW) ->> v_column;
    IF v_value IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM p3_vocabulary_revision c
        WHERE c.vocabulary_domain=v_domain AND c.code=v_value
          AND c.authority_release_id=TG_ARGV[2] AND NOT c.deprecated
    ) THEN
        RAISE EXCEPTION 'Unknown P3 vocabulary code %.%=%', TG_TABLE_NAME, v_column, v_value;
    END IF;
    RETURN NEW;
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_enforce_vocab_code() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_forbid_update_delete(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_forbid_update_delete() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RAISE EXCEPTION 'P3 append-only authority table % rejects %', TG_TABLE_NAME, TG_OP;
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_forbid_update_delete() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_guard_object_registry_mutation(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_guard_object_registry_mutation() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF TG_OP='DELETE' THEN RAISE EXCEPTION 'P3 object registry is append-only'; END IF;
    IF NEW.object_id IS DISTINCT FROM OLD.object_id OR NEW.object_type IS DISTINCT FROM OLD.object_type OR NEW.identity_strategy IS DISTINCT FROM OLD.identity_strategy
       OR NEW.idempotency_key IS DISTINCT FROM OLD.idempotency_key OR NEW.origin_phase IS DISTINCT FROM OLD.origin_phase OR NEW.origin_authority_id IS DISTINCT FROM OLD.origin_authority_id
       OR NEW.allocation_release_id IS DISTINCT FROM OLD.allocation_release_id OR NEW.content_hash IS DISTINCT FROM OLD.content_hash OR NEW.stable_identity_note IS DISTINCT FROM OLD.stable_identity_note
       OR (OLD.retired_release_id IS NOT NULL AND NEW.retired_release_id IS DISTINCT FROM OLD.retired_release_id) THEN
        RAISE EXCEPTION 'P3 object identity-bearing fields are immutable';
    END IF;
    RETURN NEW;
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_guard_object_registry_mutation() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_install_contract_triggers(text); Type: PROCEDURE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE PROCEDURE p3a_v27_shadow.p3_install_contract_triggers(IN p_release_id text)
    LANGUAGE plpgsql
    AS $$
DECLARE r RECORD; tname TEXT;
BEGIN
    FOR r IN SELECT table_name,column_name,vocabulary_domain FROM p3_categorical_field_binding WHERE authority_release_id=p_release_id LOOP
        tname := 'p3_vocab_'||substr(md5(r.table_name||'.'||r.column_name),1,16);
        EXECUTE format('DROP TRIGGER IF EXISTS %I ON %I',tname,r.table_name);
        EXECUTE format('CREATE TRIGGER %I BEFORE INSERT OR UPDATE OF %I ON %I FOR EACH ROW EXECUTE FUNCTION p3_enforce_vocab_code(%L,%L,%L)',tname,r.column_name,r.table_name,r.vocabulary_domain,r.column_name,p_release_id);
    END LOOP;
    FOR r IN SELECT table_name,column_name,array_to_string(allowed_object_types,'|') allowed FROM p3_object_reference_type_contract WHERE authority_release_id=p_release_id LOOP
        tname := 'p3_type_'||substr(md5(r.table_name||'.'||r.column_name),1,16);
        EXECUTE format('DROP TRIGGER IF EXISTS %I ON %I',tname,r.table_name);
        EXECUTE format('CREATE TRIGGER %I BEFORE INSERT OR UPDATE OF %I ON %I FOR EACH ROW EXECUTE FUNCTION p3_enforce_object_reference_type(%L,%L)',tname,r.column_name,r.table_name,r.column_name,r.allowed);
    END LOOP;
END; $$;


ALTER PROCEDURE p3a_v27_shadow.p3_install_contract_triggers(IN p_release_id text) OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_adjudication_closure_deferred(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_adjudication_closure_deferred() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE aid TEXT;
BEGIN
  IF TG_TABLE_NAME='p3_canonical_family_membership' THEN
    SELECT created_by_adjudication_id INTO aid
      FROM p3_canonical_family_revision
     WHERE family_revision_id=COALESCE(NEW.family_revision_id,OLD.family_revision_id);
  ELSE
    aid:=COALESCE(NEW.adjudication_id,OLD.adjudication_id);
  END IF;
  IF aid IS NOT NULL AND EXISTS (SELECT 1 FROM p3_adjudication_decision WHERE adjudication_id=aid) THEN
    PERFORM p3_assert_adjudication_member_partition(aid);
    PERFORM p3_assert_split_result_partition(aid);
    PERFORM p3_assert_canonical_promotion_closure(aid);
  END IF;
  RETURN COALESCE(NEW,OLD);
END $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_adjudication_closure_deferred() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_adjudication_completeness(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_adjudication_completeness() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE aid TEXT; a RECORD; n INTEGER; bad INTEGER; prior TEXT;
BEGIN
    aid:=COALESCE(NEW.adjudication_id,OLD.adjudication_id);
    SELECT * INTO a FROM p3_adjudication_decision WHERE adjudication_id=aid;
    IF a.adjudication_id IS NULL THEN RETURN COALESCE(NEW,OLD); END IF;
    IF a.decision_ordinal=1 AND a.supersedes_adjudication_id IS NOT NULL THEN RAISE EXCEPTION 'First decision cannot supersede another'; END IF;
    IF a.decision_ordinal>1 THEN
      SELECT adjudication_id INTO prior FROM p3_adjudication_decision WHERE candidate_revision_id=a.candidate_revision_id AND decision_ordinal=a.decision_ordinal-1;
      IF prior IS NULL OR a.supersedes_adjudication_id IS DISTINCT FROM prior THEN RAISE EXCEPTION 'Decision supersession chain is not exact'; END IF;
    END IF;
    IF a.decision_status IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') THEN
      SELECT COUNT(*) INTO n FROM p3_adjudication_member WHERE adjudication_id=aid AND member_disposition='ACCEPT';
      IF n<2 THEN RAISE EXCEPTION 'Accepted decision requires at least two accepted members'; END IF;
    END IF;
    IF a.decision_status='ACCEPTED_WITH_VARIANTS' AND NOT EXISTS (SELECT 1 FROM p3_adjudication_member WHERE adjudication_id=aid AND member_disposition='ACCEPT' AND variant_revision_id IS NOT NULL) THEN RAISE EXCEPTION 'Variant acceptance requires variant assignment'; END IF;
    IF a.decision_status='SPLIT_REQUIRED' AND NOT EXISTS (SELECT 1 FROM p3_adjudication_split_point WHERE adjudication_id=aid) THEN RAISE EXCEPTION 'Split decision requires split point'; END IF;
    IF a.decision_status='HIERARCHICAL_RELATION_ONLY' AND NOT EXISTS (SELECT 1 FROM p3_adjudication_hierarchy_relation WHERE adjudication_id=aid) THEN RAISE EXCEPTION 'Hierarchy decision requires hierarchy row'; END IF;
    IF a.decision_status IN ('BLOCKED_UNRESOLVED','INSUFFICIENT_AUTHORITY') AND NOT EXISTS (SELECT 1 FROM p3_adjudication_unresolved_boundary WHERE adjudication_id=aid) THEN RAISE EXCEPTION 'Blocked decision requires unresolved boundary'; END IF;
    RETURN COALESCE(NEW,OLD);
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_adjudication_completeness() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_candidate_origin_deferred(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_candidate_origin_deferred() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE rid TEXT;
BEGIN
  rid:=COALESCE(NEW.candidate_revision_id,OLD.candidate_revision_id);
  IF rid IS NOT NULL AND EXISTS (SELECT 1 FROM p3_candidate_revision WHERE candidate_revision_id=rid) THEN PERFORM p3_assert_candidate_origin(rid); END IF;
  RETURN COALESCE(NEW,OLD);
END $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_candidate_origin_deferred() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_candidate_status_event(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_candidate_status_event() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE p_stage TEXT; p_ord INTEGER; revision_family TEXT; revision_release TEXT;
BEGIN
    SELECT candidate_family_id,authority_release_id INTO revision_family,revision_release FROM p3_candidate_revision WHERE candidate_revision_id=NEW.candidate_revision_id;
    IF revision_family IS DISTINCT FROM NEW.candidate_family_id OR revision_release IS DISTINCT FROM NEW.authority_release_id THEN RAISE EXCEPTION 'Candidate event revision/family/release mismatch'; END IF;
    SELECT to_stage,event_ordinal INTO p_stage,p_ord FROM p3_candidate_status_event WHERE candidate_revision_id=NEW.candidate_revision_id ORDER BY event_ordinal DESC LIMIT 1;
    IF p_ord IS NULL THEN
        IF NEW.event_ordinal<>1 OR NEW.from_stage IS NOT NULL OR NEW.to_stage<>'DISCOVERED' THEN RAISE EXCEPTION 'Invalid first candidate revision event'; END IF;
    ELSE
        IF NEW.event_ordinal<>p_ord+1 OR NEW.from_stage IS DISTINCT FROM p_stage THEN RAISE EXCEPTION 'Noncontiguous candidate revision event'; END IF;
        IF NOT EXISTS (SELECT 1 FROM p3_candidate_lifecycle_transition t WHERE t.from_stage=NEW.from_stage AND t.to_stage=NEW.to_stage AND t.authority_release_id=NEW.authority_release_id) THEN RAISE EXCEPTION 'Disallowed candidate transition % -> %',NEW.from_stage,NEW.to_stage; END IF;
    END IF;
    RETURN NEW;
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_candidate_status_event() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_component_closure(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_component_closure() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE cid TEXT; c RECORD; mn INTEGER; en INTEGER; bad INTEGER;
BEGIN
    cid:=COALESCE(NEW.component_id,OLD.component_id);
    SELECT * INTO c FROM p3_candidate_component WHERE component_id=cid;
    IF c.component_id IS NULL THEN RETURN COALESCE(NEW,OLD); END IF;
    SELECT COUNT(*) INTO mn FROM p3_component_membership WHERE component_id=cid;
    SELECT COUNT(*) INTO en FROM p3_component_connectivity_edge WHERE component_id=cid;
    IF mn<>c.member_count OR en<>c.connectivity_edge_count THEN RAISE EXCEPTION 'Component % stored counts do not reconcile',cid; END IF;
    SELECT COUNT(*) INTO bad
      FROM p3_component_connectivity_edge e
      JOIN p3_pair_projection pr ON pr.projection_id=e.projection_id
      JOIN p3_pair_fact_bundle pf ON pf.pair_fact_id=pr.pair_fact_id
     WHERE e.component_id=cid AND (
       (c.component_type='STRICT_RESPONSE_COMPONENT' AND pf.relation_type<>'PROPOSITION_RESPONSE_IDENTITY')
       OR (c.component_type='PROPOSITION_ONLY_COMPONENT' AND pf.relation_type<>'PROPOSITION_IDENTITY_ONLY')
       OR NOT pf.proposition_graph_allowed
       OR e.authority_release_id<>c.authority_release_id OR pr.authority_release_id<>c.authority_release_id OR pf.authority_release_id<>c.authority_release_id
       OR NOT EXISTS (SELECT 1 FROM p3_component_membership m WHERE m.component_id=cid AND m.member_object_id=pr.left_subject_id)
       OR NOT EXISTS (SELECT 1 FROM p3_component_membership m WHERE m.component_id=cid AND m.member_object_id=pr.right_subject_id));
    IF bad<>0 THEN RAISE EXCEPTION 'Component % contains invalid projected connectivity edges',cid; END IF;
    RETURN COALESCE(NEW,OLD);
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_component_closure() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_genealogy_cardinality(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_genealogy_cardinality() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE gid TEXT; g RECORD; pred INTEGER; succ INTEGER; overlap INTEGER;
BEGIN
    gid:=COALESCE(NEW.genealogy_id,OLD.genealogy_id); SELECT * INTO g FROM p3_family_genealogy WHERE genealogy_id=gid;
    IF g.genealogy_id IS NULL THEN RETURN COALESCE(NEW,OLD); END IF;
    SELECT COUNT(*) FILTER(WHERE genealogy_role='PREDECESSOR'),COUNT(*) FILTER(WHERE genealogy_role='SUCCESSOR') INTO pred,succ FROM p3_family_genealogy_member WHERE genealogy_id=gid;
    SELECT COUNT(*) INTO overlap FROM p3_family_genealogy_member p JOIN p3_family_genealogy_member q USING(genealogy_id,family_id) WHERE p.genealogy_id=gid AND p.genealogy_role='PREDECESSOR' AND q.genealogy_role='SUCCESSOR';
    IF overlap<>0 OR (g.relation_type='SPLIT' AND NOT(pred=1 AND succ>=2)) OR (g.relation_type='MERGE' AND NOT(pred>=2 AND succ=1))
       OR (g.relation_type='SUPERSEDE' AND NOT(pred>=1 AND succ>=1)) OR (g.relation_type='DEPRECATE' AND NOT(pred>=1 AND succ=0)) THEN RAISE EXCEPTION 'Genealogy % cardinality invalid',gid; END IF;
    RETURN COALESCE(NEW,OLD);
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_genealogy_cardinality() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_hyperedge_cardinality(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_hyperedge_cardinality() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE hid TEXT:=COALESCE(NEW.hyperedge_id,OLD.hyperedge_id); h RECORD; c RECORD; n INTEGER;
BEGIN
    SELECT hyperedge_type,authority_release_id INTO h FROM p3_hyperedge WHERE hyperedge_id=hid;
    IF h.hyperedge_type IS NULL THEN RETURN COALESCE(NEW,OLD); END IF;
    FOR c IN SELECT * FROM p3_hyperedge_role_type_contract WHERE hyperedge_type=h.hyperedge_type AND authority_release_id=h.authority_release_id LOOP
        SELECT COUNT(*) INTO n FROM p3_hyperedge_membership WHERE hyperedge_id=hid AND participant_role=c.participant_role;
        IF n<c.minimum_count OR (c.maximum_count IS NOT NULL AND n>c.maximum_count) THEN RAISE EXCEPTION 'Hyperedge % role % cardinality % outside [%..%]',hid,c.participant_role,n,c.minimum_count,c.maximum_count; END IF;
    END LOOP;
    IF TG_OP='DELETE' THEN RETURN OLD; ELSE RETURN NEW; END IF;
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_hyperedge_cardinality() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_hyperedge_member_type(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_hyperedge_member_type() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE h RECORD; c RECORD; actual TEXT;
BEGIN
    SELECT hyperedge_type,authority_effect,authority_release_id INTO h FROM p3_hyperedge WHERE hyperedge_id=NEW.hyperedge_id;
    SELECT * INTO c FROM p3_hyperedge_role_type_contract WHERE hyperedge_type=h.hyperedge_type AND participant_role=NEW.participant_role AND authority_release_id=h.authority_release_id;
    SELECT object_type INTO actual FROM p3_object_registry WHERE object_id=NEW.object_id;
    IF c.hyperedge_type IS NULL OR NOT(actual=ANY(c.allowed_object_types)) OR h.authority_effect<>c.authority_effect_ceiling THEN
        RAISE EXCEPTION 'Invalid hyperedge participant %, role %, type %, effect %',NEW.object_id,NEW.participant_role,actual,h.authority_effect;
    END IF;
    RETURN NEW;
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_hyperedge_member_type() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_internal_pair_closure(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_internal_pair_closure() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE rid TEXT; members INTEGER; pairs INTEGER; bad INTEGER;
BEGIN
    rid:=COALESCE(NEW.candidate_revision_id,OLD.candidate_revision_id);
    SELECT COUNT(*) INTO members FROM p3_candidate_membership WHERE candidate_revision_id=rid AND membership_role='PROPOSED_MEMBER';
    SELECT COUNT(*) INTO pairs FROM p3_internal_pair_matrix WHERE candidate_revision_id=rid;
    IF members>=2 AND pairs<>(members*(members-1))/2 THEN RAISE EXCEPTION 'Candidate % pair matrix incomplete',rid; END IF;
    SELECT COUNT(*) INTO bad
      FROM p3_internal_pair_matrix x
      LEFT JOIN p3_pair_projection pr ON pr.projection_id=x.direct_pair_projection_id
      LEFT JOIN p3_pair_fact_bundle pf ON pf.pair_fact_id=pr.pair_fact_id
     WHERE x.candidate_revision_id=rid AND (
       NOT EXISTS (SELECT 1 FROM p3_candidate_membership m WHERE m.candidate_revision_id=rid AND m.member_object_id=x.left_object_id AND m.membership_role='PROPOSED_MEMBER')
       OR NOT EXISTS (SELECT 1 FROM p3_candidate_membership m WHERE m.candidate_revision_id=rid AND m.member_object_id=x.right_object_id AND m.membership_role='PROPOSED_MEMBER')
       OR (x.pair_state IN ('DIRECT_POSITIVE','DIRECT_COLLISION','DIRECT_UNRESOLVED','HIERARCHICAL_ONLY') AND x.direct_pair_projection_id IS NULL)
       OR (x.direct_pair_projection_id IS NOT NULL AND NOT ((pr.left_subject_id=x.left_object_id AND pr.right_subject_id=x.right_object_id) OR (pr.left_subject_id=x.right_object_id AND pr.right_subject_id=x.left_object_id)))
       OR (x.pair_state='DIRECT_POSITIVE' AND pf.relation_type NOT IN ('PROPOSITION_RESPONSE_IDENTITY','PROPOSITION_IDENTITY_ONLY'))
       OR (x.pair_state='DIRECT_COLLISION' AND pf.relation_type NOT IN ('EXPLICIT_NEGATIVE','REDIRECT_OTHER_DOMAIN'))
       OR (x.pair_state='DIRECT_UNRESOLVED' AND pf.relation_type<>'UNRESOLVED')
       OR (x.pair_state='HIERARCHICAL_ONLY' AND pf.relation_type NOT IN ('NESTED_TARGET_RELATION','CONSTRUCT_COORDINATE')));
    IF bad<>0 THEN RAISE EXCEPTION 'Candidate % pair rows violate member, projection, endpoint, or state/fact compatibility',rid; END IF;
    RETURN COALESCE(NEW,OLD);
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_internal_pair_closure() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_pair_endpoint_resolution(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_pair_endpoint_resolution() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE pf TEXT; side TEXT; r RECORD; expected TEXT; n INTEGER; bad INTEGER;
BEGIN
    pf:=COALESCE(NEW.pair_fact_id,OLD.pair_fact_id); side:=COALESCE(NEW.endpoint_side,OLD.endpoint_side);
    SELECT * INTO r FROM p3_pair_endpoint_resolution WHERE pair_fact_id=pf AND endpoint_side=side;
    IF r.pair_fact_id IS NULL THEN RETURN COALESCE(NEW,OLD); END IF;
    SELECT CASE WHEN side='LEFT' THEN left_object_id ELSE right_object_id END INTO expected FROM p3_pair_fact_bundle WHERE pair_fact_id=pf;
    IF r.original_lineage_id IS DISTINCT FROM expected THEN RAISE EXCEPTION 'Pair endpoint original lineage mismatch'; END IF;
    SELECT COUNT(*) INTO n FROM p3_pair_endpoint_resolved_subject WHERE pair_fact_id=pf AND endpoint_side=side;
    IF r.resolution_status='ORIGINAL_LINEAGE' AND (n<>1 OR NOT EXISTS (SELECT 1 FROM p3_pair_endpoint_resolved_subject WHERE pair_fact_id=pf AND endpoint_side=side AND resolved_subject_id=r.original_lineage_id)) THEN RAISE EXCEPTION 'Original-lineage resolution must retain exactly the original lineage'; END IF;
    IF r.resolution_status='SEGMENT_BOUND' THEN
      IF n<1 THEN RAISE EXCEPTION 'Segment-bound resolution requires at least one segment'; END IF;
      SELECT COUNT(*) INTO bad FROM p3_pair_endpoint_resolved_subject x LEFT JOIN p3_lineage_segment sg ON sg.segment_id=x.resolved_subject_id
        WHERE x.pair_fact_id=pf AND x.endpoint_side=side AND sg.parent_lineage_id IS DISTINCT FROM r.original_lineage_id;
      IF bad<>0 THEN RAISE EXCEPTION 'Resolved segment is not a child of original lineage'; END IF;
    END IF;
    IF r.resolution_status IN ('BLOCKED_HETEROGENEOUS','FAIL_CLOSED_UNRESOLVED') AND n<>0 THEN RAISE EXCEPTION 'Blocked endpoint cannot expose resolved subjects'; END IF;
    RETURN COALESCE(NEW,OLD);
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_pair_endpoint_resolution() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_pair_projection(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_pair_projection() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE v_left TEXT; v_right TEXT; v_ls TEXT; v_rs TEXT;
BEGIN
  SELECT left_object_id,right_object_id INTO v_left,v_right FROM p3_pair_fact_bundle WHERE pair_fact_id=NEW.pair_fact_id;
  IF NOT FOUND THEN RAISE EXCEPTION 'unknown pair fact %',NEW.pair_fact_id; END IF;
  IF NEW.left_subject_id=NEW.right_subject_id THEN RAISE EXCEPTION 'pair projection endpoints must differ'; END IF;
  IF NOT EXISTS (SELECT 1 FROM p3_pair_endpoint_resolved_subject WHERE pair_fact_id=NEW.pair_fact_id AND endpoint_side='LEFT' AND resolved_subject_id=NEW.left_subject_id) THEN
    RAISE EXCEPTION 'left subject % is not an authorized endpoint resolution',NEW.left_subject_id;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM p3_pair_endpoint_resolved_subject WHERE pair_fact_id=NEW.pair_fact_id AND endpoint_side='RIGHT' AND resolved_subject_id=NEW.right_subject_id) THEN
    RAISE EXCEPTION 'right subject % is not an authorized endpoint resolution',NEW.right_subject_id;
  END IF;
  SELECT resolution_status INTO v_ls FROM p3_pair_endpoint_resolution WHERE pair_fact_id=NEW.pair_fact_id AND endpoint_side='LEFT';
  SELECT resolution_status INTO v_rs FROM p3_pair_endpoint_resolution WHERE pair_fact_id=NEW.pair_fact_id AND endpoint_side='RIGHT';
  IF NEW.projection_basis='ORIGINAL_LINEAGES' AND (NEW.left_subject_id<>v_left OR NEW.right_subject_id<>v_right OR v_ls<>'ORIGINAL_LINEAGE' OR v_rs<>'ORIGINAL_LINEAGE') THEN
    RAISE EXCEPTION 'ORIGINAL_LINEAGES projection must use both original lineage endpoints';
  END IF;
  IF NEW.projection_basis='SEGMENT_BINDING' AND v_ls='ORIGINAL_LINEAGE' AND v_rs='ORIGINAL_LINEAGE' THEN
    RAISE EXCEPTION 'SEGMENT_BINDING requires at least one governed segment-bound endpoint';
  END IF;
  RETURN NEW;
END $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_pair_projection() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_promotion_pointer(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_promotion_pointer() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE latest_status TEXT;
BEGIN
    SELECT status INTO latest_status FROM p3_release_status_event WHERE release_id=NEW.promoted_release_id ORDER BY event_ordinal DESC LIMIT 1;
    IF latest_status IS DISTINCT FROM 'PROMOTED' THEN RAISE EXCEPTION 'Promotion pointer requires latest PROMOTED event, got %',latest_status; END IF;
    RETURN NEW;
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_promotion_pointer() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_release_status_event(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_release_status_event() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE p_status TEXT; p_ord INTEGER;
BEGIN
    SELECT status,event_ordinal INTO p_status,p_ord FROM p3_release_status_event WHERE release_id=NEW.release_id ORDER BY event_ordinal DESC LIMIT 1;
    IF p_ord IS NULL THEN
        IF NEW.event_ordinal<>1 OR NEW.status<>'DRAFT' THEN RAISE EXCEPTION 'Invalid first release event'; END IF;
    ELSE
        IF NEW.event_ordinal<>p_ord+1 THEN RAISE EXCEPTION 'Noncontiguous release event'; END IF;
        IF NOT EXISTS (SELECT 1 FROM p3_release_lifecycle_transition t WHERE t.from_status=p_status AND t.to_status=NEW.status AND t.authority_release_id=NEW.release_id) THEN RAISE EXCEPTION 'Disallowed release transition % -> %',p_status,NEW.status; END IF;
    END IF;
    RETURN NEW;
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_release_status_event() OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_validate_segment_membership(); Type: FUNCTION; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE FUNCTION p3a_v27_shadow.p3_validate_segment_membership() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE sid TEXT; parent TEXT; bad INTEGER; n INTEGER;
BEGIN
    sid:=COALESCE(NEW.segment_id,OLD.segment_id); SELECT parent_lineage_id INTO parent FROM p3_lineage_segment WHERE segment_id=sid;
    IF parent IS NULL THEN RETURN COALESCE(NEW,OLD); END IF;
    SELECT COUNT(*) INTO n FROM p3_lineage_segment_member WHERE segment_id=sid;
    IF n<1 THEN RAISE EXCEPTION 'Segment % requires at least one implementation',sid; END IF;
    SELECT COUNT(*) INTO bad FROM p3_lineage_segment_member m WHERE m.segment_id=sid AND NOT EXISTS
      (SELECT 1 FROM p3_imported_lineage_membership i WHERE i.lineage_id=parent AND i.implementation_id=m.implementation_id);
    IF bad<>0 THEN RAISE EXCEPTION 'Segment % contains implementation outside parent lineage',sid; END IF;
    RETURN COALESCE(NEW,OLD);
END; $$;


ALTER FUNCTION p3a_v27_shadow.p3_validate_segment_membership() OWNER TO rawlsing_p3a_owner;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: p3_adjudication_collision_disposition; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_adjudication_collision_disposition (
    adjudication_id text NOT NULL,
    collision_id text NOT NULL,
    disposition text NOT NULL,
    rationale text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_adjudication_collision_disposition OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_adjudication_decision; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_adjudication_decision (
    adjudication_id text NOT NULL,
    candidate_revision_id text NOT NULL,
    decision_ordinal integer NOT NULL,
    decision_status text NOT NULL,
    canonical_family_id text,
    canonical_proposition jsonb,
    response_portability_status text DEFAULT 'NOT_AUTHORIZED_BY_P3'::text NOT NULL,
    rationale text NOT NULL,
    evidence_bundle_hash character(64) NOT NULL,
    supersedes_adjudication_id text,
    authority_release_id text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    CONSTRAINT p3_adjudication_decision_decision_ordinal_check CHECK ((decision_ordinal >= 1)),
    CONSTRAINT p3_adjudication_decision_decision_status_check CHECK ((decision_status = ANY (ARRAY['ACCEPTED_CANONICAL'::text, 'ACCEPTED_WITH_VARIANTS'::text, 'SPLIT_REQUIRED'::text, 'HIERARCHICAL_RELATION_ONLY'::text, 'BLOCKED_UNRESOLVED'::text, 'INSUFFICIENT_AUTHORITY'::text, 'REJECTED_SEMANTIC_ARTIFACT'::text, 'REJECTED'::text]))),
    CONSTRAINT p3_adjudication_decision_evidence_bundle_hash_check CHECK ((evidence_bundle_hash ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT p3_adjudication_decision_response_portability_status_check CHECK ((response_portability_status = 'NOT_AUTHORIZED_BY_P3'::text)),
    CONSTRAINT p3_adjudication_status_fields CHECK ((((decision_status = ANY (ARRAY['ACCEPTED_CANONICAL'::text, 'ACCEPTED_WITH_VARIANTS'::text])) AND (canonical_family_id IS NOT NULL) AND (canonical_proposition IS NOT NULL)) OR ((decision_status <> ALL (ARRAY['ACCEPTED_CANONICAL'::text, 'ACCEPTED_WITH_VARIANTS'::text])) AND (canonical_family_id IS NULL) AND (canonical_proposition IS NULL))))
);


ALTER TABLE p3a_v27_shadow.p3_adjudication_decision OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_adjudication_hierarchy_relation; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_adjudication_hierarchy_relation (
    adjudication_id text NOT NULL,
    broader_object_id text NOT NULL,
    narrower_object_id text NOT NULL,
    relation_role text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_adjudication_hierarchy_relation OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_adjudication_member; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_adjudication_member (
    adjudication_id text NOT NULL,
    member_object_id text NOT NULL,
    member_disposition text NOT NULL,
    variant_revision_id text,
    CONSTRAINT p3_adjudication_member_member_disposition_check CHECK ((member_disposition = ANY (ARRAY['ACCEPT'::text, 'EXCLUDE'::text, 'HIERARCHICAL'::text, 'UNRESOLVED'::text, 'SPLIT'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_adjudication_member OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_adjudication_split_member; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_adjudication_split_member (
    adjudication_id text NOT NULL,
    split_ordinal integer NOT NULL,
    split_side text NOT NULL,
    member_object_id text NOT NULL,
    CONSTRAINT p3_adjudication_split_member_split_side_check CHECK ((split_side = ANY (ARRAY['LEFT'::text, 'RIGHT'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_adjudication_split_member OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_adjudication_split_point; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_adjudication_split_point (
    adjudication_id text NOT NULL,
    split_ordinal integer NOT NULL,
    dimension text NOT NULL,
    rationale text NOT NULL,
    CONSTRAINT p3_adjudication_split_point_split_ordinal_check CHECK ((split_ordinal >= 1))
);


ALTER TABLE p3a_v27_shadow.p3_adjudication_split_point OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_adjudication_split_result; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_adjudication_split_result (
    adjudication_id text NOT NULL,
    result_ordinal integer NOT NULL,
    successor_candidate_family_id text NOT NULL,
    successor_origin_key character(64) NOT NULL,
    rationale text NOT NULL,
    CONSTRAINT p3_adjudication_split_result_result_ordinal_check CHECK ((result_ordinal >= 1)),
    CONSTRAINT p3_adjudication_split_result_successor_origin_key_check CHECK (((successor_origin_key ~ '^[0-9a-f]{64}$'::text) AND (successor_origin_key !~ '^0{64}$'::text)))
);


ALTER TABLE p3a_v27_shadow.p3_adjudication_split_result OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_adjudication_split_result_member; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_adjudication_split_result_member (
    adjudication_id text NOT NULL,
    result_ordinal integer NOT NULL,
    member_object_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_adjudication_split_result_member OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_adjudication_unresolved_boundary; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_adjudication_unresolved_boundary (
    adjudication_id text NOT NULL,
    boundary_id text NOT NULL,
    left_object_id text NOT NULL,
    right_object_id text NOT NULL,
    reason text NOT NULL,
    status text NOT NULL,
    CONSTRAINT p3_adjudication_unresolved_boundary_check CHECK ((left_object_id < right_object_id)),
    CONSTRAINT p3_adjudication_unresolved_boundary_status_check CHECK ((status = ANY (ARRAY['OPEN'::text, 'FAIL_CLOSED'::text, 'RESOLVED_ACCEPT'::text, 'RESOLVED_EXCLUDE'::text, 'RESOLVED_SPLIT'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_adjudication_unresolved_boundary OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_authority_release; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_authority_release (
    release_id text NOT NULL,
    parent_release_id text,
    schema_version text NOT NULL,
    builder_version text NOT NULL,
    input_manifest_hash character(64) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    object_counts jsonb DEFAULT '{}'::jsonb NOT NULL,
    validation_return_hash character(64) NOT NULL,
    migration_artifact text,
    rollback_artifact text,
    CONSTRAINT p3_authority_release_check CHECK (((parent_release_id IS NULL) OR (parent_release_id <> release_id))),
    CONSTRAINT p3_authority_release_input_manifest_hash_check CHECK ((input_manifest_hash ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT p3_authority_release_validation_return_hash_check CHECK ((validation_return_hash ~ '^[0-9a-f]{64}$'::text))
);


ALTER TABLE p3a_v27_shadow.p3_authority_release OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_candidate_attachment_projection; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_candidate_attachment_projection (
    candidate_revision_id text NOT NULL,
    projection_id text NOT NULL,
    attachment_role text NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_candidate_attachment_projection_attachment_role_check CHECK ((attachment_role = ANY (ARRAY['ORPHAN_ATTACHMENT'::text, 'STRICT_COMPONENT_BRIDGE'::text, 'SEED_TO_STRICT_BRIDGE'::text, 'ATTACHMENT_GROUP_CONNECTOR'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_candidate_attachment_projection OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_candidate_component; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_candidate_component (
    component_id text NOT NULL,
    component_type text NOT NULL,
    build_rule_version text NOT NULL,
    content_hash character(64) NOT NULL,
    connectivity_edge_count integer NOT NULL,
    member_count integer NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_candidate_component_component_type_check CHECK ((component_type = ANY (ARRAY['STRICT_RESPONSE_COMPONENT'::text, 'PROPOSITION_ONLY_COMPONENT'::text]))),
    CONSTRAINT p3_candidate_component_connectivity_edge_count_check CHECK ((connectivity_edge_count >= 1)),
    CONSTRAINT p3_candidate_component_content_hash_check CHECK ((content_hash ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT p3_candidate_component_member_count_check CHECK ((member_count >= 2))
);


ALTER TABLE p3a_v27_shadow.p3_candidate_component OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_candidate_component_link; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_candidate_component_link (
    candidate_revision_id text NOT NULL,
    component_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_candidate_component_link OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_candidate_diagnostic_flag; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_candidate_diagnostic_flag (
    candidate_revision_id text NOT NULL,
    flag text NOT NULL,
    evidence_ids jsonb DEFAULT '[]'::jsonb NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_candidate_diagnostic_flag OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_candidate_family; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_candidate_family (
    candidate_family_id text NOT NULL,
    created_release_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_candidate_family OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_candidate_lifecycle_transition; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_candidate_lifecycle_transition (
    from_stage text,
    to_stage text NOT NULL,
    guard_text text NOT NULL,
    authority_release_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_candidate_lifecycle_transition OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_candidate_membership; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_candidate_membership (
    candidate_revision_id text NOT NULL,
    member_object_id text NOT NULL,
    membership_role text NOT NULL,
    membership_basis text NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_candidate_membership_membership_basis_check CHECK ((membership_basis = ANY (ARRAY['COMPONENT_MEMBER'::text, 'ATTACHMENT_PROJECTION'::text, 'DIRECT_DIAGNOSTIC'::text, 'HIERARCHICAL_CONTEXT'::text]))),
    CONSTRAINT p3_candidate_membership_membership_role_check CHECK ((membership_role = ANY (ARRAY['PROPOSED_MEMBER'::text, 'PROPOSED_HIERARCHICAL_CONTEXT'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_candidate_membership OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_candidate_ranking; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_candidate_ranking (
    candidate_revision_id text NOT NULL,
    primary_class_rank integer NOT NULL,
    hard_collision_count integer NOT NULL,
    open_obligation_count integer NOT NULL,
    signature_completeness numeric NOT NULL,
    source_count integer NOT NULL,
    lineage_count integer NOT NULL,
    direct_positive_density numeric NOT NULL,
    structure_support_count integer NOT NULL,
    response_variant_complexity integer NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_candidate_ranking_direct_positive_density_check CHECK (((direct_positive_density >= (0)::numeric) AND (direct_positive_density <= (1)::numeric))),
    CONSTRAINT p3_candidate_ranking_hard_collision_count_check CHECK ((hard_collision_count >= 0)),
    CONSTRAINT p3_candidate_ranking_lineage_count_check CHECK ((lineage_count >= 2)),
    CONSTRAINT p3_candidate_ranking_open_obligation_count_check CHECK ((open_obligation_count >= 0)),
    CONSTRAINT p3_candidate_ranking_primary_class_rank_check CHECK ((primary_class_rank >= 0)),
    CONSTRAINT p3_candidate_ranking_response_variant_complexity_check CHECK ((response_variant_complexity >= 0)),
    CONSTRAINT p3_candidate_ranking_signature_completeness_check CHECK (((signature_completeness >= (0)::numeric) AND (signature_completeness <= (1)::numeric))),
    CONSTRAINT p3_candidate_ranking_source_count_check CHECK ((source_count >= 1)),
    CONSTRAINT p3_candidate_ranking_structure_support_count_check CHECK ((structure_support_count >= 0))
);


ALTER TABLE p3a_v27_shadow.p3_candidate_ranking OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_candidate_revision; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_candidate_revision (
    candidate_revision_id text NOT NULL,
    candidate_family_id text NOT NULL,
    revision_number integer NOT NULL,
    candidate_classification text NOT NULL,
    candidate_origin_type text NOT NULL,
    origin_key character(64) NOT NULL,
    canonical_signature_id text,
    evidence_bundle_hash character(64) NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_candidate_revision_candidate_classification_check CHECK ((candidate_classification = ANY (ARRAY['CLEAN_CANDIDATE'::text, 'VARIANT_BEARING_CANDIDATE'::text, 'SPLIT_RISK'::text, 'HIERARCHY_ONLY_RISK'::text, 'COLLISION_BEARING_CANDIDATE'::text, 'STRUCTURE_ONLY_DIAGNOSTIC'::text, 'INSUFFICIENT_AUTHORITY_RISK'::text, 'SEMANTIC_ARTIFACT_RISK'::text]))),
    CONSTRAINT p3_candidate_revision_evidence_bundle_hash_check CHECK ((evidence_bundle_hash ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT p3_candidate_revision_origin_key_check CHECK (((origin_key ~ '^[0-9a-f]{64}$'::text) AND (origin_key !~ '^0{64}$'::text))),
    CONSTRAINT p3_candidate_revision_revision_number_check CHECK ((revision_number >= 1))
);


ALTER TABLE p3a_v27_shadow.p3_candidate_revision OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_candidate_status_event; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_candidate_status_event (
    candidate_family_id text NOT NULL,
    candidate_revision_id text NOT NULL,
    event_ordinal integer NOT NULL,
    from_stage text,
    to_stage text NOT NULL,
    guard_evidence_id text NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_candidate_status_event_event_ordinal_check CHECK ((event_ordinal >= 1))
);


ALTER TABLE p3a_v27_shadow.p3_candidate_status_event OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_candidate_revision_current_stage; Type: VIEW; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE VIEW p3a_v27_shadow.p3_candidate_revision_current_stage AS
 SELECT r.candidate_revision_id,
    r.candidate_family_id,
    e.to_stage AS lifecycle_stage,
    e.event_ordinal,
    e.authority_release_id
   FROM (p3a_v27_shadow.p3_candidate_revision r
     JOIN LATERAL ( SELECT e_1.to_stage,
            e_1.event_ordinal,
            e_1.authority_release_id
           FROM p3a_v27_shadow.p3_candidate_status_event e_1
          WHERE (e_1.candidate_revision_id = r.candidate_revision_id)
          ORDER BY e_1.event_ordinal DESC
         LIMIT 1) e ON (true));


ALTER TABLE p3a_v27_shadow.p3_candidate_revision_current_stage OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_canonical_family; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_canonical_family (
    canonical_family_id text NOT NULL,
    created_by_adjudication_id text NOT NULL,
    created_release_id text NOT NULL,
    retired_release_id text
);


ALTER TABLE p3a_v27_shadow.p3_canonical_family OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_canonical_family_membership; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_canonical_family_membership (
    family_revision_id text NOT NULL,
    member_object_id text NOT NULL,
    variant_revision_id text
);


ALTER TABLE p3a_v27_shadow.p3_canonical_family_membership OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_canonical_family_revision; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_canonical_family_revision (
    family_revision_id text NOT NULL,
    canonical_family_id text NOT NULL,
    revision_number integer NOT NULL,
    canonical_signature_id text NOT NULL,
    canonical_proposition jsonb NOT NULL,
    evidence_bundle_hash character(64) NOT NULL,
    created_by_adjudication_id text NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_canonical_family_revision_evidence_bundle_hash_check CHECK ((evidence_bundle_hash ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT p3_canonical_family_revision_revision_number_check CHECK ((revision_number >= 1))
);


ALTER TABLE p3a_v27_shadow.p3_canonical_family_revision OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_categorical_field_binding; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_categorical_field_binding (
    table_name text NOT NULL,
    column_name text NOT NULL,
    vocabulary_domain text NOT NULL,
    authority_release_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_categorical_field_binding OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_closure_obligation; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_closure_obligation (
    closure_obligation_id text NOT NULL,
    candidate_revision_id text NOT NULL,
    left_object_id text NOT NULL,
    right_object_id text NOT NULL,
    obligation_type text NOT NULL,
    status text NOT NULL,
    resolution_adjudication_id text,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_closure_obligation_check CHECK ((left_object_id < right_object_id)),
    CONSTRAINT p3_closure_obligation_check1 CHECK (((status = ANY (ARRAY['RESOLVED_ACCEPT'::text, 'RESOLVED_SPLIT'::text, 'RESOLVED_EXCLUDE'::text])) = (resolution_adjudication_id IS NOT NULL))),
    CONSTRAINT p3_closure_obligation_status_check CHECK ((status = ANY (ARRAY['OPEN'::text, 'RESOLVED_ACCEPT'::text, 'RESOLVED_SPLIT'::text, 'RESOLVED_EXCLUDE'::text, 'FAIL_CLOSED'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_closure_obligation OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_collision_authority_source; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_collision_authority_source (
    collision_id text NOT NULL,
    source_authority_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_collision_authority_source OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_collision_scope_registry; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_collision_scope_registry (
    collision_id text NOT NULL,
    collision_type text NOT NULL,
    scope_type text NOT NULL,
    orientation text NOT NULL,
    left_role text,
    right_role text,
    left_object_id text NOT NULL,
    right_object_id text NOT NULL,
    hard_blocker boolean NOT NULL,
    source_scope text,
    historical_scope jsonb,
    downstream_effects jsonb DEFAULT '[]'::jsonb NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_collision_scope_registry_check CHECK ((left_object_id < right_object_id)),
    CONSTRAINT p3_collision_scope_registry_check1 CHECK ((((orientation = 'DIRECTIONAL'::text) AND (left_role IS NOT NULL) AND (right_role IS NOT NULL) AND (left_role <> right_role)) OR ((orientation = 'SYMMETRIC'::text) AND (left_role IS NULL) AND (right_role IS NULL)))),
    CONSTRAINT p3_collision_scope_registry_orientation_check CHECK ((orientation = ANY (ARRAY['SYMMETRIC'::text, 'DIRECTIONAL'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_collision_scope_registry OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_component_connectivity_edge; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_component_connectivity_edge (
    component_id text NOT NULL,
    projection_id text NOT NULL,
    authority_release_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_component_connectivity_edge OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_component_membership; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_component_membership (
    component_id text NOT NULL,
    member_object_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_component_membership OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_runtime_promotion_pointer; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_runtime_promotion_pointer (
    singleton_key boolean DEFAULT true NOT NULL,
    promoted_release_id text NOT NULL,
    promoted_at timestamp with time zone NOT NULL,
    promotion_evidence_hash character(64) NOT NULL,
    CONSTRAINT p3_runtime_promotion_pointer_promotion_evidence_hash_check CHECK ((promotion_evidence_hash ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT p3_runtime_promotion_pointer_singleton_key_check CHECK (singleton_key)
);


ALTER TABLE p3a_v27_shadow.p3_runtime_promotion_pointer OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_current_promoted_release; Type: VIEW; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE VIEW p3a_v27_shadow.p3_current_promoted_release AS
 SELECT r.release_id,
    r.parent_release_id,
    r.schema_version,
    r.builder_version,
    r.input_manifest_hash,
    r.created_at,
    r.object_counts,
    r.validation_return_hash,
    r.migration_artifact,
    r.rollback_artifact
   FROM (p3a_v27_shadow.p3_authority_release r
     JOIN p3a_v27_shadow.p3_runtime_promotion_pointer p ON ((p.promoted_release_id = r.release_id)));


ALTER TABLE p3a_v27_shadow.p3_current_promoted_release OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_dependency_edge; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_dependency_edge (
    dependency_id text NOT NULL,
    dependent_id text NOT NULL,
    authority_input_id text NOT NULL,
    dependency_role text NOT NULL,
    dirty_if_changed boolean NOT NULL,
    impact_priority text NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_dependency_edge_impact_priority_check CHECK ((impact_priority = ANY (ARRAY['FATAL'::text, 'HIGH'::text, 'MEDIUM'::text, 'LOW'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_dependency_edge OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_doctrine_delta; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_doctrine_delta (
    doctrine_delta_id text NOT NULL,
    trigger_candidate_id text NOT NULL,
    old_rule text,
    new_rule text NOT NULL,
    required_rebuild_scope text NOT NULL,
    authority_release_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_doctrine_delta OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_doctrine_delta_affected_object; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_doctrine_delta_affected_object (
    doctrine_delta_id text NOT NULL,
    affected_object_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_doctrine_delta_affected_object OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_excluded_object; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_excluded_object (
    exclusion_id text NOT NULL,
    excluded_object_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_excluded_object OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_exclusion_promotion; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_exclusion_promotion (
    adjudication_id text NOT NULL,
    candidate_exclusion_id text NOT NULL,
    canonical_exclusion_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_exclusion_promotion OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_failure_ledger; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_failure_ledger (
    failure_id text NOT NULL,
    build_run_id text NOT NULL,
    severity text NOT NULL,
    object_id text,
    failure_code text NOT NULL,
    message text NOT NULL,
    source_artifact text,
    created_at timestamp with time zone NOT NULL,
    CONSTRAINT p3_failure_ledger_severity_check CHECK ((severity = ANY (ARRAY['FATAL'::text, 'ERROR'::text, 'WARNING'::text, 'INFO'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_failure_ledger OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_family_exclusion; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_family_exclusion (
    exclusion_id text NOT NULL,
    owner_object_id text NOT NULL,
    exclusion_type text NOT NULL,
    prohibited_operation text NOT NULL,
    evidence_or_rule text NOT NULL,
    scope text NOT NULL,
    tested_surface_complete boolean DEFAULT false NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_family_exclusion_exclusion_type_check CHECK ((exclusion_type = ANY (ARRAY['NAMED_MEMBER'::text, 'RULE_BASED'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_family_exclusion OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_family_genealogy; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_family_genealogy (
    genealogy_id text NOT NULL,
    relation_type text NOT NULL,
    adjudication_id text NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_family_genealogy_relation_type_check CHECK ((relation_type = ANY (ARRAY['SPLIT'::text, 'MERGE'::text, 'SUPERSEDE'::text, 'DEPRECATE'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_family_genealogy OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_family_genealogy_member; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_family_genealogy_member (
    genealogy_id text NOT NULL,
    family_id text NOT NULL,
    genealogy_role text NOT NULL,
    CONSTRAINT p3_family_genealogy_member_genealogy_role_check CHECK ((genealogy_role = ANY (ARRAY['PREDECESSOR'::text, 'SUCCESSOR'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_family_genealogy_member OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_family_variant; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_family_variant (
    variant_id text NOT NULL,
    owner_object_id text NOT NULL,
    created_release_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_family_variant OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_family_variant_revision; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_family_variant_revision (
    variant_revision_id text NOT NULL,
    variant_id text NOT NULL,
    revision_number integer NOT NULL,
    variant_dimension text NOT NULL,
    variant_value text NOT NULL,
    value_portability_status text DEFAULT 'NOT_AUTHORIZED_BY_P3'::text NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_family_variant_revision_revision_number_check CHECK ((revision_number >= 1)),
    CONSTRAINT p3_family_variant_revision_value_portability_status_check CHECK ((value_portability_status = 'NOT_AUTHORIZED_BY_P3'::text)),
    CONSTRAINT p3_family_variant_revision_variant_dimension_check CHECK ((variant_dimension = ANY (ARRAY['RESPONSE_TOPOLOGY'::text, 'WORDING_TRANSLATION'::text, 'SOURCE_RESPONSE_FORM'::text, 'HISTORICAL_INTERVAL'::text, 'OTHER_EXPLICITLY_GOVERNED'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_family_variant_revision OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_frozen_historical_candidate_identity; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_frozen_historical_candidate_identity (
    historical_identity_id text NOT NULL,
    historical_object_type text NOT NULL,
    historical_object_id text NOT NULL,
    historical_family_id text,
    historical_revision_number integer,
    allocation_release_id text NOT NULL,
    origin_key character(64) NOT NULL,
    evidence_bundle_hash character(64) NOT NULL,
    source_package text NOT NULL,
    graph_reconstruction_status text NOT NULL,
    reconstruction_unavailable_reason text NOT NULL,
    successor_candidate_family_id text,
    successor_candidate_revision_id text,
    migration_reason text NOT NULL,
    authority_release_id text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    CONSTRAINT p3_frozen_historical_candidat_graph_reconstruction_status_check CHECK ((graph_reconstruction_status = ANY (ARRAY['FULL_GRAPH_UNAVAILABLE'::text, 'FROZEN_IDENTITY_ONLY'::text]))),
    CONSTRAINT p3_frozen_historical_candidate_historical_revision_number_check CHECK (((historical_revision_number IS NULL) OR (historical_revision_number >= 1))),
    CONSTRAINT p3_frozen_historical_candidate_ide_historical_object_type_check CHECK ((historical_object_type = ANY (ARRAY['CANDIDATE_FAMILY'::text, 'CANDIDATE_REVISION'::text]))),
    CONSTRAINT p3_frozen_historical_candidate_ident_evidence_bundle_hash_check CHECK ((evidence_bundle_hash ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT p3_frozen_historical_candidate_identity_check CHECK ((((historical_object_type = 'CANDIDATE_FAMILY'::text) AND (historical_family_id IS NULL) AND (historical_revision_number IS NULL)) OR ((historical_object_type = 'CANDIDATE_REVISION'::text) AND (historical_family_id IS NOT NULL) AND (historical_revision_number IS NOT NULL)))),
    CONSTRAINT p3_frozen_historical_candidate_identity_origin_key_check CHECK (((origin_key ~ '^[0-9a-f]{64}$'::text) AND (origin_key !~ '^0{64}$'::text)))
);


ALTER TABLE p3a_v27_shadow.p3_frozen_historical_candidate_identity OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_hyperedge; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_hyperedge (
    hyperedge_id text NOT NULL,
    hyperedge_type text NOT NULL,
    authority_effect text NOT NULL,
    causal_authority boolean DEFAULT false NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_hyperedge_causal_authority_check CHECK ((NOT causal_authority))
);


ALTER TABLE p3a_v27_shadow.p3_hyperedge OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_hyperedge_membership; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_hyperedge_membership (
    hyperedge_id text NOT NULL,
    object_id text NOT NULL,
    participant_role text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_hyperedge_membership OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_hyperedge_role_type_contract; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_hyperedge_role_type_contract (
    hyperedge_type text NOT NULL,
    participant_role text NOT NULL,
    allowed_object_types text[] NOT NULL,
    minimum_count integer NOT NULL,
    maximum_count integer,
    authority_effect_ceiling text NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_hyperedge_role_type_contract_check CHECK (((maximum_count IS NULL) OR (maximum_count >= minimum_count))),
    CONSTRAINT p3_hyperedge_role_type_contract_minimum_count_check CHECK ((minimum_count >= 0))
);


ALTER TABLE p3a_v27_shadow.p3_hyperedge_role_type_contract OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_identity_key_contract; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_identity_key_contract (
    object_type text NOT NULL,
    identity_strategy text NOT NULL,
    id_pattern text NOT NULL,
    idempotency_key_spec text NOT NULL,
    authority_release_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_identity_key_contract OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_imported_lineage_membership; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_imported_lineage_membership (
    lineage_id text NOT NULL,
    implementation_id text NOT NULL,
    ordinal_position integer NOT NULL,
    source_authority_id text NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_imported_lineage_membership_ordinal_position_check CHECK ((ordinal_position >= 0))
);


ALTER TABLE p3a_v27_shadow.p3_imported_lineage_membership OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_internal_pair_closure; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_internal_pair_closure (
    candidate_revision_id text NOT NULL,
    left_object_id text NOT NULL,
    right_object_id text NOT NULL,
    closure_obligation_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_internal_pair_closure OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_internal_pair_collision; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_internal_pair_collision (
    candidate_revision_id text NOT NULL,
    left_object_id text NOT NULL,
    right_object_id text NOT NULL,
    collision_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_internal_pair_collision OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_internal_pair_coordinate_constraint; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_internal_pair_coordinate_constraint (
    candidate_revision_id text NOT NULL,
    left_object_id text NOT NULL,
    right_object_id text NOT NULL,
    projection_id text NOT NULL,
    coordinate_relation_type text NOT NULL,
    evidence_ids jsonb NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_internal_pair_coordinate_cons_coordinate_relation_type_check CHECK ((coordinate_relation_type = ANY (ARRAY['NESTED_TARGET_RELATION'::text, 'CONSTRUCT_COORDINATE'::text, 'VALUE_PORTABILITY_ONLY'::text]))),
    CONSTRAINT p3_internal_pair_coordinate_constraint_evidence_ids_check CHECK (((jsonb_typeof(evidence_ids) = 'array'::text) AND (jsonb_array_length(evidence_ids) > 0)))
);


ALTER TABLE p3a_v27_shadow.p3_internal_pair_coordinate_constraint OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_internal_pair_matrix; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_internal_pair_matrix (
    candidate_revision_id text NOT NULL,
    left_object_id text NOT NULL,
    right_object_id text NOT NULL,
    pair_state text NOT NULL,
    direct_pair_projection_id text,
    CONSTRAINT p3_internal_pair_matrix_check CHECK ((left_object_id < right_object_id)),
    CONSTRAINT p3_internal_pair_matrix_check1 CHECK ((((pair_state = ANY (ARRAY['UNRULED'::text, 'SIGNATURE_CONFLICT'::text, 'SIGNATURE_COMPATIBLE'::text])) AND (direct_pair_projection_id IS NULL)) OR ((pair_state = ANY (ARRAY['DIRECT_POSITIVE'::text, 'DIRECT_COLLISION'::text, 'DIRECT_UNRESOLVED'::text, 'HIERARCHICAL_ONLY'::text])) AND (direct_pair_projection_id IS NOT NULL)))),
    CONSTRAINT p3_internal_pair_matrix_pair_state_check CHECK ((pair_state = ANY (ARRAY['DIRECT_POSITIVE'::text, 'DIRECT_COLLISION'::text, 'DIRECT_UNRESOLVED'::text, 'HIERARCHICAL_ONLY'::text, 'UNRULED'::text, 'SIGNATURE_CONFLICT'::text, 'SIGNATURE_COMPATIBLE'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_internal_pair_matrix OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_internal_pair_redirect_boundary; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_internal_pair_redirect_boundary (
    candidate_revision_id text NOT NULL,
    left_object_id text NOT NULL,
    right_object_id text NOT NULL,
    projection_id text NOT NULL,
    redirect_scope text NOT NULL,
    evidence_ids jsonb NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_internal_pair_redirect_boundary_evidence_ids_check CHECK (((jsonb_typeof(evidence_ids) = 'array'::text) AND (jsonb_array_length(evidence_ids) > 0)))
);


ALTER TABLE p3a_v27_shadow.p3_internal_pair_redirect_boundary OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_internal_pair_unresolved_boundary; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_internal_pair_unresolved_boundary (
    candidate_revision_id text NOT NULL,
    left_object_id text NOT NULL,
    right_object_id text NOT NULL,
    projection_id text NOT NULL,
    unresolved_boundary_type text NOT NULL,
    evidence_ids jsonb NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_internal_pair_unresolved_boun_unresolved_boundary_type_check CHECK ((unresolved_boundary_type = ANY (ARRAY['EXACT_FOUNDATION_UNRESOLVED'::text, 'FAIL_CLOSED_UNRESOLVED'::text, 'OTHER_UNRESOLVED'::text]))),
    CONSTRAINT p3_internal_pair_unresolved_boundary_evidence_ids_check CHECK (((jsonb_typeof(evidence_ids) = 'array'::text) AND (jsonb_array_length(evidence_ids) > 0)))
);


ALTER TABLE p3a_v27_shadow.p3_internal_pair_unresolved_boundary OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_lineage_disposition; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_lineage_disposition (
    subject_id text NOT NULL,
    subject_type text NOT NULL,
    disposition_status text NOT NULL,
    reason text NOT NULL,
    canonical_family_id text,
    evidence_ids jsonb NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_lineage_disposition_check CHECK (((disposition_status = 'CANONICAL_MEMBER'::text) = (canonical_family_id IS NOT NULL))),
    CONSTRAINT p3_lineage_disposition_disposition_status_check CHECK ((disposition_status = ANY (ARRAY['ADMINISTRATIVE_METADATA_PRESERVED'::text, 'BLOCKED_UNRESOLVED'::text, 'CANDIDATE_PARTICIPANT'::text, 'CANONICAL_MEMBER'::text, 'CONSTRAINT_ONLY_PRESERVED'::text, 'DERIVED_OR_INDEX_PRESERVED'::text, 'OUT_OF_SCOPE_NONQUESTION'::text, 'SOURCE_LOCAL_SINGLETON_PRESERVED'::text, 'SUPERSEDED_BY_SEGMENT'::text, 'UNADJUDICATED'::text]))),
    CONSTRAINT p3_lineage_disposition_evidence_ids_check CHECK ((jsonb_typeof(evidence_ids) = 'array'::text)),
    CONSTRAINT p3_lineage_disposition_subject_type_check CHECK ((subject_type = ANY (ARRAY['IMPORTED_SOURCE_LOCAL_LINEAGE'::text, 'LINEAGE_SEGMENT'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_lineage_disposition OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_lineage_participation; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_lineage_participation (
    lineage_id text NOT NULL,
    participation_status text NOT NULL,
    effective_pair_incident_count integer NOT NULL,
    proposition_pair_incident_count integer NOT NULL,
    signature_requirement text NOT NULL,
    authority_note text,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_lineage_participation_effective_pair_incident_count_check CHECK ((effective_pair_incident_count >= 0)),
    CONSTRAINT p3_lineage_participation_proposition_pair_incident_count_check CHECK ((proposition_pair_incident_count >= 0))
);


ALTER TABLE p3a_v27_shadow.p3_lineage_participation OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_lineage_segment; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_lineage_segment (
    segment_id text NOT NULL,
    parent_lineage_id text NOT NULL,
    segment_reason text NOT NULL,
    first_wave text,
    last_wave text,
    p2_lineage_unchanged boolean NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_lineage_segment_p2_lineage_unchanged_check CHECK (p2_lineage_unchanged)
);


ALTER TABLE p3a_v27_shadow.p3_lineage_segment OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_lineage_segment_member; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_lineage_segment_member (
    segment_id text NOT NULL,
    implementation_id text NOT NULL,
    ordinal_position integer NOT NULL,
    CONSTRAINT p3_lineage_segment_member_ordinal_position_check CHECK ((ordinal_position >= 0))
);


ALTER TABLE p3a_v27_shadow.p3_lineage_segment_member OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_object_reference_type_contract; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_object_reference_type_contract (
    table_name text NOT NULL,
    column_name text NOT NULL,
    allowed_object_types text[] NOT NULL,
    authority_release_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_object_reference_type_contract OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_object_registry; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_object_registry (
    object_id text NOT NULL,
    object_type text NOT NULL,
    identity_strategy text NOT NULL,
    idempotency_key text NOT NULL,
    origin_phase text NOT NULL,
    origin_authority_id text,
    allocation_release_id text NOT NULL,
    retired_release_id text,
    content_hash character(64),
    stable_identity_note text NOT NULL,
    CONSTRAINT p3_object_registry_content_hash_check CHECK (((content_hash IS NULL) OR (content_hash ~ '^[0-9a-f]{64}$'::text))),
    CONSTRAINT p3_object_registry_identity_strategy_check CHECK ((identity_strategy = ANY (ARRAY['INHERITED_UPSTREAM_ID'::text, 'CONTENT_ADDRESSED_DERIVED_ID'::text, 'REGISTRY_ALLOCATED_DURABLE_ID'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_object_registry OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_pair_endpoint_resolution; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_pair_endpoint_resolution (
    pair_fact_id text NOT NULL,
    endpoint_side text NOT NULL,
    original_lineage_id text NOT NULL,
    resolution_status text NOT NULL,
    evidence_ids jsonb DEFAULT '[]'::jsonb NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_pair_endpoint_resolution_endpoint_side_check CHECK ((endpoint_side = ANY (ARRAY['LEFT'::text, 'RIGHT'::text]))),
    CONSTRAINT p3_pair_endpoint_resolution_resolution_status_check CHECK ((resolution_status = ANY (ARRAY['ORIGINAL_LINEAGE'::text, 'SEGMENT_BOUND'::text, 'BLOCKED_HETEROGENEOUS'::text, 'FAIL_CLOSED_UNRESOLVED'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_pair_endpoint_resolution OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_pair_endpoint_resolved_subject; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_pair_endpoint_resolved_subject (
    pair_fact_id text NOT NULL,
    endpoint_side text NOT NULL,
    resolved_subject_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_pair_endpoint_resolved_subject OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_pair_fact_bundle; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_pair_fact_bundle (
    pair_fact_id text NOT NULL,
    left_object_id text NOT NULL,
    right_object_id text NOT NULL,
    orientation text NOT NULL,
    relation_type text NOT NULL,
    target_relation text,
    operator_relation text,
    timeframe_relation text,
    response_relation text,
    source_portability_ceiling text NOT NULL,
    p3_portability_ceiling text NOT NULL,
    proposition_graph_allowed boolean NOT NULL,
    j_family_candidate_eligibility text NOT NULL,
    creates_endpoint_authority boolean DEFAULT false NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_pair_fact_bundle_check CHECK ((left_object_id <> right_object_id)),
    CONSTRAINT p3_pair_fact_bundle_check1 CHECK (((orientation = 'DIRECTIONAL'::text) OR (left_object_id < right_object_id))),
    CONSTRAINT p3_pair_fact_bundle_check2 CHECK (((proposition_graph_allowed = false) OR (relation_type = ANY (ARRAY['PROPOSITION_RESPONSE_IDENTITY'::text, 'PROPOSITION_IDENTITY_ONLY'::text])))),
    CONSTRAINT p3_pair_fact_bundle_creates_endpoint_authority_check CHECK ((NOT creates_endpoint_authority)),
    CONSTRAINT p3_pair_fact_bundle_orientation_check CHECK ((orientation = ANY (ARRAY['SYMMETRIC'::text, 'DIRECTIONAL'::text]))),
    CONSTRAINT p3_pair_fact_bundle_p3_portability_ceiling_check CHECK ((p3_portability_ceiling = ANY (ARRAY['QUESTION_PROPOSITION_AND_RESPONSE_CONTRACT'::text, 'QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY'::text, 'QUESTION_PROPOSITION_ONLY'::text, 'DOMAIN_COORDINATE_ONLY'::text, 'CONSTRUCT_TARGET_COORDINATE_ONLY'::text, 'HIERARCHICAL_ONLY'::text, 'NO_POSITIVE_AUTHORITY'::text]))),
    CONSTRAINT p3_pair_fact_bundle_relation_type_check CHECK ((relation_type = ANY (ARRAY['PROPOSITION_RESPONSE_IDENTITY'::text, 'PROPOSITION_IDENTITY_ONLY'::text, 'NESTED_TARGET_RELATION'::text, 'CONSTRUCT_COORDINATE'::text, 'STRUCTURE_MEMBER_ANALOGY'::text, 'EXPLICIT_NEGATIVE'::text, 'REDIRECT_OTHER_DOMAIN'::text, 'UNRESOLVED'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_pair_fact_bundle OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_pair_fact_evidence; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_pair_fact_evidence (
    pair_fact_id text NOT NULL,
    side text NOT NULL,
    evidence_id text NOT NULL,
    evidence_type text NOT NULL,
    CONSTRAINT p3_pair_fact_evidence_side_check CHECK ((side = ANY (ARRAY['LEFT'::text, 'RIGHT'::text, 'RELATION'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_pair_fact_evidence OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_pair_fact_source_authority; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_pair_fact_source_authority (
    pair_fact_id text NOT NULL,
    registry_code text NOT NULL,
    authority_id text NOT NULL,
    authority_role text NOT NULL,
    governing boolean NOT NULL,
    superseded_by_authority_id text,
    CONSTRAINT p3_pair_fact_source_authority_check CHECK (((authority_role = 'GOVERNING'::text) = governing))
);


ALTER TABLE p3a_v27_shadow.p3_pair_fact_source_authority OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_pair_projection; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_pair_projection (
    projection_id text NOT NULL,
    pair_fact_id text NOT NULL,
    left_subject_id text NOT NULL,
    right_subject_id text NOT NULL,
    projection_basis text NOT NULL,
    evidence_ids jsonb NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_pair_projection_evidence_ids_check CHECK (((jsonb_typeof(evidence_ids) = 'array'::text) AND (jsonb_array_length(evidence_ids) > 0))),
    CONSTRAINT p3_pair_projection_projection_basis_check CHECK ((projection_basis = ANY (ARRAY['ORIGINAL_LINEAGES'::text, 'SEGMENT_BINDING'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_pair_projection OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_proposition_signature; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_proposition_signature (
    signature_id text NOT NULL,
    subject_id text NOT NULL,
    signature_status text NOT NULL,
    content_hash character(64) NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_proposition_signature_content_hash_check CHECK ((content_hash ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT p3_proposition_signature_signature_status_check CHECK ((signature_status = ANY (ARRAY['COMPLETE'::text, 'PARTIAL_FAIL_CLOSED'::text, 'HETEROGENEOUS'::text, 'CONFLICTING'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_proposition_signature OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_release_change_ledger; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_release_change_ledger (
    release_id text NOT NULL,
    object_id text NOT NULL,
    change_type text NOT NULL,
    prior_content_hash character(64),
    content_hash character(64) NOT NULL,
    reason text,
    CONSTRAINT p3_release_change_ledger_change_type_check CHECK ((change_type = ANY (ARRAY['ADDED'::text, 'REVISED'::text, 'SUPERSEDED'::text, 'DEPRECATED'::text, 'UNCHANGED_REFERENCE'::text]))),
    CONSTRAINT p3_release_change_ledger_content_hash_check CHECK ((content_hash ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT p3_release_change_ledger_prior_content_hash_check CHECK (((prior_content_hash IS NULL) OR (prior_content_hash ~ '^[0-9a-f]{64}$'::text)))
);


ALTER TABLE p3a_v27_shadow.p3_release_change_ledger OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_release_lifecycle_transition; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_release_lifecycle_transition (
    from_status text,
    to_status text NOT NULL,
    guard_text text NOT NULL,
    authority_release_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_release_lifecycle_transition OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_release_object_snapshot; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_release_object_snapshot (
    release_id text NOT NULL,
    object_id text NOT NULL,
    content_hash character(64) NOT NULL,
    CONSTRAINT p3_release_object_snapshot_content_hash_check CHECK ((content_hash ~ '^[0-9a-f]{64}$'::text))
);


ALTER TABLE p3a_v27_shadow.p3_release_object_snapshot OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_release_status_event; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_release_status_event (
    release_id text NOT NULL,
    event_ordinal integer NOT NULL,
    status text NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    evidence_hash character(64) NOT NULL,
    CONSTRAINT p3_release_status_event_event_ordinal_check CHECK ((event_ordinal >= 1)),
    CONSTRAINT p3_release_status_event_evidence_hash_check CHECK ((evidence_hash ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT p3_release_status_event_status_check CHECK ((status = ANY (ARRAY['DRAFT'::text, 'VALIDATED'::text, 'SHADOW'::text, 'PROMOTED'::text, 'ROLLED_BACK'::text, 'SUPERSEDED'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_release_status_event OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_response_contract_reference; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_response_contract_reference (
    reference_id text NOT NULL,
    subject_id text NOT NULL,
    upstream_response_contract_id text,
    response_topology text NOT NULL,
    response_contract_hash character(64),
    authority_artifact text NOT NULL,
    p4_authority boolean DEFAULT false NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_response_contract_reference_p4_authority_check CHECK ((NOT p4_authority)),
    CONSTRAINT p3_response_contract_reference_response_contract_hash_check CHECK (((response_contract_hash IS NULL) OR (response_contract_hash ~ '^[0-9a-f]{64}$'::text)))
);


ALTER TABLE p3a_v27_shadow.p3_response_contract_reference OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_signature_field; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_signature_field (
    signature_id text NOT NULL,
    field_name text NOT NULL,
    field_value text,
    normalized_value_code text,
    evidence_state text NOT NULL,
    confidence text NOT NULL,
    CONSTRAINT p3_signature_field_check CHECK (((evidence_state <> 'KNOWN'::text) OR (field_value IS NOT NULL))),
    CONSTRAINT p3_signature_field_confidence_check CHECK ((confidence = ANY (ARRAY['HIGH'::text, 'MEDIUM'::text, 'LOW'::text, 'NOT_APPLICABLE'::text]))),
    CONSTRAINT p3_signature_field_evidence_state_check CHECK ((evidence_state = ANY (ARRAY['KNOWN'::text, 'EXPLICITLY_UNSPECIFIED'::text, 'NOT_APPLICABLE'::text, 'UNRECOVERED'::text, 'HETEROGENEOUS'::text, 'CONFLICTING'::text, 'DIAGNOSTIC_ONLY'::text])))
);


ALTER TABLE p3a_v27_shadow.p3_signature_field OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_signature_field_evidence; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_signature_field_evidence (
    signature_id text NOT NULL,
    field_name text NOT NULL,
    evidence_type text NOT NULL,
    evidence_id text NOT NULL,
    evidence_role text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_signature_field_evidence OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_structural_context_reference; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_structural_context_reference (
    reference_id text NOT NULL,
    subject_id text NOT NULL,
    source_field text NOT NULL,
    source_value jsonb,
    authority_artifact text NOT NULL,
    p5_authority boolean DEFAULT false NOT NULL,
    authority_release_id text NOT NULL,
    CONSTRAINT p3_structural_context_reference_p5_authority_check CHECK ((NOT p5_authority))
);


ALTER TABLE p3a_v27_shadow.p3_structural_context_reference OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_upstream_object_reference; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_upstream_object_reference (
    object_id text NOT NULL,
    upstream_phase text NOT NULL,
    source_family text,
    license_provenance_state text NOT NULL,
    upstream_object_type text NOT NULL,
    upstream_object_id text NOT NULL,
    authority_artifact text NOT NULL,
    authority_hash character(64) NOT NULL,
    license_provenance_ref text,
    read_only boolean DEFAULT true NOT NULL,
    CONSTRAINT p3_upstream_object_reference_authority_hash_check CHECK ((authority_hash ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT p3_upstream_object_reference_read_only_check CHECK (read_only)
);


ALTER TABLE p3a_v27_shadow.p3_upstream_object_reference OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_variant_membership; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_variant_membership (
    variant_revision_id text NOT NULL,
    member_object_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_variant_membership OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_variant_promotion; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_variant_promotion (
    adjudication_id text NOT NULL,
    candidate_variant_revision_id text NOT NULL,
    canonical_variant_revision_id text NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_variant_promotion OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_vocabulary_code; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_vocabulary_code (
    vocabulary_domain text NOT NULL,
    code text NOT NULL,
    introduced_release_id text NOT NULL,
    retired_release_id text
);


ALTER TABLE p3a_v27_shadow.p3_vocabulary_code OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_vocabulary_revision; Type: TABLE; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TABLE p3a_v27_shadow.p3_vocabulary_revision (
    vocabulary_domain text NOT NULL,
    code text NOT NULL,
    authority_release_id text NOT NULL,
    label text NOT NULL,
    definition text NOT NULL,
    authority_effect text,
    deprecated boolean DEFAULT false NOT NULL
);


ALTER TABLE p3a_v27_shadow.p3_vocabulary_revision OWNER TO rawlsing_p3a_owner;

--
-- Name: p3_adjudication_collision_disposition p3_adjudication_collision_disposition_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_collision_disposition
    ADD CONSTRAINT p3_adjudication_collision_disposition_pkey PRIMARY KEY (adjudication_id, collision_id);


--
-- Name: p3_adjudication_decision p3_adjudication_decision_candidate_revision_id_decision_ord_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_decision
    ADD CONSTRAINT p3_adjudication_decision_candidate_revision_id_decision_ord_key UNIQUE (candidate_revision_id, decision_ordinal);


--
-- Name: p3_adjudication_decision p3_adjudication_decision_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_decision
    ADD CONSTRAINT p3_adjudication_decision_pkey PRIMARY KEY (adjudication_id);


--
-- Name: p3_adjudication_hierarchy_relation p3_adjudication_hierarchy_relation_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_hierarchy_relation
    ADD CONSTRAINT p3_adjudication_hierarchy_relation_pkey PRIMARY KEY (adjudication_id, broader_object_id, narrower_object_id);


--
-- Name: p3_adjudication_member p3_adjudication_member_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_member
    ADD CONSTRAINT p3_adjudication_member_pkey PRIMARY KEY (adjudication_id, member_object_id);


--
-- Name: p3_adjudication_split_member p3_adjudication_split_member_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_member
    ADD CONSTRAINT p3_adjudication_split_member_pkey PRIMARY KEY (adjudication_id, split_ordinal, split_side, member_object_id);


--
-- Name: p3_adjudication_split_point p3_adjudication_split_point_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_point
    ADD CONSTRAINT p3_adjudication_split_point_pkey PRIMARY KEY (adjudication_id, split_ordinal);


--
-- Name: p3_adjudication_split_result p3_adjudication_split_result_adjudication_id_successor_cand_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_result
    ADD CONSTRAINT p3_adjudication_split_result_adjudication_id_successor_cand_key UNIQUE (adjudication_id, successor_candidate_family_id);


--
-- Name: p3_adjudication_split_result_member p3_adjudication_split_result_member_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_result_member
    ADD CONSTRAINT p3_adjudication_split_result_member_pkey PRIMARY KEY (adjudication_id, result_ordinal, member_object_id);


--
-- Name: p3_adjudication_split_result p3_adjudication_split_result_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_result
    ADD CONSTRAINT p3_adjudication_split_result_pkey PRIMARY KEY (adjudication_id, result_ordinal);


--
-- Name: p3_adjudication_unresolved_boundary p3_adjudication_unresolved_boundary_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_unresolved_boundary
    ADD CONSTRAINT p3_adjudication_unresolved_boundary_pkey PRIMARY KEY (adjudication_id, boundary_id);


--
-- Name: p3_authority_release p3_authority_release_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_authority_release
    ADD CONSTRAINT p3_authority_release_pkey PRIMARY KEY (release_id);


--
-- Name: p3_candidate_attachment_projection p3_candidate_attachment_projection_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_attachment_projection
    ADD CONSTRAINT p3_candidate_attachment_projection_pkey PRIMARY KEY (candidate_revision_id, projection_id);


--
-- Name: p3_candidate_component_link p3_candidate_component_link_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_component_link
    ADD CONSTRAINT p3_candidate_component_link_pkey PRIMARY KEY (candidate_revision_id, component_id);


--
-- Name: p3_candidate_component p3_candidate_component_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_component
    ADD CONSTRAINT p3_candidate_component_pkey PRIMARY KEY (component_id);


--
-- Name: p3_candidate_diagnostic_flag p3_candidate_diagnostic_flag_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_diagnostic_flag
    ADD CONSTRAINT p3_candidate_diagnostic_flag_pkey PRIMARY KEY (candidate_revision_id, flag);


--
-- Name: p3_candidate_family p3_candidate_family_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_family
    ADD CONSTRAINT p3_candidate_family_pkey PRIMARY KEY (candidate_family_id);


--
-- Name: p3_candidate_lifecycle_transition p3_candidate_lifecycle_transi_from_stage_to_stage_authority_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_lifecycle_transition
    ADD CONSTRAINT p3_candidate_lifecycle_transi_from_stage_to_stage_authority_key UNIQUE (from_stage, to_stage, authority_release_id);


--
-- Name: p3_candidate_membership p3_candidate_membership_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_membership
    ADD CONSTRAINT p3_candidate_membership_pkey PRIMARY KEY (candidate_revision_id, member_object_id);


--
-- Name: p3_candidate_ranking p3_candidate_ranking_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_ranking
    ADD CONSTRAINT p3_candidate_ranking_pkey PRIMARY KEY (candidate_revision_id);


--
-- Name: p3_candidate_revision p3_candidate_revision_authority_release_id_origin_key_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_revision
    ADD CONSTRAINT p3_candidate_revision_authority_release_id_origin_key_key UNIQUE (authority_release_id, origin_key);


--
-- Name: p3_candidate_revision p3_candidate_revision_candidate_family_id_authority_release_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_revision
    ADD CONSTRAINT p3_candidate_revision_candidate_family_id_authority_release_key UNIQUE (candidate_family_id, authority_release_id);


--
-- Name: p3_candidate_revision p3_candidate_revision_candidate_family_id_revision_number_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_revision
    ADD CONSTRAINT p3_candidate_revision_candidate_family_id_revision_number_key UNIQUE (candidate_family_id, revision_number);


--
-- Name: p3_candidate_revision p3_candidate_revision_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_revision
    ADD CONSTRAINT p3_candidate_revision_pkey PRIMARY KEY (candidate_revision_id);


--
-- Name: p3_candidate_status_event p3_candidate_status_event_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_status_event
    ADD CONSTRAINT p3_candidate_status_event_pkey PRIMARY KEY (candidate_revision_id, event_ordinal);


--
-- Name: p3_canonical_family_membership p3_canonical_family_membership_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_membership
    ADD CONSTRAINT p3_canonical_family_membership_pkey PRIMARY KEY (family_revision_id, member_object_id);


--
-- Name: p3_canonical_family p3_canonical_family_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family
    ADD CONSTRAINT p3_canonical_family_pkey PRIMARY KEY (canonical_family_id);


--
-- Name: p3_canonical_family_revision p3_canonical_family_revision_canonical_family_id_authority__key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_revision
    ADD CONSTRAINT p3_canonical_family_revision_canonical_family_id_authority__key UNIQUE (canonical_family_id, authority_release_id);


--
-- Name: p3_canonical_family_revision p3_canonical_family_revision_canonical_family_id_revision_n_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_revision
    ADD CONSTRAINT p3_canonical_family_revision_canonical_family_id_revision_n_key UNIQUE (canonical_family_id, revision_number);


--
-- Name: p3_canonical_family_revision p3_canonical_family_revision_created_by_adjudication_id_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_revision
    ADD CONSTRAINT p3_canonical_family_revision_created_by_adjudication_id_key UNIQUE (created_by_adjudication_id);


--
-- Name: p3_canonical_family_revision p3_canonical_family_revision_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_revision
    ADD CONSTRAINT p3_canonical_family_revision_pkey PRIMARY KEY (family_revision_id);


--
-- Name: p3_categorical_field_binding p3_categorical_field_binding_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_categorical_field_binding
    ADD CONSTRAINT p3_categorical_field_binding_pkey PRIMARY KEY (table_name, column_name, authority_release_id);


--
-- Name: p3_closure_obligation p3_closure_obligation_candidate_revision_id_left_object_id__key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_closure_obligation
    ADD CONSTRAINT p3_closure_obligation_candidate_revision_id_left_object_id__key UNIQUE (candidate_revision_id, left_object_id, right_object_id, obligation_type);


--
-- Name: p3_closure_obligation p3_closure_obligation_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_closure_obligation
    ADD CONSTRAINT p3_closure_obligation_pkey PRIMARY KEY (closure_obligation_id);


--
-- Name: p3_collision_authority_source p3_collision_authority_source_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_collision_authority_source
    ADD CONSTRAINT p3_collision_authority_source_pkey PRIMARY KEY (collision_id, source_authority_id);


--
-- Name: p3_collision_scope_registry p3_collision_scope_registry_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_collision_scope_registry
    ADD CONSTRAINT p3_collision_scope_registry_pkey PRIMARY KEY (collision_id);


--
-- Name: p3_component_connectivity_edge p3_component_connectivity_edge_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_component_connectivity_edge
    ADD CONSTRAINT p3_component_connectivity_edge_pkey PRIMARY KEY (component_id, projection_id);


--
-- Name: p3_component_membership p3_component_membership_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_component_membership
    ADD CONSTRAINT p3_component_membership_pkey PRIMARY KEY (component_id, member_object_id);


--
-- Name: p3_dependency_edge p3_dependency_edge_dependent_id_authority_input_id_dependen_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_dependency_edge
    ADD CONSTRAINT p3_dependency_edge_dependent_id_authority_input_id_dependen_key UNIQUE (dependent_id, authority_input_id, dependency_role, authority_release_id);


--
-- Name: p3_dependency_edge p3_dependency_edge_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_dependency_edge
    ADD CONSTRAINT p3_dependency_edge_pkey PRIMARY KEY (dependency_id);


--
-- Name: p3_doctrine_delta_affected_object p3_doctrine_delta_affected_object_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_doctrine_delta_affected_object
    ADD CONSTRAINT p3_doctrine_delta_affected_object_pkey PRIMARY KEY (doctrine_delta_id, affected_object_id);


--
-- Name: p3_doctrine_delta p3_doctrine_delta_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_doctrine_delta
    ADD CONSTRAINT p3_doctrine_delta_pkey PRIMARY KEY (doctrine_delta_id);


--
-- Name: p3_excluded_object p3_excluded_object_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_excluded_object
    ADD CONSTRAINT p3_excluded_object_pkey PRIMARY KEY (exclusion_id, excluded_object_id);


--
-- Name: p3_exclusion_promotion p3_exclusion_promotion_canonical_exclusion_id_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_exclusion_promotion
    ADD CONSTRAINT p3_exclusion_promotion_canonical_exclusion_id_key UNIQUE (canonical_exclusion_id);


--
-- Name: p3_exclusion_promotion p3_exclusion_promotion_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_exclusion_promotion
    ADD CONSTRAINT p3_exclusion_promotion_pkey PRIMARY KEY (adjudication_id, candidate_exclusion_id);


--
-- Name: p3_failure_ledger p3_failure_ledger_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_failure_ledger
    ADD CONSTRAINT p3_failure_ledger_pkey PRIMARY KEY (failure_id);


--
-- Name: p3_family_exclusion p3_family_exclusion_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_exclusion
    ADD CONSTRAINT p3_family_exclusion_pkey PRIMARY KEY (exclusion_id);


--
-- Name: p3_family_genealogy_member p3_family_genealogy_member_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_genealogy_member
    ADD CONSTRAINT p3_family_genealogy_member_pkey PRIMARY KEY (genealogy_id, family_id, genealogy_role);


--
-- Name: p3_family_genealogy p3_family_genealogy_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_genealogy
    ADD CONSTRAINT p3_family_genealogy_pkey PRIMARY KEY (genealogy_id);


--
-- Name: p3_family_variant p3_family_variant_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_variant
    ADD CONSTRAINT p3_family_variant_pkey PRIMARY KEY (variant_id);


--
-- Name: p3_family_variant_revision p3_family_variant_revision_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_variant_revision
    ADD CONSTRAINT p3_family_variant_revision_pkey PRIMARY KEY (variant_revision_id);


--
-- Name: p3_family_variant_revision p3_family_variant_revision_variant_id_authority_release_id_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_variant_revision
    ADD CONSTRAINT p3_family_variant_revision_variant_id_authority_release_id_key UNIQUE (variant_id, authority_release_id);


--
-- Name: p3_family_variant_revision p3_family_variant_revision_variant_id_revision_number_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_variant_revision
    ADD CONSTRAINT p3_family_variant_revision_variant_id_revision_number_key UNIQUE (variant_id, revision_number);


--
-- Name: p3_frozen_historical_candidate_identity p3_frozen_historical_candidat_historical_object_type_histor_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_frozen_historical_candidate_identity
    ADD CONSTRAINT p3_frozen_historical_candidat_historical_object_type_histor_key UNIQUE (historical_object_type, historical_object_id, allocation_release_id);


--
-- Name: p3_frozen_historical_candidate_identity p3_frozen_historical_candidate_identity_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_frozen_historical_candidate_identity
    ADD CONSTRAINT p3_frozen_historical_candidate_identity_pkey PRIMARY KEY (historical_identity_id);


--
-- Name: p3_hyperedge_membership p3_hyperedge_membership_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_hyperedge_membership
    ADD CONSTRAINT p3_hyperedge_membership_pkey PRIMARY KEY (hyperedge_id, object_id, participant_role);


--
-- Name: p3_hyperedge p3_hyperedge_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_hyperedge
    ADD CONSTRAINT p3_hyperedge_pkey PRIMARY KEY (hyperedge_id);


--
-- Name: p3_hyperedge_role_type_contract p3_hyperedge_role_type_contract_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_hyperedge_role_type_contract
    ADD CONSTRAINT p3_hyperedge_role_type_contract_pkey PRIMARY KEY (hyperedge_type, participant_role, authority_release_id);


--
-- Name: p3_identity_key_contract p3_identity_key_contract_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_identity_key_contract
    ADD CONSTRAINT p3_identity_key_contract_pkey PRIMARY KEY (object_type, authority_release_id);


--
-- Name: p3_imported_lineage_membership p3_imported_lineage_membershi_implementation_id_authority_r_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_imported_lineage_membership
    ADD CONSTRAINT p3_imported_lineage_membershi_implementation_id_authority_r_key UNIQUE (implementation_id, authority_release_id);


--
-- Name: p3_imported_lineage_membership p3_imported_lineage_membershi_lineage_id_ordinal_position_a_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_imported_lineage_membership
    ADD CONSTRAINT p3_imported_lineage_membershi_lineage_id_ordinal_position_a_key UNIQUE (lineage_id, ordinal_position, authority_release_id);


--
-- Name: p3_imported_lineage_membership p3_imported_lineage_membership_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_imported_lineage_membership
    ADD CONSTRAINT p3_imported_lineage_membership_pkey PRIMARY KEY (lineage_id, implementation_id, authority_release_id);


--
-- Name: p3_internal_pair_closure p3_internal_pair_closure_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_closure
    ADD CONSTRAINT p3_internal_pair_closure_pkey PRIMARY KEY (candidate_revision_id, left_object_id, right_object_id, closure_obligation_id);


--
-- Name: p3_internal_pair_collision p3_internal_pair_collision_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_collision
    ADD CONSTRAINT p3_internal_pair_collision_pkey PRIMARY KEY (candidate_revision_id, left_object_id, right_object_id, collision_id);


--
-- Name: p3_internal_pair_coordinate_constraint p3_internal_pair_coordinate_constraint_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_coordinate_constraint
    ADD CONSTRAINT p3_internal_pair_coordinate_constraint_pkey PRIMARY KEY (candidate_revision_id, left_object_id, right_object_id, projection_id);


--
-- Name: p3_internal_pair_matrix p3_internal_pair_matrix_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_matrix
    ADD CONSTRAINT p3_internal_pair_matrix_pkey PRIMARY KEY (candidate_revision_id, left_object_id, right_object_id);


--
-- Name: p3_internal_pair_redirect_boundary p3_internal_pair_redirect_boundary_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_redirect_boundary
    ADD CONSTRAINT p3_internal_pair_redirect_boundary_pkey PRIMARY KEY (candidate_revision_id, left_object_id, right_object_id, projection_id);


--
-- Name: p3_internal_pair_unresolved_boundary p3_internal_pair_unresolved_boundary_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_unresolved_boundary
    ADD CONSTRAINT p3_internal_pair_unresolved_boundary_pkey PRIMARY KEY (candidate_revision_id, left_object_id, right_object_id, projection_id);


--
-- Name: p3_lineage_disposition p3_lineage_disposition_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_disposition
    ADD CONSTRAINT p3_lineage_disposition_pkey PRIMARY KEY (subject_id, authority_release_id);


--
-- Name: p3_lineage_participation p3_lineage_participation_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_participation
    ADD CONSTRAINT p3_lineage_participation_pkey PRIMARY KEY (lineage_id, authority_release_id);


--
-- Name: p3_lineage_segment_member p3_lineage_segment_member_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_segment_member
    ADD CONSTRAINT p3_lineage_segment_member_pkey PRIMARY KEY (segment_id, implementation_id);


--
-- Name: p3_lineage_segment_member p3_lineage_segment_member_segment_id_ordinal_position_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_segment_member
    ADD CONSTRAINT p3_lineage_segment_member_segment_id_ordinal_position_key UNIQUE (segment_id, ordinal_position);


--
-- Name: p3_lineage_segment p3_lineage_segment_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_segment
    ADD CONSTRAINT p3_lineage_segment_pkey PRIMARY KEY (segment_id);


--
-- Name: p3_object_reference_type_contract p3_object_reference_type_contract_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_object_reference_type_contract
    ADD CONSTRAINT p3_object_reference_type_contract_pkey PRIMARY KEY (table_name, column_name, authority_release_id);


--
-- Name: p3_object_registry p3_object_registry_idempotency_key_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_object_registry
    ADD CONSTRAINT p3_object_registry_idempotency_key_key UNIQUE (idempotency_key);


--
-- Name: p3_object_registry p3_object_registry_object_id_object_type_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_object_registry
    ADD CONSTRAINT p3_object_registry_object_id_object_type_key UNIQUE (object_id, object_type);


--
-- Name: p3_object_registry p3_object_registry_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_object_registry
    ADD CONSTRAINT p3_object_registry_pkey PRIMARY KEY (object_id);


--
-- Name: p3_pair_endpoint_resolution p3_pair_endpoint_resolution_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_endpoint_resolution
    ADD CONSTRAINT p3_pair_endpoint_resolution_pkey PRIMARY KEY (pair_fact_id, endpoint_side);


--
-- Name: p3_pair_endpoint_resolved_subject p3_pair_endpoint_resolved_subject_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_endpoint_resolved_subject
    ADD CONSTRAINT p3_pair_endpoint_resolved_subject_pkey PRIMARY KEY (pair_fact_id, endpoint_side, resolved_subject_id);


--
-- Name: p3_pair_fact_bundle p3_pair_fact_bundle_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_fact_bundle
    ADD CONSTRAINT p3_pair_fact_bundle_pkey PRIMARY KEY (pair_fact_id);


--
-- Name: p3_pair_fact_evidence p3_pair_fact_evidence_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_fact_evidence
    ADD CONSTRAINT p3_pair_fact_evidence_pkey PRIMARY KEY (pair_fact_id, side, evidence_id);


--
-- Name: p3_pair_fact_source_authority p3_pair_fact_source_authority_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_fact_source_authority
    ADD CONSTRAINT p3_pair_fact_source_authority_pkey PRIMARY KEY (pair_fact_id, registry_code, authority_id);


--
-- Name: p3_pair_projection p3_pair_projection_pair_fact_id_left_subject_id_right_subje_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_projection
    ADD CONSTRAINT p3_pair_projection_pair_fact_id_left_subject_id_right_subje_key UNIQUE (pair_fact_id, left_subject_id, right_subject_id);


--
-- Name: p3_pair_projection p3_pair_projection_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_projection
    ADD CONSTRAINT p3_pair_projection_pkey PRIMARY KEY (projection_id);


--
-- Name: p3_proposition_signature p3_proposition_signature_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_proposition_signature
    ADD CONSTRAINT p3_proposition_signature_pkey PRIMARY KEY (signature_id);


--
-- Name: p3_proposition_signature p3_proposition_signature_subject_id_authority_release_id_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_proposition_signature
    ADD CONSTRAINT p3_proposition_signature_subject_id_authority_release_id_key UNIQUE (subject_id, authority_release_id);


--
-- Name: p3_release_change_ledger p3_release_change_ledger_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_release_change_ledger
    ADD CONSTRAINT p3_release_change_ledger_pkey PRIMARY KEY (release_id, object_id);


--
-- Name: p3_release_lifecycle_transition p3_release_lifecycle_transiti_from_status_to_status_authori_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_release_lifecycle_transition
    ADD CONSTRAINT p3_release_lifecycle_transiti_from_status_to_status_authori_key UNIQUE (from_status, to_status, authority_release_id);


--
-- Name: p3_release_object_snapshot p3_release_object_snapshot_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_release_object_snapshot
    ADD CONSTRAINT p3_release_object_snapshot_pkey PRIMARY KEY (release_id, object_id);


--
-- Name: p3_release_status_event p3_release_status_event_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_release_status_event
    ADD CONSTRAINT p3_release_status_event_pkey PRIMARY KEY (release_id, event_ordinal);


--
-- Name: p3_response_contract_reference p3_response_contract_reference_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_response_contract_reference
    ADD CONSTRAINT p3_response_contract_reference_pkey PRIMARY KEY (reference_id);


--
-- Name: p3_runtime_promotion_pointer p3_runtime_promotion_pointer_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_runtime_promotion_pointer
    ADD CONSTRAINT p3_runtime_promotion_pointer_pkey PRIMARY KEY (singleton_key);


--
-- Name: p3_runtime_promotion_pointer p3_runtime_promotion_pointer_promoted_release_id_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_runtime_promotion_pointer
    ADD CONSTRAINT p3_runtime_promotion_pointer_promoted_release_id_key UNIQUE (promoted_release_id);


--
-- Name: p3_signature_field_evidence p3_signature_field_evidence_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_signature_field_evidence
    ADD CONSTRAINT p3_signature_field_evidence_pkey PRIMARY KEY (signature_id, field_name, evidence_type, evidence_id);


--
-- Name: p3_signature_field p3_signature_field_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_signature_field
    ADD CONSTRAINT p3_signature_field_pkey PRIMARY KEY (signature_id, field_name);


--
-- Name: p3_structural_context_reference p3_structural_context_reference_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_structural_context_reference
    ADD CONSTRAINT p3_structural_context_reference_pkey PRIMARY KEY (reference_id);


--
-- Name: p3_upstream_object_reference p3_upstream_object_reference_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_upstream_object_reference
    ADD CONSTRAINT p3_upstream_object_reference_pkey PRIMARY KEY (object_id);


--
-- Name: p3_upstream_object_reference p3_upstream_object_reference_upstream_phase_upstream_object_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_upstream_object_reference
    ADD CONSTRAINT p3_upstream_object_reference_upstream_phase_upstream_object_key UNIQUE (upstream_phase, upstream_object_type, upstream_object_id);


--
-- Name: p3_variant_membership p3_variant_membership_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_variant_membership
    ADD CONSTRAINT p3_variant_membership_pkey PRIMARY KEY (variant_revision_id, member_object_id);


--
-- Name: p3_variant_promotion p3_variant_promotion_canonical_variant_revision_id_key; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_variant_promotion
    ADD CONSTRAINT p3_variant_promotion_canonical_variant_revision_id_key UNIQUE (canonical_variant_revision_id);


--
-- Name: p3_variant_promotion p3_variant_promotion_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_variant_promotion
    ADD CONSTRAINT p3_variant_promotion_pkey PRIMARY KEY (adjudication_id, candidate_variant_revision_id);


--
-- Name: p3_vocabulary_code p3_vocabulary_code_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_vocabulary_code
    ADD CONSTRAINT p3_vocabulary_code_pkey PRIMARY KEY (vocabulary_domain, code);


--
-- Name: p3_vocabulary_revision p3_vocabulary_revision_pkey; Type: CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_vocabulary_revision
    ADD CONSTRAINT p3_vocabulary_revision_pkey PRIMARY KEY (vocabulary_domain, code, authority_release_id);


--
-- Name: p3_pair_fact_one_governing_source; Type: INDEX; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE UNIQUE INDEX p3_pair_fact_one_governing_source ON p3a_v27_shadow.p3_pair_fact_source_authority USING btree (pair_fact_id) WHERE governing;


--
-- Name: p3_adjudication_collision_disposition p3_adjudication_collision_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_adjudication_collision_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_adjudication_collision_disposition FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_adjudication_decision p3_adjudication_decision_complete; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_adjudication_decision_complete AFTER INSERT ON p3a_v27_shadow.p3_adjudication_decision DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_adjudication_completeness();


--
-- Name: p3_adjudication_decision p3_adjudication_decision_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_adjudication_decision_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_adjudication_decision FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_adjudication_hierarchy_relation p3_adjudication_hierarchy_complete; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_adjudication_hierarchy_complete AFTER INSERT ON p3a_v27_shadow.p3_adjudication_hierarchy_relation DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_adjudication_completeness();


--
-- Name: p3_adjudication_hierarchy_relation p3_adjudication_hierarchy_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_adjudication_hierarchy_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_adjudication_hierarchy_relation FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_adjudication_member p3_adjudication_member_complete; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_adjudication_member_complete AFTER INSERT ON p3a_v27_shadow.p3_adjudication_member DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_adjudication_completeness();


--
-- Name: p3_adjudication_member p3_adjudication_member_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_adjudication_member_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_adjudication_member FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_canonical_family_membership p3_adjudication_partition_canonical_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_adjudication_partition_canonical_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_canonical_family_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_adjudication_closure_deferred();


--
-- Name: p3_adjudication_decision p3_adjudication_partition_decision_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_adjudication_partition_decision_closure AFTER INSERT ON p3a_v27_shadow.p3_adjudication_decision DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_adjudication_closure_deferred();


--
-- Name: p3_exclusion_promotion p3_adjudication_partition_exclusion_promotion_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_adjudication_partition_exclusion_promotion_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_exclusion_promotion DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_adjudication_closure_deferred();


--
-- Name: p3_adjudication_member p3_adjudication_partition_member_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_adjudication_partition_member_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_adjudication_member DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_adjudication_closure_deferred();


--
-- Name: p3_adjudication_split_result_member p3_adjudication_partition_split_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_adjudication_partition_split_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_adjudication_split_result_member DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_adjudication_closure_deferred();


--
-- Name: p3_variant_promotion p3_adjudication_partition_variant_promotion_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_adjudication_partition_variant_promotion_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_variant_promotion DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_adjudication_closure_deferred();


--
-- Name: p3_adjudication_split_point p3_adjudication_split_complete; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_adjudication_split_complete AFTER INSERT ON p3a_v27_shadow.p3_adjudication_split_point DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_adjudication_completeness();


--
-- Name: p3_adjudication_split_member p3_adjudication_split_member_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_adjudication_split_member_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_adjudication_split_member FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_adjudication_split_point p3_adjudication_split_point_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_adjudication_split_point_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_adjudication_split_point FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_adjudication_unresolved_boundary p3_adjudication_unresolved_complete; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_adjudication_unresolved_complete AFTER INSERT ON p3a_v27_shadow.p3_adjudication_unresolved_boundary DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_adjudication_completeness();


--
-- Name: p3_adjudication_unresolved_boundary p3_adjudication_unresolved_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_adjudication_unresolved_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_adjudication_unresolved_boundary FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_candidate_status_event p3_candidate_event_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_candidate_event_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_candidate_status_event FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_candidate_attachment_projection p3_candidate_origin_attachment_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_candidate_origin_attachment_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_candidate_attachment_projection DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_candidate_origin_deferred();


--
-- Name: p3_candidate_component_link p3_candidate_origin_component_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_candidate_origin_component_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_candidate_component_link DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_candidate_origin_deferred();


--
-- Name: p3_candidate_membership p3_candidate_origin_member_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_candidate_origin_member_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_candidate_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_candidate_origin_deferred();


--
-- Name: p3_candidate_revision p3_candidate_origin_revision_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_candidate_origin_revision_closure AFTER INSERT ON p3a_v27_shadow.p3_candidate_revision DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_candidate_origin_deferred();


--
-- Name: p3_candidate_status_event p3_candidate_status_event_validate; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_candidate_status_event_validate BEFORE INSERT ON p3a_v27_shadow.p3_candidate_status_event FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_candidate_status_event();


--
-- Name: p3_canonical_family_revision p3_canonical_family_revision_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_canonical_family_revision_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_canonical_family_revision FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_component_connectivity_edge p3_component_edge_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_component_edge_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_component_connectivity_edge DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_component_closure();


--
-- Name: p3_candidate_component p3_component_header_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_component_header_closure AFTER INSERT OR UPDATE ON p3a_v27_shadow.p3_candidate_component DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_component_closure();


--
-- Name: p3_component_membership p3_component_member_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_component_member_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_component_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_component_closure();


--
-- Name: p3_doctrine_delta p3_doctrine_delta_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_doctrine_delta_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_doctrine_delta FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_family_exclusion p3_family_exclusion_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_family_exclusion_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_family_exclusion FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_family_genealogy p3_family_genealogy_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_family_genealogy_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_family_genealogy FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_frozen_historical_candidate_identity p3_frozen_historical_candidate_identity_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_frozen_historical_candidate_identity_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_frozen_historical_candidate_identity FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_family_genealogy p3_genealogy_header_cardinality; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_genealogy_header_cardinality AFTER INSERT ON p3a_v27_shadow.p3_family_genealogy DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_genealogy_cardinality();


--
-- Name: p3_family_genealogy_member p3_genealogy_member_cardinality; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_genealogy_member_cardinality AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_family_genealogy_member DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_genealogy_cardinality();


--
-- Name: p3_hyperedge p3_hyperedge_cardinality_after_header; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_hyperedge_cardinality_after_header AFTER INSERT OR UPDATE ON p3a_v27_shadow.p3_hyperedge DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_hyperedge_cardinality();


--
-- Name: p3_hyperedge p3_hyperedge_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_hyperedge_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_hyperedge FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_hyperedge_membership p3_hyperedge_member_cardinality; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_hyperedge_member_cardinality AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_hyperedge_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_hyperedge_cardinality();


--
-- Name: p3_hyperedge_membership p3_hyperedge_member_type_validate; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_hyperedge_member_type_validate BEFORE INSERT OR UPDATE ON p3a_v27_shadow.p3_hyperedge_membership FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_hyperedge_member_type();


--
-- Name: p3_internal_pair_collision p3_internal_pair_collision_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_internal_pair_collision_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_internal_pair_collision DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_internal_pair_closure();


--
-- Name: p3_internal_pair_matrix p3_internal_pair_header_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_internal_pair_header_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_internal_pair_matrix DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_internal_pair_closure();


--
-- Name: p3_candidate_membership p3_internal_pair_member_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_internal_pair_member_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_candidate_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_internal_pair_closure();


--
-- Name: p3_internal_pair_closure p3_internal_pair_obligation_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_internal_pair_obligation_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_internal_pair_closure DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_internal_pair_closure();


--
-- Name: p3_object_registry p3_object_registry_identity_validate; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_object_registry_identity_validate BEFORE INSERT OR UPDATE ON p3a_v27_shadow.p3_object_registry FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_identity_contract();


--
-- Name: p3_object_registry p3_object_registry_mutation_guard; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_object_registry_mutation_guard BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_object_registry FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_guard_object_registry_mutation();


--
-- Name: p3_pair_endpoint_resolution p3_pair_endpoint_header_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_pair_endpoint_header_closure AFTER INSERT OR UPDATE ON p3a_v27_shadow.p3_pair_endpoint_resolution DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_pair_endpoint_resolution();


--
-- Name: p3_pair_endpoint_resolved_subject p3_pair_endpoint_subject_closure; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_pair_endpoint_subject_closure AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_pair_endpoint_resolved_subject DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_pair_endpoint_resolution();


--
-- Name: p3_pair_projection p3_pair_projection_validate; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_pair_projection_validate BEFORE INSERT OR UPDATE ON p3a_v27_shadow.p3_pair_projection FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_pair_projection();


--
-- Name: p3_runtime_promotion_pointer p3_promotion_pointer_validate; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_promotion_pointer_validate BEFORE INSERT OR UPDATE ON p3a_v27_shadow.p3_runtime_promotion_pointer FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_promotion_pointer();


--
-- Name: p3_release_status_event p3_release_event_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_release_event_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_release_status_event FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_release_status_event p3_release_status_event_validate; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_release_status_event_validate BEFORE INSERT ON p3a_v27_shadow.p3_release_status_event FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_release_status_event();


--
-- Name: p3_lineage_segment p3_segment_header_nonempty; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_segment_header_nonempty AFTER INSERT OR UPDATE ON p3a_v27_shadow.p3_lineage_segment DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_segment_membership();


--
-- Name: p3_lineage_segment_member p3_segment_member_subset; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE CONSTRAINT TRIGGER p3_segment_member_subset AFTER INSERT OR DELETE OR UPDATE ON p3a_v27_shadow.p3_lineage_segment_member DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_validate_segment_membership();


--
-- Name: p3_family_variant p3_type_0cef6345bad4b6d5; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_0cef6345bad4b6d5 BEFORE INSERT OR UPDATE OF owner_object_id ON p3a_v27_shadow.p3_family_variant FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('owner_object_id', 'CANDIDATE_FAMILY|CANONICAL_FAMILY');


--
-- Name: p3_family_exclusion p3_type_10008172d2238ff8; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_10008172d2238ff8 BEFORE INSERT OR UPDATE OF owner_object_id ON p3a_v27_shadow.p3_family_exclusion FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('owner_object_id', 'CANDIDATE_FAMILY|CANONICAL_FAMILY');


--
-- Name: p3_component_membership p3_type_14fba0b351e0aa23; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_14fba0b351e0aa23 BEFORE INSERT OR UPDATE OF member_object_id ON p3a_v27_shadow.p3_component_membership FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('member_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_pair_fact_bundle p3_type_157ed629260ca678; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_157ed629260ca678 BEFORE INSERT OR UPDATE OF left_object_id ON p3a_v27_shadow.p3_pair_fact_bundle FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('left_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_internal_pair_closure p3_type_16954c6d98f388d4; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_16954c6d98f388d4 BEFORE INSERT OR UPDATE OF closure_obligation_id ON p3a_v27_shadow.p3_internal_pair_closure FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('closure_obligation_id', 'CLOSURE_OBLIGATION');


--
-- Name: p3_pair_projection p3_type_1f2e585b1974338f; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_1f2e585b1974338f BEFORE INSERT OR UPDATE OF left_subject_id ON p3a_v27_shadow.p3_pair_projection FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('left_subject_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_lineage_segment_member p3_type_28b00844ed620a0c; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_28b00844ed620a0c BEFORE INSERT OR UPDATE OF implementation_id ON p3a_v27_shadow.p3_lineage_segment_member FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('implementation_id', 'IMPORTED_IMPLEMENTATION');


--
-- Name: p3_canonical_family_membership p3_type_2b52b7f318e16149; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_2b52b7f318e16149 BEFORE INSERT OR UPDATE OF member_object_id ON p3a_v27_shadow.p3_canonical_family_membership FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('member_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_variant_membership p3_type_2cfd50ad8a41f63c; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_2cfd50ad8a41f63c BEFORE INSERT OR UPDATE OF member_object_id ON p3a_v27_shadow.p3_variant_membership FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('member_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_component_connectivity_edge p3_type_30a5d552a0e5568c; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_30a5d552a0e5568c BEFORE INSERT OR UPDATE OF component_id ON p3a_v27_shadow.p3_component_connectivity_edge FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('component_id', 'CANDIDATE_COMPONENT');


--
-- Name: p3_adjudication_unresolved_boundary p3_type_3103f00003de15cc; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_3103f00003de15cc BEFORE INSERT OR UPDATE OF right_object_id ON p3a_v27_shadow.p3_adjudication_unresolved_boundary FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('right_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT|CANDIDATE_FAMILY|CANONICAL_FAMILY');


--
-- Name: p3_adjudication_hierarchy_relation p3_type_3b934bac3ecd639c; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_3b934bac3ecd639c BEFORE INSERT OR UPDATE OF narrower_object_id ON p3a_v27_shadow.p3_adjudication_hierarchy_relation FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('narrower_object_id', 'CANDIDATE_FAMILY|CANONICAL_FAMILY');


--
-- Name: p3_collision_scope_registry p3_type_40bdafcb8da2a4a3; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_40bdafcb8da2a4a3 BEFORE INSERT OR UPDATE OF left_object_id ON p3a_v27_shadow.p3_collision_scope_registry FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('left_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_proposition_signature p3_type_54836a5c21114597; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_54836a5c21114597 BEFORE INSERT OR UPDATE OF subject_id ON p3a_v27_shadow.p3_proposition_signature FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('subject_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT|CANDIDATE_REVISION|CANONICAL_FAMILY_REVISION');


--
-- Name: p3_internal_pair_matrix p3_type_5a37e755d8e24bab; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_5a37e755d8e24bab BEFORE INSERT OR UPDATE OF left_object_id ON p3a_v27_shadow.p3_internal_pair_matrix FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('left_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_collision_scope_registry p3_type_6e201ce0310e2313; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_6e201ce0310e2313 BEFORE INSERT OR UPDATE OF right_object_id ON p3a_v27_shadow.p3_collision_scope_registry FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('right_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_imported_lineage_membership p3_type_712879ecf639d0f2; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_712879ecf639d0f2 BEFORE INSERT OR UPDATE OF lineage_id ON p3a_v27_shadow.p3_imported_lineage_membership FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('lineage_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE');


--
-- Name: p3_internal_pair_matrix p3_type_77f3e1c5fb74fa76; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_77f3e1c5fb74fa76 BEFORE INSERT OR UPDATE OF right_object_id ON p3a_v27_shadow.p3_internal_pair_matrix FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('right_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_candidate_attachment_projection p3_type_7ce9cb8da011e81d; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_7ce9cb8da011e81d BEFORE INSERT OR UPDATE OF projection_id ON p3a_v27_shadow.p3_candidate_attachment_projection FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('projection_id', 'PAIR_PROJECTION');


--
-- Name: p3_lineage_segment p3_type_80a6ccb7eed4bb1f; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_80a6ccb7eed4bb1f BEFORE INSERT OR UPDATE OF parent_lineage_id ON p3a_v27_shadow.p3_lineage_segment FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('parent_lineage_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE');


--
-- Name: p3_excluded_object p3_type_85c5985e5d3f6012; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_85c5985e5d3f6012 BEFORE INSERT OR UPDATE OF excluded_object_id ON p3a_v27_shadow.p3_excluded_object FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('excluded_object_id', 'IMPORTED_IMPLEMENTATION|IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_candidate_membership p3_type_962b97d699a38cd1; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_962b97d699a38cd1 BEFORE INSERT OR UPDATE OF member_object_id ON p3a_v27_shadow.p3_candidate_membership FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('member_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_adjudication_unresolved_boundary p3_type_a23253f8cbc970ba; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_a23253f8cbc970ba BEFORE INSERT OR UPDATE OF left_object_id ON p3a_v27_shadow.p3_adjudication_unresolved_boundary FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('left_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT|CANDIDATE_FAMILY|CANONICAL_FAMILY');


--
-- Name: p3_adjudication_split_result_member p3_type_a30a4e1b2da91ac0; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_a30a4e1b2da91ac0 BEFORE INSERT OR UPDATE OF member_object_id ON p3a_v27_shadow.p3_adjudication_split_result_member FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('member_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_closure_obligation p3_type_a3fbae85eefd9a61; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_a3fbae85eefd9a61 BEFORE INSERT OR UPDATE OF right_object_id ON p3a_v27_shadow.p3_closure_obligation FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('right_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_lineage_disposition p3_type_a63242f4a7a1c685; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_a63242f4a7a1c685 BEFORE INSERT OR UPDATE OF subject_id ON p3a_v27_shadow.p3_lineage_disposition FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('subject_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_imported_lineage_membership p3_type_a6b10f2c36968e05; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_a6b10f2c36968e05 BEFORE INSERT OR UPDATE OF implementation_id ON p3a_v27_shadow.p3_imported_lineage_membership FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('implementation_id', 'IMPORTED_IMPLEMENTATION');


--
-- Name: p3_adjudication_hierarchy_relation p3_type_a8f88ca9547e225e; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_a8f88ca9547e225e BEFORE INSERT OR UPDATE OF broader_object_id ON p3a_v27_shadow.p3_adjudication_hierarchy_relation FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('broader_object_id', 'CANDIDATE_FAMILY|CANONICAL_FAMILY');


--
-- Name: p3_candidate_status_event p3_type_aaeb973c461da5fb; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_aaeb973c461da5fb BEFORE INSERT OR UPDATE OF candidate_revision_id ON p3a_v27_shadow.p3_candidate_status_event FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('candidate_revision_id', 'CANDIDATE_REVISION');


--
-- Name: p3_closure_obligation p3_type_b279804675492dc3; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_b279804675492dc3 BEFORE INSERT OR UPDATE OF left_object_id ON p3a_v27_shadow.p3_closure_obligation FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('left_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_adjudication_split_member p3_type_b9270734e4501dfa; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_b9270734e4501dfa BEFORE INSERT OR UPDATE OF member_object_id ON p3a_v27_shadow.p3_adjudication_split_member FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('member_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_pair_endpoint_resolved_subject p3_type_bbd7802a9c0fcea7; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_bbd7802a9c0fcea7 BEFORE INSERT OR UPDATE OF resolved_subject_id ON p3a_v27_shadow.p3_pair_endpoint_resolved_subject FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('resolved_subject_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_adjudication_member p3_type_bbdaa2f835e9bc13; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_bbdaa2f835e9bc13 BEFORE INSERT OR UPDATE OF member_object_id ON p3a_v27_shadow.p3_adjudication_member FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('member_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_pair_projection p3_type_bf006ab7bf2eb277; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_bf006ab7bf2eb277 BEFORE INSERT OR UPDATE OF right_subject_id ON p3a_v27_shadow.p3_pair_projection FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('right_subject_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_response_contract_reference p3_type_c367eddbb0f1e94a; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_c367eddbb0f1e94a BEFORE INSERT OR UPDATE OF subject_id ON p3a_v27_shadow.p3_response_contract_reference FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('subject_id', 'IMPORTED_IMPLEMENTATION|IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_internal_pair_collision p3_type_c949655f9d1822a9; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_c949655f9d1822a9 BEFORE INSERT OR UPDATE OF collision_id ON p3a_v27_shadow.p3_internal_pair_collision FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('collision_id', 'COLLISION');


--
-- Name: p3_pair_endpoint_resolution p3_type_dd9c0060092b512d; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_dd9c0060092b512d BEFORE INSERT OR UPDATE OF original_lineage_id ON p3a_v27_shadow.p3_pair_endpoint_resolution FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('original_lineage_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE');


--
-- Name: p3_component_connectivity_edge p3_type_e24b2fadf00556a4; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_e24b2fadf00556a4 BEFORE INSERT OR UPDATE OF projection_id ON p3a_v27_shadow.p3_component_connectivity_edge FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('projection_id', 'PAIR_PROJECTION');


--
-- Name: p3_pair_fact_bundle p3_type_e3b6e4179f9f2a14; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_e3b6e4179f9f2a14 BEFORE INSERT OR UPDATE OF right_object_id ON p3a_v27_shadow.p3_pair_fact_bundle FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('right_object_id', 'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT');


--
-- Name: p3_structural_context_reference p3_type_e4e70b4142a5c5b0; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_type_e4e70b4142a5c5b0 BEFORE INSERT OR UPDATE OF subject_id ON p3a_v27_shadow.p3_structural_context_reference FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_object_reference_type('subject_id', 'IMPORTED_IMPLEMENTATION|IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT|CANDIDATE_FAMILY|CANONICAL_FAMILY|FAMILY_VARIANT');


--
-- Name: p3_family_variant_revision p3_variant_revision_immutable; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_variant_revision_immutable BEFORE DELETE OR UPDATE ON p3a_v27_shadow.p3_family_variant_revision FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_forbid_update_delete();


--
-- Name: p3_signature_field p3_vocab_07fe2f6e9182ecbd; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_07fe2f6e9182ecbd BEFORE INSERT OR UPDATE OF field_name ON p3a_v27_shadow.p3_signature_field FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('signature_field_name', 'field_name', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_lineage_disposition p3_vocab_0c7261155b4b23a9; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_0c7261155b4b23a9 BEFORE INSERT OR UPDATE OF disposition_status ON p3a_v27_shadow.p3_lineage_disposition FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('lineage_p3_disposition_status', 'disposition_status', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_family_exclusion p3_vocab_0f213941ed51d3af; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_0f213941ed51d3af BEFORE INSERT OR UPDATE OF exclusion_type ON p3a_v27_shadow.p3_family_exclusion FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('exclusion_type', 'exclusion_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_candidate_revision p3_vocab_12ed79e43b76148e; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_12ed79e43b76148e BEFORE INSERT OR UPDATE OF candidate_classification ON p3a_v27_shadow.p3_candidate_revision FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('candidate_classification', 'candidate_classification', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_adjudication_decision p3_vocab_180b99d603bd9d2d; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_180b99d603bd9d2d BEFORE INSERT OR UPDATE OF response_portability_status ON p3a_v27_shadow.p3_adjudication_decision FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('response_portability_status', 'response_portability_status', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_object_registry p3_vocab_222af508c7b766bb; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_222af508c7b766bb BEFORE INSERT OR UPDATE OF object_type ON p3a_v27_shadow.p3_object_registry FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('object_type', 'object_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_candidate_status_event p3_vocab_2c05f8c57c5c44c6; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_2c05f8c57c5c44c6 BEFORE INSERT OR UPDATE OF from_stage ON p3a_v27_shadow.p3_candidate_status_event FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('lifecycle_stage', 'from_stage', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_bundle p3_vocab_31e4d72138167cb9; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_31e4d72138167cb9 BEFORE INSERT OR UPDATE OF response_relation ON p3a_v27_shadow.p3_pair_fact_bundle FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('axis_relation', 'response_relation', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_evidence p3_vocab_37b1032aacfcd6e9; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_37b1032aacfcd6e9 BEFORE INSERT OR UPDATE OF side ON p3a_v27_shadow.p3_pair_fact_evidence FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('evidence_side', 'side', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_bundle p3_vocab_381712017c75a496; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_381712017c75a496 BEFORE INSERT OR UPDATE OF p3_portability_ceiling ON p3a_v27_shadow.p3_pair_fact_bundle FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('portability_ceiling', 'p3_portability_ceiling', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_family_variant_revision p3_vocab_3b5fedcae76c67ac; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_3b5fedcae76c67ac BEFORE INSERT OR UPDATE OF variant_dimension ON p3a_v27_shadow.p3_family_variant_revision FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('variant_dimension', 'variant_dimension', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_release_lifecycle_transition p3_vocab_3d1fe397656eba30; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_3d1fe397656eba30 BEFORE INSERT OR UPDATE OF to_status ON p3a_v27_shadow.p3_release_lifecycle_transition FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('release_status', 'to_status', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_response_contract_reference p3_vocab_3dfe81d9200d7b78; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_3dfe81d9200d7b78 BEFORE INSERT OR UPDATE OF response_topology ON p3a_v27_shadow.p3_response_contract_reference FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('response_topology', 'response_topology', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_bundle p3_vocab_3f577a823c9977bc; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_3f577a823c9977bc BEFORE INSERT OR UPDATE OF target_relation ON p3a_v27_shadow.p3_pair_fact_bundle FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('axis_relation', 'target_relation', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_upstream_object_reference p3_vocab_42af4b016d8c9955; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_42af4b016d8c9955 BEFORE INSERT OR UPDATE OF license_provenance_state ON p3a_v27_shadow.p3_upstream_object_reference FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('license_provenance_state', 'license_provenance_state', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_hyperedge_role_type_contract p3_vocab_449f85191b6558dc; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_449f85191b6558dc BEFORE INSERT OR UPDATE OF authority_effect_ceiling ON p3a_v27_shadow.p3_hyperedge_role_type_contract FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('hyperedge_authority_effect', 'authority_effect_ceiling', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_collision_scope_registry p3_vocab_473e841fea9f33e6; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_473e841fea9f33e6 BEFORE INSERT OR UPDATE OF orientation ON p3a_v27_shadow.p3_collision_scope_registry FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('collision_orientation', 'orientation', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_bundle p3_vocab_48f65fcd403742ee; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_48f65fcd403742ee BEFORE INSERT OR UPDATE OF j_family_candidate_eligibility ON p3a_v27_shadow.p3_pair_fact_bundle FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('pair_authority_eligibility', 'j_family_candidate_eligibility', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_family_variant_revision p3_vocab_4947b3288b9edd43; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_4947b3288b9edd43 BEFORE INSERT OR UPDATE OF value_portability_status ON p3a_v27_shadow.p3_family_variant_revision FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('response_portability_status', 'value_portability_status', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_candidate_status_event p3_vocab_52126c334b7706e4; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_52126c334b7706e4 BEFORE INSERT OR UPDATE OF to_stage ON p3a_v27_shadow.p3_candidate_status_event FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('lifecycle_stage', 'to_stage', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_dependency_edge p3_vocab_5e708f09afcb18fa; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_5e708f09afcb18fa BEFORE INSERT OR UPDATE OF dependency_role ON p3a_v27_shadow.p3_dependency_edge FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('dependency_role', 'dependency_role', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_hyperedge p3_vocab_5f13e1652eeb0f32; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_5f13e1652eeb0f32 BEFORE INSERT OR UPDATE OF hyperedge_type ON p3a_v27_shadow.p3_hyperedge FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('hyperedge_type', 'hyperedge_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_lineage_participation p3_vocab_61ca9a427350f298; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_61ca9a427350f298 BEFORE INSERT OR UPDATE OF participation_status ON p3a_v27_shadow.p3_lineage_participation FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('lineage_participation_status', 'participation_status', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_candidate_lifecycle_transition p3_vocab_6374919003c6f05d; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_6374919003c6f05d BEFORE INSERT OR UPDATE OF to_stage ON p3a_v27_shadow.p3_candidate_lifecycle_transition FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('lifecycle_stage', 'to_stage', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_dependency_edge p3_vocab_6587d17bbefaf004; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_6587d17bbefaf004 BEFORE INSERT OR UPDATE OF impact_priority ON p3a_v27_shadow.p3_dependency_edge FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('impact_priority', 'impact_priority', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_signature_field_evidence p3_vocab_66730f7dd3351ad1; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_66730f7dd3351ad1 BEFORE INSERT OR UPDATE OF evidence_role ON p3a_v27_shadow.p3_signature_field_evidence FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('evidence_role', 'evidence_role', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_evidence p3_vocab_6c67951a2abb6a55; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_6c67951a2abb6a55 BEFORE INSERT OR UPDATE OF evidence_type ON p3a_v27_shadow.p3_pair_fact_evidence FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('evidence_type', 'evidence_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_candidate_membership p3_vocab_7496322186b3d356; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_7496322186b3d356 BEFORE INSERT OR UPDATE OF membership_role ON p3a_v27_shadow.p3_candidate_membership FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('candidate_membership_role', 'membership_role', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_projection p3_vocab_74bb5a4d8c2b5e24; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_74bb5a4d8c2b5e24 BEFORE INSERT OR UPDATE OF projection_basis ON p3a_v27_shadow.p3_pair_projection FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('pair_projection_basis', 'projection_basis', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_collision_scope_registry p3_vocab_84b539dfb913a702; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_84b539dfb913a702 BEFORE INSERT OR UPDATE OF collision_type ON p3a_v27_shadow.p3_collision_scope_registry FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('collision_type', 'collision_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_source_authority p3_vocab_87a14cf7ec7471e2; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_87a14cf7ec7471e2 BEFORE INSERT OR UPDATE OF authority_role ON p3a_v27_shadow.p3_pair_fact_source_authority FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('source_authority_role', 'authority_role', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_hyperedge_role_type_contract p3_vocab_88cc9e07124436be; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_88cc9e07124436be BEFORE INSERT OR UPDATE OF hyperedge_type ON p3a_v27_shadow.p3_hyperedge_role_type_contract FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('hyperedge_type', 'hyperedge_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_lineage_segment p3_vocab_89518042dc01538e; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_89518042dc01538e BEFORE INSERT OR UPDATE OF segment_reason ON p3a_v27_shadow.p3_lineage_segment FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('lineage_segment_reason', 'segment_reason', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_collision_scope_registry p3_vocab_8c3a3bfca358a255; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_8c3a3bfca358a255 BEFORE INSERT OR UPDATE OF scope_type ON p3a_v27_shadow.p3_collision_scope_registry FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('collision_scope', 'scope_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_release_change_ledger p3_vocab_8e81c54df0b86032; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_8e81c54df0b86032 BEFORE INSERT OR UPDATE OF change_type ON p3a_v27_shadow.p3_release_change_ledger FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('release_change_type', 'change_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_signature_field_evidence p3_vocab_9af2718e17c54910; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_9af2718e17c54910 BEFORE INSERT OR UPDATE OF evidence_type ON p3a_v27_shadow.p3_signature_field_evidence FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('evidence_type', 'evidence_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_bundle p3_vocab_9d0b4aaef41386d3; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_9d0b4aaef41386d3 BEFORE INSERT OR UPDATE OF orientation ON p3a_v27_shadow.p3_pair_fact_bundle FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('relation_orientation', 'orientation', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_release_status_event p3_vocab_a288a9ebfa66569a; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_a288a9ebfa66569a BEFORE INSERT OR UPDATE OF status ON p3a_v27_shadow.p3_release_status_event FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('release_status', 'status', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_adjudication_member p3_vocab_a810fa0b2a89b486; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_a810fa0b2a89b486 BEFORE INSERT OR UPDATE OF member_disposition ON p3a_v27_shadow.p3_adjudication_member FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('adjudication_member_disposition', 'member_disposition', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_internal_pair_matrix p3_vocab_a84080c3d454fb22; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_a84080c3d454fb22 BEFORE INSERT OR UPDATE OF pair_state ON p3a_v27_shadow.p3_internal_pair_matrix FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('pair_state', 'pair_state', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_failure_ledger p3_vocab_a9ed33cead7f799f; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_a9ed33cead7f799f BEFORE INSERT OR UPDATE OF severity ON p3a_v27_shadow.p3_failure_ledger FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('failure_severity', 'severity', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_bundle p3_vocab_ac723dd88cb83a1c; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_ac723dd88cb83a1c BEFORE INSERT OR UPDATE OF operator_relation ON p3a_v27_shadow.p3_pair_fact_bundle FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('axis_relation', 'operator_relation', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_family_genealogy_member p3_vocab_b1a748253280fdbb; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_b1a748253280fdbb BEFORE INSERT OR UPDATE OF genealogy_role ON p3a_v27_shadow.p3_family_genealogy_member FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('genealogy_role', 'genealogy_role', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_source_authority p3_vocab_b26a4e922427ebc1; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_b26a4e922427ebc1 BEFORE INSERT OR UPDATE OF registry_code ON p3a_v27_shadow.p3_pair_fact_source_authority FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('upstream_registry', 'registry_code', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_signature_field p3_vocab_b446a47223d71e0a; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_b446a47223d71e0a BEFORE INSERT OR UPDATE OF confidence ON p3a_v27_shadow.p3_signature_field FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('confidence_level', 'confidence', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_candidate_membership p3_vocab_b63a86e15199f583; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_b63a86e15199f583 BEFORE INSERT OR UPDATE OF membership_basis ON p3a_v27_shadow.p3_candidate_membership FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('candidate_membership_basis', 'membership_basis', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_closure_obligation p3_vocab_b66797b59f326cf7; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_b66797b59f326cf7 BEFORE INSERT OR UPDATE OF status ON p3a_v27_shadow.p3_closure_obligation FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('closure_status', 'status', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_adjudication_decision p3_vocab_b9b02d01d2ea6d6d; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_b9b02d01d2ea6d6d BEFORE INSERT OR UPDATE OF decision_status ON p3a_v27_shadow.p3_adjudication_decision FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('adjudication_decision_status', 'decision_status', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_lineage_disposition p3_vocab_be3e63445f8fe212; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_be3e63445f8fe212 BEFORE INSERT OR UPDATE OF subject_type ON p3a_v27_shadow.p3_lineage_disposition FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('object_type', 'subject_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_candidate_attachment_projection p3_vocab_bff214a08e98de25; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_bff214a08e98de25 BEFORE INSERT OR UPDATE OF attachment_role ON p3a_v27_shadow.p3_candidate_attachment_projection FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('attachment_role', 'attachment_role', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_closure_obligation p3_vocab_c2bcd0648d9c092e; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_c2bcd0648d9c092e BEFORE INSERT OR UPDATE OF obligation_type ON p3a_v27_shadow.p3_closure_obligation FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('closure_obligation_type', 'obligation_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_doctrine_delta p3_vocab_c49cb0b874c29fdf; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_c49cb0b874c29fdf BEFORE INSERT OR UPDATE OF required_rebuild_scope ON p3a_v27_shadow.p3_doctrine_delta FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('rebuild_scope', 'required_rebuild_scope', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_proposition_signature p3_vocab_c52b0f2d229b3cb7; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_c52b0f2d229b3cb7 BEFORE INSERT OR UPDATE OF signature_status ON p3a_v27_shadow.p3_proposition_signature FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('signature_status', 'signature_status', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_endpoint_resolution p3_vocab_c7a6ec8f20472200; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_c7a6ec8f20472200 BEFORE INSERT OR UPDATE OF resolution_status ON p3a_v27_shadow.p3_pair_endpoint_resolution FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('endpoint_resolution_status', 'resolution_status', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_release_lifecycle_transition p3_vocab_c88f89ec9953062c; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_c88f89ec9953062c BEFORE INSERT OR UPDATE OF from_status ON p3a_v27_shadow.p3_release_lifecycle_transition FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('release_status', 'from_status', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_candidate_diagnostic_flag p3_vocab_cec7b67e3ec2c81b; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_cec7b67e3ec2c81b BEFORE INSERT OR UPDATE OF flag ON p3a_v27_shadow.p3_candidate_diagnostic_flag FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('candidate_diagnostic_flag', 'flag', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_object_registry p3_vocab_d1c32bee63d67a54; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_d1c32bee63d67a54 BEFORE INSERT OR UPDATE OF identity_strategy ON p3a_v27_shadow.p3_object_registry FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('identity_strategy', 'identity_strategy', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_candidate_revision p3_vocab_d2d7c618ca113de6; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_d2d7c618ca113de6 BEFORE INSERT OR UPDATE OF candidate_origin_type ON p3a_v27_shadow.p3_candidate_revision FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('candidate_origin_type', 'candidate_origin_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_hyperedge_role_type_contract p3_vocab_d62b41158bc478a1; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_d62b41158bc478a1 BEFORE INSERT OR UPDATE OF participant_role ON p3a_v27_shadow.p3_hyperedge_role_type_contract FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('hyperedge_participant_role', 'participant_role', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_adjudication_split_member p3_vocab_d682f8cec5c2cf43; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_d682f8cec5c2cf43 BEFORE INSERT OR UPDATE OF split_side ON p3a_v27_shadow.p3_adjudication_split_member FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('split_side', 'split_side', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_bundle p3_vocab_e4fa091657ebe25e; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_e4fa091657ebe25e BEFORE INSERT OR UPDATE OF relation_type ON p3a_v27_shadow.p3_pair_fact_bundle FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('pair_relation_type', 'relation_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_signature_field p3_vocab_e54a2ff65332542c; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_e54a2ff65332542c BEFORE INSERT OR UPDATE OF evidence_state ON p3a_v27_shadow.p3_signature_field FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('field_evidence_state', 'evidence_state', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_hyperedge p3_vocab_e5d3a771c6be0e29; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_e5d3a771c6be0e29 BEFORE INSERT OR UPDATE OF authority_effect ON p3a_v27_shadow.p3_hyperedge FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('hyperedge_authority_effect', 'authority_effect', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_candidate_lifecycle_transition p3_vocab_e7d157ba27f286aa; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_e7d157ba27f286aa BEFORE INSERT OR UPDATE OF from_stage ON p3a_v27_shadow.p3_candidate_lifecycle_transition FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('lifecycle_stage', 'from_stage', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_pair_fact_bundle p3_vocab_eca44de80e100f79; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_eca44de80e100f79 BEFORE INSERT OR UPDATE OF timeframe_relation ON p3a_v27_shadow.p3_pair_fact_bundle FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('axis_relation', 'timeframe_relation', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_upstream_object_reference p3_vocab_fa00340c36e3e8a0; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_fa00340c36e3e8a0 BEFORE INSERT OR UPDATE OF source_family ON p3a_v27_shadow.p3_upstream_object_reference FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('source_family', 'source_family', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_family_genealogy p3_vocab_fbb0811c3930bb77; Type: TRIGGER; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

CREATE TRIGGER p3_vocab_fbb0811c3930bb77 BEFORE INSERT OR UPDATE OF relation_type ON p3a_v27_shadow.p3_family_genealogy FOR EACH ROW EXECUTE FUNCTION p3a_v27_shadow.p3_enforce_vocab_code('genealogy_relation_type', 'relation_type', 'P3-AUTHORITY-2026-08-01-R36');


--
-- Name: p3_adjudication_decision p3_adjudication_canonical_family_fk; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_decision
    ADD CONSTRAINT p3_adjudication_canonical_family_fk FOREIGN KEY (canonical_family_id) REFERENCES p3a_v27_shadow.p3_canonical_family(canonical_family_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: p3_adjudication_collision_disposition p3_adjudication_collision_disposition_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_collision_disposition
    ADD CONSTRAINT p3_adjudication_collision_disposition_adjudication_id_fkey FOREIGN KEY (adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_adjudication_collision_disposition p3_adjudication_collision_disposition_collision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_collision_disposition
    ADD CONSTRAINT p3_adjudication_collision_disposition_collision_id_fkey FOREIGN KEY (collision_id) REFERENCES p3a_v27_shadow.p3_collision_scope_registry(collision_id);


--
-- Name: p3_adjudication_decision p3_adjudication_decision_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_decision
    ADD CONSTRAINT p3_adjudication_decision_adjudication_id_fkey FOREIGN KEY (adjudication_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_adjudication_decision p3_adjudication_decision_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_decision
    ADD CONSTRAINT p3_adjudication_decision_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_adjudication_decision p3_adjudication_decision_candidate_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_decision
    ADD CONSTRAINT p3_adjudication_decision_candidate_revision_id_fkey FOREIGN KEY (candidate_revision_id) REFERENCES p3a_v27_shadow.p3_candidate_revision(candidate_revision_id);


--
-- Name: p3_adjudication_decision p3_adjudication_decision_canonical_family_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_decision
    ADD CONSTRAINT p3_adjudication_decision_canonical_family_id_fkey FOREIGN KEY (canonical_family_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_adjudication_decision p3_adjudication_decision_supersedes_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_decision
    ADD CONSTRAINT p3_adjudication_decision_supersedes_adjudication_id_fkey FOREIGN KEY (supersedes_adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_adjudication_hierarchy_relation p3_adjudication_hierarchy_relation_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_hierarchy_relation
    ADD CONSTRAINT p3_adjudication_hierarchy_relation_adjudication_id_fkey FOREIGN KEY (adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_adjudication_hierarchy_relation p3_adjudication_hierarchy_relation_broader_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_hierarchy_relation
    ADD CONSTRAINT p3_adjudication_hierarchy_relation_broader_object_id_fkey FOREIGN KEY (broader_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_adjudication_hierarchy_relation p3_adjudication_hierarchy_relation_narrower_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_hierarchy_relation
    ADD CONSTRAINT p3_adjudication_hierarchy_relation_narrower_object_id_fkey FOREIGN KEY (narrower_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_adjudication_member p3_adjudication_member_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_member
    ADD CONSTRAINT p3_adjudication_member_adjudication_id_fkey FOREIGN KEY (adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_adjudication_member p3_adjudication_member_member_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_member
    ADD CONSTRAINT p3_adjudication_member_member_object_id_fkey FOREIGN KEY (member_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_adjudication_member p3_adjudication_member_variant_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_member
    ADD CONSTRAINT p3_adjudication_member_variant_revision_id_fkey FOREIGN KEY (variant_revision_id) REFERENCES p3a_v27_shadow.p3_family_variant_revision(variant_revision_id);


--
-- Name: p3_adjudication_split_member p3_adjudication_split_member_adjudication_id_split_ordinal_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_member
    ADD CONSTRAINT p3_adjudication_split_member_adjudication_id_split_ordinal_fkey FOREIGN KEY (adjudication_id, split_ordinal) REFERENCES p3a_v27_shadow.p3_adjudication_split_point(adjudication_id, split_ordinal);


--
-- Name: p3_adjudication_split_member p3_adjudication_split_member_member_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_member
    ADD CONSTRAINT p3_adjudication_split_member_member_object_id_fkey FOREIGN KEY (member_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_adjudication_split_point p3_adjudication_split_point_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_point
    ADD CONSTRAINT p3_adjudication_split_point_adjudication_id_fkey FOREIGN KEY (adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_adjudication_split_result_member p3_adjudication_split_result__adjudication_id_result_ordin_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_result_member
    ADD CONSTRAINT p3_adjudication_split_result__adjudication_id_result_ordin_fkey FOREIGN KEY (adjudication_id, result_ordinal) REFERENCES p3a_v27_shadow.p3_adjudication_split_result(adjudication_id, result_ordinal);


--
-- Name: p3_adjudication_split_result p3_adjudication_split_result_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_result
    ADD CONSTRAINT p3_adjudication_split_result_adjudication_id_fkey FOREIGN KEY (adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_adjudication_split_result_member p3_adjudication_split_result_member_member_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_result_member
    ADD CONSTRAINT p3_adjudication_split_result_member_member_object_id_fkey FOREIGN KEY (member_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_adjudication_split_result p3_adjudication_split_result_successor_candidate_family_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_split_result
    ADD CONSTRAINT p3_adjudication_split_result_successor_candidate_family_id_fkey FOREIGN KEY (successor_candidate_family_id) REFERENCES p3a_v27_shadow.p3_candidate_family(candidate_family_id);


--
-- Name: p3_adjudication_unresolved_boundary p3_adjudication_unresolved_boundary_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_unresolved_boundary
    ADD CONSTRAINT p3_adjudication_unresolved_boundary_adjudication_id_fkey FOREIGN KEY (adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_adjudication_unresolved_boundary p3_adjudication_unresolved_boundary_left_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_unresolved_boundary
    ADD CONSTRAINT p3_adjudication_unresolved_boundary_left_object_id_fkey FOREIGN KEY (left_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_adjudication_unresolved_boundary p3_adjudication_unresolved_boundary_right_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_adjudication_unresolved_boundary
    ADD CONSTRAINT p3_adjudication_unresolved_boundary_right_object_id_fkey FOREIGN KEY (right_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_authority_release p3_authority_release_parent_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_authority_release
    ADD CONSTRAINT p3_authority_release_parent_release_id_fkey FOREIGN KEY (parent_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_candidate_attachment_projection p3_candidate_attachment_projection_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_attachment_projection
    ADD CONSTRAINT p3_candidate_attachment_projection_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_candidate_attachment_projection p3_candidate_attachment_projection_candidate_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_attachment_projection
    ADD CONSTRAINT p3_candidate_attachment_projection_candidate_revision_id_fkey FOREIGN KEY (candidate_revision_id) REFERENCES p3a_v27_shadow.p3_candidate_revision(candidate_revision_id);


--
-- Name: p3_candidate_attachment_projection p3_candidate_attachment_projection_projection_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_attachment_projection
    ADD CONSTRAINT p3_candidate_attachment_projection_projection_id_fkey FOREIGN KEY (projection_id) REFERENCES p3a_v27_shadow.p3_pair_projection(projection_id);


--
-- Name: p3_candidate_component p3_candidate_component_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_component
    ADD CONSTRAINT p3_candidate_component_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_candidate_component p3_candidate_component_component_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_component
    ADD CONSTRAINT p3_candidate_component_component_id_fkey FOREIGN KEY (component_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_candidate_component_link p3_candidate_component_link_candidate_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_component_link
    ADD CONSTRAINT p3_candidate_component_link_candidate_revision_id_fkey FOREIGN KEY (candidate_revision_id) REFERENCES p3a_v27_shadow.p3_candidate_revision(candidate_revision_id);


--
-- Name: p3_candidate_component_link p3_candidate_component_link_component_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_component_link
    ADD CONSTRAINT p3_candidate_component_link_component_id_fkey FOREIGN KEY (component_id) REFERENCES p3a_v27_shadow.p3_candidate_component(component_id);


--
-- Name: p3_candidate_diagnostic_flag p3_candidate_diagnostic_flag_candidate_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_diagnostic_flag
    ADD CONSTRAINT p3_candidate_diagnostic_flag_candidate_revision_id_fkey FOREIGN KEY (candidate_revision_id) REFERENCES p3a_v27_shadow.p3_candidate_revision(candidate_revision_id);


--
-- Name: p3_candidate_family p3_candidate_family_candidate_family_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_family
    ADD CONSTRAINT p3_candidate_family_candidate_family_id_fkey FOREIGN KEY (candidate_family_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_candidate_family p3_candidate_family_created_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_family
    ADD CONSTRAINT p3_candidate_family_created_release_id_fkey FOREIGN KEY (created_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_candidate_lifecycle_transition p3_candidate_lifecycle_transition_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_lifecycle_transition
    ADD CONSTRAINT p3_candidate_lifecycle_transition_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_candidate_membership p3_candidate_membership_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_membership
    ADD CONSTRAINT p3_candidate_membership_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_candidate_membership p3_candidate_membership_candidate_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_membership
    ADD CONSTRAINT p3_candidate_membership_candidate_revision_id_fkey FOREIGN KEY (candidate_revision_id) REFERENCES p3a_v27_shadow.p3_candidate_revision(candidate_revision_id);


--
-- Name: p3_candidate_membership p3_candidate_membership_member_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_membership
    ADD CONSTRAINT p3_candidate_membership_member_object_id_fkey FOREIGN KEY (member_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_candidate_ranking p3_candidate_ranking_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_ranking
    ADD CONSTRAINT p3_candidate_ranking_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_candidate_ranking p3_candidate_ranking_candidate_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_ranking
    ADD CONSTRAINT p3_candidate_ranking_candidate_revision_id_fkey FOREIGN KEY (candidate_revision_id) REFERENCES p3a_v27_shadow.p3_candidate_revision(candidate_revision_id);


--
-- Name: p3_candidate_revision p3_candidate_revision_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_revision
    ADD CONSTRAINT p3_candidate_revision_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_candidate_revision p3_candidate_revision_candidate_family_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_revision
    ADD CONSTRAINT p3_candidate_revision_candidate_family_id_fkey FOREIGN KEY (candidate_family_id) REFERENCES p3a_v27_shadow.p3_candidate_family(candidate_family_id);


--
-- Name: p3_candidate_revision p3_candidate_revision_candidate_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_revision
    ADD CONSTRAINT p3_candidate_revision_candidate_revision_id_fkey FOREIGN KEY (candidate_revision_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_candidate_revision p3_candidate_revision_canonical_signature_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_revision
    ADD CONSTRAINT p3_candidate_revision_canonical_signature_id_fkey FOREIGN KEY (canonical_signature_id) REFERENCES p3a_v27_shadow.p3_proposition_signature(signature_id);


--
-- Name: p3_candidate_status_event p3_candidate_status_event_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_status_event
    ADD CONSTRAINT p3_candidate_status_event_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_candidate_status_event p3_candidate_status_event_candidate_family_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_status_event
    ADD CONSTRAINT p3_candidate_status_event_candidate_family_id_fkey FOREIGN KEY (candidate_family_id) REFERENCES p3a_v27_shadow.p3_candidate_family(candidate_family_id);


--
-- Name: p3_candidate_status_event p3_candidate_status_event_candidate_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_candidate_status_event
    ADD CONSTRAINT p3_candidate_status_event_candidate_revision_id_fkey FOREIGN KEY (candidate_revision_id) REFERENCES p3a_v27_shadow.p3_candidate_revision(candidate_revision_id);


--
-- Name: p3_canonical_family p3_canonical_family_canonical_family_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family
    ADD CONSTRAINT p3_canonical_family_canonical_family_id_fkey FOREIGN KEY (canonical_family_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_canonical_family p3_canonical_family_created_by_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family
    ADD CONSTRAINT p3_canonical_family_created_by_adjudication_id_fkey FOREIGN KEY (created_by_adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_canonical_family p3_canonical_family_created_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family
    ADD CONSTRAINT p3_canonical_family_created_release_id_fkey FOREIGN KEY (created_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_canonical_family_membership p3_canonical_family_membership_family_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_membership
    ADD CONSTRAINT p3_canonical_family_membership_family_revision_id_fkey FOREIGN KEY (family_revision_id) REFERENCES p3a_v27_shadow.p3_canonical_family_revision(family_revision_id);


--
-- Name: p3_canonical_family_membership p3_canonical_family_membership_member_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_membership
    ADD CONSTRAINT p3_canonical_family_membership_member_object_id_fkey FOREIGN KEY (member_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_canonical_family_membership p3_canonical_family_membership_variant_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_membership
    ADD CONSTRAINT p3_canonical_family_membership_variant_revision_id_fkey FOREIGN KEY (variant_revision_id) REFERENCES p3a_v27_shadow.p3_family_variant_revision(variant_revision_id);


--
-- Name: p3_canonical_family p3_canonical_family_retired_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family
    ADD CONSTRAINT p3_canonical_family_retired_release_id_fkey FOREIGN KEY (retired_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_canonical_family_revision p3_canonical_family_revision_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_revision
    ADD CONSTRAINT p3_canonical_family_revision_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_canonical_family_revision p3_canonical_family_revision_canonical_family_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_revision
    ADD CONSTRAINT p3_canonical_family_revision_canonical_family_id_fkey FOREIGN KEY (canonical_family_id) REFERENCES p3a_v27_shadow.p3_canonical_family(canonical_family_id);


--
-- Name: p3_canonical_family_revision p3_canonical_family_revision_canonical_signature_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_revision
    ADD CONSTRAINT p3_canonical_family_revision_canonical_signature_id_fkey FOREIGN KEY (canonical_signature_id) REFERENCES p3a_v27_shadow.p3_proposition_signature(signature_id);


--
-- Name: p3_canonical_family_revision p3_canonical_family_revision_created_by_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_revision
    ADD CONSTRAINT p3_canonical_family_revision_created_by_adjudication_id_fkey FOREIGN KEY (created_by_adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_canonical_family_revision p3_canonical_family_revision_family_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_canonical_family_revision
    ADD CONSTRAINT p3_canonical_family_revision_family_revision_id_fkey FOREIGN KEY (family_revision_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_categorical_field_binding p3_categorical_field_binding_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_categorical_field_binding
    ADD CONSTRAINT p3_categorical_field_binding_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_closure_obligation p3_closure_obligation_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_closure_obligation
    ADD CONSTRAINT p3_closure_obligation_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_closure_obligation p3_closure_obligation_candidate_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_closure_obligation
    ADD CONSTRAINT p3_closure_obligation_candidate_revision_id_fkey FOREIGN KEY (candidate_revision_id) REFERENCES p3a_v27_shadow.p3_candidate_revision(candidate_revision_id);


--
-- Name: p3_closure_obligation p3_closure_obligation_closure_obligation_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_closure_obligation
    ADD CONSTRAINT p3_closure_obligation_closure_obligation_id_fkey FOREIGN KEY (closure_obligation_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_closure_obligation p3_closure_obligation_left_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_closure_obligation
    ADD CONSTRAINT p3_closure_obligation_left_object_id_fkey FOREIGN KEY (left_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_closure_obligation p3_closure_obligation_right_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_closure_obligation
    ADD CONSTRAINT p3_closure_obligation_right_object_id_fkey FOREIGN KEY (right_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_closure_obligation p3_closure_resolution_adjudication_fk; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_closure_obligation
    ADD CONSTRAINT p3_closure_resolution_adjudication_fk FOREIGN KEY (resolution_adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: p3_collision_authority_source p3_collision_authority_source_collision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_collision_authority_source
    ADD CONSTRAINT p3_collision_authority_source_collision_id_fkey FOREIGN KEY (collision_id) REFERENCES p3a_v27_shadow.p3_collision_scope_registry(collision_id);


--
-- Name: p3_collision_scope_registry p3_collision_scope_registry_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_collision_scope_registry
    ADD CONSTRAINT p3_collision_scope_registry_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_collision_scope_registry p3_collision_scope_registry_collision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_collision_scope_registry
    ADD CONSTRAINT p3_collision_scope_registry_collision_id_fkey FOREIGN KEY (collision_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_collision_scope_registry p3_collision_scope_registry_left_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_collision_scope_registry
    ADD CONSTRAINT p3_collision_scope_registry_left_object_id_fkey FOREIGN KEY (left_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_collision_scope_registry p3_collision_scope_registry_right_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_collision_scope_registry
    ADD CONSTRAINT p3_collision_scope_registry_right_object_id_fkey FOREIGN KEY (right_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_component_connectivity_edge p3_component_connectivity_edge_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_component_connectivity_edge
    ADD CONSTRAINT p3_component_connectivity_edge_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_component_connectivity_edge p3_component_connectivity_edge_component_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_component_connectivity_edge
    ADD CONSTRAINT p3_component_connectivity_edge_component_id_fkey FOREIGN KEY (component_id) REFERENCES p3a_v27_shadow.p3_candidate_component(component_id);


--
-- Name: p3_component_connectivity_edge p3_component_connectivity_edge_projection_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_component_connectivity_edge
    ADD CONSTRAINT p3_component_connectivity_edge_projection_id_fkey FOREIGN KEY (projection_id) REFERENCES p3a_v27_shadow.p3_pair_projection(projection_id);


--
-- Name: p3_component_membership p3_component_membership_component_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_component_membership
    ADD CONSTRAINT p3_component_membership_component_id_fkey FOREIGN KEY (component_id) REFERENCES p3a_v27_shadow.p3_candidate_component(component_id);


--
-- Name: p3_component_membership p3_component_membership_member_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_component_membership
    ADD CONSTRAINT p3_component_membership_member_object_id_fkey FOREIGN KEY (member_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_dependency_edge p3_dependency_edge_authority_input_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_dependency_edge
    ADD CONSTRAINT p3_dependency_edge_authority_input_id_fkey FOREIGN KEY (authority_input_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_dependency_edge p3_dependency_edge_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_dependency_edge
    ADD CONSTRAINT p3_dependency_edge_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_dependency_edge p3_dependency_edge_dependency_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_dependency_edge
    ADD CONSTRAINT p3_dependency_edge_dependency_id_fkey FOREIGN KEY (dependency_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_dependency_edge p3_dependency_edge_dependent_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_dependency_edge
    ADD CONSTRAINT p3_dependency_edge_dependent_id_fkey FOREIGN KEY (dependent_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_doctrine_delta_affected_object p3_doctrine_delta_affected_object_affected_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_doctrine_delta_affected_object
    ADD CONSTRAINT p3_doctrine_delta_affected_object_affected_object_id_fkey FOREIGN KEY (affected_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_doctrine_delta_affected_object p3_doctrine_delta_affected_object_doctrine_delta_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_doctrine_delta_affected_object
    ADD CONSTRAINT p3_doctrine_delta_affected_object_doctrine_delta_id_fkey FOREIGN KEY (doctrine_delta_id) REFERENCES p3a_v27_shadow.p3_doctrine_delta(doctrine_delta_id);


--
-- Name: p3_doctrine_delta p3_doctrine_delta_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_doctrine_delta
    ADD CONSTRAINT p3_doctrine_delta_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_doctrine_delta p3_doctrine_delta_doctrine_delta_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_doctrine_delta
    ADD CONSTRAINT p3_doctrine_delta_doctrine_delta_id_fkey FOREIGN KEY (doctrine_delta_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_doctrine_delta p3_doctrine_delta_trigger_candidate_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_doctrine_delta
    ADD CONSTRAINT p3_doctrine_delta_trigger_candidate_id_fkey FOREIGN KEY (trigger_candidate_id) REFERENCES p3a_v27_shadow.p3_candidate_family(candidate_family_id);


--
-- Name: p3_excluded_object p3_excluded_object_excluded_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_excluded_object
    ADD CONSTRAINT p3_excluded_object_excluded_object_id_fkey FOREIGN KEY (excluded_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_excluded_object p3_excluded_object_exclusion_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_excluded_object
    ADD CONSTRAINT p3_excluded_object_exclusion_id_fkey FOREIGN KEY (exclusion_id) REFERENCES p3a_v27_shadow.p3_family_exclusion(exclusion_id);


--
-- Name: p3_exclusion_promotion p3_exclusion_promotion_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_exclusion_promotion
    ADD CONSTRAINT p3_exclusion_promotion_adjudication_id_fkey FOREIGN KEY (adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_exclusion_promotion p3_exclusion_promotion_candidate_exclusion_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_exclusion_promotion
    ADD CONSTRAINT p3_exclusion_promotion_candidate_exclusion_id_fkey FOREIGN KEY (candidate_exclusion_id) REFERENCES p3a_v27_shadow.p3_family_exclusion(exclusion_id);


--
-- Name: p3_exclusion_promotion p3_exclusion_promotion_canonical_exclusion_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_exclusion_promotion
    ADD CONSTRAINT p3_exclusion_promotion_canonical_exclusion_id_fkey FOREIGN KEY (canonical_exclusion_id) REFERENCES p3a_v27_shadow.p3_family_exclusion(exclusion_id);


--
-- Name: p3_failure_ledger p3_failure_ledger_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_failure_ledger
    ADD CONSTRAINT p3_failure_ledger_object_id_fkey FOREIGN KEY (object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_family_exclusion p3_family_exclusion_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_exclusion
    ADD CONSTRAINT p3_family_exclusion_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_family_exclusion p3_family_exclusion_exclusion_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_exclusion
    ADD CONSTRAINT p3_family_exclusion_exclusion_id_fkey FOREIGN KEY (exclusion_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_family_exclusion p3_family_exclusion_owner_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_exclusion
    ADD CONSTRAINT p3_family_exclusion_owner_object_id_fkey FOREIGN KEY (owner_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_family_genealogy p3_family_genealogy_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_genealogy
    ADD CONSTRAINT p3_family_genealogy_adjudication_id_fkey FOREIGN KEY (adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_family_genealogy p3_family_genealogy_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_genealogy
    ADD CONSTRAINT p3_family_genealogy_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_family_genealogy p3_family_genealogy_genealogy_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_genealogy
    ADD CONSTRAINT p3_family_genealogy_genealogy_id_fkey FOREIGN KEY (genealogy_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_family_genealogy_member p3_family_genealogy_member_family_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_genealogy_member
    ADD CONSTRAINT p3_family_genealogy_member_family_id_fkey FOREIGN KEY (family_id) REFERENCES p3a_v27_shadow.p3_canonical_family(canonical_family_id);


--
-- Name: p3_family_genealogy_member p3_family_genealogy_member_genealogy_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_genealogy_member
    ADD CONSTRAINT p3_family_genealogy_member_genealogy_id_fkey FOREIGN KEY (genealogy_id) REFERENCES p3a_v27_shadow.p3_family_genealogy(genealogy_id);


--
-- Name: p3_family_variant p3_family_variant_created_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_variant
    ADD CONSTRAINT p3_family_variant_created_release_id_fkey FOREIGN KEY (created_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_family_variant p3_family_variant_owner_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_variant
    ADD CONSTRAINT p3_family_variant_owner_object_id_fkey FOREIGN KEY (owner_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_family_variant_revision p3_family_variant_revision_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_variant_revision
    ADD CONSTRAINT p3_family_variant_revision_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_family_variant_revision p3_family_variant_revision_variant_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_variant_revision
    ADD CONSTRAINT p3_family_variant_revision_variant_id_fkey FOREIGN KEY (variant_id) REFERENCES p3a_v27_shadow.p3_family_variant(variant_id);


--
-- Name: p3_family_variant_revision p3_family_variant_revision_variant_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_variant_revision
    ADD CONSTRAINT p3_family_variant_revision_variant_revision_id_fkey FOREIGN KEY (variant_revision_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_family_variant p3_family_variant_variant_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_family_variant
    ADD CONSTRAINT p3_family_variant_variant_id_fkey FOREIGN KEY (variant_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_frozen_historical_candidate_identity p3_frozen_historical_candidat_successor_candidate_family_i_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_frozen_historical_candidate_identity
    ADD CONSTRAINT p3_frozen_historical_candidat_successor_candidate_family_i_fkey FOREIGN KEY (successor_candidate_family_id) REFERENCES p3a_v27_shadow.p3_candidate_family(candidate_family_id);


--
-- Name: p3_frozen_historical_candidate_identity p3_frozen_historical_candidate_ident_allocation_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_frozen_historical_candidate_identity
    ADD CONSTRAINT p3_frozen_historical_candidate_ident_allocation_release_id_fkey FOREIGN KEY (allocation_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_frozen_historical_candidate_identity p3_frozen_historical_candidate_identi_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_frozen_historical_candidate_identity
    ADD CONSTRAINT p3_frozen_historical_candidate_identi_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_hyperedge p3_hyperedge_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_hyperedge
    ADD CONSTRAINT p3_hyperedge_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_hyperedge p3_hyperedge_hyperedge_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_hyperedge
    ADD CONSTRAINT p3_hyperedge_hyperedge_id_fkey FOREIGN KEY (hyperedge_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_hyperedge_membership p3_hyperedge_membership_hyperedge_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_hyperedge_membership
    ADD CONSTRAINT p3_hyperedge_membership_hyperedge_id_fkey FOREIGN KEY (hyperedge_id) REFERENCES p3a_v27_shadow.p3_hyperedge(hyperedge_id);


--
-- Name: p3_hyperedge_membership p3_hyperedge_membership_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_hyperedge_membership
    ADD CONSTRAINT p3_hyperedge_membership_object_id_fkey FOREIGN KEY (object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_hyperedge_role_type_contract p3_hyperedge_role_type_contract_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_hyperedge_role_type_contract
    ADD CONSTRAINT p3_hyperedge_role_type_contract_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_identity_key_contract p3_identity_key_contract_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_identity_key_contract
    ADD CONSTRAINT p3_identity_key_contract_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_imported_lineage_membership p3_imported_lineage_membership_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_imported_lineage_membership
    ADD CONSTRAINT p3_imported_lineage_membership_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_imported_lineage_membership p3_imported_lineage_membership_implementation_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_imported_lineage_membership
    ADD CONSTRAINT p3_imported_lineage_membership_implementation_id_fkey FOREIGN KEY (implementation_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_imported_lineage_membership p3_imported_lineage_membership_lineage_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_imported_lineage_membership
    ADD CONSTRAINT p3_imported_lineage_membership_lineage_id_fkey FOREIGN KEY (lineage_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_internal_pair_closure p3_internal_pair_closure_candidate_revision_id_left_object_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_closure
    ADD CONSTRAINT p3_internal_pair_closure_candidate_revision_id_left_object_fkey FOREIGN KEY (candidate_revision_id, left_object_id, right_object_id) REFERENCES p3a_v27_shadow.p3_internal_pair_matrix(candidate_revision_id, left_object_id, right_object_id);


--
-- Name: p3_internal_pair_closure p3_internal_pair_closure_closure_obligation_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_closure
    ADD CONSTRAINT p3_internal_pair_closure_closure_obligation_id_fkey FOREIGN KEY (closure_obligation_id) REFERENCES p3a_v27_shadow.p3_closure_obligation(closure_obligation_id);


--
-- Name: p3_internal_pair_collision p3_internal_pair_collision_candidate_revision_id_left_obje_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_collision
    ADD CONSTRAINT p3_internal_pair_collision_candidate_revision_id_left_obje_fkey FOREIGN KEY (candidate_revision_id, left_object_id, right_object_id) REFERENCES p3a_v27_shadow.p3_internal_pair_matrix(candidate_revision_id, left_object_id, right_object_id);


--
-- Name: p3_internal_pair_collision p3_internal_pair_collision_collision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_collision
    ADD CONSTRAINT p3_internal_pair_collision_collision_id_fkey FOREIGN KEY (collision_id) REFERENCES p3a_v27_shadow.p3_collision_scope_registry(collision_id);


--
-- Name: p3_internal_pair_coordinate_constraint p3_internal_pair_coordinate_c_candidate_revision_id_left_o_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_coordinate_constraint
    ADD CONSTRAINT p3_internal_pair_coordinate_c_candidate_revision_id_left_o_fkey FOREIGN KEY (candidate_revision_id, left_object_id, right_object_id) REFERENCES p3a_v27_shadow.p3_internal_pair_matrix(candidate_revision_id, left_object_id, right_object_id);


--
-- Name: p3_internal_pair_coordinate_constraint p3_internal_pair_coordinate_constrain_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_coordinate_constraint
    ADD CONSTRAINT p3_internal_pair_coordinate_constrain_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_internal_pair_coordinate_constraint p3_internal_pair_coordinate_constraint_projection_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_coordinate_constraint
    ADD CONSTRAINT p3_internal_pair_coordinate_constraint_projection_id_fkey FOREIGN KEY (projection_id) REFERENCES p3a_v27_shadow.p3_pair_projection(projection_id);


--
-- Name: p3_internal_pair_matrix p3_internal_pair_matrix_candidate_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_matrix
    ADD CONSTRAINT p3_internal_pair_matrix_candidate_revision_id_fkey FOREIGN KEY (candidate_revision_id) REFERENCES p3a_v27_shadow.p3_candidate_revision(candidate_revision_id);


--
-- Name: p3_internal_pair_matrix p3_internal_pair_matrix_direct_pair_projection_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_matrix
    ADD CONSTRAINT p3_internal_pair_matrix_direct_pair_projection_id_fkey FOREIGN KEY (direct_pair_projection_id) REFERENCES p3a_v27_shadow.p3_pair_projection(projection_id);


--
-- Name: p3_internal_pair_matrix p3_internal_pair_matrix_left_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_matrix
    ADD CONSTRAINT p3_internal_pair_matrix_left_object_id_fkey FOREIGN KEY (left_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_internal_pair_matrix p3_internal_pair_matrix_right_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_matrix
    ADD CONSTRAINT p3_internal_pair_matrix_right_object_id_fkey FOREIGN KEY (right_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_internal_pair_redirect_boundary p3_internal_pair_redirect_bou_candidate_revision_id_left_o_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_redirect_boundary
    ADD CONSTRAINT p3_internal_pair_redirect_bou_candidate_revision_id_left_o_fkey FOREIGN KEY (candidate_revision_id, left_object_id, right_object_id) REFERENCES p3a_v27_shadow.p3_internal_pair_matrix(candidate_revision_id, left_object_id, right_object_id);


--
-- Name: p3_internal_pair_redirect_boundary p3_internal_pair_redirect_boundary_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_redirect_boundary
    ADD CONSTRAINT p3_internal_pair_redirect_boundary_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_internal_pair_redirect_boundary p3_internal_pair_redirect_boundary_projection_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_redirect_boundary
    ADD CONSTRAINT p3_internal_pair_redirect_boundary_projection_id_fkey FOREIGN KEY (projection_id) REFERENCES p3a_v27_shadow.p3_pair_projection(projection_id);


--
-- Name: p3_internal_pair_unresolved_boundary p3_internal_pair_unresolved_b_candidate_revision_id_left_o_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_unresolved_boundary
    ADD CONSTRAINT p3_internal_pair_unresolved_b_candidate_revision_id_left_o_fkey FOREIGN KEY (candidate_revision_id, left_object_id, right_object_id) REFERENCES p3a_v27_shadow.p3_internal_pair_matrix(candidate_revision_id, left_object_id, right_object_id);


--
-- Name: p3_internal_pair_unresolved_boundary p3_internal_pair_unresolved_boundary_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_unresolved_boundary
    ADD CONSTRAINT p3_internal_pair_unresolved_boundary_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_internal_pair_unresolved_boundary p3_internal_pair_unresolved_boundary_projection_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_internal_pair_unresolved_boundary
    ADD CONSTRAINT p3_internal_pair_unresolved_boundary_projection_id_fkey FOREIGN KEY (projection_id) REFERENCES p3a_v27_shadow.p3_pair_projection(projection_id);


--
-- Name: p3_lineage_disposition p3_lineage_disposition_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_disposition
    ADD CONSTRAINT p3_lineage_disposition_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_lineage_disposition p3_lineage_disposition_canonical_family_fk; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_disposition
    ADD CONSTRAINT p3_lineage_disposition_canonical_family_fk FOREIGN KEY (canonical_family_id) REFERENCES p3a_v27_shadow.p3_canonical_family(canonical_family_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: p3_lineage_disposition p3_lineage_disposition_canonical_family_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_disposition
    ADD CONSTRAINT p3_lineage_disposition_canonical_family_id_fkey FOREIGN KEY (canonical_family_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_lineage_disposition p3_lineage_disposition_subject_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_disposition
    ADD CONSTRAINT p3_lineage_disposition_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_lineage_participation p3_lineage_participation_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_participation
    ADD CONSTRAINT p3_lineage_participation_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_lineage_participation p3_lineage_participation_lineage_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_participation
    ADD CONSTRAINT p3_lineage_participation_lineage_id_fkey FOREIGN KEY (lineage_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_lineage_segment p3_lineage_segment_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_segment
    ADD CONSTRAINT p3_lineage_segment_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_lineage_segment_member p3_lineage_segment_member_implementation_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_segment_member
    ADD CONSTRAINT p3_lineage_segment_member_implementation_id_fkey FOREIGN KEY (implementation_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_lineage_segment_member p3_lineage_segment_member_segment_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_segment_member
    ADD CONSTRAINT p3_lineage_segment_member_segment_id_fkey FOREIGN KEY (segment_id) REFERENCES p3a_v27_shadow.p3_lineage_segment(segment_id);


--
-- Name: p3_lineage_segment p3_lineage_segment_parent_lineage_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_segment
    ADD CONSTRAINT p3_lineage_segment_parent_lineage_id_fkey FOREIGN KEY (parent_lineage_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_lineage_segment p3_lineage_segment_segment_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_lineage_segment
    ADD CONSTRAINT p3_lineage_segment_segment_id_fkey FOREIGN KEY (segment_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_object_reference_type_contract p3_object_reference_type_contract_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_object_reference_type_contract
    ADD CONSTRAINT p3_object_reference_type_contract_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_object_registry p3_object_registry_allocation_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_object_registry
    ADD CONSTRAINT p3_object_registry_allocation_release_id_fkey FOREIGN KEY (allocation_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_object_registry p3_object_registry_retired_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_object_registry
    ADD CONSTRAINT p3_object_registry_retired_release_id_fkey FOREIGN KEY (retired_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_pair_endpoint_resolution p3_pair_endpoint_resolution_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_endpoint_resolution
    ADD CONSTRAINT p3_pair_endpoint_resolution_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_pair_endpoint_resolution p3_pair_endpoint_resolution_original_lineage_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_endpoint_resolution
    ADD CONSTRAINT p3_pair_endpoint_resolution_original_lineage_id_fkey FOREIGN KEY (original_lineage_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_pair_endpoint_resolution p3_pair_endpoint_resolution_pair_fact_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_endpoint_resolution
    ADD CONSTRAINT p3_pair_endpoint_resolution_pair_fact_id_fkey FOREIGN KEY (pair_fact_id) REFERENCES p3a_v27_shadow.p3_pair_fact_bundle(pair_fact_id);


--
-- Name: p3_pair_endpoint_resolved_subject p3_pair_endpoint_resolved_subje_pair_fact_id_endpoint_side_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_endpoint_resolved_subject
    ADD CONSTRAINT p3_pair_endpoint_resolved_subje_pair_fact_id_endpoint_side_fkey FOREIGN KEY (pair_fact_id, endpoint_side) REFERENCES p3a_v27_shadow.p3_pair_endpoint_resolution(pair_fact_id, endpoint_side);


--
-- Name: p3_pair_endpoint_resolved_subject p3_pair_endpoint_resolved_subject_resolved_subject_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_endpoint_resolved_subject
    ADD CONSTRAINT p3_pair_endpoint_resolved_subject_resolved_subject_id_fkey FOREIGN KEY (resolved_subject_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_pair_fact_bundle p3_pair_fact_bundle_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_fact_bundle
    ADD CONSTRAINT p3_pair_fact_bundle_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_pair_fact_bundle p3_pair_fact_bundle_left_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_fact_bundle
    ADD CONSTRAINT p3_pair_fact_bundle_left_object_id_fkey FOREIGN KEY (left_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_pair_fact_bundle p3_pair_fact_bundle_pair_fact_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_fact_bundle
    ADD CONSTRAINT p3_pair_fact_bundle_pair_fact_id_fkey FOREIGN KEY (pair_fact_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_pair_fact_bundle p3_pair_fact_bundle_right_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_fact_bundle
    ADD CONSTRAINT p3_pair_fact_bundle_right_object_id_fkey FOREIGN KEY (right_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_pair_fact_evidence p3_pair_fact_evidence_pair_fact_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_fact_evidence
    ADD CONSTRAINT p3_pair_fact_evidence_pair_fact_id_fkey FOREIGN KEY (pair_fact_id) REFERENCES p3a_v27_shadow.p3_pair_fact_bundle(pair_fact_id);


--
-- Name: p3_pair_fact_source_authority p3_pair_fact_source_authority_pair_fact_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_fact_source_authority
    ADD CONSTRAINT p3_pair_fact_source_authority_pair_fact_id_fkey FOREIGN KEY (pair_fact_id) REFERENCES p3a_v27_shadow.p3_pair_fact_bundle(pair_fact_id);


--
-- Name: p3_pair_projection p3_pair_projection_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_projection
    ADD CONSTRAINT p3_pair_projection_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_pair_projection p3_pair_projection_left_subject_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_projection
    ADD CONSTRAINT p3_pair_projection_left_subject_id_fkey FOREIGN KEY (left_subject_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_pair_projection p3_pair_projection_pair_fact_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_projection
    ADD CONSTRAINT p3_pair_projection_pair_fact_id_fkey FOREIGN KEY (pair_fact_id) REFERENCES p3a_v27_shadow.p3_pair_fact_bundle(pair_fact_id);


--
-- Name: p3_pair_projection p3_pair_projection_projection_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_projection
    ADD CONSTRAINT p3_pair_projection_projection_id_fkey FOREIGN KEY (projection_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_pair_projection p3_pair_projection_right_subject_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_pair_projection
    ADD CONSTRAINT p3_pair_projection_right_subject_id_fkey FOREIGN KEY (right_subject_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_proposition_signature p3_proposition_signature_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_proposition_signature
    ADD CONSTRAINT p3_proposition_signature_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_proposition_signature p3_proposition_signature_signature_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_proposition_signature
    ADD CONSTRAINT p3_proposition_signature_signature_id_fkey FOREIGN KEY (signature_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_proposition_signature p3_proposition_signature_subject_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_proposition_signature
    ADD CONSTRAINT p3_proposition_signature_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_release_change_ledger p3_release_change_ledger_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_release_change_ledger
    ADD CONSTRAINT p3_release_change_ledger_object_id_fkey FOREIGN KEY (object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_release_change_ledger p3_release_change_ledger_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_release_change_ledger
    ADD CONSTRAINT p3_release_change_ledger_release_id_fkey FOREIGN KEY (release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_release_lifecycle_transition p3_release_lifecycle_transition_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_release_lifecycle_transition
    ADD CONSTRAINT p3_release_lifecycle_transition_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_release_object_snapshot p3_release_object_snapshot_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_release_object_snapshot
    ADD CONSTRAINT p3_release_object_snapshot_object_id_fkey FOREIGN KEY (object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_release_object_snapshot p3_release_object_snapshot_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_release_object_snapshot
    ADD CONSTRAINT p3_release_object_snapshot_release_id_fkey FOREIGN KEY (release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_release_status_event p3_release_status_event_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_release_status_event
    ADD CONSTRAINT p3_release_status_event_release_id_fkey FOREIGN KEY (release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_response_contract_reference p3_response_contract_reference_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_response_contract_reference
    ADD CONSTRAINT p3_response_contract_reference_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_response_contract_reference p3_response_contract_reference_reference_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_response_contract_reference
    ADD CONSTRAINT p3_response_contract_reference_reference_id_fkey FOREIGN KEY (reference_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_response_contract_reference p3_response_contract_reference_subject_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_response_contract_reference
    ADD CONSTRAINT p3_response_contract_reference_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_runtime_promotion_pointer p3_runtime_promotion_pointer_promoted_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_runtime_promotion_pointer
    ADD CONSTRAINT p3_runtime_promotion_pointer_promoted_release_id_fkey FOREIGN KEY (promoted_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_signature_field_evidence p3_signature_field_evidence_signature_id_field_name_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_signature_field_evidence
    ADD CONSTRAINT p3_signature_field_evidence_signature_id_field_name_fkey FOREIGN KEY (signature_id, field_name) REFERENCES p3a_v27_shadow.p3_signature_field(signature_id, field_name);


--
-- Name: p3_signature_field p3_signature_field_signature_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_signature_field
    ADD CONSTRAINT p3_signature_field_signature_id_fkey FOREIGN KEY (signature_id) REFERENCES p3a_v27_shadow.p3_proposition_signature(signature_id);


--
-- Name: p3_structural_context_reference p3_structural_context_reference_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_structural_context_reference
    ADD CONSTRAINT p3_structural_context_reference_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_structural_context_reference p3_structural_context_reference_reference_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_structural_context_reference
    ADD CONSTRAINT p3_structural_context_reference_reference_id_fkey FOREIGN KEY (reference_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_structural_context_reference p3_structural_context_reference_subject_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_structural_context_reference
    ADD CONSTRAINT p3_structural_context_reference_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_upstream_object_reference p3_upstream_object_reference_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_upstream_object_reference
    ADD CONSTRAINT p3_upstream_object_reference_object_id_fkey FOREIGN KEY (object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_variant_membership p3_variant_membership_member_object_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_variant_membership
    ADD CONSTRAINT p3_variant_membership_member_object_id_fkey FOREIGN KEY (member_object_id) REFERENCES p3a_v27_shadow.p3_object_registry(object_id);


--
-- Name: p3_variant_membership p3_variant_membership_variant_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_variant_membership
    ADD CONSTRAINT p3_variant_membership_variant_revision_id_fkey FOREIGN KEY (variant_revision_id) REFERENCES p3a_v27_shadow.p3_family_variant_revision(variant_revision_id);


--
-- Name: p3_variant_promotion p3_variant_promotion_adjudication_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_variant_promotion
    ADD CONSTRAINT p3_variant_promotion_adjudication_id_fkey FOREIGN KEY (adjudication_id) REFERENCES p3a_v27_shadow.p3_adjudication_decision(adjudication_id);


--
-- Name: p3_variant_promotion p3_variant_promotion_candidate_variant_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_variant_promotion
    ADD CONSTRAINT p3_variant_promotion_candidate_variant_revision_id_fkey FOREIGN KEY (candidate_variant_revision_id) REFERENCES p3a_v27_shadow.p3_family_variant_revision(variant_revision_id);


--
-- Name: p3_variant_promotion p3_variant_promotion_canonical_variant_revision_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_variant_promotion
    ADD CONSTRAINT p3_variant_promotion_canonical_variant_revision_id_fkey FOREIGN KEY (canonical_variant_revision_id) REFERENCES p3a_v27_shadow.p3_family_variant_revision(variant_revision_id);


--
-- Name: p3_vocabulary_code p3_vocabulary_code_introduced_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_vocabulary_code
    ADD CONSTRAINT p3_vocabulary_code_introduced_release_id_fkey FOREIGN KEY (introduced_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_vocabulary_code p3_vocabulary_code_retired_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_vocabulary_code
    ADD CONSTRAINT p3_vocabulary_code_retired_release_id_fkey FOREIGN KEY (retired_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_vocabulary_revision p3_vocabulary_revision_authority_release_id_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_vocabulary_revision
    ADD CONSTRAINT p3_vocabulary_revision_authority_release_id_fkey FOREIGN KEY (authority_release_id) REFERENCES p3a_v27_shadow.p3_authority_release(release_id);


--
-- Name: p3_vocabulary_revision p3_vocabulary_revision_vocabulary_domain_code_fkey; Type: FK CONSTRAINT; Schema: p3a_v27_shadow; Owner: rawlsing_p3a_owner
--

ALTER TABLE ONLY p3a_v27_shadow.p3_vocabulary_revision
    ADD CONSTRAINT p3_vocabulary_revision_vocabulary_domain_code_fkey FOREIGN KEY (vocabulary_domain, code) REFERENCES p3a_v27_shadow.p3_vocabulary_code(vocabulary_domain, code);


--
-- PostgreSQL database dump complete
--

\unrestrict LtCdHEzHHRfhHLI7UYmcCFQmhW1AtE6DMMfcmiNWU7dFUNLjerG7Zc5jjZSj6qF

