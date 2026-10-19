"""A41 versioned native receipt ingestion protocol.

A receipt is only accepted when every artifact it names re-materialises from the
shared Git object store at its exact commit/path with matching blob SHA-1 and
byte SHA-256. Nothing is trusted from the receipt's own text.

Protocol versions:
  A41_NATIVE_RECEIPT@1.0.0   current accepted producer bank
  A41_NATIVE_RECEIPT@1.1.0   reserved for exact E41/W41/P41 returns (slots pending)

A receipt's ``coverage`` says which frozen-scope cells it actually occupies and
at which occupancy kind. Occupancy kinds are NOT interchangeable: a sourcefree
local positive can never satisfy an original measured occupancy cell.
"""
from __future__ import annotations

import json
from pathlib import Path

from .gitpreimage import GitPreimage, PreimageError

RECEIPT_SCHEMA = "A41_NATIVE_RECEIPT@1.0.0"
BANK_SCHEMA = "A41_RECEIPT_BANK@1.0.0"

# Occupancy kinds, strongest first. These are deliberately non-substitutable.
OCCUPANCY_KINDS = (
    "ORIGINAL_MEASURED_OCCUPANCY",           # requires independently issued U/E_pre
    "HISTORICAL_SCOPE_POSITIVE",             # historical receipt at a bounded scope
    "EMPIRICAL_NULL_WITH_CAUSE",             # measured null, cause recorded, never fake zero
    "SOURCEFREE_LOCAL_POSITIVE",             # method/owner local positive, NOT original occupancy
    "DOCUMENTARY_IDENTITY_RECONCILIATION",   # identity census / accounting only
    "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER", # narrow owner, precise stop
    "SOURCE_INTRINSIC_NONAPPLICABILITY_PROVED",
)

# Only these two kinds can ever satisfy an ORIGINAL_ESTATE_OCCUPANCY cell.
ORIGINALLY_ADMISSIBLE = ("ORIGINAL_MEASURED_OCCUPANCY",)

REQUIRED_RECEIPT_FIELDS = (
    "schema", "receipt_id", "receipt_kind", "origin_commit", "claim_id",
    "claim_grain", "occupancy_kind", "evidence_state", "proof_grade",
    "artifacts", "coverage", "limitations", "currentness",
)


class ReceiptRefusal(ValueError):
    """Typed refusal at the ingestion boundary; never a silent fallback."""


def _require(cond, code):
    if not cond:
        raise ReceiptRefusal(code)


def validate_receipt_shape(receipt: dict) -> None:
    _require(isinstance(receipt, dict), "NOT_A_RECEIPT_OBJECT")
    for field in REQUIRED_RECEIPT_FIELDS:
        _require(field in receipt and receipt[field] not in (None, "", []),
                 f"RECEIPT_MISSING_FIELD:{field}")
    _require(receipt["schema"] == RECEIPT_SCHEMA,
             f"RECEIPT_SCHEMA_UNSUPPORTED:{receipt['schema']}")
    _require(receipt["occupancy_kind"] in OCCUPANCY_KINDS,
             f"RECEIPT_UNKNOWN_OCCUPANCY_KIND:{receipt['occupancy_kind']}")
    _require(isinstance(receipt["artifacts"], list) and receipt["artifacts"],
             "RECEIPT_HAS_NO_ARTIFACTS")
    _require("downstream_consumer_read_refs" in receipt
             and isinstance(receipt["downstream_consumer_read_refs"], list),
             "RECEIPT_MISSING_CONSUMER_READ_REFS_KEY")
    cov = receipt["coverage"]
    _require(isinstance(cov, dict), "RECEIPT_COVERAGE_NOT_OBJECT")
    for key in ("wave_ids", "axis_ids", "register_151_ids", "ledger_101_ids",
                "global_relations", "occupancy_grain_note"):
        _require(key in cov, f"RECEIPT_COVERAGE_MISSING:{key}")
    _require(isinstance(cov["wave_ids"], list), "RECEIPT_WAVE_IDS_NOT_LIST")
    _require(isinstance(cov["axis_ids"], list), "RECEIPT_AXIS_IDS_NOT_LIST")


def ingest_receipt(receipt: dict, gp: GitPreimage, *, expected_scope=None) -> dict:
    """Verify one receipt against the object store and against the frozen scope.

    Returns an ``ingested`` record carrying the verified preimages. Raises
    ``ReceiptRefusal`` on any shape, preimage or scope failure.
    """
    validate_receipt_shape(receipt)
    commit = receipt["origin_commit"]
    verified = []
    for art in receipt["artifacts"]:
        _require(isinstance(art, dict) and "path" in art, "ARTIFACT_SHAPE_INVALID")
        rec = gp.verify(commit, art["path"],
                        expect_blob_sha1=art.get("blob_sha1"),
                        expect_sha256=art.get("sha256"),
                        expect_bytes=art.get("bytes"))
        verified.append(rec)

    # Fail closed if the receipt claims a scope cell the frozen universe lacks.
    if expected_scope is not None:
        known_waves = {w["source_id"] for w in expected_scope["waves"]}
        known_axes = set(expected_scope["axis_ids"])
        known_reg = expected_scope.get("register_151_ids") or set()
        known_led = expected_scope.get("ledger_101_ids") or set()
        for wid in receipt["coverage"]["wave_ids"]:
            _require(wid in known_waves, f"RECEIPT_UNKNOWN_WAVE_ID:{wid}")
        for aid in receipt["coverage"]["axis_ids"]:
            _require(aid in known_axes, f"RECEIPT_UNKNOWN_AXIS_ID:{aid}")
        for rid in receipt["coverage"]["register_151_ids"]:
            if known_reg:
                _require(rid in known_reg, f"RECEIPT_UNKNOWN_REGISTER_ID:{rid}")
        for lid in receipt["coverage"]["ledger_101_ids"]:
            if known_led:
                _require(lid in known_led, f"RECEIPT_UNKNOWN_LEDGER_ID:{lid}")

    # An ORIGINAL_MEASURED occupancy claim must carry an issued U/E_pre authority.
    if receipt["occupancy_kind"] in ORIGINALLY_ADMISSIBLE:
        _require(receipt["coverage"]["wave_ids"],
                 "ORIGINAL_OCCUPANCY_WITH_EMPTY_WAVE_SCOPE")
        _require(receipt.get("independent_u_e_pre_authority"),
                 "ORIGINAL_OCCUPANCY_WITHOUT_ISSUED_U_E_PRE")
        # Anti-promotion: the frozen expected scope says whether U/E_pre is issued.
        if expected_scope is not None:
            wmap = expected_scope.get("wave_expected_u_e_pre", {})
            for wid in receipt["coverage"]["wave_ids"]:
                status = wmap.get(wid)
                if status != "ISSUED_AND_RECONCILED":
                    raise ReceiptRefusal(
                        f"FALSE_PROMOTION_SOURCEFREE_TO_ORIGINAL_OCCUPANCY:{wid}:{status}")

    # Declared consumer registry: a receipt may not claim an unknown consumer read.
    if expected_scope is not None:
        declared = set(expected_scope.get("declared_consumers", []))
        if declared:
            for ref in receipt.get("downstream_consumer_read_refs", []):
                _require(str(ref) in declared,
                         f"RECEIPT_UNKNOWN_OR_FORGED_CONSUMER_REF:{ref}")

    # Archive/current/clock consistency.
    cn = receipt.get("currentness")
    _require(isinstance(cn, dict), "RECEIPT_MISSING_CURRENTNESS")
    _require(cn.get("archive_or_current") in ("ARCHIVE", "CURRENT"),
             f"RECEIPT_BAD_CURRENTNESS_KIND:{cn.get('archive_or_current')}")
    _require(isinstance(cn.get("as_of"), str) and len(cn["as_of"]) >= 10,
             "RECEIPT_MISSING_AS_OF")
    if expected_scope is not None:
        clock = expected_scope.get("declared_clock")
        if clock is not None:
            _require(cn["as_of"] <= clock,
                     f"RECEIPT_CURRENTNESS_CLOCK_VIOLATION:{cn['as_of']}>{clock}")
    if cn.get("archive_or_current") == "CURRENT":
        _require(receipt["occupancy_kind"] != "HISTORICAL_SCOPE_POSITIVE",
                 "CURRENT_RECEIPT_CANNOT_CARRY_HISTORICAL_ONLY_GRADE")

    return {
        "receipt_id": receipt["receipt_id"],
        "receipt_kind": receipt["receipt_kind"],
        "origin_commit": commit,
        "claim_id": receipt["claim_id"],
        "claim_grain": receipt["claim_grain"],
        "occupancy_kind": receipt["occupancy_kind"],
        "evidence_state": receipt["evidence_state"],
        "proof_grade": receipt["proof_grade"],
        "coverage": receipt["coverage"],
        "limitations": receipt["limitations"],
        "unknown_bounds": receipt.get("unknown_bounds"),
        "method_source": receipt.get("method_source"),
        "currentness": receipt.get("currentness"),
        "producer_inputs": receipt.get("producer_inputs"),
        "releases": receipt.get("releases"),
        "native_test_ref": receipt.get("native_test_ref"),
        "replay_ref": receipt.get("replay_ref"),
        "downstream_consumer_read_refs": receipt.get("downstream_consumer_read_refs"),
        "verified_artifacts": verified,
        "ingestion_state": "VERIFIED_PREIMAGE_ACCEPTED",
    }


def ingest_bank(bank: dict, gp: GitPreimage, *, expected_scope=None) -> dict:
    """Ingest a whole receipt bank. Duplicate receipt ids are a refusal."""
    _require(bank.get("schema") == BANK_SCHEMA,
             f"BANK_SCHEMA_UNSUPPORTED:{bank.get('schema')}")
    _require(isinstance(bank.get("receipts"), list), "BANK_HAS_NO_RECEIPTS")
    seen = set()
    ingested = []
    for receipt in bank["receipts"]:
        _require(receipt["receipt_id"] not in seen,
                 f"BANK_DUPLICATE_RECEIPT_ID:{receipt['receipt_id']}")
        seen.add(receipt["receipt_id"])
        ingested.append(ingest_receipt(receipt, gp, expected_scope=expected_scope))
    return {
        "schema": BANK_SCHEMA,
        "bank_digest": bank.get("bank_digest"),
        "ingested_count": len(ingested),
        "ingested": ingested,
        "pending_slots": bank.get("pending_slots", []),
    }


# --------------------------------------------------------------------------
# E41/W41/P41 pending native output contracts (versioned, ready to consume)
# --------------------------------------------------------------------------
PENDING_RETURN_SLOTS = [
    {
        "slot_id": "E41",
        "campaign": "Full available empirical F1-F4 and N10E computation",
        "expected_native_output_contract": "A41_NATIVE_RECEIPT@1.1.0",
        "expected_artifact_kinds": ["computed_slice_evidence", "source_function_reachability_ledger"],
        "parent_nodes": ["N2", "N3", "N4", "N10E"],
        "state": "PENDING_RETURN__NOT_YET_AVAILABLE",
    },
    {
        "slot_id": "W41",
        "campaign": "Source-qualified objective structural, multifield and temporal world F5-F7/N9",
        "expected_native_output_contract": "A41_NATIVE_RECEIPT@1.1.0",
        "expected_artifact_kinds": ["selected_objective_world", "n9_current_historical_serving_receipt"],
        "parent_nodes": ["N5", "N6", "N7", "N8E", "N8S", "N9"],
        "state": "PENDING_RETURN__NOT_YET_AVAILABLE",
    },
    {
        "slot_id": "P41",
        "campaign": "Full generic N9->N10E->N10W progressive possibility service F8",
        "expected_native_output_contract": "A41_NATIVE_RECEIPT@1.1.0",
        "expected_artifact_kinds": ["progressive_possibility_service_receipt", "consumer_read_refs"],
        "parent_nodes": ["N10E", "N10W", "N11"],
        "state": "PENDING_RETURN__NOT_YET_AVAILABLE",
    },
]


def load_bank_file(path: Path) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ReceiptRefusal(f"BANK_FILE_UNREADABLE:{exc}") from exc
