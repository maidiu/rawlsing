"""Run every BP2P4J court and write the complete evidence set.

Usage:
    python3 tools/run_courts.py

Writes ``evidence/`` (JSON receipts, JUnit XML, logs) and exits non-zero if any
court fails. The original pinned BP2 and BP4 suites are executed from the staged
byte-exact copies; no upstream test is edited.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

os.environ.setdefault("PYTHONHASHSEED", "0")
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

import bp2p4  # noqa: E402
from bp2p4 import c12_verify, reunion, seed as seed_mod  # noqa: E402
from bp2p4.assertion import ASSERTION_NAME, joined_downstream_a0_a2_assertion  # noqa: E402
from bp2p4.product import JoinedProduct  # noqa: E402
from bp2p4.severance import (  # noqa: E402
    EDGE_CUT_DESCRIPTION,
    SEVERANCE_EDGES,
    SUPPLEMENTARY_EDGES,
    run_all_severances,
    severance_receipt,
)

EVIDENCE = RETURN / "evidence"
JUNIT = EVIDENCE / "junit"
LOGS = EVIDENCE / "logs"
NEW_COURTS = (
    "tests/test_source_closure.py",
    "tests/test_joined_product.py",
    "tests/test_joined_severance.py",
    "tests/test_joined_security.py",
)


def _json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, default=str) + "\n",
                    encoding="utf8")


def _fresh(name: str) -> Path:
    root = EVIDENCE / "runtime" / name
    if root.exists():
        shutil.rmtree(root)
    return root


def _env(**extra) -> dict:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.update({key: str(value) for key, value in extra.items()})
    return env


# ---------------------------------------------------------------------------
# courts
# ---------------------------------------------------------------------------
def _run_pytest(court: str, junit: Path, cwd: Path, *, extra_env: dict | None = None,
                log: Path | None = None) -> dict:
    junit.parent.mkdir(parents=True, exist_ok=True)
    env = _env(**(extra_env or {}))
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", court, f"--junitxml={junit}", "-q"],
        cwd=str(cwd), capture_output=True, text=True, env=env)
    output = (completed.stdout or "") + (completed.stderr or "")
    if log is not None:
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(output, encoding="utf8")
    counts = _junit_counts(junit)
    return {
        "court": court,
        "cwd": str(cwd),
        "returncode": completed.returncode,
        "junit": str(junit.relative_to(RETURN)),
        "counts": counts,
        "tail": output.strip().splitlines()[-3:],
    }


def _junit_counts(path: Path) -> dict:
    import xml.etree.ElementTree as ET

    if not path.exists():
        return {}
    root = ET.parse(path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is None:
        return {}
    return {key: int(suite.get(key, 0))
            for key in ("tests", "failures", "errors", "skipped")}


def _new_courts() -> dict:
    results = {}
    for court in NEW_COURTS:
        name = Path(court).stem
        results[name] = _run_pytest(
            court, JUNIT / f"{name}.xml", RETURN,
            log=LOGS / f"{name}.log")
    return results


def _original_courts() -> dict:
    bp2_dir = RETURN / "vendor" / "bp2"
    bp4_dir = RETURN / "vendor" / "bp4"
    bp2 = _run_pytest("tests", JUNIT / "original_bp2_50.xml", bp2_dir,
                      extra_env={}, log=LOGS / "original_bp2.log")
    bp2["config"] = "tests/pytest.ini"
    # The original BP4 suite imports the live pinned rawlsing_next M6 module from
    # the checkout root, exactly as it did in its own return.
    bp4 = _run_pytest("tests", JUNIT / "original_bp4_15.xml", bp4_dir,
                      extra_env={"PYTHONPATH": str(bootstrap_repo())},
                      log=LOGS / "original_bp4.log")
    bp4["config"] = "default"
    return {"bp2_original": bp2, "bp4_original": bp4}


def bootstrap_repo() -> Path:
    return bp2p4.bootstrap.REPO


# ---------------------------------------------------------------------------
# evidence
# ---------------------------------------------------------------------------
def _environment_passport() -> dict:
    import sqlite3

    return {
        "schema": "BP2P4J_ENVIRONMENT_PASSPORT@1",
        "repository": "maidiu/rawlsing",
        "branch": "agent/rabochii-sorok-20261020-bp2p4j-joined-technical-alpha-r1",
        "sealed_startup": "267e97ff88acc4b19ea832bf8147f3ac2fa3bc81",
        "return_prefix": "WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1/",
        "model": "DeepSeek V4.1-Flash (harness-declared)",
        "reasoning_effort_requested": "MAX",
        "harness": "DeepSeek Harness local session",
        "one_agent_no_subagent": True,
        "python": platform.python_version(),
        "pytest": _version("pytest"),
        "sqlite3": sqlite3.sqlite_version,
        "git": _git_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "third_party_packages": "stdlib only",
        "paid_api_calls": "UNKNOWN__NO_EXTERNAL_API_INVOKED",
        "account_quota_spend": "UNKNOWN",
        "upstream_edits": [],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def _version(name: str) -> str:
    module = __import__(name)
    return getattr(module, "__version__", "unknown")


def _git_version() -> str:
    completed = subprocess.run(["git", "--version"], capture_output=True, text=True)
    return completed.stdout.strip()


def _source_summary() -> dict:
    manifest = bp2p4.verify_sources()
    return {
        "schema": "BP2P4J_SOURCE_SUMMARY@1",
        "manifest_path": "vendor/source_manifest.json",
        "file_count": manifest["file_count"],
        "origin_commits": manifest["origin_commits"],
        "files": [
            {"path": row["staged_path"], "sha256": row["sha256"],
             "git_blob_sha1": row["git_blob_sha1"],
             "origin_commit": row["origin_commit"],
             "origin_path": row["origin_path"]}
            for row in manifest["files"]
        ],
        "loaded_module_verification": bp2p4.verify_loaded_modules(strict=False),
    }


def _positive(fresh_root: Path) -> tuple[dict, dict]:
    artifacts = reunion.build_fresh(fresh_root / "join")
    receipt = joined_downstream_a0_a2_assertion(fresh_root / "product", artifacts)
    document = {
        "schema": "BP2P4J_JOINED_POSITIVE@1",
        "assertion": ASSERTION_NAME,
        "mode": artifacts.mode,
        "bp2_artifacts": artifacts.public(),
        "custody": seed_mod.build_seed(artifacts).custody(),
        "envelope": seed_mod.build_seed(artifacts).envelope,
        "envelope_validation": seed_mod.build_seed(artifacts).envelope_validation,
        "assertion_receipt": receipt,
        "reconciliation": reunion.reconciliation(artifacts.receipt["persisted"],
                                                  artifacts),
    }
    _json(EVIDENCE / "joined_positive.json", document)
    return artifacts, document


def _literal(fresh_root: Path) -> dict | None:
    runtime = reunion.origin_runtime_available()
    if runtime is None:
        return None
    evidence = RETURN / "vendor" / "bp2" / "evidence" / "joined_positive_receipt.json"
    artifacts = reunion.load_origin_literal(runtime, evidence_path=evidence)
    receipt = joined_downstream_a0_a2_assertion(fresh_root / "literal", artifacts)
    document = {
        "schema": "BP2P4J_LITERAL_ORIGIN_JOIN@1",
        "origin_runtime": str(runtime),
        "local_only": True,
        "reproducible_from_committed_sources": False,
        "note": (
            "The BP2 origin runtime contains a random TEST_ONLY key and a journal "
            "identity bound to its absolute path, so the literal target cannot be "
            "reproduced from committed sources. This direct literal cross-check is "
            "recorded when the surviving runtime is present."),
        "bp2_artifacts": artifacts.public(),
        "assertion_receipt": receipt,
        "reconciliation": reunion.reconciliation(artifacts.receipt["persisted"],
                                                  artifacts),
    }
    _json(EVIDENCE / "literal_origin_join.json", document)
    return document


def _custody_ledger(positive: dict) -> dict:
    artifacts = positive["bp2_artifacts"]
    custody = positive["custody"]
    receipt = positive["assertion_receipt"]
    life_events = []
    from bp1.composer import build_two_actor_life

    life = build_two_actor_life()
    for event in life.a_ledger.events:
        life_events.append({"stage": "BP1_A_" + event.kind, "ref": event.event_id,
                            "hash": event.hash,
                            "causal_parents": list(event.causal_parent_event_ids)})
    steps = life_events + [
        {"stage": "BP2_C8_OCCURRENCE", "occurrence_id": custody["c8_occurrence_id"],
         "state_digest": custody["c8_state_digest"],
         "commit_receipt_id": custody["c8_commit_receipt_id"],
         "writer_version": custody["c8_writer_version"]},
        {"stage": "BP2_E1_EVENT", "event_id": custody["e1_event_id"],
         "event_hash": custody["e1_event_hash"],
         "adp019_admission_receipt": custody["adp019_admission_receipt"]},
        {"stage": "BP2_CAN008_RULE_A", "rule_a_content_hash": custody["rule_a_content_hash"],
         "response_hash": custody["response_hash"]},
        {"stage": "BP2_CAN011_RULE_T", "rule_t_content_hash": custody["rule_t_content_hash"],
         "dependency_hash": custody["rule_t_dependency_hash"],
         "grant_hash": custody["grant_hash"]},
        {"stage": "BP2_C9_TARGET_COMMIT", "target_id": custody["target_id"],
         "target_record_hash": custody["target_record_hash"],
         "authorization_hash": artifacts["c9_authorization_hash"],
         "commit_receipt_hash": artifacts["c9_commit_receipt_hash"],
         "publication_grade": "TEST_ONLY_SOURCEFREE_TECHNICAL"},
        {"stage": "BP2_INDEPENDENT_E2", "receipt_hash": custody["e2_receipt_hash"],
         "act": receipt["practice"]["performed_act"],
         "actuator_ref": "TEST_ONLY_ACTUATOR_BP2_INDEPENDENT",
         "occurrence_ref": "TEST_ONLY_OCCURRENCE_BP2_E2",
         "consumed_state_hash": custody["consumed_state_hash"]},
        {"stage": "BP4_C10_COUPLED_READ", "receipt_hash":
         receipt["a0"]["claim_hashes"][0],
         "actor_world_clock": receipt["a0"]["clock"]},
        {"stage": "BP4_C12_ROOT_CHECKPOINT", "branch_id": "root",
         "world_clock": receipt["a0"]["clock"],
         "practice_target_ref": receipt["practice"]["source_target_ref"]},
        {"stage": "BP4_M6_ACTOR_SAFE_CLAIM", "claim_kinds": receipt["a0"]["claims"],
         "claim_hashes": receipt["a0"]["claim_hashes"]},
        {"stage": "A0_ENCOUNTER_OBSERVATION", "clock": receipt["a0"]["clock"],
         "position": receipt["a0"]["position"],
         "practice_label": receipt["a0"]["projects"][0]["practice_label"]},
        {"stage": "A2_OFFSCREEN_LIFE", "event_id": receipt["a2"]["offscreen_event_id"],
         "event_hash": receipt["a2"]["offscreen_event_hash"],
         "completed_units": receipt["a2"]["other_completed_units"]},
        {"stage": "A2_M6_HIDDEN_BEFORE_ATTEND",
         "state": receipt["a2"]["m6_hidden_before_attend"]["state"],
         "code": receipt["a2"]["m6_hidden_before_attend"]["code"]},
        {"stage": "A2_REENTRY", "claims": receipt["a2"]["reentry_claim_kinds"],
         "target_id": receipt["a2"]["reentry_target"]},
    ]
    links = [
        {"from": "BP1 histories", "to": "BP2 C8 occurrence",
         "check": "actor/other source + snapshot hashes and BP1 causal parents inside the committed payload"},
        {"from": "BP2 C8 occurrence", "to": "BP2 E1",
         "check": "E1 content hash carries occurrence id, C8 state digest and commit receipt id"},
        {"from": "BP2 E1", "to": "BP2 CAN008 RULE_A",
         "check": "response receipt hash over the E1 event hash, rule and conditioning readset"},
        {"from": "BP2 CAN008 RULE_A", "to": "BP2 CAN011 RULE_T",
         "check": "target dependency hash equals the response-rule content hash"},
        {"from": "BP2 CAN011 RULE_T/grant", "to": "BP2 C9 target commit",
         "check": "sealed record embeds response hash, permission ref and authorization digest"},
        {"from": "BP2 C9 target commit", "to": "BP2 independent E2",
         "check": "E2 receipt consumed_state_hash equals the committed record digest"},
        {"from": "BP2 C9 target + E2", "to": "BP4 C10",
         "check": "BP4 re-verifies the C8 keyed proof/OUT9, the sealed target row digest and both BP1 snapshots"},
        {"from": "BP2 target + E2", "to": "BP4 C12 practice",
         "check": "practice materialized from the committed target and the performed E2 act"},
        {"from": "BP4 C12 world", "to": "BP4 M6 claim",
         "check": "only actor-perceived events become claims; unperceived offscreen event is NONRENDERABLE"},
        {"from": "BP4 C12 world time", "to": "A2 offscreen life",
         "check": "offscreen REPAIR at world clock 40 uses the workshop tool available from the BP2 E2"},
    ]
    document = {
        "schema": "BP2P4J_CROSS_DOMAIN_CUSTODY@1",
        "steps": steps,
        "verified_links": links,
        "summary": {
            "target_id": custody["target_id"],
            "consumed_state_hash": custody["consumed_state_hash"],
            "c8_state_digest": custody["c8_state_digest"],
            "e2_receipt_hash": custody["e2_receipt_hash"],
            "a0_claim_hashes": receipt["a0"]["claim_hashes"],
            "a2_offscreen_event_id": receipt["a2"]["offscreen_event_id"],
        },
    }
    _json(EVIDENCE / "custody_ledger.json", document)
    return document


def _alternatives(fresh_root: Path) -> dict:
    from bp2_joined.producer import JoinedProducer

    bp2_alternatives = {}
    for name, sever in (("no_change", "RULE_A_REGISTRY_EMPTY"),
                        ("deny", "RULE_T_SELF_ISSUED")):
        root = fresh_root / ("bp2_" + name)
        producer = JoinedProducer(root)
        outcome = producer.run(sever=sever)
        pipeline = producer.pipeline
        bp2_alternatives[name] = {
            "ok": outcome.ok,
            "stage": outcome.stage_reached,
            "failure_code": outcome.failure_code,
            "target_branch": pipeline.decision.branch.value if pipeline and pipeline.decision else "",
            "target_reason": pipeline.decision.reason.value if pipeline and pipeline.decision else "",
            "response_status": pipeline.response.status.value if pipeline and pipeline.response else "",
            "target_rows": producer.c9.db.execute("SELECT count(*) FROM target_state").fetchone()[0],
            "occurrence_rows": producer.c9.db.execute("SELECT count(*) FROM occurrence").fetchone()[0],
        }
        producer.close()

    artifacts = reunion.build_fresh(fresh_root / "alt_join")
    product = JoinedProduct(fresh_root / "alt_product", artifacts=artifacts)
    try:
        inspect_result = product.inspect()
        attend_result = product.attend()
        repairs = []
        repair_exhausted = None
        for _ in range(10):
            result = product.repair()
            repairs.append(result)
            if result.get("status") == "DENY":
                repair_exhausted = result
                break
        repair_first = repairs[0] if repairs else {}
        travel_deny = product.travel("nowhere")
        travel_market = product.travel("market")
        repair_wrong_place = product.repair()
        address_deny = product.address_other("Are you there?")
        product_state = product.joined_source()
    finally:
        product.close()
    e2_absent = JoinedProduct(fresh_root / "alt_no_e2", artifacts=artifacts, e2=None)
    try:
        no_e2_a0 = e2_absent.observe()
        no_e2_wait = e2_absent.wait(30)
        e2_absent_event = e2_absent.store.world_event(
            "root", no_e2_wait["offscreen_events"][-1])
        no_e2_other = e2_absent.other()
    finally:
        e2_absent.close()
    document = {
        "schema": "BP2P4J_ALTERNATIVES@1",
        "bp2_no_change": bp2_alternatives["no_change"],
        "bp2_deny": bp2_alternatives["deny"],
        "product_no_change": {
            "inspect": inspect_result,
            "attend": attend_result,
        },
        "product_deny": {
            "repair_material_exhausted": repair_exhausted or {"status": "NOT_REACHED"},
            "travel_unknown_location": travel_deny,
            "repair_wrong_location": repair_wrong_place,
            "address_absent_other": address_deny,
        },
        "product_positive": {
            "repair_calls": len(repairs),
            "repair_first": repair_first,
            "travel_to_market": travel_market,
            "practice_label": product_state["practice"]["practice_label"],
        },
        "no_performed_e2_alternative": {
            "a0_e2_admitted": no_e2_a0["c9"]["e2_admitted"],
            "a0_projects": no_e2_a0["self"]["state"]["projects"],
            "a0_tools_remaining": no_e2_a0["self"]["state"]["tools_remaining"],
            "offscreen_kind": e2_absent_event["kind"],
            "offscreen_completed_units": no_e2_other["public"]["completed_units"],
            "note": "same committed target, E2 not performed: no practice, no tool, "
                    "and the offscreen life becomes a lawful NO_CHANGE",
        },
    }
    _json(EVIDENCE / "alternatives_receipt.json", document)
    return document


def _severances(fresh_root: Path, intact) -> dict:
    trials = run_all_severances(fresh_root / "severance", intact)
    receipt = severance_receipt(trials)
    receipt["declared_edges"] = list(SEVERANCE_EDGES)
    receipt["declared_supplementary"] = list(SUPPLEMENTARY_EDGES)
    receipt["cut_descriptions"] = EDGE_CUT_DESCRIPTION
    _json(EVIDENCE / "severance_receipt.json", receipt)
    return receipt


def _cold_and_fork(fresh_root: Path, intact) -> dict:
    root = fresh_root / "cold"
    product = JoinedProduct(root, artifacts=intact)
    product.say("cold probe utterance")
    product.wait(30)
    before = product.observe()
    product.close()
    second = subprocess.run(
        [sys.executable, str(RETURN / "run_joined.py"), "--root", str(root),
         "observe"],
        capture_output=True, text=True, cwd=str(RETURN), env=_env())
    after = json.loads(second.stdout) if second.returncode == 0 else {}
    document = {
        "schema": "BP2P4J_COLD_REENTRY@1",
        "returncode": second.returncode,
        "stderr": second.stderr[-500:],
        "before": {"clock": before["clock"], "claims": [c["kind"] for c in before["claims"]],
                   "c9_target_id": before["c9"]["target_id"],
                   "c9_state_hash": before["c9"]["state_hash"],
                   "c8_state_digest": before["c8"]["state_digest"]},
        "after": {"clock": after.get("clock"),
                  "claims": [c["kind"] for c in after.get("claims", [])],
                  "c9_target_id": after.get("c9", {}).get("target_id"),
                  "c9_state_hash": after.get("c9", {}).get("state_hash"),
                  "c8_state_digest": after.get("c8", {}).get("state_digest")},
        "equal": bool(after) and before["clock"] == after["clock"]
        and [c["kind"] for c in before["claims"]] == [
            c["kind"] for c in after.get("claims", [])]
        and before["c9"]["target_id"] == after["c9"]["target_id"],
    }
    _json(EVIDENCE / "cold_reentry.json", document)

    fork_root = fresh_root / "fork"
    product = JoinedProduct(fork_root, artifacts=intact)
    try:
        product.say("branch point")
        fork = product.fork("branch_leave")
        product.use("branch_leave")
        product.leave_tool()
        product.wait(30)
        leave = product.other()
        product.use("root")
        product.take_tool()
        product.wait(30)
        take = product.other()
        shared = product.store.shared_root_equal("branch_leave", "root")
    finally:
        product.close()
    fork_doc = {
        "schema": "BP2P4J_FORK@1",
        "fork": fork,
        "shared_root_equal": shared["equal"],
        "leave_branch_completed_units": leave["public"]["completed_units"],
        "take_branch_completed_units": take["public"]["completed_units"],
        "leave_public_events": leave["public"]["public_work_events"],
        "take_public_events": take["public"]["public_work_events"],
        "divergent": leave["public"]["completed_units"] != take["public"]["completed_units"],
    }
    _json(EVIDENCE / "fork_receipt.json", fork_doc)
    return {"cold": document, "fork": fork_doc}


def _security(fresh_root: Path, intact) -> dict:
    from bp2p4.c12_verify import chain_digest, upstream_verify_defect, verify_branch_chain

    product = JoinedProduct(fresh_root / "security", artifacts=intact)
    try:
        product.say("security probe")
        chain_before = chain_digest(product.store, "root")
        verify = verify_branch_chain(product.store, "root")
        upstream = upstream_verify_defect(product.store, "root")
        db_path = product.store.path
    finally:
        product.close()
    document = {
        "schema": "BP2P4J_SECURITY_RECEIPT@1",
        "closed_in_candidate": [
            "shape-valid envelope with unbacked BP2 identities refused",
            "native-smuggling envelope refused",
            "self-actuator and self-occurrence E2 refused",
            "forged world owner receipt refused",
            "C12 append-only triggers refuse UPDATE/DELETE",
            "retroactive and future-child rows refused",
            "forged actor perception caught by the same A0/A2 assertion",
            "BP4 C10 refuses a tampered sealed target preimage",
        ],
        "typed_residuals": [
            "raw SQLite access can DROP the C12 append-only trigger and delete rows; "
            "remaining rows stay valid and completeness is only detectable against an "
            "out-of-band chain digest",
            "BP4 C12Store.verify recomputes digest(body) including the body hash, so "
            "it reports false errors on intact rows; this return verifies independently",
            "BP2 C8 key/anchor remain TEST_ONLY fixtures, not production KMS",
            "no ADP019 admission, native rule, native E2 or native actor",
        ],
        "independent_chain_verify": verify,
        "upstream_verify_defect": upstream,
        "chain_digest_before_attack": chain_before,
        "c12_db_path": str(db_path),
    }
    _json(EVIDENCE / "security_receipt.json", document)
    return document


def _clock_docket(positive: dict, literal: dict | None) -> dict:
    document = {
        "schema": "BP2P4J_CLOCK_DOCKET@1",
        "domains": {
            "bp2": {
                "name": "BP2_TEST_ONLY_LOGICAL_CLOCK",
                "event_time": 202,
                "target_commit_time": 202,
                "e2_action_time": 217,
                "authority": "TEST_ONLY_FIXTURE_CLOCK_NOT_TRUSTED_TIME",
            },
            "bp4": {
                "name": "BP4_TEST_ONLY_WORLD_CLOCK",
                "origin": 10,
                "offscreen_event_clock": 40,
                "authority": "TEST_ONLY_SOURCEFREE_WORLD_CLOCK",
            },
        },
        "relation": "DECLARED_PROCESS_ORDER_NOT_NUMERIC_COMPARISON",
        "numeric_ordering_used": False,
        "process_order": positive["custody"]["clock"]["process_order"],
        "declared_bridge": positive["custody"]["clock"],
        "time_coordinate_hold": (
            "an existing C12 root without the post-BP2 world-root marker is refused "
            "with TIME_COORDINATE_HOLD"),
        "literal_origin_present": literal is not None,
    }
    _json(EVIDENCE / "clock_docket.json", document)
    return document


def _not_run() -> dict:
    return {
        "schema": "BP2P4J_NOT_RUN_INVENTORY@1",
        "not_run": [
            {"item": "native Pyat N11/N12 world", "owner": "Pyat HQ",
             "reason": "user STOP on R53 J52/W52 not waived; no source/workaround authority"},
            {"item": "native ADP007/010/015/016/017/019/020",
             "owner": "respective ADP owners", "reason": "no native receipts issued"},
            {"item": "native CAN008 RULE_A / CAN011 RULE_T",
             "owner": "competent rule issuers", "reason": "TEST_ONLY rules only"},
            {"item": "native performed E2", "owner": "independent actuator owner",
             "reason": "TEST_ONLY declared actuator"},
            {"item": "C8 D1/D2/D3 production writer/key/anchor/admission",
             "owner": "C8 owners", "reason": "TEST_ONLY key, path-bound journal, no ADP019"},
            {"item": "C11 native weld and native C12 person", "owner": "C11/C12 authorities",
             "reason": "not attempted"},
            {"item": "A4/A5 human validation", "owner": "product owner",
             "reason": "outside L1 technical alpha"},
            {"item": "literal BP2 origin runtime", "owner": "local artifact",
             "reason": "local-only; absent in a fresh clone, recorded as NOT_RUN there"},
            {"item": "raw original35 respondent data", "owner": "source custodian",
             "reason": "no permission; never accessed"},
        ],
    }


def _native_gap() -> dict:
    return {
        "schema": "BP2P4J_NATIVE_FUNCTIONAL_GAP@1",
        "epistemic_rule": "input -> authenticating decision -> receipt -> consumer -> scientific effect",
        "gaps": [
            {"function": "world/opportunity", "owner": "Pyat N11/N12 + ADP010",
             "receipt": "source-qualified world/encounter", "consumer": "BP4 world root",
             "current": "TEST_ONLY_SOURCEFREE_WORLD"},
            {"function": "actor genesis/other", "owner": "ADP007/ADP015",
             "receipt": "actor and independent other", "consumer": "BP1 histories",
             "current": "TEST_ONLY_BP1_FIXTURES"},
            {"function": "occurrence admission", "owner": "ADP019",
             "receipt": "external admission", "consumer": "BP2 E1",
             "current": "ADP019_ADMISSION_RECEIPT_ABSENT"},
            {"function": "response/target rules", "owner": "CAN008/CAN011",
             "receipt": "concrete RULE_A and RULE_T/grant", "consumer": "BP2 C9",
             "current": "TEST_ONLY_ONLY"},
            {"function": "performed E2", "owner": "native actuator owner",
             "receipt": "performed action owner receipt", "consumer": "BP2 later E2",
             "current": "TEST_ONLY_ACTUATOR"},
            {"function": "trusted journal", "owner": "C8 D1/D2/D3",
             "receipt": "cutover + KMS/anchor + admission", "consumer": "BP2 C8/OUT9",
             "current": "TEST_ONLY_KEY_AND_PATH_BOUND_JOURNAL"},
            {"function": "memory/access", "owner": "ADP016/ADP017",
             "receipt": "memory and access receipts", "consumer": "BP4 M6 claims",
             "current": "C12_LOCAL_PERCEPTION_ONLY"},
            {"function": "native person", "owner": "C11/C12",
             "receipt": "weld and generated person", "consumer": "A0-A5 product",
             "current": "NOT_ATTEMPTED"},
        ],
    }


def _authority_holds() -> dict:
    return {
        "schema": "BP2P4J_AUTHORITY_HOLD_REGISTER@1",
        "holds": [
            {"authority": "Pyat N11/N12 world and original35", "status": "HOLD",
             "note": "user STOP R53 J52/W52 respected"},
            {"authority": "ADP007 actor, ADP015 other", "status": "HOLD"},
            {"authority": "ADP010 opportunity/encounter", "status": "HOLD"},
            {"authority": "ADP019 admission", "status": "HOLD"},
            {"authority": "ADP016 memory / ADP017 access", "status": "HOLD"},
            {"authority": "CAN008 RULE_A", "status": "HOLD"},
            {"authority": "CAN011 RULE_T + grant", "status": "HOLD"},
            {"authority": "native performed E2", "status": "HOLD"},
            {"authority": "C8 D1/D2/D3", "status": "HOLD"},
            {"authority": "C11 weld", "status": "HOLD"},
            {"authority": "native C12 person", "status": "HOLD"},
            {"authority": "A4/A5 human validation", "status": "HOLD"},
        ],
        "self_adoption": False,
    }


def _gap_table() -> dict:
    return {
        "schema": "BP2P4J_SOURCE_ACTOR_PERFORMER_CLOCK_GAP@1",
        "rows": [
            {"dimension": "source", "test_only": "BP1 fixture actors + G18 material receipts",
             "native": "Pyat source-qualified world", "owner": "Pyat HQ", "status": "HOLD"},
            {"dimension": "actor", "test_only": "two distinct TEST_ONLY_BP1 actor histories",
             "native": "ADP007 genesis + ADP015 other", "owner": "ADP007/ADP015",
             "status": "HOLD"},
            {"dimension": "event", "test_only": "TEST_ONLY C8 occurrence + TEST_ONLY E1",
             "native": "ADP019 admitted occurrence", "owner": "ADP019", "status": "HOLD"},
            {"dimension": "rule", "test_only": "TEST_ONLY CAN008/CAN011 rules",
             "native": "issued RULE_A and RULE_T/grant", "owner": "CAN008/CAN011",
             "status": "HOLD"},
            {"dimension": "performer", "test_only": "TEST_ONLY_ACTUATOR_BP2_INDEPENDENT",
             "native": "native actuator/occurrence owner", "owner": "action owner",
             "status": "HOLD"},
            {"dimension": "clock", "test_only": "two declared logical domains with process-order bridge",
             "native": "trusted time and source-authorized as-of", "owner": "C8/ADP019",
             "status": "HOLD"},
            {"dimension": "writer", "test_only": "TEST_ONLY HMAC key + path-bound journal",
             "native": "C8 D1 cutover and D2 KMS/anchor", "owner": "C8 D1/D2",
             "status": "HOLD"},
            {"dimension": "person", "test_only": "C12 technical continuation over TEST_ONLY state",
             "native": "pipeline-generated C12 person", "owner": "C11/C12",
             "status": "HOLD"},
        ],
    }


def _privacy_law() -> dict:
    return {
        "schema": "BP2P4J_PRIVACY_AND_LAW@1",
        "raw_respondent_data_accessed": False,
        "original35_accessed": False,
        "pyat_native_world_accessed": False,
        "production_installation": False,
        "upstream_edits": [],
        "upstream_tests_edited": [],
        "actor_identifiers": "TEST_ONLY_BP1_ACTOR_A/B fixtures, not real persons",
        "cryptography": "TEST_ONLY HMAC key file; not a production key",
        "native_authority_issued": False,
        "pyat_stop_respected": True,
    }


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    manifest = bp2p4.verify_sources()
    _json(EVIDENCE / "environment_passport.json", _environment_passport())
    _json(EVIDENCE / "source_manifest_summary.json", _source_summary())

    fresh_root = _fresh("main")
    intact, positive = _positive(fresh_root)
    literal = _literal(fresh_root)
    _custody_ledger(positive)
    _alternatives(fresh_root)
    _severances(fresh_root, intact)
    _cold_and_fork(fresh_root, intact)
    _security(fresh_root, intact)
    _clock_docket(positive, literal)
    _json(EVIDENCE / "not_run_inventory.json", _not_run())
    _json(EVIDENCE / "native_functional_gap.json", _native_gap())
    _json(EVIDENCE / "authority_hold_register.json", _authority_holds())
    _json(EVIDENCE / "source_actor_performer_clock_gap.json", _gap_table())
    _json(EVIDENCE / "privacy_and_law.json", _privacy_law())

    demo = subprocess.run(
        [sys.executable, str(RETURN / "run_joined.py"), "--root",
         str(fresh_root / "cli_demo"), "demo"],
        capture_output=True, text=True, cwd=str(RETURN), env=_env())
    (LOGS / "cli_demo.log").write_text(
        (demo.stdout or "") + (demo.stderr or ""), encoding="utf8")
    _json(EVIDENCE / "cli_demo.json", {
        "schema": "BP2P4J_CLI_DEMO@1",
        "returncode": demo.returncode,
        "log": "evidence/logs/cli_demo.log",
        "stdout_bytes": len(demo.stdout or ""),
    })

    new_courts = _new_courts()
    originals = _original_courts()
    results = {
        "schema": "BP2P4J_COURT_RESULTS@1",
        "manifest_file_count": manifest["file_count"],
        "new_courts": new_courts,
        "original_courts": originals,
        "literal_origin_ran": literal is not None,
        "all_green": all(row["returncode"] == 0 for row in new_courts.values())
        and all(row["returncode"] == 0 for row in originals.values()),
    }
    _json(EVIDENCE / "court_results.json", results)
    print(json.dumps({
        "manifest": manifest["file_count"],
        "literal_origin": literal is not None,
        "all_green": results["all_green"],
        "new": {name: row["counts"] for name, row in new_courts.items()},
        "original": {name: row["counts"] for name, row in originals.items()},
    }, sort_keys=True, default=str))
    return 0 if results["all_green"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
