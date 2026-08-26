\set ON_ERROR_STOP on
BEGIN;

-- Contract release. It contains no adjudication; it installs the replay invariants.
INSERT INTO p3_authority_release(
  release_id,parent_release_id,schema_version,builder_version,input_manifest_hash,created_at,
  object_counts,validation_return_hash,migration_artifact,rollback_artifact)
VALUES (
  'P3-AUTHORITY-2026-08-02-R41','P3-AUTHORITY-2026-08-01-R40','p3-v7-p3c-replay-v1',
  'p3c-evidence-first-replay-v1','30ca921f23ab88350a256e06daae35a0cfcd074c625db9388f3310f7c257374b',TIMESTAMPTZ '2026-08-02 11:59:59+00',
  '{"contract_only":true}'::jsonb,'78743e74e59117f8c04a163d25262c75c194cc434d1584c1b3cd80b7d33b0155',
  '84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/sql/p3c_replay_contract_v1.sql',
  'restore Section 83 PostgreSQL dump');

INSERT INTO p3_identity_key_contract(object_type,identity_strategy,id_pattern,idempotency_key_spec,authority_release_id)
SELECT object_type,identity_strategy,id_pattern,idempotency_key_spec,'P3-AUTHORITY-2026-08-02-R41'
FROM p3_identity_key_contract WHERE authority_release_id='P3-AUTHORITY-2026-08-01-R40';
INSERT INTO p3_vocabulary_revision(vocabulary_domain,code,authority_release_id,label,definition,authority_effect,deprecated)
SELECT vocabulary_domain,code,'P3-AUTHORITY-2026-08-02-R41',label,definition,authority_effect,deprecated
FROM p3_vocabulary_revision WHERE authority_release_id='P3-AUTHORITY-2026-08-01-R40';

INSERT INTO p3_candidate_lifecycle_transition(from_stage,to_stage,guard_text,authority_release_id)
SELECT from_stage,to_stage,guard_text,'P3-AUTHORITY-2026-08-02-R41'
FROM p3_candidate_lifecycle_transition WHERE authority_release_id='P3-AUTHORITY-2026-08-01-R40';
INSERT INTO p3_release_lifecycle_transition(from_status,to_status,guard_text,authority_release_id)
SELECT from_status,to_status,guard_text,'P3-AUTHORITY-2026-08-02-R41'
FROM p3_release_lifecycle_transition WHERE authority_release_id='P3-AUTHORITY-2026-08-01-R40';

-- P3C split successors are a new governed candidate-origin code.
INSERT INTO p3_vocabulary_code(vocabulary_domain,code,introduced_release_id)
VALUES ('candidate_origin_type','P3C_SPLIT_SUCCESSOR','P3-AUTHORITY-2026-08-02-R41');
INSERT INTO p3_vocabulary_revision(vocabulary_domain,code,authority_release_id,label,definition,authority_effect,deprecated)
VALUES ('candidate_origin_type','P3C_SPLIT_SUCCESSOR','P3-AUTHORITY-2026-08-02-R41',
        'P3C split successor','Exact candidate materialized from a governed P3C split-result partition.',
        'Permits only an exact singleton successor with no borrowed P3A connectivity.',false);
DROP TRIGGER p3_vocab_d2d7c618ca113de6 ON p3_candidate_revision;
CREATE TRIGGER p3_vocab_d2d7c618ca113de6 BEFORE INSERT OR UPDATE OF candidate_origin_type ON p3_candidate_revision
FOR EACH ROW EXECUTE FUNCTION p3_enforce_vocab_code('candidate_origin_type','candidate_origin_type','P3-AUTHORITY-2026-08-02-R41');

INSERT INTO p3_vocabulary_code(vocabulary_domain,code,introduced_release_id)
VALUES ('candidate_membership_basis','P3C_SPLIT_RESULT','P3-AUTHORITY-2026-08-02-R41');
INSERT INTO p3_vocabulary_revision(vocabulary_domain,code,authority_release_id,label,definition,authority_effect,deprecated)
VALUES ('candidate_membership_basis','P3C_SPLIT_RESULT','P3-AUTHORITY-2026-08-02-R41',
        'P3C split result','Membership follows an exact governed P3C split-result partition.',
        'Authorizes the exact successor membership only.',false);
DROP TRIGGER p3_vocab_b63a86e15199f583 ON p3_candidate_membership;
CREATE TRIGGER p3_vocab_b63a86e15199f583 BEFORE INSERT OR UPDATE OF membership_basis ON p3_candidate_membership
FOR EACH ROW EXECUTE FUNCTION p3_enforce_vocab_code('candidate_membership_basis','membership_basis','P3-AUTHORITY-2026-08-02-R41');

INSERT INTO p3_vocabulary_code(vocabulary_domain,code,introduced_release_id)
VALUES ('adjudication_member_disposition','ALREADY_CANONICAL','P3-AUTHORITY-2026-08-02-R41');
INSERT INTO p3_vocabulary_revision(vocabulary_domain,code,authority_release_id,label,definition,authority_effect,deprecated)
VALUES ('adjudication_member_disposition','ALREADY_CANONICAL','P3-AUTHORITY-2026-08-02-R41',
        'Already canonical','Candidate member is already present in the exact predecessor canonical-family revision.',
        'Adds evidence without duplicating canonical membership.',false);
DROP TRIGGER p3_vocab_a810fa0b2a89b486 ON p3_adjudication_member;
CREATE TRIGGER p3_vocab_a810fa0b2a89b486 BEFORE INSERT OR UPDATE OF member_disposition ON p3_adjudication_member
FOR EACH ROW EXECUTE FUNCTION p3_enforce_vocab_code('adjudication_member_disposition','member_disposition','P3-AUTHORITY-2026-08-02-R41');

INSERT INTO p3_release_status_event VALUES
 ('P3-AUTHORITY-2026-08-02-R41',1,'DRAFT',TIMESTAMPTZ '2026-08-02 11:59:59.000001+00','93020e407d3a25999a6dfe97a4ba03ce84aeea04599c0951cc94ec9132ed15f0'),
 ('P3-AUTHORITY-2026-08-02-R41',2,'VALIDATED',TIMESTAMPTZ '2026-08-02 11:59:59.000002+00','bba6ef0de57bb349e72685ec5c668022667f4d22dd2e5dea287d701223892f9a'),
 ('P3-AUTHORITY-2026-08-02-R41',3,'SHADOW',TIMESTAMPTZ '2026-08-02 11:59:59.000003+00','1a89791de0102e6774e5b437210ada4eb25c3d076bf1a29a187347aa06444087'),
 ('P3-AUTHORITY-2026-08-02-R41',4,'PROMOTED',TIMESTAMPTZ '2026-08-02 11:59:59.000004+00','64ab63c7c7ed248040a75000b7b564c38d15d2a4a79d787497c99f8e12b6a2bd');

-- Overlapping candidates need an exact non-admission disposition.
ALTER TABLE p3_candidate_ranking DROP CONSTRAINT p3_candidate_ranking_lineage_count_check;
ALTER TABLE p3_candidate_ranking ADD CONSTRAINT p3_candidate_ranking_lineage_count_check CHECK(lineage_count>=1);

ALTER TABLE p3_candidate_membership DROP CONSTRAINT p3_candidate_membership_membership_basis_check;
ALTER TABLE p3_candidate_membership ADD CONSTRAINT p3_candidate_membership_membership_basis_check
  CHECK(membership_basis IN ('COMPONENT_MEMBER','ATTACHMENT_PROJECTION','DIRECT_DIAGNOSTIC','HIERARCHICAL_CONTEXT','P3C_SPLIT_RESULT'));

ALTER TABLE p3_adjudication_member DROP CONSTRAINT p3_adjudication_member_member_disposition_check;
ALTER TABLE p3_adjudication_member ADD CONSTRAINT p3_adjudication_member_member_disposition_check
  CHECK(member_disposition IN ('ACCEPT','ALREADY_CANONICAL','EXCLUDE','HIERARCHICAL','UNRESOLVED','SPLIT'));

CREATE TABLE p3_replay_obligation_baseline AS
SELECT closure_obligation_id,candidate_revision_id,left_object_id,right_object_id,obligation_type
FROM p3_closure_obligation WHERE status='OPEN';
ALTER TABLE p3_replay_obligation_baseline ADD PRIMARY KEY(closure_obligation_id);

CREATE TABLE p3_singleton_split_authority (
  candidate_revision_id TEXT PRIMARY KEY REFERENCES p3_candidate_revision(candidate_revision_id) DEFERRABLE INITIALLY DEFERRED,
  parent_adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id) DEFERRABLE INITIALLY DEFERRED,
  parent_candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id),
  exact_member_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
  evidence_hash CHAR(64) NOT NULL CHECK(evidence_hash ~ '^[0-9a-f]{64}$'),
  authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);
CREATE TABLE p3_family_revision_predecessor (
  family_revision_id TEXT PRIMARY KEY REFERENCES p3_canonical_family_revision(family_revision_id) DEFERRABLE INITIALLY DEFERRED,
  predecessor_family_revision_id TEXT REFERENCES p3_canonical_family_revision(family_revision_id),
  predecessor_membership_hash CHAR(64) NOT NULL CHECK(predecessor_membership_hash ~ '^[0-9a-f]{64}$'),
  extension_rule TEXT NOT NULL CHECK(extension_rule IN ('NEW_FAMILY','PREDECESSOR_UNION_NEW_ACCEPTS','EVIDENCE_ONLY_CONFIRMATION')),
  authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);
CREATE TABLE p3_adjudication_pair_resolution (
  adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id) DEFERRABLE INITIALLY DEFERRED,
  closure_obligation_id TEXT NOT NULL REFERENCES p3_closure_obligation(closure_obligation_id),
  resolution_status TEXT NOT NULL CHECK(resolution_status IN ('RESOLVED_ACCEPT','RESOLVED_SPLIT','RESOLVED_EXCLUDE')),
  rationale TEXT NOT NULL,
  evidence_hash CHAR(64) NOT NULL CHECK(evidence_hash ~ '^[0-9a-f]{64}$'),
  authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
  PRIMARY KEY(adjudication_id,closure_obligation_id), UNIQUE(closure_obligation_id)
);
CREATE TABLE p3_adjudication_stronger_boundary_resolution (
  adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id) DEFERRABLE INITIALLY DEFERRED,
  boundary_kind TEXT NOT NULL CHECK(boundary_kind IN ('HIERARCHICAL_ONLY','UNRESOLVED_BOUNDARY','REDIRECT_BOUNDARY','COORDINATE_CONSTRAINT')),
  boundary_key TEXT NOT NULL,
  left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
  right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
  disposition TEXT NOT NULL CHECK(disposition IN ('CONTEXT_RESTORED_ACCEPT','PROPOSITION_IDENTITY_ACCEPT_VALUE_PORTABILITY_DENIED','SPLIT_BOUNDARY','EXCLUDE_BOUNDARY')),
  rationale TEXT NOT NULL,
  evidence_hash CHAR(64) NOT NULL CHECK(evidence_hash ~ '^[0-9a-f]{64}$'),
  authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
  PRIMARY KEY(adjudication_id,boundary_kind,boundary_key)
);

-- Candidate lifecycle is release-neutral: later authority releases append events to immutable candidates.
CREATE OR REPLACE FUNCTION p3_validate_candidate_status_event() RETURNS trigger AS $$
DECLARE p_stage TEXT; p_ord INTEGER; revision_family TEXT;
BEGIN
  SELECT candidate_family_id INTO revision_family FROM p3_candidate_revision WHERE candidate_revision_id=NEW.candidate_revision_id;
  IF revision_family IS DISTINCT FROM NEW.candidate_family_id THEN RAISE EXCEPTION 'Candidate event revision/family mismatch'; END IF;
  SELECT to_stage,event_ordinal INTO p_stage,p_ord FROM p3_candidate_status_event WHERE candidate_revision_id=NEW.candidate_revision_id ORDER BY event_ordinal DESC LIMIT 1;
  IF p_ord IS NULL THEN
    IF NEW.event_ordinal<>1 OR NEW.from_stage IS NOT NULL OR NEW.to_stage<>'DISCOVERED' THEN RAISE EXCEPTION 'Invalid first candidate revision event'; END IF;
  ELSE
    IF NEW.event_ordinal<>p_ord+1 OR NEW.from_stage IS DISTINCT FROM p_stage THEN RAISE EXCEPTION 'Noncontiguous candidate revision event'; END IF;
    IF NOT EXISTS (SELECT 1 FROM p3_candidate_lifecycle_transition t WHERE t.from_stage=NEW.from_stage AND t.to_stage=NEW.to_stage) THEN RAISE EXCEPTION 'Disallowed candidate transition % -> %',NEW.from_stage,NEW.to_stage; END IF;
  END IF;
  RETURN NEW;
END; $$ LANGUAGE plpgsql;

-- Split successors are exact P3C products, not borrowed P3A components.
CREATE OR REPLACE FUNCTION p3_assert_candidate_origin(p_revision TEXT) RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE v_origin TEXT; v_components INTEGER; v_attachments INTEGER; v_missing INTEGER; v_extra INTEGER; v_members INTEGER;
BEGIN
  SELECT candidate_origin_type INTO v_origin FROM p3_candidate_revision WHERE candidate_revision_id=p_revision;
  IF NOT FOUND THEN RAISE EXCEPTION 'unknown candidate revision %',p_revision; END IF;
  SELECT COUNT(*) INTO v_components FROM p3_candidate_component_link WHERE candidate_revision_id=p_revision;
  SELECT COUNT(*) INTO v_attachments FROM p3_candidate_attachment_projection WHERE candidate_revision_id=p_revision;
  IF v_origin IN ('STRICT_RESPONSE_COMPONENT','PROPOSITION_ONLY_SEED') THEN
    IF v_components<>1 OR v_attachments<>0 THEN RAISE EXCEPTION 'base candidate % requires exactly one component and no attachment projection',p_revision; END IF;
    SELECT COUNT(*) INTO v_missing FROM (SELECT cm.member_object_id FROM p3_component_membership cm JOIN p3_candidate_component_link cl USING(component_id) WHERE cl.candidate_revision_id=p_revision EXCEPT SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=p_revision AND membership_role='PROPOSED_MEMBER') q;
    SELECT COUNT(*) INTO v_extra FROM (SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=p_revision AND membership_role='PROPOSED_MEMBER' EXCEPT SELECT cm.member_object_id FROM p3_component_membership cm JOIN p3_candidate_component_link cl USING(component_id) WHERE cl.candidate_revision_id=p_revision) q;
  ELSIF v_origin='ATTACHMENT_REVIEW' THEN
    IF v_attachments<1 THEN RAISE EXCEPTION 'attachment review requires at least one attachment projection'; END IF;
    WITH expected AS (SELECT cm.member_object_id FROM p3_component_membership cm JOIN p3_candidate_component_link cl USING(component_id) WHERE cl.candidate_revision_id=p_revision UNION SELECT pp.left_subject_id FROM p3_pair_projection pp JOIN p3_candidate_attachment_projection ap USING(projection_id) WHERE ap.candidate_revision_id=p_revision UNION SELECT pp.right_subject_id FROM p3_pair_projection pp JOIN p3_candidate_attachment_projection ap USING(projection_id) WHERE ap.candidate_revision_id=p_revision)
    SELECT COUNT(*) INTO v_missing FROM (SELECT member_object_id FROM expected EXCEPT SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=p_revision AND membership_role='PROPOSED_MEMBER') q;
    WITH expected AS (SELECT cm.member_object_id FROM p3_component_membership cm JOIN p3_candidate_component_link cl USING(component_id) WHERE cl.candidate_revision_id=p_revision UNION SELECT pp.left_subject_id FROM p3_pair_projection pp JOIN p3_candidate_attachment_projection ap USING(projection_id) WHERE ap.candidate_revision_id=p_revision UNION SELECT pp.right_subject_id FROM p3_pair_projection pp JOIN p3_candidate_attachment_projection ap USING(projection_id) WHERE ap.candidate_revision_id=p_revision)
    SELECT COUNT(*) INTO v_extra FROM (SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=p_revision AND membership_role='PROPOSED_MEMBER' EXCEPT SELECT member_object_id FROM expected) q;
  ELSIF v_origin='NONCONNECTIVE_DIAGNOSTIC_CASE' THEN
    IF v_components<>0 OR v_attachments<>0 THEN RAISE EXCEPTION 'diagnostic candidate cannot borrow graph connectivity'; END IF; v_missing:=0;v_extra:=0;
  ELSIF v_origin='P3C_SPLIT_SUCCESSOR' THEN
    SELECT COUNT(*) INTO v_members FROM p3_candidate_membership WHERE candidate_revision_id=p_revision AND membership_role='PROPOSED_MEMBER';
    IF v_components<>0 OR v_attachments<>0 OR v_members<>1 THEN RAISE EXCEPTION 'split successor % must be an exact singleton with no borrowed connectivity',p_revision; END IF; v_missing:=0;v_extra:=0;
  ELSE RAISE EXCEPTION 'unknown candidate origin %',v_origin;
  END IF;
  IF COALESCE(v_missing,0)<>0 OR COALESCE(v_extra,0)<>0 THEN RAISE EXCEPTION 'candidate origin membership mismatch: missing %, extra %',v_missing,v_extra; END IF;
END $$;

CREATE OR REPLACE FUNCTION p3_validate_adjudication_completeness() RETURNS trigger AS $$
DECLARE aid TEXT; a RECORD; n_new INTEGER; n_old INTEGER; prior TEXT;
BEGIN
  aid:=COALESCE(NEW.adjudication_id,OLD.adjudication_id); SELECT * INTO a FROM p3_adjudication_decision WHERE adjudication_id=aid;
  IF a.adjudication_id IS NULL THEN RETURN COALESCE(NEW,OLD); END IF;
  IF a.decision_ordinal=1 AND a.supersedes_adjudication_id IS NOT NULL THEN RAISE EXCEPTION 'First decision cannot supersede another'; END IF;
  IF a.decision_ordinal>1 THEN SELECT adjudication_id INTO prior FROM p3_adjudication_decision WHERE candidate_revision_id=a.candidate_revision_id AND decision_ordinal=a.decision_ordinal-1; IF prior IS NULL OR a.supersedes_adjudication_id IS DISTINCT FROM prior THEN RAISE EXCEPTION 'Decision supersession chain is not exact'; END IF; END IF;
  IF a.decision_status IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') THEN
    SELECT COUNT(*) FILTER(WHERE member_disposition='ACCEPT'),COUNT(*) FILTER(WHERE member_disposition='ALREADY_CANONICAL') INTO n_new,n_old FROM p3_adjudication_member WHERE adjudication_id=aid;
    IF n_new+n_old<2 AND NOT EXISTS (SELECT 1 FROM p3_singleton_split_authority s WHERE s.candidate_revision_id=a.candidate_revision_id AND s.parent_adjudication_id IS NOT NULL) THEN RAISE EXCEPTION 'Accepted decision requires two governed members or exact singleton split authority'; END IF;
  END IF;
  IF a.decision_status='ACCEPTED_WITH_VARIANTS' AND NOT EXISTS (SELECT 1 FROM p3_adjudication_member WHERE adjudication_id=aid AND member_disposition IN ('ACCEPT','ALREADY_CANONICAL') AND variant_revision_id IS NOT NULL) THEN RAISE EXCEPTION 'Variant acceptance requires variant assignment'; END IF;
  IF a.decision_status='SPLIT_REQUIRED' AND NOT EXISTS (SELECT 1 FROM p3_adjudication_split_point WHERE adjudication_id=aid) THEN RAISE EXCEPTION 'Split decision requires split point'; END IF;
  IF a.decision_status='HIERARCHICAL_RELATION_ONLY' AND NOT EXISTS (SELECT 1 FROM p3_adjudication_hierarchy_relation WHERE adjudication_id=aid) THEN RAISE EXCEPTION 'Hierarchy decision requires hierarchy row'; END IF;
  IF a.decision_status IN ('BLOCKED_UNRESOLVED','INSUFFICIENT_AUTHORITY') AND NOT EXISTS (SELECT 1 FROM p3_adjudication_unresolved_boundary WHERE adjudication_id=aid) THEN RAISE EXCEPTION 'Blocked decision requires unresolved boundary'; END IF;
  RETURN COALESCE(NEW,OLD);
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_assert_canonical_promotion_closure(p_adjudication TEXT) RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE v_status TEXT; v_family TEXT; v_revision TEXT; v_pred TEXT; v_rule TEXT; v_missing INTEGER; v_extra INTEGER; v_bad INTEGER;
BEGIN
  SELECT decision_status,canonical_family_id INTO v_status,v_family FROM p3_adjudication_decision WHERE adjudication_id=p_adjudication;
  IF v_status NOT IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') THEN RETURN; END IF;
  SELECT family_revision_id INTO v_revision FROM p3_canonical_family_revision WHERE created_by_adjudication_id=p_adjudication;
  IF NOT FOUND THEN RAISE EXCEPTION 'accepted adjudication lacks canonical family revision'; END IF;
  SELECT predecessor_family_revision_id,extension_rule INTO v_pred,v_rule FROM p3_family_revision_predecessor WHERE family_revision_id=v_revision;
  IF NOT FOUND THEN RAISE EXCEPTION 'family revision lacks predecessor contract'; END IF;
  WITH expected AS (
    SELECT member_object_id FROM p3_canonical_family_membership WHERE family_revision_id=v_pred
    UNION SELECT member_object_id FROM p3_adjudication_member WHERE adjudication_id=p_adjudication AND member_disposition='ACCEPT')
  SELECT COUNT(*) INTO v_missing FROM (SELECT member_object_id FROM expected EXCEPT SELECT member_object_id FROM p3_canonical_family_membership WHERE family_revision_id=v_revision) q;
  WITH expected AS (
    SELECT member_object_id FROM p3_canonical_family_membership WHERE family_revision_id=v_pred
    UNION SELECT member_object_id FROM p3_adjudication_member WHERE adjudication_id=p_adjudication AND member_disposition='ACCEPT')
  SELECT COUNT(*) INTO v_extra FROM (SELECT member_object_id FROM p3_canonical_family_membership WHERE family_revision_id=v_revision EXCEPT SELECT member_object_id FROM expected) q;
  IF v_missing<>0 OR v_extra<>0 THEN RAISE EXCEPTION 'canonical revision is not predecessor union disjoint accepts: missing %, extra %',v_missing,v_extra; END IF;
  SELECT COUNT(*) INTO v_bad FROM p3_adjudication_member a WHERE a.adjudication_id=p_adjudication AND a.member_disposition='ALREADY_CANONICAL' AND (v_pred IS NULL OR NOT EXISTS (SELECT 1 FROM p3_canonical_family_membership m WHERE m.family_revision_id=v_pred AND m.member_object_id=a.member_object_id));
  IF v_bad<>0 THEN RAISE EXCEPTION 'ALREADY_CANONICAL member absent from predecessor'; END IF;
  SELECT COUNT(*) INTO v_bad FROM p3_adjudication_member a WHERE a.adjudication_id=p_adjudication AND a.member_disposition='ACCEPT' AND v_pred IS NOT NULL AND EXISTS (SELECT 1 FROM p3_canonical_family_membership m WHERE m.family_revision_id=v_pred AND m.member_object_id=a.member_object_id);
  IF v_bad<>0 THEN RAISE EXCEPTION 'new ACCEPT overlaps predecessor membership'; END IF;
  IF v_status='ACCEPTED_WITH_VARIANTS' AND EXISTS (SELECT 1 FROM p3_canonical_family_membership m WHERE m.family_revision_id=v_revision AND m.variant_revision_id IS NULL) THEN RAISE EXCEPTION 'variant-bearing canonical revision has unassigned member'; END IF;
  IF v_status='ACCEPTED_CANONICAL' AND EXISTS (SELECT 1 FROM p3_canonical_family_membership m WHERE m.family_revision_id=v_revision AND m.variant_revision_id IS NOT NULL) THEN RAISE EXCEPTION 'canonical decision unexpectedly carries variants'; END IF;
  IF EXISTS (SELECT 1 FROM p3_adjudication_member a WHERE a.adjudication_id=p_adjudication AND a.member_disposition='EXCLUDE' AND NOT EXISTS (SELECT 1 FROM p3_family_exclusion e JOIN p3_excluded_object eo ON eo.exclusion_id=e.exclusion_id WHERE e.owner_object_id=v_family AND e.exclusion_type='NAMED_MEMBER' AND e.authority_release_id=(SELECT authority_release_id FROM p3_adjudication_decision WHERE adjudication_id=p_adjudication) AND eo.excluded_object_id=a.member_object_id)) THEN RAISE EXCEPTION 'excluded member lacks exact named exclusion'; END IF;
END $$;

CREATE OR REPLACE FUNCTION p3_guard_obligation_resolution() RETURNS trigger AS $$
BEGIN
  IF OLD.status<>'OPEN' THEN RAISE EXCEPTION 'resolved closure obligation is immutable'; END IF;
  IF NEW.status NOT IN ('RESOLVED_ACCEPT','RESOLVED_SPLIT','RESOLVED_EXCLUDE') OR NEW.resolution_adjudication_id IS NULL THEN RAISE EXCEPTION 'closure obligation may transition only OPEN -> exact resolved status'; END IF;
  IF NEW.closure_obligation_id<>OLD.closure_obligation_id OR NEW.candidate_revision_id<>OLD.candidate_revision_id OR NEW.left_object_id<>OLD.left_object_id OR NEW.right_object_id<>OLD.right_object_id OR NEW.obligation_type<>OLD.obligation_type OR NEW.authority_release_id<>OLD.authority_release_id THEN RAISE EXCEPTION 'closure obligation identity fields are immutable'; END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;
CREATE TRIGGER p3_closure_obligation_resolution_guard BEFORE UPDATE ON p3_closure_obligation FOR EACH ROW EXECUTE FUNCTION p3_guard_obligation_resolution();

CREATE OR REPLACE FUNCTION p3_assert_replay_evidence_closure(p_adjudication TEXT) RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE v_candidate TEXT; v_status TEXT; v_missing INTEGER;
BEGIN
  SELECT candidate_revision_id,decision_status INTO v_candidate,v_status FROM p3_adjudication_decision WHERE adjudication_id=p_adjudication;
  IF NOT FOUND THEN RAISE EXCEPTION 'unknown adjudication %',p_adjudication; END IF;
  SELECT COUNT(*) INTO v_missing FROM p3_replay_obligation_baseline b WHERE b.candidate_revision_id=v_candidate AND NOT EXISTS (SELECT 1 FROM p3_adjudication_pair_resolution r JOIN p3_closure_obligation o USING(closure_obligation_id) WHERE r.adjudication_id=p_adjudication AND r.closure_obligation_id=b.closure_obligation_id AND o.status=r.resolution_status AND o.resolution_adjudication_id=p_adjudication);
  IF v_missing<>0 THEN RAISE EXCEPTION 'adjudication % leaves % baseline pair obligations unresolved',p_adjudication,v_missing; END IF;
  IF v_status IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') THEN
    SELECT COUNT(*) INTO v_missing FROM p3_internal_pair_collision c WHERE c.candidate_revision_id=v_candidate AND NOT EXISTS (SELECT 1 FROM p3_adjudication_collision_disposition d WHERE d.adjudication_id=p_adjudication AND d.collision_id=c.collision_id);
    IF v_missing<>0 THEN RAISE EXCEPTION 'accepted collision-bearing candidate lacks % collision dispositions',v_missing; END IF;
    WITH required(kind,bkey,l,r) AS (
      SELECT 'HIERARCHICAL_ONLY',coalesce(direct_pair_projection_id,left_object_id||':'||right_object_id),left_object_id,right_object_id FROM p3_internal_pair_matrix WHERE candidate_revision_id=v_candidate AND pair_state='HIERARCHICAL_ONLY'
      UNION ALL SELECT 'UNRESOLVED_BOUNDARY',projection_id,left_object_id,right_object_id FROM p3_internal_pair_unresolved_boundary WHERE candidate_revision_id=v_candidate
      UNION ALL SELECT 'REDIRECT_BOUNDARY',projection_id,left_object_id,right_object_id FROM p3_internal_pair_redirect_boundary WHERE candidate_revision_id=v_candidate
      UNION ALL SELECT 'COORDINATE_CONSTRAINT',projection_id,left_object_id,right_object_id FROM p3_internal_pair_coordinate_constraint WHERE candidate_revision_id=v_candidate)
    SELECT COUNT(*) INTO v_missing FROM required q WHERE NOT EXISTS (SELECT 1 FROM p3_adjudication_stronger_boundary_resolution r WHERE r.adjudication_id=p_adjudication AND r.boundary_kind=q.kind AND r.boundary_key=q.bkey AND r.left_object_id=q.l AND r.right_object_id=q.r);
    IF v_missing<>0 THEN RAISE EXCEPTION 'accepted candidate lacks % stronger-boundary resolutions',v_missing; END IF;
  END IF;
END $$;

CREATE OR REPLACE FUNCTION p3_validate_replay_evidence_deferred() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE aid TEXT;
BEGIN
  IF TG_TABLE_NAME='p3_closure_obligation' THEN aid:=COALESCE(NEW.resolution_adjudication_id,OLD.resolution_adjudication_id);
  ELSE aid:=COALESCE(NEW.adjudication_id,OLD.adjudication_id); END IF;
  IF aid IS NOT NULL AND EXISTS(SELECT 1 FROM p3_adjudication_decision WHERE adjudication_id=aid) THEN PERFORM p3_assert_replay_evidence_closure(aid); END IF;
  RETURN COALESCE(NEW,OLD);
END $$;
CREATE CONSTRAINT TRIGGER p3_replay_decision_evidence_closure AFTER INSERT ON p3_adjudication_decision DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_replay_evidence_deferred();
CREATE CONSTRAINT TRIGGER p3_replay_pair_resolution_closure AFTER INSERT OR UPDATE OR DELETE ON p3_adjudication_pair_resolution DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_replay_evidence_deferred();
CREATE CONSTRAINT TRIGGER p3_replay_collision_resolution_closure AFTER INSERT OR UPDATE OR DELETE ON p3_adjudication_collision_disposition DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_replay_evidence_deferred();
CREATE CONSTRAINT TRIGGER p3_replay_boundary_resolution_closure AFTER INSERT OR UPDATE OR DELETE ON p3_adjudication_stronger_boundary_resolution DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_replay_evidence_deferred();
CREATE CONSTRAINT TRIGGER p3_replay_obligation_update_closure AFTER UPDATE ON p3_closure_obligation DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_replay_evidence_deferred();

CREATE TRIGGER p3_singleton_split_authority_immutable BEFORE UPDATE OR DELETE ON p3_singleton_split_authority FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_family_revision_predecessor_immutable BEFORE UPDATE OR DELETE ON p3_family_revision_predecessor FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_pair_resolution_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_pair_resolution FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_stronger_boundary_resolution_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_stronger_boundary_resolution FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();

COMMIT;
