-- Rawlsing P3 PostgreSQL-Compatible Logical DDL v1
-- This file defines the target relational contract. It is NOT an installation script.
-- No live database write is authorized by this plan. Installation requires P3 closure,
-- a user-designated repository/database, shadow mode, comparison, promotion, and rollback.

BEGIN;

CREATE TABLE p3_authority_release (
    release_id TEXT PRIMARY KEY,
    parent_release_id TEXT REFERENCES p3_authority_release(release_id),
    schema_version TEXT NOT NULL,
    builder_version TEXT NOT NULL,
    input_manifest_hash CHAR(64) NOT NULL CHECK (input_manifest_hash ~ '^[0-9a-f]{64}$'),
    status TEXT NOT NULL CHECK (status IN ('DRAFT','VALIDATED','SHADOW','PROMOTED','ROLLED_BACK','SUPERSEDED')),
    created_at TIMESTAMPTZ NOT NULL,
    migration_artifact TEXT,
    rollback_artifact TEXT,
    validation_return_hash CHAR(64) NOT NULL CHECK (validation_return_hash ~ '^[0-9a-f]{64}$')
);

CREATE TABLE p3_vocabulary (
    vocabulary_domain TEXT NOT NULL,
    code TEXT NOT NULL,
    label TEXT NOT NULL,
    definition TEXT NOT NULL,
    authority_effect TEXT,
    valid_from_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    valid_to_release_id TEXT REFERENCES p3_authority_release(release_id),
    deprecated BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (vocabulary_domain, code, valid_from_release_id)
);

CREATE TABLE p3_object_id_registry (
    object_id TEXT PRIMARY KEY,
    object_type TEXT NOT NULL,
    allocation_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    stable_identity_note TEXT NOT NULL,
    retired_release_id TEXT REFERENCES p3_authority_release(release_id),
    content_hash CHAR(64),
    CHECK (content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$')
);

CREATE TABLE p3_lineage_segment (
    segment_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    parent_lineage_id TEXT NOT NULL,
    segment_reason TEXT NOT NULL,
    first_wave TEXT,
    last_wave TEXT,
    p2_lineage_unchanged BOOLEAN NOT NULL CHECK (p2_lineage_unchanged),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);

CREATE TABLE p3_lineage_segment_member (
    segment_id TEXT NOT NULL REFERENCES p3_lineage_segment(segment_id),
    implementation_id TEXT NOT NULL,
    ordinal_position INTEGER NOT NULL CHECK (ordinal_position >= 0),
    PRIMARY KEY (segment_id, implementation_id),
    UNIQUE (segment_id, ordinal_position)
);

CREATE TABLE p3_proposition_signature (
    signature_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    subject_type TEXT NOT NULL CHECK (subject_type IN ('SOURCE_LOCAL_LINEAGE','P3_LINEAGE_SEGMENT')),
    subject_id TEXT NOT NULL,
    signature_status TEXT NOT NULL CHECK (signature_status IN ('COMPLETE','PARTIAL_FAIL_CLOSED','HETEROGENEOUS','CONFLICTING')),
    content_hash CHAR(64) NOT NULL CHECK (content_hash ~ '^[0-9a-f]{64}$'),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    UNIQUE (subject_type, subject_id, authority_release_id)
);

CREATE TABLE p3_signature_field (
    signature_id TEXT NOT NULL REFERENCES p3_proposition_signature(signature_id),
    field_name TEXT NOT NULL,
    field_value TEXT,
    evidence_state TEXT NOT NULL CHECK (evidence_state IN (
        'KNOWN','EXPLICITLY_UNSPECIFIED','NOT_APPLICABLE','UNRECOVERED',
        'HETEROGENEOUS','CONFLICTING','DIAGNOSTIC_ONLY'
    )),
    confidence TEXT NOT NULL CHECK (confidence IN ('HIGH','MEDIUM','LOW','NOT_APPLICABLE')),
    PRIMARY KEY (signature_id, field_name),
    CHECK (
        evidence_state <> 'KNOWN'
        OR field_value IS NOT NULL
    )
);

CREATE TABLE p3_signature_field_evidence (
    signature_id TEXT NOT NULL,
    field_name TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    evidence_id TEXT NOT NULL,
    evidence_role TEXT NOT NULL,
    PRIMARY KEY (signature_id, field_name, evidence_type, evidence_id),
    FOREIGN KEY (signature_id, field_name)
        REFERENCES p3_signature_field(signature_id, field_name)
);

CREATE TABLE p3_pair_fact_bundle (
    pair_fact_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    left_object_id TEXT NOT NULL,
    right_object_id TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    target_relation TEXT,
    operator_relation TEXT,
    timeframe_relation TEXT,
    response_relation TEXT,
    portability_ceiling TEXT NOT NULL,
    connectivity_allowed BOOLEAN NOT NULL,
    creates_endpoint_authority BOOLEAN NOT NULL DEFAULT FALSE CHECK (NOT creates_endpoint_authority),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    CHECK (left_object_id < right_object_id),
    CHECK (
        connectivity_allowed = FALSE
        OR relation_type IN ('PROPOSITION_RESPONSE_IDENTITY','PROPOSITION_IDENTITY_ONLY')
    )
);

CREATE TABLE p3_pair_fact_p2_ruling (
    pair_fact_id TEXT NOT NULL REFERENCES p3_pair_fact_bundle(pair_fact_id),
    p2_ruling_id TEXT NOT NULL,
    PRIMARY KEY (pair_fact_id, p2_ruling_id)
);

CREATE TABLE p3_pair_fact_evidence (
    pair_fact_id TEXT NOT NULL REFERENCES p3_pair_fact_bundle(pair_fact_id),
    side TEXT NOT NULL CHECK (side IN ('LEFT','RIGHT','RELATION')),
    evidence_id TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    PRIMARY KEY (pair_fact_id, side, evidence_id)
);

CREATE TABLE p3_collision_scope_registry (
    collision_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    collision_type TEXT NOT NULL,
    scope_type TEXT NOT NULL,
    left_object_id TEXT NOT NULL,
    right_object_id TEXT NOT NULL,
    hard_blocker BOOLEAN NOT NULL,
    source_scope TEXT,
    valid_from TEXT,
    valid_to TEXT,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    CHECK (left_object_id < right_object_id)
);

CREATE TABLE p3_collision_authority_source (
    collision_id TEXT NOT NULL REFERENCES p3_collision_scope_registry(collision_id),
    source_authority_id TEXT NOT NULL,
    PRIMARY KEY (collision_id, source_authority_id)
);

CREATE TABLE p3_candidate_component (
    component_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    build_rule_version TEXT NOT NULL,
    connectivity_edge_count INTEGER NOT NULL CHECK (connectivity_edge_count >= 0),
    member_count INTEGER NOT NULL CHECK (member_count >= 2),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);

CREATE TABLE p3_component_membership (
    component_id TEXT NOT NULL REFERENCES p3_candidate_component(component_id),
    member_object_id TEXT NOT NULL,
    PRIMARY KEY (component_id, member_object_id)
);

CREATE TABLE p3_candidate_family (
    candidate_family_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    candidate_status TEXT NOT NULL,
    canonical_signature_id TEXT REFERENCES p3_proposition_signature(signature_id),
    evidence_bundle_hash CHAR(64) NOT NULL CHECK (evidence_bundle_hash ~ '^[0-9a-f]{64}$'),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);

CREATE TABLE p3_candidate_component_link (
    candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id),
    component_id TEXT NOT NULL REFERENCES p3_candidate_component(component_id),
    PRIMARY KEY (candidate_family_id, component_id)
);

CREATE TABLE p3_candidate_membership (
    candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id),
    member_object_id TEXT NOT NULL,
    membership_role TEXT NOT NULL CHECK (membership_role IN ('PROPOSED_MEMBER','ACCEPTED_MEMBER','EXCLUDED_MEMBER','HIERARCHICAL_RELATIVE')),
    PRIMARY KEY (candidate_family_id, member_object_id, membership_role)
);

CREATE TABLE p3_internal_pair_matrix (
    candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id),
    left_object_id TEXT NOT NULL,
    right_object_id TEXT NOT NULL,
    pair_state TEXT NOT NULL CHECK (pair_state IN (
        'DIRECT_POSITIVE','DIRECT_COLLISION','HIERARCHICAL_ONLY','UNRULED',
        'SIGNATURE_CONFLICT','SIGNATURE_COMPATIBLE'
    )),
    direct_pair_fact_id TEXT REFERENCES p3_pair_fact_bundle(pair_fact_id),
    collision_id TEXT REFERENCES p3_collision_scope_registry(collision_id),
    PRIMARY KEY (candidate_family_id, left_object_id, right_object_id),
    CHECK (left_object_id < right_object_id)
);

CREATE TABLE p3_closure_obligation (
    closure_obligation_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id),
    left_object_id TEXT NOT NULL,
    right_object_id TEXT NOT NULL,
    obligation_type TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('OPEN','RESOLVED_ACCEPT','RESOLVED_SPLIT','RESOLVED_EXCLUDE','FAIL_CLOSED')),
    resolution_adjudication_id TEXT,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    CHECK (left_object_id < right_object_id)
);

CREATE TABLE p3_family_variant (
    variant_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    candidate_or_family_id TEXT NOT NULL,
    variant_dimension TEXT NOT NULL,
    variant_value TEXT NOT NULL,
    value_portability_status TEXT NOT NULL DEFAULT 'NOT_AUTHORIZED_BY_P3'
        CHECK (value_portability_status = 'NOT_AUTHORIZED_BY_P3'),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);

CREATE TABLE p3_variant_membership (
    variant_id TEXT NOT NULL REFERENCES p3_family_variant(variant_id),
    member_object_id TEXT NOT NULL,
    PRIMARY KEY (variant_id, member_object_id)
);

CREATE TABLE p3_family_exclusion (
    exclusion_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    candidate_or_family_id TEXT NOT NULL,
    exclusion_type TEXT NOT NULL CHECK (exclusion_type IN ('NAMED_MEMBER','RULE_BASED')),
    prohibited_operation TEXT NOT NULL,
    evidence_or_rule TEXT NOT NULL,
    scope TEXT NOT NULL,
    tested_surface_complete BOOLEAN NOT NULL DEFAULT FALSE,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);

CREATE TABLE p3_excluded_object (
    exclusion_id TEXT NOT NULL REFERENCES p3_family_exclusion(exclusion_id),
    excluded_object_id TEXT NOT NULL,
    PRIMARY KEY (exclusion_id, excluded_object_id)
);

CREATE TABLE p3_hyperedge (
    hyperedge_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    hyperedge_type TEXT NOT NULL,
    authority_effect TEXT NOT NULL,
    causal_authority BOOLEAN NOT NULL DEFAULT FALSE CHECK (NOT causal_authority),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);

CREATE TABLE p3_hyperedge_membership (
    hyperedge_id TEXT NOT NULL REFERENCES p3_hyperedge(hyperedge_id),
    object_id TEXT NOT NULL,
    participant_role TEXT NOT NULL,
    PRIMARY KEY (hyperedge_id, object_id, participant_role)
);

CREATE TABLE p3_adjudication_decision (
    adjudication_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id),
    decision_status TEXT NOT NULL,
    canonical_family_id TEXT,
    canonical_proposition JSONB,
    response_portability_status TEXT NOT NULL DEFAULT 'NOT_AUTHORIZED_BY_P3'
        CHECK (response_portability_status = 'NOT_AUTHORIZED_BY_P3'),
    unresolved_boundaries JSONB NOT NULL DEFAULT '[]'::jsonb,
    rationale TEXT NOT NULL,
    evidence_bundle_hash CHAR(64) NOT NULL CHECK (evidence_bundle_hash ~ '^[0-9a-f]{64}$'),
    supersedes_adjudication_id TEXT REFERENCES p3_adjudication_decision(adjudication_id),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE p3_adjudication_member (
    adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id),
    member_object_id TEXT NOT NULL,
    member_disposition TEXT NOT NULL CHECK (member_disposition IN ('ACCEPT','EXCLUDE','HIERARCHICAL','UNRESOLVED')),
    variant_id TEXT REFERENCES p3_family_variant(variant_id),
    PRIMARY KEY (adjudication_id, member_object_id)
);

CREATE TABLE p3_doctrine_delta (
    doctrine_delta_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    trigger_candidate_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id),
    old_rule TEXT,
    new_rule TEXT NOT NULL,
    required_rebuild_scope TEXT NOT NULL,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);

CREATE TABLE p3_doctrine_delta_affected_object (
    doctrine_delta_id TEXT NOT NULL REFERENCES p3_doctrine_delta(doctrine_delta_id),
    affected_object_id TEXT NOT NULL,
    PRIMARY KEY (doctrine_delta_id, affected_object_id)
);

CREATE TABLE p3_family_genealogy (
    genealogy_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    relation_type TEXT NOT NULL CHECK (relation_type IN ('SPLIT','MERGE','SUPERSEDE','DEPRECATE')),
    adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);

CREATE TABLE p3_family_genealogy_member (
    genealogy_id TEXT NOT NULL REFERENCES p3_family_genealogy(genealogy_id),
    family_id TEXT NOT NULL,
    genealogy_role TEXT NOT NULL CHECK (genealogy_role IN ('PREDECESSOR','SUCCESSOR')),
    PRIMARY KEY (genealogy_id, family_id, genealogy_role)
);

CREATE TABLE p3_artifact_dependency (
    dependency_id TEXT PRIMARY KEY REFERENCES p3_object_id_registry(object_id),
    dependent_artifact_id TEXT NOT NULL,
    authority_input_id TEXT NOT NULL,
    dependency_role TEXT NOT NULL,
    dirty_if_changed BOOLEAN NOT NULL,
    impact_priority TEXT NOT NULL CHECK (impact_priority IN ('FATAL','HIGH','MEDIUM','LOW')),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);

CREATE TABLE p3_doctrine_test (
    test_id TEXT PRIMARY KEY,
    test_class TEXT NOT NULL,
    test_definition TEXT NOT NULL,
    required BOOLEAN NOT NULL,
    introduced_by_doctrine_delta_id TEXT REFERENCES p3_doctrine_delta(doctrine_delta_id)
);

CREATE TABLE p3_failure_ledger (
    failure_id TEXT PRIMARY KEY,
    build_run_id TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('FATAL','ERROR','WARNING','INFO')),
    object_id TEXT,
    failure_code TEXT NOT NULL,
    message TEXT NOT NULL,
    source_artifact TEXT,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE UNIQUE INDEX p3_one_promoted_release
    ON p3_authority_release ((status))
    WHERE status = 'PROMOTED';

CREATE VIEW p3_current_promoted_release AS
SELECT *
FROM p3_authority_release
WHERE status = 'PROMOTED';

-- This DDL intentionally excludes response transformation authority,
-- causal direction, strata assignment authority, respondent joins, and simulation state.

ROLLBACK;
