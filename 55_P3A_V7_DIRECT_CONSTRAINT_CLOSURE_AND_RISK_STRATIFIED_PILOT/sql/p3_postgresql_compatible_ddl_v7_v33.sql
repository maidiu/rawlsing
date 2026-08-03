-- Rawlsing P3 PostgreSQL-Compatible Logical DDL v6
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
    CHECK (identity_strategy IN ('INHERITED_UPSTREAM_ID','CONTENT_ADDRESSED_DERIVED_ID','REGISTRY_ALLOCATED_DURABLE_ID')),
    UNIQUE (object_id, object_type)
);
CREATE TABLE p3_upstream_object_reference (
    object_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), upstream_phase TEXT NOT NULL, source_family TEXT, license_provenance_state TEXT NOT NULL,
    upstream_object_type TEXT NOT NULL, upstream_object_id TEXT NOT NULL, authority_artifact TEXT NOT NULL,
    authority_hash CHAR(64) NOT NULL CHECK (authority_hash ~ '^[0-9a-f]{64}$'), license_provenance_ref TEXT,
    read_only BOOLEAN NOT NULL DEFAULT TRUE CHECK (read_only), UNIQUE(upstream_phase,upstream_object_type,upstream_object_id)
);
CREATE TABLE p3_imported_lineage_membership (
    lineage_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    implementation_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    ordinal_position INTEGER NOT NULL CHECK(ordinal_position>=0), source_authority_id TEXT NOT NULL,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(lineage_id,implementation_id,authority_release_id),
    UNIQUE(implementation_id,authority_release_id), UNIQUE(lineage_id,ordinal_position,authority_release_id)
);

CREATE TABLE p3_lineage_participation (lineage_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), participation_status TEXT NOT NULL, effective_pair_incident_count INTEGER NOT NULL CHECK(effective_pair_incident_count>=0), proposition_pair_incident_count INTEGER NOT NULL CHECK(proposition_pair_incident_count>=0), signature_requirement TEXT NOT NULL, authority_note TEXT, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), PRIMARY KEY(lineage_id,authority_release_id));
CREATE TABLE p3_lineage_disposition (
    subject_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    subject_type TEXT NOT NULL CHECK(subject_type IN ('IMPORTED_SOURCE_LOCAL_LINEAGE','LINEAGE_SEGMENT')),
    disposition_status TEXT NOT NULL CHECK(disposition_status IN ('ADMINISTRATIVE_METADATA_PRESERVED','BLOCKED_UNRESOLVED','CANDIDATE_PARTICIPANT','CANONICAL_MEMBER','CONSTRAINT_ONLY_PRESERVED','DERIVED_OR_INDEX_PRESERVED','OUT_OF_SCOPE_NONQUESTION','SOURCE_LOCAL_SINGLETON_PRESERVED','SUPERSEDED_BY_SEGMENT','UNADJUDICATED')),
    reason TEXT NOT NULL,
    canonical_family_id TEXT REFERENCES p3_object_registry(object_id),
    evidence_ids JSONB NOT NULL CHECK(jsonb_typeof(evidence_ids)='array'),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(subject_id,authority_release_id),
    CHECK((disposition_status='CANONICAL_MEMBER')=(canonical_family_id IS NOT NULL))
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
CREATE TABLE p3_pair_endpoint_resolution (
    pair_fact_id TEXT NOT NULL REFERENCES p3_pair_fact_bundle(pair_fact_id), endpoint_side TEXT NOT NULL CHECK(endpoint_side IN ('LEFT','RIGHT')),
    original_lineage_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), resolution_status TEXT NOT NULL CHECK(resolution_status IN ('ORIGINAL_LINEAGE','SEGMENT_BOUND','BLOCKED_HETEROGENEOUS','FAIL_CLOSED_UNRESOLVED')),
    evidence_ids JSONB NOT NULL DEFAULT '[]'::jsonb, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(pair_fact_id,endpoint_side)
);
CREATE TABLE p3_pair_endpoint_resolved_subject (
    pair_fact_id TEXT NOT NULL, endpoint_side TEXT NOT NULL, resolved_subject_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    PRIMARY KEY(pair_fact_id,endpoint_side,resolved_subject_id),
    FOREIGN KEY(pair_fact_id,endpoint_side) REFERENCES p3_pair_endpoint_resolution(pair_fact_id,endpoint_side)
);


CREATE TABLE p3_pair_projection (
    projection_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id),
    pair_fact_id TEXT NOT NULL REFERENCES p3_pair_fact_bundle(pair_fact_id),
    left_subject_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    right_subject_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    projection_basis TEXT NOT NULL CHECK(projection_basis IN ('ORIGINAL_LINEAGES','SEGMENT_BINDING')),
    evidence_ids JSONB NOT NULL CHECK(jsonb_typeof(evidence_ids)='array' AND jsonb_array_length(evidence_ids)>0),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    UNIQUE(pair_fact_id,left_subject_id,right_subject_id)
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
    component_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), component_type TEXT NOT NULL CHECK(component_type IN ('STRICT_RESPONSE_COMPONENT','PROPOSITION_ONLY_COMPONENT')),
    build_rule_version TEXT NOT NULL, content_hash CHAR(64) NOT NULL CHECK(content_hash ~ '^[0-9a-f]{64}$'),
    connectivity_edge_count INTEGER NOT NULL CHECK(connectivity_edge_count>=1), member_count INTEGER NOT NULL CHECK(member_count>=2),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);
CREATE TABLE p3_component_membership (component_id TEXT NOT NULL REFERENCES p3_candidate_component(component_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), PRIMARY KEY(component_id,member_object_id));
CREATE TABLE p3_component_connectivity_edge (
    component_id TEXT NOT NULL REFERENCES p3_candidate_component(component_id),
    projection_id TEXT NOT NULL REFERENCES p3_pair_projection(projection_id),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(component_id,projection_id)
);

CREATE TABLE p3_candidate_family (
    candidate_family_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), created_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id)
);
CREATE TABLE p3_candidate_revision (
    candidate_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id), revision_number INTEGER NOT NULL CHECK(revision_number>=1),
    candidate_classification TEXT NOT NULL CHECK(candidate_classification IN ('CLEAN_CANDIDATE','VARIANT_BEARING_CANDIDATE','SPLIT_RISK','HIERARCHY_ONLY_RISK','COLLISION_BEARING_CANDIDATE','STRUCTURE_ONLY_DIAGNOSTIC','INSUFFICIENT_AUTHORITY_RISK','SEMANTIC_ARTIFACT_RISK')),
    candidate_origin_type TEXT NOT NULL,
    origin_key CHAR(64) NOT NULL CHECK(origin_key ~ '^[0-9a-f]{64}$' AND origin_key !~ '^0{64}$'),
    canonical_signature_id TEXT REFERENCES p3_proposition_signature(signature_id), evidence_bundle_hash CHAR(64) NOT NULL CHECK(evidence_bundle_hash ~ '^[0-9a-f]{64}$'),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(candidate_family_id,revision_number), UNIQUE(candidate_family_id,authority_release_id), UNIQUE(authority_release_id,origin_key)
);
CREATE TABLE p3_candidate_status_event (
    candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id), candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id),
    event_ordinal INTEGER NOT NULL CHECK(event_ordinal>=1), from_stage TEXT, to_stage TEXT NOT NULL, guard_evidence_id TEXT NOT NULL, occurred_at TIMESTAMPTZ NOT NULL,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), PRIMARY KEY(candidate_revision_id,event_ordinal)
);
CREATE TABLE p3_candidate_component_link (candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), component_id TEXT NOT NULL REFERENCES p3_candidate_component(component_id), PRIMARY KEY(candidate_revision_id,component_id));
CREATE TABLE p3_candidate_membership (
    candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id),
    member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    membership_role TEXT NOT NULL CHECK(membership_role IN ('PROPOSED_MEMBER','PROPOSED_HIERARCHICAL_CONTEXT')),
    membership_basis TEXT NOT NULL CHECK(membership_basis IN ('COMPONENT_MEMBER','ATTACHMENT_PROJECTION','DIRECT_DIAGNOSTIC','HIERARCHICAL_CONTEXT')),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(candidate_revision_id,member_object_id)
);

CREATE TABLE p3_candidate_attachment_projection (
    candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id),
    projection_id TEXT NOT NULL REFERENCES p3_pair_projection(projection_id),
    attachment_role TEXT NOT NULL CHECK(attachment_role IN ('ORPHAN_ATTACHMENT','STRICT_COMPONENT_BRIDGE','SEED_TO_STRICT_BRIDGE','ATTACHMENT_GROUP_CONNECTOR')),
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(candidate_revision_id,projection_id)
);

CREATE TABLE p3_candidate_diagnostic_flag (candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), flag TEXT NOT NULL, evidence_ids JSONB NOT NULL DEFAULT '[]'::jsonb, PRIMARY KEY(candidate_revision_id,flag));
CREATE TABLE p3_candidate_ranking (candidate_revision_id TEXT PRIMARY KEY REFERENCES p3_candidate_revision(candidate_revision_id), primary_class_rank INTEGER NOT NULL CHECK(primary_class_rank>=0), hard_collision_count INTEGER NOT NULL CHECK(hard_collision_count>=0), open_obligation_count INTEGER NOT NULL CHECK(open_obligation_count>=0), signature_completeness NUMERIC NOT NULL CHECK(signature_completeness>=0 AND signature_completeness<=1), source_count INTEGER NOT NULL CHECK(source_count>=1), lineage_count INTEGER NOT NULL CHECK(lineage_count>=2), direct_positive_density NUMERIC NOT NULL CHECK(direct_positive_density>=0 AND direct_positive_density<=1), structure_support_count INTEGER NOT NULL CHECK(structure_support_count>=0), response_variant_complexity INTEGER NOT NULL CHECK(response_variant_complexity>=0), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id));
CREATE TABLE p3_internal_pair_matrix (
    candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id),
    left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    pair_state TEXT NOT NULL CHECK(pair_state IN ('DIRECT_POSITIVE','DIRECT_COLLISION','DIRECT_UNRESOLVED','HIERARCHICAL_ONLY','UNRULED','SIGNATURE_CONFLICT','SIGNATURE_COMPATIBLE')),
    direct_pair_projection_id TEXT REFERENCES p3_pair_projection(projection_id),
    PRIMARY KEY(candidate_revision_id,left_object_id,right_object_id),
    CHECK(left_object_id < right_object_id),
    CHECK((pair_state IN ('UNRULED','SIGNATURE_CONFLICT','SIGNATURE_COMPATIBLE') AND direct_pair_projection_id IS NULL) OR (pair_state IN ('DIRECT_POSITIVE','DIRECT_COLLISION','DIRECT_UNRESOLVED','HIERARCHICAL_ONLY') AND direct_pair_projection_id IS NOT NULL))
);
CREATE TABLE p3_internal_pair_collision (
    candidate_revision_id TEXT NOT NULL, left_object_id TEXT NOT NULL, right_object_id TEXT NOT NULL,
    collision_id TEXT NOT NULL REFERENCES p3_collision_scope_registry(collision_id), PRIMARY KEY(candidate_revision_id,left_object_id,right_object_id,collision_id),
    FOREIGN KEY(candidate_revision_id,left_object_id,right_object_id) REFERENCES p3_internal_pair_matrix(candidate_revision_id,left_object_id,right_object_id)
);
CREATE TABLE p3_closure_obligation (
    closure_obligation_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id),
    left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), obligation_type TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('OPEN','RESOLVED_ACCEPT','RESOLVED_SPLIT','RESOLVED_EXCLUDE','FAIL_CLOSED')), resolution_adjudication_id TEXT,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id < right_object_id),
    UNIQUE(candidate_revision_id,left_object_id,right_object_id,obligation_type),
    CHECK((status IN ('RESOLVED_ACCEPT','RESOLVED_SPLIT','RESOLVED_EXCLUDE'))=(resolution_adjudication_id IS NOT NULL))
);
CREATE TABLE p3_internal_pair_closure (
    candidate_revision_id TEXT NOT NULL, left_object_id TEXT NOT NULL, right_object_id TEXT NOT NULL,
    closure_obligation_id TEXT NOT NULL REFERENCES p3_closure_obligation(closure_obligation_id),
    PRIMARY KEY(candidate_revision_id,left_object_id,right_object_id,closure_obligation_id),
    FOREIGN KEY(candidate_revision_id,left_object_id,right_object_id) REFERENCES p3_internal_pair_matrix(candidate_revision_id,left_object_id,right_object_id)
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
    rationale TEXT NOT NULL, evidence_bundle_hash CHAR(64) NOT NULL CHECK(evidence_bundle_hash ~ '^[0-9a-f]{64}$'),
    supersedes_adjudication_id TEXT REFERENCES p3_adjudication_decision(adjudication_id), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), created_at TIMESTAMPTZ NOT NULL, UNIQUE(candidate_revision_id,decision_ordinal)
);
ALTER TABLE p3_adjudication_decision ADD CONSTRAINT p3_adjudication_status_fields CHECK (
    (decision_status IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') AND canonical_family_id IS NOT NULL AND canonical_proposition IS NOT NULL)
 OR (decision_status NOT IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') AND canonical_family_id IS NULL AND canonical_proposition IS NULL)
);
CREATE TABLE p3_adjudication_member (adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), member_disposition TEXT NOT NULL CHECK(member_disposition IN ('ACCEPT','EXCLUDE','HIERARCHICAL','UNRESOLVED','SPLIT')), variant_revision_id TEXT REFERENCES p3_family_variant_revision(variant_revision_id), PRIMARY KEY(adjudication_id,member_object_id));
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


CREATE TABLE p3_adjudication_split_result (
    adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id),
    result_ordinal INTEGER NOT NULL CHECK(result_ordinal>=1),
    successor_candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id),
    successor_origin_key CHAR(64) NOT NULL CHECK(successor_origin_key ~ '^[0-9a-f]{64}$' AND successor_origin_key !~ '^0{64}$'),
    rationale TEXT NOT NULL,
    PRIMARY KEY(adjudication_id,result_ordinal),
    UNIQUE(adjudication_id,successor_candidate_family_id)
);
CREATE TABLE p3_adjudication_split_result_member (
    adjudication_id TEXT NOT NULL,
    result_ordinal INTEGER NOT NULL,
    member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    PRIMARY KEY(adjudication_id,result_ordinal,member_object_id),
    FOREIGN KEY(adjudication_id,result_ordinal) REFERENCES p3_adjudication_split_result(adjudication_id,result_ordinal)
);
CREATE TABLE p3_variant_promotion (
    adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id),
    candidate_variant_revision_id TEXT NOT NULL REFERENCES p3_family_variant_revision(variant_revision_id),
    canonical_variant_revision_id TEXT NOT NULL REFERENCES p3_family_variant_revision(variant_revision_id),
    PRIMARY KEY(adjudication_id,candidate_variant_revision_id), UNIQUE(canonical_variant_revision_id)
);
CREATE TABLE p3_exclusion_promotion (
    adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id),
    candidate_exclusion_id TEXT NOT NULL REFERENCES p3_family_exclusion(exclusion_id),
    canonical_exclusion_id TEXT NOT NULL REFERENCES p3_family_exclusion(exclusion_id),
    PRIMARY KEY(adjudication_id,candidate_exclusion_id), UNIQUE(canonical_exclusion_id)
);

CREATE TABLE p3_canonical_family (canonical_family_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), created_by_adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), created_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), retired_release_id TEXT REFERENCES p3_authority_release(release_id));
CREATE TABLE p3_canonical_family_revision (
    family_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), canonical_family_id TEXT NOT NULL REFERENCES p3_canonical_family(canonical_family_id), revision_number INTEGER NOT NULL CHECK(revision_number>=1),
    canonical_signature_id TEXT NOT NULL REFERENCES p3_proposition_signature(signature_id), canonical_proposition JSONB NOT NULL, evidence_bundle_hash CHAR(64) NOT NULL CHECK(evidence_bundle_hash ~ '^[0-9a-f]{64}$'),
    created_by_adjudication_id TEXT NOT NULL UNIQUE REFERENCES p3_adjudication_decision(adjudication_id), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(canonical_family_id,revision_number), UNIQUE(canonical_family_id,authority_release_id)
);
CREATE TABLE p3_canonical_family_membership (family_revision_id TEXT NOT NULL REFERENCES p3_canonical_family_revision(family_revision_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), variant_revision_id TEXT REFERENCES p3_family_variant_revision(variant_revision_id), PRIMARY KEY(family_revision_id,member_object_id));


ALTER TABLE p3_closure_obligation ADD CONSTRAINT p3_closure_resolution_adjudication_fk FOREIGN KEY(resolution_adjudication_id) REFERENCES p3_adjudication_decision(adjudication_id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE p3_adjudication_decision ADD CONSTRAINT p3_adjudication_canonical_family_fk FOREIGN KEY(canonical_family_id) REFERENCES p3_canonical_family(canonical_family_id) DEFERRABLE INITIALLY DEFERRED;
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

CREATE OR REPLACE FUNCTION p3_guard_object_registry_mutation() RETURNS trigger AS $$
BEGIN
    IF TG_OP='DELETE' THEN RAISE EXCEPTION 'P3 object registry is append-only'; END IF;
    IF NEW.object_id IS DISTINCT FROM OLD.object_id OR NEW.object_type IS DISTINCT FROM OLD.object_type OR NEW.identity_strategy IS DISTINCT FROM OLD.identity_strategy
       OR NEW.idempotency_key IS DISTINCT FROM OLD.idempotency_key OR NEW.origin_phase IS DISTINCT FROM OLD.origin_phase OR NEW.origin_authority_id IS DISTINCT FROM OLD.origin_authority_id
       OR NEW.allocation_release_id IS DISTINCT FROM OLD.allocation_release_id OR NEW.content_hash IS DISTINCT FROM OLD.content_hash OR NEW.stable_identity_note IS DISTINCT FROM OLD.stable_identity_note
       OR (OLD.retired_release_id IS NOT NULL AND NEW.retired_release_id IS DISTINCT FROM OLD.retired_release_id) THEN
        RAISE EXCEPTION 'P3 object identity-bearing fields are immutable';
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_component_closure() RETURNS trigger AS $$
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
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_internal_pair_closure() RETURNS trigger AS $$
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
       OR (x.pair_state='HIERARCHICAL_ONLY' AND pf.relation_type<>'NESTED_TARGET_RELATION'));
    IF bad<>0 THEN RAISE EXCEPTION 'Candidate % pair rows violate member, projection, endpoint, or state/fact compatibility',rid; END IF;
    RETURN COALESCE(NEW,OLD);
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_adjudication_completeness() RETURNS trigger AS $$
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
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_genealogy_cardinality() RETURNS trigger AS $$
DECLARE gid TEXT; g RECORD; pred INTEGER; succ INTEGER; overlap INTEGER;
BEGIN
    gid:=COALESCE(NEW.genealogy_id,OLD.genealogy_id); SELECT * INTO g FROM p3_family_genealogy WHERE genealogy_id=gid;
    IF g.genealogy_id IS NULL THEN RETURN COALESCE(NEW,OLD); END IF;
    SELECT COUNT(*) FILTER(WHERE genealogy_role='PREDECESSOR'),COUNT(*) FILTER(WHERE genealogy_role='SUCCESSOR') INTO pred,succ FROM p3_family_genealogy_member WHERE genealogy_id=gid;
    SELECT COUNT(*) INTO overlap FROM p3_family_genealogy_member p JOIN p3_family_genealogy_member q USING(genealogy_id,family_id) WHERE p.genealogy_id=gid AND p.genealogy_role='PREDECESSOR' AND q.genealogy_role='SUCCESSOR';
    IF overlap<>0 OR (g.relation_type='SPLIT' AND NOT(pred=1 AND succ>=2)) OR (g.relation_type='MERGE' AND NOT(pred>=2 AND succ=1))
       OR (g.relation_type='SUPERSEDE' AND NOT(pred>=1 AND succ>=1)) OR (g.relation_type='DEPRECATE' AND NOT(pred>=1 AND succ=0)) THEN RAISE EXCEPTION 'Genealogy % cardinality invalid',gid; END IF;
    RETURN COALESCE(NEW,OLD);
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_pair_endpoint_resolution() RETURNS trigger AS $$
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
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_segment_membership() RETURNS trigger AS $$
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
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_forbid_update_delete() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'P3 append-only authority table % rejects %', TG_TABLE_NAME, TG_OP;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_candidate_status_event() RETURNS trigger AS $$
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
CREATE TRIGGER p3_object_registry_mutation_guard BEFORE UPDATE OR DELETE ON p3_object_registry FOR EACH ROW EXECUTE FUNCTION p3_guard_object_registry_mutation();
CREATE CONSTRAINT TRIGGER p3_component_header_closure AFTER INSERT OR UPDATE ON p3_candidate_component DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_component_closure();
CREATE CONSTRAINT TRIGGER p3_component_member_closure AFTER INSERT OR UPDATE OR DELETE ON p3_component_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_component_closure();
CREATE CONSTRAINT TRIGGER p3_component_edge_closure AFTER INSERT OR UPDATE OR DELETE ON p3_component_connectivity_edge DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_component_closure();
CREATE CONSTRAINT TRIGGER p3_internal_pair_header_closure AFTER INSERT OR UPDATE OR DELETE ON p3_internal_pair_matrix DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_internal_pair_closure();
CREATE CONSTRAINT TRIGGER p3_internal_pair_member_closure AFTER INSERT OR UPDATE OR DELETE ON p3_candidate_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_internal_pair_closure();
CREATE CONSTRAINT TRIGGER p3_segment_member_subset AFTER INSERT OR UPDATE OR DELETE ON p3_lineage_segment_member DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_segment_membership();
CREATE CONSTRAINT TRIGGER p3_segment_header_nonempty AFTER INSERT OR UPDATE ON p3_lineage_segment DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_segment_membership();
CREATE CONSTRAINT TRIGGER p3_pair_endpoint_header_closure AFTER INSERT OR UPDATE ON p3_pair_endpoint_resolution DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_pair_endpoint_resolution();
CREATE CONSTRAINT TRIGGER p3_pair_endpoint_subject_closure AFTER INSERT OR UPDATE OR DELETE ON p3_pair_endpoint_resolved_subject DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_pair_endpoint_resolution();
CREATE CONSTRAINT TRIGGER p3_internal_pair_collision_closure AFTER INSERT OR UPDATE OR DELETE ON p3_internal_pair_collision DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_internal_pair_closure();
CREATE CONSTRAINT TRIGGER p3_internal_pair_obligation_closure AFTER INSERT OR UPDATE OR DELETE ON p3_internal_pair_closure DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_internal_pair_closure();
CREATE TRIGGER p3_hyperedge_member_type_validate BEFORE INSERT OR UPDATE ON p3_hyperedge_membership FOR EACH ROW EXECUTE FUNCTION p3_validate_hyperedge_member_type();
CREATE CONSTRAINT TRIGGER p3_hyperedge_member_cardinality AFTER INSERT OR UPDATE OR DELETE ON p3_hyperedge_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_hyperedge_cardinality();
CREATE CONSTRAINT TRIGGER p3_hyperedge_cardinality_after_header AFTER INSERT OR UPDATE ON p3_hyperedge DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_hyperedge_cardinality();

CREATE TRIGGER p3_candidate_status_event_validate BEFORE INSERT ON p3_candidate_status_event FOR EACH ROW EXECUTE FUNCTION p3_validate_candidate_status_event();
CREATE TRIGGER p3_release_status_event_validate BEFORE INSERT ON p3_release_status_event FOR EACH ROW EXECUTE FUNCTION p3_validate_release_status_event();
CREATE TRIGGER p3_promotion_pointer_validate BEFORE INSERT OR UPDATE ON p3_runtime_promotion_pointer FOR EACH ROW EXECUTE FUNCTION p3_validate_promotion_pointer();

CREATE CONSTRAINT TRIGGER p3_adjudication_decision_complete AFTER INSERT ON p3_adjudication_decision DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_adjudication_completeness();
CREATE CONSTRAINT TRIGGER p3_adjudication_member_complete AFTER INSERT ON p3_adjudication_member DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_adjudication_completeness();
CREATE CONSTRAINT TRIGGER p3_adjudication_hierarchy_complete AFTER INSERT ON p3_adjudication_hierarchy_relation DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_adjudication_completeness();
CREATE CONSTRAINT TRIGGER p3_adjudication_split_complete AFTER INSERT ON p3_adjudication_split_point DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_adjudication_completeness();
CREATE CONSTRAINT TRIGGER p3_adjudication_unresolved_complete AFTER INSERT ON p3_adjudication_unresolved_boundary DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_adjudication_completeness();
CREATE CONSTRAINT TRIGGER p3_genealogy_header_cardinality AFTER INSERT ON p3_family_genealogy DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_genealogy_cardinality();
CREATE CONSTRAINT TRIGGER p3_genealogy_member_cardinality AFTER INSERT OR UPDATE OR DELETE ON p3_family_genealogy_member DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_genealogy_cardinality();
CREATE TRIGGER p3_adjudication_decision_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_decision FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_member_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_member FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_collision_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_collision_disposition FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_hierarchy_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_hierarchy_relation FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_split_point_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_split_point FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_split_member_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_split_member FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_unresolved_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_unresolved_boundary FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
-- v32 repair: candidate evidence hashes are finalized after the complete
-- packet evidence surface is persisted and recomputed. The blanket v31
-- immutable trigger prevented the required convergence writeback.
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
CREATE VIEW p3_candidate_revision_current_stage AS
SELECT r.candidate_revision_id,r.candidate_family_id,e.to_stage AS lifecycle_stage,e.event_ordinal,e.authority_release_id
FROM p3_candidate_revision r JOIN LATERAL (
  SELECT to_stage,event_ordinal,authority_release_id FROM p3_candidate_status_event e
  WHERE e.candidate_revision_id=r.candidate_revision_id ORDER BY event_ordinal DESC LIMIT 1
) e ON TRUE;

-- P3 excludes response transformation, causal direction, strata assignment, respondent joins, and simulation state.

-- V27 executable-closure validation contracts.
CREATE OR REPLACE FUNCTION p3_validate_pair_projection() RETURNS TRIGGER LANGUAGE plpgsql AS $$
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
CREATE TRIGGER p3_pair_projection_validate BEFORE INSERT OR UPDATE ON p3_pair_projection FOR EACH ROW EXECUTE FUNCTION p3_validate_pair_projection();

CREATE OR REPLACE FUNCTION p3_assert_candidate_origin(p_revision TEXT) RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE v_origin TEXT; v_components INTEGER; v_attachments INTEGER; v_missing INTEGER; v_extra INTEGER;
BEGIN
  SELECT candidate_origin_type INTO v_origin FROM p3_candidate_revision WHERE candidate_revision_id=p_revision;
  IF NOT FOUND THEN RAISE EXCEPTION 'unknown candidate revision %',p_revision; END IF;
  SELECT COUNT(*) INTO v_components FROM p3_candidate_component_link WHERE candidate_revision_id=p_revision;
  SELECT COUNT(*) INTO v_attachments FROM p3_candidate_attachment_projection WHERE candidate_revision_id=p_revision;
  IF v_origin IN ('STRICT_RESPONSE_COMPONENT','PROPOSITION_ONLY_SEED') THEN
    IF v_components<>1 OR v_attachments<>0 THEN RAISE EXCEPTION 'base candidate requires exactly one component and no attachment projection'; END IF;
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

CREATE OR REPLACE FUNCTION p3_assert_adjudication_member_partition(p_adjudication TEXT) RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE v_revision TEXT; v_missing INTEGER; v_extra INTEGER;
BEGIN
  SELECT candidate_revision_id INTO v_revision FROM p3_adjudication_decision WHERE adjudication_id=p_adjudication;
  IF NOT FOUND THEN RAISE EXCEPTION 'unknown adjudication %',p_adjudication; END IF;
  SELECT COUNT(*) INTO v_missing FROM (SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=v_revision AND membership_role='PROPOSED_MEMBER' EXCEPT SELECT member_object_id FROM p3_adjudication_member WHERE adjudication_id=p_adjudication) q;
  SELECT COUNT(*) INTO v_extra FROM (SELECT member_object_id FROM p3_adjudication_member WHERE adjudication_id=p_adjudication EXCEPT SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=v_revision AND membership_role='PROPOSED_MEMBER') q;
  IF v_missing<>0 OR v_extra<>0 THEN RAISE EXCEPTION 'adjudication member partition mismatch: missing %, extra %',v_missing,v_extra; END IF;
END $$;

CREATE OR REPLACE FUNCTION p3_assert_split_result_partition(p_adjudication TEXT) RETURNS VOID LANGUAGE plpgsql AS $$
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

CREATE OR REPLACE FUNCTION p3_assert_canonical_promotion_closure(p_adjudication TEXT) RETURNS VOID LANGUAGE plpgsql AS $$
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

CREATE OR REPLACE FUNCTION p3_validate_candidate_origin_deferred() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE rid TEXT;
BEGIN
  rid:=COALESCE(NEW.candidate_revision_id,OLD.candidate_revision_id);
  IF rid IS NOT NULL AND EXISTS (SELECT 1 FROM p3_candidate_revision WHERE candidate_revision_id=rid) THEN PERFORM p3_assert_candidate_origin(rid); END IF;
  RETURN COALESCE(NEW,OLD);
END $$;
CREATE CONSTRAINT TRIGGER p3_candidate_origin_revision_closure AFTER INSERT ON p3_candidate_revision DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_candidate_origin_deferred();
CREATE CONSTRAINT TRIGGER p3_candidate_origin_component_closure AFTER INSERT OR UPDATE OR DELETE ON p3_candidate_component_link DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_candidate_origin_deferred();
CREATE CONSTRAINT TRIGGER p3_candidate_origin_attachment_closure AFTER INSERT OR UPDATE OR DELETE ON p3_candidate_attachment_projection DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_candidate_origin_deferred();
CREATE CONSTRAINT TRIGGER p3_candidate_origin_member_closure AFTER INSERT OR UPDATE OR DELETE ON p3_candidate_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_candidate_origin_deferred();

CREATE OR REPLACE FUNCTION p3_validate_adjudication_closure_deferred() RETURNS trigger LANGUAGE plpgsql AS $$
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
CREATE CONSTRAINT TRIGGER p3_adjudication_partition_decision_closure AFTER INSERT ON p3_adjudication_decision DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_adjudication_closure_deferred();
CREATE CONSTRAINT TRIGGER p3_adjudication_partition_member_closure AFTER INSERT OR UPDATE OR DELETE ON p3_adjudication_member DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_adjudication_closure_deferred();
CREATE CONSTRAINT TRIGGER p3_adjudication_partition_split_closure AFTER INSERT OR UPDATE OR DELETE ON p3_adjudication_split_result_member DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_adjudication_closure_deferred();
CREATE CONSTRAINT TRIGGER p3_adjudication_partition_canonical_closure AFTER INSERT OR UPDATE OR DELETE ON p3_canonical_family_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_adjudication_closure_deferred();
CREATE CONSTRAINT TRIGGER p3_adjudication_partition_variant_promotion_closure AFTER INSERT OR UPDATE OR DELETE ON p3_variant_promotion DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_adjudication_closure_deferred();
CREATE CONSTRAINT TRIGGER p3_adjudication_partition_exclusion_promotion_closure AFTER INSERT OR UPDATE OR DELETE ON p3_exclusion_promotion DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_adjudication_closure_deferred();

-- The file is a rollback-safe logical installation contract. Every object above is parsed in one transaction.
COMMIT;
