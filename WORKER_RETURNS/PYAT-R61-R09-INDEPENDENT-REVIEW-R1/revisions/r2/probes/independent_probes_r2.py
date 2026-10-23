#!/usr/bin/env python3
"""R61-R09V R2 independent hostile probes for the whole capture boundary.

Reviewer-owned probes only. Fixtures are disposable and live beneath this
returnroot. The candidate verifier is imported read-only; it is never edited.
"""
from __future__ import annotations

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
R2ROOT = HERE.parent
ROOT = HERE.parents[4] if len(HERE.parents) > 4 else HERE
for candidate in (HERE, *HERE.parents):
    if (candidate / "CROSS_HQ_CONTROL_ROOM" / "universal_runner_verify.py").is_file():
        ROOT = candidate
        break
MODULE_PATH = ROOT / "CROSS_HQ_CONTROL_ROOM" / "universal_runner_verify.py"
SPEC = importlib.util.spec_from_file_location("r09v_r2_verify", MODULE_PATH)
verify = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = verify
SPEC.loader.exec_module(verify)

WORK = R2ROOT / "probes" / "work"
WORK.mkdir(parents=True, exist_ok=True)
ISSUER = "trusted-supervisor-A"
POLICY = b'{"policy":"R09_R2_REVIEW_POLICY","revision":2}\n'
EXPECTED_RESULT = {"label": "baseline", "value": 42}
EXPECTED_EVENTS = (
    {"module": "native_fixture", "qualname": "add", "status": "RETURNED"},
    {"module": "native_fixture", "qualname": "double", "status": "RETURNED"},
)
SUPPORT = "def add(a, b):\n    return a + b\n\ndef double(value):\n    return value * 2\n"
ENTRY = (
    "from native_fixture import add, double\n"
    "RESULT = {\"label\": \"baseline\", \"value\": double(add(20, 1))}\n"
)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def git_blob(repo: Path, commit: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{relative}"], cwd=repo)


class Fixture:
    def __init__(self, name: str, *, support: str = SUPPORT,
                 entry: str | None = None):
        self.base = Path(tempfile.mkdtemp(prefix=f"r2probe-{name}-", dir=WORK))
        self.repo = self.base / "candidate"
        self.repo.mkdir()
        self.support = self.repo / "native_fixture.py"
        self.entry = self.repo / "native_entry.py"
        self.policy = self.base / "protected_policy.json"
        self.support.write_text(support, encoding="utf-8")
        self.entry.write_text(entry if entry is not None else ENTRY,
                              encoding="utf-8")
        self.policy.write_bytes(POLICY)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "r09v@example.invalid")
        git(self.repo, "config", "user.name", "R09V Reviewer")
        git(self.repo, "add", "native_fixture.py", "native_entry.py")
        git(self.repo, "commit", "-q", "-m", "fixture")
        self.commit = git(self.repo, "rev-parse", "HEAD")
        self.tree = git(self.repo, "rev-parse", f"{self.commit}^{{tree}}")
        self.trust_root = verify.TrustRoot(ISSUER)
        self.supervisor = verify.LocalNativeSupervisor(
            repo_root=self.repo, policy_path=self.policy,
            target_module="native_fixture", target_file=self.support,
            entrypoint=self.entry, trust_root=self.trust_root)
        self.expectation = verify.TrustedExpectation(
            issuer=ISSUER, candidate_commit=self.commit,
            candidate_tree=self.tree, policy_sha256=sha_bytes(POLICY),
            run_id=f"run-{name}", nonce=f"nonce-{name}",
            entrypoint_sha256=sha_bytes(git_blob(
                self.repo, self.commit, "native_entry.py")),
            expected_imports={"native_fixture": sha_bytes(git_blob(
                self.repo, self.commit, "native_fixture.py"))},
            expected_events=EXPECTED_EVENTS, expected_result=EXPECTED_RESULT,
            trust_root_fingerprint=self.trust_root.fingerprint)

    def observe(self):
        return self.supervisor.observe(
            candidate_commit=self.commit, run_id=self.expectation.run_id,
            nonce=self.expectation.nonce)

    def decision(self, observation, expectation=None, ledger=None,
                 trust_root=None):
        return verify.verify_observation(
            observation=observation,
            expectation=expectation or self.expectation,
            nonce_ledger=ledger or verify.NonceLedger(
                self.base / "ledger.jsonl"),
            trust_root=trust_root or self.trust_root)

    def cleanup(self):
        shutil.rmtree(self.base, ignore_errors=True)


def record(out: dict, name: str, *, required: str, observed: str,
           pass_value: bool, extra=None):
    out[name] = {
        "required": required,
        "observed": observed,
        "pass": bool(pass_value),
        "extra": extra or {},
    }


def require(out: dict, name: str, decision: dict, required: str,
            reason: str | None = None, extra=None):
    observed = decision.get("decision")
    ok = observed == required
    if reason is not None:
        ok = ok and reason in decision.get("reasons", [])
    record(out, name, required=required, observed=observed, pass_value=ok,
           extra={"reasons": decision.get("reasons"), **(extra or {})})
    return ok


def probe_legit(out: dict) -> Fixture | None:
    fx = Fixture("legit")
    obs = fx.observe()
    dec = fx.decision(obs)
    require(out, "P0_legit_baseline", dec, verify.ACCEPT,
            extra={"result": dec.get("observed", {}).get("result")})
    return fx


def probe_json_dump_forgery(out: dict):
    marker = WORK / "json_dump_actual.txt"
    marker.unlink(missing_ok=True)
    support = (
        "import json\n"
        "_real_dump = json.dump\n"
        "def _forged_dump(obj, handle, **kwargs):\n"
        "    forged = dict(obj)\n"
        "    forged['result'] = {'label': 'baseline', 'value': 42}\n"
        "    _real_dump(forged, handle, **kwargs)\n"
        "json.dump = _forged_dump\n"
        "def add(a, b):\n"
        "    return a + b\n"
        "def double(value):\n"
        "    return value * 2 - 1\n"
    )
    entry = (
        "from native_fixture import add, double\n"
        "from pathlib import Path\n"
        f"marker = Path({str(marker)!r})\n"
        "_actual = double(add(20, 1))\n"
        "marker.write_text(str(_actual), encoding='utf-8')\n"
        "RESULT = {'label': 'baseline', 'value': _actual}\n"
    )
    fx = Fixture("json-dump", support=support, entry=entry)
    obs = fx.observe()
    dec = fx.decision(obs)
    actual = marker.read_text(encoding="utf-8") if marker.exists() else None
    # A genuine independent capture must refuse because the actual returned
    # value was 41 while the sealed observation claims 42.
    require(out, "P1_child_json_dump_forges_result", dec, verify.REFUSE,
            extra={"actual_returned_value": actual,
                   "sealed_result": obs.get("result"),
                   "marker_exists": marker.exists()})
    fx.cleanup()


def probe_loaded_bytes_forgery(out: dict):
    marker = WORK / "loaded_bytes_actual.txt"
    marker.unlink(missing_ok=True)
    benign_digest = sha_bytes(SUPPORT.encode("utf-8"))
    # Entry source is generated after the fixture target path is known; use a
    # placeholder and rewrite the committed file before the commit.
    base = Path(tempfile.mkdtemp(prefix="r2probe-loaded-", dir=WORK))
    repo = base / "candidate"
    repo.mkdir()
    support = repo / "native_fixture.py"
    entry = repo / "native_entry.py"
    policy = base / "policy.json"
    support.write_text(SUPPORT, encoding="utf-8")
    policy.write_bytes(POLICY)
    target = str(support.resolve())
    entry_source = (
        "import importlib.abc\n"
        "import importlib.util\n"
        "import sys\n"
        "from pathlib import Path\n"
        f"TARGET = {target!r}\n"
        f"MARKER = {str(marker)!r}\n"
        "MALICIOUS = 'def add(a, b):\\n    return a + b\\n\\ndef double(value):\\n    return value * 2 - 1\\n'\n"
        "class _Loader(importlib.abc.Loader):\n"
        "    def create_module(self, spec):\n"
        "        return None\n"
        "    def exec_module(self, module):\n"
        "        exec(compile(MALICIOUS, TARGET, 'exec'), module.__dict__)\n"
        "class _Finder(importlib.abc.MetaPathFinder):\n"
        "    def find_spec(self, fullname, path=None, target=None):\n"
        "        if fullname == 'native_fixture':\n"
        "            return importlib.util.spec_from_loader(fullname, _Loader())\n"
        "        return None\n"
        "sys.meta_path.insert(0, _Finder())\n"
        "import native_fixture\n"
        "frame = sys._getframe()\n"
        "while frame is not None:\n"
        "    if 'loaded_sources' in frame.f_locals:\n"
        "        frame.f_locals['loaded_sources']['native_fixture'] = {\n"
        f"            'path': TARGET, 'loaded_sha256': {benign_digest!r}}}\n"
        "        break\n"
        "    frame = frame.f_back\n"
        "_actual = native_fixture.double(native_fixture.add(20, 1))\n"
        "Path(MARKER).write_text(str(_actual), encoding='utf-8')\n"
        "RESULT = {'label': 'baseline', 'value': 42}\n"
    )
    entry.write_text(entry_source, encoding="utf-8")
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "r09v@example.invalid")
    git(repo, "config", "user.name", "R09V Reviewer")
    git(repo, "add", "native_fixture.py", "native_entry.py")
    git(repo, "commit", "-q", "-m", "loaded-bytes-fixture")
    commit = git(repo, "rev-parse", "HEAD")
    tree = git(repo, "rev-parse", f"{commit}^{{tree}}")
    trust_root = verify.TrustRoot(ISSUER)
    supervisor = verify.LocalNativeSupervisor(
        repo_root=repo, policy_path=policy, target_module="native_fixture",
        target_file=support, entrypoint=entry, trust_root=trust_root)
    expectation = verify.TrustedExpectation(
        issuer=ISSUER, candidate_commit=commit, candidate_tree=tree,
        policy_sha256=sha_bytes(POLICY), run_id="run-loaded",
        nonce="nonce-loaded",
        entrypoint_sha256=sha_bytes(git_blob(repo, commit, "native_entry.py")),
        expected_imports={"native_fixture": benign_digest},
        expected_events=EXPECTED_EVENTS, expected_result=EXPECTED_RESULT,
        trust_root_fingerprint=trust_root.fingerprint)
    obs = supervisor.observe(candidate_commit=commit, run_id="run-loaded",
                             nonce="nonce-loaded")
    dec = verify.verify_observation(
        observation=obs, expectation=expectation,
        nonce_ledger=verify.NonceLedger(base / "ledger.jsonl"),
        trust_root=trust_root)
    actual = marker.read_text(encoding="utf-8") if marker.exists() else None
    require(out, "P2_child_forges_loaded_bytes_and_result", dec, verify.REFUSE,
            extra={
                "actual_returned_value": actual,
                "sealed_result": obs.get("result"),
                "reported_import": (obs.get("imports") or {}).get("native_fixture"),
                "tree_digest": sha_bytes(git_blob(repo, commit, "native_fixture.py")),
                "marker_exists": marker.exists(),
            })
    shutil.rmtree(base, ignore_errors=True)


def probe_bare_mapping_and_fake_issuer(out: dict):
    fx = Fixture("bare")
    obs = fx.observe()
    dec = fx.decision(dict(obs))
    require(out, "P3_bare_mapping", dec, verify.REFUSE, "UNTRUSTED_OBSERVATION")
    obs["issuer"] = "attacker"
    dec = fx.decision(obs)
    require(out, "P4_fake_issuer_rewrite", dec, verify.REFUSE,
            "OBSERVATION_AUTHENTICATION_FAILED")
    fx.cleanup()


def probe_self_root(out: dict):
    fx = Fixture("selfroot")
    attacker = verify.TrustRoot(ISSUER)
    supervisor = verify.LocalNativeSupervisor(
        repo_root=fx.repo, policy_path=fx.policy,
        target_module="native_fixture", target_file=fx.support,
        entrypoint=fx.entry, trust_root=attacker)
    expectation = verify.TrustedExpectation(
        issuer=ISSUER, candidate_commit=fx.commit, candidate_tree=fx.tree,
        policy_sha256=sha_bytes(POLICY), run_id="run-selfroot",
        nonce="nonce-selfroot",
        entrypoint_sha256=sha_bytes(git_blob(
            fx.repo, fx.commit, "native_entry.py")),
        expected_imports={"native_fixture": sha_bytes(git_blob(
            fx.repo, fx.commit, "native_fixture.py"))},
        expected_events=EXPECTED_EVENTS, expected_result=EXPECTED_RESULT,
        trust_root_fingerprint=attacker.fingerprint)
    obs = supervisor.observe(candidate_commit=fx.commit, run_id="run-selfroot",
                             nonce="nonce-selfroot")
    dec = verify.verify_observation(
        observation=obs, expectation=expectation,
        nonce_ledger=verify.NonceLedger(fx.base / "ledger.jsonl"),
        trust_root=attacker)
    # This is a caller-supplied self-root, not a subject-channel forgery. It is
    # recorded as a boundary finding: the verifier has no external anchor for
    # which trust root is admissible.
    record(out, "P5_self_root_caller_accepted", required="BOUNDARY_DISCLOSED",
           observed=dec.get("decision"),
           pass_value=dec.get("decision") == verify.ACCEPT,
           extra={"reasons": dec.get("reasons"),
                  "fingerprint": attacker.fingerprint})
    fx.cleanup()


def probe_ledger(out: dict):
    fx = Fixture("ledger")
    obs = fx.observe()
    dec = fx.decision(obs, ledger=verify.NonceLedger())
    require(out, "P6_nondurable_ledger", dec, verify.REFUSE,
            "NONCE_LEDGER_NOT_DURABLE")

    path = fx.base / "cold.jsonl"
    first = fx.decision(obs, ledger=verify.NonceLedger(path))
    second = fx.decision(obs, ledger=verify.NonceLedger(path))
    require(out, "P7_cold_replay_first", first, verify.ACCEPT)
    require(out, "P8_cold_replay_second", second, verify.REFUSE, "NONCE_REPLAYED")

    code = (
        "import importlib.util, sys\n"
        "spec = importlib.util.spec_from_file_location('r09v', sys.argv[1])\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "sys.modules['r09v'] = module\n"
        "spec.loader.exec_module(module)\n"
        "print(module.NonceLedger(sys.argv[2]).claim('issuer', 'run', 'nonce'))\n"
    )
    atomic = fx.base / "atomic.jsonl"
    procs = [subprocess.Popen(
        ["/usr/local/bin/python3", "-c", code, str(MODULE_PATH), str(atomic)],
        stdout=subprocess.PIPE, text=True) for _ in range(2)]
    outcomes = sorted(p.communicate(timeout=60)[0].strip() for p in procs)
    record(out, "P9_concurrent_nonce", required="['CLAIMED', 'REPLAYED']",
           observed=str(outcomes),
           pass_value=outcomes == ["CLAIMED", "REPLAYED"],
           extra={"outcomes": outcomes})
    fx.cleanup()


def probe_malformed(out: dict):
    fx = Fixture("malformed")
    obs = fx.observe()
    bad_expectation = verify.TrustedExpectation(
        issuer=fx.expectation.issuer,
        candidate_commit=fx.expectation.candidate_commit,
        candidate_tree=fx.expectation.candidate_tree,
        policy_sha256=fx.expectation.policy_sha256,
        run_id=fx.expectation.run_id, nonce=fx.expectation.nonce,
        entrypoint_sha256=fx.expectation.entrypoint_sha256,
        expected_imports=fx.expectation.expected_imports,
        expected_events=fx.expectation.expected_events,
        expected_result={"x": {1, 2}},
        trust_root_fingerprint=fx.expectation.trust_root_fingerprint)
    try:
        dec = fx.decision(obs, expectation=bad_expectation)
        require(out, "P10_non_serializable_expectation", dec, verify.REFUSE,
                "EXPECTATION_RESULT_NOT_SERIALIZABLE")
    except Exception as exc:
        record(out, "P10_non_serializable_expectation",
               required=verify.REFUSE,
               observed=f"EXCEPTION:{type(exc).__name__}",
               pass_value=False,
               extra={"detail": str(exc)[:300]})
    obs["result"] = {"x": {1, 2}}
    try:
        dec = fx.decision(obs)
        require(out, "P11_non_serializable_observation", dec, verify.REFUSE,
                "OBSERVATION_AUTHENTICATION_FAILED")
    except Exception as exc:
        record(out, "P11_non_serializable_observation",
               required=verify.REFUSE,
               observed=f"EXCEPTION:{type(exc).__name__}",
               pass_value=False,
               extra={"detail": str(exc)[:300]})
    fx.cleanup()


def probe_out_of_tree(out: dict):
    base = Path(tempfile.mkdtemp(prefix="r2probe-outside-", dir=WORK))
    repo = base / "candidate"
    repo.mkdir()
    outside = base / "outside"
    outside.mkdir()
    support = outside / "native_fixture.py"
    entry = outside / "native_entry.py"
    support.write_text(SUPPORT, encoding="utf-8")
    entry.write_text(ENTRY, encoding="utf-8")
    policy = base / "policy.json"
    policy.write_bytes(POLICY)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "r09v@example.invalid")
    git(repo, "config", "user.name", "R09V Reviewer")
    git(repo, "commit", "-q", "--allow-empty", "-m", "empty")
    commit = git(repo, "rev-parse", "HEAD")
    trust_root = verify.TrustRoot(ISSUER)
    supervisor = verify.LocalNativeSupervisor(
        repo_root=repo, policy_path=policy, target_module="native_fixture",
        target_file=support, entrypoint=entry, trust_root=trust_root)
    obs = supervisor.observe(candidate_commit=commit, run_id="run-outside",
                             nonce="nonce-outside")
    dec = verify.verify_observation(
        observation=obs, expectation=verify.TrustedExpectation(
            issuer=ISSUER, candidate_commit=commit,
            candidate_tree=git(repo, "rev-parse", f"{commit}^{{tree}}"),
            policy_sha256=sha_bytes(POLICY), run_id="run-outside",
            nonce="nonce-outside",
            entrypoint_sha256=sha_bytes(entry.read_bytes()),
            expected_imports={"native_fixture": sha_bytes(support.read_bytes())},
            expected_events=EXPECTED_EVENTS, expected_result=EXPECTED_RESULT,
            trust_root_fingerprint=trust_root.fingerprint),
        nonce_ledger=verify.NonceLedger(base / "ledger.jsonl"),
        trust_root=trust_root)
    require(out, "P12_out_of_tree", dec, verify.REFUSE,
            "SUPERVISOR_REFUSED:ENTRYPOINT_OUTSIDE_CANDIDATE_TREE")
    shutil.rmtree(base, ignore_errors=True)


def probe_c11(out: dict):
    entry = ROOT / "tests" / "universal_runner" / "native_c11_entry.py"
    case = ROOT / "tests" / "universal_runner" / "native_c11_case.py"
    base = Path(tempfile.mkdtemp(prefix="r2probe-c11-", dir=WORK))
    policy = base / "policy.json"
    policy.write_bytes(POLICY)
    commit = git(ROOT, "rev-parse", "HEAD")
    tree = git(ROOT, "rev-parse", f"{commit}^{{tree}}")
    # Independent reference: plain process, actual C11 owners, no runner.
    code = (
        "import json, sys\n"
        f"sys.path.insert(0, {str(ROOT)!r})\n"
        f"sys.path.insert(0, {str(entry.parent)!r})\n"
        "import native_c11_entry\n"
        "print(json.dumps(native_c11_entry.RESULT, sort_keys=True))\n"
    )
    completed = subprocess.run(
        ["/usr/local/bin/python3", "-I", "-c", code], cwd=str(ROOT),
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    independent = json.loads(completed.stdout) if completed.returncode == 0 else None
    trust_root = verify.TrustRoot(ISSUER)
    supervisor = verify.LocalNativeSupervisor(
        repo_root=ROOT, policy_path=policy, target_module="native_c11_entry",
        target_file=entry, entrypoint=entry, trust_root=trust_root)
    expectation = verify.TrustedExpectation(
        issuer=ISSUER, candidate_commit=commit, candidate_tree=tree,
        policy_sha256=sha_bytes(POLICY), run_id="run-c11", nonce="nonce-c11",
        entrypoint_sha256=sha_bytes(git_blob(
            ROOT, commit, "tests/universal_runner/native_c11_entry.py")),
        expected_imports={
            "native_c11_case": sha_bytes(git_blob(
                ROOT, commit, "tests/universal_runner/native_c11_case.py")),
            "rawlsing_next.pre553_c11_ingest": sha_bytes(git_blob(
                ROOT, commit, "rawlsing_next/pre553_c11_ingest.py")),
            "rawlsing_next.pre553_c11_repository": sha_bytes(git_blob(
                ROOT, commit, "rawlsing_next/pre553_c11_repository.py")),
        },
        expected_events=(
            {"module": "native_c11_entry", "qualname": "run_native",
             "status": "RETURNED"},
        ),
        expected_result=independent,
        trust_root_fingerprint=trust_root.fingerprint)
    obs = supervisor.observe(candidate_commit=commit, run_id="run-c11",
                             nonce="nonce-c11")
    dec = verify.verify_observation(
        observation=obs, expectation=expectation,
        nonce_ledger=verify.NonceLedger(base / "ledger.jsonl"),
        trust_root=trust_root)
    require(out, "P13_actual_c11_positive", dec, verify.ACCEPT,
            extra={"independent_reference": independent,
                   "sealed_result": obs.get("result"),
                   "imports": sorted((obs.get("imports") or {}).keys())})
    # Same C11 run, wrong externally frozen expectation must refuse.
    wrong = verify.TrustedExpectation(
        **{**expectation.__dict__, "expected_result": {
            "accepted": False, "disposition": "WRONG"}})
    dec = verify.verify_observation(
        observation=obs, expectation=wrong,
        nonce_ledger=verify.NonceLedger(base / "ledger2.jsonl"),
        trust_root=trust_root)
    require(out, "P14_c11_wrong_expectation", dec, verify.REFUSE,
            "RESULT_MISMATCH")
    shutil.rmtree(base, ignore_errors=True)


def main() -> int:
    out: dict = {}
    probes = [
        ("legit", lambda: probe_legit(out) and None),
        ("bare", lambda: probe_bare_mapping_and_fake_issuer(out)),
        ("json_dump", lambda: probe_json_dump_forgery(out)),
        ("loaded_bytes", lambda: probe_loaded_bytes_forgery(out)),
        ("self_root", lambda: probe_self_root(out)),
        ("ledger", lambda: probe_ledger(out)),
        ("malformed", lambda: probe_malformed(out)),
        ("out_of_tree", lambda: probe_out_of_tree(out)),
        ("c11", lambda: probe_c11(out)),
    ]
    for probe_name, probe_fn in probes:
        try:
            probe_fn()
        except Exception as exc:
            record(out, f"PROBE_CRASH:{probe_name}", required="completed",
                   observed=f"EXCEPTION:{type(exc).__name__}",
                   pass_value=False, extra={"detail": str(exc)[:300]})
    # probe_legit cleans itself via the lambda above; ensure no fixture leak.
    for child in WORK.iterdir():
        if child.is_dir() and child.name.startswith("r2probe-"):
            shutil.rmtree(child, ignore_errors=True)
    out["_summary"] = {
        "probes": len([k for k in out if not k.startswith("_")]),
        "passed": sum(1 for k, v in out.items()
                      if not k.startswith("_") and v.get("pass")),
        "failed": sorted(k for k, v in out.items()
                         if not k.startswith("_") and not v.get("pass")),
        "module": str(MODULE_PATH),
        "module_sha256": sha_bytes(MODULE_PATH.read_bytes()),
        "head": git(ROOT, "rev-parse", "HEAD"),
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if not out["_summary"]["failed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
