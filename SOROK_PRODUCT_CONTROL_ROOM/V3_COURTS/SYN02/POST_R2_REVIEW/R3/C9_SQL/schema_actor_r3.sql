-- TEST_ONLY SOURCEFREE C9-R3 ACTOR AUTHORITY SCHEMA. PROPOSED, NOT OWNER-FROZEN.
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = FULL;
PRAGMA user_version = 1;
PRAGMA application_id = 1129533491;

CREATE TABLE IF NOT EXISTS actor_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
INSERT OR IGNORE INTO actor_meta VALUES
    ('schema', 'C9_ACTOR_AUTHORITY_R3@1'),
    ('namespace', 'TEST_ONLY_C9_R3'),
    ('owner_state', 'NOT_OWNER_FROZEN'),
    ('legacy_domain', 'C9P_CANDIDATE_TRANSACTION@1');

CREATE TABLE IF NOT EXISTS rule_issuance (
    rule_hash TEXT PRIMARY KEY,
    rule_kind TEXT NOT NULL CHECK (rule_kind IN ('A', 'T')),
    issued_state TEXT NOT NULL CHECK (issued_state IN
        ('ISSUED', 'HELD', 'DENIED', 'INTEGRITY_FAILED')),
    issuer_ref TEXT NOT NULL,
    source_cut_hash TEXT NOT NULL,
    canonical_rule_json TEXT NOT NULL,
    created_admin_us INTEGER NOT NULL,
    CHECK (rule_hash <> ''),
    CHECK (issuer_ref <> ''),
    CHECK (source_cut_hash <> '')
);

CREATE TABLE IF NOT EXISTS actor_branch (
    actor_id TEXT NOT NULL,
    branch_id TEXT NOT NULL,
    branch_epoch TEXT NOT NULL,
    parent_actor_id TEXT,
    parent_branch_id TEXT,
    parent_branch_epoch TEXT,
    fork_base_version_hash TEXT,
    fork_source_cut_hash TEXT,
    fork_c12_branch_id TEXT,
    fork_c12_root_hash TEXT,
    fork_c12_perception_hash TEXT,
    fork_c12_watermark INTEGER,
    source_grant_hash TEXT NOT NULL,
    source_cut_hash TEXT NOT NULL,
    source_root_hash TEXT NOT NULL,
    c12_branch_id TEXT NOT NULL,
    created_admin_us INTEGER NOT NULL,
    PRIMARY KEY (actor_id, branch_id),
    UNIQUE (actor_id, branch_id, branch_epoch),
    UNIQUE (actor_id, branch_epoch),
    UNIQUE (actor_id, c12_branch_id),
    FOREIGN KEY (parent_actor_id, parent_branch_id)
        REFERENCES actor_branch(actor_id, branch_id),
    CHECK (
        (parent_actor_id IS NULL AND parent_branch_id IS NULL
         AND parent_branch_epoch IS NULL)
        OR
        (parent_actor_id IS NOT NULL AND parent_branch_id IS NOT NULL
         AND parent_branch_epoch IS NOT NULL)
    ),
    CHECK (source_grant_hash <> ''),
    CHECK (source_cut_hash <> ''),
    CHECK (source_root_hash <> ''),
    CHECK (c12_branch_id <> ''),
    CHECK (fork_c12_watermark IS NULL OR fork_c12_watermark >= 0)
);

CREATE TABLE IF NOT EXISTS actor_version (
    actor_id TEXT NOT NULL,
    branch_id TEXT NOT NULL,
    branch_epoch TEXT NOT NULL,
    version_no INTEGER NOT NULL CHECK (version_no >= 0),
    version_kind TEXT NOT NULL CHECK (version_kind IN
        ('GENESIS_VALID_EMPTY', 'FORK_INHERITED', 'SEMANTIC_CHANGE',
         'ADMINISTRATIVE_NOCHANGE', 'MIGRATION')),
    version_hash TEXT NOT NULL,
    parent_version_hash TEXT,
    semantic_hash TEXT NOT NULL,
    canonical_state_json TEXT NOT NULL,
    state_grade TEXT NOT NULL CHECK (state_grade IN
        ('VALID_EMPTY', 'VERSIONED_PRESENT', 'MIGRATION_HELD')),
    source_cut_hash TEXT NOT NULL,
    event_effective_us INTEGER,
    decision_receipt_hash TEXT,
    created_admin_us INTEGER NOT NULL,
    PRIMARY KEY (actor_id, branch_id, version_no),
    UNIQUE (actor_id, branch_id, branch_epoch, version_no),
    UNIQUE (actor_id, branch_id, branch_epoch, version_hash),
    FOREIGN KEY (actor_id, branch_id, branch_epoch)
        REFERENCES actor_branch(actor_id, branch_id, branch_epoch),
    FOREIGN KEY (decision_receipt_hash)
        REFERENCES decision_receipt(receipt_hash),
    CHECK (
        (version_kind = 'FORK_INHERITED' AND parent_version_hash IS NOT NULL)
        OR
        (version_kind = 'GENESIS_VALID_EMPTY' AND version_no = 0
         AND parent_version_hash IS NULL)
        OR
        (version_kind IN ('SEMANTIC_CHANGE', 'ADMINISTRATIVE_NOCHANGE')
         AND version_no > 0 AND parent_version_hash IS NOT NULL)
        OR version_kind = 'MIGRATION'
    ),
    CHECK (
        (state_grade = 'VALID_EMPTY' AND canonical_state_json = '{}')
        OR state_grade <> 'VALID_EMPTY'
    ),
    CHECK (source_cut_hash <> '')
);

CREATE TABLE IF NOT EXISTS actor_head (
    actor_id TEXT NOT NULL,
    branch_id TEXT NOT NULL,
    branch_epoch TEXT NOT NULL,
    head_version_no INTEGER NOT NULL,
    head_version_hash TEXT NOT NULL,
    head_semantic_hash TEXT NOT NULL,
    last_receipt_seq INTEGER NOT NULL DEFAULT 0 CHECK (last_receipt_seq >= 0),
    last_finalized_seq INTEGER NOT NULL DEFAULT 0 CHECK (last_finalized_seq >= 0),
    updated_admin_us INTEGER NOT NULL,
    PRIMARY KEY (actor_id, branch_id),
    FOREIGN KEY (actor_id, branch_id, branch_epoch)
        REFERENCES actor_branch(actor_id, branch_id, branch_epoch),
    FOREIGN KEY (actor_id, branch_id, branch_epoch, head_version_no)
        REFERENCES actor_version(actor_id, branch_id, branch_epoch, version_no),
    CHECK (last_finalized_seq <= last_receipt_seq)
);

CREATE TABLE IF NOT EXISTS actor_target (
    actor_id TEXT NOT NULL,
    branch_id TEXT NOT NULL,
    branch_epoch TEXT NOT NULL,
    target_id TEXT NOT NULL,
    target_hash TEXT NOT NULL,
    record_json TEXT NOT NULL,
    source_receipt_hash TEXT,
    created_receipt_hash TEXT NOT NULL,
    created_admin_us INTEGER NOT NULL,
    PRIMARY KEY (actor_id, branch_id, branch_epoch, target_id),
    UNIQUE (actor_id, branch_id, branch_epoch, target_hash),
    FOREIGN KEY (actor_id, branch_id, branch_epoch)
        REFERENCES actor_branch(actor_id, branch_id, branch_epoch),
    FOREIGN KEY (created_receipt_hash) REFERENCES decision_receipt(receipt_hash)
);

CREATE TABLE IF NOT EXISTS world_receipt (
    world_receipt_hash TEXT PRIMARY KEY,
    world_event_id TEXT NOT NULL,
    c8_branch_id TEXT NOT NULL,
    c8_root_hash TEXT NOT NULL,
    c8_head_hash TEXT NOT NULL,
    world_parent_hash TEXT,
    effective_us INTEGER NOT NULL,
    source_owner TEXT NOT NULL,
    source_grade TEXT NOT NULL,
    source_cut_hash TEXT NOT NULL,
    payload_digest TEXT NOT NULL,
    canonical_receipt_json TEXT NOT NULL,
    verified_admin_us INTEGER NOT NULL,
    UNIQUE (c8_branch_id, world_event_id, c8_root_hash)
);

CREATE TABLE IF NOT EXISTS legacy_bridge (
    legacy_receipt_hash TEXT PRIMARY KEY,
    legacy_db_id TEXT NOT NULL,
    legacy_event_hash TEXT NOT NULL,
    legacy_response_ref TEXT NOT NULL,
    legacy_target_branch TEXT NOT NULL,
    legacy_target_reason TEXT NOT NULL,
    legacy_before_hash TEXT NOT NULL,
    legacy_after_hash TEXT NOT NULL,
    legacy_domain_hash TEXT NOT NULL,
    legacy_receipt_json TEXT NOT NULL,
    verified_admin_us INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS decision_receipt (
    receipt_hash TEXT PRIMARY KEY,
    decision_kind TEXT NOT NULL CHECK (decision_kind IN
        ('COMMITTED_CHANGE', 'TRUE_NO_CHANGE_EVALUATED', 'HELD_MISSING_RULE',
         'HELD_MISSING_SOURCE', 'SOURCE_DENIED', 'DEFERRED',
         'NOT_APPLICABLE_BY_ISSUED_RULE', 'INTEGRITY_FAILED')),
    actor_id TEXT NOT NULL,
    branch_id TEXT NOT NULL,
    branch_epoch TEXT NOT NULL,
    commit_seq INTEGER NOT NULL CHECK (commit_seq > 0),
    prior_receipt_hash TEXT,
    event_key TEXT NOT NULL,
    attempt_no INTEGER NOT NULL CHECK (attempt_no > 0),
    source_scope_hash TEXT NOT NULL,
    settled_scope_hash TEXT NOT NULL,
    source_root_hash TEXT NOT NULL,
    source_cut_hash TEXT NOT NULL,
    legacy_receipt_hash TEXT,
    legacy_event_hash TEXT,
    legacy_after_hash TEXT,
    legacy_domain_hash TEXT,
    world_receipt_hash TEXT,
    world_event_id TEXT,
    source_status TEXT NOT NULL CHECK (source_status IN
        ('QUALIFIED', 'SOURCE_HELD', 'SOURCE_DENIED', 'INTEGRITY_FAILED', 'UNKNOWN')),
    world_occurrence TEXT NOT NULL CHECK (world_occurrence IN
        ('PROPOSED_ONLY', 'OCCURRED', 'NOT_REALIZED', 'NO_EVENT',
         'NOT_YET_OBSERVED', 'OCCURRENCE_UNKNOWN')),
    actor_presence TEXT NOT NULL CHECK (actor_presence IN
        ('CO_PRESENT', 'NOT_PRESENT', 'UNKNOWN', 'NOT_APPLICABLE')),
    actor_reception TEXT NOT NULL CHECK (actor_reception IN
        ('RECEIVED', 'PARTIAL', 'NOT_WITNESSED', 'TESTIMONY',
         'UNKNOWN', 'NOT_APPLICABLE')),
    proposal_state TEXT NOT NULL CHECK (proposal_state IN
        ('PROPOSAL_PRESENT', 'NO_PROPOSAL', 'NO_EVENT', 'UNKNOWN')),
    evaluation_basis TEXT NOT NULL CHECK (evaluation_basis IN
        ('ISSUED_RULE_T_EVALUATED', 'NO_PROPOSAL_HELD', 'NO_EVENT_HELD',
         'RULE_MISSING_HELD', 'SOURCE_HELD', 'SOURCE_DENIED',
         'SCIENTIFIC_HOLD', 'NOT_APPLICABLE_BY_ISSUED_RULE',
         'INTEGRITY_FAILED')),
    rule_a_status TEXT NOT NULL CHECK (rule_a_status IN
        ('APPLIED_WITH_RESPONSE', 'APPLIED_VALID_EMPTY', 'HELD_MISSING_RULE',
         'HELD_SOURCE', 'NOT_APPLICABLE_BY_ISSUED_RULE', 'INTEGRITY_FAILED')),
    rule_t_status TEXT NOT NULL CHECK (rule_t_status IN
        ('COMMITTED_CHANGE', 'TRUE_NO_CHANGE_EVALUATED', 'HELD_MISSING_RULE',
         'HELD_MISSING_SOURCE', 'DEFERRED', 'NOT_APPLICABLE_BY_ISSUED_RULE',
         'INTEGRITY_FAILED')),
    actor_state_status TEXT NOT NULL CHECK (actor_state_status IN
        ('VALID_EMPTY', 'VERSIONED_PRESENT', 'UNAVAILABLE_PENDING_RECONCILIATION',
         'MIGRATION_HELD')),
    memory_evidence TEXT NOT NULL CHECK (memory_evidence IN
        ('ACTOR_ACCESSIBLE', 'PARTIAL_TRACE', 'BELIEF_WITH_SOURCE',
         'ACTOR_UNKNOWN', 'ANALYST_ONLY', 'NOT_APPLICABLE')),
    sci05_status TEXT NOT NULL CHECK (sci05_status IN
        ('ADMITTED', 'DENIED', 'HELD', 'INTEGRITY_FAILED', 'NOT_APPLICABLE')),
    sci05_certificate_hash TEXT,
    before_version_hash TEXT NOT NULL,
    result_version_hash TEXT,
    before_semantic_hash TEXT NOT NULL,
    after_semantic_hash TEXT,
    rule_a_hash TEXT,
    rule_t_hash TEXT,
    evaluated_readset_hash TEXT,
    permission_hash TEXT,
    exact_reason TEXT NOT NULL,
    canonical_receipt_json TEXT NOT NULL,
    effective_us INTEGER,
    admin_committed_us INTEGER NOT NULL,
    UNIQUE (actor_id, branch_id, branch_epoch, commit_seq),
    FOREIGN KEY (actor_id, branch_id, branch_epoch)
        REFERENCES actor_branch(actor_id, branch_id, branch_epoch),
    FOREIGN KEY (legacy_receipt_hash) REFERENCES legacy_bridge(legacy_receipt_hash),
    FOREIGN KEY (world_receipt_hash) REFERENCES world_receipt(world_receipt_hash),
    FOREIGN KEY (rule_a_hash) REFERENCES rule_issuance(rule_hash),
    FOREIGN KEY (rule_t_hash) REFERENCES rule_issuance(rule_hash),
    CHECK (source_root_hash <> ''),
    CHECK (source_cut_hash <> ''),
    CHECK (world_occurrence <> 'OCCURRED' OR world_receipt_hash IS NOT NULL),
    CHECK (
        (decision_kind IN ('COMMITTED_CHANGE', 'TRUE_NO_CHANGE_EVALUATED')
         AND result_version_hash IS NOT NULL
         AND after_semantic_hash IS NOT NULL
         AND rule_t_hash IS NOT NULL
         AND evaluated_readset_hash IS NOT NULL
         AND evaluation_basis = 'ISSUED_RULE_T_EVALUATED'
         AND source_status = 'QUALIFIED'
         AND world_occurrence = 'OCCURRED'
         AND actor_presence = 'CO_PRESENT'
         AND actor_reception IN ('RECEIVED', 'PARTIAL')
         AND sci05_status IN ('ADMITTED', 'NOT_APPLICABLE'))
        OR
        (decision_kind NOT IN ('COMMITTED_CHANGE', 'TRUE_NO_CHANGE_EVALUATED')
         AND result_version_hash IS NULL
         AND after_semantic_hash IS NULL
         AND rule_t_hash IS NULL
         AND evaluated_readset_hash IS NULL)
    ),
    CHECK (
        decision_kind IN ('COMMITTED_CHANGE', 'TRUE_NO_CHANGE_EVALUATED')
        OR rule_t_status NOT IN ('COMMITTED_CHANGE', 'TRUE_NO_CHANGE_EVALUATED')
    ),
    CHECK (
        (decision_kind = 'TRUE_NO_CHANGE_EVALUATED'
         AND after_semantic_hash = before_semantic_hash
         AND rule_t_status = 'TRUE_NO_CHANGE_EVALUATED')
        OR decision_kind <> 'TRUE_NO_CHANGE_EVALUATED'
    ),
    CHECK (
        (decision_kind = 'COMMITTED_CHANGE'
         AND after_semantic_hash <> before_semantic_hash
         AND rule_t_status = 'COMMITTED_CHANGE')
        OR decision_kind <> 'COMMITTED_CHANGE'
    ),
    CHECK (
        (decision_kind = 'HELD_MISSING_RULE'
         AND rule_t_status = 'HELD_MISSING_RULE'
         AND evaluation_basis IN ('NO_PROPOSAL_HELD', 'NO_EVENT_HELD',
                                  'RULE_MISSING_HELD'))
        OR decision_kind <> 'HELD_MISSING_RULE'
    ),
    CHECK (
        (proposal_state = 'NO_PROPOSAL' AND evaluation_basis = 'NO_PROPOSAL_HELD')
        OR proposal_state <> 'NO_PROPOSAL'
    ),
    CHECK (
        (proposal_state = 'NO_EVENT' AND evaluation_basis = 'NO_EVENT_HELD')
        OR proposal_state <> 'NO_EVENT'
    ),
    CHECK (
        (sci05_status IN ('DENIED', 'HELD', 'INTEGRITY_FAILED')
         AND sci05_certificate_hash IS NULL)
        OR sci05_status IN ('ADMITTED', 'NOT_APPLICABLE')
    )
);

CREATE TABLE IF NOT EXISTS event_attempt (
    attempt_id TEXT PRIMARY KEY,
    event_key TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    branch_id TEXT NOT NULL,
    branch_epoch TEXT NOT NULL,
    attempt_no INTEGER NOT NULL CHECK (attempt_no > 0),
    idempotency_key TEXT NOT NULL,
    request_digest TEXT NOT NULL,
    source_root_hash TEXT NOT NULL,
    source_cut_hash TEXT NOT NULL,
    source_scope_hash TEXT NOT NULL,
    settled_scope_hash TEXT NOT NULL,
    prior_attempt_id TEXT,
    receipt_hash TEXT NOT NULL,
    attempt_state TEXT NOT NULL CHECK (attempt_state IN
        ('HELD', 'FINALIZED', 'SUPERSEDED')),
    supersedes_receipt_hash TEXT,
    supersession_grant_hash TEXT,
    canonical_attempt_json TEXT NOT NULL,
    created_admin_us INTEGER NOT NULL,
    UNIQUE (actor_id, branch_id, branch_epoch, event_key, attempt_no),
    UNIQUE (idempotency_key),
    FOREIGN KEY (actor_id, branch_id, branch_epoch)
        REFERENCES actor_branch(actor_id, branch_id, branch_epoch),
    FOREIGN KEY (receipt_hash) REFERENCES decision_receipt(receipt_hash),
    FOREIGN KEY (prior_attempt_id) REFERENCES event_attempt(attempt_id),
    CHECK (
        attempt_state <> 'FINALIZED'
        OR prior_attempt_id IS NOT NULL
        OR supersedes_receipt_hash IS NULL
    ),
    CHECK (
        (prior_attempt_id IS NULL AND supersession_grant_hash IS NULL)
        OR
        (prior_attempt_id IS NOT NULL AND supersession_grant_hash IS NOT NULL
         AND supersession_grant_hash <> '')
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_final_event_once
    ON event_attempt(actor_id, branch_id, branch_epoch, event_key)
    WHERE attempt_state = 'FINALIZED';

CREATE TABLE IF NOT EXISTS requalification_grant (
    grant_hash TEXT PRIMARY KEY,
    actor_id TEXT NOT NULL,
    branch_id TEXT NOT NULL,
    branch_epoch TEXT NOT NULL,
    event_key TEXT NOT NULL,
    prior_attempt_id TEXT NOT NULL,
    prior_receipt_hash TEXT NOT NULL,
    issuance_kind TEXT NOT NULL CHECK (issuance_kind IN
        ('RULE_A', 'RULE_T', 'SOURCE')),
    issuance_ref TEXT NOT NULL,
    issued_state TEXT NOT NULL CHECK (issued_state IN
        ('ISSUED', 'HELD', 'DENIED')),
    source_cut_hash TEXT NOT NULL,
    canonical_grant_json TEXT NOT NULL,
    created_admin_us INTEGER NOT NULL,
    UNIQUE (prior_attempt_id),
    FOREIGN KEY (actor_id, branch_id, branch_epoch)
        REFERENCES actor_branch(actor_id, branch_id, branch_epoch),
    FOREIGN KEY (prior_attempt_id) REFERENCES event_attempt(attempt_id),
    CHECK (grant_hash <> ''),
    CHECK (issuance_ref <> ''),
    CHECK (source_cut_hash <> '')
);

CREATE TABLE IF NOT EXISTS projection_outbox (
    receipt_hash TEXT PRIMARY KEY,
    actor_id TEXT NOT NULL,
    branch_id TEXT NOT NULL,
    branch_epoch TEXT NOT NULL,
    commit_seq INTEGER NOT NULL,
    actor_result_hash TEXT,
    world_receipt_hash TEXT,
    payload_digest TEXT NOT NULL,
    envelope_json TEXT NOT NULL,
    projection_state TEXT NOT NULL CHECK (projection_state IN
        ('PENDING', 'PROJECTED', 'ACKED')),
    projected_c12_hash TEXT,
    acked_admin_us INTEGER,
    attempt_count INTEGER NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
    last_error_code TEXT,
    FOREIGN KEY (receipt_hash) REFERENCES decision_receipt(receipt_hash),
    UNIQUE (actor_id, branch_id, branch_epoch, commit_seq),
    CHECK (
        projection_state <> 'ACKED'
        OR (projected_c12_hash IS NOT NULL AND acked_admin_us IS NOT NULL)
    )
);

CREATE TABLE IF NOT EXISTS reconciliation_fault (
    fault_id TEXT PRIMARY KEY,
    actor_id TEXT NOT NULL,
    branch_id TEXT NOT NULL,
    branch_epoch TEXT NOT NULL,
    c12_branch_id TEXT,
    world_receipt_hash TEXT,
    receipt_hash TEXT,
    fault_code TEXT NOT NULL,
    source_snapshot_hash TEXT,
    observed_digest TEXT,
    fault_state TEXT NOT NULL CHECK (fault_state IN
        ('OPEN', 'RECONCILED', 'INTEGRITY_HELD')),
    evidence_json TEXT NOT NULL,
    created_admin_us INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS migration_receipt (
    old_archive_blob_hash TEXT NOT NULL,
    old_field_path TEXT NOT NULL,
    mapping_kind TEXT NOT NULL CHECK (mapping_kind IN
        ('SOURCE_VERIFIED', 'CARRIER_ONLY', 'DERIVED_VIEW_ONLY',
         'UNSAFE_HISTORICAL', 'UNKNOWN', 'SOURCE_HELD')),
    owner_decision_hash TEXT,
    new_actor_ref TEXT,
    reason TEXT NOT NULL,
    PRIMARY KEY (old_archive_blob_hash, old_field_path)
);

CREATE TRIGGER IF NOT EXISTS decision_final_requires_issued_rule
BEFORE INSERT ON decision_receipt
WHEN NEW.decision_kind IN ('COMMITTED_CHANGE', 'TRUE_NO_CHANGE_EVALUATED')
  AND NOT EXISTS (
      SELECT 1 FROM rule_issuance
      WHERE rule_hash = NEW.rule_t_hash
        AND rule_kind = 'T'
        AND issued_state = 'ISSUED'
  )
BEGIN SELECT RAISE(ABORT, 'ISSUED_RULE_T_REQUIRED'); END;

CREATE TRIGGER IF NOT EXISTS rule_issuance_no_update
BEFORE UPDATE ON rule_issuance
BEGIN SELECT RAISE(ABORT, 'RULE_ISSUANCE_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS rule_issuance_no_delete
BEFORE DELETE ON rule_issuance
BEGIN SELECT RAISE(ABORT, 'RULE_ISSUANCE_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS actor_version_no_update
BEFORE UPDATE ON actor_version
BEGIN SELECT RAISE(ABORT, 'ACTOR_VERSION_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS actor_version_no_delete
BEFORE DELETE ON actor_version
BEGIN SELECT RAISE(ABORT, 'ACTOR_VERSION_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS decision_receipt_no_update
BEFORE UPDATE ON decision_receipt
BEGIN SELECT RAISE(ABORT, 'DECISION_RECEIPT_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS decision_receipt_no_delete
BEFORE DELETE ON decision_receipt
BEGIN SELECT RAISE(ABORT, 'DECISION_RECEIPT_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS event_attempt_no_update
BEFORE UPDATE ON event_attempt
BEGIN SELECT RAISE(ABORT, 'EVENT_ATTEMPT_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS event_attempt_no_delete
BEFORE DELETE ON event_attempt
BEGIN SELECT RAISE(ABORT, 'EVENT_ATTEMPT_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS world_receipt_no_update
BEFORE UPDATE ON world_receipt
BEGIN SELECT RAISE(ABORT, 'WORLD_RECEIPT_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS world_receipt_no_delete
BEFORE DELETE ON world_receipt
BEGIN SELECT RAISE(ABORT, 'WORLD_RECEIPT_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS legacy_bridge_no_update
BEFORE UPDATE ON legacy_bridge
BEGIN SELECT RAISE(ABORT, 'LEGACY_BRIDGE_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS legacy_bridge_no_delete
BEFORE DELETE ON legacy_bridge
BEGIN SELECT RAISE(ABORT, 'LEGACY_BRIDGE_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS actor_branch_no_update
BEFORE UPDATE ON actor_branch
BEGIN SELECT RAISE(ABORT, 'ACTOR_BRANCH_IMMUTABLE'); END;
CREATE TRIGGER IF NOT EXISTS actor_branch_no_delete
BEFORE DELETE ON actor_branch
BEGIN SELECT RAISE(ABORT, 'ACTOR_BRANCH_IMMUTABLE'); END;
CREATE TRIGGER IF NOT EXISTS actor_target_no_update
BEFORE UPDATE ON actor_target
BEGIN SELECT RAISE(ABORT, 'ACTOR_TARGET_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS actor_target_no_delete
BEFORE DELETE ON actor_target
BEGIN SELECT RAISE(ABORT, 'ACTOR_TARGET_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS requalification_grant_no_update
BEFORE UPDATE ON requalification_grant
BEGIN SELECT RAISE(ABORT, 'REQUALIFICATION_GRANT_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS requalification_grant_no_delete
BEFORE DELETE ON requalification_grant
BEGIN SELECT RAISE(ABORT, 'REQUALIFICATION_GRANT_APPEND_ONLY'); END;

CREATE TRIGGER IF NOT EXISTS actor_head_monotone
BEFORE UPDATE ON actor_head
WHEN OLD.actor_id <> NEW.actor_id
  OR OLD.branch_id <> NEW.branch_id
  OR OLD.branch_epoch <> NEW.branch_epoch
  OR NEW.head_version_no < OLD.head_version_no
  OR NEW.last_receipt_seq < OLD.last_receipt_seq
  OR NEW.last_finalized_seq < OLD.last_finalized_seq
BEGIN SELECT RAISE(ABORT, 'ACTOR_HEAD_MONOTONICITY'); END;

CREATE TRIGGER IF NOT EXISTS outbox_transition
BEFORE UPDATE ON projection_outbox
WHEN OLD.receipt_hash <> NEW.receipt_hash
  OR OLD.actor_id <> NEW.actor_id
  OR OLD.branch_id <> NEW.branch_id
  OR OLD.branch_epoch <> NEW.branch_epoch
  OR OLD.commit_seq <> NEW.commit_seq
  OR (OLD.projection_state = 'ACKED' AND NEW.projection_state <> 'ACKED')
  OR (OLD.projection_state = 'PROJECTED' AND NEW.projection_state = 'PENDING')
  OR (NEW.projection_state = 'ACKED' AND OLD.projection_state NOT IN
      ('PROJECTED', 'ACKED'))
BEGIN SELECT RAISE(ABORT, 'OUTBOX_STATE_TRANSITION_REFUSED'); END;
