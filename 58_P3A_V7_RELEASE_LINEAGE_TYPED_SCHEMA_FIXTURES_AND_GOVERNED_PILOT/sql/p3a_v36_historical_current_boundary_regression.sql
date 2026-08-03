\set ON_ERROR_STOP on
SET search_path TO p3a_v27_shadow, public;
\pset format unaligned
\pset tuples_only on

SELECT 'frozen_identity_count', count(*) FROM p3_frozen_historical_candidate_identity;
SELECT 'fabricated_historical_revisions', count(*) FROM p3_candidate_revision WHERE revision_number=1 AND authority_release_id IN ('P3-AUTHORITY-2026-08-01-R31','P3-AUTHORITY-2026-08-01-R35');
SELECT 'current_r36_revisions', count(*) FROM p3_candidate_revision WHERE authority_release_id='P3-AUTHORITY-2026-08-01-R36';
SELECT 'bad_current_base_candidates', count(*)
FROM p3_candidate_revision cr
LEFT JOIN (SELECT candidate_revision_id,count(*) n FROM p3_candidate_component_link GROUP BY 1) cl USING(candidate_revision_id)
LEFT JOIN (SELECT candidate_revision_id,count(*) n FROM p3_candidate_attachment_projection GROUP BY 1) ap USING(candidate_revision_id)
WHERE cr.authority_release_id='P3-AUTHORITY-2026-08-01-R36'
  AND cr.candidate_origin_type IN ('STRICT_RESPONSE_COMPONENT','PROPOSITION_ONLY_SEED')
  AND (coalesce(cl.n,0)<>1 OR coalesce(ap.n,0)<>0);
SELECT 'historical_runtime_addressable', count(*)
FROM p3_frozen_historical_candidate_identity h
JOIN p3_candidate_revision cr ON cr.candidate_revision_id=h.historical_object_id;
SELECT 'successor_mapping_rows', count(*) FROM p3_frozen_historical_candidate_identity WHERE successor_candidate_revision_id IS NOT NULL;

BEGIN;
DO $$ BEGIN
  BEGIN
    UPDATE p3_frozen_historical_candidate_identity
       SET migration_reason='mutated'
     WHERE historical_identity_id=(SELECT historical_identity_id FROM p3_frozen_historical_candidate_identity LIMIT 1);
    RAISE EXCEPTION 'frozen identity mutation unexpectedly succeeded';
  EXCEPTION WHEN raise_exception THEN
    IF SQLERRM NOT LIKE 'P3 append-only authority table%' THEN RAISE; END IF;
  END;
END $$;
ROLLBACK;
SELECT 'frozen_identity_mutation_rejected', 'PASS';

BEGIN;
DO $$ DECLARE fam text; rev text; BEGIN
  fam := 'P3CAND-999902';
  rev := 'P3CANDREV-999902-R0001';
  INSERT INTO p3_object_registry(object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,allocation_release_id,retired_release_id,content_hash,stable_identity_note)
  VALUES
    (fam,'CANDIDATE_FAMILY','REGISTRY_ALLOCATED_DURABLE_ID','regression-malformed-family','REGRESSION','regression','P3-AUTHORITY-2026-08-01-R36',NULL,NULL,'Regression malformed family'),
    (rev,'CANDIDATE_REVISION','REGISTRY_ALLOCATED_DURABLE_ID','regression-malformed-family:R0001','REGRESSION',fam,'P3-AUTHORITY-2026-08-01-R36',NULL,NULL,'Regression malformed revision');
  INSERT INTO p3_candidate_family(candidate_family_id,created_release_id) VALUES (fam,'P3-AUTHORITY-2026-08-01-R36');
  INSERT INTO p3_candidate_revision(candidate_revision_id,candidate_family_id,revision_number,candidate_classification,candidate_origin_type,origin_key,canonical_signature_id,evidence_bundle_hash,authority_release_id)
  VALUES (rev,fam,1,'INSUFFICIENT_AUTHORITY_RISK','STRICT_RESPONSE_COMPONENT',repeat('3',64),NULL,repeat('4',64),'P3-AUTHORITY-2026-08-01-R36');
  SET CONSTRAINTS ALL IMMEDIATE;
  RAISE EXCEPTION 'malformed R36 base candidate unexpectedly succeeded';
EXCEPTION WHEN raise_exception THEN
  IF SQLERRM NOT LIKE 'base candidate % requires exactly one component and no attachment projection%' THEN RAISE; END IF;
END $$;
ROLLBACK;
SELECT 'malformed_r36_base_candidate_rejected', 'PASS';

BEGIN;
DO $$ DECLARE fam text; rev text; comp text; template_rev text; BEGIN
  fam := 'P3CAND-999903';
  rev := 'P3CANDREV-999903-R0001';
  SELECT candidate_revision_id INTO template_rev FROM p3_candidate_revision WHERE candidate_origin_type='STRICT_RESPONSE_COMPONENT' ORDER BY candidate_revision_id LIMIT 1;
  SELECT component_id INTO comp FROM p3_candidate_component_link WHERE candidate_revision_id=template_rev LIMIT 1;
  INSERT INTO p3_object_registry(object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,allocation_release_id,retired_release_id,content_hash,stable_identity_note)
  VALUES
    (fam,'CANDIDATE_FAMILY','REGISTRY_ALLOCATED_DURABLE_ID','regression-valid-family','REGRESSION','regression','P3-AUTHORITY-2026-08-01-R36',NULL,NULL,'Regression valid family'),
    (rev,'CANDIDATE_REVISION','REGISTRY_ALLOCATED_DURABLE_ID','regression-valid-family:R0001','REGRESSION',fam,'P3-AUTHORITY-2026-08-01-R36',NULL,NULL,'Regression valid revision');
  INSERT INTO p3_candidate_family(candidate_family_id,created_release_id) VALUES (fam,'P3-AUTHORITY-2026-08-01-R36');
  INSERT INTO p3_candidate_revision(candidate_revision_id,candidate_family_id,revision_number,candidate_classification,candidate_origin_type,origin_key,canonical_signature_id,evidence_bundle_hash,authority_release_id)
  VALUES (rev,fam,1,'INSUFFICIENT_AUTHORITY_RISK','STRICT_RESPONSE_COMPONENT',repeat('5',64),NULL,repeat('6',64),'P3-AUTHORITY-2026-08-01-R36');
  INSERT INTO p3_candidate_component_link(candidate_revision_id,component_id) VALUES (rev,comp);
  INSERT INTO p3_candidate_membership(candidate_revision_id,member_object_id,membership_role,membership_basis,authority_release_id)
  SELECT rev,member_object_id,'PROPOSED_MEMBER','COMPONENT_MEMBER','P3-AUTHORITY-2026-08-01-R36'
  FROM p3_component_membership WHERE component_id=comp;
  INSERT INTO p3_internal_pair_matrix(candidate_revision_id,left_object_id,right_object_id,pair_state,direct_pair_projection_id)
  SELECT rev,left_object_id,right_object_id,pair_state,direct_pair_projection_id
  FROM p3_internal_pair_matrix WHERE candidate_revision_id=template_rev;
  SET CONSTRAINTS ALL IMMEDIATE;
END $$;
ROLLBACK;
SELECT 'valid_r36_base_candidate_commits_in_rollback_fixture', 'PASS';

SELECT 'regression_fixture_rows_persisted', count(*)
FROM p3_object_registry
WHERE object_id LIKE 'P3CAND-99990%' OR object_id LIKE 'P3CANDREV-99990%';
