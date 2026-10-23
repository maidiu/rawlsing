"""Focused R2 native controls for the external-trust-root verifier."""
from __future__ import annotations

from dataclasses import replace
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

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
POLICY_BYTES = b'{"policy":"R09_R2_TEST_POLICY","revision":2}\n'
EXPECTED_RESULT = {"label": "baseline", "value": 42}
EXPECTED_EVENTS = (
    {"module": "native_fixture", "qualname": "add", "status": "RETURNED"},
    {"module": "native_fixture", "qualname": "double", "status": "RETURNED"},
)
TRUSTED_ISSUER = "trusted-supervisor-A"
C11_RESULT = {
    "accepted": True,
    "disposition": "ACCEPTED_C11_LOGICAL_RELEASE",
    "event_count": 2,
    "release_id": "REL-R09",
    "repository_length": 1,
    "m01_m18_count": 18,
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def git_blob(repo: Path, commit: str, relative: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{commit}:{relative}"], cwd=repo)


class RepoFixture:
    def __init__(self, root: Path, *, support_source: str = SUPPORT_SOURCE,
                 entry_source: str = ENTRY_SOURCE):
        self.root = root
        root.mkdir(parents=True, exist_ok=True)
        self.repo = root / "candidate"
        self.repo.mkdir()
        self.support = self.repo / "native_fixture.py"
        self.entry = self.repo / "native_entry.py"
        self.policy = root / "protected_policy.json"
        self.support.write_text(support_source, encoding="utf-8")
        self.entry.write_text(entry_source, encoding="utf-8")
        self.policy.write_bytes(POLICY_BYTES)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "r09@example.invalid")
        git(self.repo, "config", "user.name", "R09 Fixture")
        git(self.repo, "add", "native_fixture.py", "native_entry.py")
        git(self.repo, "commit", "-q", "-m", "fixture")
        self.commit = git(self.repo, "rev-parse", "HEAD")
        self.tree = git(self.repo, "rev-parse", f"{self.commit}^{{tree}}")
        self.trust_root = verify.TrustRoot(TRUSTED_ISSUER)
        self.supervisor = verify.LocalNativeSupervisor(
            repo_root=self.repo,
            policy_path=self.policy,
            target_module="native_fixture",
            target_file=self.support,
            entrypoint=self.entry,
            trust_root=self.trust_root,
        )
        self.expectation = self.make_expectation()

    def make_expectation(self, *, run_id: str = "run-baseline",
                         nonce: str = "nonce-baseline") -> verify.TrustedExpectation:
        return verify.TrustedExpectation(
            issuer=TRUSTED_ISSUER,
            candidate_commit=self.commit,
            candidate_tree=self.tree,
            policy_sha256=digest_bytes(POLICY_BYTES),
            run_id=run_id,
            nonce=nonce,
            entrypoint_sha256=digest_bytes(git_blob(
                self.repo, self.commit, "native_entry.py")),
            expected_imports={
                "native_fixture": digest_bytes(git_blob(
                    self.repo, self.commit, "native_fixture.py")),
            },
            expected_events=EXPECTED_EVENTS,
            expected_result=EXPECTED_RESULT,
            trust_root_fingerprint=self.trust_root.fingerprint,
        )

    def observe(self, *, run_id: str = "run-baseline",
                nonce: str = "nonce-baseline") -> dict:
        return self.supervisor.observe(
            candidate_commit=self.commit, run_id=run_id, nonce=nonce)

    def verify(self, observation, expectation=None, ledger=None):
        return verify.verify_observation(
            observation=observation,
            expectation=expectation or self.expectation,
            nonce_ledger=ledger or verify.NonceLedger(
                self.root / "default-ledger.jsonl"),
            trust_root=self.trust_root)


def assert_refused(decision: dict, reason: str) -> None:
    assert decision["decision"] == verify.REFUSE
    assert reason in decision["reasons"], decision
    assert decision["promotion"] == verify.PROMOTION
    assert decision["generic_promotion_authorized"] is False


def test_sealed_baseline_is_accepted_locally_but_never_promoted(tmp_path):
    fixture = RepoFixture(tmp_path)
    observation = fixture.observe()
    decision = fixture.verify(observation)

    assert decision["decision"] == verify.ACCEPT
    assert decision["reasons"] == []
    assert decision["ceiling"] == verify.CEILING
    assert decision["production_state"] == "DEPLOYMENT_HOLD"
    assert decision["generic_promotion_authorized"] is False
    assert decision["observed"]["result"] == EXPECTED_RESULT
    assert observation["imports"]["native_fixture"]["tree_bound"] is True
    assert observation["entrypoint"]["tree_bound"] is True


def test_existing_c11_native_owner_and_repository_are_executed(tmp_path):
    commit = git(ROOT, "rev-parse", "HEAD")
    tree = git(ROOT, "rev-parse", f"{commit}^{{tree}}")
    entry = ROOT / "tests" / "universal_runner" / "native_c11_entry.py"
    case = ROOT / "tests" / "universal_runner" / "native_c11_case.py"
    policy = tmp_path / "policy.json"
    policy.write_bytes(POLICY_BYTES)
    trust_root = verify.TrustRoot(TRUSTED_ISSUER)
    supervisor = verify.LocalNativeSupervisor(
        repo_root=ROOT, policy_path=policy,
        target_module="native_c11_entry", target_file=entry,
        entrypoint=entry, trust_root=trust_root)
    expectation = verify.TrustedExpectation(
        issuer=TRUSTED_ISSUER, candidate_commit=commit, candidate_tree=tree,
        policy_sha256=digest_bytes(POLICY_BYTES),
        run_id="run-c11", nonce="nonce-c11",
        entrypoint_sha256=digest_bytes(git_blob(
            ROOT, commit, "tests/universal_runner/native_c11_entry.py")),
        expected_imports={
            "native_c11_case": digest_bytes(git_blob(
                ROOT, commit, "tests/universal_runner/native_c11_case.py")),
            "rawlsing_next.pre553_c11_ingest": digest_bytes(git_blob(
                ROOT, commit, "rawlsing_next/pre553_c11_ingest.py")),
            "rawlsing_next.pre553_c11_repository": digest_bytes(git_blob(
                ROOT, commit, "rawlsing_next/pre553_c11_repository.py")),
        },
        expected_events=(
            {"module": "native_c11_entry", "qualname": "run_native",
             "status": "RETURNED"},
        ),
        expected_result=C11_RESULT,
        trust_root_fingerprint=trust_root.fingerprint,
    )
    observation = supervisor.observe(
        candidate_commit=commit, run_id="run-c11", nonce="nonce-c11")
    decision = verify.verify_observation(
        observation=observation, expectation=expectation,
        nonce_ledger=verify.NonceLedger(tmp_path / "c11-ledger.jsonl"),
        trust_root=trust_root)

    assert decision["decision"] == verify.ACCEPT, decision
    assert decision["observed"]["result"] == C11_RESULT
    assert observation["imports"]["native_c11_case"]["tree_bound"] is True
    assert observation["imports"]["rawlsing_next.pre553_c11_ingest"]["tree_bound"] is True
    assert "rawlsing_next.pre553_c11_ingest" in observation["import_events"]


def test_unsealed_mapping_and_mutated_seal_are_refused(tmp_path):
    fixture = RepoFixture(tmp_path)
    observation = fixture.observe()
    fabricated = dict(observation)
    decision = fixture.verify(fabricated)
    assert_refused(decision, "UNTRUSTED_OBSERVATION")

    observation["issuer"] = "attacker"
    decision = fixture.verify(observation)
    assert_refused(decision, "OBSERVATION_AUTHENTICATION_FAILED")


def test_attacker_trust_root_and_rewritten_issuer_are_refused(tmp_path):
    fixture = RepoFixture(tmp_path)
    attacker = verify.TrustRoot("attacker-issuer")
    observation = fixture.observe()
    observation["issuer"] = attacker.issuer
    decision = fixture.verify(observation)
    assert_refused(decision, "OBSERVATION_AUTHENTICATION_FAILED")

    attacker_supervisor = verify.LocalNativeSupervisor(
        repo_root=fixture.repo, policy_path=fixture.policy,
        target_module="native_fixture", target_file=fixture.support,
        entrypoint=fixture.entry, trust_root=attacker)
    attacker_observation = attacker_supervisor.observe(
        candidate_commit=fixture.commit, run_id="run-baseline",
        nonce="nonce-baseline")
    decision = fixture.verify(attacker_observation)
    assert_refused(decision, "TRUST_ROOT_FINGERPRINT_MISMATCH")


def test_out_of_tree_execution_is_refused_before_acceptance(tmp_path):
    repo = tmp_path / "candidate"
    repo.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    support = outside / "native_fixture.py"
    entry = outside / "native_entry.py"
    policy = tmp_path / "policy.json"
    support.write_text(SUPPORT_SOURCE, encoding="utf-8")
    entry.write_text(ENTRY_SOURCE, encoding="utf-8")
    policy.write_bytes(POLICY_BYTES)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "r09@example.invalid")
    git(repo, "config", "user.name", "R09 Fixture")
    git(repo, "commit", "-q", "--allow-empty", "-m", "empty")
    commit = git(repo, "rev-parse", "HEAD")
    root = verify.TrustRoot(TRUSTED_ISSUER)
    supervisor = verify.LocalNativeSupervisor(
        repo_root=repo, policy_path=policy, target_module="native_fixture",
        target_file=support, entrypoint=entry, trust_root=root)
    observation = supervisor.observe(
        candidate_commit=commit, run_id="run-outside", nonce="nonce-outside")
    expectation = verify.TrustedExpectation(
        issuer=TRUSTED_ISSUER, candidate_commit=commit,
        candidate_tree=git(repo, "rev-parse", f"{commit}^{{tree}}"),
        policy_sha256=digest_bytes(POLICY_BYTES), run_id="run-outside",
        nonce="nonce-outside", entrypoint_sha256=digest_bytes(
            entry.read_bytes()),
        expected_imports={"native_fixture": digest_bytes(
            support.read_bytes())}, expected_events=EXPECTED_EVENTS,
        expected_result=EXPECTED_RESULT,
        trust_root_fingerprint=root.fingerprint)
    decision = verify.verify_observation(
        observation=observation, expectation=expectation,
        nonce_ledger=verify.NonceLedger(tmp_path / "ledger.jsonl"),
        trust_root=root)
    assert_refused(decision, "SUPERVISOR_REFUSED:ENTRYPOINT_OUTSIDE_CANDIDATE_TREE")


def test_loaded_bytes_not_restored_file_are_refused(tmp_path):
    fixture = RepoFixture(tmp_path)
    mutated = SUPPORT_SOURCE + "\nMUTATED_AT_RUNTIME = True\n"
    fixture.support.write_text(mutated, encoding="utf-8")
    observation = fixture.observe()
    decision = fixture.verify(observation)
    assert_refused(
        decision,
        "NATIVE_CUSTODY_FAILED:IMPORT_LOADED_BYTES_NOT_IN_TREE:native_fixture")
    assert observation["imports"]["native_fixture"]["loaded_sha256"] != (
        observation["imports"]["native_fixture"]["tree_sha256"])


def test_self_restoring_import_is_refused_from_load_time_digest(tmp_path):
    original = SUPPORT_SOURCE
    support_path = tmp_path / "candidate" / "native_fixture.py"
    mutated = (
        "import atexit\n"
        "from pathlib import Path\n"
        f"_ORIGINAL = {original!r}\n"
        "atexit.register(lambda: Path(__file__).write_text(_ORIGINAL, encoding='utf-8'))\n"
        "def add(a, b):\n"
        "    return a + b\n"
        "\n"
        "def double(value):\n"
        "    return value * 2 - 1\n"
    )
    fixture = RepoFixture(tmp_path, support_source=original)
    support_path.write_text(mutated, encoding="utf-8")
    observation = fixture.observe()
    decision = fixture.verify(observation)
    assert_refused(
        decision,
        "NATIVE_CUSTODY_FAILED:IMPORT_LOADED_BYTES_NOT_IN_TREE:native_fixture")
    assert support_path.read_text(encoding="utf-8") == mutated
    assert observation["result"] == {"label": "baseline", "value": 41}
    support_path.write_text(original, encoding="utf-8")


def test_mandatory_durable_ledger_and_cold_replay_refusal(tmp_path):
    fixture = RepoFixture(tmp_path)
    observation = fixture.observe()
    in_memory = fixture.verify(observation, ledger=verify.NonceLedger())
    assert_refused(in_memory, "NONCE_LEDGER_NOT_DURABLE")

    ledger_path = tmp_path / "ledger.jsonl"
    ledger_a = verify.NonceLedger(ledger_path)
    ledger_b = verify.NonceLedger(ledger_path)
    first = fixture.verify(observation, ledger=ledger_a)
    second = fixture.verify(observation, ledger=ledger_b)
    assert first["decision"] == verify.ACCEPT
    assert_refused(second, "NONCE_REPLAYED")

    cold = fixture.verify(observation, ledger=verify.NonceLedger(ledger_path))
    assert_refused(cold, "NONCE_REPLAYED")


def test_stale_nonce_and_wrong_bindings_are_refused(tmp_path):
    fixture = RepoFixture(tmp_path)
    observation = fixture.observe(run_id="run-baseline", nonce="nonce-current")
    ledger = verify.NonceLedger(tmp_path / "ledger.jsonl")
    stale = fixture.verify(
        observation,
        expectation=fixture.make_expectation(
            run_id="run-baseline", nonce="nonce-stale"),
        ledger=ledger)
    assert_refused(stale, "NONCE_MISMATCH")

    for field, mutant, reason in (
        ("candidate_commit", "0" * 40, "CANDIDATE_COMMIT_MISMATCH"),
        ("candidate_tree", "1" * 40, "CANDIDATE_TREE_MISMATCH"),
        ("policy_sha256", "2" * 64, "POLICY_MISMATCH"),
        ("entrypoint_sha256", "3" * 64, "ENTRYPOINT_DIGEST_MISMATCH"),
    ):
        expectation = replace(fixture.expectation, **{field: mutant})
        decision = fixture.verify(observation, expectation=expectation,
                                  ledger=verify.NonceLedger(
                                      tmp_path / f"{field}.jsonl"))
        assert_refused(decision, reason)


def test_missing_event_status_spoof_and_wrong_result_are_refused(tmp_path):
    entry_missing = (
        "from native_fixture import add\n"
        "_ = add(20, 1)\n"
        "RESULT = {\"label\": \"baseline\", \"value\": 42}\n"
    )
    fixture = RepoFixture(tmp_path / "missing", entry_source=entry_missing)
    decision = fixture.verify(fixture.observe())
    assert_refused(decision, "NATIVE_EVENT_ANTI_JOIN")

    support = (
        "def add(a, b):\n"
        "    return a + b\n"
        "\n"
        "def double(value):\n"
        "    raise RuntimeError('forced status mutation')\n"
    )
    entry = (
        "from native_fixture import add, double\n"
        "try:\n"
        "    double(add(20, 1))\n"
        "except RuntimeError:\n"
        "    pass\n"
        "RESULT = {\"label\": \"baseline\", \"value\": 42}\n"
    )
    spoof = RepoFixture(tmp_path / "spoof", support_source=support,
                        entry_source=entry)
    decision = spoof.verify(spoof.observe())
    assert_refused(decision, "NATIVE_EVENT_STATUS_MISMATCH")

    wrong = RepoFixture(
        tmp_path / "wrong",
        entry_source=(
            "from native_fixture import add, double\n"
            "RESULT = {\"label\": \"baseline\", \"value\": double(add(20, 1)) - 1}\n"
        ))
    decision = wrong.verify(wrong.observe())
    assert_refused(decision, "RESULT_MISMATCH")


def test_malformed_typed_inputs_fail_closed_without_crashing(tmp_path):
    fixture = RepoFixture(tmp_path)
    observation = fixture.observe()
    observation["result"] = {"x": {1, 2}}
    decision = fixture.verify(observation)
    assert_refused(decision, "OBSERVATION_AUTHENTICATION_FAILED")

    bad_expectation = replace(fixture.expectation,
                              expected_result={"x": {1, 2}})
    decision = fixture.verify(observation, expectation=bad_expectation)
    assert_refused(decision, "EXPECTATION_RESULT_NOT_SERIALIZABLE")


def test_cli_requires_durable_ledger_and_trust_root(tmp_path):
    fixture = RepoFixture(tmp_path)
    observation = fixture.observe()
    observation_path = tmp_path / "observation.json"
    expectation_path = tmp_path / "expectation.json"
    key_path = tmp_path / "trust-root.key"
    observation_path.write_text(json.dumps(
        verify.serialize_observation(observation)), encoding="utf-8")
    expectation_path.write_text(json.dumps({
        "issuer": fixture.expectation.issuer,
        "candidate_commit": fixture.expectation.candidate_commit,
        "candidate_tree": fixture.expectation.candidate_tree,
        "policy_sha256": fixture.expectation.policy_sha256,
        "run_id": fixture.expectation.run_id,
        "nonce": fixture.expectation.nonce,
        "entrypoint_sha256": fixture.expectation.entrypoint_sha256,
        "expected_imports": dict(fixture.expectation.expected_imports),
        "expected_events": [dict(row) for row in
                            fixture.expectation.expected_events],
        "expected_result": fixture.expectation.expected_result,
        "trust_root_fingerprint": fixture.expectation.trust_root_fingerprint,
    }), encoding="utf-8")
    key_path.write_bytes(fixture.trust_root._key)
    base = ["/usr/local/bin/python3", str(MODULE_PATH),
            "--observation", str(observation_path),
            "--expectation", str(expectation_path),
            "--trust-root-key", str(key_path)]
    first = subprocess.run(base, capture_output=True, text=True)
    second = subprocess.run(base, capture_output=True, text=True)
    assert first.returncode == 2
    assert second.returncode == 2
    assert json.loads(first.stdout)["decision"] == verify.REFUSE
    assert json.loads(second.stdout)["decision"] == verify.REFUSE
    assert "NONCE_LEDGER_NOT_DURABLE" in json.loads(first.stdout)["reasons"]
    no_root = subprocess.run(base[:-2], capture_output=True, text=True)
    assert no_root.returncode == 2
    assert "TRUST_ROOT_REQUIRED" in json.loads(no_root.stdout)["reasons"]

    ledger_path = tmp_path / "cli-ledger.jsonl"
    with_ledger = base + ["--nonce-ledger", str(ledger_path)]
    first = subprocess.run(with_ledger, capture_output=True, text=True)
    second = subprocess.run(with_ledger, capture_output=True, text=True)
    assert first.returncode == 0
    assert json.loads(first.stdout)["decision"] == verify.ACCEPT
    assert second.returncode == 2
    assert "NONCE_REPLAYED" in json.loads(second.stdout)["reasons"]


def test_cross_process_nonce_claim_is_atomic(tmp_path):
    ledger_path = tmp_path / "atomic-ledger.jsonl"
    code = (
        "import importlib.util, sys\n"
        "spec = importlib.util.spec_from_file_location('r09v', sys.argv[1])\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "sys.modules['r09v'] = module\n"
        "spec.loader.exec_module(module)\n"
        "print(module.NonceLedger(sys.argv[2]).claim('issuer', 'run', 'nonce'))\n"
    )
    processes = [
        subprocess.Popen(["/usr/local/bin/python3", "-c", code,
                          str(MODULE_PATH), str(ledger_path)],
                         stdout=subprocess.PIPE, text=True)
        for _ in range(2)
    ]
    outcomes = sorted(proc.communicate(timeout=60)[0].strip()
                      for proc in processes)
    assert outcomes == ["CLAIMED", "REPLAYED"]
