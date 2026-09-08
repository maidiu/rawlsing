"""OBL058 CAUSAL_USE_PERMISSION R9 bounded repair candidate.

R9 preserves the frozen R8 native broker transport, the R7 native
object-generation/lifecycle mechanism, and the R6 semantic receipt law.  It
changes only native-core binding: an import-cache or loader-produced object is
accepted only when correctness-relevant module callables are genuine C
extension functions bound to that exact module object, the receipt base is the
expected extension type, and the loaded extension path is the exact
repository-built artifact for the frozen native sources.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import asdict, dataclass
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import sysconfig
import tempfile
from typing import Any

AUTHORITY_ID = "OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0"
SCHEMA_VERSION = "OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0"
FIXTURE_CLASS = "NONCURRENT_SYNTHETIC"
DECISION_PERMIT = "PERMIT"
DECISION_DENY = "DENY"
SOURCE_BASIS_KIND = "EXPLICIT_SOURCE_OWNED_CAUSAL_USE_PERMISSION"
NO_MATCHING_BASIS_KIND = "NO_MATCHING_SOURCE_OWNED_CAUSAL_USE_PERMISSION"
MECHANISM_REVISION = "OBL058_CAUSAL_USE_PERMISSION_NATIVE_BINDING_MECHANISM_R9@1.0.0"

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


def _receipt_integrity_payload(receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {
        k: receipt[k]
        for k in (
            "authority_id",
            "schema_version",
            "fixture_class",
            "scope",
            "scope_digest",
            "decision",
            "basis_kind",
            "basis_id",
            "basis_scope_digest",
            "basis_proof_digest",
            "authority_instance_id",
        )
    }


def receipt_digest(receipt: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        _canonical_json(_receipt_integrity_payload(receipt)).encode("utf-8")
    ).hexdigest()


_NATIVE_NAME = "_obl058_r8_native"
_NATIVE_REQUIRED_FUNCTIONS = (
    "start_broker",
    "shutdown_broker",
    "transport_configured",
    "close_success_count",
    "pin_count",
    "transport_success_count",
    "broker_pid",
    "broker_path",
)


def _native_source_paths() -> tuple[Path, ...]:
    source_path = Path(__file__).with_name("obl058_r8_native.c")
    return (
        source_path,
        source_path.with_name("obl058_r8_native_part1.inc"),
        source_path.with_name("obl058_r8_native_part2.inc"),
        source_path.with_name("obl058_r8_native_part3.inc"),
    )


def _native_output_path() -> Path:
    source_digest = hashlib.sha256(
        b"".join(path.read_bytes() for path in _native_source_paths())
    ).hexdigest()[:20]
    extension_suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
    build_root = Path(tempfile.gettempdir()) / "rawlsing_obl058_r8_native" / (
        f"py{sys.version_info.major}{sys.version_info.minor}"
    )
    build_root.mkdir(parents=True, exist_ok=True)
    return build_root / f"_obl058_r8_native_{source_digest}{extension_suffix}"


def _verify_native_module(module: object, expected_output: Path) -> object:
    """Accept only the exact C-extension module object used for authority.

    A Python module can imitate names and return values, but it cannot create a
    CPython built-in module function whose non-rebindable ``__self__`` is that
    same ordinary module object.  Requiring the correctness-relevant entry
    points to be genuine built-in functions bound to the candidate module makes
    a shape-compatible import-cache substitute fail closed.  Exact origin/file
    checks additionally bind the accepted extension to the repository-built
    artifact derived from the frozen native sources.
    """

    try:
        if module.__class__.__name__ != "module":
            raise ImportError("native_core_not_module")
        if module.__name__ != _NATIVE_NAME:
            raise ImportError("native_core_wrong_name")
        expected_text = str(expected_output.resolve())
        if str(Path(module.__file__).resolve()) != expected_text:
            raise ImportError("native_core_wrong_file")
        spec = module.__spec__
        if spec is None or str(Path(spec.origin).resolve()) != expected_text:
            raise ImportError("native_core_wrong_origin")

        builtin_bound_type = [].append.__class__
        for name in _NATIVE_REQUIRED_FUNCTIONS:
            function = module.__dict__[name]
            if function.__class__ is not builtin_bound_type:
                raise ImportError(f"native_core_nonbuiltin_entry:{name}")
            if function.__self__ is not module:
                raise ImportError(f"native_core_wrong_binding:{name}")

        receipt_base = module.__dict__["NativeReceiptBase"]
        if receipt_base.__class__ is not type:
            raise ImportError("native_core_receipt_base_not_type")
        if receipt_base.__module__ != _NATIVE_NAME:
            raise ImportError("native_core_receipt_base_wrong_module")
        method_descriptor_type = str.upper.__class__
        for name in (
            "_source_issue",
            "_source_validate",
            "_source_close",
            "_body_json_copy",
            "_is_source_issued",
        ):
            descriptor = receipt_base.__dict__[name]
            if descriptor.__class__ is not method_descriptor_type:
                raise ImportError(f"native_core_wrong_descriptor:{name}")
    except (AttributeError, KeyError, TypeError, ValueError, OSError) as exc:
        raise ImportError("native_core_source_origin_validation_failed") from exc
    return module


def _load_native_module():
    output_path = _native_output_path()
    existing = sys.modules.get(_NATIVE_NAME)
    if existing is not None:
        return _verify_native_module(existing, output_path)

    if not output_path.exists():
        linker = shlex.split(sysconfig.get_config_var("LDSHARED") or "cc -shared")
        include_dir = sysconfig.get_path("include")
        if not include_dir:
            raise ImportError("python_include_directory_unavailable")
        temporary_output = output_path.with_name(
            output_path.name + f".{os.getpid()}.tmp"
        )
        command = linker + [
            "-fPIC",
            "-O2",
            "-std=c11",
            f"-I{include_dir}",
            str(_native_source_paths()[0]),
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
                "native_broker_transport_core_build_failed:" + result.stderr[-4000:]
            )
        temporary_output.replace(output_path)

    # Do not place a loader-produced object in the import cache until its
    # C-extension origin/binding has been verified.
    spec = importlib.util.spec_from_file_location(_NATIVE_NAME, output_path)
    if spec is None or spec.loader is None:
        raise ImportError("native_broker_transport_core_load_spec_failed")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        verified = _verify_native_module(module, output_path)
    except Exception:
        if sys.modules.get(_NATIVE_NAME) is module:
            sys.modules.pop(_NATIVE_NAME, None)
        raise
    sys.modules[_NATIVE_NAME] = verified
    return verified


_native = _load_native_module()
_native.start_broker(
    str(Path(__file__).with_name("causal_use_permission_candidate_r6.py").resolve())
)


class IssuedReceipt(_native.NativeReceiptBase, Mapping[str, Any]):
    """Exact R9 source receipt using the verified R8 native core."""

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


def validate_receipt(
    receipt: Mapping[str, Any], *, expected_scope: ExactScope
) -> str:
    expected_scope.validate()
    if type(receipt) is not IssuedReceipt:
        raise PermissionContractError("receipt_not_issued_by_source_authority")
    try:
        result = receipt._source_validate(expected_scope.canonical())
    except Exception as exc:
        _raise_contract(exc)
    if type(result) is not tuple or len(result) != 2:
        raise PermissionContractError("authority_broker_protocol_error")
    decision, response_instance_id = result
    if decision not in {DECISION_PERMIT, DECISION_DENY}:
        raise PermissionContractError("authority_broker_protocol_error")
    body = receipt._public_body()
    if response_instance_id != body.get("authority_instance_id"):
        raise PermissionContractError("wrong_authority_instance")
    return str(decision)


# Read-only producer/reviewer observations. They do not expose or mutate the
# native generation key or broker transport configuration.
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
