"""Focused checks for the existing MCR commission/return validator.

These tests use a temporary synthetic Git repository.  They do not execute or
authorize any source, respondent, native, science or actor operation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from CROSS_HQ_CONTROL_ROOM import verify_copy_paste_commission_r1 as validator


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


def _fixture(tmp_path: Path) -> tuple[Path, str, str, str, Path]:
    repo = tmp_path / "candidate"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "validator-test@example.invalid")
    _git(repo, "config", "user.name", "validator-test")

    source = repo / "registry" / "obligations.tsv"
    _write(source, "id\tdestination\nOBL-A\tW03\nOBL-B\tW04\n")
    _git(repo, "add", "registry/obligations.tsv")
    _git(repo, "commit", "-q", "-m", "source registry")
    source_commit = _git(repo, "rev-parse", "HEAD")
    source_blob = _git(repo, "rev-parse", f"HEAD:{source.relative_to(repo).as_posix()}")

    output_a = repo / "outputs" / "OBL-A.txt"
    evidence_a = repo / "evidence" / "OBL-A.txt"
    output_b = repo / "outputs" / "OBL-B.txt"
    evidence_b = repo / "evidence" / "OBL-B.txt"
    delivered = repo / "delivered_ids.txt"
    _write(output_a, "A output\n")
    _write(evidence_a, "A evidence\n")
    _write(output_b, "B output\n")
    _write(evidence_b, "B evidence\n")
    _write(delivered, "OBL-A\nOBL-B\n")
    tracked_evidence = repo / "RECEIVING_EVIDENCE.md"
    _write(tracked_evidence, "tracked self-contained placeholder\n")
    _git(repo, "add", "outputs", "evidence", "delivered_ids.txt", "RECEIVING_EVIDENCE.md")
    _git(repo, "commit", "-q", "-m", "candidate outputs")
    candidate = _git(repo, "rev-parse", "HEAD")

    source_tuple = {
        "path": source.relative_to(repo).as_posix(),
        "commit": source_commit,
        "blob": source_blob,
    }
    obligations = []
    for oid, destination in (("OBL-A", "W03"), ("OBL-B", "W04")):
        obligations.append({
            "id": oid,
            "result": f"Exact temporary {destination} obligation check",
            "output": f"outputs/{oid}.txt",
            "check_kind": "SOURCE",
            "check": f"SOURCE: exact synthetic source row {oid}",
            "positive": f"PASS={oid} exact source row is present",
            "negative": f"RED={oid} source row is absent",
            "evidence": f"evidence/{oid}.txt",
            "minimum_grade": "S1",
            "consumer": "temporary exact candidate receiver",
            "owner": "separate temporary receiver",
            "failure": "INCOMPLETE",
            "source": source_tuple,
        })
    scope = {
        "parent": "Synthetic exact external evidence boundary test",
        "source": source_tuple,
        "expected_count": 2,
        "identity_columns": ["id"],
        "enumerator": "RUN: read synthetic exact identities A and B",
        "no_drop_check": "RUN: compare synthetic exact identities A and B",
    }
    receiving = {
        "gate": "python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py --verify-return",
        "independent_owner": "separate temporary exact-head receiver",
        "all_obligations": "PASS_REQUIRED",
        "author_ceiling": "DELIVERED_PENDING_RECEIVING",
        "on_any_failure": "INCOMPLETE",
    }
    contract = (
        "MCR_COMPLETION_CONTRACT_BEGIN\n"
        + "MCR_SCOPE: " + json.dumps(scope, sort_keys=True) + "\n"
        + "".join("MCR_OBLIGATION: " + json.dumps(ob, sort_keys=True) + "\n" for ob in obligations)
        + "MCR_RECEIVING: " + json.dumps(receiving, sort_keys=True) + "\n"
        + "MCR_COMPLETION_CONTRACT_END"
    )
    fields = {
        "REPOSITORY": "example/rawlsing-test",
        "AGENT_TYPE": "bounded synthetic validator test engineer",
        "INTELLIGENCE_LEVEL": "I3",
        "SINGLE_AGENT_FULL_DELIVERABLE": "YES",
        "EXECUTION_SURFACE": "S0_S1 source records; S2 temporary repository only",
        "USER_SELECTED_EDITOR_MODEL_PAIR": "synthetic local editor model test",
        "MODEL": "synthetic-test-model",
        "REASONING": "HIGH",
        "PROVIDER/EDITOR_HARNESS": "synthetic test harness",
        "MODEL_MAX_AVAILABILITY": "SYNTHETIC_TEST_ONLY",
        "HOST_ACCOUNT_QUOTA_COST": "UNKNOWN_TEST_ONLY",
        "BRANCH": "agent/synthetic-validator-test",
        "STARTUP_SHA": "a" * 40,
        "ACTIVE_WORKER_NO_DISTURBANCE": "synthetic isolated temp repository only",
        "BROWSER?": "NO_SYNTHETIC_TEST",
        "DEEPSEEK?": "YES_SYNTHETIC_TEST",
        "CODEX_6_1_HIGH_NECESSARY?": "NO_SYNTHETIC_TEST",
        "OTHERWISE_MIDDLE?": "YES_SYNTHETIC_TEST",
        "WHY_NOT_BROWSER": "synthetic filesystem evidence requires local test repository",
        "WHY_NOT_FLASH": "synthetic format test has no model execution",
        "WHY_NOT_CODEX_HIGH": "no consequence or source decision in synthetic test",
        "WHY_NOT_MIDDLE": "synthetic test is the smallest local format check",
        "SCIENCE_SOURCE_ACTOR_AUTHORITY": "NO_SOURCE_SCIENCE_ACTOR_AUTHORITY",
        "POST_RETURN_INDEPENDENT_REVIEW": "separate synthetic receiver at same candidate",
        "MCR": "REQUIRED",
        "COMMISSION_KIND": "BUILD",
        "CONTRACT_ID": "SYNTHETIC-MCR-VALIDATOR-TEST",
        "CONTRACT_SOURCE_CUT": f"synthetic source @ {source_commit}",
        "WORK_SCOPE_AND_FLIGHT": "PARENT=synthetic exact validator test; TRANCHE=external evidence boundary; PILOT=CALIBRATION_NONTERMINAL synthetic; PARALLEL=READY synthetic source checks",
        "TERMINAL_CONSUMER_AND_EFFECT": "CONSUMER=synthetic exact receiver; EFFECT=external evidence path rule",
        "FROZEN_ORACLE_AND_COUNTEREXAMPLE": "POS=external evidence accepted; NEG=tracked evidence rejected",
        "PREBUILD_CONTRACT_CHALLENGE": "CHALLENGE=tracked candidate evidence self-certifies; DISPOSITION=exclude candidate tracking",
        "EXECUTION_AND_AUTHOR_PREFLIGHT": "RUNNER=temporary python git fixture; PREFLIGHT=validate and verify return",
        "CLOSURE_AND_OUT_OF_SCOPE": "ACCEPT_AT=synthetic validator format only; EXCLUDE=real source and native authority",
    }
    prompt = "LAUNCH synthetic MCR validator test\n" + "\n".join(
        f"{key}: {value}" for key, value in fields.items()
    ) + "\nENGINEERING SCIENTIFIC AUTHORITY source review test return\n" + contract
    commission = (
        "AGENT TYPE: synthetic validator test engineer\n"
        "INTELLIGENCE LEVEL: I3\n"
        "```text\n" + prompt + "\n```\n"
    )
    checked = validator.validate(commission)
    assert checked["status"] == "PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH", checked["errors"]
    contract_sha = checked["mcr_completion_contract_sha256"]
    records = []
    for oid in ("OBL-A", "OBL-B"):
        records.append({
            "id": oid,
            "candidate_sha": candidate,
            "contract_sha256": contract_sha,
            "status": "PASS",
            "grade": "S1",
            "output_file": f"outputs/{oid}.txt",
            "output_sha256": _sha(repo / "outputs" / f"{oid}.txt"),
            "evidence_file": f"evidence/{oid}.txt",
            "evidence_sha256": _sha(repo / "evidence" / f"{oid}.txt"),
        })
    coverage = {
        "candidate_sha": candidate,
        "contract_sha256": contract_sha,
        "delivered_ids_file": "delivered_ids.txt",
        "delivered_ids_sha256": _sha(repo / "delivered_ids.txt"),
    }
    evidence_text = "MCR_COMPLETION_EVIDENCE_BEGIN\n" + "".join(
        "MCR_EVIDENCE: " + json.dumps(record, sort_keys=True) + "\n" for record in records
    ) + "MCR_COVERAGE: " + json.dumps(coverage, sort_keys=True) + "\nMCR_COMPLETION_EVIDENCE_END\n"
    external = tmp_path / "RECEIVING_EVIDENCE.md"
    _write(external, evidence_text)
    return repo, commission, candidate, evidence_text, external


def test_launch_artifact_has_single_external_fenced_prompt():
    repo = Path(__file__).resolve().parents[1]
    launch = repo / "WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md"
    result = validator.validate(launch.read_text(encoding="utf-8"))
    assert result["status"] == "PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH", result["errors"]
    assert result["mcr_required_obligation_count"] == 12
    frozen = (repo / "PYAT_W03_W04_MCR_C_Commission.md").read_text(encoding="utf-8")
    assert validator.validate(frozen)["status"] == "RED_INVALID_FOR_DISPATCH"


def test_external_evidence_positive_and_tracked_negative(tmp_path):
    repo, commission, candidate, evidence_text, external = _fixture(tmp_path)
    positive = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=external
    )
    assert positive["status"] == "READY_FOR_INDEPENDENT_RECEIVING", positive["errors"]
    assert positive["evidence_externality"].startswith("OUTSIDE_CANDIDATE_ROOT")
    tracked = repo / "RECEIVING_EVIDENCE.md"
    negative = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=tracked
    )
    assert negative["status"] == "RED_INCOMPLETE"
    assert "MCR_C_EVIDENCE_TRACKED_AT_CANDIDATE" in negative["errors"]
    restored = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=external
    )
    assert restored["status"] == "READY_FOR_INDEPENDENT_RECEIVING", restored["errors"]


def test_forged_candidate_and_output_hash_are_rejected(tmp_path):
    repo, commission, candidate, evidence_text, external = _fixture(tmp_path)
    wrong_candidate = validator.verify_return(
        commission, evidence_text, "f" * 40, repo, returned_path=external
    )
    assert wrong_candidate["status"] == "RED_INCOMPLETE"
    assert "MCR_C_CHECKOUT_NOT_EXACT_CANDIDATE" in wrong_candidate["errors"]

    forged = evidence_text.replace(_sha(repo / "outputs" / "OBL-A.txt"), "0" * 64, 1)
    forged_result = validator.verify_return(
        commission, forged, candidate, repo, returned_path=external
    )
    assert forged_result["status"] == "RED_INCOMPLETE"
    assert any("MCR_C_OUTPUT_DIGEST_MISMATCH_OBL-A" == item for item in forged_result["errors"])
    restored = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=external
    )
    assert restored["status"] == "READY_FOR_INDEPENDENT_RECEIVING", restored["errors"]


def test_existing_self_test_remains_green():
    result = validator.self_test()
    assert result["status"] == "PASS_SELF_TEST"
    assert result["negative_mutations_rejected"] == 32
