"""OBL058 CAUSAL_USE_PERMISSION R6 bounded repair candidate.

R6 preserves the R5 one-shot source decision and broker binding while adding
requester-process generation to every authoritative broker record. Validation is
accepted only from the same OS-observed process generation that requested
issuance. Receipt records are retired by weak-reference finalization so a later
object generation cannot inherit a stale broker record merely by reusing a
process-local object address.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import asdict, dataclass
import atexit
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import uuid
import weakref
from typing import Any

AUTHORITY_ID = "OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0"
SCHEMA_VERSION = "OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0"
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
    actor_id="NONCURRENT_SYNTHETIC::actor::obl058-r6-a1",
    world_id="NONCURRENT_SYNTHETIC::world::obl058-r6-w1",
    subject_id="NONCURRENT_SYNTHETIC::subject::obl058-r6-s1",
    time_id="NONCURRENT_SYNTHETIC::time::obl058-r6-t1",
    transition_id="NONCURRENT_SYNTHETIC::transition::obl058-r6-tr1",
)
REGISTERED_POSITIVE_BASIS_ID = "NONCURRENT_SYNTHETIC::basis::obl058-r6-source-owned-permit-001"


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
        "basis_scope_digest", "basis_proof_digest", "authority_instance_id",
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


def _service_build_body(
    *, scope: dict[str, str], basis_id: str, fixture_class: str, authority_instance_id: str
) -> str:
    exact_scope = _service_validate_scope_dict(scope)
    if fixture_class != FIXTURE_CLASS:
        raise PermissionContractError("project_current_or_unknown_fixture_not_authorized")
    if not isinstance(basis_id, str) or not basis_id.strip():
        raise PermissionContractError("missing_basis_id")
    if not isinstance(authority_instance_id, str) or not authority_instance_id:
        raise PermissionContractError("service_protocol_error")

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
        "authority_instance_id": authority_instance_id,
    }
    body["receipt_digest"] = receipt_digest(body)
    return _canonical_json(body)


def _service_validate_body(*, body_json: str, expected_scope: dict[str, str]) -> tuple[str, str]:
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
        "basis_scope_digest", "basis_proof_digest", "authority_instance_id",
        "receipt_digest",
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
    if not isinstance(body["authority_instance_id"], str) or not body["authority_instance_id"]:
        raise PermissionContractError("wrong_authority_instance")

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
            "basis_scope_digest", "basis_proof_digest", "authority_instance_id",
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
    return str(body["decision"]), str(body["authority_instance_id"])


def _emit_line(stream, payload: dict[str, Any]) -> None:
    stream.write((_canonical_json(payload) + "\n").encode("utf-8"))
    stream.flush()


def _read_line(stream) -> dict[str, Any]:
    line = stream.readline()
    if not line:
        raise PermissionContractError("authority_service_unavailable")
    try:
        value = json.loads(line.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PermissionContractError("authority_service_protocol_error") from exc
    if type(value) is not dict:
        raise PermissionContractError("authority_service_protocol_error")
    return value


def _receipt_authority_service_loop_r6() -> int:
    """One-shot authority child for one exact broker-owned receipt record."""
    first = sys.stdin.buffer.readline()
    try:
        request = json.loads(first)
        if type(request) is not dict or set(request) != {
            "op", "object_id", "scope", "basis_id", "fixture_class", "request_id"
        } or request.get("op") != "initialize":
            raise PermissionContractError("service_protocol_error")
        request_id = request["request_id"]
        object_id = request["object_id"]
        if not isinstance(request_id, str) or not request_id:
            raise PermissionContractError("service_protocol_error")
        if not isinstance(object_id, int) or object_id <= 0:
            raise PermissionContractError("service_protocol_error")
        authority_instance_id = uuid.uuid4().hex
        authoritative_body = _service_build_body(
            scope=request["scope"],
            basis_id=request["basis_id"],
            fixture_class=request["fixture_class"],
            authority_instance_id=authority_instance_id,
        )
        _emit_line(sys.stdout.buffer, {
            "ok": True,
            "request_id": request_id,
            "body_json": authoritative_body,
            "authority_instance_id": authority_instance_id,
        })
    except PermissionContractError as exc:
        _emit_line(sys.stdout.buffer, {"ok": False, "error": str(exc)})
        return 1
    except Exception:
        _emit_line(sys.stdout.buffer, {"ok": False, "error": "service_internal_error"})
        return 1

    for raw in sys.stdin.buffer:
        request: dict[str, Any] | None = None
        try:
            request = json.loads(raw)
            if type(request) is not dict or set(request) != {
                "op", "object_id", "body_json", "expected_scope", "request_id"
            } or request.get("op") != "validate":
                raise PermissionContractError("service_protocol_error")
            request_id = request["request_id"]
            request_object_id = request["object_id"]
            if not isinstance(request_id, str) or not request_id:
                raise PermissionContractError("service_protocol_error")
            if not isinstance(request_object_id, int) or request_object_id <= 0:
                raise PermissionContractError("service_protocol_error")
            decision, body_instance_id = _service_validate_body(
                body_json=request["body_json"],
                expected_scope=request["expected_scope"],
            )
            if (
                request_object_id != object_id
                or request["body_json"] != authoritative_body
                or body_instance_id != authority_instance_id
            ):
                raise PermissionContractError("receipt_not_issued_by_source_authority")
            _emit_line(sys.stdout.buffer, {
                "ok": True,
                "request_id": request_id,
                "decision": decision,
                "authority_instance_id": authority_instance_id,
            })
        except PermissionContractError as exc:
            _emit_line(sys.stdout.buffer, {
                "ok": False,
                "request_id": request.get("request_id") if isinstance(request, dict) else None,
                "error": str(exc),
            })
        except Exception:
            _emit_line(sys.stdout.buffer, {
                "ok": False,
                "request_id": None,
                "error": "service_internal_error",
            })
    return 0


def _terminate_proc(proc: object) -> None:
    if not isinstance(proc, subprocess.Popen):
        return
    try:
        if proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=1)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def _child_roundtrip(
    proc: subprocess.Popen[bytes], request: dict[str, Any], *, expected_request_id: str
) -> dict[str, Any]:
    if proc.stdin is None or proc.stdout is None or proc.poll() is not None:
        raise PermissionContractError("authority_service_unavailable")
    _emit_line(proc.stdin, request)
    response = _read_line(proc.stdout)
    if response.get("request_id") != expected_request_id:
        raise PermissionContractError("authority_service_response_mismatch")
    if response.get("ok") is not True:
        raise PermissionContractError(str(response.get("error") or "authority_service_protocol_error"))
    return response


def _broker_start_child(
    *, object_id: int, scope: dict[str, str], basis_id: str, fixture_class: str
) -> tuple[subprocess.Popen[bytes], str, str]:
    path = str(Path(__file__).resolve())
    proc = subprocess.Popen(
        [sys.executable, "-S", path, "--receipt-authority-service-r6"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=False,
        bufsize=0,
    )
    request_id = uuid.uuid4().hex
    response = _child_roundtrip(proc, {
        "op": "initialize",
        "object_id": object_id,
        "scope": scope,
        "basis_id": basis_id,
        "fixture_class": fixture_class,
        "request_id": request_id,
    }, expected_request_id=request_id)
    body_json = response.get("body_json")
    authority_instance_id = response.get("authority_instance_id")
    if not isinstance(body_json, str) or not body_json:
        _terminate_proc(proc)
        raise PermissionContractError("authority_service_protocol_error")
    if not isinstance(authority_instance_id, str) or not authority_instance_id:
        _terminate_proc(proc)
        raise PermissionContractError("authority_service_protocol_error")
    return proc, body_json, authority_instance_id


def _broker_emit(conn: socket.socket, payload: dict[str, Any]) -> None:
    conn.sendall((_canonical_json(payload) + "\n").encode("utf-8"))


def _broker_read(conn: socket.socket) -> dict[str, Any]:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            raise PermissionContractError("broker_protocol_error")
        chunks.append(chunk)
        total += len(chunk)
        if total > 1_000_000:
            raise PermissionContractError("broker_protocol_error")
        if b"\n" in chunk:
            break
    raw = b"".join(chunks).split(b"\n", 1)[0]
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PermissionContractError("broker_protocol_error") from exc
    if type(value) is not dict:
        raise PermissionContractError("broker_protocol_error")
    return value


def _proc_starttime(pid: int) -> str:
    try:
        raw = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
        tail = raw.rsplit(") ", 1)[1].split()
        return tail[19]
    except Exception as exc:
        raise PermissionContractError("process_generation_unavailable") from exc


def _peer_identity(conn: socket.socket) -> tuple[int, int, str]:
    creds_raw = conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
    peer_pid, peer_uid, _peer_gid = struct.unpack("3i", creds_raw)
    return peer_pid, peer_uid, _proc_starttime(peer_pid)


def _broker_service_loop_r6(socket_path: str) -> int:
    """Own one-shot authority children and process/object-generation bindings."""
    records: dict[int, tuple[int, str, int, str, str, subprocess.Popen[bytes]]] = {}
    server: socket.socket | None = None
    try:
        try:
            os.unlink(socket_path)
        except FileNotFoundError:
            pass
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(socket_path)
        os.chmod(socket_path, 0o600)
        server.listen(64)
        while True:
            conn, _ = server.accept()
            with conn:
                request: dict[str, Any] | None = None
                request_id: str | None = None
                try:
                    peer_pid, peer_uid, peer_start = _peer_identity(conn)
                    request = _broker_read(conn)
                    request_id = request.get("request_id")
                    if not isinstance(request_id, str) or not request_id:
                        raise PermissionContractError("broker_protocol_error")
                    op = request.get("op")
                    if op == "ping":
                        if set(request) != {"op", "request_id"}:
                            raise PermissionContractError("broker_protocol_error")
                        _broker_emit(conn, {"ok": True, "request_id": request_id, "pong": True})
                        continue
                    if op == "issue":
                        if set(request) != {"op", "object_id", "scope", "basis_id", "fixture_class", "request_id"}:
                            raise PermissionContractError("broker_protocol_error")
                        object_id = request["object_id"]
                        if not isinstance(object_id, int) or object_id <= 0:
                            raise PermissionContractError("broker_protocol_error")
                        if object_id in records:
                            raise PermissionContractError("object_identity_already_issued")
                        proc, body_json, instance_id = _broker_start_child(
                            object_id=object_id,
                            scope=request["scope"],
                            basis_id=request["basis_id"],
                            fixture_class=request["fixture_class"],
                        )
                        records[object_id] = (peer_pid, peer_start, peer_uid, body_json, instance_id, proc)
                        _broker_emit(conn, {"ok": True, "request_id": request_id, "body_json": body_json, "authority_instance_id": instance_id})
                        continue
                    if op == "validate":
                        if set(request) != {"op", "object_id", "body_json", "expected_scope", "request_id"}:
                            raise PermissionContractError("broker_protocol_error")
                        object_id = request["object_id"]
                        if not isinstance(object_id, int) or object_id <= 0:
                            raise PermissionContractError("broker_protocol_error")
                        record = records.get(object_id)
                        if record is None:
                            raise PermissionContractError("receipt_not_issued_by_source_authority")
                        owner_pid, owner_start, owner_uid, authoritative_body, instance_id, proc = record
                        if peer_pid != owner_pid or peer_uid != owner_uid or peer_start != owner_start:
                            raise PermissionContractError("requester_process_generation_mismatch")
                        child_request_id = uuid.uuid4().hex
                        child_response = _child_roundtrip(proc, {
                            "op": "validate",
                            "object_id": object_id,
                            "body_json": request["body_json"],
                            "expected_scope": request["expected_scope"],
                            "request_id": child_request_id,
                        }, expected_request_id=child_request_id)
                        if child_response.get("authority_instance_id") != instance_id:
                            raise PermissionContractError("wrong_authority_instance")
                        decision = child_response.get("decision")
                        if decision not in {DECISION_PERMIT, DECISION_DENY}:
                            raise PermissionContractError("authority_service_protocol_error")
                        _broker_emit(conn, {"ok": True, "request_id": request_id, "decision": decision, "authority_instance_id": instance_id})
                        continue
                    if op == "close":
                        if set(request) != {"op", "object_id", "request_id"}:
                            raise PermissionContractError("broker_protocol_error")
                        object_id = request["object_id"]
                        record = records.get(object_id)
                        if record is None:
                            _broker_emit(conn, {"ok": True, "request_id": request_id, "closed": False})
                            continue
                        owner_pid, owner_start, owner_uid, _body, _instance, proc = record
                        if peer_pid != owner_pid or peer_uid != owner_uid or peer_start != owner_start:
                            raise PermissionContractError("requester_process_generation_mismatch")
                        records.pop(object_id, None)
                        _terminate_proc(proc)
                        _broker_emit(conn, {"ok": True, "request_id": request_id, "closed": True})
                        continue
                    raise PermissionContractError("broker_protocol_error")
                except PermissionContractError as exc:
                    _broker_emit(conn, {"ok": False, "request_id": request_id, "error": str(exc)})
                except Exception:
                    _broker_emit(conn, {"ok": False, "request_id": request_id, "error": "broker_internal_error"})
    finally:
        for record in records.values():
            _terminate_proc(record[5])
        if server is not None:
            try:
                server.close()
            except Exception:
                pass
        try:
            os.unlink(socket_path)
        except FileNotFoundError:
            pass
    return 0


def _raw_broker_request(socket_path: str, expected_pid: int, expected_starttime: str, expected_uid: int, request: dict[str, Any]) -> dict[str, Any]:
    if _proc_starttime(expected_pid) != expected_starttime:
        raise PermissionContractError("authority_broker_identity_mismatch")
    conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        conn.settimeout(30)
        conn.connect(socket_path)
        creds_raw = conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
        peer_pid, peer_uid, _peer_gid = struct.unpack("3i", creds_raw)
        if peer_pid != expected_pid or peer_uid != expected_uid:
            raise PermissionContractError("authority_broker_identity_mismatch")
        _broker_emit(conn, request)
        response = _broker_read(conn)
    except (OSError, TimeoutError) as exc:
        raise PermissionContractError("authority_broker_unavailable") from exc
    finally:
        conn.close()
    if response.get("request_id") != request.get("request_id"):
        raise PermissionContractError("authority_broker_response_mismatch")
    if response.get("ok") is not True:
        raise PermissionContractError(str(response.get("error") or "authority_broker_protocol_error"))
    return response


def _start_broker() -> tuple[subprocess.Popen[bytes], str, str, str]:
    directory = tempfile.mkdtemp(prefix="obl058-r6-broker-")
    socket_path = str(Path(directory) / "authority.sock")
    proc = subprocess.Popen([sys.executable, "-S", str(Path(__file__).resolve()), "--broker-service-r6", socket_path], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=False, close_fds=True)
    starttime = _proc_starttime(proc.pid)
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            shutil.rmtree(directory, ignore_errors=True)
            raise PermissionContractError("authority_broker_unavailable")
        if os.path.exists(socket_path):
            try:
                request_id = uuid.uuid4().hex
                response = _raw_broker_request(socket_path, proc.pid, starttime, os.getuid(), {"op": "ping", "request_id": request_id})
                if response.get("pong") is True:
                    return proc, socket_path, directory, starttime
            except PermissionContractError:
                pass
        time.sleep(0.01)
    _terminate_proc(proc)
    shutil.rmtree(directory, ignore_errors=True)
    raise PermissionContractError("authority_broker_unavailable")


def _cleanup_broker(proc: subprocess.Popen[bytes], directory: str) -> None:
    _terminate_proc(proc)
    shutil.rmtree(directory, ignore_errors=True)


def _build_bound_broker_request(socket_path: str, broker_pid: int, broker_starttime: str, broker_uid: int):
    namespace: dict[str, Any] = {}
    source = (
        "def bound_broker_request(request):\n"
        "    _json = __import__('json')\n"
        "    _socket = __import__('socket')\n"
        "    _struct = __import__('struct')\n"
        f"    _path = {socket_path!r}\n"
        f"    _pid = {broker_pid!r}\n"
        f"    _start = {broker_starttime!r}\n"
        f"    _uid = {broker_uid!r}\n"
        "    try:\n"
        "        _raw_stat = open('/proc/%d/stat' % _pid, 'r', encoding='utf-8').read()\n"
        "        _tail = _raw_stat.rsplit(') ', 1)[1].split()\n"
        "        if _tail[19] != _start:\n"
        "            raise PermissionContractError('authority_broker_identity_mismatch')\n"
        "    except PermissionContractError:\n"
        "        raise\n"
        "    except Exception as _exc:\n"
        "        raise PermissionContractError('authority_broker_identity_unavailable') from _exc\n"
        "    _conn = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)\n"
        "    try:\n"
        "        _conn.settimeout(30)\n"
        "        _conn.connect(_path)\n"
        "        _creds = _conn.getsockopt(_socket.SOL_SOCKET, _socket.SO_PEERCRED, _struct.calcsize('3i'))\n"
        "        _peer_pid, _peer_uid, _peer_gid = _struct.unpack('3i', _creds)\n"
        "        if _peer_pid != _pid or _peer_uid != _uid:\n"
        "            raise PermissionContractError('authority_broker_identity_mismatch')\n"
        "        _wire = (_json.dumps(request, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\\n').encode('utf-8')\n"
        "        _conn.sendall(_wire)\n"
        "        _chunks = []\n"
        "        _total = 0\n"
        "        while True:\n"
        "            _chunk = _conn.recv(4096)\n"
        "            if not _chunk:\n"
        "                raise OSError('broker eof')\n"
        "            _chunks.append(_chunk)\n"
        "            _total += len(_chunk)\n"
        "            if _total > 1000000:\n"
        "                raise OSError('broker response too large')\n"
        "            if b'\\n' in _chunk:\n"
        "                break\n"
        "        _response = _json.loads(b''.join(_chunks).split(b'\\n', 1)[0].decode('utf-8'))\n"
        "    except PermissionContractError:\n"
        "        raise\n"
        "    except Exception as _exc:\n"
        "        raise PermissionContractError('authority_broker_unavailable') from _exc\n"
        "    finally:\n"
        "        _conn.close()\n"
        "    if type(_response) is not dict or _response.get('request_id') != request.get('request_id'):\n"
        "        raise PermissionContractError('authority_broker_response_mismatch')\n"
        "    if _response.get('ok') is not True:\n"
        "        raise PermissionContractError(str(_response.get('error') or 'authority_broker_protocol_error'))\n"
        "    return _response\n"
    )
    exec(source, globals(), namespace)
    return namespace["bound_broker_request"]


class IssuedReceipt(Mapping[str, Any]):
    __slots__ = ("_body_json", "__weakref__")

    def __init__(self) -> None:
        object.__setattr__(self, "_body_json", "")

    def _public_body(self) -> dict[str, Any]:
        try:
            raw = object.__getattribute__(self, "_body_json")
        except AttributeError as exc:
            raise PermissionContractError("receipt_not_issued_by_source_authority") from exc
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

    def close(self) -> None:
        _close_record(id(self))


def _close_record(object_id: int) -> None:
    try:
        request_id = uuid.uuid4().hex
        _bound_broker_request({"op": "close", "object_id": object_id, "request_id": request_id})
    except PermissionContractError:
        pass


def _finalize_receipt_record(object_id: int) -> None:
    _close_record(object_id)


def issue_noncurrent_synthetic_receipt(*, scope: ExactScope, basis_id: str, fixture_class: str = FIXTURE_CLASS) -> Mapping[str, Any]:
    scope.validate()
    if fixture_class != FIXTURE_CLASS:
        raise PermissionContractError("project_current_or_unknown_fixture_not_authorized")
    if not isinstance(basis_id, str) or not basis_id.strip():
        raise PermissionContractError("missing_basis_id")
    receipt = IssuedReceipt()
    request_id = uuid.uuid4().hex
    response = _bound_broker_request({"op": "issue", "object_id": id(receipt), "scope": scope.canonical(), "basis_id": basis_id, "fixture_class": fixture_class, "request_id": request_id})
    body_json = response.get("body_json")
    if not isinstance(body_json, str) or not body_json:
        raise PermissionContractError("authority_broker_protocol_error")
    object.__setattr__(receipt, "_body_json", body_json)
    weakref.finalize(receipt, _finalize_receipt_record, id(receipt))
    return receipt


def _build_bound_validator(socket_path: str, broker_pid: int, broker_starttime: str, broker_uid: int):
    namespace: dict[str, Any] = {}
    source = (
        "def bound_validate_receipt(receipt, *, expected_scope):\n"
        "    expected_scope.validate()\n"
        "    if type(receipt) is not IssuedReceipt:\n"
        "        raise PermissionContractError('receipt_not_issued_by_source_authority')\n"
        "    try:\n"
        "        _body_json = object.__getattribute__(receipt, '_body_json')\n"
        "    except AttributeError as _exc:\n"
        "        raise PermissionContractError('receipt_not_issued_by_source_authority') from _exc\n"
        "    if not isinstance(_body_json, str) or not _body_json:\n"
        "        raise PermissionContractError('receipt_not_issued_by_source_authority')\n"
        "    _json = __import__('json')\n"
        "    _socket = __import__('socket')\n"
        "    _struct = __import__('struct')\n"
        "    _uuid = __import__('uuid')\n"
        f"    _path = {socket_path!r}\n"
        f"    _pid = {broker_pid!r}\n"
        f"    _start = {broker_starttime!r}\n"
        f"    _uid = {broker_uid!r}\n"
        "    try:\n"
        "        _raw_stat = open('/proc/%d/stat' % _pid, 'r', encoding='utf-8').read()\n"
        "        _tail = _raw_stat.rsplit(') ', 1)[1].split()\n"
        "        if _tail[19] != _start:\n"
        "            raise PermissionContractError('authority_broker_identity_mismatch')\n"
        "    except PermissionContractError:\n"
        "        raise\n"
        "    except Exception as _exc:\n"
        "        raise PermissionContractError('authority_broker_identity_unavailable') from _exc\n"
        "    _conn = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)\n"
        "    try:\n"
        "        _conn.settimeout(30)\n"
        "        _conn.connect(_path)\n"
        "        _creds = _conn.getsockopt(_socket.SOL_SOCKET, _socket.SO_PEERCRED, _struct.calcsize('3i'))\n"
        "        _peer_pid, _peer_uid, _peer_gid = _struct.unpack('3i', _creds)\n"
        "        if _peer_pid != _pid or _peer_uid != _uid:\n"
        "            raise PermissionContractError('authority_broker_identity_mismatch')\n"
        "        _request_id = _uuid.uuid4().hex\n"
        "        _request = {'op':'validate','object_id':id(receipt),'body_json':_body_json,'expected_scope':expected_scope.canonical(),'request_id':_request_id}\n"
        "        _conn.sendall((_json.dumps(_request, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\\n').encode('utf-8'))\n"
        "        _chunks = []\n"
        "        _total = 0\n"
        "        while True:\n"
        "            _chunk = _conn.recv(4096)\n"
        "            if not _chunk:\n"
        "                raise OSError('broker eof')\n"
        "            _chunks.append(_chunk)\n"
        "            _total += len(_chunk)\n"
        "            if _total > 1000000:\n"
        "                raise OSError('broker response too large')\n"
        "            if b'\\n' in _chunk:\n"
        "                break\n"
        "        _response = _json.loads(b''.join(_chunks).split(b'\\n', 1)[0].decode('utf-8'))\n"
        "    except PermissionContractError:\n"
        "        raise\n"
        "    except Exception as _exc:\n"
        "        raise PermissionContractError('authority_broker_unavailable') from _exc\n"
        "    finally:\n"
        "        _conn.close()\n"
        "    if type(_response) is not dict or _response.get('request_id') != _request_id:\n"
        "        raise PermissionContractError('authority_broker_response_mismatch')\n"
        "    if _response.get('ok') is not True:\n"
        "        raise PermissionContractError(str(_response.get('error') or 'authority_broker_protocol_error'))\n"
        "    _decision = _response.get('decision')\n"
        "    if _decision not in {DECISION_PERMIT, DECISION_DENY}:\n"
        "        raise PermissionContractError('authority_broker_protocol_error')\n"
        "    try:\n"
        "        _body = _json.loads(_body_json)\n"
        "    except Exception as _exc:\n"
        "        raise PermissionContractError('malformed_receipt_body') from _exc\n"
        "    if type(_body) is not dict or _response.get('authority_instance_id') != _body.get('authority_instance_id'):\n"
        "        raise PermissionContractError('wrong_authority_instance')\n"
        "    return str(_decision)\n"
    )
    exec(source, globals(), namespace)
    return namespace["bound_validate_receipt"]


if __name__ == "__main__":
    if sys.argv[1:] == ["--receipt-authority-service-r6"]:
        raise SystemExit(_receipt_authority_service_loop_r6())
    if len(sys.argv) == 3 and sys.argv[1] == "--broker-service-r6":
        raise SystemExit(_broker_service_loop_r6(sys.argv[2]))
    raise SystemExit("unsupported invocation")
else:
    _broker_proc, _broker_socket_path, _broker_dir, _broker_start = _start_broker()
    _bound_broker_request = _build_bound_broker_request(_broker_socket_path, _broker_proc.pid, _broker_start, os.getuid())
    validate_receipt = _build_bound_validator(_broker_socket_path, _broker_proc.pid, _broker_start, os.getuid())
    atexit.register(_cleanup_broker, _broker_proc, _broker_dir)
    del _broker_proc
    del _broker_socket_path
    del _broker_dir
    del _broker_start
