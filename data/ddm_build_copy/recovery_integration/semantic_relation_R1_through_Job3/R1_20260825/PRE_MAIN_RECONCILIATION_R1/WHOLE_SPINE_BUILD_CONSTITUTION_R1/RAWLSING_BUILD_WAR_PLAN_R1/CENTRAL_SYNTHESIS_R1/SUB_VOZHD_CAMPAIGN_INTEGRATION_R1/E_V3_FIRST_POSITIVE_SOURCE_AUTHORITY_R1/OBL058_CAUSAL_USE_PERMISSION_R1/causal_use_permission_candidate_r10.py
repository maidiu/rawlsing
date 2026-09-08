"""OBL058 CAUSAL_USE_PERMISSION R10 bounded repair candidate.

R10 preserves the frozen R9 native source-origin binding and the established
native broker/lifecycle/semantic controls.  It changes only the final public
validation dispatch.  The public ``validate_receipt`` object is a verified C
extension function that holds the genuine native validation descriptor directly;
it does not look up ``_source_validate`` through the mutable Python receipt
class, instance, metaclass, module alias, or another Python callable at decision
time.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping
import hashlib
import importlib.util
import os
from pathlib import Path
import shlex
import subprocess
import sys
import sysconfig
import tempfile
from typing import Any

import causal_use_permission_candidate_r9 as _r9

AUTHORITY_ID = _r9.AUTHORITY_ID
SCHEMA_VERSION = _r9.SCHEMA_VERSION
FIXTURE_CLASS = _r9.FIXTURE_CLASS
DECISION_PERMIT = _r9.DECISION_PERMIT
DECISION_DENY = _r9.DECISION_DENY
SOURCE_BASIS_KIND = _r9.SOURCE_BASIS_KIND
NO_MATCHING_BASIS_KIND = _r9.NO_MATCHING_BASIS_KIND
PermissionContractError = _r9.PermissionContractError
ExactScope = _r9.ExactScope
REGISTERED_POSITIVE_SCOPE = _r9.REGISTERED_POSITIVE_SCOPE
REGISTERED_POSITIVE_BASIS_ID = _r9.REGISTERED_POSITIVE_BASIS_ID
scope_digest = _r9.scope_digest
receipt_digest = _r9.receipt_digest
_SCOPE_PREFIXES = _r9._SCOPE_PREFIXES
MECHANISM_REVISION = "OBL058_CAUSAL_USE_PERMISSION_PUBLIC_NATIVE_DISPATCH_R10@1.0.0"

_native = _r9._native
_NATIVE_NAME = _r9._NATIVE_NAME

_DISPATCH_NAME = "_obl058_r10_dispatch"
_DISPATCH_REQUIRED_FUNCTIONS = (
    "bind_contract",
    "public_validate",
    "bound_descriptor_identity",
)


def _dispatch_output_path() -> Path:
    source = Path(__file__).with_name("obl058_r10_dispatch.c")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:20]
    suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
    root = Path(tempfile.gettempdir()) / "rawlsing_obl058_r10_dispatch" / (
        f"py{sys.version_info.major}{sys.version_info.minor}"
    )
    root.mkdir(parents=True, exist_ok=True)
    return root / f"_obl058_r10_dispatch_{digest}{suffix}"


def _verify_dispatch_module(module: object, expected_output: Path) -> object:
    try:
        if module.__class__.__name__ != "module":
            raise ImportError("dispatch_not_module")
        if module.__name__ != _DISPATCH_NAME:
            raise ImportError("dispatch_wrong_name")
        expected = str(expected_output.resolve())
        if str(Path(module.__file__).resolve()) != expected:
            raise ImportError("dispatch_wrong_file")
        spec = module.__spec__
        if spec is None or str(Path(spec.origin).resolve()) != expected:
            raise ImportError("dispatch_wrong_origin")
        builtin_bound_type = [].append.__class__
        for name in _DISPATCH_REQUIRED_FUNCTIONS:
            fn = module.__dict__[name]
            if fn.__class__ is not builtin_bound_type:
                raise ImportError(f"dispatch_nonbuiltin_entry:{name}")
            if fn.__self__ is not module:
                raise ImportError(f"dispatch_wrong_binding:{name}")
    except (AttributeError, KeyError, TypeError, ValueError, OSError) as exc:
        raise ImportError("dispatch_source_origin_validation_failed") from exc
    return module


def _load_dispatch_module():
    output = _dispatch_output_path()
    existing = sys.modules.get(_DISPATCH_NAME)
    if existing is not None:
        return _verify_dispatch_module(existing, output)

    source = Path(__file__).with_name("obl058_r10_dispatch.c")
    if not output.exists():
        linker = shlex.split(sysconfig.get_config_var("LDSHARED") or "cc -shared")
        include_dir = sysconfig.get_path("include")
        if not include_dir:
            raise ImportError("python_include_directory_unavailable")
        temporary = output.with_name(output.name + f".{os.getpid()}.tmp")
        result = subprocess.run(
            linker
            + [
                "-fPIC",
                "-O2",
                "-std=c11",
                f"-I{include_dir}",
                str(source),
                "-o",
                str(temporary),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise ImportError(
                "native_public_dispatch_build_failed:" + result.stderr[-4000:]
            )
        temporary.replace(output)

    spec = importlib.util.spec_from_file_location(_DISPATCH_NAME, output)
    if spec is None or spec.loader is None:
        raise ImportError("native_public_dispatch_load_spec_failed")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        verified = _verify_dispatch_module(module, output)
    except Exception:
        if sys.modules.get(_DISPATCH_NAME) is module:
            sys.modules.pop(_DISPATCH_NAME, None)
        raise
    sys.modules[_DISPATCH_NAME] = verified
    return verified


class IssuedReceipt(_native.NativeReceiptBase, Mapping[str, Any]):
    """Exact R10 source receipt; decision dispatch is not a class lookup."""

    __slots__ = ()

    def _public_body(self) -> dict[str, Any]:
        # Public presentation only; validation does not call this method.
        import json

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
        except Exception:
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
        # Issuance remains source-owned by the verified R9 native base.  Even if
        # this Python method is later shadowed, the R10 public validator below
        # will accept only native-issued state.
        receipt._source_issue(scope.canonical(), basis_id, fixture_class)
    except Exception as exc:
        _raise_contract(exc)
    return receipt


_dispatch = _load_dispatch_module()
_dispatch.bind_contract(
    IssuedReceipt,
    ExactScope,
    PermissionContractError,
    _native.NativeReceiptBase,
)

# Crucial R10 boundary: expose the verified built-in function object itself.
# It directly invokes the native base's stored C descriptor and therefore does
# not consult IssuedReceipt._source_validate or any later module alias.
validate_receipt = _dispatch.public_validate


def native_lifetime_reservation_count() -> int:
    return int(_native.pin_count())


def native_successful_close_count() -> int:
    return int(_native.close_success_count())


def native_transport_success_count() -> int:
    return int(_native.transport_success_count())


def native_broker_pid() -> int:
    return int(_native.broker_pid())


def native_broker_socket_path() -> str:
    return str(_native.broker_path())


def native_public_dispatch_identity() -> int:
    return int(_dispatch.bound_descriptor_identity())
