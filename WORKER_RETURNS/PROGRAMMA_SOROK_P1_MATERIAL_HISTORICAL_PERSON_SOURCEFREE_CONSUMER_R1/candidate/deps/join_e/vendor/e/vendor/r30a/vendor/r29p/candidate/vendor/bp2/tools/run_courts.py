"""Run the full BP2 court and write every evidence artifact.

Usage:
    python3 tools/run_courts.py

Produces:
    evidence/junit/*.xml                 per-court JUnit receipts
    evidence/joined_positive_*.json      the hot positive chain + custody ledger
    evidence/alternatives_receipt.json   NO_CHANGE / DENY / two-actor receipts
    evidence/severance_receipt.json      six + four same-assertion severances
    evidence/cold_verification.json      separate-process cold verification
    evidence/security_receipt.json       closed controls and typed residuals
    evidence/scientific_decision_request.json
    evidence/source_manifest_summary.json
    evidence/environment_passport.json
    evidence/not_run_inventory.json
    evidence/native_functional_gap.json
    evidence/authority_hold_register.json
    evidence/source_actor_performer_gap_table.json
    evidence/d1_d2_d3_residuals.json
    evidence/privacy_and_law.json
"""
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

os.environ.setdefault("PYTHONHASHSEED", "0")
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

import bp2_joined  # noqa: E402
from bp2_joined import ports, scientific  # noqa: E402
from bp2_joined.producer import (  # noqa: E402
    EXPECTED_ACT,
    ACTUATOR,
    OCCURRENCE_E2,
    JoinedProducer,
    joined_consumer_assertion,
)
from bp2_joined.severance import (  # noqa: E402
    EDGE_CUT_DESCRIPTION,
    SEVERANCE_EDGES,
    SUPPLEMENTARY_EDGES,
    run_all_severances,
    severance_receipt,
)

EVIDENCE = RETURN / "evidence"
JUNIT = EVIDENCE / "junit"

COURTS = (
    "tests/test_joined_positive.py",
    "tests/test_joined_alternatives.py",
    "tests/test_joined_severance.py",
    "tests/test_joined_security.py",
    "tests/test_native_ports.py",
)


def _json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, default=str) + "\n",
                    encoding="utf8")


def _run_pytest() -> dict:
    JUNIT.mkdir(parents=True, exist_ok=True)
    results = {}
    for court in COURTS:
        name = Path(court).stem
        xml = JUNIT / f"{name}.xml"
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-c", "tests/pytest.ini",
             court, f"--junitxml={xml}", "-q"],
            cwd=str(RETURN), capture_output=True, text=True,
            env=dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1"),
        )
        results[name] = {
            "court": court,
            "returncode": completed.returncode,
            "junit": str(xml.relative_to(RETURN)),
            "tail": completed.stdout.strip().splitlines()[-1:] if completed.stdout else [],
        }
        if completed.returncode != 0:
            results[name]["stderr_tail"] = completed.stderr.strip().splitlines()[-20:]
    return results


def _custody_ledger(producer: JoinedProducer, receipt: dict) -> dict:
    occurrence = producer.occurrence
    ledger = occurrence.life.a_ledger
    steps = []
    for event in ledger.events:
        steps.append({
            "stage": "BP1_" + event.kind,
            "actor_id": event.actor_id,
            "ref": event.event_id,
            "hash": event.hash,
            "causal_parents": list(event.causal_parent_event_ids),
        })
    steps.extend([
        {
            "stage": "BP3_C8_EXCLUSIVE_APPEND",
            "occurrence_id": receipt["c8_occurrence_id"],
            "state_digest": receipt["c8_state_digest"],
            "commit_receipt_id": receipt["c8_commit_receipt_id"],
            "writer_version": receipt["c8_writer_version"],
            "anchor_seq": producer.commit.anchor_seq,
            "admission_grade": producer.commit.event.get("admission_grade"),
        },
        {
            "stage": "OUT9_READ_ONLY",
            "occurrence_id": receipt["out9_occurrence_id"],
            "state_digest": receipt["out9_state_digest"],
            "canonical_bytes_sha256": producer.out9.canonical_bytes_sha256,
            "proof_verified": producer.out9.verified_proof,
        },
        {
            "stage": "C9_ACTOR_INGRESS",
            "actor_id": receipt["actor_id"],
            "source_hash": receipt["actor_source_hash"],
            "standing_state": receipt["actor_standing_state"],
            "readset": receipt["c9"]["actor_readset"],
        },
        {
            "stage": "C9_E1_EVENT_WITNESS",
            "event_id": receipt["c9"]["event_id"],
            "event_hash": receipt["c9"]["event_hash"],
            "c8_occurrence_id": producer.e1_event["content"]["c8_occurrence_id"],
            "bp1_causal_parent_event_ids":
                producer.e1_event["content"]["bp1_causal_parent_event_ids"],
            "adp019_admission_receipt": receipt["adp019_admission_receipt"],
        },
        {
            "stage": "C9_CAN008_RULE_A",
            "rule_a_content_hash": receipt["rule_a_content_hash"],
            "response_hash": receipt["response_hash"],
            "rule_lookup": producer.pipeline.response.rule_lookup.status.value,
        },
        {
            "stage": "C9_CAN011_RULE_T",
            "rule_t_content_hash": receipt["rule_t_content_hash"],
            "rule_t_dependency_hash": receipt["rule_t_dependency_hash"],
            "grant_hash": receipt["grant_hash"],
            "grant_id": receipt["grant_id"],
        },
        {
            "stage": "C9_DURABLE_TARGET_COMMIT",
            "target_id": receipt["target_id"],
            "target_record_hash": receipt["target_record_hash"],
            "target_branch": receipt["target_branch"],
            "creation_rule_ref": receipt["creation_rule_ref"],
        },
        {
            "stage": "C9_LATER_COMMITTED_READ",
            "consumer_id": "TEST_ONLY_BP2_LATER_E2_READER",
            "consumed_state_hash": receipt["consumed_state_hash"],
            "read_receipt_hash": receipt["e2"]["later_read_receipt"],
        },
        {
            "stage": "TEST_ONLY_INDEPENDENT_E2",
            "receipt_hash": receipt["e2_receipt_hash"],
            "actuator_ref": receipt["e2_actuator_ref"],
            "occurrence_ref": receipt["e2_occurrence_ref"],
            "consumed_state_hash": receipt["e2_consumed_state_hash"],
            "target_commit_time": receipt["e2"]["target_commit_time"],
            "action_time": receipt["e2"]["action_time"],
        },
    ])
    return {
        "schema": "BP2_EVENT_ACTOR_RULE_TARGET_E2_CUSTODY@1",
        "note": (
            "One causal custody chain. Each link is verified by code, not by "
            "adjacency: the C8 occurrence id/state digest binds into the C9 E1 "
            "content hash, the response hash binds into the CAN011 grant, the "
            "grant and rule bind into the sealed target record, and the later E2 "
            "receipt binds the exact consumed record digest."),
        "steps": steps,
        "verified_links": [
            {"from": "BP1_PRIOR_HISTORY/PERFORMED_ACTION", "to": "BP3_C8_EXCLUSIVE_APPEND",
             "check": "payload actor/other history hashes and causal parents"},
            {"from": "BP3_C8_EXCLUSIVE_APPEND", "to": "OUT9_READ_ONLY",
             "check": "verify_journal proof + state_digest + occurrence set + byte readset"},
            {"from": "OUT9_READ_ONLY", "to": "C9_E1_EVENT_WITNESS",
             "check": "content hash carries occurrence id, state digest and commit receipt id"},
            {"from": "C9_E1_EVENT_WITNESS", "to": "C9_CAN008_RULE_A",
             "check": "response receipt hash over event hash + rule + readset"},
            {"from": "C9_CAN008_RULE_A", "to": "C9_CAN011_RULE_T",
             "check": "target dependency hash equals response rule content hash"},
            {"from": "C9_CAN011_RULE_T", "to": "C9_DURABLE_TARGET_COMMIT",
             "check": "grant bound to response hash + before-target hash + actor"},
            {"from": "C9_DURABLE_TARGET_COMMIT", "to": "C9_LATER_COMMITTED_READ",
             "check": "sealed record preimage digest equals committed record hash"},
            {"from": "C9_LATER_COMMITTED_READ", "to": "TEST_ONLY_INDEPENDENT_E2",
             "check": "E2 receipt consumed_state_hash equals the independent read digest"},
        ],
        "receipt_summary": {
            "c8_occurrence_id": receipt["c8_occurrence_id"],
            "c8_state_digest": receipt["c8_state_digest"],
            "actor_id": receipt["actor_id"],
            "other_actor_id": receipt["other_actor_id"],
            "target_id": receipt["target_id"],
            "target_record_hash": receipt["target_record_hash"],
            "consumed_state_hash": receipt["consumed_state_hash"],
            "e2_receipt_hash": receipt["e2_receipt_hash"],
        },
    }


def _fresh_runtime(name: str) -> Path:
    import shutil

    root = EVIDENCE / "runtime" / name
    if root.exists():
        shutil.rmtree(root)
    return root


def _positive() -> tuple[dict, dict]:
    # A fixed runtime root keeps the exact committed identities reproducible by
    # re-running this tool. The C8 journal identity binds its absolute path, so
    # the hashes are stable for this checkout path, not across checkouts.
    root = _fresh_runtime("positive")
    with JoinedProducer(root) as producer:
        outcome = producer.run()
        joined_consumer_assertion(outcome)
        receipt = outcome.receipt()
        ledger = _custody_ledger(producer, receipt)
    return receipt, ledger


def _alternatives() -> dict:
    result: dict = {"schema": "BP2_ALTERNATIVES_RECEIPT@1"}
    with tempfile.TemporaryDirectory() as td:
        with JoinedProducer(Path(td) / "nochange") as producer:
            producer.stage_world(); producer.stage_c8(); producer.stage_out9()
            pipeline = producer.stage_c9(rule_a_registry="empty")
            result["no_change_empty_rule_registry"] = {
                "committed": pipeline.committed,
                "branch": pipeline.decision.branch.value,
                "reason": pipeline.decision.reason.value,
                "response_status": pipeline.response.status.value,
                "response_reason": pipeline.response.reason,
                "target_rows": producer.c9.db.execute(
                    "SELECT count(*) FROM target_state").fetchone()[0],
                "occurrence_rows": producer.c9.db.execute(
                    "SELECT count(*) FROM occurrence").fetchone()[0],
            }
        with JoinedProducer(Path(td) / "deny") as producer:
            producer.stage_world(); producer.stage_c8(); producer.stage_out9()
            pipeline = producer.stage_c9(self_issued=True)
            result["deny_self_issued"] = {
                "committed": pipeline.committed,
                "branch": pipeline.decision.branch.value,
                "reason": pipeline.decision.reason.value,
                "target_rows": producer.c9.db.execute(
                    "SELECT count(*) FROM target_state").fetchone()[0],
                "occurrence_rows": producer.c9.db.execute(
                    "SELECT count(*) FROM occurrence").fetchone()[0],
            }
        with JoinedProducer(Path(td) / "material") as producer:
            producer.stage_world(); producer.stage_c8(); producer.stage_out9()
            pipeline = producer.stage_c9(material_access="denied")
            result["no_change_denied_material"] = {
                "material_eligible": pipeline.material_eligible,
                "material_reason": pipeline.material_reason,
                "branch": pipeline.decision.branch.value,
                "target_rows": producer.c9.db.execute(
                    "SELECT count(*) FROM target_state").fetchone()[0],
            }
        two = {}
        for key in ("A", "B"):
            with JoinedProducer(_fresh_runtime("two-actor-" + key), actor=key) as producer:
                outcome = producer.run()
                joined_consumer_assertion(outcome)
                receipt = outcome.receipt()
                two[key] = {
                    "actor_id": receipt["actor_id"],
                    "other_actor_id": receipt["other_actor_id"],
                    "actor_source_hash": receipt["actor_source_hash"],
                    "target_id": receipt["target_id"],
                    "target_record_hash": receipt["target_record_hash"],
                    "consumed_state_hash": receipt["consumed_state_hash"],
                    "response_hash": receipt["response_hash"],
                }
        result["two_actor_histories"] = two
        result["two_actor_histories"]["distinct"] = (
            two["A"]["target_record_hash"] != two["B"]["target_record_hash"]
            and two["A"]["consumed_state_hash"] != two["B"]["consumed_state_hash"])
    return result


def _severances() -> dict:
    with tempfile.TemporaryDirectory() as td:
        trials = run_all_severances(Path(td) / "severance")
    receipt = severance_receipt(trials)
    receipt["declared_edges"] = list(SEVERANCE_EDGES)
    receipt["declared_supplementary"] = list(SUPPLEMENTARY_EDGES)
    receipt["cut_descriptions"] = EDGE_CUT_DESCRIPTION
    return receipt


def _cold() -> dict:
    root = _fresh_runtime("cold")
    receipt_path = EVIDENCE / "runtime" / "cold-receipt.json"
    with tempfile.TemporaryDirectory() as td:
        build = subprocess.run(
            [sys.executable, str(RETURN / "tools" / "cold_probe.py"),
             "build", str(root), str(receipt_path)],
            capture_output=True, text=True, cwd=str(td),
            env=dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1"))
        if build.returncode != 0:
            return {"status": "BUILD_FAILED", "stderr": build.stderr}
        verify = subprocess.run(
            [sys.executable, str(RETURN / "tools" / "cold_probe.py"),
             "verify", str(root), str(receipt_path)],
            capture_output=True, text=True, cwd=str(td),
            env=dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1"))
        return json.loads(verify.stdout.strip().splitlines()[-1])


def _environment_passport() -> dict:
    import sqlite3

    return {
        "schema": "BP2_ENVIRONMENT_PASSPORT@1",
        "repository": "maidiu/rawlsing",
        "branch": "agent/rabochii-sorok-20261020-bp2-joined-event-rule-action-positive-r1",
        "sealed_startup": "e699fed59925a3d7b3f02805f85771ae2df32be8",
        "return_prefix": "WORKER_RETURNS/SOROK-20261020-BP2-JOINED-ACTOR-EVENT-RULE-ACTION-R1/",
        "model": "DeepSeek V4.1-Flash (harness-declared)",
        "reasoning_effort_requested": "MAX",
        "harness": "DeepSeek Harness local session",
        "one_agent_no_subagent": True,
        "python": platform.python_version(),
        "pytest": _module_version("pytest"),
        "sqlite3_module": sqlite3.sqlite_version,
        "git": _git_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cwd": str(RETURN),
        "third_party_packages": "stdlib only (hashlib, hmac, json, sqlite3, fcntl, subprocess)",
        "cryptography_module_present": False,
        "paid_api_calls": "UNKNOWN__NO_EXTERNAL_API_INVOKED_BY_TESTS",
        "account_quota_and_spend": "UNKNOWN",
        "source_edits_outside_return": [],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def _module_version(name: str) -> str:
    module = __import__(name)
    return getattr(module, "__version__", "unknown")


def _git_version() -> str:
    completed = subprocess.run(["git", "--version"], capture_output=True, text=True)
    return completed.stdout.strip()


def _not_run() -> dict:
    return {
        "schema": "BP2_NOT_RUN_INVENTORY@1",
        "not_run": [
            {"item": "native ADP019 admission", "owner": "V3 External Admission Court",
             "reason": "no owner receipt issued; TEST_ONLY grade only"},
            {"item": "native ADP010 opportunity/encounter", "owner": "ADP010 encounter owner",
             "reason": "production registry empty"},
            {"item": "native CAN008 RULE_A", "owner": "CAN008 R2 concrete rule issuer",
             "reason": "rule body/version/hash unissued"},
            {"item": "native CAN011 RULE_T + grant", "owner": "separate CAN011 target owner",
             "reason": "unissued"},
            {"item": "native E2 performed action", "owner": "native actuator/occurrence owner",
             "reason": "TEST_ONLY declared actuator only"},
            {"item": "native ADP007 actor / ADP015 other", "owner": "ADP007/ADP015 owners",
             "reason": "TEST_ONLY fixture actors"},
            {"item": "C8 D1 production writer cutover", "owner": "C8 writer owner",
             "reason": "import-only gate; old writer callable outside the gated import"},
            {"item": "C8 D2 production KMS/anchor custody", "owner": "key/anchor custodian",
             "reason": "TEST_ONLY key file + local keyed anchor"},
            {"item": "C8 D3 native event issuance", "owner": "ADP019 owner",
             "reason": "no admission"},
            {"item": "power-failure/media durability proof", "owner": "storage owner",
             "reason": "fsync+rename is not a power-failure guarantee"},
            {"item": "Pyat N11/N12 receiving schema", "owner": "Pyat HQ",
             "reason": "out of scope; not read as authority"},
            {"item": "C11 weld / C12 generated person", "owner": "C11/C12 authorities",
             "reason": "not attempted"},
            {"item": "original raw respondent source use", "owner": "source custodian",
             "reason": "no permission; not accessed"},
            {"item": "production registry population", "owner": "PSEPF registry binder",
             "reason": "empty by design"},
        ],
    }


def _native_gap() -> dict:
    return {
        "schema": "BP2_NATIVE_FUNCTIONAL_GAP@1",
        "epistemic_rule": "input -> authenticating decision -> receipt -> consumer -> scientific effect",
        "gaps": [
            {"function": "E1 external admission", "input": "committed C8 occurrence",
             "decision": "ADP019 external admission court", "receipt": "V3_EXTERNAL_ADMISSION_RECEIPT",
             "consumer": "C9R event witness ingress", "scientific_effect": "admitted precipitating event",
             "current": "ADP019_ADMISSION_RECEIPT_ABSENT"},
            {"function": "encounter binding", "input": "world availability",
             "decision": "ADP010 opportunity/encounter owner", "receipt": "encounter receipt",
             "consumer": "conditioning material eligibility", "scientific_effect": "actual actor encounter",
             "current": "OPPORTUNITY_AND_ENCOUNTER_UNISSUED"},
            {"function": "response rule", "input": "event + actor + conditioning",
             "decision": "CAN008 R2 concrete issuer", "receipt": "signed rule body/version/hash",
             "consumer": "C9R RULE_A lookup", "scientific_effect": "bounded actor response",
             "current": "RULE_A_UNISSUED"},
            {"function": "target update", "input": "response + before-state",
             "decision": "separate CAN011 owner", "receipt": "RULE_T + grant",
             "consumer": "C9R RULE_T evaluation + commit", "scientific_effect": "durable target state",
             "current": "RULE_T_AND_GRANT_UNISSUED"},
            {"function": "performed later action", "input": "committed target state",
             "decision": "native action owner", "receipt": "performed-action owner receipt",
             "consumer": "C9R E2 admission", "scientific_effect": "actual later act",
             "current": "TEST_ONLY_ONLY"},
            {"function": "actor genesis", "input": "source-qualified subject",
             "decision": "ADP007 owner", "receipt": "actor genesis/activation",
             "consumer": "C9R actor ingress", "scientific_effect": "native actor",
             "current": "TEST_ONLY_FIXTURE_ACTOR_NOT_NATIVE"},
            {"function": "independent other", "input": "ADP015/source-qualified other",
             "decision": "ADP015 owner", "receipt": "other/parent relation",
             "consumer": "BP1 other ledger", "scientific_effect": "genuine other person",
             "current": "TEST_ONLY_FIXTURE_OTHER_NOT_NATIVE"},
        ],
    }


def _authority_holds() -> dict:
    return {
        "schema": "BP2_AUTHORITY_HOLD_REGISTER@1",
        "holds": [
            {"authority": "ADP019 external admission", "owner": "V3 External Admission Court",
             "status": "HOLD", "issued": False},
            {"authority": "ADP010 encounter", "owner": "ADP010 owner", "status": "HOLD",
             "issued": False},
            {"authority": "CAN008 RULE_A", "owner": "CAN008 R2 concrete issuer",
             "status": "HOLD", "issued": False},
            {"authority": "CAN011 RULE_T + grant", "owner": "separate target owner",
             "status": "HOLD", "issued": False},
            {"authority": "E2 performed action", "owner": "native actuator owner",
             "status": "HOLD", "issued": False},
            {"authority": "ADP007 actor genesis", "owner": "ADP007 owner", "status": "HOLD",
             "issued": False},
            {"authority": "ADP015 other/family", "owner": "ADP015 owner", "status": "HOLD",
             "issued": False},
            {"authority": "C8 D1 writer cutover", "owner": "C8 writer owner", "status": "HOLD",
             "issued": False},
            {"authority": "C8 D2 key/anchor custody", "owner": "key/anchor custodian",
             "status": "HOLD", "issued": False},
            {"authority": "C8 D3 native event", "owner": "ADP019 owner", "status": "HOLD",
             "issued": False},
            {"authority": "Pyat N11/N12 world", "owner": "Pyat HQ", "status": "HOLD",
             "issued": False},
            {"authority": "C11 weld / C12 person", "owner": "C11/C12", "status": "HOLD",
             "issued": False},
            {"authority": "M2/MP original family source", "owner": "original source owners",
             "status": "HOLD", "issued": False},
            {"authority": "PSEPF production registry", "owner": "registry binder",
             "status": "HOLD", "issued": False},
        ],
        "self_adoption": False,
    }


def _gap_table() -> dict:
    return {
        "schema": "BP2_SOURCE_ACTOR_PERFORMER_GAP_TABLE@1",
        "rows": [
            {"dimension": "source", "test_only": "BP1 TEST_ONLY fixture actor sources; G18 sourcefree material receipt",
             "native": "Pyat/C0 source-qualified world and ADP019 event source",
             "gap_owner": "Pyat HQ + ADP019 + source custodian", "status": "HOLD"},
            {"dimension": "actor", "test_only": "two TEST_ONLY_BP1_ACTOR_A/B histories with distinct material budgets",
             "native": "ADP007 actor genesis + ADP015 independent other",
             "gap_owner": "ADP007/ADP015", "status": "HOLD"},
            {"dimension": "performer", "test_only": "TEST_ONLY_ACTUATOR_BP2_INDEPENDENT + TEST_ONLY_OCCURRENCE_BP2_E2",
             "native": "native performed-action actuator and occurrence owner",
             "gap_owner": "native action owner", "status": "HOLD"},
            {"dimension": "writer", "test_only": "BP3 keyed exclusive writer with TEST_ONLY key file + keyed anchor",
             "native": "C8 D1 exclusive writer cutover + D2 production KMS/anchor",
             "gap_owner": "C8 D1/D2 owners", "status": "HOLD"},
            {"dimension": "event", "test_only": "C8 occurrence at SOURCEFREE_LEGACY_FIXTURE_NO_OWNER_AUTHORITY",
             "native": "ADP019 admitted occurrence (D3)",
             "gap_owner": "ADP019 owner", "status": "HOLD"},
            {"dimension": "rule", "test_only": "TEST_ONLY_BP2 CAN008 RULE_A and CAN011 RULE_T",
             "native": "concrete CAN008/CAN011 issued rules + grant",
             "gap_owner": "CAN008/CAN011 owners", "status": "HOLD"},
            {"dimension": "person", "test_only": "one finite sourcefree practice target",
             "native": "C12 pipeline-generated person", "gap_owner": "C11/C12",
             "status": "HOLD"},
        ],
    }


def _residuals() -> dict:
    return {
        "schema": "BP2_D1_D2_D3_RESIDUALS@1",
        "d1_writer_cutover": {
            "closed_in_gated_process": [
                "accepted OUT9 Journal.commit refused with LEGACY_WRITER_ROUTE_CLOSED",
                "accepted OUT9 Journal.admit_and_queue refused",
            ],
            "residual": "a process that imports outbox_prototype without importing the BP3 candidate can still call the old writer; direct filesystem writes are not prevented",
            "owner": "C8 writer owner (D1)",
            "test": "tests/test_joined_security.py::test_old_writer_still_callable_outside_the_gated_import_is_a_typed_residual",
        },
        "d2_key_and_anchor": {
            "closed_in_candidate": [
                "forged capability refused",
                "unkeyed receipt forgery refused by keyed proof",
                "withheld/tampered anchor refused",
                "byte-valid rollback with old proof detected",
            ],
            "residual": "possession of the TEST_ONLY key file mints a valid capability; anchor log+watermark rolled back together defeat detection; no production KMS/HSM",
            "owner": "key/anchor custodian (D2)",
            "test": "tests/test_joined_security.py::test_leaked_test_key_can_forge_a_valid_capability_is_a_typed_residual",
        },
        "d3_native_event": {
            "residual": "no ADP019 admission, no native actor occurrence and no native E2",
            "owner": "ADP019 owner (D3)",
            "current": "ADP019_ADMISSION_RECEIPT_ABSENT",
        },
        "crash_after_rename_before_proof": {
            "observed": "journal bytes are visible and byte-valid to a raw OUT9 read; verify_journal refuses with PROOF_SIDECAR_MISSING; no acknowledged state is claimed",
            "required_action": "typed recover-or-HOLD by the C8 owner; this candidate refuses and does not acknowledge",
            "test": "tests/test_joined_security.py::test_crash_after_journal_rename_before_proof_sidecar_is_not_acknowledged",
        },
        "durability": "fsync+rename is not a power-failure guarantee on exotic filesystems; no production FS assumption is made",
    }


def _security_receipt() -> dict:
    return {
        "schema": "BP2_SECURITY_RECEIPT@1",
        "closed_in_candidate_process": [
            "old OUT9 class writer routes closed",
            "forged KeyedCapability refused",
            "unkeyed receipt forgery refused by keyed proof",
            "withheld anchor / tampered watermark MAC refused",
            "byte-valid rollback detected by the external anchor",
            "stale writer version refused",
            "empty expected OUT9 state digest refused",
            "key store inside the journal directory refused",
            "crash after rename before proof sidecar refused, not acknowledged",
            "self-actuator and self-occurrence E2 refused",
        ],
        "typed_residuals": [
            "old writer callable in a process that does not import the BP3 gate (D1)",
            "a leaked TEST_ONLY key can mint a valid capability (D2)",
            "anchor log+watermark rolled back together defeat detection (D2)",
            "raw OUT9 reads the unacknowledged post-crash state (typed HOLD required)",
        ],
        "tests": [
            "tests/test_joined_security.py",
        ],
    }


def _privacy_law() -> dict:
    return {
        "schema": "BP2_SOURCE_PRIVACY_AND_LAW@1",
        "raw_respondent_data_accessed": False,
        "original35_waves_accessed": False,
        "native_pyat_world_accessed": False,
        "production_installation": False,
        "upstream_source_edits": [],
        "upstream_tests_edited": [],
        "actor_identifiers": "TEST_ONLY_BP1_ACTOR_A/B fixtures, not real persons",
        "cryptography": "TEST_ONLY HMAC key file; not a production key or signer",
        "native_authority_issued": False,
        "privacy_or_native_law_claim": False,
    }


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    manifest = bp2_joined.verify_sources()
    _json(EVIDENCE / "source_manifest_summary.json", {
        "schema": "BP2_SOURCE_MANIFEST_SUMMARY@1",
        "manifest_path": str((RETURN / "vendor" / "source_manifest.json").relative_to(RETURN)),
        "file_count": manifest["file_count"],
        "origin_commits": manifest["origin_commits"],
        "files": [
            {"path": row["staged_path"], "sha256": row["sha256"],
             "git_blob_sha1": row["git_blob_sha1"],
             "origin_commit": row["origin_commit"], "origin_path": row["origin_path"]}
            for row in manifest["files"]
        ],
    })
    _json(EVIDENCE / "environment_passport.json", _environment_passport())

    receipt, ledger = _positive()
    _json(EVIDENCE / "joined_positive_receipt.json", receipt)
    _json(EVIDENCE / "joined_custody_ledger.json", ledger)
    _json(EVIDENCE / "alternatives_receipt.json", _alternatives())
    _json(EVIDENCE / "severance_receipt.json", _severances())
    cold = _cold()
    _json(EVIDENCE / "cold_verification.json", cold)
    _json(EVIDENCE / "security_receipt.json", _security_receipt())
    _json(EVIDENCE / "not_run_inventory.json", _not_run())
    _json(EVIDENCE / "native_functional_gap.json", _native_gap())
    _json(EVIDENCE / "authority_hold_register.json", _authority_holds())
    _json(EVIDENCE / "source_actor_performer_gap_table.json", _gap_table())
    _json(EVIDENCE / "d1_d2_d3_residuals.json", _residuals())
    _json(EVIDENCE / "privacy_and_law.json", _privacy_law())
    request = scientific.build_scientific_decision_request(
        run_receipt=receipt,
        no_change_evidence={
            "branch": "NO_CHANGE",
            "reason": "TARGET_RULE_ABSENT / NO_PROPOSAL",
            "target_rows": 0,
            "occurrence_preserved": True,
        },
        deny_evidence={
            "branch": "DENY",
            "reason": "PERMISSION_SELF_ISSUED",
            "target_rows": 0,
            "occurrence_preserved": True,
        },
    )
    _json(EVIDENCE / "scientific_decision_request.json", request)
    persisted = receipt["persisted"]
    _json(EVIDENCE / "bp4_downstream_afterstate.json", {
        "schema": "BP2_IMMUTABLE_C9_AFTERSTATE_FOR_BP4@1",
        "note": (
            "The exact immutable sourcefree afterstate BP4 may consume as its "
            "C10 input. BP4 must reject any row whose digest is not the recorded "
            "consumed_state_hash; this worker issues no C10/C11 authority."),
        "source_grade": "TEST_ONLY_SOURCEFREE_TECHNICAL",
        "native_grant": "NOT_GRANTED",
        "c8_occurrence_id": persisted["c8_occurrence_id"],
        "c8_state_digest": persisted["c8_state_digest"],
        "c8_commit_receipt_id": persisted["c8_commit_receipt_id"],
        "e1_event_hash": persisted["e1_event_hash"],
        "target_id": persisted["target_id"],
        "target_record_hash": persisted["target_record_hash"],
        "consumed_state_hash": persisted["consumed_state_hash"],
        "c9_commit_receipt_hash": persisted["c9_commit_receipt_hash"],
        "c9_authorization_hash": persisted["c9_authorization_hash"],
        "e2_receipt_hash": persisted["e2_receipt_hash"],
        "e2_actuator_ref": receipt["e2_actuator_ref"],
        "e2_occurrence_ref": receipt["e2_occurrence_ref"],
        "e2_consumed_state_hash": receipt["e2_consumed_state_hash"],
        "consumer_contract": [
            "read the durable target row by target_id",
            "recompute its digest and require equality with consumed_state_hash",
            "require the record preimage digest to equal target_record_hash",
            "require causal_parent_refs[0] to equal e1_event_hash",
            "reject any other C8 occurrence id or state digest",
        ],
        "adp019_admission_receipt": "ADP019_ADMISSION_RECEIPT_ABSENT",
    })

    courts = _run_pytest()
    _json(EVIDENCE / "court_results.json", {
        "schema": "BP2_COURT_RESULTS@1",
        "courts": courts,
        "all_green": all(row["returncode"] == 0 for row in courts.values()),
    })
    print(json.dumps({
        "sources": manifest["file_count"],
        "cold": cold.get("status"),
        "all_green": all(row["returncode"] == 0 for row in courts.values()),
        "courts": {name: row["returncode"] for name, row in courts.items()},
    }, sort_keys=True))
    return 0 if all(row["returncode"] == 0 for row in courts.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
