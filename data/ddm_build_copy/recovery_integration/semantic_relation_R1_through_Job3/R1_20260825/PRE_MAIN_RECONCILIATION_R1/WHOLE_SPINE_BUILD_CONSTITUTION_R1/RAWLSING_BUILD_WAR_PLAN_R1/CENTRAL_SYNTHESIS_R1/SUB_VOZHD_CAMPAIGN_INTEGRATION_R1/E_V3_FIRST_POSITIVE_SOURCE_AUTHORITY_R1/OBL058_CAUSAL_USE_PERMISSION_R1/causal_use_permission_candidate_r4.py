"""OBL058 CAUSAL_USE_PERMISSION R4 bounded repair candidate.

The R4 source-origin boundary is process-isolated. The parent Python module does
not hold the authoritative issuance ledger. The authority process accepts only
exact scope/basis inputs, computes each receipt body itself, and binds that body
to the supplied object identity. Caller-built receipt content is never accepted
by the issuance protocol.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import asdict, dataclass
import atexit
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

AUTHORITY_ID = "OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.3.0"
SCHEMA_VERSION = "OBL058_CAUSAL_USE_PERMISSION_RECEIPT@4.0.0"
FIXTURE_CLASS = "NONCURRENT_SYNTHETIC"
DECISION_PERMIT = "PERMIT"
DECISION_DENY = "DENY"
SOURCE_BASIS_KIND = "EXPLICIT_SOURCE_OWNED_CAUSAL_USE_PERMISSION"
NO_MATCHING_BASIS_KIND = "NO_MATCHING_SOURCE_OWNED_CAUSAL_USE_PERMISSION"

_SCOPE_PREFIXES = {
    "actor_id": "NONCURRENT_SYNTHETIC::actor::",
    "world_id": "NONCURRENT_SYNTHETIC::world::",
    "subject_id": "NONCURRENT_SYNTHETIC::subject::",
    "time_id": "NONCURRENT_SYNTHETIC::time::",
    "transition_id": "NONCURRENT_SYNTHETIC::transition::",
}


class PermissionContractError(ValueError):
    """Fail-closed contract violation."""


@dataclass(frozen=True)
class ExactScope:
    actor_id: str
    world_id: str
    subject_id: str
    time_id: str
    transition_id: str

    def validate(self) -> None:
        for name, value in asdict(self).items():
            prefix = _SCOPE_PREFIXES[name]
            if not isinstance(value, str) or not value.startswith(prefix):
                raise PermissionContractError(f"noncurrent_synthetic_scope_required:{name}")
            if not value[len(prefix):].strip():
                raise PermissionContractError(f"missing_or_invalid_scope:{name}")

    def canonical(self) -> dict[str, str]:
        self.validate()
        return asdict(self)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def scope_digest(scope: ExactScope) -> str:
    return hashlib.sha256(_canonical_json(scope.canonical()).encode("utf-8")).hexdigest()


REGISTERED_POSITIVE_SCOPE = ExactScope(
    actor_id="NONCURRENT_SYNTHETIC::actor::obl058-r4-a1",
    world_id="NONCURRENT_SYNTHETIC::world::obl058-r4-w1",
    subject_id="NONCURRENT_SYNTHETIC::subject::obl058-r4-s1",
    time_id="NONCURRENT_SYNTHETIC::time::obl058-r4-t1",
    transition_id="NONCURRENT_SYNTHETIC::transition::obl058-r4-tr1",
)
REGISTERED_POSITIVE_BASIS_ID = "NONCURRENT_SYNTHETIC::basis::obl058-r4-source-owned-permit-001"


def _basis_proof_digest(*, basis_id: str, sd: str, basis_kind: str, decision: str) -> str:
    payload = {
        "basis_id": basis_id,
        "scope_digest": sd,
        "basis_kind": basis_kind,
        "decision": decision,
    }
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _receipt_integrity_payload(receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {k: receipt[k] for k in (
        "authority_id", "schema_version", "fixture_class", "scope",
        "scope_digest", "decision", "basis_kind", "basis_id",
        "basis_scope_digest", "basis_proof_digest",
    )}


def receipt_digest(receipt: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        _canonical_json(_receipt_integrity_payload(receipt)).encode("utf-8")
    ).hexdigest()


def _service_validate_scope_dict(scope: object) -> dict[str, str]:
    if type(scope) is not dict or set(scope) != set(_SCOPE_PREFIXES):
        raise PermissionContractError("malformed_scope")
    out: dict[str, str] = {}
    for name, prefix in _SCOPE_PREFIXES.items():
        value = scope.get(name)
        if not isinstance(value, str) or not value.startswith(prefix):
            raise PermissionContractError(f"noncurrent_synthetic_scope_required:{name}")
        if not value[len(prefix):].strip():
            raise PermissionContractError(f"missing_or_invalid_scope:{name}")
        out[name] = value
    return out


def _service_scope_digest(scope: dict[str, str]) -> str:
    return hashlib.sha256(_canonical_json(scope).encode("utf-8")).hexdigest()


def _service_build_body(*, scope: dict[str, str], basis_id: str, fixture_class: str) -> str:
    exact_scope = _service_validate_scope_dict(scope)
    if fixture_class != FIXTURE_CLASS:
        raise PermissionContractError("project_current_or_unknown_fixture_not_authorized")
    if not isinstance(basis_id, str) or not basis_id.strip():
        raise PermissionContractError("missing_basis_id")

    sd = _service_scope_digest(exact_scope)
    registered_sd = _service_scope_digest(REGISTERED_POSITIVE_SCOPE.canonical())
    if basis_id == REGISTERED_POSITIVE_BASIS_ID and sd == registered_sd:
        decision = DECISION_PERMIT
        basis_kind = SOURCE_BASIS_KIND
    else:
        decision = DECISION_DENY
        basis_kind = NO_MATCHING_BASIS_KIND

    body: dict[str, Any] = {
        "authority_id": AUTHORITY_ID,
        "schema_version": SCHEMA_VERSION,
        "fixture_class": FIXTURE_CLASS,
        "scope": exact_scope,
        "scope_digest": sd,
        "decision": decision,
        "basis_kind": basis_kind,
        "basis_id": basis_id,
        "basis_scope_digest": sd,
        "basis_proof_digest": _basis_proof_digest(
            basis_id=basis_id,
            sd=sd,
            basis_kind=basis_kind,
            decision=decision,
        ),
    }
    body["receipt_digest"] = receipt_digest(body)
    return _canonical_json(body)


def _service_validate_body(*, body_json: str, expected_scope: dict[str, str]) -> str:
    if not isinstance(body_json, str) or not body_json:
        raise PermissionContractError("malformed_receipt_body")
    try:
        body = json.loads(body_json)
    except (TypeError, json.JSONDecodeError) as exc:
        raise PermissionContractError("malformed_receipt_body") from exc
    if type(body) is not dict:
        raise PermissionContractError("malformed_receipt_body")

    required = {
        "authority_id", "schema_version", "fixture_class", "scope",
        "scope_digest", "decision", "basis_kind", "basis_id",
        "basis_scope_digest", "basis_proof_digest", "receipt_digest",
    }
    if set(body) != required:
        raise PermissionContractError("malformed_receipt_keys")
    if body["authority_id"] != AUTHORITY_ID:
        raise PermissionContractError("wrong_authority")
    if body["schema_version"] != SCHEMA_VERSION:
        raise PermissionContractError("wrong_schema")
    if body["fixture_class"] != FIXTURE_CLASS:
        raise PermissionContractError("project_current_or_unknown_fixture_not_authorized")
    if body["decision"] not in {DECISION_PERMIT, DECISION_DENY}:
        raise PermissionContractError("invalid_decision")

    scope = _service_validate_scope_dict(body["scope"])
    expected = _service_validate_scope_dict(expected_scope)
    if scope != expected:
        raise PermissionContractError("scope_mismatch_or_stale")
    sd = _service_scope_digest(expected)
    if body["scope_digest"] != sd:
        raise PermissionContractError("scope_digest_mismatch")
    if body["basis_scope_digest"] != sd:
        raise PermissionContractError("basis_scope_mismatch")
    if not isinstance(body["basis_id"], str) or not body["basis_id"].strip():
        raise PermissionContractError("missing_basis_id")

    integrity = hashlib.sha256(
        _canonical_json({k: body[k] for k in (
            "authority_id", "schema_version", "fixture_class", "scope",
            "scope_digest", "decision", "basis_kind", "basis_id",
            "basis_scope_digest", "basis_proof_digest",
        )}).encode("utf-8")
    ).hexdigest()
    if body["receipt_digest"] != integrity:
        raise PermissionContractError("receipt_integrity_mismatch")

    registered_sd = _service_scope_digest(REGISTERED_POSITIVE_SCOPE.canonical())
    registered = body["basis_id"] == REGISTERED_POSITIVE_BASIS_ID and sd == registered_sd
    if body["decision"] == DECISION_PERMIT:
        if not registered:
            raise PermissionContractError("positive_decision_without_registered_source_basis")
        if body["basis_kind"] != SOURCE_BASIS_KIND:
            raise PermissionContractError("positive_decision_without_source_owned_basis")
        expected_proof = _basis_proof_digest(
            basis_id=body["basis_id"], sd=sd,
            basis_kind=SOURCE_BASIS_KIND, decision=DECISION_PERMIT,
        )
        if body["basis_proof_digest"] != expected_proof:
            raise PermissionContractError("source_basis_proof_mismatch")
    else:
        if registered:
            raise PermissionContractError("denial_conflicts_with_registered_source_basis")
        if body["basis_kind"] != NO_MATCHING_BASIS_KIND:
            raise PermissionContractError("invalid_denial_basis_kind")
        expected_proof = _basis_proof_digest(
            basis_id=body["basis_id"], sd=sd,
            basis_kind=NO_MATCHING_BASIS_KIND, decision=DECISION_DENY,
        )
        if body["basis_proof_digest"] != expected_proof:
            raise PermissionContractError("denial_basis_proof_mismatch")
    return str(body["decision"])


def _authority_service_loop() -> int:
    # This dictionary exists only inside the authority subprocess. No parent
    # function closure/default/global contains or aliases it.
    issued: dict[int, str] = {}

    def emit(payload: dict[str, Any]) -> None:
        sys.stdout.write(_canonical_json(payload) + "\n")
        sys.stdout.flush()

    for line in sys.stdin:
        try:
            request = json.loads(line)
            if type(request) is not dict or not isinstance(request.get("op"), str):
                raise PermissionContractError("service_protocol_error")
            op = request["op"]

            if op == "issue":
                if set(request) != {"op", "object_id", "scope", "basis_id", "fixture_class"}:
                    raise PermissionContractError("service_protocol_error")
                object_id = request["object_id"]
                if not isinstance(object_id, int) or object_id <= 0:
                    raise PermissionContractError("service_protocol_error")
                if object_id in issued:
                    raise PermissionContractError("object_identity_already_issued")
                body_json = _service_build_body(
                    scope=request["scope"],
                    basis_id=request["basis_id"],
                    fixture_class=request["fixture_class"],
                )
                issued[object_id] = body_json
                emit({"ok": True, "body_json": body_json})

            elif op == "validate":
                if set(request) != {"op", "object_id", "body_json", "expected_scope"}:
                    raise PermissionContractError("service_protocol_error")
                object_id = request["object_id"]
                if not isinstance(object_id, int) or object_id <= 0:
                    raise PermissionContractError("service_protocol_error")
                decision = _service_validate_body(
                    body_json=request["body_json"],
                    expected_scope=request["expected_scope"],
                )
                authoritative = issued.get(object_id)
                if authoritative is None or authoritative != request["body_json"]:
                    raise PermissionContractError("receipt_not_issued_by_source_authority")
                emit({"ok": True, "decision": decision})

            else:
                raise PermissionContractError("service_protocol_error")

        except PermissionContractError as exc:
            emit({"ok": False, "error": str(exc)})
        except Exception:
            emit({"ok": False, "error": "service_internal_error"})
    return 0


class IssuedReceipt(Mapping[str, Any]):
    __slots__ = ("_body_json",)

    def __init__(self, body_json: str = "") -> None:
        object.__setattr__(self, "_body_json", body_json)

    def _public_body(self) -> dict[str, Any]:
        raw = object.__getattribute__(self, "_body_json")
        if not isinstance(raw, str) or not raw:
            raise PermissionContractError("receipt_not_issued_by_source_authority")
        try:
            body = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise PermissionContractError("malformed_receipt_body") from exc
        if type(body) is not dict:
            raise PermissionContractError("malformed_receipt_body")
        return body

    def __getitem__(self, key: str) -> Any:
        value = self._public_body()[key]
        if key == "scope":
            return dict(value)
        return value

    def __iter__(self) -> Iterator[str]:
        return iter(self._public_body())

    def __len__(self) -> int:
        return len(self._public_body())

    def __copy__(self):
        raise TypeError("source_receipt_not_copyable")

    def __deepcopy__(self, memo):
        raise TypeError("source_receipt_not_copyable")

    def __reduce_ex__(self, protocol):
        raise TypeError("source_receipt_not_serializable")


def _start_service() -> subprocess.Popen[bytes]:
    path = str(Path(__file__).resolve())
    proc = subprocess.Popen(
        [sys.executable, path, "--authority-service"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=False,
        bufsize=0,
    )
    if proc.stdin is None or proc.stdout is None:
        raise PermissionContractError("authority_service_unavailable")
    return proc


def _build_service_request(write_fd: int, read_fd: int):
    # The generated request function has no closure/defaults. Its code constants
    # contain only the process pipe descriptors. Recovering those descriptors
    # exposes the same narrow protocol, not the subprocess-local ledger.
    namespace: dict[str, Any] = {}
    source = f'''
def service_request(request):
    if type(request) is not dict:
        raise PermissionContractError("authority_service_protocol_error")
    raw = (_canonical_json(request) + "\\n").encode("utf-8")
    try:
        offset = 0
        while offset < len(raw):
            written = os.write({write_fd}, raw[offset:])
            if written <= 0:
                raise OSError("short write")
            offset += written
        chunks = []
        while True:
            chunk = os.read({read_fd}, 4096)
            if not chunk:
                raise OSError("service eof")
            chunks.append(chunk)
            if b"\\n" in chunk:
                break
    except OSError as exc:
        raise PermissionContractError("authority_service_unavailable") from exc
    line = b"".join(chunks).split(b"\\n", 1)[0]
    try:
        response = json.loads(line.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PermissionContractError("authority_service_protocol_error") from exc
    if type(response) is not dict or response.get("ok") is not True:
        error = response.get("error") if isinstance(response, dict) else None
        raise PermissionContractError(str(error or "authority_service_protocol_error"))
    return response
'''
    exec(source, globals(), namespace)
    return namespace["service_request"]


def _register_service_stop(proc: subprocess.Popen[bytes]) -> None:
    def _stop(_proc=proc):
        try:
            if _proc.poll() is None:
                _proc.terminate()
                _proc.wait(timeout=1)
        except Exception:
            pass
    atexit.register(_stop)


def issue_noncurrent_synthetic_receipt(
    *,
    scope: ExactScope,
    basis_id: str,
    fixture_class: str = FIXTURE_CLASS,
) -> Mapping[str, Any]:
    scope.validate()
    if fixture_class != FIXTURE_CLASS:
        raise PermissionContractError("project_current_or_unknown_fixture_not_authorized")
    if not isinstance(basis_id, str) or not basis_id.strip():
        raise PermissionContractError("missing_basis_id")

    receipt = IssuedReceipt()
    response = _service_request({
        "op": "issue",
        "object_id": id(receipt),
        "scope": scope.canonical(),
        "basis_id": basis_id,
        "fixture_class": fixture_class,
    })
    body_json = response.get("body_json")
    if not isinstance(body_json, str) or not body_json:
        raise PermissionContractError("authority_service_protocol_error")
    object.__setattr__(receipt, "_body_json", body_json)

    # Lifetime pinning prevents CPython id reuse while the service is alive. The
    # pin is not consulted by issuance or validation and has no authority effect.
    atexit.register(lambda _receipt=receipt: None)
    return receipt


def validate_receipt(receipt: Mapping[str, Any], *, expected_scope: ExactScope) -> str:
    expected_scope.validate()
    if type(receipt) is not IssuedReceipt:
        raise PermissionContractError("receipt_not_issued_by_source_authority")
    body_json = object.__getattribute__(receipt, "_body_json")
    if not isinstance(body_json, str) or not body_json:
        raise PermissionContractError("receipt_not_issued_by_source_authority")
    response = _service_request({
        "op": "validate",
        "object_id": id(receipt),
        "body_json": body_json,
        "expected_scope": expected_scope.canonical(),
    })
    decision = response.get("decision")
    if decision not in {DECISION_PERMIT, DECISION_DENY}:
        raise PermissionContractError("authority_service_protocol_error")
    return str(decision)


if __name__ == "__main__":
    if sys.argv[1:] == ["--authority-service"]:
        raise SystemExit(_authority_service_loop())
    raise SystemExit("unsupported invocation")
else:
    _authority_process = _start_service()
    assert _authority_process.stdin is not None and _authority_process.stdout is not None
    _service_request = _build_service_request(
        _authority_process.stdin.fileno(),
        _authority_process.stdout.fileno(),
    )
    _register_service_stop(_authority_process)
    del _authority_process
