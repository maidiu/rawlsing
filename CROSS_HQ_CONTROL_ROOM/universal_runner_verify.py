#!/usr/bin/env python3
"""R09 R2 local native verification with an external trusted supervisor.

The caller supplies a trust root whose signing key is held outside the executed
subject, a frozen expectation, and a durable one-shot nonce ledger. The
supervisor executes only entrypoint bytes read from the exact candidate commit,
captures actual loaded source bytes for repository imports, traces actual target
calls, and seals the observation in the parent process. Candidate-authored
receipts, mappings, flags and self-pins are not accepted evidence.

This is a local TEST_ONLY capability. It does not install or attest a protected
CI required check and does not authorize generic promotion.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from dataclasses import dataclass
from pathlib import Path
import re
import secrets
import subprocess
import sys
import tempfile
import threading
from typing import Any, Mapping

try:
    import fcntl
except ImportError:
    fcntl = None

CONTRACT_ID = "R61-R09-NATIVE-RUNNER-VERIFY@2"
OBSERVATION_SCHEMA = "R61_R09_SUPERVISOR_OBSERVATION@2"
DECISION_SCHEMA = "R61_R09_NATIVE_VERIFICATION_DECISION@2"
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
    "SAME_UID_CAN_REWRITE_VERIFIER_OR_RUNTIME",
    "TRUST_ROOT_MUST_BE_HELD_OUTSIDE_SUBJECT_CONTROL",
    "AUTHOR_VALIDATION_IS_NOT_INDEPENDENT_REVIEW",
)


class SupervisorError(ValueError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def typed_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def safe_typed_digest(value: Any) -> str | None:
    try:
        return typed_digest(value)
    except (TypeError, ValueError):
        return None


def sha256_file(path: str | os.PathLike[str]) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class TrustRoot:
    """Signing handle supplied by the external verifier.

    The key must live outside subject control. A child process does not receive
    it. This local implementation does not claim an external key service.
    """

    def __init__(self, issuer: str, key: bytes | None = None):
        if not isinstance(issuer, str) or not issuer:
            raise SupervisorError("ISSUER_INVALID")
        if key is None:
            key = secrets.token_bytes(32)
        if not isinstance(key, bytes) or len(key) < 32:
            raise SupervisorError("TRUST_ROOT_KEY_TOO_SHORT")
        self.issuer = issuer
        self._key = key
        self.fingerprint = sha256_bytes(key)

    def seal(self, payload: Mapping[str, Any]) -> str:
        return hmac.new(self._key, canonical_json(dict(payload)).encode("utf-8"),
                        hashlib.sha256).hexdigest()

    def matches(self, payload: Mapping[str, Any], authentication: Any) -> bool:
        if not isinstance(authentication, str):
            return False
        try:
            expected = self.seal(payload)
        except (TypeError, ValueError):
            return False
        return hmac.compare_digest(expected, authentication)


class TrustedObservation(dict):
    """Mutable mapping carrying a parent-issued HMAC over its current content."""

    def __init__(self, payload: Mapping[str, Any], *, authentication: str,
                 trust_root_fingerprint: str):
        super().__init__(payload)
        self.authentication = authentication
        self.trust_root_fingerprint = trust_root_fingerprint


def seal_observation(payload: Mapping[str, Any], trust_root: TrustRoot) -> TrustedObservation:
    return TrustedObservation(
        payload,
        authentication=trust_root.seal(payload),
        trust_root_fingerprint=trust_root.fingerprint,
    )


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
    trust_root_fingerprint: str = ""


class NonceLedger:
    """Durable cross-process one-shot nonce ledger.

    The data file is re-read under an exclusive advisory lock for every claim.
    A crash after append leaves the nonce consumed (fail closed). A malformed
    ledger fails closed. Without a path or fcntl the ledger is not durable.
    """

    def __init__(self, path: str | os.PathLike[str] | None = None):
        self.path = Path(path).resolve() if path is not None else None
        self.durable = bool(self.path is not None and fcntl is not None)
        self._lock = threading.Lock()
        self.last_status = "UNCLAIMED"

    def _key(self, issuer: str, run_id: str, nonce: str) -> str:
        return typed_digest([issuer, run_id, nonce])

    def claim(self, issuer: str, run_id: str, nonce: str) -> str:
        with self._lock:
            if not self.durable or self.path is None:
                self.last_status = "NOT_DURABLE"
                return self.last_status
            try:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                lock_path = self.path.with_name(self.path.name + ".lock")
                lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
            except OSError:
                self.last_status = "IO_ERROR"
                return self.last_status
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_EX)
                try:
                    lines = (self.path.read_text(encoding="ascii").splitlines()
                             if self.path.exists() else [])
                except (OSError, UnicodeError):
                    self.last_status = "CORRUPT"
                    return self.last_status
                clean = [line.strip() for line in lines if line.strip()]
                if any(not HEX64.fullmatch(line) for line in clean):
                    self.last_status = "CORRUPT"
                    return self.last_status
                key = self._key(issuer, run_id, nonce)
                if key in clean:
                    self.last_status = "REPLAYED"
                    return self.last_status
                try:
                    descriptor = os.open(
                        self.path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
                    try:
                        os.write(descriptor, (key + "\n").encode("ascii"))
                        os.fsync(descriptor)
                    finally:
                        os.close(descriptor)
                except OSError:
                    self.last_status = "IO_ERROR"
                    return self.last_status
                self.last_status = "CLAIMED"
                return self.last_status
            finally:
                try:
                    fcntl.flock(lock_fd, fcntl.LOCK_UN)
                finally:
                    os.close(lock_fd)

    def consume(self, issuer: str, run_id: str, nonce: str) -> bool:
        return self.claim(issuer, run_id, nonce) == "CLAIMED"


WRAPPER_SOURCE = r'''
import builtins
import hashlib
import importlib.abc
import importlib.machinery
import importlib.util
import json
import os
import sys

config = json.loads(open(sys.argv[1], encoding="utf-8").read())
repo_root = os.path.abspath(config["repo_root"])
entrypoint = os.path.abspath(config["entrypoint"])
target_file = os.path.abspath(config["target_file"])
target_module = config["target_module"]
observation_path = config["observation_path"]
entry_bytes = __import__("base64").b64decode(config["entrypoint_source_b64"])
sys.dont_write_bytecode = True
sys.path.insert(0, repo_root)
sys.path.insert(0, os.path.dirname(entrypoint))

import_events = []
loaded_sources = {}


def audit(event, args):
    if event == "import":
        import_events.append(str(args[0]))


sys.addaudithook(audit)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


class _BytesLoader(importlib.abc.Loader):
    def __init__(self, code, origin):
        self.code = code
        self.origin = origin

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        module.__file__ = self.origin
        module.__loader__ = self
        exec(self.code, module.__dict__)


class _CustodyFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        spec = importlib.machinery.PathFinder.find_spec(fullname, path, target)
        if spec is None or not spec.origin or not spec.origin.endswith(".py"):
            return spec
        origin = os.path.abspath(spec.origin)
        if not origin.startswith(repo_root + os.sep):
            return spec
        try:
            data = open(origin, "rb").read()
            code = compile(data, origin, "exec")
        except (OSError, SyntaxError, ValueError):
            return spec
        loaded_sources[fullname] = {
            "path": origin,
            "loaded_sha256": _sha(data),
        }
        spec.loader = _BytesLoader(code, origin)
        return spec


sys.meta_path.insert(0, _CustodyFinder())

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
namespace = {"__name__": "__main__", "__file__": entrypoint}
sys.settrace(tracer)
try:
    exec(compile(entry_bytes, entrypoint, "exec"), namespace, namespace)
    if "RESULT" in namespace:
        result = namespace["RESULT"]
    else:
        execution_status = "NO_RESULT"
except BaseException as exc:
    execution_status = "ERROR"
    error = {"type": type(exc).__name__, "message": str(exc)[:1000]}
finally:
    sys.settrace(None)

payload = {
    "execution_status": execution_status,
    "error": error,
    "result": result,
    "events": events,
    "loaded_sources": loaded_sources,
    "import_events": list(dict.fromkeys(import_events)),
}
with open(observation_path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, sort_keys=True)
os._exit(0)
'''


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-c", "gc.auto=0", *args], cwd=str(repo),
                          text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=30, check=False)


def _git_tree(repo: Path, commit: str) -> str:
    completed = _git(repo, "rev-parse", f"{commit}^{{tree}}")
    tree = completed.stdout.strip()
    if completed.returncode != 0 or not HEX40.fullmatch(tree):
        raise SupervisorError("CANDIDATE_TREE_UNRESOLVED")
    return tree


def _git_blob(repo: Path, commit: str, relative: str) -> bytes:
    completed = subprocess.run(
        ["git", "-c", "gc.auto=0", "show", f"{commit}:{relative}"],
        cwd=str(repo), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=60, check=False)
    if completed.returncode != 0:
        raise SupervisorError(f"BLOB_NOT_IN_CANDIDATE_TREE:{relative}")
    return completed.stdout


def _relative_to(path: Path, root: Path) -> str | None:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def _refusal_payload(*, issuer: str, candidate_commit: str,
                     candidate_tree: str, policy_sha256: str, run_id: str,
                     nonce: str, reasons: list[str]) -> dict[str, Any]:
    return {
        "schema": OBSERVATION_SCHEMA,
        "issuer": issuer,
        "candidate_commit": candidate_commit,
        "candidate_tree": candidate_tree,
        "policy_sha256": policy_sha256,
        "run_id": run_id,
        "nonce": nonce,
        "entrypoint": {"path": None, "sha256": None, "tree_bound": False},
        "target_file": {"path": None, "sha256": None, "tree_bound": False},
        "process": {"argv": [], "exit_code": None, "timed_out": False},
        "execution_status": "REFUSED",
        "error": None,
        "result": None,
        "events": [],
        "imports": {},
        "import_events": [],
        "custody_failures": reasons,
        "supervisor_refusals": reasons,
        "observation_scope": "LOCAL_EXTERNAL_TRUST_ROOT",
    }


class LocalNativeSupervisor:
    """Local supervisor: committed entrypoint bytes, load-time import custody.

    The entrypoint is executed from the exact bytes in the candidate commit.
    Imported repository modules are compiled from bytes read once by a custody
    loader; the parent compares each load-time digest with the candidate tree.
    """

    def __init__(self, *, repo_root: str | os.PathLike[str], issuer: str = "",
                 policy_path: str | os.PathLike[str], target_module: str,
                 target_file: str | os.PathLike[str],
                 entrypoint: str | os.PathLike[str],
                 trust_root: TrustRoot | None = None,
                 python: str | None = None, timeout: int = 60):
        self.repo_root = Path(repo_root).resolve()
        if trust_root is None:
            if not issuer:
                raise SupervisorError("TRUST_ROOT_OR_ISSUER_REQUIRED")
            trust_root = TrustRoot(issuer)
        if issuer and trust_root.issuer != issuer:
            raise SupervisorError("ISSUER_TRUST_ROOT_MISMATCH")
        self.trust_root = trust_root
        self.issuer = trust_root.issuer
        self.policy_path = Path(policy_path).resolve()
        self.target_module = str(target_module)
        self.target_file = Path(target_file).resolve()
        self.entrypoint = Path(entrypoint).resolve()
        self.python = python or sys.executable
        self.timeout = int(timeout)
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", self.target_module):
            raise SupervisorError("TARGET_MODULE_INVALID")
        if not self.policy_path.is_file():
            raise SupervisorError(f"TRUSTED_INPUT_MISSING:{self.policy_path}")

    def _seal(self, payload: dict[str, Any]) -> TrustedObservation:
        return seal_observation(payload, self.trust_root)

    def observe(self, *, candidate_commit: str, run_id: str,
                nonce: str) -> TrustedObservation:
        if not HEX40.fullmatch(candidate_commit):
            raise SupervisorError("CANDIDATE_COMMIT_INVALID")
        candidate_tree = _git_tree(self.repo_root, candidate_commit)
        policy_sha256 = sha256_file(self.policy_path)
        base = {
            "issuer": self.issuer,
            "candidate_commit": candidate_commit,
            "candidate_tree": candidate_tree,
            "policy_sha256": policy_sha256,
            "run_id": run_id,
            "nonce": nonce,
        }
        entry_rel = _relative_to(self.entrypoint, self.repo_root)
        target_rel = _relative_to(self.target_file, self.repo_root)
        if entry_rel is None:
            return self._seal(_refusal_payload(
                **base, reasons=["ENTRYPOINT_OUTSIDE_CANDIDATE_TREE"]))
        if target_rel is None:
            return self._seal(_refusal_payload(
                **base, reasons=["TARGET_FILE_OUTSIDE_CANDIDATE_TREE"]))
        try:
            entry_bytes = _git_blob(self.repo_root, candidate_commit, entry_rel)
            _git_blob(self.repo_root, candidate_commit, target_rel)
        except SupervisorError as exc:
            return self._seal(_refusal_payload(**base, reasons=[str(exc)]))
        entry_sha256 = sha256_bytes(entry_bytes)
        target_worktree_sha256 = sha256_file(self.target_file)
        with tempfile.TemporaryDirectory(prefix="r09-native-") as directory:
            work = Path(directory)
            wrapper = work / "supervisor_wrapper.py"
            config_path = work / "config.json"
            output_path = work / "observation.json"
            wrapper.write_text(WRAPPER_SOURCE, encoding="utf-8")
            config_path.write_text(canonical_json({
                "repo_root": str(self.repo_root),
                "entrypoint": str(self.entrypoint),
                "entrypoint_source_b64": base64.b64encode(entry_bytes).decode("ascii"),
                "target_file": str(self.target_file),
                "target_module": self.target_module,
                "observation_path": str(output_path),
            }), encoding="utf-8")
            environment = {
                "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                "LANG": "C.UTF-8",
                "PYTHONDONTWRITEBYTECODE": "1",
            }
            try:
                completed = subprocess.run(
                    [self.python, "-I", str(wrapper), str(config_path)],
                    cwd=str(work), env=environment, text=True,
                    timeout=self.timeout, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, check=False)
                timed_out = False
            except subprocess.TimeoutExpired as exc:
                completed = subprocess.CompletedProcess(
                    exc.cmd, -1, exc.stdout or "", exc.stderr or "")
                timed_out = True
            child: dict[str, Any] = {}
            if output_path.is_file():
                try:
                    child = json.loads(output_path.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    child = {}
            loaded = child.get("loaded_sources")
            imports: dict[str, Any] = {}
            custody_failures: list[str] = []
            if isinstance(loaded, Mapping):
                for name, record in loaded.items():
                    if not isinstance(name, str) or not isinstance(record, Mapping):
                        custody_failures.append(f"IMPORT_RECORD_INVALID:{name}")
                        continue
                    path_value = record.get("path")
                    loaded_sha = record.get("loaded_sha256")
                    if not isinstance(path_value, str) or not isinstance(loaded_sha, str):
                        custody_failures.append(f"IMPORT_RECORD_INVALID:{name}")
                        continue
                    resolved = Path(path_value).resolve()
                    relative = _relative_to(resolved, self.repo_root)
                    if relative is None:
                        custody_failures.append(f"IMPORT_OUTSIDE_CANDIDATE_TREE:{name}")
                        imports[name] = {"path": str(resolved),
                                         "loaded_sha256": loaded_sha,
                                         "within_target_dir": False,
                                         "tree_bound": False}
                        continue
                    try:
                        blob = _git_blob(self.repo_root, candidate_commit,
                                         relative)
                    except SupervisorError:
                        custody_failures.append(
                            f"IMPORT_NOT_IN_CANDIDATE_TREE:{name}")
                        imports[name] = {"path": str(resolved),
                                         "loaded_sha256": loaded_sha,
                                         "within_target_dir": False,
                                         "tree_bound": False}
                        continue
                    tree_sha = sha256_bytes(blob)
                    bound = tree_sha == loaded_sha
                    if not bound:
                        custody_failures.append(
                            f"IMPORT_LOADED_BYTES_NOT_IN_TREE:{name}")
                    imports[name] = {
                        "path": str(resolved),
                        "loaded_sha256": loaded_sha,
                        "tree_sha256": tree_sha,
                        "within_target_dir": resolved.parent == self.target_file.parent,
                        "tree_bound": bound,
                    }
            payload = {
                "schema": OBSERVATION_SCHEMA,
                "issuer": self.issuer,
                "candidate_commit": candidate_commit,
                "candidate_tree": candidate_tree,
                "policy_sha256": policy_sha256,
                "run_id": run_id,
                "nonce": nonce,
                "entrypoint": {"path": str(self.entrypoint),
                               "sha256": entry_sha256,
                               "tree_bound": True,
                               "relative_path": entry_rel},
                "target_file": {"path": str(self.target_file),
                                "sha256": target_worktree_sha256,
                                "tree_bound": True,
                                "relative_path": target_rel},
                "process": {
                    "argv": [self.python, "-I", "supervisor_wrapper.py"],
                    "exit_code": completed.returncode,
                    "stdout_sha256": sha256_bytes(
                        str(completed.stdout).encode("utf-8")),
                    "stderr_sha256": sha256_bytes(
                        str(completed.stderr).encode("utf-8")),
                    "timed_out": timed_out,
                },
                "execution_status": child.get("execution_status",
                                              "NO_OBSERVATION"),
                "error": child.get("error"),
                "result": child.get("result"),
                "events": child.get("events", []),
                "imports": imports,
                "import_events": child.get("import_events", []),
                "custody_failures": custody_failures,
                "supervisor_refusals": [],
                "observation_scope": "LOCAL_EXTERNAL_TRUST_ROOT",
            }
            return self._seal(payload)


def _event_key(event: Mapping[str, Any]) -> tuple[str, str]:
    return (str(event.get("module")), str(event.get("qualname")))


def _expectation_problems(expectation: Any) -> list[str]:
    if not isinstance(expectation, TrustedExpectation):
        return ["EXPECTATION_INVALID"]
    problems = []
    for name in ("issuer", "candidate_commit", "candidate_tree",
                 "policy_sha256", "run_id", "nonce", "entrypoint_sha256",
                 "trust_root_fingerprint"):
        if not isinstance(getattr(expectation, name), str) or not getattr(
                expectation, name):
            problems.append(f"EXPECTATION_FIELD_INVALID:{name}")
    for name in ("candidate_commit", "candidate_tree"):
        value = getattr(expectation, name)
        if isinstance(value, str) and not HEX40.fullmatch(value):
            problems.append(f"EXPECTATION_FIELD_INVALID:{name}")
    for name in ("policy_sha256", "entrypoint_sha256",
                 "trust_root_fingerprint"):
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
    if safe_typed_digest(expectation.expected_result) is None:
        problems.append("EXPECTATION_RESULT_NOT_SERIALIZABLE")
    return sorted(set(problems))


def _observation_authentic(observation: Mapping[str, Any],
                           trust_root: TrustRoot | None,
                           expectation: TrustedExpectation) -> tuple[bool, list[str]]:
    reasons = []
    if trust_root is None:
        return False, ["TRUST_ROOT_REQUIRED"]
    if not isinstance(trust_root, TrustRoot):
        return False, ["TRUST_ROOT_INVALID"]
    if not isinstance(observation, TrustedObservation):
        return False, ["UNTRUSTED_OBSERVATION"]
    if observation.trust_root_fingerprint != trust_root.fingerprint:
        reasons.append("TRUST_ROOT_FINGERPRINT_MISMATCH")
    if (isinstance(expectation, TrustedExpectation)
            and expectation.trust_root_fingerprint != trust_root.fingerprint):
        reasons.append("EXPECTATION_TRUST_ROOT_MISMATCH")
    if not trust_root.matches(dict(observation), observation.authentication):
        reasons.append("OBSERVATION_AUTHENTICATION_FAILED")
    return not reasons, reasons


def verify_observation(
    *, observation: Mapping[str, Any], expectation: TrustedExpectation,
    nonce_ledger: NonceLedger, trust_root: TrustRoot | None = None,
    candidate_evidence: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    reasons: list[str] = []
    expectation_problems = _expectation_problems(expectation)
    reasons.extend(expectation_problems)
    if candidate_evidence not in (None, {}):
        reasons.append("CANDIDATE_AUTHORED_EVIDENCE")
    authentic, auth_reasons = _observation_authentic(
        observation, trust_root, expectation)
    reasons.extend(auth_reasons)
    if not authentic:
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
    else:
        if entrypoint.get("sha256") != expectation.entrypoint_sha256:
            reasons.append("ENTRYPOINT_DIGEST_MISMATCH")
        if entrypoint.get("tree_bound") is not True:
            reasons.append("ENTRYPOINT_NOT_TREE_BOUND")

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

    supervisor_refusals = observation.get("supervisor_refusals")
    if supervisor_refusals:
        reasons.extend(f"SUPERVISOR_REFUSED:{row}"
                       for row in supervisor_refusals)
    custody_failures = observation.get("custody_failures")
    if custody_failures:
        reasons.extend(f"NATIVE_CUSTODY_FAILED:{row}"
                       for row in custody_failures)

    durable_reasons = []
    if not isinstance(nonce_ledger, NonceLedger) or not nonce_ledger.durable:
        durable_reasons.append("NONCE_LEDGER_NOT_DURABLE")
    binding_clear = not reasons and not expectation_problems and not durable_reasons
    if binding_clear:
        claim = nonce_ledger.claim(expectation.issuer, expectation.run_id,
                                   expectation.nonce)
        if claim == "REPLAYED":
            reasons.append("NONCE_REPLAYED")
        elif claim == "CORRUPT":
            reasons.append("NONCE_LEDGER_CORRUPT")
        elif claim != "CLAIMED":
            reasons.append("NONCE_LEDGER_IO_FAILURE")
    elif durable_reasons:
        reasons.extend(durable_reasons)

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
        for name in sorted(set(expected_imports)):
            if name not in actual_names:
                reasons.append(f"NATIVE_IMPORT_MISSING:{name}")
                continue
            record = actual_imports.get(name)
            if not isinstance(record, Mapping):
                reasons.append(f"NATIVE_IMPORT_RECORD_INVALID:{name}")
                continue
            if record.get("loaded_sha256") != expected_imports[name]:
                reasons.append(f"NATIVE_IMPORT_DIGEST_MISMATCH:{name}")
            if record.get("tree_bound") is not True:
                reasons.append(f"NATIVE_IMPORT_NOT_TREE_BOUND:{name}")
        import_events = observation.get("import_events")
        if not isinstance(import_events, list):
            reasons.append("NATIVE_IMPORT_EVENT_CAPTURE_INVALID")
        else:
            for name in sorted(expected_imports):
                if name not in import_events:
                    reasons.append(f"NATIVE_IMPORT_EVENT_MISSING:{name}")

    if safe_typed_digest(observation.get("result")) is None:
        reasons.append("OBSERVED_RESULT_NOT_SERIALIZABLE")
    elif typed_digest(observation.get("result")) != typed_digest(
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
                import_digests[str(name)] = {
                    "loaded_sha256": record.get("loaded_sha256"),
                    "tree_bound": record.get("tree_bound"),
                }
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
    result_digest = safe_typed_digest(observed.get("result"))
    expected_digest = safe_typed_digest(expected_result)
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
            "result_digest": result_digest,
            "events": event_rows,
            "imports": import_digests,
            "custody_failures": observed.get("custody_failures", []),
            "process_exit_code": (
                observed.get("process", {}).get("exit_code")
                if isinstance(observed.get("process"), Mapping) else None
            ),
            "execution_status": observed.get("execution_status"),
        },
        "expected": {
            "result_digest": expected_digest,
            "imports": expected_imports,
        },
        "trusted_runtime_exclusions": list(TRUSTED_RUNTIME_EXCLUSIONS),
        "production_state": "DEPLOYMENT_HOLD",
        "requires_independent_review": True,
    }


def serialize_observation(observation: TrustedObservation) -> dict[str, Any]:
    payload = dict(observation)
    payload["_authentication"] = observation.authentication
    payload["_trust_root_fingerprint"] = observation.trust_root_fingerprint
    return payload


def observation_from_serialized(payload: Mapping[str, Any]) -> TrustedObservation:
    data = dict(payload)
    authentication = data.pop("_authentication", None)
    fingerprint = data.pop("_trust_root_fingerprint", None)
    return TrustedObservation(data, authentication=authentication,
                              trust_root_fingerprint=fingerprint)


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="Verify one R09 sealed observation without promotion.")
    parser.add_argument("--observation", required=True)
    parser.add_argument("--expectation", required=True)
    parser.add_argument("--nonce-ledger", default=None)
    parser.add_argument("--trust-root-key", default=None)
    args = parser.parse_args(argv)
    observation = observation_from_serialized(
        json.loads(Path(args.observation).read_text(encoding="utf-8")))
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
        trust_root_fingerprint=raw.get("trust_root_fingerprint", ""),
    )
    trust_root = None
    if args.trust_root_key:
        key = Path(args.trust_root_key).read_bytes()
        trust_root = TrustRoot(raw["issuer"], key)
    decision = verify_observation(
        observation=observation, expectation=expectation,
        nonce_ledger=NonceLedger(args.nonce_ledger),
        trust_root=trust_root,
    )
    print(json.dumps(decision, indent=2, sort_keys=True))
    return 0 if decision["decision"] == ACCEPT else 2


if __name__ == "__main__":
    raise SystemExit(main())
