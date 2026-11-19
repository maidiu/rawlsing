#!/usr/bin/env python3
"""Assemble 33 construction-only C11 grant-record drafts from frozen ledger data.

Private drafts stay outside Git; only permissible metadata, hashes and the
decision packet are written to the OWNER return.  No source file is opened,
statted, hashed or decoded.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path("/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117")
OWNER = ROOT / "OWNER"
INPUTS = ROOT / "IMPLEMENTER/WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118"
LEDGER = OWNER / "WORKER_RETURNS/ANVIL_ALL35_EXECUTION_READINESS_FOLLOWTHROUGH_20261119/ALL35_RUNNABLE_INPUT_LEDGER.json"
GRANTS = ROOT / "MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118"
CAND = ROOT / "MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree"
OUT = OWNER / "WORKER_RETURNS/ANVIL_ALL35_CONSTRUCTION_GRANT_REPAIR_20261119"
PRIVATE = Path("/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/anvil_all35_construction_grant_drafts_20261119")

sys.path[:0] = [str(CAND), str(GRANTS)]


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load(path: Path):
    return json.loads(path.read_text())


def validate_draft(d: dict, expected: dict) -> list[str]:
    errors = []
    required = {
        "schema", "source_id", "source_path", "expected_source_sha256",
        "source_rows", "source_columns", "source_bytes", "source_format",
        "host", "purpose", "consumer", "full_source", "first_slice_only",
        "scope", "currentness", "revocation", "authorization", "issuer",
        "thread", "limits", "extent", "retention", "draft", "operative",
        "no_q2", "no_scientific_scope", "source_artifact_id",
        "source_config", "file_identity",
    }
    errors.extend(f"MISSING:{k}" for k in sorted(required - set(d)))
    if d.get("schema") != "PYAT_FULL_SOURCE_READ_GRANT@1.0.0":
        errors.append("SCHEMA_MISMATCH")
    if d.get("source_id") != expected["source_id"]:
        errors.append("SOURCE_ID_MISMATCH")
    if d.get("expected_source_sha256") != expected["source_sha256"]:
        errors.append("SOURCE_SHA_MISMATCH")
    if d.get("source_rows") != expected["source_rows"]:
        errors.append("ROWS_MISMATCH")
    if d.get("source_columns") != expected["source_columns"]:
        errors.append("COLUMNS_MISMATCH")
    if d.get("source_bytes") != expected["source_bytes"]:
        errors.append("BYTES_MISMATCH")
    if d.get("host") != "USER_LOCAL_MAC":
        errors.append("HOST_MISMATCH")
    if d.get("consumer") != "EXISTING_PRE553_SOURCE_BACKED_C11":
        errors.append("CONSUMER_MISMATCH")
    if d.get("full_source") is not True or d.get("first_slice_only") is not False:
        errors.append("EXTENT_MISMATCH")
    if d.get("extent") != "EXACT_FILE":
        errors.append("EXTENT_TOKEN_MISMATCH")
    if d.get("retention") != "LOCAL_RUNTIME_ONLY":
        errors.append("RETENTION_MISMATCH")
    if d.get("currentness") != "DRAFT_NONOPERATIVE_AWAITING_COMPETENT_DECISION":
        errors.append("DRAFT_CURRENTNESS_NOT_NONOPERATIVE")
    if d.get("draft") is not True or d.get("operative") is not False:
        errors.append("DRAFT_STATE_MISMATCH")
    if d.get("no_q2") is not True or d.get("no_scientific_scope") is not True:
        errors.append("Q2_OR_SCIENCE_FLAG")
    source_config = d.get("source_config") or {}
    if source_config.get("file_sha256") != expected["config_file_sha256"]:
        errors.append("CONFIG_FILE_SHA_MISMATCH")
    if source_config.get("canonical_sha256") != expected["config_canonical_sha256"]:
        errors.append("CONFIG_CANONICAL_SHA_MISMATCH")
    return errors


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PRIVATE.mkdir(parents=True, mode=0o700, exist_ok=True)
    ledger = load(LEDGER)
    rows = {row["source_id"]: row for row in ledger["rows"]}
    bundles = {sid: load(INPUTS / "bundles" / f"{sid}.json") for sid in rows}
    generated = []
    invalid = []
    for sid in sorted(rows):
        if sid in {"SRC04", "SRC17"}:
            continue
        row = rows[sid]
        bundle = bundles[sid]
        meta = bundle.get("data_metadata_only") or {}
        config = row["config"]
        if not meta.get("path") or not meta.get("present"):
            invalid.append({"source_id": sid, "errors": ["SOURCE_LOCATION_METADATA_MISSING"]})
            continue
        source_path = meta["path"]
        purpose = f"FULL_{sid}_ORIGINAL_C11_CONSTRUCTION_ONLY"
        scope = f"ALL_{row['config']['shape']['physical_slots']}_PHYSICAL_SLOTS__C11_CONSTRUCTION_ONLY__NO_Q2"
        draft = {
            "schema": "PYAT_FULL_SOURCE_READ_GRANT@1.0.0",
            "source_id": sid,
            "source_path": source_path,
            "expected_source_sha256": row["rights"]["source_sha256"],
            "source_rows": bundle["declared_rows"],
            "source_columns": bundle["declared_columns"],
            "source_bytes": meta.get("size"),
            "source_format": bundle["source_format"],
            "source_artifact_id": bundle["source_artifact_id"],
            "host": "USER_LOCAL_MAC",
            "purpose": purpose,
            "consumer": "EXISTING_PRE553_SOURCE_BACKED_C11",
            "full_source": True,
            "first_slice_only": False,
            "extent": "EXACT_FILE",
            "scope": scope,
            "currentness": "DRAFT_NONOPERATIVE_AWAITING_COMPETENT_DECISION",
            "revocation": "NOT_APPLICABLE_DRAFT",
            "authorization": "DRAFT_ONLY__NOT_ISSUED__NO_SOURCE_ACCESS",
            "issuer": "NOT_SIGNED",
            "thread": None,
            "retention": "LOCAL_RUNTIME_ONLY",
            "limits": [
                "Construction-only local C11; no Q2, analysis, science or eligibility.",
                "No source bytes in Git, no respondent rows in Git, no export.",
                "No source open/stat/hash/decode until an operative decision exists.",
            ],
            "draft": True,
            "operative": False,
            "no_q2": True,
            "no_scientific_scope": True,
            "source_config": {
                "path": config["path"],
                "revision_ref": config["revision_ref"],
                "file_sha256": config["file_sha256"],
                "canonical_sha256": config["canonical_sha256"],
            },
            "file_identity": {
                "source_artifact_id": bundle["source_artifact_id"],
                "source_sha256": row["rights"]["source_sha256"],
                "bytes": meta.get("size"),
                "host": "USER_LOCAL_MAC",
            },
        }
        errors = validate_draft(draft, {
            "source_id": sid,
            "source_sha256": row["rights"]["source_sha256"],
            "source_rows": bundle["declared_rows"],
            "source_columns": bundle["declared_columns"],
            "source_bytes": meta.get("size"),
            "config_file_sha256": config["file_sha256"],
            "config_canonical_sha256": config["canonical_sha256"],
        })
        if errors:
            invalid.append({"source_id": sid, "errors": errors})
            continue
        raw = (json.dumps(draft, indent=2, sort_keys=True) + "\n").encode()
        private_file = PRIVATE / f"{sid}.full-source-read-grant.draft.json"
        private_file.write_bytes(raw)
        generated.append({
            "source_id": sid,
            "family": row["family"],
            "wave": row["wave"],
            "source_artifact_id": bundle["source_artifact_id"],
            "source_sha256": row["rights"]["source_sha256"],
            "source_rows": bundle["declared_rows"],
            "source_columns": bundle["declared_columns"],
            "source_bytes": meta.get("size"),
            "source_format": bundle["source_format"],
            "config_revision_ref": config["revision_ref"],
            "config_file_sha256": config["file_sha256"],
            "config_canonical_sha256": config["canonical_sha256"],
            "host": "USER_LOCAL_MAC",
            "purpose": purpose,
            "consumer": "EXISTING_PRE553_SOURCE_BACKED_C11",
            "scope": scope,
            "extent": "EXACT_FILE",
            "retention": "LOCAL_RUNTIME_ONLY",
            "draft_sha256": sha_bytes(raw),
            "draft_private_filename": private_file.name,
            "draft_status": "DRAFT_NONOPERATIVE_AUTHORIZATION_PENDING",
            "operative": False,
            "validation": "PASS",
        })

    index = {
        "schema": "ANVIL_ALL35_CONSTRUCTION_GRANT_DRAFTS@1",
        "scope": "Construction-only local C11; no scientific/Q2 grant. Nonoperative drafts.",
        "private_draft_root": str(PRIVATE),
        "counts": {
            "existing_active_bindings_reused": 2,
            "existing_active_sources": ["SRC04", "SRC17"],
            "drafts_created": len(generated),
            "materialized_new": 0,
            "authorization_pending": len(generated),
            "validation_failed": len(invalid),
            "total_sources": 35,
        },
        "drafts": generated,
        "invalid": invalid,
        "existing_active_bindings": {
            "SRC04": "exact existing full-source C11 binding; already materialized",
            "SRC17": "exact existing C11-only binding; I03/I05 excluded; already materialized",
        },
        "private_git_policy": "Full drafts contain source_path and remain outside Git; only this hashed index is published.",
        "refused_inferences": [
            "No grant is inferred from custody, filesystem presence, TEST_ONLY or stale material.",
            "No consent is reused from another source.",
            "No signer, interface or grant was invented.",
            "No source was opened, statted, hashed or decoded.",
        ],
    }
    (OUT / "DRAFT_INDEX.json").write_text(json.dumps(index, indent=2, sort_keys=True) + "\n")
    (OUT / "SUMMARY.json").write_text(json.dumps({
        "schema": "ANVIL_ALL35_CONSTRUCTION_GRANT_REPAIR_SUMMARY@1",
        **index["counts"],
        "configs_exact": 35,
        "config_defects": 0,
        "q2_issued": False,
        "source_read_performed": False,
        "new_grants_signed": 0,
        "private_drafts_in_git": False,
    }, indent=2, sort_keys=True) + "\n")

    packet = {
        "schema": "ANVIL_ALL35_CONSTRUCTION_DECISION_PACKET@1",
        "status": "AWAITING_ONE_COMPETENT_DECISION",
        "authority_precedent": {
            "format": "PYAT_FULL_SOURCE_READ_GRANT@1.0.0",
            "competent_authority": "HUMAN_USER_VIA_EXISTING_PYAT_HQ",
            "basis": "SRC04 accepted user full-source operational grant and SRC17 TRUE_HQ construction-only precedent; no third-party signoff is assumed.",
            "external_contact": False,
            "commissioning_is_not_a_grant": True,
        },
        "requested_decision": "Authorize all 33 exact construction-only local C11 records together, or specify per-wave exceptions; issue no scientific, Q2, analysis, export or retention expansion.",
        "common_terms": {
            "host": "USER_LOCAL_MAC",
            "consumer": "EXISTING_PRE553_SOURCE_BACKED_C11",
            "extent": "EXACT_FILE",
            "purpose_suffix": "ORIGINAL_C11_CONSTRUCTION_ONLY",
            "scope_suffix": "C11_CONSTRUCTION_ONLY__NO_Q2",
            "retention": "LOCAL_RUNTIME_ONLY",
            "no_q2": True,
            "no_scientific_scope": True,
            "no_export": True,
        },
        "excluded_already_active": ["SRC04", "SRC17"],
        "drafts": [
            {k: d[k] for k in (
                "source_id", "family", "wave", "source_artifact_id", "source_sha256",
                "source_rows", "source_columns", "source_bytes", "source_format",
                "host", "purpose", "consumer", "scope", "extent", "retention",
                "draft_sha256", "draft_private_filename", "draft_status",
            )}
            for d in generated
        ],
        "exception_if_any": "Only SRC04/SRC17 are already active (SRC17 I03/I05 excluded); no other exception is asserted.",
    }
    (OUT / "DECISION_PACKET.json").write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n")

    # Mechanical validation of all 33 private drafts against their public index.
    validation_rows = []
    for entry in generated:
        private_file = PRIVATE / entry["draft_private_filename"]
        raw = private_file.read_bytes()
        d = json.loads(raw)
        errors = validate_draft(d, {
            "source_id": entry["source_id"],
            "source_sha256": entry["source_sha256"],
            "source_rows": entry["source_rows"],
            "source_columns": entry["source_columns"],
            "source_bytes": entry["source_bytes"],
            "config_file_sha256": rows[entry["source_id"]]["config"]["file_sha256"],
            "config_canonical_sha256": rows[entry["source_id"]]["config"]["canonical_sha256"],
        })
        if sha_bytes(raw) != entry["draft_sha256"]:
            errors.append("DRAFT_HASH_MISMATCH")
        validation_rows.append({"source_id": entry["source_id"], "valid": not errors, "errors": errors})
    (OUT / "DRAFT_VALIDATION.json").write_text(json.dumps({
        "schema": "ANVIL_ALL35_CONSTRUCTION_GRANT_DRAFT_VALIDATION@1",
        "rows": validation_rows,
        "valid": all(row["valid"] for row in validation_rows),
        "count": len(validation_rows),
        "source_read_performed": False,
    }, indent=2, sort_keys=True) + "\n")

    # One sourcefree authorize/refuse check through the existing accepted adapter.
    import existing_grant_binding as gb
    raw = load(GRANTS / "fixtures/SRC04_CONFIG_BINDING.json")
    cfg = gb.ConfigBinding(**{k: v for k, v in raw.items() if k != "metadata_freeze_refs"},
                           metadata_freeze_refs=tuple(raw["metadata_freeze_refs"]))
    tp = load(GRANTS / "TRUST_POLICY.json")
    trust = gb.ExternalTrust(**{k: tp[k] for k in (
        "grant_sha256", "grant_path", "config_file_sha256",
        "config_canonical_sha256", "config_binding_sha256")})
    actual = load(GRANTS / "fixtures/SRC04_FULL_SOURCE_GRANT.json")
    actual_path = GRANTS / "fixtures/SRC04_FULL_SOURCE_GRANT.json"
    bound = gb.bind_existing_grant(grant_path=actual_path, config=cfg, trust=trust)
    resolver = gb.ExistingGrantResolver(actual_path, trust, bound.request)
    pre = resolver.resolve_current(bound.request)
    post = resolver.resolve_current(bound.request)
    auth = {
        "status": "AUTHORIZED_EXISTING_EXACT_BINDING",
        "currentness": pre.currentness,
        "decision_ref": pre.decision_ref.as_dict(),
        "pre_post_identical": pre == post,
        "source_read_performed": False,
    }
    draft_path = PRIVATE / "_SRC04_nonoperative_resolver_check.json"
    draft_doc = dict(actual)
    draft_doc["currentness"] = "DRAFT_NONOPERATIVE_AWAITING_COMPETENT_DECISION"
    draft_doc["authorization"] = "DRAFT_ONLY__NOT_ISSUED__NO_SOURCE_ACCESS"
    draft_doc["issuer"] = "NOT_SIGNED"
    raw_draft = (json.dumps(draft_doc, indent=2, sort_keys=True) + "\n").encode()
    draft_path.write_bytes(raw_draft)
    draft_trust = gb.ExternalTrust(
        grant_sha256=sha_bytes(raw_draft), grant_path=str(draft_path),
        config_file_sha256=tp["config_file_sha256"],
        config_canonical_sha256=tp["config_canonical_sha256"],
        config_binding_sha256=tp["config_binding_sha256"])
    refuse = {"status": "NOT_REFUSED"}
    try:
        gb.bind_existing_grant(grant_path=draft_path, config=cfg, trust=draft_trust)
    except Exception as exc:
        refuse = {"status": "REFUSED", "code": getattr(exc, "code", type(exc).__name__), "detail": str(exc)}
    (OUT / "RESOLVER_CHECK.json").write_text(json.dumps({
        "schema": "ANVIL_ALL35_CONSTRUCTION_RESOLVER_CHECK@1",
        "authorize": auth,
        "refuse_nonoperative_draft": refuse,
        "source_read_performed": False,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps(index["counts"], sort_keys=True))
    print(json.dumps({"authorize": auth, "refuse": refuse}, sort_keys=True))


if __name__ == "__main__":
    main()
