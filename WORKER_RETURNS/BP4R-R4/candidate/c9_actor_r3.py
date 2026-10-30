"""TEST_ONLY sourcefree C9-R3 actor and C12 mirror proof helper.

This module is a bounded SQLite test implementation, not a production C9/C12
implementation and not an owner-frozen storage contract. It exercises exact
idempotent replay, typed payload conflicts, held/final status orthogonality,
requalification, actor CAS, separate world/mirror/ACK states, cold reopen, fork
inheritance, and the actual C12 perception-only suffix defect.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "schema_actor_r3.sql"
MIRROR_SCHEMA = HERE / "schema_mirror_r3.sql"
NOW = 1_780_000_000_000_000
REQUEST_SCHEMA = "C9_R3_REQUEST@1"
RECEIPT_SCHEMA = "C9_R3_DECISION_RECEIPT@1"
SUPPORTED_C12_WRITER_SCHEMAS = frozenset({"BP4_C12_STORE@1"})

FINAL_KINDS = {"COMMITTED_CHANGE", "TRUE_NO_CHANGE_EVALUATED"}
DECISIONS = {
    "COMMITTED_CHANGE",
    "TRUE_NO_CHANGE_EVALUATED",
    "HELD_MISSING_RULE",
    "HELD_MISSING_SOURCE",
    "SOURCE_DENIED",
    "DEFERRED",
    "NOT_APPLICABLE_BY_ISSUED_RULE",
    "INTEGRITY_FAILED",
}
RULE_T_STATUSES = {
    "COMMITTED_CHANGE",
    "TRUE_NO_CHANGE_EVALUATED",
    "HELD_MISSING_RULE",
    "HELD_MISSING_SOURCE",
    "DEFERRED",
    "NOT_APPLICABLE_BY_ISSUED_RULE",
    "INTEGRITY_FAILED",
}
HELD_RULE_T = {
    "HELD_MISSING_RULE": {"HELD_MISSING_RULE"},
    "HELD_MISSING_SOURCE": {"HELD_MISSING_SOURCE"},
    "SOURCE_DENIED": {"HELD_MISSING_SOURCE", "INTEGRITY_FAILED"},
    "DEFERRED": {"DEFERRED"},
    "NOT_APPLICABLE_BY_ISSUED_RULE": {"NOT_APPLICABLE_BY_ISSUED_RULE"},
    "INTEGRITY_FAILED": {"INTEGRITY_FAILED"},
}
HELD_BASIS = {
    "HELD_MISSING_RULE": {
        "NO_PROPOSAL_HELD",
        "NO_EVENT_HELD",
        "RULE_MISSING_HELD",
    },
    "HELD_MISSING_SOURCE": {"SOURCE_HELD"},
    "SOURCE_DENIED": {"SOURCE_DENIED"},
    "DEFERRED": {"SCIENTIFIC_HOLD"},
    "NOT_APPLICABLE_BY_ISSUED_RULE": {"NOT_APPLICABLE_BY_ISSUED_RULE"},
    "INTEGRITY_FAILED": {"INTEGRITY_FAILED"},
}
EVALUATION_BASES = {
    "ISSUED_RULE_T_EVALUATED",
    "NO_PROPOSAL_HELD",
    "NO_EVENT_HELD",
    "RULE_MISSING_HELD",
    "SOURCE_HELD",
    "SOURCE_DENIED",
    "SCIENTIFIC_HOLD",
    "NOT_APPLICABLE_BY_ISSUED_RULE",
    "INTEGRITY_FAILED",
}
WORLD_OCCURRENCES = {
    "PROPOSED_ONLY",
    "OCCURRED",
    "NOT_REALIZED",
    "NO_EVENT",
    "NOT_YET_OBSERVED",
    "OCCURRENCE_UNKNOWN",
}
SOURCE_STATUSES = {
    "QUALIFIED",
    "SOURCE_HELD",
    "SOURCE_DENIED",
    "INTEGRITY_FAILED",
    "UNKNOWN",
}
ACTOR_PRESENCES = {"CO_PRESENT", "NOT_PRESENT", "UNKNOWN", "NOT_APPLICABLE"}
ACTOR_RECEPTIONS = {
    "RECEIVED",
    "PARTIAL",
    "NOT_WITNESSED",
    "TESTIMONY",
    "UNKNOWN",
    "NOT_APPLICABLE",
}
RULE_A_STATUSES = {
    "APPLIED_WITH_RESPONSE",
    "APPLIED_VALID_EMPTY",
    "HELD_MISSING_RULE",
    "HELD_SOURCE",
    "NOT_APPLICABLE_BY_ISSUED_RULE",
    "INTEGRITY_FAILED",
}
ACTOR_STATES = {
    "VALID_EMPTY",
    "VERSIONED_PRESENT",
    "UNAVAILABLE_PENDING_RECONCILIATION",
    "MIGRATION_HELD",
}
MEMORY_EVIDENCE = {
    "ACTOR_ACCESSIBLE",
    "PARTIAL_TRACE",
    "BELIEF_WITH_SOURCE",
    "ACTOR_UNKNOWN",
    "ANALYST_ONLY",
    "NOT_APPLICABLE",
}
SCI05_STATUSES = {"ADMITTED", "DENIED", "HELD", "INTEGRITY_FAILED", "NOT_APPLICABLE"}
PROPOSAL_STATES = {"PROPOSAL_PRESENT", "NO_PROPOSAL", "NO_EVENT", "UNKNOWN"}


class Refusal(RuntimeError):
    """Typed sourcefree refusal with a stable code."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


class IdempotencyConflict(Refusal):
    """The idempotency key exists with a different request digest or scope."""


def canon(value: Any) -> str:
    """Return compact sorted JSON used by every identity in this proof."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha(value: Any) -> str:
    """Return SHA-256 over canonical JSON."""
    return hashlib.sha256(canon(value).encode("utf8")).hexdigest()


def sha_file(path: str | Path) -> str:
    """Return the SHA-256 of exact file bytes."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _refuse(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise Refusal(code, detail)


def _connect(path: str | Path, schema: Path) -> sqlite3.Connection:
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), isolation_level=None, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(schema.read_text(encoding="utf8"))
    return conn


def _insert(conn: sqlite3.Connection, table: str, values: Mapping[str, Any]) -> None:
    columns = list(values)
    placeholders = ",".join("?" for _ in columns)
    conn.execute(
        f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})",
        tuple(values[column] for column in columns),
    )


def _clone_row(conn: sqlite3.Connection, table: str, row: Mapping[str, Any]) -> None:
    _insert(conn, table, row)


@dataclass(frozen=True)
class PublishRequest:
    """One test-only actor publication request."""

    event_key: str
    idempotency_key: str
    decision_kind: str
    source_cut_hash: str
    source_scope_hash: str
    settled_scope_hash: str
    attempt_no: int = 0
    source_root_hash: str = "TEST_ONLY_SOURCE_ROOT"
    source_status: str = "QUALIFIED"
    world_occurrence: str = "OCCURRED"
    actor_presence: str = "CO_PRESENT"
    actor_reception: str = "RECEIVED"
    proposal_state: str = "PROPOSAL_PRESENT"
    evaluation_basis: str = "RULE_MISSING_HELD"
    rule_a_status: str = "APPLIED_WITH_RESPONSE"
    rule_t_status: str = "HELD_MISSING_RULE"
    rule_a_hash: str | None = None
    rule_t_hash: str | None = None
    evaluated_readset_hash: str | None = None
    permission_hash: str | None = None
    actor_state_status: str = "VALID_EMPTY"
    memory_evidence: str = "ACTOR_UNKNOWN"
    sci05_status: str = "ADMITTED"
    sci05_certificate_hash: str | None = None
    world_receipt_hash: str | None = None
    world_event_id: str | None = None
    legacy_receipt_hash: str | None = None
    legacy_event_hash: str | None = None
    legacy_after_hash: str | None = None
    legacy_domain_hash: str | None = None
    target_id: str | None = None
    target_hash: str | None = None
    prior_attempt_id: str | None = None
    supersession_grant_hash: str | None = None
    semantic_payload: Mapping[str, Any] | None = None
    exact_reason: str = ""
    effective_us: int | None = None

    def request_digest(self) -> str:
        """Return the stable digest of every semantic request field."""
        return sha({"schema": REQUEST_SCHEMA, "request": asdict(self)})


def _validate_request(request: PublishRequest) -> bool:
    _refuse(request.decision_kind in DECISIONS, "UNKNOWN_DECISION_KIND")
    _refuse(request.source_status in SOURCE_STATUSES, "UNKNOWN_SOURCE_STATUS")
    _refuse(request.world_occurrence in WORLD_OCCURRENCES, "UNKNOWN_WORLD_OCCURRENCE")
    _refuse(request.actor_presence in ACTOR_PRESENCES, "UNKNOWN_ACTOR_PRESENCE")
    _refuse(request.actor_reception in ACTOR_RECEPTIONS, "UNKNOWN_ACTOR_RECEPTION")
    _refuse(request.rule_a_status in RULE_A_STATUSES, "UNKNOWN_RULE_A_STATUS")
    _refuse(request.rule_t_status in RULE_T_STATUSES, "UNKNOWN_RULE_T_STATUS")
    _refuse(request.actor_state_status in ACTOR_STATES, "UNKNOWN_ACTOR_STATE")
    _refuse(request.memory_evidence in MEMORY_EVIDENCE, "UNKNOWN_MEMORY_EVIDENCE")
    _refuse(request.sci05_status in SCI05_STATUSES, "UNKNOWN_SCI05_STATUS")
    _refuse(request.evaluation_basis in EVALUATION_BASES, "UNKNOWN_EVALUATION_BASIS")
    _refuse(request.proposal_state in PROPOSAL_STATES, "UNKNOWN_PROPOSAL_STATE")
    _refuse(request.event_key != "", "EVENT_KEY_REQUIRED")
    _refuse(request.idempotency_key != "", "IDEMPOTENCY_KEY_REQUIRED")
    _refuse(request.source_cut_hash != "", "SOURCE_CUT_REQUIRED")
    _refuse(request.source_scope_hash != "", "SOURCE_SCOPE_REQUIRED")
    _refuse(request.settled_scope_hash != "", "SETTLED_SCOPE_REQUIRED")
    _refuse(
        (request.target_id is None) == (request.target_hash is None),
        "TARGET_PAIR_REQUIRED",
    )
    _refuse(
        (request.prior_attempt_id is None)
        == (request.supersession_grant_hash is None),
        "REQUALIFICATION_PAIR_REQUIRED",
    )
    final = request.decision_kind in FINAL_KINDS
    if final:
        _refuse(request.rule_t_status == request.decision_kind, "STATUS_AXIS_CONFLICT")
        _refuse(
            request.evaluation_basis == "ISSUED_RULE_T_EVALUATED",
            "TRUE_NO_CHANGE_REQUIRES_ISSUED_RULE_T_EVALUATION",
        )
        _refuse(request.rule_t_hash is not None, "RULE_T_HASH_REQUIRED")
        _refuse(
            request.evaluated_readset_hash is not None,
            "EVALUATED_READSET_REQUIRED",
        )
        _refuse(request.source_status == "QUALIFIED", "FINAL_REQUIRES_QUALIFIED_SOURCE")
        _refuse(
            request.sci05_status in ("ADMITTED", "NOT_APPLICABLE"),
            "SCI05_DENIED_CANNOT_FINALIZE",
        )
        _refuse(
            request.world_occurrence == "OCCURRED",
            "FINAL_REQUIRES_OCCURRED_WORLD",
        )
        _refuse(
            request.actor_presence == "CO_PRESENT"
            and request.actor_reception in ("RECEIVED", "PARTIAL"),
            "FINAL_REQUIRES_ACTOR_PRESENCE",
        )
        _refuse(
            request.proposal_state == "PROPOSAL_PRESENT",
            "FINAL_CANNOT_INFER_NO_CHANGE",
        )
        if request.decision_kind == "COMMITTED_CHANGE":
            _refuse(request.semantic_payload is not None, "SEMANTIC_PAYLOAD_REQUIRED")
    else:
        _refuse(
            request.rule_t_status not in ("COMMITTED_CHANGE", "TRUE_NO_CHANGE_EVALUATED"),
            "STATUS_AXIS_CONFLICT",
        )
        _refuse(
            request.rule_t_status in HELD_RULE_T[request.decision_kind],
            "STATUS_AXIS_CONFLICT",
        )
        _refuse(
            request.evaluation_basis in HELD_BASIS[request.decision_kind],
            "HELD_BASIS_CONFLICT",
        )
        _refuse(request.rule_t_hash is None, "HELD_CANNOT_CLAIM_RULE_T")
        _refuse(
            request.evaluated_readset_hash is None,
            "HELD_CANNOT_CLAIM_EVALUATED_READSET",
        )
        _refuse(
            request.evaluation_basis != "ISSUED_RULE_T_EVALUATED",
            "HELD_CANNOT_CLAIM_RULE_T_EVALUATION",
        )
        if request.proposal_state == "NO_PROPOSAL":
            _refuse(
                request.evaluation_basis == "NO_PROPOSAL_HELD",
                "NO_PROPOSAL_BASIS_CONFLICT",
            )
        if request.proposal_state == "NO_EVENT":
            _refuse(
                request.evaluation_basis == "NO_EVENT_HELD",
                "NO_EVENT_BASIS_CONFLICT",
            )
    if request.world_occurrence == "OCCURRED":
        _refuse(request.world_receipt_hash is not None, "WORLD_RECEIPT_REQUIRED")
    if request.sci05_status in ("DENIED", "HELD", "INTEGRITY_FAILED"):
        _refuse(
            request.sci05_certificate_hash is None,
            "SCI05_DENIED_WITH_CERTIFICATE_INVALID",
        )
    return final


class ActorAuthority:
    """One test-only canonical actor branch authority."""

    def __init__(
        self,
        path: str | Path,
        *,
        actor_id: str,
        branch_id: str = "b0",
        branch_epoch: str = "e0",
        source_cut_hash: str = "TEST_ONLY_SOURCE_CUT",
        source_root_hash: str = "TEST_ONLY_SOURCE_ROOT",
        source_grant_hash: str = "TEST_ONLY_SOURCE_GRANT",
        c12_branch_id: str = "c12-root",
        admin_now: int = NOW,
    ) -> None:
        self.path = Path(path)
        self.actor_id = actor_id
        self.branch_id = branch_id
        self.branch_epoch = branch_epoch
        self.admin_now = admin_now
        self.conn = _connect(self.path, SCHEMA)
        branch = self._branch_row()
        if branch is None:
            _refuse(source_grant_hash != "", "SOURCE_GRANT_REQUIRED")
            _insert(
                self.conn,
                "actor_branch",
                {
                    "actor_id": actor_id,
                    "branch_id": branch_id,
                    "branch_epoch": branch_epoch,
                    "parent_actor_id": None,
                    "parent_branch_id": None,
                    "parent_branch_epoch": None,
                    "fork_base_version_hash": None,
                    "fork_source_cut_hash": None,
                    "fork_c12_branch_id": None,
                    "fork_c12_root_hash": None,
                    "fork_c12_perception_hash": None,
                    "fork_c12_watermark": None,
                    "source_grant_hash": source_grant_hash,
                    "source_cut_hash": source_cut_hash,
                    "source_root_hash": source_root_hash,
                    "c12_branch_id": c12_branch_id,
                    "created_admin_us": admin_now,
                },
            )
            semantic = sha({})
            version_hash = sha(
                {
                    "schema": "C9_ACTOR_VERSION_R3@1",
                    "actor": actor_id,
                    "branch": branch_id,
                    "epoch": branch_epoch,
                    "version": 0,
                    "kind": "GENESIS_VALID_EMPTY",
                    "parent": None,
                    "semantic": semantic,
                    "state": {},
                }
            )
            _insert(
                self.conn,
                "actor_version",
                {
                    "actor_id": actor_id,
                    "branch_id": branch_id,
                    "branch_epoch": branch_epoch,
                    "version_no": 0,
                    "version_kind": "GENESIS_VALID_EMPTY",
                    "version_hash": version_hash,
                    "parent_version_hash": None,
                    "semantic_hash": semantic,
                    "canonical_state_json": "{}",
                    "state_grade": "VALID_EMPTY",
                    "source_cut_hash": source_cut_hash,
                    "event_effective_us": None,
                    "decision_receipt_hash": None,
                    "created_admin_us": admin_now,
                },
            )
            _insert(
                self.conn,
                "actor_head",
                {
                    "actor_id": actor_id,
                    "branch_id": branch_id,
                    "branch_epoch": branch_epoch,
                    "head_version_no": 0,
                    "head_version_hash": version_hash,
                    "head_semantic_hash": semantic,
                    "last_receipt_seq": 0,
                    "last_finalized_seq": 0,
                    "updated_admin_us": admin_now,
                },
            )
        else:
            _refuse(branch["actor_id"] == actor_id, "ACTOR_BRANCH_MISMATCH")
            _refuse(branch["branch_epoch"] == branch_epoch, "BRANCH_EPOCH_MISMATCH")
            self.branch_epoch = str(branch["branch_epoch"])
        branch = self._branch_row()
        _refuse(branch is not None, "ACTOR_BRANCH_MISSING")
        self.source_cut_hash = str(branch["source_cut_hash"])
        self.source_root_hash = str(branch["source_root_hash"])
        self.c12_branch_id = str(branch["c12_branch_id"])

    def _branch_row(self) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM actor_branch WHERE actor_id=? AND branch_id=?",
            (self.actor_id, self.branch_id),
        ).fetchone()

    def head(self) -> dict[str, Any]:
        """Return the current actor head."""
        row = self.conn.execute(
            "SELECT * FROM actor_head WHERE actor_id=? AND branch_id=?",
            (self.actor_id, self.branch_id),
        ).fetchone()
        _refuse(row is not None, "ACTOR_HEAD_MISSING")
        return dict(row)

    def head_signature(self) -> tuple[Any, ...]:
        """Return the CAS tuple used by expected-head callers."""
        head = self.head()
        return (
            head["branch_epoch"],
            head["head_version_no"],
            head["head_version_hash"],
            head["last_receipt_seq"],
            head["last_finalized_seq"],
        )

    def add_world_receipt(
        self,
        *,
        world_receipt_hash: str,
        world_event_id: str,
        c8_branch_id: str,
        c8_root_hash: str,
        c8_head_hash: str,
        effective_us: int,
        source_owner: str = "TEST_ONLY_C8_OWNER",
        source_grade: str = "TEST_ONLY_SOURCEFREE",
        source_cut_hash: str = "TEST_ONLY_C8_SOURCE_CUT",
        payload_digest: str | None = None,
        world_parent_hash: str | None = None,
    ) -> dict[str, Any]:
        """Insert one external C8 world receipt without changing actor state."""
        body = {
            "world_receipt_hash": world_receipt_hash,
            "world_event_id": world_event_id,
            "c8_branch_id": c8_branch_id,
            "c8_root_hash": c8_root_hash,
            "c8_head_hash": c8_head_hash,
            "effective_us": effective_us,
            "source_owner": source_owner,
            "source_grade": source_grade,
            "source_cut_hash": source_cut_hash,
        }
        _insert(
            self.conn,
            "world_receipt",
            {
                **body,
                "world_parent_hash": world_parent_hash,
                "payload_digest": payload_digest or sha({"world": world_event_id}),
                "canonical_receipt_json": canon(body),
                "verified_admin_us": self.admin_now,
            },
        )
        return body

    def add_rule(
        self,
        *,
        rule_hash: str,
        rule_kind: str,
        issuer_ref: str,
        source_cut_hash: str,
        issued_state: str = "ISSUED",
        rule_body: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Insert one issued-or-held test-only Rule A/T identity."""
        _refuse(rule_kind in ("A", "T"), "RULE_KIND_INVALID")
        _refuse(
            issued_state in ("ISSUED", "HELD", "DENIED", "INTEGRITY_FAILED"),
            "RULE_STATE_INVALID",
        )
        _insert(
            self.conn,
            "rule_issuance",
            {
                "rule_hash": rule_hash,
                "rule_kind": rule_kind,
                "issued_state": issued_state,
                "issuer_ref": issuer_ref,
                "source_cut_hash": source_cut_hash,
                "canonical_rule_json": canon(
                    dict(rule_body or {"hash": rule_hash, "kind": rule_kind})
                ),
                "created_admin_us": self.admin_now,
            },
        )
        return {
            "rule_hash": rule_hash,
            "rule_kind": rule_kind,
            "issued_state": issued_state,
        }

    def add_legacy_bridge(
        self,
        *,
        legacy_receipt_hash: str,
        legacy_db_id: str,
        legacy_event_hash: str,
        legacy_response_ref: str,
        legacy_target_branch: str,
        legacy_target_reason: str,
        legacy_before_hash: str,
        legacy_after_hash: str,
        legacy_domain_hash: str,
        legacy_tables: list[str],
    ) -> dict[str, Any]:
        """Insert one frozen legacy S36 receipt identity."""
        body = {
            "schema": "SOROK_C9_LEGACY_BRIDGE_R3@1",
            "receipt_hash": legacy_receipt_hash,
            "readset_tables": legacy_tables,
        }
        _insert(
            self.conn,
            "legacy_bridge",
            {
                "legacy_receipt_hash": legacy_receipt_hash,
                "legacy_db_id": legacy_db_id,
                "legacy_event_hash": legacy_event_hash,
                "legacy_response_ref": legacy_response_ref,
                "legacy_target_branch": legacy_target_branch,
                "legacy_target_reason": legacy_target_reason,
                "legacy_before_hash": legacy_before_hash,
                "legacy_after_hash": legacy_after_hash,
                "legacy_domain_hash": legacy_domain_hash,
                "legacy_receipt_json": canon(body),
                "verified_admin_us": self.admin_now,
            },
        )
        return body

    def add_requalification_grant(
        self,
        *,
        grant_hash: str,
        prior_attempt_id: str,
        issuance_kind: str,
        issuance_ref: str,
        source_cut_hash: str,
        issued_state: str = "ISSUED",
    ) -> dict[str, Any]:
        """Insert one fresh Rule A/T or source issuance for a held attempt."""
        _refuse(grant_hash != "", "GRANT_HASH_REQUIRED")
        _refuse(issuance_kind in ("RULE_A", "RULE_T", "SOURCE"), "GRANT_KIND_INVALID")
        _refuse(issuance_ref != "", "GRANT_ISSUANCE_REF_REQUIRED")
        _refuse(source_cut_hash != "", "GRANT_SOURCE_CUT_REQUIRED")
        _refuse(
            issued_state in ("ISSUED", "HELD", "DENIED"),
            "GRANT_STATE_INVALID",
        )
        prior = self._attempt_by_id(prior_attempt_id)
        _refuse(prior is not None, "PRIOR_ATTEMPT_MISSING")
        _refuse(
            prior["actor_id"] == self.actor_id
            and prior["branch_id"] == self.branch_id
            and prior["branch_epoch"] == self.branch_epoch,
            "PRIOR_ATTEMPT_SCOPE_MISMATCH",
        )
        _refuse(prior["attempt_state"] == "HELD", "PRIOR_ATTEMPT_NOT_HELD")
        if issuance_kind in ("RULE_A", "RULE_T"):
            wanted = "A" if issuance_kind == "RULE_A" else "T"
            _refuse(
                self.conn.execute(
                    "SELECT 1 FROM rule_issuance WHERE rule_hash=? AND rule_kind=? "
                    "AND issued_state='ISSUED' AND source_cut_hash=?",
                    (issuance_ref, wanted, source_cut_hash),
                ).fetchone()
                is not None,
                "GRANT_ISSUANCE_NOT_ISSUED",
            )
        body = {
            "schema": "C9_REQUALIFICATION_GRANT_R3@1",
            "grant_hash": grant_hash,
            "actor": self.actor_id,
            "branch": self.branch_id,
            "epoch": self.branch_epoch,
            "event_key": prior["event_key"],
            "prior_attempt_id": prior_attempt_id,
            "prior_receipt_hash": prior["receipt_hash"],
            "issuance_kind": issuance_kind,
            "issuance_ref": issuance_ref,
            "issued_state": issued_state,
            "source_cut_hash": source_cut_hash,
        }
        _insert(
            self.conn,
            "requalification_grant",
            {
                "grant_hash": grant_hash,
                "actor_id": self.actor_id,
                "branch_id": self.branch_id,
                "branch_epoch": self.branch_epoch,
                "event_key": prior["event_key"],
                "prior_attempt_id": prior_attempt_id,
                "prior_receipt_hash": prior["receipt_hash"],
                "issuance_kind": issuance_kind,
                "issuance_ref": issuance_ref,
                "issued_state": issued_state,
                "source_cut_hash": source_cut_hash,
                "canonical_grant_json": canon(body),
                "created_admin_us": self.admin_now,
            },
        )
        return body

    def _grant_for_requalification(
        self,
        request: PublishRequest,
        prior: sqlite3.Row,
    ) -> sqlite3.Row | None:
        grant_hash = request.supersession_grant_hash
        if grant_hash is None:
            return None
        return self.conn.execute(
            "SELECT * FROM requalification_grant WHERE grant_hash=? "
            "AND actor_id=? AND branch_id=? AND branch_epoch=? AND event_key=? "
            "AND prior_attempt_id=? AND prior_receipt_hash=? "
            "AND source_cut_hash=? AND issued_state='ISSUED'",
            (
                grant_hash,
                self.actor_id,
                self.branch_id,
                self.branch_epoch,
                request.event_key,
                prior["attempt_id"],
                prior["receipt_hash"],
                request.source_cut_hash,
            ),
        ).fetchone()

    def _attempt_by_key(self, idempotency_key: str) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM event_attempt WHERE idempotency_key=?",
            (idempotency_key,),
        ).fetchone()

    def _attempt_by_id(self, attempt_id: str) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM event_attempt WHERE attempt_id=?", (attempt_id,)
        ).fetchone()

    def _receipt_by_hash(self, receipt_hash: str) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM decision_receipt WHERE receipt_hash=?", (receipt_hash,)
        ).fetchone()

    def _validate_references(self, request: PublishRequest, final: bool) -> None:
        branch = self._branch_row()
        _refuse(branch is not None, "ACTOR_BRANCH_MISSING")
        if request.world_receipt_hash is not None:
            _refuse(
                self.conn.execute(
                    "SELECT 1 FROM world_receipt WHERE world_receipt_hash=?",
                    (request.world_receipt_hash,),
                ).fetchone()
                is not None,
                "WORLD_RECEIPT_MISSING",
            )
        if request.legacy_receipt_hash is not None:
            _refuse(
                self.conn.execute(
                    "SELECT 1 FROM legacy_bridge WHERE legacy_receipt_hash=?",
                    (request.legacy_receipt_hash,),
                ).fetchone()
                is not None,
                "LEGACY_RECEIPT_MISSING",
            )
        if request.rule_a_hash is not None:
            _refuse(
                self.conn.execute(
                    "SELECT 1 FROM rule_issuance WHERE rule_hash=? AND rule_kind='A'",
                    (request.rule_a_hash,),
                ).fetchone()
                is not None,
                "RULE_A_ISSUANCE_MISSING",
            )
        if request.rule_t_hash is not None:
            _refuse(
                self.conn.execute(
                    "SELECT 1 FROM rule_issuance WHERE rule_hash=? AND rule_kind='T'",
                    (request.rule_t_hash,),
                ).fetchone()
                is not None,
                "RULE_T_ISSUANCE_MISSING",
            )
        if final:
            _refuse(
                self.conn.execute(
                    "SELECT 1 FROM rule_issuance WHERE rule_hash=? "
                    "AND rule_kind='T' AND issued_state='ISSUED'",
                    (request.rule_t_hash,),
                ).fetchone()
                is not None,
                "ISSUED_RULE_T_REQUIRED",
            )

    def _check_expected(self, expected_head: Any) -> None:
        if expected_head is None:
            return
        head = self.head()
        wanted = {
            "branch_epoch": head["branch_epoch"],
            "head_version_no": head["head_version_no"],
            "head_version_hash": head["head_version_hash"],
            "last_receipt_seq": head["last_receipt_seq"],
            "last_finalized_seq": head["last_finalized_seq"],
        }
        if isinstance(expected_head, Mapping):
            matched = set(wanted).issubset(expected_head.keys()) and all(
                expected_head[key] == value for key, value in wanted.items()
            )
        else:
            matched = tuple(expected_head) == self.head_signature()
        _refuse(matched, "CAS_CONFLICT")

    def _result(self, attempt_id: str, *, replayed: bool) -> dict[str, Any]:
        attempt = self._attempt_by_id(attempt_id)
        _refuse(attempt is not None, "PUBLISHED_ATTEMPT_MISSING")
        receipt = self._receipt_by_hash(attempt["receipt_hash"])
        _refuse(receipt is not None, "PUBLISHED_RECEIPT_MISSING")
        outbox = self.conn.execute(
            "SELECT projection_state FROM projection_outbox WHERE receipt_hash=?",
            (attempt["receipt_hash"],),
        ).fetchone()
        _refuse(outbox is not None, "PUBLISHED_OUTBOX_MISSING")
        return {
            "replayed": replayed,
            "receipt_hash": attempt["receipt_hash"],
            "receipt_json": receipt["canonical_receipt_json"],
            "receipt": json.loads(receipt["canonical_receipt_json"]),
            "seq": int(receipt["commit_seq"]),
            "final": receipt["decision_kind"] in FINAL_KINDS,
            "version_hash": receipt["result_version_hash"],
            "attempt_id": attempt["attempt_id"],
            "attempt_no": int(attempt["attempt_no"]),
            "head": self.head(),
            "outbox_state": outbox[0],
        }

    def publish(
        self,
        request: PublishRequest,
        *,
        expected_head: Any = None,
        fault: str | None = None,
    ) -> dict[str, Any]:
        """Publish one receipt atomically, replaying exact idempotent retries."""
        final = _validate_request(request)
        digest = request.request_digest()
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            existing = self._attempt_by_key(request.idempotency_key)
            if existing is not None:
                _refuse(
                    existing["actor_id"] == self.actor_id
                    and existing["branch_id"] == self.branch_id
                    and existing["branch_epoch"] == self.branch_epoch,
                    "IDEMPOTENCY_KEY_SCOPE_MISMATCH",
                )
                if existing["request_digest"] != digest:
                    raise IdempotencyConflict("IDEMPOTENCY_PAYLOAD_CONFLICT")
                self.conn.execute("COMMIT")
                return self._result(existing["attempt_id"], replayed=True)
            self._check_expected(expected_head)
            head = self.head()
            branch = self._branch_row()
            _refuse(branch is not None, "ACTOR_BRANCH_MISSING")
            event_final = self.conn.execute(
                "SELECT attempt_id FROM event_attempt WHERE actor_id=? "
                "AND branch_id=? AND branch_epoch=? AND event_key=? "
                "AND attempt_state='FINALIZED'",
                (self.actor_id, self.branch_id, self.branch_epoch, request.event_key),
            ).fetchone()
            _refuse(event_final is None, "EVENT_ALREADY_FINALIZED")
            prior = None
            if request.prior_attempt_id is not None:
                prior = self._attempt_by_id(request.prior_attempt_id)
                _refuse(prior is not None, "PRIOR_ATTEMPT_MISSING")
                _refuse(
                    prior["actor_id"] == self.actor_id
                    and prior["branch_id"] == self.branch_id
                    and prior["branch_epoch"] == self.branch_epoch
                    and prior["event_key"] == request.event_key,
                    "PRIOR_ATTEMPT_SCOPE_MISMATCH",
                )
                _refuse(prior["attempt_state"] == "HELD", "PRIOR_ATTEMPT_NOT_HELD")
                _refuse(
                    request.supersession_grant_hash is not None
                    and request.supersession_grant_hash != "",
                    "REQUALIFICATION_GRANT_REQUIRED",
                )
            latest_attempt_no = int(
                self.conn.execute(
                    "SELECT coalesce(max(attempt_no),0) FROM event_attempt "
                    "WHERE actor_id=? AND branch_id=? AND branch_epoch=? "
                    "AND event_key=?",
                    (
                        self.actor_id,
                        self.branch_id,
                        self.branch_epoch,
                        request.event_key,
                    ),
                ).fetchone()[0]
            )
            attempt_no = request.attempt_no
            if attempt_no <= 0:
                attempt_no = latest_attempt_no + 1
            _refuse(attempt_no == latest_attempt_no + 1, "ATTEMPT_NO_GAP")
            if prior is not None:
                _refuse(
                    int(prior["attempt_no"]) == latest_attempt_no,
                    "PRIOR_ATTEMPT_NOT_LATEST",
                )
            if attempt_no > 1:
                _refuse(prior is not None, "PRIOR_ATTEMPT_REQUIRED")
                _refuse(
                    self._grant_for_requalification(request, prior) is not None,
                    "REQUALIFICATION_GRANT_MISSING",
                )
            else:
                _refuse(
                    request.supersession_grant_hash is None,
                    "GRANT_WITHOUT_PRIOR",
                )
            _refuse(
                request.source_cut_hash == branch["source_cut_hash"]
                and request.source_root_hash == branch["source_root_hash"],
                "SOURCE_CHANGED_REQUIRES_FORK",
            )
            self._validate_references(request, final)
            seq = int(head["last_receipt_seq"]) + 1
            before_version = str(head["head_version_hash"])
            before_semantic = str(head["head_semantic_hash"])
            before_version_row = self.conn.execute(
                "SELECT * FROM actor_version WHERE actor_id=? AND branch_id=? "
                "AND branch_epoch=? AND version_no=?",
                (
                    self.actor_id,
                    self.branch_id,
                    self.branch_epoch,
                    head["head_version_no"],
                ),
            ).fetchone()
            _refuse(before_version_row is not None, "ACTOR_VERSION_MISSING")
            version_state_json = str(before_version_row["canonical_state_json"])
            version_state_grade = str(before_version_row["state_grade"])
            after_semantic = None
            result_version = None
            if final:
                if request.decision_kind == "TRUE_NO_CHANGE_EVALUATED":
                    after_semantic = before_semantic
                else:
                    after_semantic = sha(
                        {
                            "actor": self.actor_id,
                            "branch": self.branch_id,
                            "epoch": self.branch_epoch,
                            "event": request.event_key,
                            "payload": dict(request.semantic_payload or {}),
                        }
                    )
                    _refuse(
                        after_semantic != before_semantic,
                        "COMMITTED_CHANGE_REQUIRES_DIFFERENT_SEMANTIC",
                    )
                    version_state_json = canon(
                        {
                            "event_key": request.event_key,
                            "semantic": after_semantic,
                            "payload": dict(request.semantic_payload or {}),
                        }
                    )
                    version_state_grade = (
                        "VERSIONED_PRESENT"
                        if request.actor_state_status == "VALID_EMPTY"
                        else request.actor_state_status
                    )
                result_version = sha(
                    {
                        "schema": "C9_ACTOR_VERSION_R3@1",
                        "actor": self.actor_id,
                        "branch": self.branch_id,
                        "epoch": self.branch_epoch,
                        "seq": seq,
                        "parent": before_version,
                        "semantic": after_semantic,
                        "kind": request.decision_kind,
                    }
                )
            prior_receipt = None if prior is None else str(prior["receipt_hash"])
            receipt_body = {
                "schema": RECEIPT_SCHEMA,
                "actor": self.actor_id,
                "branch": self.branch_id,
                "epoch": self.branch_epoch,
                "commit_seq": seq,
                "event_key": request.event_key,
                "attempt_no": attempt_no,
                "idempotency_key": request.idempotency_key,
                "request_digest": digest,
                "decision_kind": request.decision_kind,
                "before_version_hash": before_version,
                "result_version_hash": result_version,
                "before_semantic_hash": before_semantic,
                "after_semantic_hash": after_semantic,
                "source_root_hash": request.source_root_hash,
                "source_cut_hash": request.source_cut_hash,
                "source_scope_hash": request.source_scope_hash,
                "settled_scope_hash": request.settled_scope_hash,
                "source_status": request.source_status,
                "world_occurrence": request.world_occurrence,
                "actor_presence": request.actor_presence,
                "actor_reception": request.actor_reception,
                "proposal_state": request.proposal_state,
                "evaluation_basis": request.evaluation_basis,
                "rule_a_status": request.rule_a_status,
                "rule_t_status": request.rule_t_status,
                "rule_a_hash": request.rule_a_hash,
                "rule_t_hash": request.rule_t_hash,
                "evaluated_readset_hash": request.evaluated_readset_hash,
                "permission_hash": request.permission_hash,
                "actor_state_status": request.actor_state_status,
                "memory_evidence": request.memory_evidence,
                "sci05_status": request.sci05_status,
                "sci05_certificate_hash": request.sci05_certificate_hash,
                "world_receipt_hash": request.world_receipt_hash,
                "legacy_receipt_hash": request.legacy_receipt_hash,
                "prior_receipt_hash": prior_receipt,
                "exact_reason": request.exact_reason,
            }
            receipt_hash = sha(receipt_body)
            receipt_json = canon(receipt_body)
            attempt_id = "ATT-" + sha(
                {
                    "actor": self.actor_id,
                    "branch": self.branch_id,
                    "epoch": self.branch_epoch,
                    "event": request.event_key,
                    "attempt_no": attempt_no,
                    "idempotency": request.idempotency_key,
                }
            )[:32]
            _insert(
                self.conn,
                "decision_receipt",
                {
                    "receipt_hash": receipt_hash,
                    "decision_kind": request.decision_kind,
                    "actor_id": self.actor_id,
                    "branch_id": self.branch_id,
                    "branch_epoch": self.branch_epoch,
                    "commit_seq": seq,
                    "prior_receipt_hash": prior_receipt,
                    "event_key": request.event_key,
                    "attempt_no": attempt_no,
                    "source_scope_hash": request.source_scope_hash,
                    "settled_scope_hash": request.settled_scope_hash,
                    "source_root_hash": request.source_root_hash,
                    "source_cut_hash": request.source_cut_hash,
                    "legacy_receipt_hash": request.legacy_receipt_hash,
                    "legacy_event_hash": request.legacy_event_hash,
                    "legacy_after_hash": request.legacy_after_hash,
                    "legacy_domain_hash": request.legacy_domain_hash,
                    "world_receipt_hash": request.world_receipt_hash,
                    "world_event_id": request.world_event_id,
                    "source_status": request.source_status,
                    "world_occurrence": request.world_occurrence,
                    "actor_presence": request.actor_presence,
                    "actor_reception": request.actor_reception,
                    "proposal_state": request.proposal_state,
                    "evaluation_basis": request.evaluation_basis,
                    "rule_a_status": request.rule_a_status,
                    "rule_t_status": request.rule_t_status,
                    "actor_state_status": request.actor_state_status,
                    "memory_evidence": request.memory_evidence,
                    "sci05_status": request.sci05_status,
                    "sci05_certificate_hash": request.sci05_certificate_hash,
                    "before_version_hash": before_version,
                    "result_version_hash": result_version,
                    "before_semantic_hash": before_semantic,
                    "after_semantic_hash": after_semantic,
                    "rule_a_hash": request.rule_a_hash,
                    "rule_t_hash": request.rule_t_hash,
                    "evaluated_readset_hash": request.evaluated_readset_hash,
                    "permission_hash": request.permission_hash,
                    "exact_reason": request.exact_reason,
                    "canonical_receipt_json": receipt_json,
                    "effective_us": request.effective_us,
                    "admin_committed_us": self.admin_now,
                },
            )
            if final:
                _insert(
                    self.conn,
                    "actor_version",
                    {
                        "actor_id": self.actor_id,
                        "branch_id": self.branch_id,
                        "branch_epoch": self.branch_epoch,
                        "version_no": int(head["head_version_no"]) + 1,
                        "version_kind": (
                            "ADMINISTRATIVE_NOCHANGE"
                            if request.decision_kind == "TRUE_NO_CHANGE_EVALUATED"
                            else "SEMANTIC_CHANGE"
                        ),
                        "version_hash": result_version,
                        "parent_version_hash": before_version,
                        "semantic_hash": after_semantic,
                        "canonical_state_json": version_state_json,
                        "state_grade": version_state_grade,
                        "source_cut_hash": request.source_cut_hash,
                        "event_effective_us": request.effective_us,
                        "decision_receipt_hash": receipt_hash,
                        "created_admin_us": self.admin_now,
                    },
                )
            _insert(
                self.conn,
                "event_attempt",
                {
                    "attempt_id": attempt_id,
                    "event_key": request.event_key,
                    "actor_id": self.actor_id,
                    "branch_id": self.branch_id,
                    "branch_epoch": self.branch_epoch,
                    "attempt_no": attempt_no,
                    "idempotency_key": request.idempotency_key,
                    "request_digest": digest,
                    "source_root_hash": request.source_root_hash,
                    "source_cut_hash": request.source_cut_hash,
                    "source_scope_hash": request.source_scope_hash,
                    "settled_scope_hash": request.settled_scope_hash,
                    "prior_attempt_id": request.prior_attempt_id,
                    "receipt_hash": receipt_hash,
                    "attempt_state": "FINALIZED" if final else "HELD",
                    "supersedes_receipt_hash": prior_receipt,
                    "supersession_grant_hash": request.supersession_grant_hash,
                    "canonical_attempt_json": canon(
                        {
                            "event_key": request.event_key,
                            "attempt_no": attempt_no,
                            "idempotency_key": request.idempotency_key,
                            "request_digest": digest,
                            "prior_attempt_id": request.prior_attempt_id,
                        }
                    ),
                    "created_admin_us": self.admin_now,
                },
            )
            if request.target_id is not None:
                _insert(
                    self.conn,
                    "actor_target",
                    {
                        "actor_id": self.actor_id,
                        "branch_id": self.branch_id,
                        "branch_epoch": self.branch_epoch,
                        "target_id": request.target_id,
                        "target_hash": request.target_hash,
                        "record_json": canon(
                            {
                                "actor": self.actor_id,
                                "branch": self.branch_id,
                                "epoch": self.branch_epoch,
                                "target_id": request.target_id,
                            }
                        ),
                        "source_receipt_hash": request.world_receipt_hash,
                        "created_receipt_hash": receipt_hash,
                        "created_admin_us": self.admin_now,
                    },
                )
            _insert(
                self.conn,
                "projection_outbox",
                {
                    "receipt_hash": receipt_hash,
                    "actor_id": self.actor_id,
                    "branch_id": self.branch_id,
                    "branch_epoch": self.branch_epoch,
                    "commit_seq": seq,
                    "actor_result_hash": result_version,
                    "world_receipt_hash": request.world_receipt_hash,
                    "payload_digest": sha({"receipt": receipt_hash}),
                    "envelope_json": canon(
                        {
                            "receipt_hash": receipt_hash,
                            "version_hash": result_version,
                            "decision_kind": request.decision_kind,
                        }
                    ),
                    "projection_state": "PENDING",
                    "projected_c12_hash": None,
                    "acked_admin_us": None,
                    "attempt_count": 0,
                    "last_error_code": None,
                },
            )
            changed = self.conn.execute(
                "UPDATE actor_head SET head_version_no=?,head_version_hash=?,"
                "head_semantic_hash=?,last_receipt_seq=?,last_finalized_seq=?,"
                "updated_admin_us=? WHERE actor_id=? AND branch_id=? "
                "AND branch_epoch=? AND head_version_no=? AND head_version_hash=? "
                "AND last_receipt_seq=? AND last_finalized_seq=?",
                (
                    int(head["head_version_no"]) + (1 if final else 0),
                    result_version if final else head["head_version_hash"],
                    after_semantic if final else head["head_semantic_hash"],
                    seq,
                    seq if final else head["last_finalized_seq"],
                    self.admin_now,
                    self.actor_id,
                    self.branch_id,
                    self.branch_epoch,
                    head["head_version_no"],
                    head["head_version_hash"],
                    head["last_receipt_seq"],
                    head["last_finalized_seq"],
                ),
            ).rowcount
            _refuse(changed == 1, "CAS_CONFLICT")
            if fault == "before_commit":
                raise Refusal("C3_INJECTED_FAILURE")
            self.conn.execute("COMMIT")
            return self._result(attempt_id, replayed=False)
        except BaseException:
            if self.conn.in_transaction:
                self.conn.execute("ROLLBACK")
            raise

    def fork_branch(
        self,
        *,
        branch_id: str,
        branch_epoch: str,
        source_cut_hash: str,
        source_root_hash: str,
        source_grant_hash: str,
        c12_branch_id: str,
        c12_root_hash: str,
        c12_perception_hash: str,
        c12_watermark: int = 0,
    ) -> dict[str, Any]:
        """Create one inherited branch without copying receipts or heads."""
        _refuse(source_grant_hash != "", "SOURCE_GRANT_REQUIRED")
        _refuse(c12_perception_hash != "", "C12_PERCEPTION_HASH_REQUIRED")
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            parent = self._branch_row()
            _refuse(parent is not None, "ACTOR_BRANCH_MISSING")
            parent_head = self.head()
            parent_version = self.conn.execute(
                "SELECT * FROM actor_version WHERE actor_id=? AND branch_id=? "
                "AND branch_epoch=? AND version_no=?",
                (
                    self.actor_id,
                    self.branch_id,
                    self.branch_epoch,
                    parent_head["head_version_no"],
                ),
            ).fetchone()
            _refuse(parent_version is not None, "PARENT_VERSION_MISSING")
            _refuse(
                self.conn.execute(
                    "SELECT 1 FROM actor_branch WHERE actor_id=? AND branch_id=?",
                    (self.actor_id, branch_id),
                ).fetchone()
                is None,
                "ACTOR_BRANCH_EXISTS",
            )
            _insert(
                self.conn,
                "actor_branch",
                {
                    "actor_id": self.actor_id,
                    "branch_id": branch_id,
                    "branch_epoch": branch_epoch,
                    "parent_actor_id": self.actor_id,
                    "parent_branch_id": self.branch_id,
                    "parent_branch_epoch": self.branch_epoch,
                    "fork_base_version_hash": parent_head["head_version_hash"],
                    "fork_source_cut_hash": source_cut_hash,
                    "fork_c12_branch_id": c12_branch_id,
                    "fork_c12_root_hash": c12_root_hash,
                    "fork_c12_perception_hash": c12_perception_hash,
                    "fork_c12_watermark": c12_watermark,
                    "source_grant_hash": source_grant_hash,
                    "source_cut_hash": source_cut_hash,
                    "source_root_hash": source_root_hash,
                    "c12_branch_id": c12_branch_id,
                    "created_admin_us": self.admin_now,
                },
            )
            version_hash = sha(
                {
                    "schema": "C9_ACTOR_VERSION_R3@1",
                    "actor": self.actor_id,
                    "branch": branch_id,
                    "epoch": branch_epoch,
                    "version": 0,
                    "kind": "FORK_INHERITED",
                    "parent": parent_head["head_version_hash"],
                    "semantic": parent_head["head_semantic_hash"],
                }
            )
            _insert(
                self.conn,
                "actor_version",
                {
                    "actor_id": self.actor_id,
                    "branch_id": branch_id,
                    "branch_epoch": branch_epoch,
                    "version_no": 0,
                    "version_kind": "FORK_INHERITED",
                    "version_hash": version_hash,
                    "parent_version_hash": parent_head["head_version_hash"],
                    "semantic_hash": parent_head["head_semantic_hash"],
                    "canonical_state_json": parent_version["canonical_state_json"],
                    "state_grade": parent_version["state_grade"],
                    "source_cut_hash": source_cut_hash,
                    "event_effective_us": None,
                    "decision_receipt_hash": None,
                    "created_admin_us": self.admin_now,
                },
            )
            _insert(
                self.conn,
                "actor_head",
                {
                    "actor_id": self.actor_id,
                    "branch_id": branch_id,
                    "branch_epoch": branch_epoch,
                    "head_version_no": 0,
                    "head_version_hash": version_hash,
                    "head_semantic_hash": parent_head["head_semantic_hash"],
                    "last_receipt_seq": 0,
                    "last_finalized_seq": 0,
                    "updated_admin_us": self.admin_now,
                },
            )
            self.conn.execute("COMMIT")
        except BaseException:
            if self.conn.in_transaction:
                self.conn.execute("ROLLBACK")
            raise
        return {
            "actor_id": self.actor_id,
            "branch_id": branch_id,
            "branch_epoch": branch_epoch,
            "parent_branch_id": self.branch_id,
            "parent_version_hash": parent_head["head_version_hash"],
            "version_hash": version_hash,
        }

    def read_semantic(self) -> dict[str, Any]:
        """Read the current semantic projection without mutating actor state."""
        head = self.head()
        row = self.conn.execute(
            "SELECT * FROM actor_version WHERE actor_id=? AND branch_id=? "
            "AND branch_epoch=? AND version_no=?",
            (
                self.actor_id,
                self.branch_id,
                self.branch_epoch,
                head["head_version_no"],
            ),
        ).fetchone()
        _refuse(row is not None, "ACTOR_VERSION_MISSING")
        return {
            "actor_id": self.actor_id,
            "branch_id": self.branch_id,
            "branch_epoch": self.branch_epoch,
            "version_no": head["head_version_no"],
            "version_hash": head["head_version_hash"],
            "semantic_hash": head["head_semantic_hash"],
            "state": json.loads(row["canonical_state_json"]),
            "source_cut_hash": row["source_cut_hash"],
            "receipt_seq": head["last_receipt_seq"],
            "finalized_seq": head["last_finalized_seq"],
        }

    def verify(self) -> dict[str, Any]:
        """Check actor head, receipt, attempt, Rule T and outbox invariants."""
        errors: list[str] = []
        head = self.conn.execute(
            "SELECT * FROM actor_head WHERE actor_id=? AND branch_id=?",
            (self.actor_id, self.branch_id),
        ).fetchone()
        if head is None:
            errors.append("head_missing")
        else:
            version = self.conn.execute(
                "SELECT * FROM actor_version WHERE actor_id=? AND branch_id=? "
                "AND branch_epoch=? AND version_no=? AND version_hash=?",
                (
                    self.actor_id,
                    self.branch_id,
                    head["branch_epoch"],
                    head["head_version_no"],
                    head["head_version_hash"],
                ),
            ).fetchone()
            if version is None:
                errors.append("head_version_missing")
            elif version["semantic_hash"] != head["head_semantic_hash"]:
                errors.append("head_semantic_mismatch")
            receipt_max = self.conn.execute(
                "SELECT coalesce(max(commit_seq),0) FROM decision_receipt "
                "WHERE actor_id=? AND branch_id=? AND branch_epoch=?",
                (self.actor_id, self.branch_id, head["branch_epoch"]),
            ).fetchone()[0]
            if int(receipt_max) != int(head["last_receipt_seq"]):
                errors.append("receipt_seq_mismatch")
            finalized_max = self.conn.execute(
                "SELECT coalesce(max(commit_seq),0) FROM decision_receipt "
                "WHERE actor_id=? AND branch_id=? AND branch_epoch=? "
                "AND decision_kind IN ('COMMITTED_CHANGE','TRUE_NO_CHANGE_EVALUATED')",
                (self.actor_id, self.branch_id, head["branch_epoch"]),
            ).fetchone()[0]
            if int(finalized_max) != int(head["last_finalized_seq"]):
                errors.append("finalized_seq_mismatch")
        missing_outbox = self.conn.execute(
            "SELECT count(*) FROM decision_receipt r WHERE r.actor_id=? "
            "AND r.branch_id=? AND NOT EXISTS (SELECT 1 FROM projection_outbox o "
            "WHERE o.receipt_hash=r.receipt_hash)",
            (self.actor_id, self.branch_id),
        ).fetchone()[0]
        if missing_outbox:
            errors.append("outbox_missing")
        bad_targets = self.conn.execute(
            "SELECT count(*) FROM actor_target t WHERE t.actor_id=? "
            "AND t.branch_id=? AND NOT EXISTS (SELECT 1 FROM decision_receipt r "
            "WHERE r.receipt_hash=t.created_receipt_hash)",
            (self.actor_id, self.branch_id),
        ).fetchone()[0]
        if bad_targets:
            errors.append("target_receipt_missing")
        bad_attempts = self.conn.execute(
            "SELECT count(*) FROM event_attempt a WHERE a.actor_id=? "
            "AND a.branch_id=? AND NOT EXISTS (SELECT 1 FROM decision_receipt r "
            "WHERE r.receipt_hash=a.receipt_hash)",
            (self.actor_id, self.branch_id),
        ).fetchone()[0]
        if bad_attempts:
            errors.append("attempt_receipt_missing")
        bad_final_rule = self.conn.execute(
            "SELECT count(*) FROM decision_receipt r WHERE r.actor_id=? "
            "AND r.branch_id=? "
            "AND r.decision_kind IN ('COMMITTED_CHANGE','TRUE_NO_CHANGE_EVALUATED') "
            "AND NOT EXISTS (SELECT 1 FROM rule_issuance i WHERE i.rule_hash="
            "r.rule_t_hash AND i.rule_kind='T' AND i.issued_state='ISSUED')",
            (self.actor_id, self.branch_id),
        ).fetchone()[0]
        if bad_final_rule:
            errors.append("final_receipt_rule_t_not_issued")
        return {
            "ok": not errors,
            "errors": errors,
            "actor_id": self.actor_id,
            "branch_id": self.branch_id,
            "head": dict(head) if head is not None else None,
            "schema_sha256": sha_file(SCHEMA),
            "tables": sorted(
                row[0]
                for row in self.conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                )
            ),
        }


class MirrorStore:
    """TEST_ONLY C12-side actor projection and exact watermark store."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.conn = _connect(self.path, MIRROR_SCHEMA)

    def add_root_branch(
        self,
        *,
        c12_branch_id: str,
        actor_id: str,
        actor_branch_epoch: str,
        c12_root_hash: str,
        c12_created_clock: int,
        admin_now: int = NOW,
    ) -> None:
        """Add one root mirror branch with an empty base set."""
        _insert(
            self.conn,
            "mirror_branch",
            {
                "c12_branch_id": c12_branch_id,
                "actor_id": actor_id,
                "actor_branch_epoch": actor_branch_epoch,
                "c12_parent_branch_id": None,
                "c12_root_hash": c12_root_hash,
                "c12_fork_clock": None,
                "c12_created_clock": c12_created_clock,
                "c9_start_seq": 0,
                "c9_start_receipt_hash": None,
                "base_c12_branch_id": None,
                "base_c12_root_hash": None,
                "base_c12_perception_hash": None,
                "base_c12_perception_count": 0,
                "mirror_state": "ROOT_READY",
                "created_admin_us": admin_now,
            },
        )
        _insert(
            self.conn,
            "mirror_watermark",
            {
                "c12_branch_id": c12_branch_id,
                "last_seq": 0,
                "last_receipt_hash": None,
                "last_projection_hash": None,
                "watermark_state": "CLEAN",
                "updated_admin_us": admin_now,
            },
        )

    def add_fork_branch(
        self,
        *,
        c12_branch_id: str,
        actor_id: str,
        actor_branch_epoch: str,
        c12_parent_branch_id: str,
        c12_root_hash: str,
        c12_fork_clock: int,
        c12_created_clock: int,
        c9_start_seq: int,
        c9_start_receipt_hash: str | None,
        base_c12_root_hash: str,
        base_c12_perception_hash: str,
        base_c12_perception_count: int,
        mirror_state: str = "FORK_HELD",
        admin_now: int = NOW,
    ) -> None:
        """Add one fork mirror branch with exact base perception identity."""
        _refuse(
            mirror_state in ("FORK_READY", "FORK_HELD", "MIRROR_HELD"),
            "MIRROR_FORK_STATE_INVALID",
        )
        _refuse(base_c12_perception_hash != "", "BASE_PERCEPTION_HASH_REQUIRED")
        _insert(
            self.conn,
            "mirror_branch",
            {
                "c12_branch_id": c12_branch_id,
                "actor_id": actor_id,
                "actor_branch_epoch": actor_branch_epoch,
                "c12_parent_branch_id": c12_parent_branch_id,
                "c12_root_hash": c12_root_hash,
                "c12_fork_clock": c12_fork_clock,
                "c12_created_clock": c12_created_clock,
                "c9_start_seq": c9_start_seq,
                "c9_start_receipt_hash": c9_start_receipt_hash,
                "base_c12_branch_id": c12_parent_branch_id,
                "base_c12_root_hash": base_c12_root_hash,
                "base_c12_perception_hash": base_c12_perception_hash,
                "base_c12_perception_count": base_c12_perception_count,
                "mirror_state": mirror_state,
                "created_admin_us": admin_now,
            },
        )
        _insert(
            self.conn,
            "mirror_watermark",
            {
                "c12_branch_id": c12_branch_id,
                "last_seq": c9_start_seq,
                "last_receipt_hash": c9_start_receipt_hash,
                "last_projection_hash": (
                    sha({"fork_start": c12_branch_id}) if c9_start_seq > 0 else None
                ),
                "watermark_state": (
                    "CLEAN" if mirror_state == "FORK_READY" else "FORK_HELD"
                ),
                "updated_admin_us": admin_now,
            },
        )

    def hold_watermark(self, c12_branch_id: str, state: str) -> None:
        """Set a held watermark to exercise fail-closed consumers."""
        _refuse(
            state in ("CLEAN", "SYNC_HELD", "MIRROR_CONFLICT", "FORK_HELD"),
            "WATERMARK_STATE_INVALID",
        )
        self.conn.execute(
            "UPDATE mirror_watermark SET watermark_state=?,updated_admin_us=? "
            "WHERE c12_branch_id=?",
            (state, NOW, c12_branch_id),
        )

    def project(
        self,
        authority: ActorAuthority,
        receipt_hash: str,
        *,
        c12_root_hash: str,
        c12_last_clock: int,
        projection: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Project one committed actor receipt after C9; never rerun Rule T."""
        receipt = authority.conn.execute(
            "SELECT * FROM decision_receipt WHERE receipt_hash=?", (receipt_hash,)
        ).fetchone()
        _refuse(receipt is not None, "RECEIPT_MISSING")
        _refuse(
            receipt["actor_id"] == authority.actor_id
            and receipt["branch_id"] == authority.branch_id
            and receipt["branch_epoch"] == authority.branch_epoch,
            "RECEIPT_SCOPE_MISMATCH",
        )
        branch = self.conn.execute(
            "SELECT * FROM mirror_branch WHERE c12_branch_id=?",
            (authority.c12_branch_id,),
        ).fetchone()
        _refuse(branch is not None, "MIRROR_BRANCH_MISSING")
        _refuse(
            branch["actor_id"] == authority.actor_id
            and branch["actor_branch_epoch"] == authority.branch_epoch,
            "MIRROR_BRANCH_SCOPE_MISMATCH",
        )
        watermark = self.conn.execute(
            "SELECT * FROM mirror_watermark WHERE c12_branch_id=?",
            (authority.c12_branch_id,),
        ).fetchone()
        _refuse(watermark is not None, "MIRROR_WATERMARK_MISSING")
        _refuse(watermark["watermark_state"] == "CLEAN", "SYNC_HELD")
        _refuse(branch["c12_root_hash"] == c12_root_hash, "C12_ROOT_MISMATCH")
        projection_body = dict(
            projection
            or {
                "c9_receipt_hash": receipt_hash,
                "c9_decision_kind": receipt["decision_kind"],
                "c9_actor_version_hash": receipt["result_version_hash"],
                "c9_semantic_hash": receipt["after_semantic_hash"],
            }
        )
        projection_hash = sha(projection_body)
        existing = self.conn.execute(
            "SELECT * FROM mirror_receipt WHERE c12_branch_id=? AND c9_seq=?",
            (authority.c12_branch_id, receipt["commit_seq"]),
        ).fetchone()
        if existing is not None:
            _refuse(
                existing["c9_receipt_hash"] == receipt_hash
                and existing["projection_hash"] == projection_hash,
                "MIRROR_CONFLICT",
            )
            _refuse(
                int(watermark["last_seq"]) >= int(receipt["commit_seq"]),
                "MIRROR_WATERMARK_REGRESSION",
            )
            replayed = True
        else:
            _refuse(
                int(receipt["commit_seq"]) == int(watermark["last_seq"]) + 1,
                "MIRROR_SEQ_GAP",
            )
            self.conn.execute("BEGIN IMMEDIATE")
            try:
                _insert(
                    self.conn,
                    "mirror_receipt",
                    {
                        "c12_branch_id": authority.c12_branch_id,
                        "c9_seq": receipt["commit_seq"],
                        "c9_receipt_hash": receipt_hash,
                        "c9_actor_version_hash": receipt["result_version_hash"],
                        "c9_decision_kind": receipt["decision_kind"],
                        "c9_semantic_hash": receipt["after_semantic_hash"],
                        "projection_hash": projection_hash,
                        "canonical_projection_json": canon(projection_body),
                        "c12_root_hash": c12_root_hash,
                        "c12_last_clock": c12_last_clock,
                        "c8_world_receipt_hash": receipt["world_receipt_hash"],
                        "created_admin_us": NOW,
                    },
                )
                self.conn.execute(
                    "UPDATE mirror_watermark SET last_seq=?,last_receipt_hash=?,"
                    "last_projection_hash=?,updated_admin_us=? WHERE c12_branch_id=?",
                    (
                        receipt["commit_seq"],
                        receipt_hash,
                        projection_hash,
                        NOW,
                        authority.c12_branch_id,
                    ),
                )
                self.conn.execute("COMMIT")
            except BaseException:
                if self.conn.in_transaction:
                    self.conn.execute("ROLLBACK")
                raise
            replayed = False
        outbox = authority.conn.execute(
            "SELECT * FROM projection_outbox WHERE receipt_hash=?", (receipt_hash,)
        ).fetchone()
        _refuse(outbox is not None, "OUTBOX_MISSING")
        if outbox["projection_state"] != "ACKED":
            if (
                outbox["projected_c12_hash"] is not None
                and outbox["projected_c12_hash"] != projection_hash
            ):
                raise Refusal("MIRROR_CONFLICT", "OUTBOX_PROJECTION_MISMATCH")
            authority.conn.execute("BEGIN IMMEDIATE")
            try:
                authority.conn.execute(
                    "UPDATE projection_outbox SET projection_state='PROJECTED',"
                    "projected_c12_hash=?,"
                    "attempt_count=attempt_count+CASE "
                    "WHEN projection_state='PENDING' THEN 1 ELSE 0 END,"
                    "last_error_code=NULL WHERE receipt_hash=? "
                    "AND projection_state IN ('PENDING','PROJECTED')",
                    (projection_hash, receipt_hash),
                )
                authority.conn.execute("COMMIT")
            except BaseException:
                if authority.conn.in_transaction:
                    authority.conn.execute("ROLLBACK")
                raise
        return {
            "state": "CLEAN",
            "replayed": replayed,
            "projection_hash": projection_hash,
        }

    def ack(self, authority: ActorAuthority, receipt_hash: str) -> dict[str, Any]:
        """Acknowledge an already projected and cleanly watermarked receipt."""
        row = authority.conn.execute(
            "SELECT * FROM projection_outbox WHERE receipt_hash=?", (receipt_hash,)
        ).fetchone()
        _refuse(row is not None, "OUTBOX_MISSING")
        if row["projection_state"] == "ACKED":
            return {"state": "ACKED", "replayed": True}
        _refuse(row["projection_state"] == "PROJECTED", "ACK_REQUIRES_PROJECTED")
        mirror = self.conn.execute(
            "SELECT * FROM mirror_receipt WHERE c12_branch_id=? AND c9_receipt_hash=?",
            (authority.c12_branch_id, receipt_hash),
        ).fetchone()
        _refuse(mirror is not None, "ACK_REQUIRES_MIRROR")
        _refuse(
            mirror["projection_hash"] == row["projected_c12_hash"],
            "ACK_PROJECTION_MISMATCH",
        )
        watermark = self.conn.execute(
            "SELECT * FROM mirror_watermark WHERE c12_branch_id=?",
            (authority.c12_branch_id,),
        ).fetchone()
        _refuse(
            watermark is not None
            and watermark["watermark_state"] == "CLEAN"
            and int(watermark["last_seq"]) >= int(mirror["c9_seq"]),
            "ACK_REQUIRES_CLEAN_WATERMARK",
        )
        authority.conn.execute(
            "UPDATE projection_outbox SET projection_state='ACKED',"
            "acked_admin_us=?,attempt_count=attempt_count+1 WHERE receipt_hash=?",
            (NOW, receipt_hash),
        )
        return {"state": "ACKED", "replayed": False}

    def status(self, authority: ActorAuthority, receipt_hash: str) -> dict[str, Any]:
        """Return CLEAN only for exact projected, watermarked and ACKed receipt."""
        outbox = authority.conn.execute(
            "SELECT * FROM projection_outbox WHERE receipt_hash=?", (receipt_hash,)
        ).fetchone()
        if outbox is None:
            return {"state": "SYNC_HELD", "code": "OUTBOX_MISSING"}
        mirror = self.conn.execute(
            "SELECT * FROM mirror_receipt WHERE c12_branch_id=? AND c9_receipt_hash=?",
            (authority.c12_branch_id, receipt_hash),
        ).fetchone()
        watermark = self.conn.execute(
            "SELECT * FROM mirror_watermark WHERE c12_branch_id=?",
            (authority.c12_branch_id,),
        ).fetchone()
        if watermark is None:
            return {"state": "SYNC_HELD", "code": "MIRROR_WATERMARK_MISSING"}
        if watermark["watermark_state"] != "CLEAN":
            return {"state": "SYNC_HELD", "code": watermark["watermark_state"]}
        if mirror is None:
            return {"state": "SYNC_HELD", "code": "MIRROR_RECEIPT_MISSING"}
        if int(watermark["last_seq"]) < int(mirror["c9_seq"]):
            return {"state": "SYNC_HELD", "code": "MIRROR_WATERMARK_BEHIND"}
        if int(watermark["last_seq"]) == int(mirror["c9_seq"]):
            if (
                watermark["last_receipt_hash"] != mirror["c9_receipt_hash"]
                or watermark["last_projection_hash"] != mirror["projection_hash"]
            ):
                return {"state": "MIRROR_CONFLICT", "code": "WATERMARK_MISMATCH"}
        if outbox["projected_c12_hash"] != mirror["projection_hash"]:
            return {"state": "MIRROR_CONFLICT", "code": "PROJECTION_MISMATCH"}
        if outbox["projection_state"] != "ACKED":
            return {"state": "SYNC_HELD", "code": outbox["projection_state"]}
        return {"state": "CLEAN", "code": "CLEAN"}

    def verify(self) -> dict[str, Any]:
        """Check exact mirror receipt, watermark and branch state."""
        errors: list[str] = []
        for branch in self.conn.execute("SELECT * FROM mirror_branch").fetchall():
            branch_id = branch["c12_branch_id"]
            watermark = self.conn.execute(
                "SELECT * FROM mirror_watermark WHERE c12_branch_id=?",
                (branch_id,),
            ).fetchone()
            if watermark is None:
                errors.append("watermark_missing:" + branch_id)
                continue
            if watermark["watermark_state"] != "CLEAN":
                if branch["mirror_state"] == "FORK_READY":
                    errors.append("fork_ready_watermark_not_clean:" + branch_id)
                continue
            receipts = self.conn.execute(
                "SELECT c9_seq,c9_receipt_hash,projection_hash FROM mirror_receipt "
                "WHERE c12_branch_id=? ORDER BY c9_seq",
                (branch_id,),
            ).fetchall()
            expected = int(branch["c9_start_seq"]) + 1
            for receipt in receipts:
                if int(receipt["c9_seq"]) != expected:
                    errors.append(f"mirror_seq_gap:{branch_id}:{receipt['c9_seq']}")
                expected = int(receipt["c9_seq"]) + 1
            if int(watermark["last_seq"]) > int(branch["c9_start_seq"]):
                last = receipts[-1] if receipts else None
                if last is None:
                    errors.append("watermark_without_receipt:" + branch_id)
                elif (
                    int(last["c9_seq"]) != int(watermark["last_seq"])
                    or last["c9_receipt_hash"] != watermark["last_receipt_hash"]
                    or last["projection_hash"] != watermark["last_projection_hash"]
                ):
                    errors.append("watermark_receipt_mismatch:" + branch_id)
        return {
            "ok": not errors,
            "errors": errors,
            "branches": self.conn.execute(
                "SELECT count(*) FROM mirror_branch"
            ).fetchone()[0],
            "receipts": self.conn.execute(
                "SELECT count(*) FROM mirror_receipt"
            ).fetchone()[0],
            "schema_sha256": sha_file(MIRROR_SCHEMA),
        }


def c12_fork_guard(
    c12_path: str | Path,
    parent_branch_id: str,
    *,
    expected_base_perception_hash: str | None = None,
    expected_base_root_hash: str | None = None,
    mirror_state: str | None = None,
) -> dict[str, Any]:
    """Return FORK_HELD for an incomplete or unproven perception cut; never CLEAN."""
    path = Path(c12_path)
    conn: sqlite3.Connection | None = None
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            meta = dict(conn.execute("SELECT key,value FROM meta").fetchall())
        except sqlite3.Error as error:
            return {
                "state": "FORK_HELD",
                "code": "C12_SCHEMA_META_UNREADABLE",
                "detail": str(error),
            }
        writer_schema = meta.get("schema")
        if writer_schema not in SUPPORTED_C12_WRITER_SCHEMAS:
            return {
                "state": "FORK_HELD",
                "code": "C12_WRITER_SCHEMA_UNSUPPORTED",
                "writer_schema": writer_schema,
                "supported_writer_schemas": sorted(SUPPORTED_C12_WRITER_SCHEMAS),
            }
        user_version = conn.execute("PRAGMA user_version").fetchone()[0]
        application_id = conn.execute("PRAGMA application_id").fetchone()[0]
        if user_version != 0:
            return {
                "state": "FORK_HELD",
                "code": "C12_SQLITE_USER_VERSION_UNSUPPORTED",
                "user_version": int(user_version),
            }
        if application_id != 0:
            return {
                "state": "FORK_HELD",
                "code": "C12_SQLITE_APPLICATION_ID_UNSUPPORTED",
                "application_id": int(application_id),
            }
        branch = conn.execute(
            "SELECT * FROM branch WHERE branch_id=?", (parent_branch_id,)
        ).fetchone()
        if branch is None:
            return {"state": "FORK_HELD", "code": "C12_BRANCH_MISSING"}
        actual_base_root_hash = str(branch["root_hash"] or "")
        if (
            expected_base_root_hash is not None
            and actual_base_root_hash != expected_base_root_hash
        ):
            return {
                "state": "FORK_HELD",
                "code": "C12_BASE_ROOT_MISMATCH",
                "base_root_hash": actual_base_root_hash,
            }
        nonperception = [0]
        for table in ("episode", "world_event", "checkpoint"):
            row = conn.execute(
                f"SELECT max(clock) FROM {table} WHERE branch_id=?",
                (parent_branch_id,),
            ).fetchone()
            if row is not None and row[0] is not None:
                nonperception.append(int(row[0]))
        perception_rows = conn.execute(
            "SELECT seq,actor_id,event_id,clock,channel FROM perception "
            "WHERE branch_id=? ORDER BY seq",
            (parent_branch_id,),
        ).fetchall()
        perception_clocks = [int(row["clock"]) for row in perception_rows]
        perception_max = max(perception_clocks, default=0)
        cut = max(max(nonperception), perception_max)
        perception_hash = sha([dict(row) for row in perception_rows])
        if perception_max > max(nonperception):
            return {
                "state": "FORK_HELD",
                "code": "C12_PERCEPTION_ONLY_SUFFIX",
                "fork_cut": cut,
                "nonperception_last_clock": max(nonperception),
                "perception_last_clock": perception_max,
                "base_root_hash": actual_base_root_hash,
                "base_perception_hash": perception_hash,
                "base_perception_count": len(perception_rows),
            }
        if expected_base_perception_hash is None:
            return {
                "state": "FORK_HELD",
                "code": "C12_BASE_PERCEPTION_IDENTITY_UNPROVEN",
                "fork_cut": cut,
                "base_root_hash": actual_base_root_hash,
                "base_perception_hash": perception_hash,
                "base_perception_count": len(perception_rows),
            }
        if expected_base_perception_hash != perception_hash:
            return {
                "state": "FORK_HELD",
                "code": "C12_BASE_PERCEPTION_IDENTITY_MISMATCH",
                "fork_cut": cut,
                "base_root_hash": actual_base_root_hash,
                "base_perception_hash": perception_hash,
                "base_perception_count": len(perception_rows),
            }
        if mirror_state is not None and mirror_state != "CLEAN":
            return {
                "state": "FORK_HELD",
                "code": "C12_MIRROR_NOT_CLEAN",
                "fork_cut": cut,
                "mirror_state": mirror_state,
                "base_root_hash": actual_base_root_hash,
            }
        return {
            "state": "FORK_READY",
            "code": "FORK_READY",
            "fork_cut": cut,
            "nonperception_last_clock": max(nonperception),
            "perception_last_clock": perception_max,
            "base_root_hash": actual_base_root_hash,
            "base_perception_hash": perception_hash,
            "base_perception_count": len(perception_rows),
        }
    except sqlite3.Error as error:
        return {
            "state": "FORK_HELD",
            "code": "C12_READ_FAILED",
            "detail": str(error),
        }
    finally:
        if conn is not None:
            conn.close()


def schema_hashes() -> dict[str, str]:
    """Return exact DDL hashes for the return."""
    return {
        "schema_actor_r3.sql": sha_file(SCHEMA),
        "schema_mirror_r3.sql": sha_file(MIRROR_SCHEMA),
    }
