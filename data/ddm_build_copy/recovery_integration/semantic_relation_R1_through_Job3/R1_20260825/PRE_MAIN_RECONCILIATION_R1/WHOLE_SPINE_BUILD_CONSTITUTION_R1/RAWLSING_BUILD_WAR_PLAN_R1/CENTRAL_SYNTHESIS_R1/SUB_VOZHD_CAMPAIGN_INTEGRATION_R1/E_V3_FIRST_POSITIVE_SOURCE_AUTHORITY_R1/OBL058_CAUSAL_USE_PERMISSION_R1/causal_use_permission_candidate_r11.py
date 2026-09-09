"""OBL058 CAUSAL_USE_PERMISSION R11 dispatch-capability redesign.

R11 preserves the verified R9 native source core and R10 native validation
semantics while redesigning establishment around one retained capability.
The exact C built-in objects authenticated from the capability module dictionary
are retained directly. The authenticated establish function returns the exact
public validation function from that same C-owned module dictionary, and the
returned object must be identical to the previously authenticated validator.
No later module/class/instance/descriptor/alias/import attribute lookup selects
the decision path.
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
MECHANISM_REVISION = "OBL058_CAUSAL_USE_PERMISSION_RETAINED_VALIDATION_CAPABILITY_R11@1.0.0"

_native = _r9._native
_NATIVE_NAME = _r9._NATIVE_NAME

_CAPABILITY_NAME = "_obl058_r11_dispatch_capability"
_CAPABILITY_ENTRIES = (
    "establish_capability",
    "public_validate",
    "bound_descriptor_identity",
)


def _capability_output_path() -> Path:
    source = Path(__file__).with_name("obl058_r11_dispatch_capability.c")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:20]
    suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
    root = Path(tempfile.gettempdir()) / "rawlsing_obl058_r11_capability" / (
        f"py{sys.version_info.major}{sys.version_info.minor}"
    )
    root.mkdir(parents=True, exist_ok=True)
    return root / f"_obl058_r11_dispatch_capability_{digest}{suffix}"


def _verify_and_capture_capability(module: object, expected_output: Path):
    """Authenticate and return the exact callable objects that will be used.

    Verification and later invocation intentionally share object identity.
    A module can mediate ordinary attribute access, but it cannot manufacture a
    CPython built-in function whose immutable ``__self__`` is the same module
    object. Only the exact built-ins found in the verified module dictionary are
    retained and used after this function returns.
    """

    try:
        if module.__class__.__name__ != "module":
            raise ImportError("validation_capability_not_module")
        if module.__name__ != _CAPABILITY_NAME:
            raise ImportError("validation_capability_wrong_name")
        expected = str(expected_output.resolve())
        if str(Path(module.__file__).resolve()) != expected:
            raise ImportError("validation_capability_wrong_file")
        spec = module.__spec__
        if spec is None or str(Path(spec.origin).resolve()) != expected:
            raise ImportError("validation_capability_wrong_origin")

        # The dictionary itself may be exposed through a customized module
        # class, but every accepted entry below must still be a genuine built-in
        # function non-rebindably bound to this exact module object. A mediated
        # dictionary containing substituted Python callables therefore rejects.
        raw = module.__dict__
        if type(raw) is not dict:
            raise ImportError("validation_capability_dictionary_required")
        builtin_bound_type = [].append.__class__
        captured = []
        for name in _CAPABILITY_ENTRIES:
            fn = raw[name]
            if fn.__class__ is not builtin_bound_type:
                raise ImportError(f"validation_capability_nonbuiltin_entry:{name}")
            if fn.__self__ is not module:
                raise ImportError(f"validation_capability_wrong_binding:{name}")
            captured.append(fn)
    except (AttributeError, KeyError, TypeError, ValueError, OSError) as exc:
        raise ImportError("validation_capability_source_origin_failed") from exc

    establish, public_validate, identity = captured
    return module, establish, public_validate, identity


def _load_and_capture_capability():
    output = _capability_output_path()
    existing = sys.modules.get(_CAPABILITY_NAME)
    if existing is not None:
        return _verify_and_capture_capability(existing, output)

    source = Path(__file__).with_name("obl058_r11_dispatch_capability.c")
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
                "retained_validation_capability_build_failed:" + result.stderr[-4000:]
            )
        temporary.replace(output)

    spec = importlib.util.spec_from_file_location(_CAPABILITY_NAME, output)
    if spec is None or spec.loader is None:
        raise ImportError("retained_validation_capability_load_spec_failed")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        bundle = _verify_and_capture_capability(module, output)
    except Exception:
        if sys.modules.get(_CAPABILITY_NAME) is module:
            sys.modules.pop(_CAPABILITY_NAME, None)
        raise
    sys.modules[_CAPABILITY_NAME] = module
    return bundle


class IssuedReceipt(_native.NativeReceiptBase, Mapping[str, Any]):
    """Exact R11 source receipt using the verified R9 native core."""

    __slots__ = ()

    def _public_body(self) -> dict[str, Any]:
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
        receipt._source_issue(scope.canonical(), basis_id, fixture_class)
    except Exception as exc:
        _raise_contract(exc)
    return receipt


(
    _capability_module,
    _establish_capability,
    _verified_public_validate,
    _descriptor_identity_capability,
) = _load_and_capture_capability()

# The exact authenticated establishment capability is called directly. It
# returns the exact public validator from the same C-owned module dictionary.
_retained_validation_capability = _establish_capability(
    IssuedReceipt,
    ExactScope,
    PermissionContractError,
    _native.NativeReceiptBase,
)
if _retained_validation_capability is not _verified_public_validate:
    raise ImportError("validation_capability_identity_mismatch")

# Public consumers receive the exact authenticated/retained capability object.
# No subsequent module attribute lookup selects the validation decision path.
validate_receipt = _retained_validation_capability


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


def retained_validation_capability_identity() -> int:
    return int(_descriptor_identity_capability())
