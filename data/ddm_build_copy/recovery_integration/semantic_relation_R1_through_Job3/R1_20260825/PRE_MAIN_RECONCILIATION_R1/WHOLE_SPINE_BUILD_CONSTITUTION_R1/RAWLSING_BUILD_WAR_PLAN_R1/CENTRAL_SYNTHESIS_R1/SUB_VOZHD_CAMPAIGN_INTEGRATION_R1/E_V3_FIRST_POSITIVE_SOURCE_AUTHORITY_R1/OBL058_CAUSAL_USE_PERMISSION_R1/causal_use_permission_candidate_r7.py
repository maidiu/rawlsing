"""OBL058 CAUSAL_USE_PERMISSION R7 mechanism-only bounded repair candidate.

R7 preserves the frozen R6 source decision, broker identity, requester-process
binding, source-basis law, scope law, and noncurrent-only boundary.  It changes
only object-generation lifetime handling: the broker key lives in a native
receipt field that is not a Python attribute, and each live issued generation is
held by a native C allocation until explicit source close or interpreter teardown.
No Python weak-reference/finalizer registry participates in correctness.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping
import hashlib
import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import sys
import sysconfig
import tempfile
from typing import Any

import causal_use_permission_candidate_r6 as _r6

AUTHORITY_ID = _r6.AUTHORITY_ID
SCHEMA_VERSION = _r6.SCHEMA_VERSION
FIXTURE_CLASS = _r6.FIXTURE_CLASS
DECISION_PERMIT = _r6.DECISION_PERMIT
DECISION_DENY = _r6.DECISION_DENY
SOURCE_BASIS_KIND = _r6.SOURCE_BASIS_KIND
NO_MATCHING_BASIS_KIND = _r6.NO_MATCHING_BASIS_KIND
PermissionContractError = _r6.PermissionContractError
ExactScope = _r6.ExactScope
REGISTERED_POSITIVE_SCOPE = _r6.REGISTERED_POSITIVE_SCOPE
REGISTERED_POSITIVE_BASIS_ID = _r6.REGISTERED_POSITIVE_BASIS_ID
scope_digest = _r6.scope_digest
receipt_digest = _r6.receipt_digest
MECHANISM_REVISION = "OBL058_CAUSAL_USE_PERMISSION_OBJECT_GENERATION_MECHANISM_R7@1.0.0"


def _load_native_module():
    name = "_obl058_r7_native"
    existing = sys.modules.get(name)
    if existing is not None:
        return existing

    source_path = Path(__file__).with_name("obl058_r7_native.c")
    source_bytes = source_path.read_bytes()
    source_digest = hashlib.sha256(source_bytes).hexdigest()[:20]
    extension_suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
    build_root = Path(tempfile.gettempdir()) / "rawlsing_obl058_r7_native" / (
        f"py{sys.version_info.major}{sys.version_info.minor}"
    )
    build_root.mkdir(parents=True, exist_ok=True)
    output_path = build_root / f"_obl058_r7_native_{source_digest}{extension_suffix}"

    if not output_path.exists():
        linker = shlex.split(sysconfig.get_config_var("LDSHARED") or "cc -shared")
        include_dir = sysconfig.get_path("include")
        if not include_dir:
            raise ImportError("python_include_directory_unavailable")
        temporary_output = output_path.with_name(output_path.name + ".tmp")
        command = linker + [
            "-fPIC",
            "-O2",
            "-std=c11",
            f"-I{include_dir}",
            str(source_path),
            "-o",
            str(temporary_output),
        ]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise ImportError(
                "native_object_generation_core_build_failed:"
                + result.stderr[-4000:]
            )
        temporary_output.replace(output_path)

    spec = importlib.util.spec_from_file_location(name, output_path)
    if spec is None or spec.loader is None:
        raise ImportError("native_object_generation_core_load_spec_failed")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


_native = _load_native_module()
_native.bind_broker(_r6._bound_broker_request)


class IssuedReceipt(_native.NativeReceiptBase, Mapping):
    """Exact R7 source receipt with a native, non-reassignable generation key."""

    __slots__ = ()

    def _public_body(self) -> dict[str, Any]:
        raw = self._body_json_copy()
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

    def close(self) -> bool:
        try:
            return bool(self._source_close())
        except PermissionContractError:
            return False


def _raise_contract(exc: Exception):
    if isinstance(exc, PermissionContractError):
        raise exc
    raise PermissionContractError(str(exc)) from exc


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
    try:
        receipt._source_issue(scope.canonical(), basis_id, fixture_class)
    except Exception as exc:
        _raise_contract(exc)
    return receipt


def validate_receipt(receipt: Mapping[str, Any], *, expected_scope: ExactScope) -> str:
    expected_scope.validate()
    if type(receipt) is not IssuedReceipt:
        raise PermissionContractError("receipt_not_issued_by_source_authority")
    try:
        decision = receipt._source_validate(expected_scope.canonical())
    except Exception as exc:
        _raise_contract(exc)
    if decision not in {DECISION_PERMIT, DECISION_DENY}:
        raise PermissionContractError("authority_broker_protocol_error")
    return str(decision)


# Non-authoritative producer/reviewer observations.  These expose counts only;
# neither function exposes, removes, replaces, or mutates a receipt generation.
def native_lifetime_reservation_count() -> int:
    return int(_native.pin_count())


def native_successful_close_count() -> int:
    return int(_native.close_success_count())
