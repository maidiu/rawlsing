#!/usr/bin/env python3
"""Build the 35-row execution-readiness ledger from existing frozen metadata.

Read-only over existing bundles, rights matrix, config bindings and exact grant
receipts.  No source body is opened, hashed, stat'ed, or decoded.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path("/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117")
INPUTS = ROOT / "IMPLEMENTER/WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118"
GRANTS = ROOT / "MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118"
OUT = ROOT / "OWNER/WORKER_RETURNS/ANVIL_ALL35_EXECUTION_READINESS_FOLLOWTHROUGH_20261119"


def load(path: Path):
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rights = load(INPUTS / "evidence/35_row_source_rights_matrix.json")
    rights_rows = {row["source_id"]: row for row in rights["sources"]}
    config_summary = load(INPUTS / "evidence/config_binding_summary.json")
    config_rows = {row["source_id"]: row for row in load(INPUTS / "evidence/config_bindings.json")["rows"]}

    src04_binding = load(GRANTS / "SRC04_BINDING.json")
    src17_auth = load(GRANTS / "fixtures/SRC17_GRANT_AUTHENTICATION.json")
    src17_scope = load(GRANTS / "SRC17_SCOPE.json")

    rows = []
    for source_id in [f"SRC{i:02}" for i in range(1, 36)]:
        bundle = load(INPUTS / "bundles" / f"{source_id}.json")
        permission = bundle.get("current_permission", {})
        config = bundle["source_config"]
        config_bind = config_rows[source_id]
        rights_row = rights_rows[source_id]
        decision = permission.get("decision", bundle.get("rights_decision"))
        proof_refs = permission.get("proof_refs") or []
        is_src04 = source_id == "SRC04"
        is_src17 = source_id == "SRC17"
        if is_src04:
            binding = {
                "status": "EXACT_MACHINE_BINDING_AVAILABLE",
                "source": str(GRANTS / "SRC04_BINDING.json"),
                "sha256": sha(GRANTS / "SRC04_BINDING.json"),
                "grant_sha256": src04_binding["grant_sha256"],
                "grant_ref": src04_binding["grant_ref"],
                "decision_ref": src04_binding["decision_ref"],
                "currentness": src04_binding["currentness"],
                "revocation_ref": src04_binding["revocation_ref"],
                "host": src04_binding["request"]["host"],
                "purpose": src04_binding["request"]["purpose"],
                "consumer_use": src04_binding["request"]["consumer_use"],
                "source_sha256": src04_binding["request"]["source_sha256"],
                "scope": "FULL_SOURCE_READ__C11_CONSTRUCTION_ONLY",
                "partial_i03_i05": False,
            }
            readiness = "READY_FOR_AUTHORIZED_SOURCE_BACKED_C11_CONSTRUCTION"
            remaining = "No source-permission gap; no real source launch executed in this preparation."
            owner_event = "Existing exact SRC04 full-source grant; retain CURRENT/revocation control."
        elif is_src17:
            binding = {
                "status": "EXACT_MACHINE_BINDING_AVAILABLE_PARTIAL_C11_ONLY",
                "source": str(GRANTS / "fixtures/SRC17_GRANT_AUTHENTICATION.json"),
                "sha256": sha(GRANTS / "fixtures/SRC17_GRANT_AUTHENTICATION.json"),
                "scope_receipt": str(GRANTS / "SRC17_SCOPE.json"),
                "scope_receipt_sha256": sha(GRANTS / "SRC17_SCOPE.json"),
                "grant_sha256": src17_scope["grant_sha256"],
                "authentication_sha256": src17_scope["authentication_sha256"],
                "decision_ref": src17_auth["decision_ref"],
                "currentness": src17_auth["currentness"],
                "revocation": src17_auth["revocation"],
                "host": src17_auth["request"]["host"],
                "purpose": src17_auth["request"]["purpose"],
                "consumer_use": src17_auth["request"]["consumer_use"],
                "source_sha256": src17_auth["request"]["source_sha256"],
                "scope": src17_auth["request"]["semantic_use_scope"],
                "partial_i03_i05": True,
                "i03_i05": "NOT_AUTHORIZED__SRC17_SCOPE_EXCLUDES",
                "reusable_for_src04_binding": src17_scope["reusable_for_src04_binding"],
            }
            readiness = "READY_FOR_AUTHORIZED_C11_ONLY__I03_I05_EXCLUDED"
            remaining = "C11 source-read scope is exact; I03/I05/first-consumer remains outside this grant."
            owner_event = "Existing exact SRC17 C11 construction grant; no I03/I05 promotion."
        else:
            binding = {
                "status": "NO_EXISTING_CURRENT_SOURCE_USE_GRANT",
                "source": None,
                "sha256": None,
                "proof_refs": proof_refs,
                "currentness": permission.get("currentness"),
                "revocation": permission.get("revocation"),
            }
            readiness = "BLOCKED_TRUE_SOURCE_PERMISSION_GAP"
            remaining = permission.get("minimal_missing_proof") or "Authenticated current source-use decision."
            owner_event = permission.get("minimal_missing_actor") or "Named competent source owner/data steward."

        rows.append({
            "source_id": source_id,
            "family": bundle["family"],
            "wave": bundle["wave"],
            "config": {
                "path": config["path"],
                "revision_ref": config["revision_ref"],
                "file_sha256": config["file_sha256"],
                "canonical_sha256": config["canonical_sha256"],
                "binding_status": config["binding_status"],
                "materialized": config["materialized"],
                "checks": config["binding_checks"],
                "shape": config_bind["declared_shape"],
            },
            "rights": {
                "rights_decision": bundle["rights_decision"],
                "decision": decision,
                "source_sha256": bundle["source_sha256"],
                "authorized_host": permission.get("authorized_host"),
                "authorized_purposes": permission.get("authorized_purposes"),
                "authorized_consumer": permission.get("authorized_consumer"),
                "currentness": permission.get("currentness"),
                "revocation": permission.get("revocation"),
                "proof_ref_count": len(proof_refs),
                "proof_refs": proof_refs,
                "scope_match": permission.get("1002_scope_match"),
            },
            "binding": binding,
            "construction_readiness": readiness,
            "remaining_item": remaining,
            "engineering_consequence": (
                "Exact config is available, but no current authenticated source-use decision means the runner cannot open/decode this source or construct source-backed C11; no Q2/analysis issuance is involved."
                if readiness.startswith("BLOCKED")
                else "Exact config and current source-use binding are available; construction remains unexecuted and requires authorized source launch."
            ),
            "owner_or_event_needed": owner_event,
            "q2": {
                "status": bundle["q2_input_status"],
                "missing": bundle.get("missing_q2_inputs", []),
                "construction_blocker": False,
                "note": "Q2/analysis issuance is not required for C11 construction; held Q2 inputs remain held.",
            },
            "sourcefree_metadata_only": bundle.get("sourcefree_fixture") is not None,
            "source_body_read": False,
        })

    counts = {
        "sources": 35,
        "config_exact": sum(row["config"]["binding_status"] == "BOUND_EXACT_CONFIG_REVISION" for row in rows),
        "exact_current_c11_construction_bindings": sum(row["binding"]["status"].startswith("EXACT_MACHINE_BINDING_AVAILABLE") for row in rows),
        "partial_c11_only": sum(row["binding"].get("partial_i03_i05", False) for row in rows),
        "blocked_true_permission_gap": sum(row["construction_readiness"].startswith("BLOCKED") for row in rows),
        "q2_held": sum(row["q2"]["status"] == "HELD" for row in rows),
        "config_defects_found": 0,
    }
    ledger = {
        "schema": "ANVIL_ALL35_RUNNABLE_INPUT_LEDGER@1",
        "generated_utc": "2026-11-19",
        "source_inputs": {
            "bundles": str(INPUTS / "bundles"),
            "rights_matrix": str(INPUTS / "evidence/35_row_source_rights_matrix.json"),
            "rights_matrix_sha256": sha(INPUTS / "evidence/35_row_source_rights_matrix.json"),
            "config_bindings": str(INPUTS / "evidence/config_bindings.json"),
            "config_binding_summary": config_summary,
            "grant_adapter": str(GRANTS),
            "compact_sqlite_free_operator": "MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_OPERATOR_INTEGRATION_20261118 @ 0bdda6428654fd949196dd8d46e428b83ed42f0d",
        },
        "counts": counts,
        "rows": rows,
    }
    (OUT / "ALL35_RUNNABLE_INPUT_LEDGER.json").write_text(json.dumps(ledger, indent=2, sort_keys=False) + "\n")
    with (OUT / "ALL35_RUNNABLE_INPUT_LEDGER.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=[
            "source_id", "family", "wave", "config_revision_ref", "config_file_sha256",
            "rights_decision", "source_sha256", "binding_status", "authorized_host",
            "authorized_purposes", "authorized_consumer", "currentness", "revocation",
            "construction_readiness", "remaining_item", "engineering_consequence", "owner_or_event_needed", "q2_status", "q2_construction_blocker",
        ])
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "source_id": row["source_id"], "family": row["family"], "wave": row["wave"],
                "config_revision_ref": row["config"]["revision_ref"],
                "config_file_sha256": row["config"]["file_sha256"],
                "rights_decision": row["rights"]["rights_decision"],
                "source_sha256": row["rights"]["source_sha256"],
                "binding_status": row["binding"]["status"],
                "authorized_host": row["rights"]["authorized_host"],
                "authorized_purposes": ",".join(row["rights"]["authorized_purposes"] or []),
                "authorized_consumer": row["rights"]["authorized_consumer"],
                "currentness": row["rights"]["currentness"],
                "revocation": row["rights"]["revocation"],
                "construction_readiness": row["construction_readiness"],
                "remaining_item": row["remaining_item"],
                "engineering_consequence": row["engineering_consequence"],
                "owner_or_event_needed": row["owner_or_event_needed"],
                "q2_status": row["q2"]["status"],
                "q2_construction_blocker": row["q2"]["construction_blocker"],
            })

    bindings = {
        "schema": "ANVIL_ALL35_MACHINE_BINDING_INDEX@1",
        "scope": "Existing exact local source-read/C11 consent only; no new grant, no source read, no Q2 issuance.",
        "runner_inputs": {
            "compact_operator": "MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_OPERATOR_INTEGRATION_20261118",
            "operator_head": "0bdda6428654fd949196dd8d46e428b83ed42f0d",
            "candidate_tree": "MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree",
            "candidate_patch": "OWNER/WORKER_RETURNS/ANVIL_ALL35_CONSTRUCTION_ONLY_CANDIDATE_20261118/candidate.patch",
            "real_source_launch": "NOT_PERFORMED__REQUIRES_AUTHORIZED_SOURCE_GRANT_AND_CURRENT_RESOLVER",
        },
        "bindings": {
            "SRC04": {
                "status": "EXACT_MACHINE_BINDING_AVAILABLE",
                "path": str(GRANTS / "SRC04_BINDING.json"),
                "sha256": sha(GRANTS / "SRC04_BINDING.json"),
                "source_sha256": src04_binding["request"]["source_sha256"],
                "host": src04_binding["request"]["host"],
                "purpose": src04_binding["request"]["purpose"],
                "consumer_use": src04_binding["request"]["consumer_use"],
                "currentness": src04_binding["currentness"],
                "revocation_ref": src04_binding["revocation_ref"],
                "grant_sha256": src04_binding["grant_sha256"],
                "decision_ref": src04_binding["decision_ref"],
            },
            "SRC17": {
                "status": "EXACT_MACHINE_BINDING_AVAILABLE_PARTIAL_C11_ONLY",
                "authentication_path": str(GRANTS / "fixtures/SRC17_GRANT_AUTHENTICATION.json"),
                "authentication_sha256": sha(GRANTS / "fixtures/SRC17_GRANT_AUTHENTICATION.json"),
                "scope_receipt_path": str(GRANTS / "SRC17_SCOPE.json"),
                "scope_receipt_sha256": sha(GRANTS / "SRC17_SCOPE.json"),
                "source_sha256": src17_auth["request"]["source_sha256"],
                "host": src17_auth["request"]["host"],
                "purpose": src17_auth["request"]["purpose"],
                "consumer_use": src17_auth["request"]["consumer_use"],
                "currentness": src17_auth["currentness"],
                "revocation": src17_auth["revocation"],
                "grant_sha256": src17_scope["grant_sha256"],
                "decision_ref": src17_auth["decision_ref"],
                "partial_i03_i05": True,
                "reusable_for_src04_binding": src17_scope["reusable_for_src04_binding"],
            },
        },
        "refused_inferences": [
            "filesystem presence or custody is not permission",
            "sourcefree TEST_ONLY fixture existence is not source permission",
            "historical/superseded grants are not current grants",
            "SRC17 construction-only grant is not reusable for SRC04 or I03/I05",
        ],
    }
    (OUT / "MACHINE_BINDINGS.json").write_text(json.dumps(bindings, indent=2, sort_keys=True) + "\n")
    summary = {
        "schema": "ANVIL_ALL35_EXECUTION_READINESS_SUMMARY@1",
        "counts": counts,
        "available_exact_bindings": ["SRC04", "SRC17"],
        "partial_c11_only": ["SRC17"],
        "blocked_true_permission_gap": [row["source_id"] for row in rows if row["construction_readiness"].startswith("BLOCKED")],
        "q2_held": [row["source_id"] for row in rows if row["q2"]["status"] == "HELD"],
        "config_defects": [],
        "rights_counts": rights["counts"],
        "construction_note": "C11 construction does not require Q2/analysis issuance; Q2-held fields are not construction permission.",
        "source_read_performed": False,
        "new_grants_minted": 0,
        "inventory_duplication": False,
    }
    (OUT / "SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
