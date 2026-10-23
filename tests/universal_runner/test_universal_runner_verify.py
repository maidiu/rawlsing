"""Focused native controls for the R09 local supervisor verifier."""
from __future__ import annotations

from dataclasses import replace
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "CROSS_HQ_CONTROL_ROOM" / "universal_runner_verify.py"
SPEC = importlib.util.spec_from_file_location("universal_runner_verify", MODULE_PATH)
verify = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = verify
SPEC.loader.exec_module(verify)

SUPPORT_SOURCE = (
    "def add(a, b):\n"
    "    return a + b\n"
    "\n"
    "def double(value):\n"
    "    return value * 2\n"
)
ENTRY_SOURCE = (
    "from native_fixture import add, double\n"
    "\n"
    "RESULT = {\"label\": \"baseline\", \"value\": double(add(20, 1))}\n"
)
POLICY_BYTES = b'{"policy":"R09_TEST_POLICY","revision":1}\n'
EXPECTED_RESULT = {"label": "baseline", "value": 42}
EXPECTED_EVENTS = (
    {"module": "native_fixture", "qualname": "add", "status": "RETURNED"},
    {"module": "native_fixture", "qualname": "double", "status": "RETURNED"},
)
TRUSTED_ISSUER = "trusted-supervisor-A"


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Harness:
    def __init__(self, directory: Path, *, support_source: str = SUPPORT_SOURCE,
                 entry_source: str = ENTRY_SOURCE, issuer: str = TRUSTED_ISSUER):
        self.directory = directory
        self.support_path = directory / "native_fixture.py"
        self.entry_path = directory / "native_entry.py"
        self.policy_path = directory / "protected_policy.json"
        self.support_path.write_text(support_source, encoding="utf-8")
        self.entry_path.write_text(entry_source, encoding="utf-8")
        self.policy_path.write_bytes(POLICY_BYTES)
        self.commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        self.tree = subprocess.check_output(
            ["git", "rev-parse", f"{self.commit}^{{tree}}"],
            cwd=ROOT, text=True).strip()
        self.supervisor = verify.LocalNativeSupervisor(
            repo_root=ROOT,
            issuer=issuer,
            policy_path=self.policy_path,
            target_module="native_fixture",
            target_file=self.support_path,
            entrypoint=self.entry_path,
        )
        self.expectation = verify.TrustedExpectation(
            issuer=TRUSTED_ISSUER,
            candidate_commit=self.commit,
            candidate_tree=self.tree,
            policy_sha256=digest_bytes(POLICY_BYTES),
            run_id="run-baseline",
            nonce="nonce-baseline",
            entrypoint_sha256=digest_bytes(entry_source.encode("utf-8")),
            expected_imports={
                "native_fixture": digest_bytes(support_source.encode("utf-8")),
            },
            expected_events=EXPECTED_EVENTS,
            expected_result=EXPECTED_RESULT,
        )

    def observe(self, *, run_id: str = "run-baseline",
                nonce: str = "nonce-baseline") -> dict:
        return self.supervisor.observe(
            candidate_commit=self.commit, run_id=run_id, nonce=nonce)


def assert_refused(decision: dict, reason: str) -> None:
    assert decision["decision"] == verify.REFUSE
    assert reason in decision["reasons"], decision
    assert decision["promotion"] == verify.PROMOTION
    assert decision["generic_promotion_authorized"] is False


def test_trusted_baseline_is_accepted_locally_but_not_promoted(tmp_path):
    harness = Harness(tmp_path)
    observation = harness.observe()
    decision = verify.verify_observation(
        observation=observation, expectation=harness.expectation,
        nonce_ledger=verify.NonceLedger())

    assert decision["decision"] == verify.ACCEPT
    assert decision["reasons"] == []
    assert decision["ceiling"] == verify.CEILING
    assert decision["promotion"] == verify.PROMOTION
    assert decision["production_state"] == "DEPLOYMENT_HOLD"
    assert decision["generic_promotion_authorized"] is False
    assert decision["observed"]["result"] == EXPECTED_RESULT
    assert decision["observed"]["result_digest"] == verify.typed_digest(
        EXPECTED_RESULT)
    assert decision["bindings"]["candidate_commit"] == harness.commit
    assert decision["bindings"]["candidate_tree"] == harness.tree
    assert decision["observed"]["events"] == list(EXPECTED_EVENTS)
    assert observation["imports"]["native_fixture"]["sha256"] == (
        digest_bytes(SUPPORT_SOURCE.encode("utf-8")))
    assert "native_fixture" in observation["import_events"]


def test_candidate_authored_receipt_cannot_replace_supervisor_evidence(tmp_path):
    harness = Harness(tmp_path)
    observation = harness.observe()
    forged = {
        "native": True,
        "status": "PASS",
        "self_pin": harness.tree,
        "trace": {"actual_native_c11": True},
        "attestation": "candidate-authored",
    }
    decision = verify.verify_observation(
        observation=observation, expectation=harness.expectation,
        nonce_ledger=verify.NonceLedger(), candidate_evidence=forged)

    assert_refused(decision, "CANDIDATE_AUTHORED_EVIDENCE")


@pytest.mark.parametrize("field,mutant,reason", [
    ("candidate_commit", "0" * 40, "CANDIDATE_COMMIT_MISMATCH"),
    ("candidate_tree", "1" * 40, "CANDIDATE_TREE_MISMATCH"),
    ("policy_sha256", "2" * 64, "POLICY_MISMATCH"),
    ("entrypoint_sha256", "3" * 64, "ENTRYPOINT_DIGEST_MISMATCH"),
])
def test_wrong_commit_tree_policy_or_entrypoint_is_refused(
        tmp_path, field, mutant, reason):
    harness = Harness(tmp_path)
    observation = harness.observe()
    expectation = replace(harness.expectation, **{field: mutant})
    decision = verify.verify_observation(
        observation=observation, expectation=expectation,
        nonce_ledger=verify.NonceLedger())

    assert_refused(decision, reason)


def test_stale_nonce_and_cold_replay_are_refused(tmp_path):
    harness = Harness(tmp_path)
    ledger_path = tmp_path / "nonce-ledger.jsonl"
    observation = harness.observe()
    first = verify.verify_observation(
        observation=observation, expectation=harness.expectation,
        nonce_ledger=verify.NonceLedger(ledger_path))
    assert first["decision"] == verify.ACCEPT

    cold_ledger = verify.NonceLedger(ledger_path)
    replay = verify.verify_observation(
        observation=observation, expectation=harness.expectation,
        nonce_ledger=cold_ledger)
    assert_refused(replay, "NONCE_REPLAYED")

    stale_observation = harness.observe(run_id="run-stale", nonce="nonce-current")
    stale_expectation = replace(
        harness.expectation, run_id="run-stale", nonce="nonce-stale")
    stale = verify.verify_observation(
        observation=stale_observation, expectation=stale_expectation,
        nonce_ledger=verify.NonceLedger())
    assert_refused(stale, "NONCE_MISMATCH")


def test_fake_issuer_is_refused(tmp_path):
    harness = Harness(tmp_path, issuer="candidate-issued-supervisor")
    observation = harness.observe()
    decision = verify.verify_observation(
        observation=observation, expectation=harness.expectation,
        nonce_ledger=verify.NonceLedger())

    assert_refused(decision, "ISSUER_MISMATCH")


def test_missing_native_event_from_actual_process_is_refused(tmp_path):
    entry = (
        "from native_fixture import add\n"
        "\n"
        "_ = add(20, 1)\n"
        "RESULT = {\"label\": \"baseline\", \"value\": 42}\n"
    )
    harness = Harness(tmp_path, entry_source=entry)
    observation = harness.observe()
    decision = verify.verify_observation(
        observation=observation, expectation=harness.expectation,
        nonce_ledger=verify.NonceLedger())

    assert_refused(decision, "NATIVE_EVENT_ANTI_JOIN")
    assert decision["observed"]["result"] == EXPECTED_RESULT


def test_missing_expected_native_import_is_refused(tmp_path):
    harness = Harness(tmp_path)
    observation = harness.observe()
    expectation = replace(
        harness.expectation,
        expected_imports={
            **harness.expectation.expected_imports,
            "native_absent": "4" * 64,
        })
    decision = verify.verify_observation(
        observation=observation, expectation=expectation,
        nonce_ledger=verify.NonceLedger())

    assert_refused(decision, "NATIVE_IMPORT_ANTI_JOIN")
    assert_refused(decision, "NATIVE_IMPORT_EVENT_MISSING:native_absent")


def test_same_name_status_spoof_from_actual_process_is_refused(tmp_path):
    support = (
        "def add(a, b):\n"
        "    return a + b\n"
        "\n"
        "def double(value):\n"
        "    raise RuntimeError('forced status mutation')\n"
    )
    entry = (
        "from native_fixture import add, double\n"
        "\n"
        "try:\n"
        "    double(add(20, 1))\n"
        "except RuntimeError:\n"
        "    pass\n"
        "RESULT = {\"label\": \"baseline\", \"value\": 42}\n"
    )
    harness = Harness(tmp_path, support_source=support, entry_source=entry)
    observation = harness.observe()
    decision = verify.verify_observation(
        observation=observation, expectation=harness.expectation,
        nonce_ledger=verify.NonceLedger())

    assert_refused(decision, "NATIVE_EVENT_STATUS_MISMATCH")
    assert decision["observed"]["result"] == EXPECTED_RESULT
    assert decision["observed"]["events"] == [
        {"module": "native_fixture", "qualname": "add", "status": "RETURNED"},
        {"module": "native_fixture", "qualname": "double", "status": "RAISED"},
    ]


def test_changed_runtime_import_refused_then_cold_restore_accepted(tmp_path):
    harness = Harness(tmp_path)
    ledger = verify.NonceLedger()
    baseline = verify.verify_observation(
        observation=harness.observe(run_id="run-before", nonce="nonce-before"),
        expectation=replace(harness.expectation, run_id="run-before",
                            nonce="nonce-before"),
        nonce_ledger=ledger)
    assert baseline["decision"] == verify.ACCEPT

    mutated = SUPPORT_SOURCE + "\nRUNTIME_MUTATION = True\n"
    harness.support_path.write_text(mutated, encoding="utf-8")
    changed = verify.verify_observation(
        observation=harness.observe(run_id="run-changed", nonce="nonce-changed"),
        expectation=replace(harness.expectation, run_id="run-changed",
                            nonce="nonce-changed"),
        nonce_ledger=ledger)
    assert_refused(changed, "NATIVE_IMPORT_DIGEST_MISMATCH:native_fixture")

    harness.support_path.write_text(SUPPORT_SOURCE, encoding="utf-8")
    restored = verify.verify_observation(
        observation=harness.observe(run_id="run-restored", nonce="nonce-restored"),
        expectation=replace(harness.expectation, run_id="run-restored",
                            nonce="nonce-restored"),
        nonce_ledger=ledger)
    assert restored["decision"] == verify.ACCEPT
    assert restored["reasons"] == []


def test_wrong_result_from_actual_process_is_refused(tmp_path):
    entry = (
        "from native_fixture import add, double\n"
        "\n"
        "RESULT = {\"label\": \"baseline\", \"value\": double(add(20, 1)) - 1}\n"
    )
    harness = Harness(tmp_path, entry_source=entry)
    observation = harness.observe()
    decision = verify.verify_observation(
        observation=observation, expectation=harness.expectation,
        nonce_ledger=verify.NonceLedger())

    assert_refused(decision, "RESULT_MISMATCH")
    assert decision["observed"]["result"] == {"label": "baseline", "value": 41}
