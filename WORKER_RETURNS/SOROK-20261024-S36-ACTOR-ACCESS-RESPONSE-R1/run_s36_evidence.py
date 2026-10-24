"""Generate S36 vector, refusal, legacy, source and same-assertion fault evidence."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

RET = Path(__file__).resolve().parent
EVID = RET / "evidence"
JUNIT = RET / "junit"
LOGS = RET / "logs"
PY = sys.executable
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
ENV["PYTHONPATH"] = os.pathsep.join([str(RET), str(RET / "runtime" / "native")])
for path in (str(RET), str(RET / "runtime" / "native")):
    if path not in sys.path:
        sys.path.insert(0, path)

from candidate import CandidateStore, ResponseRuleRegistry, TargetRuleRegistry, valid
from candidate.actor_access_response import (
    AMBIGUOUS_CONTRADICTORY,
    OBSERVED_CURRENT_REFUSAL,
    OBSERVED_IMMEDIATE_OBJECT_ORIENTATION,
    RECEIVABLE_NO_OBSERVED_UPTAKE,
    UNKNOWN_RECEIVABILITY,
)
from s36_harness import (
    LEGACY_HISTORY,
    committed_response,
    legacy_two_history_response,
    refusal_case,
    run_s35_case,
)

PINNED_C9R = "6fa2939972ce5a2c0cc4f2b033946b276f1c2934"
PINNED_PREFIX = (
    "WORKER_RETURNS/SOROK-20261019-C9R-WHOLE-ACTOR-BOUNDARY-AND-CONSUMER-REPAIR-R1"
)
PINNED_CANDIDATE_FILES = [
    "candidate/__init__.py",
    "candidate/action_admission.py",
    "candidate/canon.py",
    "candidate/conditioning.py",
    "candidate/events.py",
    "candidate/identity.py",
    "candidate/later_action.py",
    "candidate/native_custody.py",
    "candidate/pipeline.py",
    "candidate/release_gate.py",
    "candidate/response_rules.py",
    "candidate/target_rules.py",
    "candidate/transaction.py",
]
PINNED_NATIVE_FILES = [
    "runtime/native/rawlsing_next/v3_psepf_zero_positive_guard.py",
    "runtime/native/rawlsing_next/wsc_gt0_protocol.py",
    "runtime/native/rawlsing_next/wsc_gt0_v3_runtime.py",
]
NEW_FILES = [
    ".gitignore",
    "candidate/actor_access_response.py",
    "s36_harness.py",
    "run_s36_evidence.py",
    "tests/conftest.py",
    "tests/test_s36_vectors.py",
    "tests/test_s36_refusals.py",
    "tests/test_s36_faults_and_legacy.py",
]
REFUSAL_CASES = [
    "access_wrong_actor",
    "access_wrong_event",
    "access_wrong_source_hash",
    "access_wrong_scene",
    "access_before_event",
    "access_after_as_of",
    "access_revoked_field",
    "access_revoked_source",
    "access_bad_namespace",
    "response_wrong_actor",
    "response_wrong_event",
    "response_wrong_source_hash",
    "response_before_access",
    "response_after_as_of",
    "response_revoked_field",
    "response_revoked_source",
    "response_bad_kind",
    "response_bad_namespace",
]


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _run(cmd, *, log_name: str):
    proc = subprocess.run(
        cmd,
        cwd=str(RET),
        env=ENV,
        capture_output=True,
        text=True,
    )
    (LOGS / log_name).write_text(proc.stdout + proc.stderr)
    return proc


def _junit_counts(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    tests = sum(int(s.attrib.get("tests", 0)) for s in suites)
    failures = sum(int(s.attrib.get("failures", 0)) for s in suites)
    errors = sum(int(s.attrib.get("errors", 0)) for s in suites)
    skips = sum(int(s.attrib.get("skipped", 0)) for s in suites)
    cases = []
    for case in root.iter("testcase"):
        status = "PASS"
        if case.find("failure") is not None:
            status = "RED"
        elif case.find("error") is not None:
            status = "ERROR"
        elif case.find("skipped") is not None:
            status = "SKIP"
        cases.append(
            {
                "classname": case.attrib.get("classname", ""),
                "name": case.attrib.get("name", ""),
                "status": status,
            }
        )
    return {
        "tests": tests,
        "PASS": tests - failures - errors - skips,
        "RED": failures,
        "ERROR": errors,
        "SKIP": skips,
        "cases": cases,
    }


def _record(label: str, expected: str, result, event, store: CandidateStore) -> dict:
    response_ref = result.receipt.response_ref if result.receipt else ""
    body = committed_response(store, response_ref) if response_ref else None
    return {
        "id": label,
        "expected": expected,
        "event_id": event["event_id"],
        "event_hash": event["hash"],
        "event_time": event["time"],
        "response_status": result.response.status.value,
        "response_outcome": result.response.reason,
        "response_route": result.response.candidate_route,
        "response_receipt_hash": result.response.receipt_hash,
        "target_proposal_count": len(result.response.target_proposals),
        "uptake_refs": list(result.response.uptake_refs),
        "recruited_refs": list(result.response.recruited_refs),
        "declared_history_refs": list(result.response.declared_history_refs),
        "target_branch": result.decision.branch.value if result.decision else None,
        "target_reason": result.decision.reason.value if result.decision else None,
        "target_id": result.decision.target_id if result.decision else "",
        "target_record_hash": result.decision.record_hash if result.decision else "",
        "committed": result.committed,
        "no_ghost": result.no_ghost,
        "committed_target_ids": sorted(store.committed_target_ids()),
        "response_ref": response_ref,
        "committed_response_body": body,
        "s35_receipt": body.get("s35_receipt") if body else None,
        "s35_receipt_valid": bool(body and body.get("s35_receipt") and valid(dict(body["s35_receipt"]))),
    }


def vector_cases(root: Path) -> list[dict]:
    cases: list[dict] = []

    def run(label: str, expected: str, extra: dict | None = None, **kwargs):
        with CandidateStore(root / f"{label}.sqlite") as store:
            result, event = run_s35_case(store, **kwargs)
            record = _record(label, expected, result, event, store)
            if extra:
                record.update(extra)
            cases.append(record)

    run(
        "P1_OBSERVED_IMMEDIATE_POSITIVE",
        "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION; target_proposals=0; NO_CHANGE/NO_PROPOSAL",
    )
    run(
        "N1_B_SHARE_BUT_A_UNAWARE",
        "UNKNOWN_RECEIVABILITY; response effect valid empty; NO_CHANGE/NO_PROPOSAL",
        extra={"actor_access": "NOT_WITNESSED", "objective_material": True},
        access=None,
    )
    run(
        "N2_CONTRARY_PROJECT_NO_RESPONSE",
        "AMBIGUOUS_CONTRADICTORY; response effect valid empty; NO_CHANGE/NO_PROPOSAL",
        extra={
            "contradictory_context": True,
            "contradictory_refs": ["TEST_ONLY_S36_CONTRARY_PROJECT"],
        },
        response=None,
        contradictory_context=True,
        contradictory_refs=("TEST_ONLY_S36_CONTRARY_PROJECT",),
    )
    run(
        "N3A_B_SHARE_SAME_PUBLIC_REFUSAL",
        "OBSERVED_CURRENT_REFUSAL; B private cause not inferred; NO_CHANGE",
        extra={
            "b_act": "SHARE_TOOL",
            "response_witness_content": {
                "public_surface": "HELP_REFUSE_DUE_TO_CURRENT_TOOL_SHORTAGE",
                "actor_knows_b_motive": False,
            },
        },
        event_id="TEST_ONLY_S36_N3_SHARE",
        b_act="SHARE_TOOL",
        response_kwargs={
            "response_ref": "TEST_ONLY_S36_A_EXPLICIT_REFUSAL",
            "response_kind": "EXPLICIT_REFUSAL",
            "content": {
                "public_surface": "HELP_REFUSE_DUE_TO_CURRENT_TOOL_SHORTAGE",
                "actor_knows_b_motive": False,
            },
        },
    )
    run(
        "N3B_B_REFUSE_SAME_PUBLIC_REFUSAL",
        "OBSERVED_CURRENT_REFUSAL; B private cause not inferred; NO_CHANGE",
        extra={
            "b_act": "REFUSE_TOOL",
            "response_witness_content": {
                "public_surface": "HELP_REFUSE_DUE_TO_CURRENT_TOOL_SHORTAGE",
                "actor_knows_b_motive": False,
            },
        },
        event_id="TEST_ONLY_S36_N3_REFUSE",
        b_act="REFUSE_TOOL",
        response_kwargs={
            "response_ref": "TEST_ONLY_S36_A_EXPLICIT_REFUSAL",
            "response_kind": "EXPLICIT_REFUSAL",
            "content": {
                "public_surface": "HELP_REFUSE_DUE_TO_CURRENT_TOOL_SHORTAGE",
                "actor_knows_b_motive": False,
            },
        },
    )
    run(
        "N4A_LABEL_BASELINE",
        "P1 decision identical with fixed actor/event/access/action/world",
    )
    run(
        "N4B_LABEL_ONLY_PERTURBATION",
        "P1 decision identical with fixed actor/event/access/action/world",
        extra={
            "actor_labels": {
                "class_label": "TEST_ONLY_CLASS_LABEL",
                "demographic_label": "TEST_ONLY_DEMOGRAPHIC_LABEL",
                "Enneagram_label": "TEST_ONLY_ENNEAGRAM_LABEL",
            }
        },
        actor_labels={
            "class_label": "TEST_ONLY_CLASS_LABEL",
            "demographic_label": "TEST_ONLY_DEMOGRAPHIC_LABEL",
            "Enneagram_label": "TEST_ONLY_ENNEAGRAM_LABEL",
        },
    )
    run(
        "N5A_HISTORY_NO_CURRENT_ACCESS",
        "UNKNOWN_RECEIVABILITY based on current access only; NO_CHANGE",
        extra={"history_refs": list(LEGACY_HISTORY)},
        history=LEGACY_HISTORY,
        access=None,
        response=None,
    )
    run(
        "N5B_HISTORY_WITH_CURRENT_WITNESS",
        "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION from current access/response only; NO_CHANGE",
        extra={"history_refs": list(LEGACY_HISTORY)},
        history=LEGACY_HISTORY,
    )
    return cases


def refusal_evidence(root: Path) -> list[dict]:
    rows = []
    for case in REFUSAL_CASES:
        access, response, revoked = refusal_case(case)
        with CandidateStore(root / f"refusal_{case}.sqlite") as store:
            result, _ = run_s35_case(
                store,
                access=access,
                response=response,
                revoked_source_refs=revoked,
            )
            rows.append(
                {
                    "case": case,
                    "response_status": result.response.status.value,
                    "response_reason": result.response.reason,
                    "target_proposal_count": len(result.response.target_proposals),
                    "decision": None if result.decision is None else result.decision.branch.value,
                    "committed": result.committed,
                    "no_ghost": result.no_ghost,
                    "tables_empty": all(not rows for rows in store.snapshot().values()),
                }
            )
    with CandidateStore(root / "refusal_unbound_contrary.sqlite") as store:
        result, _ = run_s35_case(
            store,
            contradictory_context=True,
            contradictory_refs=(),
        )
        rows.append(
            {
                "case": "contradictory_context_unbound",
                "response_status": result.response.status.value,
                "response_reason": result.response.reason,
                "target_proposal_count": len(result.response.target_proposals),
                "decision": None if result.decision is None else result.decision.branch.value,
                "committed": result.committed,
                "no_ghost": result.no_ghost,
                "tables_empty": all(not rows for rows in store.snapshot().values()),
            }
        )
    return rows


def legacy_evidence(root: Path) -> dict:
    legacy, _ = legacy_two_history_response()
    with CandidateStore(root / "legacy_probe.sqlite") as store:
        s35, event = run_s35_case(store, history=LEGACY_HISTORY)
    return {
        "legacy_two_history_response": {
            "status": legacy.status.value,
            "proposal_count": len(legacy.target_proposals),
            "proposal_operation": legacy.target_proposals[0].get("operation")
            if legacy.target_proposals
            else None,
            "declared_history_refs": list(legacy.declared_history_refs),
            "note": "Existing evaluate_response adapter preserved and isolated from S35 route.",
        },
        "s35_two_history_response": {
            "event_hash": event["hash"],
            "response_status": s35.response.status.value,
            "response_outcome": s35.response.reason,
            "proposal_count": len(s35.response.target_proposals),
            "declared_history_refs": list(s35.response.declared_history_refs),
            "target_branch": s35.decision.branch.value,
            "target_reason": s35.decision.reason.value,
            "committed_target_ids": [],
            "note": "S35 route never falls back to the legacy two-history CREATE proposal.",
        },
        "native_registries": {
            "response_rule_entries": len(ResponseRuleRegistry.production().rules),
            "target_rule_entries": len(TargetRuleRegistry.production().rules),
        },
    }


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=str(RET),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def source_manifest() -> dict:
    pinned = []
    changed = []
    exact = []
    for rel in PINNED_CANDIDATE_FILES + PINNED_NATIVE_FILES:
        pinned_blob = _git("rev-parse", f"{PINNED_C9R}:{PINNED_PREFIX}/{rel}")
        local_path = RET / rel
        local_blob = _git("hash-object", str(local_path))
        sha256 = hashlib.sha256(local_path.read_bytes()).hexdigest()
        row = {
            "path": rel,
            "pinned_git_blob_sha1": pinned_blob,
            "local_git_blob_sha1": local_blob,
            "local_sha256": sha256,
        }
        if pinned_blob == local_blob:
            exact.append(row)
        else:
            changed.append(row)
        pinned.append(row)
    new = []
    for rel in NEW_FILES:
        local_path = RET / rel
        new.append(
            {
                "path": rel,
                "local_git_blob_sha1": _git("hash-object", str(local_path)),
                "local_sha256": hashlib.sha256(local_path.read_bytes()).hexdigest(),
            }
        )
    return {
        "schema": "SOROK_S36_SOURCE_MANIFEST@1",
        "pinned_c9r_commit": PINNED_C9R,
        "pinned_prefix": PINNED_PREFIX,
        "pinned_files": pinned,
        "byte_exact_files": exact,
        "changed_files": changed,
        "new_files": new,
        "changed_change_notes": {
            "candidate/pipeline.py": (
                "Additive s35_request branch selects the S35 bridge; legacy evaluate_response "
                "path remains unchanged when s35_request is None; S35 refusals abort before "
                "occurrence/response/target commit; committed response body carries s35_receipt."
            ),
            "candidate/response_rules.py": (
                "Additive optional s35_receipt field on ResponseResult with default None; "
                "existing legacy response behavior unchanged."
            ),
        },
    }


def test_evidence() -> dict:
    xml = JUNIT / "s36_full.xml"
    proc = _run(
        [
            PY,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            f"--junitxml={xml}",
            "tests",
        ],
        log_name="s36_full.log",
    )
    counts = _junit_counts(xml)
    return {
        "schema": "SOROK_S36_TEST_RUN@1",
        "command": f"{PY} -B -m pytest -q -p no:cacheprovider --junitxml={xml} tests",
        "exit": proc.returncode,
        "junit": str(xml.relative_to(RET)),
        "counts": {key: counts[key] for key in ("tests", "PASS", "RED", "ERROR", "SKIP")},
        "cases": counts["cases"],
    }


def fault_trials() -> dict:
    target = RET / "candidate" / "actor_access_response.py"
    original = target.read_text()
    claims = [
        {
            "claim_id": "ACCESS_WITNESS_GATE",
            "positive_node": "tests/test_s36_vectors.py::test_p1_observed_immediate_positive_zero_proposals",
            "old": 'if access_status != "ACCESSIBLE":',
            "new": "if True:",
        },
        {
            "claim_id": "RESPONSE_WITNESS_GATE",
            "positive_node": "tests/test_s36_vectors.py::test_p1_observed_immediate_positive_zero_proposals",
            "old": "if response is None:",
            "new": "if True:",
        },
    ]
    trials = []
    for index, claim in enumerate(claims):
        if original.count(claim["old"]) != 1:
            raise RuntimeError(f"mutation not unique: {claim['claim_id']}")
        trial = {"claim_id": claim["claim_id"], "positive_node": claim["positive_node"], "phases": {}}
        for phase, mutate in (("positive", False), ("fault", True), ("restored", False)):
            xml = JUNIT / "faults" / f"{index:02d}_{claim['claim_id'].lower()}_{phase}.xml"
            if mutate:
                target.write_text(original.replace(claim["old"], claim["new"], 1))
            try:
                proc = _run(
                    [
                        PY,
                        "-B",
                        "-m",
                        "pytest",
                        "-q",
                        "-p",
                        "no:cacheprovider",
                        f"--junitxml={xml}",
                        claim["positive_node"],
                    ],
                    log_name=f"fault_{index:02d}_{phase}.log",
                )
            finally:
                target.write_text(original)
            counts = _junit_counts(xml)
            named = next(
                (
                    case
                    for case in counts["cases"]
                    if case["name"] == claim["positive_node"].split("::")[-1]
                ),
                None,
            )
            trial["phases"][phase] = {
                "exit": proc.returncode,
                "named_status": named["status"] if named else "MISSING",
                "junit": str(xml.relative_to(RET)),
            }
        trial["pass"] = (
            trial["phases"]["positive"]["named_status"] == "PASS"
            and trial["phases"]["fault"]["named_status"] == "RED"
            and trial["phases"]["restored"]["named_status"] == "PASS"
        )
        trials.append(trial)
    return {
        "schema": "SOROK_S36_SAME_ASSERTION_FAULTS@1",
        "mutation_scope": "candidate/actor_access_response.py only; restored in finally",
        "trials": trials,
        "all_pass": all(trial["pass"] for trial in trials),
    }


def main() -> None:
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    (JUNIT / "faults").mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="s36-evidence-", dir=str(RET / "runtime")))
    try:
        vectors = vector_cases(work)
        refusals = refusal_evidence(work)
        legacy = legacy_evidence(work)
        tests = test_evidence()
        faults = fault_trials()
        manifest = source_manifest()
        _write(
            EVID / "vectors.json",
            {
                "schema": "SOROK_S36_SIX_VECTOR_EXECUTION@1",
                "pinned_c9r_commit": PINNED_C9R,
                "cases": vectors,
            },
        )
        _write(
            EVID / "refusals.json",
            {
                "schema": "SOROK_S36_REFUSAL_EVIDENCE@1",
                "cases": refusals,
                "all_refused": all(
                    row["response_status"] == "REFUSED"
                    and row["target_proposal_count"] == 0
                    and row["committed"] is False
                    and row["no_ghost"] is True
                    and row["tables_empty"] is True
                    for row in refusals
                ),
            },
        )
        _write(EVID / "legacy_path.json", legacy)
        _write(EVID / "test_run.json", tests)
        _write(EVID / "fault_trials.json", faults)
        _write(EVID / "source_manifest.json", manifest)
        print(
            json.dumps(
                {
                    "vectors": len(vectors),
                    "refusals": len(refusals),
                    "tests": tests["counts"],
                    "faults_all_pass": faults["all_pass"],
                    "legacy_proposals": legacy["legacy_two_history_response"]["proposal_count"],
                    "s35_proposals": legacy["s35_two_history_response"]["proposal_count"],
                },
                sort_keys=True,
            )
        )
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
