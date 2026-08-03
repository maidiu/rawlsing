-- Rawlsing P3 PostgreSQL-Compatible Logical DDL v4
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
    object_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), upstream_phase TEXT NOT NULL, source_family TEXT, license_provenance_state TEXT NOT NULL,
    upstream_object_type TEXT NOT NULL, upstream_object_id TEXT NOT NULL, authority_artifact TEXT NOT NULL,
    authority_hash CHAR(64) NOT NULL CHECK (authority_hash ~ '^[0-9a-f]{64}$'), license_provenance_ref TEXT,
    read_only BOOLEAN NOT NULL DEFAULT TRUE CHECK (read_only), UNIQUE(upstream_phase,upstream_object_type,upstream_object_id)
);

CREATE TABLE p3_lineage_participation (lineage_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), participation_status TEXT NOT NULL, effective_pair_incident_count INTEGER NOT NULL CHECK(effective_pair_incident_count>=0), proposition_pair_incident_count INTEGER NOT NULL CHECK(proposition_pair_incident_count>=0), signature_requirement TEXT NOT NULL, authority_note TEXT, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), PRIMARY KEY(lineage_id,authority_release_id));
CREATE TABLE p3_lineage_disposition (subject_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), subject_type TEXT NOT NULL, disposition_status TEXT NOT NULL, reason TEXT NOT NULL, evidence_ids JSONB NOT NULL DEFAULT '[]'::jsonb, candidate_family_id TEXT, canonical_family_id TEXT, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), PRIMARY KEY(subject_id,authority_release_id));

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
    proposition_graph_allowed BOOLEAN NOT NULL, j_family_candidate_eligibility TEXT NOT NULL, creates_endpoint_authority BOOLEAN NOT NULL DEFAULT FALSE CHECK(NOT creates_endpoint_authority),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id <> right_object_id), CHECK(orientation='DIRECTIONAL' OR left_object_id < right_object_id),
    CHECK(proposition_graph_allowed=FALSE OR relation_type IN ('PROPOSITION_RESPONSE_IDENTITY','PROPOSITION_IDENTITY_ONLY'))
);
CREATE TABLE p3_pair_fact_source_authority (
    pair_fact_id TEXT NOT NULL REFERENCES p3_pair_fact_bundle(pair_fact_id), registry_code TEXT NOT NULL, authority_id TEXT NOT NULL, authority_role TEXT NOT NULL,
    governing BOOLEAN NOT NULL, superseded_by_authority_id TEXT, PRIMARY KEY(pair_fact_id,registry_code,authority_id), CHECK((authority_role='GOVERNING')=governing)
);
CREATE UNIQUE INDEX p3_pair_fact_one_governing_source ON p3_pair_fact_source_authority(pair_fact_id) WHERE governing;
CREATE TABLE p3_pair_fact_evidence (
    pair_fact_id TEXT NOT NULL REFERENCES p3_pair_fact_bundle(pair_fact_id), side TEXT NOT NULL CHECK(side IN ('LEFT','RIGHT','RELATION')),
    evidence_id TEXT NOT NULL, evidence_type TEXT NOT NULL, PRIMARY KEY(pair_fact_id,side,evidence_id)
);

CREATE TABLE p3_collision_scope_registry (
    collision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), collision_type TEXT NOT NULL, scope_type TEXT NOT NULL, orientation TEXT NOT NULL CHECK(orientation IN ('SYMMETRIC','DIRECTIONAL')), left_role TEXT, right_role TEXT,
    left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    hard_blocker BOOLEAN NOT NULL, source_scope TEXT, historical_scope JSONB, downstream_effects JSONB NOT NULL DEFAULT '[]'::jsonb,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id < right_object_id),
    CHECK((orientation='DIRECTIONAL' AND left_role IS NOT NULL AND right_role IS NOT NULL AND left_role<>right_role) OR (orientation='SYMMETRIC' AND left_role IS NULL AND right_role IS NULL))
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
    candidate_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id), revision_number INTEGER NOT NULL CHECK(revision_number>=1),
    lifecycle_stage TEXT NOT NULL CHECK(lifecycle_stage IN ('DISCOVERED','GENERATED_CANDIDATE','EVIDENCE_COMPLETE','ADJUDICATION_REQUIRED','DECIDED','SUPERSEDED','DEPRECATED')),
    candidate_classification TEXT NOT NULL CHECK(candidate_classification IN ('CLEAN_CANDIDATE','VARIANT_BEARING_CANDIDATE','SPLIT_RISK','HIERARCHY_ONLY_RISK','COLLISION_BEARING_CANDIDATE','STRUCTURE_ONLY_DIAGNOSTIC','INSUFFICIENT_AUTHORITY_RISK','SEMANTIC_ARTIFACT_RISK')),
    candidate_origin_type TEXT NOT NULL,
    canonical_signature_id TEXT REFERENCES p3_proposition_signature(signature_id), evidence_bundle_hash CHAR(64) NOT NULL CHECK(evidence_bundle_hash ~ '^[0-9a-f]{64}$'),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(candidate_family_id,revision_number), UNIQUE(candidate_family_id,authority_release_id)
);
CREATE TABLE p3_candidate_status_event (
    candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id), event_ordinal INTEGER NOT NULL CHECK(event_ordinal>=1),
    from_stage TEXT, to_stage TEXT NOT NULL, guard_evidence_id TEXT NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(candidate_family_id,event_ordinal)
);
CREATE TABLE p3_candidate_component_link (candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), component_id TEXT NOT NULL REFERENCES p3_candidate_component(component_id), PRIMARY KEY(candidate_revision_id,component_id));
CREATE TABLE p3_candidate_membership (candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), membership_role TEXT NOT NULL CHECK(membership_role IN ('PROPOSED_MEMBER','ACCEPTED_MEMBER','EXCLUDED_MEMBER','HIERARCHICAL_RELATIVE')), PRIMARY KEY(candidate_revision_id,member_object_id));
CREATE TABLE p3_candidate_diagnostic_flag (candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), flag TEXT NOT NULL, evidence_ids JSONB NOT NULL DEFAULT '[]'::jsonb, PRIMARY KEY(candidate_revision_id,flag));
CREATE TABLE p3_candidate_ranking (candidate_revision_id TEXT PRIMARY KEY REFERENCES p3_candidate_revision(candidate_revision_id), primary_class_rank INTEGER NOT NULL CHECK(primary_class_rank>=0), hard_collision_count INTEGER NOT NULL CHECK(hard_collision_count>=0), open_obligation_count INTEGER NOT NULL CHECK(open_obligation_count>=0), signature_completeness NUMERIC NOT NULL CHECK(signature_completeness>=0 AND signature_completeness<=1), source_count INTEGER NOT NULL CHECK(source_count>=1), lineage_count INTEGER NOT NULL CHECK(lineage_count>=2), direct_positive_density NUMERIC NOT NULL CHECK(direct_positive_density>=0 AND direct_positive_density<=1), structure_support_count INTEGER NOT NULL CHECK(structure_support_count>=0), response_variant_complexity INTEGER NOT NULL CHECK(response_variant_complexity>=0), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id));
CREATE TABLE p3_internal_pair_matrix (
    candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), pair_state TEXT NOT NULL CHECK(pair_state IN ('DIRECT_POSITIVE','DIRECT_COLLISION','DIRECT_UNRESOLVED','HIERARCHICAL_ONLY','UNRULED','SIGNATURE_CONFLICT','SIGNATURE_COMPATIBLE')),
    direct_pair_fact_id TEXT REFERENCES p3_pair_fact_bundle(pair_fact_id), collision_id TEXT REFERENCES p3_collision_scope_registry(collision_id),
    PRIMARY KEY(candidate_revision_id,left_object_id,right_object_id), CHECK(left_object_id < right_object_id)
);
CREATE TABLE p3_closure_obligation (
    closure_obligation_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id),
    left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), obligation_type TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('OPEN','RESOLVED_ACCEPT','RESOLVED_SPLIT','RESOLVED_EXCLUDE','FAIL_CLOSED')), resolution_adjudication_id TEXT,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id < right_object_id)
);

CREATE TABLE p3_family_variant (variant_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), owner_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), created_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id));
CREATE TABLE p3_family_variant_revision (
    variant_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), variant_id TEXT NOT NULL REFERENCES p3_family_variant(variant_id), revision_number INTEGER NOT NULL CHECK(revision_number>=1),
    variant_dimension TEXT NOT NULL CHECK(variant_dimension IN ('RESPONSE_TOPOLOGY','WORDING_TRANSLATION','SOURCE_RESPONSE_FORM','HISTORICAL_INTERVAL','OTHER_EXPLICITLY_GOVERNED')),
    variant_value TEXT NOT NULL, value_portability_status TEXT NOT NULL DEFAULT 'NOT_AUTHORIZED_BY_P3' CHECK(value_portability_status='NOT_AUTHORIZED_BY_P3'),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(variant_id,revision_number), UNIQUE(variant_id,authority_release_id)
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
    adjudication_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), decision_ordinal INTEGER NOT NULL CHECK(decision_ordinal>=1),
    decision_status TEXT NOT NULL CHECK(decision_status IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS','SPLIT_REQUIRED','HIERARCHICAL_RELATION_ONLY','BLOCKED_UNRESOLVED','INSUFFICIENT_AUTHORITY','REJECTED_SEMANTIC_ARTIFACT','REJECTED')),
    canonical_family_id TEXT REFERENCES p3_object_registry(object_id), canonical_proposition JSONB, response_portability_status TEXT NOT NULL DEFAULT 'NOT_AUTHORIZED_BY_P3' CHECK(response_portability_status='NOT_AUTHORIZED_BY_P3'),
    unresolved_boundaries JSONB NOT NULL DEFAULT '[]'::jsonb, rationale TEXT NOT NULL, evidence_bundle_hash CHAR(64) NOT NULL CHECK(evidence_bundle_hash ~ '^[0-9a-f]{64}$'),
    supersedes_adjudication_id TEXT REFERENCES p3_adjudication_decision(adjudication_id), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), created_at TIMESTAMPTZ NOT NULL, UNIQUE(candidate_revision_id,decision_ordinal)
);
ALTER TABLE p3_adjudication_decision ADD CONSTRAINT p3_adjudication_status_fields CHECK (
    (decision_status IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') AND canonical_family_id IS NOT NULL AND canonical_proposition IS NOT NULL)
 OR (decision_status NOT IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') AND canonical_family_id IS NULL AND canonical_proposition IS NULL)
);
CREATE TABLE p3_adjudication_member (adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), member_disposition TEXT NOT NULL CHECK(member_disposition IN ('ACCEPT','EXCLUDE','HIERARCHICAL','UNRESOLVED')), variant_revision_id TEXT REFERENCES p3_family_variant_revision(variant_revision_id), PRIMARY KEY(adjudication_id,member_object_id));
CREATE TABLE p3_adjudication_collision_disposition (adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), collision_id TEXT NOT NULL REFERENCES p3_collision_scope_registry(collision_id), disposition TEXT NOT NULL, rationale TEXT NOT NULL, PRIMARY KEY(adjudication_id,collision_id));
CREATE TABLE p3_adjudication_hierarchy_relation (adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), broader_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), narrower_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), relation_role TEXT NOT NULL, PRIMARY KEY(adjudication_id,broader_object_id,narrower_object_id));
CREATE TABLE p3_adjudication_split_point (
    adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), split_ordinal INTEGER NOT NULL CHECK(split_ordinal>=1),
    dimension TEXT NOT NULL, rationale TEXT NOT NULL, PRIMARY KEY(adjudication_id,split_ordinal)
);
CREATE TABLE p3_adjudication_split_member (
    adjudication_id TEXT NOT NULL, split_ordinal INTEGER NOT NULL, split_side TEXT NOT NULL CHECK(split_side IN ('LEFT','RIGHT')),
    member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    PRIMARY KEY(adjudication_id,split_ordinal,split_side,member_object_id),
    FOREIGN KEY(adjudication_id,split_ordinal) REFERENCES p3_adjudication_split_point(adjudication_id,split_ordinal)
);
CREATE TABLE p3_adjudication_unresolved_boundary (
    adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), boundary_id TEXT NOT NULL,
    left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    reason TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('OPEN','FAIL_CLOSED','RESOLVED_ACCEPT','RESOLVED_EXCLUDE','RESOLVED_SPLIT')),
    PRIMARY KEY(adjudication_id,boundary_id), CHECK(left_object_id < right_object_id)
);

CREATE TABLE p3_canonical_family (canonical_family_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), created_by_adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), created_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), retired_release_id TEXT REFERENCES p3_authority_release(release_id));
CREATE TABLE p3_canonical_family_revision (
    family_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), canonical_family_id TEXT NOT NULL REFERENCES p3_canonical_family(canonical_family_id), revision_number INTEGER NOT NULL CHECK(revision_number>=1),
    canonical_signature_id TEXT NOT NULL REFERENCES p3_proposition_signature(signature_id), canonical_proposition JSONB NOT NULL, evidence_bundle_hash CHAR(64) NOT NULL CHECK(evidence_bundle_hash ~ '^[0-9a-f]{64}$'),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(canonical_family_id,revision_number), UNIQUE(canonical_family_id,authority_release_id)
);
CREATE TABLE p3_canonical_family_membership (family_revision_id TEXT NOT NULL REFERENCES p3_canonical_family_revision(family_revision_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), variant_revision_id TEXT REFERENCES p3_family_variant_revision(variant_revision_id), PRIMARY KEY(family_revision_id,member_object_id));


ALTER TABLE p3_closure_obligation ADD CONSTRAINT p3_closure_resolution_adjudication_fk FOREIGN KEY(resolution_adjudication_id) REFERENCES p3_adjudication_decision(adjudication_id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE p3_adjudication_decision ADD CONSTRAINT p3_adjudication_canonical_family_fk FOREIGN KEY(canonical_family_id) REFERENCES p3_canonical_family(canonical_family_id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE p3_lineage_disposition ADD CONSTRAINT p3_lineage_disposition_candidate_family_fk FOREIGN KEY(candidate_family_id) REFERENCES p3_candidate_family(candidate_family_id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE p3_lineage_disposition ADD CONSTRAINT p3_lineage_disposition_canonical_family_fk FOREIGN KEY(canonical_family_id) REFERENCES p3_canonical_family(canonical_family_id) DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE p3_doctrine_delta (doctrine_delta_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), trigger_candidate_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id), old_rule TEXT, new_rule TEXT NOT NULL, required_rebuild_scope TEXT NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id));
CREATE TABLE p3_doctrine_delta_affected_object (doctrine_delta_id TEXT NOT NULL REFERENCES p3_doctrine_delta(doctrine_delta_id), affected_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), PRIMARY KEY(doctrine_delta_id,affected_object_id));
CREATE TABLE p3_family_genealogy (genealogy_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), relation_type TEXT NOT NULL CHECK(relation_type IN ('SPLIT','MERGE','SUPERSEDE','DEPRECATE')), adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id));
CREATE TABLE p3_family_genealogy_member (genealogy_id TEXT NOT NULL REFERENCES p3_family_genealogy(genealogy_id), family_id TEXT NOT NULL REFERENCES p3_canonical_family(canonical_family_id), genealogy_role TEXT NOT NULL CHECK(genealogy_role IN ('PREDECESSOR','SUCCESSOR')), PRIMARY KEY(genealogy_id,family_id,genealogy_role));
CREATE TABLE p3_dependency_edge (dependency_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), dependent_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), authority_input_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), dependency_role TEXT NOT NULL, dirty_if_changed BOOLEAN NOT NULL, impact_priority TEXT NOT NULL CHECK(impact_priority IN ('FATAL','HIGH','MEDIUM','LOW')), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(dependent_id,authority_input_id,dependency_role,authority_release_id));

CREATE TABLE p3_release_object_snapshot (release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), content_hash CHAR(64) NOT NULL CHECK(content_hash ~ '^[0-9a-f]{64}$'), PRIMARY KEY(release_id,object_id));
CREATE TABLE p3_release_change_ledger (release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), change_type TEXT NOT NULL CHECK(change_type IN ('ADDED','REVISED','SUPERSEDED','DEPRECATED','UNCHANGED_REFERENCE')), prior_content_hash CHAR(64), content_hash CHAR(64) NOT NULL, reason TEXT, PRIMARY KEY(release_id,object_id), CHECK(content_hash ~ '^[0-9a-f]{64}$'), CHECK(prior_content_hash IS NULL OR prior_content_hash ~ '^[0-9a-f]{64}$'));
CREATE TABLE p3_failure_ledger (failure_id TEXT PRIMARY KEY, build_run_id TEXT NOT NULL, severity TEXT NOT NULL CHECK(severity IN ('FATAL','ERROR','WARNING','INFO')), object_id TEXT REFERENCES p3_object_registry(object_id), failure_code TEXT NOT NULL, message TEXT NOT NULL, source_artifact TEXT, created_at TIMESTAMPTZ NOT NULL);


CREATE TABLE p3_object_reference_type_contract (table_name TEXT NOT NULL, column_name TEXT NOT NULL, allowed_object_types TEXT[] NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), PRIMARY KEY(table_name,column_name,authority_release_id));

CREATE TABLE p3_categorical_field_binding (
    table_name TEXT NOT NULL, column_name TEXT NOT NULL, vocabulary_domain TEXT NOT NULL,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(table_name,column_name,authority_release_id)
);
CREATE TABLE p3_identity_key_contract (
    object_type TEXT NOT NULL, identity_strategy TEXT NOT NULL, id_pattern TEXT NOT NULL, idempotency_key_spec TEXT NOT NULL,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), PRIMARY KEY(object_type,authority_release_id)
);
CREATE TABLE p3_candidate_lifecycle_transition (
    from_stage TEXT, to_stage TEXT NOT NULL, guard_text TEXT NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    UNIQUE(from_stage,to_stage,authority_release_id)
);
CREATE TABLE p3_release_lifecycle_transition (
    from_status TEXT, to_status TEXT NOT NULL, guard_text TEXT NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    UNIQUE(from_status,to_status,authority_release_id)
);
CREATE TABLE p3_hyperedge_role_type_contract (
    hyperedge_type TEXT NOT NULL, participant_role TEXT NOT NULL, allowed_object_types TEXT[] NOT NULL,
    minimum_count INTEGER NOT NULL CHECK(minimum_count>=0), maximum_count INTEGER CHECK(maximum_count IS NULL OR maximum_count>=minimum_count),
    authority_effect_ceiling TEXT NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(hyperedge_type,participant_role,authority_release_id)
);
CREATE OR REPLACE FUNCTION p3_enforce_vocab_code() RETURNS trigger AS $$
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
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_enforce_object_reference_type() RETURNS trigger AS $$
DECLARE v_column TEXT := TG_ARGV[0]; v_allowed TEXT[] := string_to_array(TG_ARGV[1], '|'); v_object_id TEXT; v_actual TEXT;
BEGIN
    v_object_id := to_jsonb(NEW) ->> v_column;
    IF v_object_id IS NULL THEN RETURN NEW; END IF;
    SELECT object_type INTO v_actual FROM p3_object_registry WHERE object_id=v_object_id;
    IF v_actual IS NULL OR NOT (v_actual = ANY(v_allowed)) THEN
        RAISE EXCEPTION 'Invalid P3 object type %.%=% actual=% allowed=%', TG_TABLE_NAME, v_column, v_object_id, v_actual, v_allowed;
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_enforce_identity_contract() RETURNS trigger AS $$
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
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_hyperedge_member_type() RETURNS trigger AS $$
DECLARE h RECORD; c RECORD; actual TEXT;
BEGIN
    SELECT hyperedge_type,authority_effect,authority_release_id INTO h FROM p3_hyperedge WHERE hyperedge_id=NEW.hyperedge_id;
    SELECT * INTO c FROM p3_hyperedge_role_type_contract WHERE hyperedge_type=h.hyperedge_type AND participant_role=NEW.participant_role AND authority_release_id=h.authority_release_id;
    SELECT object_type INTO actual FROM p3_object_registry WHERE object_id=NEW.object_id;
    IF c.hyperedge_type IS NULL OR NOT(actual=ANY(c.allowed_object_types)) OR h.authority_effect<>c.authority_effect_ceiling THEN
        RAISE EXCEPTION 'Invalid hyperedge participant %, role %, type %, effect %',NEW.object_id,NEW.participant_role,actual,h.authority_effect;
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_hyperedge_cardinality() RETURNS trigger AS $$
DECLARE hid TEXT:=COALESCE(NEW.hyperedge_id,OLD.hyperedge_id); h RECORD; c RECORD; n INTEGER;
BEGIN
    SELECT hyperedge_type,authority_release_id INTO h FROM p3_hyperedge WHERE hyperedge_id=hid;
    IF h.hyperedge_type IS NULL THEN RETURN COALESCE(NEW,OLD); END IF;
    FOR c IN SELECT * FROM p3_hyperedge_role_type_contract WHERE hyperedge_type=h.hyperedge_type AND authority_release_id=h.authority_release_id LOOP
        SELECT COUNT(*) INTO n FROM p3_hyperedge_membership WHERE hyperedge_id=hid AND participant_role=c.participant_role;
        IF n<c.minimum_count OR (c.maximum_count IS NOT NULL AND n>c.maximum_count) THEN RAISE EXCEPTION 'Hyperedge % role % cardinality % outside [%..%]',hid,c.participant_role,n,c.minimum_count,c.maximum_count; END IF;
    END LOOP;
    IF TG_OP='DELETE' THEN RETURN OLD; ELSE RETURN NEW; END IF;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_forbid_update_delete() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'P3 append-only authority table % rejects %', TG_TABLE_NAME, TG_OP;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_candidate_status_event() RETURNS trigger AS $$
DECLARE p_stage TEXT; p_ord INTEGER;
BEGIN
    SELECT to_stage,event_ordinal INTO p_stage,p_ord FROM p3_candidate_status_event
    WHERE candidate_family_id=NEW.candidate_family_id ORDER BY event_ordinal DESC LIMIT 1;
    IF p_ord IS NULL THEN
        IF NEW.event_ordinal<>1 OR NEW.from_stage IS NOT NULL OR NEW.to_stage<>'DISCOVERED' THEN RAISE EXCEPTION 'Invalid first candidate event'; END IF;
    ELSE
        IF NEW.event_ordinal<>p_ord+1 OR NEW.from_stage IS DISTINCT FROM p_stage THEN RAISE EXCEPTION 'Noncontiguous candidate event'; END IF;
        IF NOT EXISTS (SELECT 1 FROM p3_candidate_lifecycle_transition t WHERE t.from_stage=NEW.from_stage AND t.to_stage=NEW.to_stage AND t.authority_release_id=NEW.authority_release_id) THEN RAISE EXCEPTION 'Disallowed candidate transition % -> %',NEW.from_stage,NEW.to_stage; END IF;
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_release_status_event() RETURNS trigger AS $$
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
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_promotion_pointer() RETURNS trigger AS $$
DECLARE latest_status TEXT;
BEGIN
    SELECT status INTO latest_status FROM p3_release_status_event WHERE release_id=NEW.promoted_release_id ORDER BY event_ordinal DESC LIMIT 1;
    IF latest_status IS DISTINCT FROM 'PROMOTED' THEN RAISE EXCEPTION 'Promotion pointer requires latest PROMOTED event, got %',latest_status; END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE p3_install_contract_triggers(p_release_id TEXT) LANGUAGE plpgsql AS $$
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

CREATE TRIGGER p3_object_registry_identity_validate BEFORE INSERT OR UPDATE ON p3_object_registry FOR EACH ROW EXECUTE FUNCTION p3_enforce_identity_contract();
CREATE TRIGGER p3_hyperedge_member_type_validate BEFORE INSERT OR UPDATE ON p3_hyperedge_membership FOR EACH ROW EXECUTE FUNCTION p3_validate_hyperedge_member_type();
CREATE CONSTRAINT TRIGGER p3_hyperedge_member_cardinality AFTER INSERT OR UPDATE OR DELETE ON p3_hyperedge_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_hyperedge_cardinality();
CREATE CONSTRAINT TRIGGER p3_hyperedge_cardinality_after_header AFTER INSERT OR UPDATE ON p3_hyperedge DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_hyperedge_cardinality();

CREATE TRIGGER p3_candidate_status_event_validate BEFORE INSERT ON p3_candidate_status_event FOR EACH ROW EXECUTE FUNCTION p3_validate_candidate_status_event();
CREATE TRIGGER p3_release_status_event_validate BEFORE INSERT ON p3_release_status_event FOR EACH ROW EXECUTE FUNCTION p3_validate_release_status_event();
CREATE TRIGGER p3_promotion_pointer_validate BEFORE INSERT OR UPDATE ON p3_runtime_promotion_pointer FOR EACH ROW EXECUTE FUNCTION p3_validate_promotion_pointer();

CREATE TRIGGER p3_adjudication_decision_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_decision FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_member_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_member FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_collision_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_collision_disposition FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_hierarchy_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_hierarchy_relation FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_split_point_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_split_point FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_split_member_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_split_member FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_unresolved_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_unresolved_boundary FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_candidate_revision_immutable BEFORE UPDATE OR DELETE ON p3_candidate_revision FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_variant_revision_immutable BEFORE UPDATE OR DELETE ON p3_family_variant_revision FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_family_exclusion_immutable BEFORE UPDATE OR DELETE ON p3_family_exclusion FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_hyperedge_immutable BEFORE UPDATE OR DELETE ON p3_hyperedge FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_canonical_family_revision_immutable BEFORE UPDATE OR DELETE ON p3_canonical_family_revision FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_release_event_immutable BEFORE UPDATE OR DELETE ON p3_release_status_event FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_candidate_event_immutable BEFORE UPDATE OR DELETE ON p3_candidate_status_event FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_doctrine_delta_immutable BEFORE UPDATE OR DELETE ON p3_doctrine_delta FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_family_genealogy_immutable BEFORE UPDATE OR DELETE ON p3_family_genealogy FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();

CREATE VIEW p3_current_promoted_release AS
SELECT r.* FROM p3_authority_release r JOIN p3_runtime_promotion_pointer p ON p.promoted_release_id=r.release_id;

-- P3 excludes response transformation, causal direction, strata assignment, respondent joins, and simulation state.
ROLLBACK;
