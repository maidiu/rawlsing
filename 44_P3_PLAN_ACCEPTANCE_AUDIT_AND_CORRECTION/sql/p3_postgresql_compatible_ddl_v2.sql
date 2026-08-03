-- Rawlsing P3 PostgreSQL-Compatible Logical DDL v2
-- Target contract only. No live write is authorized.
BEGIN;

CREATE TABLE p3_authority_release (
    release_id TEXT PRIMARY KEY,
    parent_release_id TEXT REFERENCES p3_authority_release(release_id),
    schema_version TEXT NOT NULL, builder_version TEXT NOT NULL,
    input_manifest_hash CHAR(64) NOT NULL CHECK (input_manifest_hash ~ '^[0-9a-f]{64}$'),
    created_at TIMESTAMPTZ NOT NULL, object_counts JSONB NOT NULL DEFAULT '{}'::jsonb,
    validation_return_hash CHAR(64) NOT NULL CHECK (validation_return_hash ~ '^[0-9a-f]{64}$'),
    migration_artifact TEXT, rollback_artifact TEXT, CHECK (parent_release_id IS NULL OR parent_release_id <> release_id)
);
CREATE TABLE p3_release_status_event (
    release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), event_ordinal INTEGER NOT NULL CHECK (event_ordinal >= 1),
    status TEXT NOT NULL CHECK (status IN ('DRAFT','VALIDATED','SHADOW','PROMOTED','ROLLED_BACK','SUPERSEDED')),
    occurred_at TIMESTAMPTZ NOT NULL, evidence_hash CHAR(64) NOT NULL CHECK (evidence_hash ~ '^[0-9a-f]{64}$'),
    PRIMARY KEY (release_id,event_ordinal)
);


CREATE TABLE p3_runtime_promotion_pointer (
    singleton_key BOOLEAN PRIMARY KEY DEFAULT TRUE CHECK (singleton_key),
    promoted_release_id TEXT NOT NULL UNIQUE REFERENCES p3_authority_release(release_id),
    promoted_at TIMESTAMPTZ NOT NULL,
    promotion_evidence_hash CHAR(64) NOT NULL CHECK (promotion_evidence_hash ~ '^[0-9a-f]{64}$')
);
-- Promotion updates this singleton transactionally after a PROMOTED event is appended;
-- historical releases may retain PROMOTED events without violating later promotions.

CREATE TABLE p3_vocabulary_code (
    vocabulary_domain TEXT NOT NULL, code TEXT NOT NULL, introduced_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    retired_release_id TEXT REFERENCES p3_authority_release(release_id), PRIMARY KEY(vocabulary_domain,code)
);
CREATE TABLE p3_vocabulary_revision (
    vocabulary_domain TEXT NOT NULL, code TEXT NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    label TEXT NOT NULL, definition TEXT NOT NULL, authority_effect TEXT, deprecated BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY(vocabulary_domain,code,authority_release_id), FOREIGN KEY(vocabulary_domain,code) REFERENCES p3_vocabulary_code(vocabulary_domain,code)
);

CREATE TABLE p3_object_registry (
    object_id TEXT PRIMARY KEY, object_type TEXT NOT NULL, identity_strategy TEXT NOT NULL, idempotency_key TEXT NOT NULL UNIQUE,
    origin_phase TEXT NOT NULL, origin_authority_id TEXT, allocation_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    retired_release_id TEXT REFERENCES p3_authority_release(release_id), content_hash CHAR(64), stable_identity_note TEXT NOT NULL,
    CHECK (content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$'),
    CHECK (identity_strategy IN ('INHERITED_UPSTREAM_ID','CONTENT_ADDRESSED_DERIVED_ID','REGISTRY_ALLOCATED_DURABLE_ID'))
);
CREATE TABLE p3_upstream_object_reference (
    object_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), upstream_phase TEXT NOT NULL, source_family TEXT,
    upstream_object_type TEXT NOT NULL, upstream_object_id TEXT NOT NULL, authority_artifact TEXT NOT NULL,
    authority_hash CHAR(64) NOT NULL CHECK (authority_hash ~ '^[0-9a-f]{64}$'), license_provenance_ref TEXT,
    read_only BOOLEAN NOT NULL DEFAULT TRUE CHECK (read_only), UNIQUE(upstream_phase,upstream_object_type,upstream_object_id)
);

CREATE TABLE p3_lineage_segment (
    segment_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), parent_lineage_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    segment_reason TEXT NOT NULL, first_wave TEXT, last_wave TEXT, p2_lineage_unchanged BOOLEAN NOT NULL CHECK (p2_lineage_unchanged),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);
CREATE TABLE p3_lineage_segment_member (
    segment_id TEXT NOT NULL REFERENCES p3_lineage_segment(segment_id), implementation_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    ordinal_position INTEGER NOT NULL CHECK (ordinal_position>=0), PRIMARY KEY(segment_id,implementation_id), UNIQUE(segment_id,ordinal_position)
);

CREATE TABLE p3_proposition_signature (
    signature_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), subject_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    signature_status TEXT NOT NULL CHECK(signature_status IN ('COMPLETE','PARTIAL_FAIL_CLOSED','HETEROGENEOUS','CONFLICTING')),
    content_hash CHAR(64) NOT NULL CHECK(content_hash ~ '^[0-9a-f]{64}$'), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    UNIQUE(subject_id,authority_release_id)
);
CREATE TABLE p3_signature_field (
    signature_id TEXT NOT NULL REFERENCES p3_proposition_signature(signature_id), field_name TEXT NOT NULL, field_value TEXT, normalized_value_code TEXT,
    evidence_state TEXT NOT NULL CHECK(evidence_state IN ('KNOWN','EXPLICITLY_UNSPECIFIED','NOT_APPLICABLE','UNRECOVERED','HETEROGENEOUS','CONFLICTING','DIAGNOSTIC_ONLY')),
    confidence TEXT NOT NULL CHECK(confidence IN ('HIGH','MEDIUM','LOW','NOT_APPLICABLE')), PRIMARY KEY(signature_id,field_name),
    CHECK(evidence_state <> 'KNOWN' OR field_value IS NOT NULL)
);
CREATE TABLE p3_signature_field_evidence (
    signature_id TEXT NOT NULL, field_name TEXT NOT NULL, evidence_type TEXT NOT NULL, evidence_id TEXT NOT NULL, evidence_role TEXT NOT NULL,
    PRIMARY KEY(signature_id,field_name,evidence_type,evidence_id), FOREIGN KEY(signature_id,field_name) REFERENCES p3_signature_field(signature_id,field_name)
);
CREATE TABLE p3_response_contract_reference (
    reference_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), subject_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    upstream_response_contract_id TEXT, response_topology TEXT NOT NULL, response_contract_hash CHAR(64), authority_artifact TEXT NOT NULL,
    p4_authority BOOLEAN NOT NULL DEFAULT FALSE CHECK(NOT p4_authority), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    CHECK(response_contract_hash IS NULL OR response_contract_hash ~ '^[0-9a-f]{64}$')
);
CREATE TABLE p3_structural_context_reference (
    reference_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), subject_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    source_field TEXT NOT NULL, source_value JSONB, authority_artifact TEXT NOT NULL, p5_authority BOOLEAN NOT NULL DEFAULT FALSE CHECK(NOT p5_authority),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);

CREATE TABLE p3_pair_fact_bundle (
    pair_fact_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), orientation TEXT NOT NULL CHECK(orientation IN ('SYMMETRIC','DIRECTIONAL')),
    relation_type TEXT NOT NULL CHECK(relation_type IN ('PROPOSITION_RESPONSE_IDENTITY','PROPOSITION_IDENTITY_ONLY','NESTED_TARGET_RELATION','CONSTRUCT_COORDINATE','STRUCTURE_MEMBER_ANALOGY','EXPLICIT_NEGATIVE','REDIRECT_OTHER_DOMAIN','UNRESOLVED')),
    target_relation TEXT, operator_relation TEXT, timeframe_relation TEXT, response_relation TEXT, source_portability_ceiling TEXT NOT NULL,
    p3_portability_ceiling TEXT NOT NULL CHECK(p3_portability_ceiling IN ('QUESTION_PROPOSITION_AND_RESPONSE_CONTRACT','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','QUESTION_PROPOSITION_ONLY','DOMAIN_COORDINATE_ONLY','CONSTRUCT_TARGET_COORDINATE_ONLY','HIERARCHICAL_ONLY','NO_POSITIVE_AUTHORITY')),
    connectivity_allowed BOOLEAN NOT NULL, creates_endpoint_authority BOOLEAN NOT NULL DEFAULT FALSE CHECK(NOT creates_endpoint_authority),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id <> right_object_id),
    CHECK(connectivity_allowed=FALSE OR relation_type IN ('PROPOSITION_RESPONSE_IDENTITY','PROPOSITION_IDENTITY_ONLY'))
);
CREATE TABLE p3_pair_fact_source_authority (
    pair_fact_id TEXT NOT NULL REFERENCES p3_pair_fact_bundle(pair_fact_id), registry_code TEXT NOT NULL, authority_id TEXT NOT NULL,
    governing BOOLEAN NOT NULL, superseded_by_authority_id TEXT, PRIMARY KEY(pair_fact_id,registry_code,authority_id)
);
CREATE UNIQUE INDEX p3_pair_fact_one_governing_source ON p3_pair_fact_source_authority(pair_fact_id) WHERE governing;
CREATE TABLE p3_pair_fact_evidence (
    pair_fact_id TEXT NOT NULL REFERENCES p3_pair_fact_bundle(pair_fact_id), side TEXT NOT NULL CHECK(side IN ('LEFT','RIGHT','RELATION')),
    evidence_id TEXT NOT NULL, evidence_type TEXT NOT NULL, PRIMARY KEY(pair_fact_id,side,evidence_id)
);

CREATE TABLE p3_collision_scope_registry (
    collision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), collision_type TEXT NOT NULL, scope_type TEXT NOT NULL,
    left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    hard_blocker BOOLEAN NOT NULL, source_scope TEXT, historical_scope JSONB, downstream_effects JSONB NOT NULL DEFAULT '[]'::jsonb,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id <> right_object_id)
);
CREATE TABLE p3_collision_authority_source (
    collision_id TEXT NOT NULL REFERENCES p3_collision_scope_registry(collision_id), source_authority_id TEXT NOT NULL, PRIMARY KEY(collision_id,source_authority_id)
);

CREATE TABLE p3_candidate_component (
    component_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), build_rule_version TEXT NOT NULL, content_hash CHAR(64) NOT NULL CHECK(content_hash ~ '^[0-9a-f]{64}$'),
    connectivity_edge_count INTEGER NOT NULL CHECK(connectivity_edge_count>=1), member_count INTEGER NOT NULL CHECK(member_count>=2),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);
CREATE TABLE p3_component_membership (component_id TEXT NOT NULL REFERENCES p3_candidate_component(component_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), PRIMARY KEY(component_id,member_object_id));

CREATE TABLE p3_candidate_family (
    candidate_family_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), created_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);
CREATE TABLE p3_candidate_revision (
    candidate_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id),
    lifecycle_stage TEXT NOT NULL CHECK(lifecycle_stage IN ('DISCOVERED','GENERATED_CANDIDATE','EVIDENCE_COMPLETE','ADJUDICATION_REQUIRED','DECIDED','SUPERSEDED','DEPRECATED')),
    candidate_classification TEXT NOT NULL CHECK(candidate_classification IN ('CLEAN_FAMILY_CANDIDATE','RESPONSE_VARIANT_CANDIDATE','SPLIT_REQUIRED','HIERARCHICAL_RELATION_ONLY','COLLISION_BEARING','STRUCTURAL_ANALOGY_ONLY','INSUFFICIENT_AUTHORITY','REJECTED_SEMANTIC_ARTIFACT')),
    canonical_signature_id TEXT REFERENCES p3_proposition_signature(signature_id), evidence_bundle_hash CHAR(64) NOT NULL CHECK(evidence_bundle_hash ~ '^[0-9a-f]{64}$'),
    rank_tuple JSONB NOT NULL DEFAULT '[]'::jsonb, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(candidate_family_id,authority_release_id)
);
CREATE TABLE p3_candidate_status_event (
    candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id), event_ordinal INTEGER NOT NULL CHECK(event_ordinal>=1),
    from_stage TEXT, to_stage TEXT NOT NULL, guard_evidence_id TEXT NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(candidate_family_id,event_ordinal)
);
CREATE TABLE p3_candidate_component_link (candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), component_id TEXT NOT NULL REFERENCES p3_candidate_component(component_id), PRIMARY KEY(candidate_revision_id,component_id));
CREATE TABLE p3_candidate_membership (candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), membership_role TEXT NOT NULL CHECK(membership_role IN ('PROPOSED_MEMBER','ACCEPTED_MEMBER','EXCLUDED_MEMBER','HIERARCHICAL_RELATIVE')), PRIMARY KEY(candidate_revision_id,member_object_id,membership_role));
CREATE TABLE p3_internal_pair_matrix (
    candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), pair_state TEXT NOT NULL CHECK(pair_state IN ('DIRECT_POSITIVE','DIRECT_COLLISION','HIERARCHICAL_ONLY','UNRULED','SIGNATURE_CONFLICT','SIGNATURE_COMPATIBLE')),
    direct_pair_fact_id TEXT REFERENCES p3_pair_fact_bundle(pair_fact_id), collision_id TEXT REFERENCES p3_collision_scope_registry(collision_id),
    PRIMARY KEY(candidate_revision_id,left_object_id,right_object_id), CHECK(left_object_id <> right_object_id)
);
CREATE TABLE p3_closure_obligation (
    closure_obligation_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id),
    left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), obligation_type TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('OPEN','RESOLVED_ACCEPT','RESOLVED_SPLIT','RESOLVED_EXCLUDE','FAIL_CLOSED')), resolution_adjudication_id TEXT,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id <> right_object_id)
);

CREATE TABLE p3_family_variant (variant_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), owner_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), created_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id));
CREATE TABLE p3_family_variant_revision (
    variant_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), variant_id TEXT NOT NULL REFERENCES p3_family_variant(variant_id),
    variant_dimension TEXT NOT NULL CHECK(variant_dimension IN ('RESPONSE_TOPOLOGY','WORDING_TRANSLATION','SOURCE_RESPONSE_FORM','HISTORICAL_INTERVAL','OTHER_EXPLICITLY_GOVERNED')),
    variant_value TEXT NOT NULL, value_portability_status TEXT NOT NULL DEFAULT 'NOT_AUTHORIZED_BY_P3' CHECK(value_portability_status='NOT_AUTHORIZED_BY_P3'),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(variant_id,authority_release_id)
);
CREATE TABLE p3_variant_membership (variant_revision_id TEXT NOT NULL REFERENCES p3_family_variant_revision(variant_revision_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), PRIMARY KEY(variant_revision_id,member_object_id));
CREATE TABLE p3_family_exclusion (
    exclusion_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), owner_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    exclusion_type TEXT NOT NULL CHECK(exclusion_type IN ('NAMED_MEMBER','RULE_BASED')), prohibited_operation TEXT NOT NULL, evidence_or_rule TEXT NOT NULL,
    scope TEXT NOT NULL, tested_surface_complete BOOLEAN NOT NULL DEFAULT FALSE, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);
CREATE TABLE p3_excluded_object (exclusion_id TEXT NOT NULL REFERENCES p3_family_exclusion(exclusion_id), excluded_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), PRIMARY KEY(exclusion_id,excluded_object_id));
CREATE TABLE p3_hyperedge (
    hyperedge_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), hyperedge_type TEXT NOT NULL, authority_effect TEXT NOT NULL,
    causal_authority BOOLEAN NOT NULL DEFAULT FALSE CHECK(NOT causal_authority), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);
CREATE TABLE p3_hyperedge_membership (hyperedge_id TEXT NOT NULL REFERENCES p3_hyperedge(hyperedge_id), object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), participant_role TEXT NOT NULL, PRIMARY KEY(hyperedge_id,object_id,participant_role));

CREATE TABLE p3_adjudication_decision (
    adjudication_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id),
    decision_status TEXT NOT NULL CHECK(decision_status IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS','SPLIT_REQUIRED','HIERARCHICAL_RELATION_ONLY','BLOCKED_UNRESOLVED','INSUFFICIENT_AUTHORITY','REJECTED_SEMANTIC_ARTIFACT','REJECTED')),
    canonical_family_id TEXT REFERENCES p3_object_registry(object_id), canonical_proposition JSONB, response_portability_status TEXT NOT NULL DEFAULT 'NOT_AUTHORIZED_BY_P3' CHECK(response_portability_status='NOT_AUTHORIZED_BY_P3'),
    unresolved_boundaries JSONB NOT NULL DEFAULT '[]'::jsonb, rationale TEXT NOT NULL, evidence_bundle_hash CHAR(64) NOT NULL CHECK(evidence_bundle_hash ~ '^[0-9a-f]{64}$'),
    supersedes_adjudication_id TEXT REFERENCES p3_adjudication_decision(adjudication_id), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), created_at TIMESTAMPTZ NOT NULL
);
CREATE TABLE p3_adjudication_member (adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), member_disposition TEXT NOT NULL CHECK(member_disposition IN ('ACCEPT','EXCLUDE','HIERARCHICAL','UNRESOLVED')), variant_revision_id TEXT REFERENCES p3_family_variant_revision(variant_revision_id), PRIMARY KEY(adjudication_id,member_object_id));
CREATE TABLE p3_adjudication_collision_disposition (adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), collision_id TEXT NOT NULL REFERENCES p3_collision_scope_registry(collision_id), disposition TEXT NOT NULL, rationale TEXT NOT NULL, PRIMARY KEY(adjudication_id,collision_id));
CREATE TABLE p3_adjudication_hierarchy_relation (adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), broader_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), narrower_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), relation_role TEXT NOT NULL, PRIMARY KEY(adjudication_id,broader_object_id,narrower_object_id));

CREATE TABLE p3_canonical_family (canonical_family_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), created_by_adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), created_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), retired_release_id TEXT REFERENCES p3_authority_release(release_id));
CREATE TABLE p3_canonical_family_revision (
    family_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), canonical_family_id TEXT NOT NULL REFERENCES p3_canonical_family(canonical_family_id), revision_number INTEGER NOT NULL CHECK(revision_number>=1),
    canonical_signature_id TEXT NOT NULL REFERENCES p3_proposition_signature(signature_id), canonical_proposition JSONB NOT NULL, evidence_bundle_hash CHAR(64) NOT NULL CHECK(evidence_bundle_hash ~ '^[0-9a-f]{64}$'),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(canonical_family_id,revision_number), UNIQUE(canonical_family_id,authority_release_id)
);
CREATE TABLE p3_canonical_family_membership (family_revision_id TEXT NOT NULL REFERENCES p3_canonical_family_revision(family_revision_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), variant_revision_id TEXT REFERENCES p3_family_variant_revision(variant_revision_id), PRIMARY KEY(family_revision_id,member_object_id));

CREATE TABLE p3_doctrine_delta (doctrine_delta_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), trigger_candidate_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id), old_rule TEXT, new_rule TEXT NOT NULL, required_rebuild_scope TEXT NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id));
CREATE TABLE p3_doctrine_delta_affected_object (doctrine_delta_id TEXT NOT NULL REFERENCES p3_doctrine_delta(doctrine_delta_id), affected_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), PRIMARY KEY(doctrine_delta_id,affected_object_id));
CREATE TABLE p3_family_genealogy (genealogy_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), relation_type TEXT NOT NULL CHECK(relation_type IN ('SPLIT','MERGE','SUPERSEDE','DEPRECATE')), adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id));
CREATE TABLE p3_family_genealogy_member (genealogy_id TEXT NOT NULL REFERENCES p3_family_genealogy(genealogy_id), family_id TEXT NOT NULL REFERENCES p3_canonical_family(canonical_family_id), genealogy_role TEXT NOT NULL CHECK(genealogy_role IN ('PREDECESSOR','SUCCESSOR')), PRIMARY KEY(genealogy_id,family_id,genealogy_role));
CREATE TABLE p3_dependency_edge (dependency_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), dependent_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), authority_input_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), dependency_role TEXT NOT NULL, dirty_if_changed BOOLEAN NOT NULL, impact_priority TEXT NOT NULL CHECK(impact_priority IN ('FATAL','HIGH','MEDIUM','LOW')), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(dependent_id,authority_input_id,dependency_role,authority_release_id));

CREATE TABLE p3_release_object_snapshot (release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), content_hash CHAR(64) NOT NULL CHECK(content_hash ~ '^[0-9a-f]{64}$'), PRIMARY KEY(release_id,object_id));
CREATE TABLE p3_release_change_ledger (release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), change_type TEXT NOT NULL CHECK(change_type IN ('ADDED','REVISED','SUPERSEDED','DEPRECATED','UNCHANGED_REFERENCE')), prior_content_hash CHAR(64), content_hash CHAR(64) NOT NULL, reason TEXT, PRIMARY KEY(release_id,object_id), CHECK(content_hash ~ '^[0-9a-f]{64}$'), CHECK(prior_content_hash IS NULL OR prior_content_hash ~ '^[0-9a-f]{64}$'));
CREATE TABLE p3_failure_ledger (failure_id TEXT PRIMARY KEY, build_run_id TEXT NOT NULL, severity TEXT NOT NULL CHECK(severity IN ('FATAL','ERROR','WARNING','INFO')), object_id TEXT REFERENCES p3_object_registry(object_id), failure_code TEXT NOT NULL, message TEXT NOT NULL, source_artifact TEXT, created_at TIMESTAMPTZ NOT NULL);


CREATE TABLE p3_categorical_field_binding (
    table_name TEXT NOT NULL, column_name TEXT NOT NULL, vocabulary_domain TEXT NOT NULL,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(table_name,column_name,authority_release_id)
);
CREATE OR REPLACE FUNCTION p3_enforce_vocab_code() RETURNS trigger AS $$
DECLARE v_domain TEXT := TG_ARGV[0]; v_column TEXT := TG_ARGV[1]; v_value TEXT;
BEGIN
    v_value := to_jsonb(NEW) ->> v_column;
    IF v_value IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM p3_vocabulary_code c
        WHERE c.vocabulary_domain=v_domain AND c.code=v_value
          AND c.retired_release_id IS NULL
    ) THEN
        RAISE EXCEPTION 'Unknown P3 vocabulary code %.%=%', TG_TABLE_NAME, v_column, v_value;
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;
-- Per-column triggers are generated from P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v2.csv
-- during migration assembly and validated before shadow installation.

CREATE VIEW p3_current_promoted_release AS
SELECT r.* FROM p3_authority_release r JOIN p3_runtime_promotion_pointer p ON p.promoted_release_id=r.release_id;

-- P3 excludes response transformation, causal direction, strata assignment, respondent joins, and simulation state.
ROLLBACK;
