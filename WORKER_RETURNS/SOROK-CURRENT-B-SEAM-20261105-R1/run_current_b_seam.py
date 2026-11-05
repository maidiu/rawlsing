#!/usr/bin/env python3
"""Bounded exact current-root B source check for pinned S48-S52."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from harness import pins  # noqa: E402

TESTS = {
    "s48": (
        "s49",
        "tests/test_s48_one_call.py::"
        "test_unsupported_fake_b_operation_is_source_owner_hold_with_no_world_or_c8_effect",
        "tests/test_s48_one_call.py::"
        "test_payload_has_no_qualified_candidates_and_no_foreign_source_json",
    ),
    "s49": (
        "s49",
        "tests/test_s49.py::"
        "test_actual_root_without_b_context_holds_without_b_event_or_c8",
    ),
    "s50": (
        "s50",
        "tests/test_s50.py::test_source_identities_all_31_exact",
        "tests/test_s50.py::test_actual_root_missing_state_hold_and_projection_is_isolated",
    ),
    "s51": (
        "s51",
        "tests/test_s51.py::test_actual_root_object_and_hypothesis_and_offer_relevance",
    ),
    "s52": (
        "s52",
        "tests/test_s52.py::test_paid_candidate_and_conditional_reason_enter_normal_generation",
    ),
}

DISPOSITIONS = {
    "s48": {
        "status": "SOURCE_OWNER_HOLD",
        "code": "S48_SOURCE_OWNER_HOLD_NO_CURRENT_OWNER_ADMISSION",
        "missing_function": "S48_MISSING_INDEPENDENT_CURRENT_B_SOURCE_PERFORMER",
        "missing": [
            "independent actor-owner-qualified current B source/provider",
            "current-root/actor/branch/clock B operation issuance",
            "normal S42 source/case admission adapter for that owner",
        ],
        "original_source_owner": "current Sorok B actor/source owner (not installed)",
        "first_importer": "s48/sources.py:issue_current_source",
        "existing_tests": [
            "test_unsupported_fake_b_operation_is_source_owner_hold_with_no_world_or_c8_effect",
            "test_payload_has_no_qualified_candidates_and_no_foreign_source_json",
        ],
    },
    "s49": {
        "status": "B_CONTEXT_HOLD",
        "code": "S49_MISSING_CURRENT_B_ACTOR_OWNED_CONTEXT",
        "missing": [
            "B-owned S39 context/history predicate source",
            "registered source/model/actor/branch/time/custody",
            "unique actual B option selection",
        ],
        "present": [
            "actual B actor identity TEST_ONLY_BP1_R26V_ACTOR_B",
            "actual B perception/ADP017 access witness",
            "B generation/performer and normal S42 adapter code",
        ],
        "original_source_owner": "Sorok S39 current B actor-context source owner (not installed)",
        "first_importer": "s49/actor.py:root_b_sources / s49/session.py:produce_b_turn",
        "existing_tests": [
            "test_actual_root_without_b_context_holds_without_b_event_or_c8",
        ],
    },
    "s50": {
        "status": "SOURCE_OWNER_HOLD",
        "code": "S50_ACTUAL_ROOT_MISSING_HISTORICAL_V3_STATE",
        "missing": [
            "backbone_state", "initial_state_provenance", "expectation_baseline",
            "striving_objects", "pressure_flow_history", "pressure_flow_memory",
            "surface_psyche_profile", "analyst_pressure_account",
            "actor_context_projection", "actor_owned_source",
        ],
        "original_source_owner": "historical Rawlsing V3 actor-state/source owner",
        "first_importer": "s50/session.py:actual_root_missing",
        "source_identity": "31/31 exact, archive identity 953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086",
        "existing_tests": [
            "test_source_identities_all_31_exact",
            "test_actual_root_missing_state_hold_and_projection_is_isolated",
        ],
    },
    "s51": {
        "status": "OPEN_CHOICE_SET",
        "code": "NO_EXISTING_S49_OPTION_EXPRESSES_PAID_FINISHING_EQUIPMENT_OFFER",
        "missing": [
            "actual current B purpose",
            "native object-formation/relevance law",
            "option-specific reason that selects a B action",
        ],
        "original_source_owner": "Sorok S51 situated-object/relevance source owner (not installed)",
        "first_importer": "s51/session.py:consume_generation",
        "existing_tests": [
            "test_actual_root_object_and_hypothesis_and_offer_relevance",
        ],
    },
    "s52": {
        "status": "CONDITIONAL_ON_INDEPENDENT_PARTICIPATION",
        "code": "S52_INDEPENDENT_COUNTERPART_NOT_OBSERVED",
        "missing": [
            "independent counterpart contribution/willingness",
            "actual paid-history-specific capability source",
            "selected B attempt or performed paid action in the normal path",
        ],
        "original_source_owner": "G18 paid-activity contract owner plus S52 current-state port",
        "first_importer": "s52/session.py:compile_candidate / s52/performer.py",
        "existing_tests": [
            "test_paid_candidate_and_conditional_reason_enter_normal_generation",
        ],
    },
}


def _json_dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _stage_env(stage: Path) -> dict:
    join_e = stage / pins.PINS["join_e"].base
    r31j = stage / pins.PINS["r31j"].base
    return {
        "S37_JOIN_E_RETURN": str(join_e),
        "S37_LANGUAGE_RETURN": str(stage / pins.PINS["language"].base),
        "S37_S36_RETURN": str(stage / pins.PINS["s36"].base),
        "S37_M35_RETURN": str(stage / pins.PINS["s37"].base / "vendor" / "m35"),
        "M35_JOIN_E_RETURN": str(join_e),
        "M35_BP2_VENDOR": str(r31j / "candidate" / "vendor" / "bp2" / "vendor"),
        "PYTHONDONTWRITEBYTECODE": "1",
    }


def _stage_return(stage: Path, key: str) -> Path:
    return stage / pins.PINS[key].base


def _run_probe(name: str, stage: Path, work: Path, logs: Path) -> dict:
    env = dict(os.environ)
    env.update(_stage_env(stage))
    env["PYTHONPATH"] = str(_stage_return(stage, name))
    command = [
        sys.executable, "-B", str(Path(__file__).resolve()),
        "--probe", name, "--stage", str(stage), "--work-dir", str(work / name),
    ]
    proc = subprocess.run(command, cwd=str(RETURN), env=env,
                          capture_output=True, text=True, timeout=600)
    log = logs / f"probe_{name}.log"
    log.write_text(proc.stdout + proc.stderr)
    if proc.returncode != 0:
        raise RuntimeError(f"PROBE_{name}_FAILED:{proc.returncode}:{proc.stderr}")
    return json.loads(proc.stdout)


def _junit_counts(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    tests = sum(int(s.attrib.get("tests", 0)) for s in suites)
    failures = sum(int(s.attrib.get("failures", 0)) for s in suites)
    errors = sum(int(s.attrib.get("errors", 0)) for s in suites)
    skips = sum(int(s.attrib.get("skipped", 0)) for s in suites)
    return {"tests": tests, "PASS": tests - failures - errors - skips,
            "RED": failures, "ERROR": errors, "SKIP": skips}


def _run_tests(key: str, closure: str, stage: Path, logs: Path,
               evidence: Path) -> dict:
    _, *nodeids = TESTS[key]
    return_dir = _stage_return(stage, key)
    env = dict(os.environ)
    env.update(_stage_env(stage))
    env["PYTHONPATH"] = str(return_dir)
    env["TMPDIR"] = str(logs / "tmp")
    (logs / "tmp").mkdir(parents=True, exist_ok=True)
    junit = evidence / "junit" / f"{key}_hold.xml"
    junit.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
        f"--junitxml={junit}",
        *[str(return_dir / nodeid) for nodeid in nodeids],
    ]
    proc = subprocess.run(command, cwd=str(RETURN), env=env,
                          capture_output=True, text=True, timeout=900)
    (logs / f"{key}_hold.log").write_text(proc.stdout + proc.stderr)
    counts = _junit_counts(junit) if junit.is_file() else {}
    return {
        "closure": closure,
        "command": " ".join(command),
        "exit": proc.returncode,
        "counts": counts,
        "junit": str(junit.relative_to(RETURN)),
        "log": str((logs / f"{key}_hold.log").relative_to(RETURN)),
        "all_pass": proc.returncode == 0 and counts.get("RED", 1) == 0
        and counts.get("ERROR", 1) == 0,
    }


def _probe_mode(args) -> int:
    stage = Path(args.stage).resolve()
    env = _stage_env(stage)
    os.environ.update(env)
    for path in (_stage_return(stage, args.probe),):
        if str(path) in sys.path:
            sys.path.remove(str(path))
        sys.path.insert(0, str(path))
    from harness.probes import PROBES

    result = PROBES[args.probe](stage, Path(args.work_dir).resolve())
    print(json.dumps(result, indent=2, sort_keys=True, default=str))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=pins.DEFAULT_SOURCE_ROOT)
    parser.add_argument("--s49-stage", type=Path,
                        default=RETURN / ".runtime" / "closures" / "s49")
    parser.add_argument("--s50-stage", type=Path,
                        default=RETURN / ".runtime" / "closures" / "s50")
    parser.add_argument("--s51-stage", type=Path,
                        default=RETURN / ".runtime" / "closures" / "s51")
    parser.add_argument("--s52-stage", type=Path,
                        default=RETURN / ".runtime" / "closures" / "s52")
    parser.add_argument("--work-dir", type=Path,
                        default=RETURN / ".runtime" / "probe-work")
    parser.add_argument("--logs-dir", type=Path, default=RETURN / "logs")
    parser.add_argument("--evidence-dir", type=Path, default=RETURN / "evidence")
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--probe", choices=("s49", "s50", "s51", "s52"))
    parser.add_argument("--stage", type=Path)
    return parser


def main(argv=None) -> int:
    started = time.time()
    args = build_parser().parse_args(argv)
    if args.probe:
        return _probe_mode(args)
    source_root = args.source_root.expanduser().resolve()
    s49 = args.s49_stage.expanduser().resolve()
    s50 = args.s50_stage.expanduser().resolve()
    s51 = args.s51_stage.expanduser().resolve()
    s52 = args.s52_stage.expanduser().resolve()
    work = args.work_dir.expanduser().resolve()
    logs = args.logs_dir.expanduser().resolve()
    evidence = args.evidence_dir.expanduser().resolve()
    logs.mkdir(parents=True, exist_ok=True)
    evidence.mkdir(parents=True, exist_ok=True)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)
    try:
        stages = {"s49": s49, "s50": s50, "s51": s51, "s52": s52}
        source_manifest = pins.manifest(source_root, stages)
        _json_dump(evidence / "source_manifest.json", source_manifest)
        probes = {
            name: _run_probe(name, stage, work, logs)
            for name, stage in stages.items()
        }
        for name, result in probes.items():
            _json_dump(evidence / f"probe_{name}.json", result)
        tests = {
            key: _run_tests(key, closure, stages[closure], logs, evidence)
            for key, (closure, *_rest) in TESTS.items()
        }
        p49 = probes["s49"]
        p50 = probes["s50"]
        p51 = probes["s51"]
        p52 = probes["s52"]
        checks = {
            "source_manifest_all_exact": source_manifest["all_exact"],
            "s49_access_observed": p49["access"].get("access_status") == "ACCESSIBLE",
            "s49_no_root_b_sources": p49["root_b_sources"] == [],
            "s49_s48_no_candidates": (
                p49["s48_candidate_specs"] == []
                and p49["s48_eligible_candidate_ids"] == []
            ),
            "s49_s48_issue_hold": (
                p49["s48_issue_current_source"].get("code")
                == "S48_SOURCE_OWNER_HOLD_NO_CURRENT_OWNER_ADMISSION"
            ),
            "s49_b_context_hold": (
                p49["b_turn"].get("stage") == "B_CONTEXT_HOLD"
                and p49["b_turn"].get("reason")
                == "S49_MISSING_CURRENT_B_ACTOR_OWNED_CONTEXT"
                and p49["b_turn"].get("event_ref") == ""
            ),
            "s49_no_world_or_clock_change": not p49["world_or_clock_changed"],
            "s49_no_normal_s42_or_c8": (
                not p49["normal_s42_reached"] and not p49["c8_created"]
            ),
            "s50_actual_hold": (
                p50["actual_root_missing"].get("status") == "SOURCE_OWNER_HOLD"
                and p50["actual_root_missing"].get("reason")
                == "S50_ACTUAL_ROOT_MISSING_HISTORICAL_V3_STATE"
            ),
            "s50_missing_fields_exact": set(p50["actual_root_missing"].get(
                "missing_fields", [])) == set(DISPOSITIONS["s50"]["missing"]),
            "s50_source_identities_exact": (
                p50["source_identity"].get("count") == 31
                and p50["source_identity"].get("all_exact") is True
            ),
            "s51_actual_purpose_unproved": (
                p51["actual_root_current_purpose_proved"] is False
            ),
            "s51_open_no_selected_option": (
                p51["generation"].get("selection_status") == "OPEN_CHOICE_SET"
                and p51["generation"].get("selected_option") == ""
                and p51["generation"].get("missing_option_relation")
                == "NO_EXISTING_S49_OPTION_EXPRESSES_PAID_FINISHING_EQUIPMENT_OFFER"
            ),
            "s51_s49_actual_hold": (
                p51["generation"].get("s49_status") == "SOURCE_OWNER_HOLD"
            ),
            "s52_conditional_no_counterpart": (
                p52["candidate"].get("status")
                == "CONDITIONAL_ON_INDEPENDENT_PARTICIPATION"
                and p52["candidate"].get("counterpart_status")
                == "INDEPENDENT_PARTICIPATION_NOT_OBSERVED"
            ),
            "s52_open_no_selected_option": (
                p52["generation"].get("selection_status") == "OPEN_CHOICE_SET"
                and p52["generation"].get("selected_option") == ""
            ),
            "s52_normal_no_perform": (
                p52["normal_paid_perform_without_counterpart"].get("performed")
                is False
                and p52["normal_paid_perform_without_counterpart"].get("status")
                == "CONDITIONAL_ON_INDEPENDENT_PARTICIPATION"
            ),
            "s52_normal_no_world_or_state_change": (
                p52["normal_no_world_or_state_change"]
            ),
            "all_probes_verify": all(
                probe.get("verify_ok") is True for probe in probes.values()
            ),
            "focused_hold_tests_pass": all(
                row["all_pass"] for row in tests.values()
            ),
        }
        report = {
            "schema": "SOROK_CURRENT_B_SEAM@1",
            "result": "PASS" if all(checks.values()) else "FAIL",
            "grade": "TEST_ONLY_ENGINEERING_SOURCE_OWNER_HOLD_NOT_NATIVE",
            "commission_base": pins.COMMISSION_BASE,
            "pins": {key: pins.PINS[key].cut
                     for key in ("s48", "s49", "s50", "s51", "s52")},
            "closures": {name: {"anchor": pins.CLOSURES[name]["anchor"],
                                "keys": pins.CLOSURES[name]["keys"]}
                         for name in stages},
            "dispositions": DISPOSITIONS,
            "probes": probes,
            "tests": tests,
            "checks": checks,
            "source_manifest": str((evidence / "source_manifest.json").relative_to(RETURN)),
            "limitations": [
                "Engineering source/first-importer disposition only.",
                "No native C8/C9/C12, CAN008/CAN011, ADP, Pyat or human authority.",
                "No invented B personality, context, willingness, choice or paid counterpart.",
                "The S48 entrypoint provider call made during prior exploration is "
                "transport/narrative only and not used as B evidence.",
                "S52 controlled counterpart performance is an existing test-only "
                "port and was not executed as actual B evidence here.",
            ],
            "commands": {
                "harness": " ".join([sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]]),
                "probes": "per-probe subprocess commands recorded in logs/probe_*.log",
                "tests": {key: row["command"] for key, row in tests.items()},
            },
            "elapsed_seconds": round(time.time() - started, 3),
        }
        out = args.json_out.expanduser().resolve() if args.json_out else evidence / "current_b_seam.json"
        _json_dump(out, report)
        print(json.dumps({
            "result": report["result"],
            "json": str(out),
            "checks": checks,
            "s49": {
                "access": p49["access"].get("access_status"),
                "b_turn": p49["b_turn"],
            },
            "s50": {
                "status": p50["actual_root_missing"].get("status"),
                "reason": p50["actual_root_missing"].get("reason"),
                "missing_fields": p50["actual_root_missing"].get("missing_fields"),
            },
            "s51": {
                "relevance": p51["relevance"],
                "generation": p51["generation"],
            },
            "s52": {
                "candidate": p52["candidate"],
                "generation": p52["generation"],
                "normal": p52["normal_paid_perform_without_counterpart"],
            },
            "tests": {key: row["counts"] for key, row in tests.items()},
        }, indent=2, sort_keys=True, default=str))
        return 0 if report["result"] == "PASS" else 1
    except Exception as exc:
        failure = {
            "schema": "SOROK_CURRENT_B_SEAM_FAILURE@1",
            "result": "ERROR",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "elapsed_seconds": round(time.time() - started, 3),
        }
        _json_dump(evidence / "current_b_seam_failure.json", failure)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
