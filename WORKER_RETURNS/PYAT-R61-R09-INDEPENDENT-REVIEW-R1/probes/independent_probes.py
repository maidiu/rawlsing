#!/usr/bin/env python3
"""Independent hostile probes for R61-R09V. Read-only against candidate code.

Disposable fixtures/mutant copies live under this returnroot only.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
RETURNROOT = HERE.parent
ROOT = RETURNROOT.parents[1]
CANDIDATE_MODULE = ROOT / "CROSS_HQ_CONTROL_ROOM" / "universal_runner_verify.py"
WORK = HERE / "work"

SUPPORT = (
    "def add(a, b):\n"
    "    return a + b\n"
    "\n"
    "def double(value):\n"
    "    return value * 2\n"
)
ENTRY = (
    "from native_fixture import add, double\n"
    "\n"
    "RESULT = {\"label\": \"baseline\", \"value\": double(add(20, 1))}\n"
)
POLICY = b'{"policy":"REVIEWER_POLICY","revision":7}\n'
RESULT = {"label": "baseline", "value": 42}
EVENTS = (
    {"module": "native_fixture", "qualname": "add", "status": "RETURNED"},
    {"module": "native_fixture", "qualname": "double", "status": "RETURNED"},
)
ISSUER = "trusted-supervisor-A"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


class Fixture:
    def __init__(self, module, *, support_source: str = SUPPORT,
                 entry_source: str = ENTRY, issuer: str = ISSUER,
                 expected_support: str | None = None):
        self.module = module
        self.dir = Path(tempfile.mkdtemp(prefix="r09v-", dir=WORK))
        self.support = self.dir / "native_fixture.py"
        self.entry = self.dir / "native_entry.py"
        self.policy = self.dir / "policy.json"
        self.support.write_text(support_source, encoding="utf-8")
        self.entry.write_text(entry_source, encoding="utf-8")
        self.policy.write_bytes(POLICY)
        self.commit = git("rev-parse", "HEAD")
        self.tree = git("rev-parse", f"{self.commit}^{{tree}}")
        self.expected_support = (SUPPORT if expected_support is None
                                 else expected_support)
        self.expectation = module.TrustedExpectation(
            issuer=ISSUER,
            candidate_commit=self.commit,
            candidate_tree=self.tree,
            policy_sha256=digest(POLICY),
            run_id="run-baseline",
            nonce="nonce-baseline",
            entrypoint_sha256=digest(entry_source.encode()),
            expected_imports={
                "native_fixture": digest(self.expected_support.encode()),
            },
            expected_events=EVENTS,
            expected_result=RESULT,
        )
        self.supervisor = module.LocalNativeSupervisor(
            repo_root=ROOT,
            issuer=issuer,
            policy_path=self.policy,
            target_module="native_fixture",
            target_file=self.support,
            entrypoint=self.entry,
        )

    def observe(self, *, run_id="run-baseline", nonce="nonce-baseline"):
        return self.supervisor.observe(
            candidate_commit=self.commit, run_id=run_id, nonce=nonce)

    def expectation_for(self, run_id, nonce):
        return self.module.TrustedExpectation(
            issuer=ISSUER,
            candidate_commit=self.commit,
            candidate_tree=self.tree,
            policy_sha256=digest(POLICY),
            run_id=run_id,
            nonce=nonce,
            entrypoint_sha256=digest(self.entry.read_bytes()),
            expected_imports={
                "native_fixture": digest(self.expected_support.encode()),
            },
            expected_events=EVENTS,
            expected_result=RESULT,
        )

    def verify(self, observation, expectation=None, ledger=None):
        return self.module.verify_observation(
            observation=observation,
            expectation=expectation or self.expectation,
            nonce_ledger=ledger or self.module.NonceLedger())


def fabricated_observation(module, fixture, marker: Path) -> dict:
    support = fixture.support
    return {
        "schema": module.OBSERVATION_SCHEMA,
        "issuer": ISSUER,
        "candidate_commit": fixture.commit,
        "candidate_tree": fixture.tree,
        "policy_sha256": digest(POLICY),
        "run_id": "run-baseline",
        "nonce": "nonce-baseline",
        "entrypoint": {"path": str(fixture.entry),
                       "sha256": digest(fixture.entry.read_bytes())},
        "target_file": {"path": str(support),
                        "sha256": digest(fixture.expected_support.encode())},
        "process": {
            "argv": ["/usr/local/bin/python3", "-I", "supervisor_wrapper.py"],
            "exit_code": 0,
            "stdout_sha256": "0" * 64,
            "stderr_sha256": "0" * 64,
            "timed_out": False,
        },
        "execution_status": "COMPLETED",
        "error": None,
        "result": RESULT,
        "events": [dict(row) for row in EVENTS],
        "imports": {
            "native_fixture": {
                "path": str(support.resolve()),
                "sha256": digest(fixture.expected_support.encode()),
                "within_target_dir": True,
            }
        },
        "import_events": ["native_fixture"],
        "observation_scope": "LOCAL_EXTERNAL_SUPERVISOR_CONTRACT",
        "candidate_receipt": {"status": "PASS", "marker_exists": marker.exists()},
    }


def run(module_path: Path) -> dict:
    module = load_module(module_path, f"r09v_probe_{abs(hash(str(module_path)))}")
    WORK.mkdir(parents=True, exist_ok=True)
    outcomes: dict[str, dict] = {}

    def record(name, required, decision, extra=None):
        got = decision.get("decision")
        outcomes[name] = {
            "required_decision": required,
            "observed_decision": got,
            "pass": got == required,
            "reasons": decision.get("reasons"),
            "extra": extra or {},
        }

    # 1. Genuine baseline positive through the actual module supervisor.
    fx = Fixture(module)
    obs = fx.observe()
    record("P0_genuine_baseline_accepted", module.ACCEPT, fx.verify(obs))

    # 2. Candidate-authored mapping accepted with no process ever launched.
    marker = Path(tempfile.mkdtemp(prefix="r09v-marker-", dir=WORK)) / "ran.txt"
    entry_with_marker = (
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('executed', encoding='utf-8')\n"
        "from native_fixture import add, double\n"
        "RESULT = {\"label\": \"baseline\", \"value\": double(add(20, 1))}\n"
    )
    fx2 = Fixture(module, entry_source=entry_with_marker)
    forged = fabricated_observation(module, fx2, marker)
    dec = fx2.verify(forged)
    record("P1_forged_observation_no_process", module.REFUSE, dec,
           {"marker_exists": marker.exists(),
            "note": "no LocalNativeSupervisor.observe call was made"})

    # 3. Fake issuer: genuine run labeled attacker, issuer rewritten post hoc.
    fx3 = Fixture(module, issuer="candidate-issued-supervisor")
    genuine_attacker = fx3.observe()
    genuine_attacker["issuer"] = ISSUER
    dec = fx3.verify(genuine_attacker, expectation=fx3.expectation_for(
        "run-baseline", "nonce-baseline"))
    record("P2_fake_issuer_rewritten_accepted", module.REFUSE, dec,
           {"original_issuer": "candidate-issued-supervisor"})

    # 4. Claimed commit/tree are unrelated to executed bytes.
    fx4 = Fixture(module)
    ev4 = fx4.observe()
    dec = fx4.verify(ev4)
    rel_support = os.path.relpath(fx4.support, ROOT)
    rel_entry = os.path.relpath(fx4.entry, ROOT)
    in_commit = {}
    for label, rel in (("support", rel_support), ("entry", rel_entry)):
        in_commit[label] = subprocess.run(
            ["git", "cat-file", "-e", f"{fx4.commit}:{rel}"], cwd=ROOT,
            capture_output=True).returncode == 0
    record("P3_claimed_tree_not_bound_to_executed_bytes", module.REFUSE, dec,
           {"executed_under_repo": False,
            "target_paths": [str(fx4.support), str(fx4.entry)],
            "path_present_in_claimed_commit": in_commit})

    # 5. Imported module self-restores to expected digest after execution.
    marker2 = Path(tempfile.mkdtemp(prefix="r09v-marker-", dir=WORK)) / "loaded.txt"
    mutated_support = (
        "import atexit\n"
        "from pathlib import Path\n"
        f"Path({str(marker2)!r}).write_text('mutated-native-loaded', encoding='utf-8')\n"
        f"_ORIGINAL = {SUPPORT!r}\n"
        "atexit.register(lambda: Path(__file__).write_text(_ORIGINAL, encoding='utf-8'))\n"
        "def add(a, b):\n"
        "    return a + b\n"
        "\n"
        "def double(value):\n"
        "    return value * 2\n"
    )
    fx5 = Fixture(module, support_source=mutated_support,
                  expected_support=SUPPORT)
    ev5 = fx5.observe()
    dec = fx5.verify(ev5)
    record("P4_loaded_bytes_differ_reported_digest", module.REFUSE, dec,
           {"marker_exists": marker2.exists(),
            "marker_text": marker2.read_text() if marker2.exists() else None,
            "post_run_file_digest_matches_expected": (
                digest(fx5.support.read_bytes()) == digest(SUPPORT.encode())),
            "reported_import_digest": ev5.get("imports", {}).get(
                "native_fixture", {}).get("sha256")})

    # 6. Default CLI accepts the same run twice in separate cold processes.
    fx6 = Fixture(module)
    ev6 = fx6.observe()
    obs_path = fx6.dir / "observation.json"
    exp_path = fx6.dir / "expectation.json"
    obs_path.write_text(json.dumps(ev6), encoding="utf-8")
    raw_exp = {
        "issuer": fx6.expectation.issuer,
        "candidate_commit": fx6.expectation.candidate_commit,
        "candidate_tree": fx6.expectation.candidate_tree,
        "policy_sha256": fx6.expectation.policy_sha256,
        "run_id": fx6.expectation.run_id,
        "nonce": fx6.expectation.nonce,
        "entrypoint_sha256": fx6.expectation.entrypoint_sha256,
        "expected_imports": dict(fx6.expectation.expected_imports),
        "expected_events": [dict(r) for r in fx6.expectation.expected_events],
        "expected_result": fx6.expectation.expected_result,
    }
    exp_path.write_text(json.dumps(raw_exp), encoding="utf-8")
    cli = ["/usr/local/bin/python3", str(module_path),
           "--observation", str(obs_path), "--expectation", str(exp_path)]
    first = subprocess.run(cli, capture_output=True, text=True)
    second = subprocess.run(cli, capture_output=True, text=True)
    record("P5_default_cli_replay_accepted", module.REFUSE,
           {"decision": module.ACCEPT if (
               first.returncode == 0 and second.returncode == 0)
            else module.REFUSE},
        {"first_exit": first.returncode, "second_exit": second.returncode,
         "first_decision": json.loads(first.stdout).get("decision")
         if first.stdout else None,
         "second_decision": json.loads(second.stdout).get("decision")
         if second.stdout else None,
         "nonce_ledger_configured": False})

    # 7. Two cold ledger instances constructed before either consumes.
    fx7 = Fixture(module)
    ev7 = fx7.observe()
    ledger_path = fx7.dir / "nonce-ledger.jsonl"
    ledger_a = module.NonceLedger(ledger_path)
    ledger_b = module.NonceLedger(ledger_path)
    dec_a = fx7.verify(ev7, ledger=ledger_a)
    dec_b = fx7.verify(ev7, ledger=ledger_b)
    record("P6_concurrent_preconstructed_ledger_replay", module.REFUSE,
           {"decision": module.ACCEPT if (
               dec_a["decision"] == module.ACCEPT
               and dec_b["decision"] == module.ACCEPT) else module.REFUSE},
           {"first": dec_a["decision"], "second": dec_b["decision"],
            "second_reasons": dec_b["reasons"]})

    # 8. Untrusted subject overwrites the supervisor observation after capture.
    marker3 = Path(tempfile.mkdtemp(prefix="r09v-marker-", dir=WORK)) / "forge.json"
    malicious_support = (
        "import atexit\n"
        "import json\n"
        "import sys\n"
        "from pathlib import Path\n"
        f"_MARKER = {str(marker3)!r}\n"
        f"_ORIGINAL = {SUPPORT!r}\n"
        "def _forge():\n"
        "    observation_path = Path(json.loads(open(sys.argv[1], encoding='utf-8').read())['observation_path'])\n"
        "    before = json.loads(observation_path.read_text(encoding='utf-8'))\n"
        "    Path(_MARKER).write_text(json.dumps({'pre_forge_result': before.get('result'), 'pre_forge_status': before.get('execution_status')}), encoding='utf-8')\n"
        "    before['result'] = {'label': 'baseline', 'value': 42}\n"
        "    observation_path.write_text(json.dumps(before), encoding='utf-8')\n"
        "    Path(__file__).write_text(_ORIGINAL, encoding='utf-8')\n"
        "atexit.register(_forge)\n"
        "def add(a, b):\n"
        "    return a + b\n"
        "\n"
        "def double(value):\n"
        "    return value * 2 - 1\n"
    )
    fx9 = Fixture(module, support_source=malicious_support,
                  expected_support=SUPPORT)
    ev9 = fx9.observe()
    dec9 = fx9.verify(ev9)
    record("P8_subject_overwrites_observation", module.REFUSE, dec9,
           {"marker": json.loads(marker3.read_text()) if marker3.exists() else None,
            "reported_result": ev9.get("result"),
            "post_run_file_restored_to_expected": (
                digest(fx9.support.read_bytes()) == digest(SUPPORT.encode()))})

    # 9. Wrong result is refused by the intact candidate (mutation target).
    wrong_entry = (
        "from native_fixture import add, double\n"
        "\n"
        "RESULT = {\"label\": \"baseline\", \"value\": double(add(20, 1)) - 1}\n"
    )
    fx8 = Fixture(module, entry_source=wrong_entry)
    dec8 = fx8.verify(fx8.observe())
    record("P7_wrong_result_refused_baseline", module.REFUSE, dec8,
           {"has_result_mismatch": "RESULT_MISMATCH" in dec8["reasons"]})

    return outcomes


def run_mutant(mutant_path: Path) -> dict:
    module = load_module(mutant_path, "r09v_probe_mutant")
    WORK.mkdir(parents=True, exist_ok=True)
    wrong_entry = (
        "from native_fixture import add, double\n"
        "\n"
        "RESULT = {\"label\": \"baseline\", \"value\": double(add(20, 1)) - 1}\n"
    )
    fx = Fixture(module, entry_source=wrong_entry)
    dec = fx.verify(fx.observe())
    return {"mutant_decision": dec["decision"], "reasons": dec["reasons"],
            "wrong_result_expected": module.REFUSE}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", default=str(CANDIDATE_MODULE))
    parser.add_argument("--mutant", default=None)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    if args.mutant:
        payload = {"mutant": args.mutant, "result": run_mutant(Path(args.mutant))}
    else:
        payload = {"module": args.module, "result": run(Path(args.module))}
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    failed = [name for name, row in payload.get("result", {}).items()
              if isinstance(row, dict) and row.get("pass") is False]
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
