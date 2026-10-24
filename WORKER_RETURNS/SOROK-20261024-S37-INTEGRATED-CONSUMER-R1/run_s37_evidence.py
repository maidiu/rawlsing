"""Generate S37 integrated-chain, boundary and source-root evidence."""
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
ENV["PYTHONPATH"] = str(RET)
if str(RET) not in sys.path:
    sys.path.insert(0, str(RET))
if str(RET / "tests") not in sys.path:
    sys.path.insert(0, str(RET / "tests"))

from s37.bootstrap import CUTS, origins, roots  # noqa: E402
from s37.harness import (  # noqa: E402
    NATIVE_SELF,
    TRIGGER,
    case_for,
    fresh_store,
    producer_for,
    setup_neutral_language,
    setup_source_language,
    source_for,
    start_session,
)
from s37.producer import IntegratedProducer  # noqa: E402
from candidate import CandidateStore, ResponseStatus, digest  # noqa: E402
from candidate.actor_access_response import (  # noqa: E402
    OBSERVED_IMMEDIATE_OBJECT_ORIENTATION,
    RECEIVABLE_NO_OBSERVED_UPTAKE,
    UNKNOWN_RECEIVABILITY,
)
from language_mediation.artifacts import (  # noqa: E402
    build_native_artifact,
    build_translation_artifact,
)
from language_mediation.equivalence import evaluate_pair  # noqa: E402
from firstclass import MaterialSourceRefusal  # noqa: E402

import test_s37_boundaries as boundary_helpers  # noqa: E402

PINNED_M35 = "4170fbf19a9d5a64bc728f5b22156bbffcec51e5"
PINNED_M35_PREFIX = "WORKER_RETURNS/SOROK-20261024-BP2-FIRSTCLASS-B-SOURCE-R1"
PINNED_S36 = CUTS["s36"]
PINNED_S36_PREFIX = "WORKER_RETURNS/SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1"
PINNED_LANGUAGE = CUTS["language"]
PINNED_LANGUAGE_PREFIX = "LANGUAGE_MEDIATION_R1"
PINNED_JOIN_E = CUTS["join_e"]
PINNED_JOIN_E_PREFIX = "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1"
M35_FILES = [
    "firstclass.py",
    "install.py",
    "candidate/vendor/bp2/bp2_joined/__init__.py",
    "candidate/vendor/bp2/bp2_joined/binding.py",
    "candidate/vendor/bp2/bp2_joined/bootstrap.py",
    "candidate/vendor/bp2/bp2_joined/material_source.py",
    "candidate/vendor/bp2/bp2_joined/ports.py",
    "candidate/vendor/bp2/bp2_joined/producer.py",
    "candidate/vendor/bp2/bp2_joined/scientific.py",
    "candidate/vendor/bp2/bp2_joined/severance.py",
]
S36_FILES = [
    "candidate/__init__.py",
    "candidate/action_admission.py",
    "candidate/actor_access_response.py",
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
LOCAL_FILES = [
    ".gitignore",
    "run_s37.py",
    "run_s37_evidence.py",
    "s37/__init__.py",
    "s37/bootstrap.py",
    "s37/harness.py",
    "s37/producer.py",
    "s37/product.py",
    "s37/reader.py",
    "s37/session.py",
    "tests/conftest.py",
    "tests/test_s37_integration.py",
    "tests/test_s37_boundaries.py",
]
LANGUAGE_FILES = [
    "language_mediation/session.py",
    "language_mediation/bootstrap.py",
    "language_mediation/plan.py",
    "language_mediation/index.py",
    "language_mediation/artifacts.py",
    "language_mediation/equivalence.py",
    "language_mediation/atoms.py",
]
JOIN_E_FILES = [
    "joined/session.py",
    "joined/refusal.py",
    "joined/lineage.py",
    "joined/provenance.py",
    "vendor/e/r31e/session.py",
    "vendor/e/r31e/expression.py",
    "vendor/e/vendor/r30a/r30a/first_session.py",
    "vendor/j/candidate/historical_actor_producer.py",
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=str(RET), capture_output=True, text=True, check=True
    ).stdout.strip()


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _run(cmd, log_name: str):
    proc = subprocess.run(
        cmd, cwd=str(RET), env=ENV, capture_output=True, text=True
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


def test_evidence() -> dict:
    xml = JUNIT / "s37_full.xml"
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
        "s37_full.log",
    )
    counts = _junit_counts(xml)
    return {
        "schema": "SOROK_S37_TEST_RUN@1",
        "command": f"{PY} -B -m pytest -q -p no:cacheprovider --junitxml={xml} tests",
        "exit": proc.returncode,
        "junit": str(xml.relative_to(RET)),
        "counts": {key: counts[key] for key in ("tests", "PASS", "RED", "ERROR", "SKIP")},
        "cases": counts["cases"],
    }


def chain_evidence(root: Path) -> dict:
    from run_s37 import run_one

    chains = [run_one(root, share=True), run_one(root, share=False)]
    return {
        "schema": "SOROK_S37_INTEGRATED_CHAINS@1",
        "grade": "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
        "native": False,
        "provider_calls": 0,
        "product_model_calls": 0,
        "chains": chains,
        "same_session_class": len({row["session_class"] for row in chains}) == 1,
        "same_reader_path": all(
            row["response_ref"] and row["c9_receipt_hash"] for row in chains
        ),
        "same_neutral_speech": chains[0]["language"]["native_text"]
        == chains[1]["language"]["native_text"]
        and chains[0]["language"]["english_text"]
        == chains[1]["language"]["english_text"],
        "share_tool": chains[0]["tools_remaining"] == 1,
        "refuse_tool": chains[1]["tools_remaining"] == 0,
        "both_no_target": all(
            row["target_branch"] == "NO_CHANGE"
            and row["target_reason"] == "NO_PROPOSAL"
            and row["target_state_rows"] == 0
            for row in chains
        ),
        "both_observed": all(
            row["outcome"]
            in {
                "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
                "OBSERVED_CURRENT_REFUSAL",
            }
            for row in chains
        ),
        "both_cold_verify": all(row["cold"]["verify_ok"] for row in chains),
    }


def boundary_evidence(root: Path) -> dict:
    producer, case, source = producer_for(root / "producer", share=True)
    try:
        c8 = producer.out9.readset["state_digest"]
        e1 = producer.e1_event["hash"]
        results: dict = {}
        with fresh_store(root / "positive.sqlite") as store:
            positive = producer.evaluate_s36(store=store)
        with fresh_store(root / "fault.sqlite") as store:
            fault = producer.evaluate_s36(store=store, access_witness=None)
        with fresh_store(root / "restored.sqlite") as store:
            restored = producer.evaluate_s36(store=store)
        results["access_fault_restore"] = {
            "c8_state_digest": c8,
            "e1_event_hash": e1,
            "positive": {
                "status": positive.response.status.value,
                "outcome": positive.response.reason,
                "target_proposals": len(positive.response.target_proposals),
                "target_branch": positive.decision.branch.value,
                "target_reason": positive.decision.reason.value,
            },
            "fault": {
                "status": fault.response.status.value,
                "outcome": fault.response.reason,
                "target_proposals": len(fault.response.target_proposals),
                "target_branch": fault.decision.branch.value,
                "target_reason": fault.decision.reason.value,
            },
            "restored": {
                "status": restored.response.status.value,
                "outcome": restored.response.reason,
                "target_proposals": len(restored.response.target_proposals),
                "target_branch": restored.decision.branch.value,
                "target_reason": restored.decision.reason.value,
            },
            "c8_unchanged": producer.out9.readset["state_digest"] == c8,
            "e1_unchanged": producer.e1_event["hash"] == e1,
            "positive_outcome": positive.response.reason
            == OBSERVED_IMMEDIATE_OBJECT_ORIENTATION,
            "fault_outcome": fault.response.reason == UNKNOWN_RECEIVABILITY,
            "restored_outcome": restored.response.reason
            == OBSERVED_IMMEDIATE_OBJECT_ORIENTATION,
            "all_zero_targets": all(
                not row.response.target_proposals
                and row.decision.branch.value == "NO_CHANGE"
                and row.decision.reason.value == "NO_PROPOSAL"
                for row in (positive, fault, restored)
            ),
        }

        with fresh_store(root / "missing-response.sqlite") as store:
            missing = producer.evaluate_s36(store=store, response_witness=None)
        results["missing_response"] = {
            "status": missing.response.status.value,
            "outcome": missing.response.reason,
            "target_proposals": len(missing.response.target_proposals),
            "target_branch": missing.decision.branch.value,
            "target_reason": missing.decision.reason.value,
            "valid_empty": missing.response.reason == RECEIVABLE_NO_OBSERVED_UPTAKE,
        }

        refusals = []
        for kind, case_name in (
            ("access", "wrong_actor"),
            ("access", "wrong_event"),
            ("access", "wrong_hash"),
            ("access", "wrong_scene"),
            ("access", "before_event"),
            ("access", "after_as_of"),
            ("access", "revoked_field"),
            ("response", "wrong_actor"),
            ("response", "wrong_event"),
            ("response", "wrong_hash"),
            ("response", "before_access"),
            ("response", "after_as_of"),
            ("response", "revoked_field"),
            ("response", "bad_kind"),
        ):
            access = boundary_helpers._access(producer)
            response = boundary_helpers._response(producer)
            if kind == "access":
                access = boundary_helpers._mutate_access(producer, case_name)
            else:
                response = boundary_helpers._mutate_response(producer, case_name)
            with fresh_store(root / f"refuse-{kind}-{case_name}.sqlite") as store:
                result = producer.evaluate_s36(
                    store=store, access_witness=access, response_witness=response
                )
                refusals.append(
                    {
                        "kind": kind,
                        "case": case_name,
                        "status": result.response.status.value,
                        "reason": result.response.reason,
                        "target_proposals": len(result.response.target_proposals),
                        "committed": result.committed,
                        "no_ghost": result.no_ghost,
                        "tables_empty": all(
                            not rows for rows in store.snapshot().values()
                        ),
                    }
                )
        results["wrong_witnesses"] = {
            "cases": refusals,
            "all_refused": all(
                row["status"] == "REFUSED"
                and row["target_proposals"] == 0
                and row["committed"] is False
                and row["no_ghost"] is True
                and row["tables_empty"] is True
                for row in refusals
            ),
        }

        preimage = []
        base = dict(source)
        for label, mutation in {
            "wrong_owner": {"b_owner": "FAKE_OWNER"},
            "wrong_event_hash": {"b_event_hash": "0" * 64},
            "wrong_clock": {"b_clock": 999},
            "wrong_operation": {"b_operation": "REFUSE_TOOL", "b_quantity": 0},
            "wrong_quantity": {"b_quantity": 5},
            "wrong_e1_hash": {"a_e1_hash": "0" * 64},
        }.items():
            changed = dict(base)
            changed.update(mutation)
            target = root / f"preimage-{label}"
            try:
                IntegratedProducer(target, case=case, source=changed)
                rejected = False
                code = ""
            except MaterialSourceRefusal as exc:
                rejected = True
                code = exc.code
            preimage.append(
                {
                    "case": label,
                    "rejected": rejected,
                    "code": code,
                    "c8_created": (target / "bp2").exists(),
                }
            )
        results["m35_preimage"] = {
            "cases": preimage,
            "all_rejected": all(
                row["rejected"]
                and row["code"] == "MATERIAL_SOURCE_PREIMAGE_MISMATCH"
                and row["c8_created"] is False
                for row in preimage
            ),
        }
    finally:
        producer.close()

    guard_session = start_session(root / "language-guard", share=True)
    try:
        setup_neutral_language(guard_session)
        plan = guard_session.expression_plan(trigger_kind="SAY", text="Hello.")
        native = build_native_artifact(
            plan, atoms=["BENCH_PRESENT", "SELF_RELIANCE_FAMILY"]
        )
        translation = build_translation_artifact(
            plan, native, atoms=["BENCH_PRESENT", "SELF_RELIANCE_FAMILY"]
        )
        guard = evaluate_pair(plan, native, translation)
        results["language_guard"] = {
            "plan_unit": plan.unit["unit_id"],
            "status": guard["status"],
            "codes": guard["codes"],
            "rejected_strengthening": guard["status"] == "REJECTED"
            and "UNAUTHORIZED_MEANING_STRENGTHENED" in guard["codes"],
        }
    finally:
        guard_session.close()

    loss_session = start_session(root / "language-loss", share=True)
    try:
        data = setup_source_language(loss_session)
        first = loss_session.say(TRIGGER)
        before = loss_session.read_s36()
        loss_session.revoke_language_access(data["family_receipt"])
        refused = loss_session.say(TRIGGER)
        loss_session.restore_language_access(data["family_receipt"])
        restored = loss_session.say(TRIGGER)
        after = loss_session.read_s36()
        results["language_access_loss"] = {
            "first_strategy": first["strategy"],
            "first_native": first["candidate"]["speech"],
            "refused_strategy": refused["strategy"],
            "refused_fallback": refused["language"]["fallback"],
            "refused_reason": refused["language"]["fallback_reason"],
            "restored_strategy": restored["strategy"],
            "restored_fallback": restored["language"]["fallback"],
            "s36_response_unchanged": before["response_ref"] == after["response_ref"],
            "s36_no_target": after["target_branch"] == "NO_CHANGE"
            and after["target_reason"] == "NO_PROPOSAL"
            and after["target_state_rows"] == 0,
            "source_preserved": bool(
                refused["language"]["plan"]["readset"]["invalidated_relation_ids"]
            ),
        }
    finally:
        loss_session.close()
    return results


def source_manifest() -> dict:
    m35_rows = []
    for rel in M35_FILES:
        local = RET / "vendor" / "m35" / rel
        pinned_blob = _git("rev-parse", f"{PINNED_M35}:{PINNED_M35_PREFIX}/{rel}")
        local_blob = _git("hash-object", str(local))
        m35_rows.append(
            {
                "path": rel,
                "pinned_git_blob_sha1": pinned_blob,
                "local_git_blob_sha1": local_blob,
                "exact": pinned_blob == local_blob,
                "sha256": _sha256(local),
            }
        )
    s36_rows = []
    for rel in S36_FILES:
        local = Path(roots()["s36_return"]) / rel
        pinned_blob = _git("rev-parse", f"{PINNED_S36}:{PINNED_S36_PREFIX}/{rel}")
        local_blob = _git("hash-object", str(local))
        s36_rows.append(
            {
                "path": rel,
                "pinned_git_blob_sha1": pinned_blob,
                "local_git_blob_sha1": local_blob,
                "exact": pinned_blob == local_blob,
                "sha256": _sha256(local),
            }
        )
    local_rows = [
        {
            "path": rel,
            "sha256": _sha256(RET / rel),
            "git_blob_sha1": _git("hash-object", str(RET / rel)),
        }
        for rel in LOCAL_FILES
    ]
    root_info = roots()
    language_rows = []
    for rel in LANGUAGE_FILES:
        local = Path(root_info["language_return"]) / rel
        pinned_blob = _git("rev-parse", f"{PINNED_LANGUAGE}:{PINNED_LANGUAGE_PREFIX}/{rel}")
        local_blob = _git("hash-object", str(local))
        language_rows.append(
            {
                "path": rel,
                "pinned_git_blob_sha1": pinned_blob,
                "local_git_blob_sha1": local_blob,
                "exact": pinned_blob == local_blob,
                "sha256": _sha256(local),
            }
        )
    join_e_rows = []
    for rel in JOIN_E_FILES:
        local = Path(root_info["join_e_return"]) / rel
        pinned_blob = _git("rev-parse", f"{PINNED_JOIN_E}:{PINNED_JOIN_E_PREFIX}/{rel}")
        local_blob = _git("hash-object", str(local))
        join_e_rows.append(
            {
                "path": rel,
                "pinned_git_blob_sha1": pinned_blob,
                "local_git_blob_sha1": local_blob,
                "exact": pinned_blob == local_blob,
                "sha256": _sha256(local),
            }
        )
    origin_rows = []
    for name, path in sorted(origin_info().items()):
        local = Path(path)
        origin_rows.append(
            {
                "module": name,
                "path": path,
                "sha256": _sha256(local) if local.is_file() else "",
            }
        )
    return {
        "schema": "SOROK_S37_SOURCE_MANIFEST@1",
        "roots": root_info,
        "m35_vendored": m35_rows,
        "m35_all_exact": all(row["exact"] for row in m35_rows),
        "s36_readonly": s36_rows,
        "s36_all_exact": all(row["exact"] for row in s36_rows),
        "local": local_rows,
        "language_readonly": language_rows,
        "language_all_exact": all(row["exact"] for row in language_rows),
        "join_e_readonly": join_e_rows,
        "join_e_all_exact": all(row["exact"] for row in join_e_rows),
        "imported_origins": origin_rows,
        "candidate_origin_is_s36": str(Path(root_info["origins"]["candidate"]))
        .startswith(root_info["s36_return"]),
        "bp2_origin_is_m35": str(Path(root_info["origins"]["bp2_joined"]))
        .startswith(str(RET / "vendor" / "m35")),
    }


def origin_info() -> dict:
    from s37.bootstrap import origins

    return origins()


def main() -> None:
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="s37-evidence-", dir=str(RET)))
    try:
        chains = chain_evidence(work / "chains")
        boundaries = boundary_evidence(work / "boundaries")
        tests = test_evidence()
        entry = _run([PY, "-B", "run_s37.py"], "entrypoint.log")
        if entry.returncode != 0:
            raise RuntimeError("S37_ENTRYPOINT_FAILED:" + entry.stderr)
        (EVID / "entrypoint.json").write_text(entry.stdout)
        manifest = source_manifest()
        _write(EVID / "chain.json", chains)
        _write(EVID / "boundaries.json", boundaries)
        _write(EVID / "test_run.json", tests)
        _write(EVID / "source_manifest.json", manifest)
        print(
            json.dumps(
                {
                    "tests": tests["counts"],
                    "chains": [row["label"] for row in chains["chains"]],
                    "same_session_class": chains["same_session_class"],
                    "same_neutral_speech": chains["same_neutral_speech"],
                    "both_no_target": chains["both_no_target"],
                    "access_fault_restore": boundaries["access_fault_restore"][
                        "positive_outcome"
                    ]
                    and boundaries["access_fault_restore"]["fault_outcome"]
                    and boundaries["access_fault_restore"]["restored_outcome"],
                    "wrong_witnesses_all_refused": boundaries["wrong_witnesses"][
                        "all_refused"
                    ],
                    "m35_preimage_all_rejected": boundaries["m35_preimage"][
                        "all_rejected"
                    ],
                    "language_guard_rejected": boundaries["language_guard"][
                        "rejected_strengthening"
                    ],
                    "language_loss_fallback": boundaries["language_access_loss"][
                        "refused_fallback"
                    ],
                    "source_roots": manifest["candidate_origin_is_s36"]
                    and manifest["bp2_origin_is_m35"],
                    "entrypoint_exit": entry.returncode,
                },
                sort_keys=True,
            )
        )
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
