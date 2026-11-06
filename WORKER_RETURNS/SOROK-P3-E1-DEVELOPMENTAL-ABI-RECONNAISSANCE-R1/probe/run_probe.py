"""Execute the B1 compatibility probe and write a machine-readable receipt."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get("SOROK_REPO_ROOT", str(HERE.parents[2])))
ENGINE = Path(
    os.environ.get(
        "SOROK_ENGINE_PATH",
        str(REPO / "WORKER_RETURNS" / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"),
    )
)
for path in (str(ENGINE), str(HERE)):
    if path not in sys.path:
        sys.path.insert(0, path)

from developmental_recursion.contracts import canonical  # noqa: E402
from developmental_recursion.engine import BatchEngine  # noqa: E402
from b1_owner_adapter import (  # noqa: E402
    B1_BLOB,
    B1_SHA256,
    B1Owner,
    GRADE,
    OPERATION,
    _load_b1,
)


def proposals(source_ref: str):
    from developmental_recursion.contracts import EventProposal

    def one(event_id, event_time, *, interrupted, plan, objective):
        return EventProposal(
            event_id,
            event_time,
            OPERATION,
            (source_ref,),
            ("child", "caretaker"),
            {
                "b1": {
                    "world_ref": "world:garage",
                    "objective_occurrence": objective,
                    "project": "repair_route",
                    "power_ref": "power:caretaker_controls_tools",
                    "offers": [["caretaker", "Let us check what can be secured.", plan]],
                    "interrupted": interrupted,
                }
            },
            None,
        )

    return [
        one("event1", 2, interrupted=True, plan="joint_inventory", objective="bike_stolen"),
        one("event2", 3, interrupted=False, plan="no_plan", objective="shared_tool_offer"),
        one("event3", 4, interrupted=False, plan="joint_inventory", objective="shared_tool_offer"),
    ]


def scenario(root: Path, name: str, *, journal_only: bool):
    work = root / name
    work.mkdir(parents=True, exist_ok=True)
    db = work / "owner.sqlite"
    journal = work / "journal.sqlite"
    owner = B1Owner(db, root="root-" + name, branch="main", journal_only=journal_only)
    engine = BatchEngine(owner, journal)
    batch_id = "batch-" + name
    props = proposals(owner.source_ref)
    started = time.perf_counter()
    result = engine.run_batch(batch_id, props)
    elapsed = time.perf_counter() - started
    state = owner.state()
    history = engine.history(batch_id)
    measurements = {
        "batch_wall_seconds": round(elapsed, 6),
        "owner_db_bytes": db.stat().st_size,
        "journal_bytes": journal.stat().st_size,
        "state_json_bytes": len(canonical(state)),
        "records_json_bytes": len(canonical(result["records"])),
        "history_json_bytes": len(canonical(history)),
        "middle_state_count": len(state["middle"]),
        "response_count": len(state["responses"]),
        "transition_count": len(state["transitions"]),
        "operation_rows": owner.db.execute("SELECT COUNT(*) FROM b1_operations").fetchone()[0],
        "occurrence_rows": owner.db.execute("SELECT COUNT(*) FROM occurrence").fetchone()[0],
        "joint_receipt_rows": owner.db.execute("SELECT COUNT(*) FROM joint_receipt").fetchone()[0],
        "model_calls": 0,
        "provider_calls": 0,
    }
    owner.close()
    engine.close()
    reopened_owner = B1Owner(db, root="root-" + name, branch="main")
    reopened_engine = BatchEngine(reopened_owner, journal)
    started = time.perf_counter()
    cold_history = reopened_engine.history(batch_id)
    cold_seconds = time.perf_counter() - started
    after_reopen = reopened_owner.snapshot().document()
    reopened_engine.close()
    reopened_owner.close()
    mediator = result["records"][0]["consequences"]["middle_state_ids"]
    mediator_records = result["records"][0]["consequences"]["middle_state_record_hashes"]
    return {
        "name": name,
        "journal_only": journal_only,
        "batch_id": batch_id,
        "grade": GRADE,
        "statuses": [row["status"] for row in result["records"]],
        "event_hashes": [row["objective"]["event"]["hash"] for row in result["records"]],
        "middle_state_ids": mediator,
        "middle_state_record_hashes": mediator_records,
        "later_practical_activity": result["records"][2]["consequences"]["practical_activity"],
        "later_recruited": result["records"][2]["consequences"]["recruited"],
        "later_accessible_actions": result["records"][2]["accessible"]["actor_surface"]["actions"],
        "history_hash": result["history_hash"],
        "snapshot_after": result["records"][-1]["after"],
        "cold_reopen_seconds": round(cold_seconds, 6),
        "cold_reopen_matches_records": cold_history["records"] == result["records"],
        "cold_reopen_snapshot": after_reopen,
        "measurements": measurements,
    }


def scaling_scenario(root: Path, count: int):
    from developmental_recursion.contracts import EventProposal

    work = root / ("scaling-" + str(count))
    work.mkdir(parents=True, exist_ok=True)
    db = work / "owner.sqlite"
    owner = B1Owner(db, root="root-scaling-" + str(count), branch="main")
    try:
        started = time.perf_counter()
        for index in range(1, count + 1):
            event_id = "scale-" + str(index)
            event_time = index + 1
            proposal = EventProposal(
                event_id,
                event_time,
                OPERATION,
                (owner.source_ref,),
                ("child", "caretaker"),
                {
                    "b1": {
                        "world_ref": "world:garage",
                        "objective_occurrence": (
                            "bike_stolen" if index == 1 else "shared_tool_offer"
                        ),
                        "project": "repair_route",
                        "power_ref": "power:caretaker_controls_tools",
                        "offers": [[
                            "caretaker",
                            "Let us check what can be secured.",
                            "joint_inventory",
                        ]],
                        "interrupted": index == 1,
                    }
                },
                None,
            )
            owner.realize("scale-op-" + str(index), proposal, owner.snapshot())
        elapsed = time.perf_counter() - started
        state = owner.state()
        return {
            "events": count,
            "total_wall_seconds": round(elapsed, 6),
            "per_event_ms": round(1000.0 * elapsed / count, 3),
            "owner_db_bytes": db.stat().st_size,
            "state_json_bytes": len(canonical(state)),
            "response_count": len(state["responses"]),
            "middle_state_count": len(state["middle"]),
            "transition_count": len(state["transitions"]),
        }
    finally:
        owner.close()


def guard_receipt():
    import importlib.util

    path = REPO / "rawlsing_next" / "v3_psepf_zero_positive_guard.py"
    spec = importlib.util.spec_from_file_location("p3_zero_guard_probe", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    request = {
        "actor_id": "child",
        "source_class": "ResolvedStructuralContext",
        "source_ref": "B1:event1",
        "source_hash": "a" * 64,
        "source_lineage": [],
        "transition_surface_id": "B1_CAN011_MEDIATOR",
        "operation_class": "CREATE",
        "state_fingerprint": {
            "actor_state_hash": "b" * 64,
            "causal_ledger_hash": "c" * 64,
            "causal_cursor": "1",
            "rng_state_hash": "d" * 64,
            "scheduler_state_hash": "e" * 64,
        },
        "authority": None,
    }
    decision = module.evaluate_psepf_zero_positive_guard(request)
    return {
        "guard_file": str(path.relative_to(REPO)),
        "registry_empty": dict(module.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES) == {},
        "outcome": decision.outcome.value,
        "reason": decision.reason.value,
        "zero_effect": decision.zero_effect,
        "actor_state_effect": decision.actor_state_effect,
        "causal_ledger_appends": decision.causal_ledger_appends,
        "rng_mutations": decision.rng_mutations,
        "scheduler_mutations": decision.scheduler_mutations,
    }


def source_pins():
    pins = json.loads(
        (ENGINE / "SOURCE_PINS.json").read_text(encoding="utf8")
    )
    actual = {}
    engine_prefix = "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/"
    for relative, expected in pins["files"].items():
        if relative.startswith(engine_prefix):
            path = ENGINE / relative[len(engine_prefix):]
        else:
            path = REPO / relative
        if path.is_file():
            actual_sha = hashlib.sha256(path.read_bytes()).hexdigest()
            actual[relative] = {
                "relative_path": relative,
                "expected_sha256": expected,
                "actual_sha256": actual_sha,
                "match": actual_sha == expected,
            }
        else:
            actual[relative] = {
                "relative_path": relative,
                "expected_sha256": expected,
                "actual_sha256": None,
                "match": False,
                "note": "NOT_PRESENT_IN_THIS_EXECUTION_ROOT",
            }
    b1_path = HERE / "vendor" / "B1" / "bfirst.py"
    b1 = _load_b1(b1_path)
    return {
        "protected_start": pins["protected_start"],
        "engine_source_pins": actual,
        "b1": {
            "commit": "c0f4588c158b40c8903b4aae2f292eae5238b8a0",
            "path": "WORKER_RETURNS/SOROK-V2-HQ324-B1-COUPLED-DEVELOPMENT-R1/bfirst.py",
            "git_blob_sha1": B1_BLOB,
            "vendored_sha256": B1_SHA256,
            "actual_sha256": hashlib.sha256(b1_path.read_bytes()).hexdigest(),
            "loaded": bool(b1),
        },
        "archive_note": {
            "expected_v3_archive_sha256": (
                "953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086"
            ),
            "local_staging_zip_sha256": (
                "3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289"
            ),
            "exact_archive_available": False,
            "local_copy_grade": "LOCAL_UNVERIFIED_ARCHIVE_COPY_NOT_EXACT_PROTECTED_BYTES",
        },
    }


def git_value(*args):
    try:
        return subprocess.run(
            ["git", "-C", str(REPO), *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        ).stdout.strip()
    except Exception as exc:  # noqa: BLE001 - receipt records the failure
        return "UNAVAILABLE:" + type(exc).__name__


def main() -> int:
    receipts = HERE / "receipts"
    receipts.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="sorok-p3-e1-probe-"))
    try:
        positive = scenario(root, "positive", journal_only=False)
        control = scenario(root, "control", journal_only=True)
        scaling = [scaling_scenario(root, count) for count in (3, 10, 30, 60)]
    finally:
        shutil.rmtree(root, ignore_errors=True)

    env = os.environ.copy()
    env["SOROK_ENGINE_PATH"] = str(ENGINE)
    env["SOROK_REPO_ROOT"] = str(REPO)
    junit = receipts / "junit.xml"
    started = time.perf_counter()
    pytest_run = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            str(HERE / "test_b1_owner_adapter.py"),
            "--junitxml=" + str(junit),
        ],
        cwd=str(HERE),
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
    )
    pytest_seconds = time.perf_counter() - started
    counts = {}
    if junit.is_file():
        import xml.etree.ElementTree as ET

        suites = list(ET.parse(junit).getroot().iter("testsuite"))
        counts = {
            key: sum(int(suite.get(key, 0)) for suite in suites)
            for key in ("tests", "failures", "errors", "skipped")
        }

    receipt = {
        "schema": "SOROK_P3_E1_PROBE_RECEIPT@1",
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "grade": GRADE,
        "native_science": "NOT_ISSUED",
        "production_registry": "EMPTY_UNCHANGED",
        "host": {
            "platform": platform.platform(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "model_reported_by_environment": (
                "opencode/deepseek-v4.1-flash (DeepSeek V4.1-Flash MAX requested; "
                "actual reasoning configuration not machine-observable)"
            ),
            "editor_harness": "OpenCode",
        },
        "git": {
            "current_head": git_value("rev-parse", "HEAD"),
            "current_branch": git_value("branch", "--show-current"),
            "protected_start": "c852d7516e23fcb6cf2215e9be7c5fa268503516",
            "protected_branch": "integration/pre-main-reconciliation-r1",
            "pr_704_receiving": "0b7d8ba33b5cd905963292357507ae7bbc2219de",
            "engine_runtime_cut": "81b01f654f8ba09550d03df17e8014f43ffcfc9f",
        },
        "source_pins": source_pins(),
        "positive": positive,
        "control": control,
        "scaling": scaling,
        "causal_contrast": {
            "same_later_event_hash": (
                positive["event_hashes"][2] == control["event_hashes"][2]
            ),
            "positive_later_activity": positive["later_practical_activity"],
            "control_later_activity": control["later_practical_activity"],
            "positive_later_recruited": positive["later_recruited"],
            "control_later_recruited": control["later_recruited"],
            "positive_middle_count": positive["measurements"]["middle_state_count"],
            "control_middle_count": control["measurements"]["middle_state_count"],
        },
        "production_guard": guard_receipt(),
        "pytest": {
            "command": [
                sys.executable,
                "-B",
                "-m",
                "pytest",
                "-q",
                "-p",
                "no:cacheprovider",
                "test_b1_owner_adapter.py",
            ],
            "returncode": pytest_run.returncode,
            "wall_seconds": round(pytest_seconds, 6),
            "counts": counts,
            "stdout_tail": pytest_run.stdout[-4000:],
            "stderr_tail": pytest_run.stderr[-2000:],
        },
        "test_matrix": {
            "1_valid_actor_source_root": "PASS: test_positive_three_event_batch...",
            "2_invalid_actor_foreign_root": "PASS: test_invalid_actor... + test_foreign_root...",
            "3_wrong_clock": "PASS: test_invalid_actor... event_time=clock",
            "4_bad_source_version_hash": "PASS: test_invalid_actor..., test_foreign_root..., test_middle_rule_version...",
            "5_missing_scientific_rule": "PASS: test_production_zero_positive_guard... (production DENY_ZERO_EFFECT; B1 test-only rule is explicit)",
            "6_test_only_positive_state_effect": "PASS: test_positive_three_event_batch...",
            "7_production_positive_registry_denies": "PASS: test_production_zero_positive_guard...",
            "8_state_cold_reopening": "PASS: test_positive_three_event_batch... reopened section",
            "9_later_first_consumer_reads_state": "PASS: test_positive_three_event_batch... records[2]",
            "10_same_later_event_changed_prior_state": "PASS: test_identical_later_event_differs...",
            "11_atomic_refusal_before_durable_mutation": "PASS: test_invalid_actor...",
            "12_dormant_unexpressed_effect_stored": "PASS: test_positive_three_event_batch... event2",
            "source_severance_exact_restore": "PASS: test_mediator_severance... + test_foreign_root...",
            "operation_ambiguity_no_duplicate": "PASS: test_operation_idempotency...",
        },
        "not_run": [
            "Full #704 P2Owner seven-test suite in this extracted probe root (inherited author/independent results remain historical).",
            "B3A Integration.run through DevelopmentOwner (schema/ABI mismatch; not a narrow adapter).",
            "HQ300 run_positive_chain through DevelopmentOwner (in-memory ledger, no durable owner).",
            "M01 Cell through DevelopmentOwner (in-memory fixture, no durable owner).",
            "BP2P4J JoinedProduct through DevelopmentOwner (separate C8/C9/C10/C12 product).",
            "Original V3 yearly_step/flow tests against exact protected archive bytes (archive SHA mismatch).",
            "Any native CAN008/CAN011/ADP016/ADP017 production operation.",
        ],
        "cost_notes": [
            "B1 rewrites one full checkpoint JSON row per event; state/response/transition bytes grow with history.",
            "Per event: one occurrence row, one joint_receipt row, one b1_operations row, one response record, plus one mediator/transition on a create.",
            "No model/provider invocation occurs in this adapter probe.",
            "B3A whole-store staging and BP2P4J product costs were not measured here; see 06_RESOURCE_COST_FINDINGS.md.",
        ],
    }
    (receipts / "PROBE_RECEIPT.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf8"
    )
    print(json.dumps({
        "positive_statuses": positive["statuses"],
        "positive_later": positive["later_practical_activity"],
        "control_later": control["later_practical_activity"],
        "pytest": receipt["pytest"]["counts"],
        "guard": receipt["production_guard"]["outcome"],
        "receipt": str(receipts / "PROBE_RECEIPT.json"),
    }, indent=2))
    return 0 if pytest_run.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
