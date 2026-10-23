#!/usr/bin/env python3
"""R09 local native runner verification with an external supervisor boundary.

Accepted observations must come from a supervisor that the caller controls and
that actually launched the process and captured imports, events and the result.
Candidate-authored booleans, traces, receipts or self-pins are never evidence.
This module banks a local TEST_ONLY capability. It does not install or attest a
protected CI required check and it does not authorize generic promotion.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
from typing import Any, Mapping

CONTRACT_ID = "R61-R09-NATIVE-RUNNER-VERIFY@1"
OBSERVATION_SCHEMA = "R61_R09_SUPERVISOR_OBSERVATION@1"
DECISION_SCHEMA = "R61_R09_NATIVE_VERIFICATION_DECISION@1"
ACCEPT = "LOCAL_NATIVE_VERIFIED"
REFUSE = "REFUSE_NATIVE_QUALIFICATION"
CEILING = "LOCAL_NATIVE_TEST_ONLY"
PROMOTION = "DEPLOYMENT_HOLD"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

TRUSTED_RUNTIME_EXCLUSIONS = (
    "PROTECTED_CI_REQUIRED_CHECK_NOT_INSTALLED",
    "REPOSITORY_ADMIN_ATTESTATION_NOT_PERFORMED",
    "PRODUCTION_KEYS_OR_SECRETS_NOT_USED",
    "ORIGINAL_SURVEY_DATA_NOT_READ",
    "SCIENTIFIC_ORIGINAL_GRADE_NOT_ISSUED",
    "LOCAL_SUBPROCESS_NOT_A_HOSTILE_CODE_SANDBOX",
    "AUTHOR_VALIDATION_IS_NOT_INDEPENDENT_REVIEW",
)


class SupervisorError(ValueError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def typed_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: str | os.PathLike[str]) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class TrustedExpectation:
    issuer: str
    candidate_commit: str
    candidate_tree: str
    policy_sha256: str
    run_id: str
    nonce: str
    entrypoint_sha256: str
    expected_imports: Mapping[str, str]
    expected_events: tuple[Mapping[str, Any], ...]
    expected_result: Any


class NonceLedger:
    """Externally supplied one-shot nonce ledger, optionally file-backed."""

    def __init__(self, path: str | os.PathLike[str] | None = None):
        self._lock = threading.Lock()
        self._path = Path(path) if path is not None else None
        self._seen: set[str] = set()
        if self._path is not None and self._path.exists():
            for line in self._path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    self._seen.add(line.strip())

    def consume(self, issuer: str, run_id: str, nonce: str) -> bool:
        key = typed_digest([issuer, run_id, nonce])
        with self._lock:
            if key in self._seen:
                return False
            self._seen.add(key)
            if self._path is not None:
                self._path.parent.mkdir(parents=True, exist_ok=True)
                descriptor = os.open(self._path,
                                     os.O_APPEND | os.O_CREAT | os.O_WRONLY,
                                     0o600)
                try:
                    os.write(descriptor, (key + "\n").encode("ascii"))
                    os.fsync(descriptor)
                finally:
                    os.close(descriptor)
        return True


WRAPPER_SOURCE = r'''
import hashlib
import json
import os
import runpy
import sys

config = json.loads(open(sys.argv[1], encoding="utf-8").read())
target_dir = os.path.abspath(config["target_dir"])
target_file = os.path.abspath(config["target_file"])
target_module = config["target_module"]
entrypoint = os.path.abspath(config["entrypoint"])
observation_path = config["observation_path"]

import_events = []


def audit(event, args):
    if event == "import":
        import_events.append(str(args[0]))


sys.addaudithook(audit)
sys.path.insert(0, target_dir)
events = []
pending = {}


def tracer(frame, event, arg):
    if os.path.abspath(frame.f_code.co_filename) != target_file:
        return None
    if event == "call":
        if frame.f_code.co_qualname == "<module>":
            return tracer
        pending[id(frame)] = {
            "module": target_module,
            "qualname": frame.f_code.co_qualname,
            "raised": False,
        }
    elif event == "exception":
        if id(frame) in pending:
            pending[id(frame)]["raised"] = True
    elif event == "return":
        record = pending.pop(id(frame), None)
        if record is not None:
            events.append({
                "module": record["module"],
                "qualname": record["qualname"],
                "status": "RAISED" if record["raised"] else "RETURNED",
            })
    return tracer


execution_status = "COMPLETED"
error = None
result = None
sys.settrace(tracer)
try:
    namespace = runpy.run_path(entrypoint, run_name="__main__")
    if "RESULT" in namespace:
        result = namespace["RESULT"]
    else:
        execution_status = "NO_RESULT"
except BaseException as exc:
    execution_status = "ERROR"
    error = {"type": type(exc).__name__, "message": str(exc)[:1000]}
finally:
    sys.settrace(None)

imports = {}
for name, module in list(sys.modules.items()):
    if name == "__main__":
        continue
    filename = getattr(module, "__file__", None)
    if not filename:
        continue
    path = os.path.abspath(filename)
    if path.startswith(target_dir + os.sep):
        imports[name] = path

payload = {
    "execution_status": execution_status,
    "error": error,
    "result": result,
    "events": events,
    "imports": imports,
    "import_events": list(dict.fromkeys(import_events)),
}
with open(observation_path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, sort_keys=True)
'''


def _git_tree(repo: Path, commit: str) -> str:
    completed = subprocess.run(
        ["git", "-c", "gc.auto=0", "rev-parse", f"{commit}^{{tree}}"],
        cwd=str(repo), text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=30, check=False,
    )
    if completed.returncode != 0:
        raise SupervisorError("CANDIDATE_TREE_UNRESOLVED")
    tree = completed.stdout.strip()
    if not HEX40.fullmatch(tree):
        raise SupervisorError("CANDIDATE_TREE_INVALID")
    return tree


class LocalNativeSupervisor:
    """Local demonstration of the externally supplied supervisor boundary.

    The object launches a fresh interpreter, traces actual calls in the pinned
    target module, records actual import names, and re-hashes imported files
    outside the child process. It is not a hostile-code sandbox and does not
    provide CI attestation.
    """

    def __init__(self, *, repo_root: str | os.PathLike[str], issuer: str,
                 policy_path: str | os.PathLike[str], target_module: str,
                 target_file: str | os.PathLike[str],
                 entrypoint: str | os.PathLike[str],
                 python: str | None = None, timeout: int = 60):
        self.repo_root = Path(repo_root).resolve()
        self.issuer = str(issuer)
        self.policy_path = Path(policy_path).resolve()
        self.target_module = str(target_module)
        self.target_file = Path(target_file).resolve()
        self.entrypoint = Path(entrypoint).resolve()
        self.python = python or sys.executable
        self.timeout = int(timeout)
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", self.target_module):
            raise SupervisorError("TARGET_MODULE_INVALID")
        for path in (self.policy_path, self.target_file, self.entrypoint):
            if not path.is_file():
                raise SupervisorError(f"TRUSTED_INPUT_MISSING:{path}")

    def observe(self, *, candidate_commit: str, run_id: str,
                nonce: str) -> dict[str, Any]:
        if not HEX40.fullmatch(candidate_commit):
            raise SupervisorError("CANDIDATE_COMMIT_INVALID")
        candidate_tree = _git_tree(self.repo_root, candidate_commit)
        policy_sha256 = sha256_file(self.policy_path)
        entrypoint_sha256 = sha256_file(self.entrypoint)
        with tempfile.TemporaryDirectory(prefix="r09-native-") as directory:
            work = Path(directory)
            wrapper = work / "supervisor_wrapper.py"
            config_path = work / "config.json"
            output_path = work / "observation.json"
            wrapper.write_text(WRAPPER_SOURCE, encoding="utf-8")
            config_path.write_text(canonical_json({
                "target_dir": str(self.target_file.parent),
                "target_file": str(self.target_file),
                "target_module": self.target_module,
                "entrypoint": str(self.entrypoint),
                "observation_path": str(output_path),
            }), encoding="utf-8")
            environment = {
                "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                "LANG": "C.UTF-8",
                "PYTHONDONTWRITEBYTECODE": "1",
            }
            completed = subprocess.run(
                [self.python, "-I", str(wrapper), str(config_path)],
                cwd=str(work), env=environment, text=True, timeout=self.timeout,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            child: dict[str, Any] = {}
            if output_path.is_file():
                try:
                    child = json.loads(output_path.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    child = {}
            raw_imports = child.get("imports")
            imports: dict[str, Any] = {}
            if isinstance(raw_imports, Mapping):
                for name, path in raw_imports.items():
                    if not isinstance(name, str) or not isinstance(path, str):
                        continue
                    resolved = Path(path).resolve()
                    within = resolved.is_relative_to(
                        self.target_file.parent)
                    digest = None
                    if resolved.is_file():
                        try:
                            digest = sha256_file(resolved)
                        except OSError:
                            digest = None
                    imports[name] = {
                        "path": str(resolved),
                        "sha256": digest,
                        "within_target_dir": within,
                    }
            return {
                "schema": OBSERVATION_SCHEMA,
                "issuer": self.issuer,
                "candidate_commit": candidate_commit,
                "candidate_tree": candidate_tree,
                "policy_sha256": policy_sha256,
                "run_id": run_id,
                "nonce": nonce,
                "entrypoint": {
                    "path": str(self.entrypoint),
                    "sha256": entrypoint_sha256,
                },
                "target_file": {
                    "path": str(self.target_file),
                    "sha256": sha256_file(self.target_file),
                },
                "process": {
                    "argv": [self.python, "-I", "supervisor_wrapper.py"],
                    "exit_code": completed.returncode,
                    "stdout_sha256": hashlib.sha256(
                        completed.stdout.encode("utf-8")).hexdigest(),
                    "stderr_sha256": hashlib.sha256(
                        completed.stderr.encode("utf-8")).hexdigest(),
                    "timed_out": False,
                },
                "execution_status": child.get("execution_status",
                                              "NO_OBSERVATION"),
                "error": child.get("error"),
                "result": child.get("result"),
                "events": child.get("events", []),
                "imports": imports,
                "import_events": child.get("import_events", []),
                "observation_scope": "LOCAL_EXTERNAL_SUPERVISOR_CONTRACT",
            }


def _event_key(event: Mapping[str, Any]) -> tuple[str, str]:
    return (str(event.get("module")), str(event.get("qualname")))


def _expectation_problems(expectation: Any) -> list[str]:
    if not isinstance(expectation, TrustedExpectation):
        return ["EXPECTATION_INVALID"]
    problems = []
    for name in ("issuer", "candidate_commit", "candidate_tree",
                 "policy_sha256", "run_id", "nonce", "entrypoint_sha256"):
        if not isinstance(getattr(expectation, name), str) or not getattr(
                expectation, name):
            problems.append(f"EXPECTATION_FIELD_INVALID:{name}")
    for name in ("candidate_commit", "candidate_tree"):
        value = getattr(expectation, name)
        if isinstance(value, str) and not HEX40.fullmatch(value):
            problems.append(f"EXPECTATION_FIELD_INVALID:{name}")
    for name in ("policy_sha256", "entrypoint_sha256"):
        value = getattr(expectation, name)
        if isinstance(value, str) and not HEX64.fullmatch(value):
            problems.append(f"EXPECTATION_FIELD_INVALID:{name}")
    if not isinstance(expectation.expected_imports, Mapping):
        problems.append("EXPECTATION_IMPORTS_INVALID")
    else:
        for name, digest in expectation.expected_imports.items():
            if not isinstance(name, str) or not isinstance(digest, str):
                problems.append("EXPECTATION_IMPORTS_INVALID")
            elif not HEX64.fullmatch(digest):
                problems.append(f"EXPECTATION_IMPORT_DIGEST_INVALID:{name}")
    if not isinstance(expectation.expected_events, (tuple, list)):
        problems.append("EXPECTATION_EVENTS_INVALID")
    else:
        for event in expectation.expected_events:
            if not isinstance(event, Mapping):
                problems.append("EXPECTATION_EVENTS_INVALID")
                break
    return sorted(set(problems))


def verify_observation(
    *, observation: Mapping[str, Any], expectation: TrustedExpectation,
    nonce_ledger: NonceLedger, candidate_evidence: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Verify one supervisor observation against an externally pinned contract."""
    reasons: list[str] = []
    expectation_problems = _expectation_problems(expectation)
    reasons.extend(expectation_problems)
    if candidate_evidence not in (None, {}):
        reasons.append("CANDIDATE_AUTHORED_EVIDENCE")
    if not isinstance(observation, Mapping):
        reasons.append("OBSERVATION_INVALID")
        return _decision(observation, expectation, reasons)
    if observation.get("schema") != OBSERVATION_SCHEMA:
        reasons.append("OBSERVATION_SCHEMA_INVALID")
    if not isinstance(nonce_ledger, NonceLedger):
        reasons.append("NONCE_LEDGER_INVALID")

    bindings = {
        "issuer": observation.get("issuer"),
        "candidate_commit": observation.get("candidate_commit"),
        "candidate_tree": observation.get("candidate_tree"),
        "policy_sha256": observation.get("policy_sha256"),
        "run_id": observation.get("run_id"),
        "nonce": observation.get("nonce"),
    }
    if bindings["issuer"] != expectation.issuer:
        reasons.append("ISSUER_MISMATCH")
    if bindings["candidate_commit"] != expectation.candidate_commit:
        reasons.append("CANDIDATE_COMMIT_MISMATCH")
    if bindings["candidate_tree"] != expectation.candidate_tree:
        reasons.append("CANDIDATE_TREE_MISMATCH")
    if bindings["policy_sha256"] != expectation.policy_sha256:
        reasons.append("POLICY_MISMATCH")
    if bindings["run_id"] != expectation.run_id:
        reasons.append("RUN_ID_MISMATCH")
    if bindings["nonce"] != expectation.nonce:
        reasons.append("NONCE_MISMATCH")

    entrypoint = observation.get("entrypoint")
    if not isinstance(entrypoint, Mapping):
        reasons.append("ENTRYPOINT_BINDING_INVALID")
    elif entrypoint.get("sha256") != expectation.entrypoint_sha256:
        reasons.append("ENTRYPOINT_DIGEST_MISMATCH")

    process = observation.get("process")
    if not isinstance(process, Mapping):
        reasons.append("PROCESS_CAPTURE_INVALID")
    else:
        if process.get("exit_code") != 0:
            reasons.append("PROCESS_EXIT_NONZERO")
        if process.get("timed_out") is True:
            reasons.append("PROCESS_TIMEOUT")
    if observation.get("execution_status") != "COMPLETED":
        reasons.append("NATIVE_EXECUTION_NOT_COMPLETED")

    binding_clear = not reasons and not expectation_problems
    if binding_clear:
        if not nonce_ledger.consume(expectation.issuer, expectation.run_id,
                                    expectation.nonce):
            reasons.append("NONCE_REPLAYED")

    actual_events = observation.get("events")
    expected_events = [dict(row) for row in expectation.expected_events
                       ] if isinstance(expectation.expected_events,
                                       (tuple, list)) else []
    if not isinstance(actual_events, list) or not all(
            isinstance(row, Mapping) for row in actual_events):
        reasons.append("NATIVE_EVENT_CAPTURE_INVALID")
    else:
        actual_keys = [_event_key(row) for row in actual_events]
        expected_keys = [_event_key(row) for row in expected_events]
        if sorted(actual_keys) != sorted(expected_keys):
            reasons.append("NATIVE_EVENT_ANTI_JOIN")
        else:
            actual_status = {_event_key(row): row.get("status")
                             for row in actual_events}
            expected_status = {_event_key(row): row.get("status")
                               for row in expected_events}
            if actual_status != expected_status:
                reasons.append("NATIVE_EVENT_STATUS_MISMATCH")
            elif actual_keys != expected_keys:
                reasons.append("NATIVE_EVENT_ORDER_MISMATCH")

    actual_imports = observation.get("imports")
    expected_imports = dict(expectation.expected_imports) if isinstance(
        expectation.expected_imports, Mapping) else {}
    if not isinstance(actual_imports, Mapping):
        reasons.append("NATIVE_IMPORT_CAPTURE_INVALID")
    else:
        actual_names = set(actual_imports)
        expected_names = set(expected_imports)
        if actual_names != expected_names:
            reasons.append("NATIVE_IMPORT_ANTI_JOIN")
        for name in sorted(actual_names & expected_names):
            record = actual_imports.get(name)
            if not isinstance(record, Mapping):
                reasons.append(f"NATIVE_IMPORT_RECORD_INVALID:{name}")
                continue
            if record.get("within_target_dir") is not True:
                reasons.append(f"NATIVE_IMPORT_OUTSIDE_SCOPE:{name}")
            if record.get("sha256") != expected_imports[name]:
                reasons.append(f"NATIVE_IMPORT_DIGEST_MISMATCH:{name}")
        import_events = observation.get("import_events")
        if not isinstance(import_events, list):
            reasons.append("NATIVE_IMPORT_EVENT_CAPTURE_INVALID")
        else:
            for name in sorted(expected_names):
                if name not in import_events:
                    reasons.append(f"NATIVE_IMPORT_EVENT_MISSING:{name}")

    if not isinstance(expectation, TrustedExpectation):
        pass
    elif False and typed_digest(observation.get("result")) != typed_digest(
            expectation.expected_result):
        reasons.append("RESULT_MISMATCH")

    return _decision(observation, expectation, reasons)


def _decision(observation: Any, expectation: Any, reasons: list[str]) -> dict[str, Any]:
    unique = sorted(set(reasons))
    accepted = not unique
    observed = observation if isinstance(observation, Mapping) else {}
    imports = observed.get("imports")
    import_digests = {}
    if isinstance(imports, Mapping):
        for name, record in imports.items():
            if isinstance(record, Mapping):
                import_digests[str(name)] = record.get("sha256")
    events = observed.get("events")
    event_rows = []
    if isinstance(events, list):
        for row in events:
            if isinstance(row, Mapping):
                event_rows.append({
                    "module": row.get("module"),
                    "qualname": row.get("qualname"),
                    "status": row.get("status"),
                })
    expected_imports = {}
    expected_result = None
    if isinstance(expectation, TrustedExpectation):
        expected_imports = dict(expectation.expected_imports)
        expected_result = expectation.expected_result
    return {
        "schema": DECISION_SCHEMA,
        "contract_id": CONTRACT_ID,
        "decision": ACCEPT if accepted else REFUSE,
        "reasons": unique,
        "ceiling": CEILING if accepted else "NONE",
        "promotion": PROMOTION,
        "generic_promotion_authorized": False,
        "r00_ceiling": "UNCHANGED_LOCAL_TEST_ONLY",
        "bindings": {
            "issuer": observed.get("issuer"),
            "candidate_commit": observed.get("candidate_commit"),
            "candidate_tree": observed.get("candidate_tree"),
            "policy_sha256": observed.get("policy_sha256"),
            "run_id": observed.get("run_id"),
            "nonce": observed.get("nonce"),
            "entrypoint_sha256": (
                observed.get("entrypoint", {}).get("sha256")
                if isinstance(observed.get("entrypoint"), Mapping) else None
            ),
        },
        "observed": {
            "result": observed.get("result"),
            "result_digest": typed_digest(observed.get("result")),
            "events": event_rows,
            "imports": import_digests,
            "process_exit_code": (
                observed.get("process", {}).get("exit_code")
                if isinstance(observed.get("process"), Mapping) else None
            ),
            "execution_status": observed.get("execution_status"),
        },
        "expected": {
            "result_digest": typed_digest(expected_result),
            "imports": expected_imports,
        },
        "trusted_runtime_exclusions": list(TRUSTED_RUNTIME_EXCLUSIONS),
        "production_state": "DEPLOYMENT_HOLD",
        "requires_independent_review": True,
    }


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="Verify one R09 supervisor observation without promoting.")
    parser.add_argument("--observation", required=True)
    parser.add_argument("--expectation", required=True)
    args = parser.parse_args(argv)
    observation = json.loads(Path(args.observation).read_text(encoding="utf-8"))
    raw = json.loads(Path(args.expectation).read_text(encoding="utf-8"))
    expectation = TrustedExpectation(
        issuer=raw["issuer"],
        candidate_commit=raw["candidate_commit"],
        candidate_tree=raw["candidate_tree"],
        policy_sha256=raw["policy_sha256"],
        run_id=raw["run_id"],
        nonce=raw["nonce"],
        entrypoint_sha256=raw["entrypoint_sha256"],
        expected_imports=raw["expected_imports"],
        expected_events=tuple(raw["expected_events"]),
        expected_result=raw["expected_result"],
    )
    decision = verify_observation(
        observation=observation, expectation=expectation,
        nonce_ledger=NonceLedger(raw.get("nonce_ledger_path")),
    )
    print(json.dumps(decision, indent=2, sort_keys=True))
    return 0 if decision["decision"] == ACCEPT else 2


if __name__ == "__main__":
    raise SystemExit(main())
