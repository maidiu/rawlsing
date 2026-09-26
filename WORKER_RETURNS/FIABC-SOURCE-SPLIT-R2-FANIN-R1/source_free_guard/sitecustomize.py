"""Audit and block raw-source or measured-candidate actions during qualification."""
from __future__ import annotations

import atexit
import builtins
import hashlib
import json
import os
from pathlib import Path
import sys
import time


_telemetry_dir = os.environ.get("FIABC_ZERO_EXECUTION_TELEMETRY_DIR")
_counts = {
    "raw_source_open_attempts": 0,
    "raw_source_hash_sha_attempts": 0,
    "decoder_calls": 0,
    "candidate_process_launch_attempts": 0,
    "synthetic_process_envelope_probe_launches": 0,
    "measured_p2x_launch_attempts": 0,
}
_violations: list[str] = []
_source_suffixes = (".dta", ".sav", ".zsav", ".por", ".sas7bdat")
_candidate_module = "rawlsing_next.ee_p2x_candidate_process_envelope"
_measured_targets = {
    "FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py",
    "RUN_FIABC_SOURCE_LOCAL_SPLIT.sh",
    "ee_p2x_darwin_court_driver.py",
    "rawlsing_next.ee_p2x_darwin_court_driver",
}


def _path_text(value: object) -> str:
    try:
        return os.fsdecode(os.fspath(value))
    except (TypeError, ValueError):
        return str(value)


def _raw_source_path(value: object) -> bool:
    path = _path_text(value).lower()
    return path.endswith(_source_suffixes)


def _argv(args: tuple[object, ...]) -> list[str]:
    if len(args) < 2 or not isinstance(args[1], (list, tuple)):
        return []
    return [_path_text(item) for item in args[1]]


def _candidate_attempt(args: tuple[object, ...]) -> bool:
    argv = _argv(args)
    if _candidate_module not in argv or "--child" not in argv:
        return False
    env = args[3] if len(args) > 3 and isinstance(args[3], dict) else {}
    candidate = env.get("RAWLSING_EE_P2X_CELL_CANDIDATE")
    if candidate not in {"A", "B", "C"}:
        return False
    try:
        mode = argv[argv.index("--context-mode") + 1]
        backend = Path(argv[argv.index("--backend-spec") + 1]).name
    except (ValueError, IndexError):
        return True
    if mode == "SIMPLE_TEST_ONLY" and backend == "fiabc_i06a_process_probe_backend.py":
        _counts["synthetic_process_envelope_probe_launches"] += 1
        return False
    return True


def _measured_attempt(args: tuple[object, ...]) -> bool:
    argv = _argv(args)
    if "--run" not in argv:
        return False
    return any(Path(token).name in _measured_targets or token in _measured_targets for token in argv)


def _audit(event: str, args: tuple[object, ...]) -> None:
    if event == "open" and args and _raw_source_path(args[0]):
        _counts["raw_source_open_attempts"] += 1
        _violations.append("raw-source open blocked")
        raise PermissionError("source-free qualification blocks raw survey opens")
    if event in ("subprocess.Popen", "os.exec", "os.posix_spawn"):
        if _measured_attempt(args):
            _counts["measured_p2x_launch_attempts"] += 1
            _violations.append("measured P2X launch blocked")
            raise PermissionError("source-free qualification blocks measured P2X")
        if _candidate_attempt(args):
            _counts["candidate_process_launch_attempts"] += 1
            _violations.append("candidate-process launch blocked")
            raise PermissionError("source-free qualification blocks candidate launch")


sys.addaudithook(_audit)


def _guard_decoder(module: object, names: tuple[str, ...]) -> None:
    for name in names:
        decoder = getattr(module, name, None)
        if not callable(decoder) or getattr(decoder, "_fiabc_guarded", False):
            continue

        def blocked(*args: object, __name: str = name, **kwargs: object) -> object:
            _counts["decoder_calls"] += 1
            _violations.append(f"decoder call blocked: {__name}")
            raise PermissionError("source-free qualification blocks survey decoding")

        blocked._fiabc_guarded = True  # type: ignore[attr-defined]
        setattr(module, name, blocked)


_original_import = builtins.__import__


def _guarded_import(name: str, globals=None, locals=None, fromlist=(), level=0):
    if name == "pyreadstat" or name.startswith("pyreadstat."):
        _original_import("pyreadstat", globals, locals, (), level)
        root = sys.modules.get("pyreadstat")
        if root is not None:
            _guard_decoder(
                root,
                (
                    "read_dta",
                    "read_sav",
                    "read_sas7bdat",
                    "read_por",
                    "read_xport",
                    "read_file_in_chunks",
                    "read_file_multiprocessing",
                ),
            )
        return _original_import(name, globals, locals, fromlist, level)
    if name == "pandas" or name.startswith("pandas."):
        _original_import("pandas", globals, locals, (), level)
        root = sys.modules.get("pandas")
        if root is not None:
            _guard_decoder(root, ("read_stata", "read_spss", "read_sas"))
        return _original_import(name, globals, locals, fromlist, level)
    return _original_import(name, globals, locals, fromlist, level)


builtins.__import__ = _guarded_import


_original_file_digest = hashlib.file_digest


def _guarded_file_digest(fileobj, digest, /, *, _bufsize=2**18):
    if _raw_source_path(getattr(fileobj, "name", "")):
        _counts["raw_source_hash_sha_attempts"] += 1
        _violations.append("raw-source hash/SHA blocked")
        raise PermissionError("source-free qualification blocks raw survey hashing")
    return _original_file_digest(fileobj, digest, _bufsize=_bufsize)


hashlib.file_digest = _guarded_file_digest


def _write_telemetry() -> None:
    if not _telemetry_dir:
        return
    directory = Path(_telemetry_dir)
    directory.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "RAWLSING_FIABC_SOURCE_FREE_ZERO_EXECUTION_PROCESS_TELEMETRY@1.0.0",
        "pid": os.getpid(),
        "python_executable": sys.executable,
        "python_version": sys.version.split()[0],
        "started_unix_ns": time.time_ns(),
        "counts": dict(_counts),
        "violations": list(_violations),
    }
    target = directory / f"process-{os.getpid()}.json"
    target.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")


atexit.register(_write_telemetry)
