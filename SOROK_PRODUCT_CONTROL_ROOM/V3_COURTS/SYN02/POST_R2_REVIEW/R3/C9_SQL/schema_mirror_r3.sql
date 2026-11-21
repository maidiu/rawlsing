-- TEST_ONLY SOURCEFREE C12 ACTOR MIRROR SCHEMA. PROPOSED, NOT OWNER-FROZEN.
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = FULL;
PRAGMA user_version = 1;
PRAGMA application_id = 1129533492;

CREATE TABLE IF NOT EXISTS mirror_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
INSERT OR IGNORE INTO mirror_meta VALUES
    ('schema', 'C12_ACTOR_MIRROR_R3@1'),
    ('namespace', 'TEST_ONLY_C9_R3'),
    ('owner_state', 'NOT_OWNER_FROZEN'),
    ('c12_source_domain', 'BP4_C12_STORE@1');

CREATE TABLE IF NOT EXISTS mirror_branch (
    c12_branch_id TEXT PRIMARY KEY,
    actor_id TEXT NOT NULL,
    actor_branch_epoch TEXT NOT NULL,
    c12_parent_branch_id TEXT,
    c12_root_hash TEXT NOT NULL,
    c12_fork_clock INTEGER,
    c12_created_clock INTEGER NOT NULL,
    c9_start_seq INTEGER NOT NULL CHECK (c9_start_seq >= 0),
    c9_start_receipt_hash TEXT,
    base_c12_branch_id TEXT,
    base_c12_root_hash TEXT,
    base_c12_perception_hash TEXT,
    base_c12_perception_count INTEGER NOT NULL DEFAULT 0
        CHECK (base_c12_perception_count >= 0),
    mirror_state TEXT NOT NULL CHECK (mirror_state IN
        ('ROOT_READY', 'FORK_READY', 'FORK_HELD', 'MIRROR_HELD')),
    created_admin_us INTEGER NOT NULL,
    UNIQUE (actor_id, actor_branch_epoch),
    CHECK (c12_branch_id <> ''),
    CHECK (
        (base_c12_branch_id IS NULL AND base_c12_root_hash IS NULL
         AND base_c12_perception_hash IS NULL
         AND base_c12_perception_count = 0
         AND c9_start_seq = 0 AND c9_start_receipt_hash IS NULL)
        OR
        (base_c12_branch_id IS NOT NULL AND base_c12_root_hash IS NOT NULL
         AND base_c12_perception_hash IS NOT NULL
         AND base_c12_perception_hash <> ''
         AND base_c12_perception_count >= 0 AND c9_start_seq >= 0)
    ),
    CHECK (mirror_state NOT IN ('FORK_READY', 'FORK_HELD')
           OR base_c12_branch_id IS NOT NULL),
    CHECK (c9_start_seq = 0 OR c9_start_receipt_hash IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS mirror_receipt (
    c12_branch_id TEXT NOT NULL,
    c9_seq INTEGER NOT NULL CHECK (c9_seq > 0),
    c9_receipt_hash TEXT NOT NULL,
    c9_actor_version_hash TEXT,
    c9_decision_kind TEXT NOT NULL,
    c9_semantic_hash TEXT,
    projection_hash TEXT NOT NULL,
    canonical_projection_json TEXT NOT NULL,
    c12_root_hash TEXT NOT NULL,
    c12_last_clock INTEGER NOT NULL CHECK (c12_last_clock >= 0),
    c8_world_receipt_hash TEXT,
    created_admin_us INTEGER NOT NULL,
    PRIMARY KEY (c12_branch_id, c9_seq),
    UNIQUE (c12_branch_id, c9_receipt_hash),
    FOREIGN KEY (c12_branch_id) REFERENCES mirror_branch(c12_branch_id)
);

CREATE TABLE IF NOT EXISTS mirror_watermark (
    c12_branch_id TEXT PRIMARY KEY,
    last_seq INTEGER NOT NULL CHECK (last_seq >= 0),
    last_receipt_hash TEXT,
    last_projection_hash TEXT,
    watermark_state TEXT NOT NULL CHECK (watermark_state IN
        ('CLEAN', 'SYNC_HELD', 'MIRROR_CONFLICT', 'FORK_HELD')),
    updated_admin_us INTEGER NOT NULL,
    FOREIGN KEY (c12_branch_id) REFERENCES mirror_branch(c12_branch_id),
    CHECK (
        (last_seq = 0 AND last_receipt_hash IS NULL
         AND last_projection_hash IS NULL)
        OR
        (last_seq > 0 AND last_receipt_hash IS NOT NULL
         AND last_projection_hash IS NOT NULL)
    )
);

CREATE TABLE IF NOT EXISTS mirror_fault (
    fault_id TEXT PRIMARY KEY,
    c12_branch_id TEXT,
    c9_seq INTEGER,
    fault_code TEXT NOT NULL,
    fault_state TEXT NOT NULL CHECK (fault_state IN
        ('OPEN', 'RECONCILED', 'INTEGRITY_HELD')),
    observed_digest TEXT,
    evidence_json TEXT NOT NULL,
    created_admin_us INTEGER NOT NULL
);

CREATE TRIGGER IF NOT EXISTS mirror_receipt_no_update
BEFORE UPDATE ON mirror_receipt
BEGIN SELECT RAISE(ABORT, 'MIRROR_RECEIPT_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS mirror_receipt_no_delete
BEFORE DELETE ON mirror_receipt
BEGIN SELECT RAISE(ABORT, 'MIRROR_RECEIPT_APPEND_ONLY'); END;
CREATE TRIGGER IF NOT EXISTS mirror_branch_no_update
BEFORE UPDATE ON mirror_branch
BEGIN SELECT RAISE(ABORT, 'MIRROR_BRANCH_IMMUTABLE'); END;
CREATE TRIGGER IF NOT EXISTS mirror_branch_no_delete
BEFORE DELETE ON mirror_branch
BEGIN SELECT RAISE(ABORT, 'MIRROR_BRANCH_IMMUTABLE'); END;
CREATE TRIGGER IF NOT EXISTS mirror_watermark_monotone
BEFORE UPDATE ON mirror_watermark
WHEN OLD.c12_branch_id <> NEW.c12_branch_id
  OR NEW.last_seq < OLD.last_seq
BEGIN SELECT RAISE(ABORT, 'MIRROR_WATERMARK_REGRESSION'); END;
CREATE TRIGGER IF NOT EXISTS mirror_watermark_exact
BEFORE UPDATE ON mirror_watermark
WHEN NEW.last_seq > 0
  AND NOT EXISTS (
      SELECT 1 FROM mirror_receipt
      WHERE c12_branch_id = NEW.c12_branch_id
        AND c9_seq = NEW.last_seq
        AND c9_receipt_hash = NEW.last_receipt_hash
        AND projection_hash = NEW.last_projection_hash
  )
BEGIN SELECT RAISE(ABORT, 'MIRROR_WATERMARK_WITHOUT_RECEIPT'); END;
CREATE TRIGGER IF NOT EXISTS mirror_watermark_insert_exact
BEFORE INSERT ON mirror_watermark
WHEN NEW.last_seq > 0
  AND NOT EXISTS (
      SELECT 1 FROM mirror_receipt
      WHERE c12_branch_id = NEW.c12_branch_id
        AND c9_seq = NEW.last_seq
        AND c9_receipt_hash = NEW.last_receipt_hash
        AND projection_hash = NEW.last_projection_hash
  )
  AND NOT EXISTS (
      SELECT 1 FROM mirror_branch
      WHERE c12_branch_id = NEW.c12_branch_id
        AND base_c12_branch_id IS NOT NULL
        AND c9_start_seq = NEW.last_seq
  )
BEGIN SELECT RAISE(ABORT, 'MIRROR_WATERMARK_WITHOUT_RECEIPT'); END;
