#!/usr/bin/env python3
"""Source-free gates for FIABC source-split R2 work-root equivalence.

This module is control-plane only.  It must never open/hash/decode a raw LiTS
or WVS source and must never import or launch a candidate backend.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Mapping, Sequence

EXPECTED_EXECUTION_BRANCH = "agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"
EXPECTED_EXECUTION_HEAD = "3d8f2ad62600b6777dcb23a28404a067502e77a0"
OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
LIVE_EVIDENCE_REL = Path("WORKER_RETURNS/EE-P2X/LOCAL_COURT")
BASELINE_SCHEMA = "RAWLSING_FIABC_SPLIT_R2_REPO_PRESTATE_BASELINE@1.0.0"
POSTRUN_SCHEMA = "RAWLSING_FIABC_SPLIT_R2_POSTRUN_CHECKOUT_VERIFICATION@1.0.0"
PRESTATE_SCHEMA = "RAWLSING_FIABC_SPLIT_R2_JOINED_PRESTATE@1.0.0"
READINESS_SCHEMA = "RAWLSING_FIABC_SPLIT_R2_MACHINE_READINESS@1.0.0"
PAIR_SCHEMA = "RAWLSING_FIABC_SPLIT_R2_PAIR_COMPATIBILITY@1.0.0"

SOURCE_SHA256 = {
    "LITS_I": "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09",
    "WVS7": "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d",
}
EXPECTED_RUNTIME = {
    "implementation": "CPython",
    "python": "3.11.3",
    "pyreadstat": "1.3.6",
    "pyarrow": "25.0.1",
    "pandas": "2.3.1",
    "numpy": "2.3.2",
    "system": "Darwin",
    "machine": "x86_64",
}
R5_SUPPORT = {
    "rawlsing_next/pre553_r5_codec.py": {
        "blob": "72f8f3c03ed065e86fea4e76bb17f8e06c2bf540",
        "protected_checkout": "PRESENT",
    },
    "rawlsing_next/pre553_r5_compact_carrier.py": {
        "blob": "92e364b31eaf27be1bca2081eff65f6ffb779c3d",
        "protected_checkout": "ABSENT",
    },
    "rawlsing_next/pre553_r5_model.py": {
        "blob": "62ce608829c3d9c2fb7c999aefe40188637edf80",
        "protected_checkout": "ABSENT",
    },
    "rawlsing_next/pre553_r5_seam.py": {
        "blob": "cef326ebbc40468428378f7fdbe76e4756179f39",
        "protected_checkout": "ABSENT",
    },
    "rawlsing_next/pre553_r5_single_pass_audit69.py": {
        "blob": "ffb063b93c86e215604eecb29a9545c7efdff399",
        "protected_checkout": "ABSENT",
    },
}
OWNER_SPECS = {
    "A": {
        "path": "rawlsing_next/pre553_r5_source_backed_adapter.py",
        "blob": "d4915e7e6755ba1850756aebff72f982f73a332b",
    },
    "B": {
        "path": "rawlsing_next/pre553_source_backed_c11_facade.py",
        "blob": "7c509c2098d0030f253344eb3f682471378812a8",
    },
    "C": {
        "path": "rawlsing_next/pre553_route_c_accelerators.py",
        "blob": "abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889",
    },
}
FORBIDDEN_PREPROVISION_ROOTS = (
    "_be1_lits_projection",
    "_lits_common_representation",
    "cells",
)
ALLOWED_PRESTATE_ROOTS = (
    "_be1_immutable",
    "_exact_owner_modules",
)


class SplitR2GateError(RuntimeError):
    pass


def _canon(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
    ).encode("utf-8")


def _semantic_hash(value: Any) -> str:
    return hashlib.sha256(_canon(value)).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    tmp = path.with_name("." + path.name + ".tmp")
    tmp.write_text(body, encoding="utf-8")
    os.replace(tmp, path)


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _git_text(root: Path, *args: str, check: bool = True) -> str:
    return _git(root, *args, check=check).stdout.decode("utf-8", "surrogateescape").strip()


def _git_show_bytes(root: Path, commit: str, path: str) -> bytes:
    proc = _git(root, "show", f"{commit}:{path}", check=False)
    if proc.returncode:
        raise SplitR2GateError(
            f"immutable prestate object unavailable: {commit}:{path}"
        )
    return proc.stdout


def _sysctl(name: str) -> str | None:
    proc = subprocess.run(
        ["sysctl", "-n", name],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    value = proc.stdout.strip()
    return value or None


def exact_repo_identity(repo_root: Path) -> Mapping[str, str]:
    root = repo_root.resolve()
    branch = _git_text(root, "branch", "--show-current")
    head = _git_text(root, "rev-parse", "--verify", "HEAD^{commit}")
    if branch != EXPECTED_EXECUTION_BRANCH:
        raise SplitR2GateError(
            f"execution branch drift: expected {EXPECTED_EXECUTION_BRANCH}, got {branch}"
        )
    if head != EXPECTED_EXECUTION_HEAD:
        raise SplitR2GateError(
            f"execution head drift: expected {EXPECTED_EXECUTION_HEAD}, got {head}"
        )
    return {"branch": branch, "head": head}


def worktree_lock_root(repo_root: Path) -> Path:
    """Return the exact Git-worktree administrative directory.

    Linked worktrees have a .git *file*.  Using the worktree's resolved Git
    administrative directory keeps the lock independent of external WORK_ROOT.
    """
    root = repo_root.resolve()
    proc = _git(root, "rev-parse", "--path-format=absolute", "--git-dir", check=False)
    if proc.returncode == 0:
        raw = proc.stdout.decode("utf-8", "surrogateescape").strip()
        if raw:
            return Path(raw).resolve()
    raw = _git_text(root, "rev-parse", "--git-dir")
    p = Path(raw)
    if not p.is_absolute():
        p = root / p
    return p.resolve()


def combined_import_abi_gate() -> Mapping[str, Any]:
    """Import all pinned scientific packages in one interpreter, then verify metadata."""
    imported = {}
    for name in ("pyreadstat", "pyarrow", "pandas", "numpy"):
        try:
            module = importlib.import_module(name)
        except Exception as exc:
            raise SplitR2GateError(
                f"combined import/ABI gate failed importing {name}: {type(exc).__name__}: {exc}"
            ) from exc
        imported[name] = {
            "module": getattr(module, "__name__", name),
            "module_version": getattr(module, "__version__", None),
        }
    observed = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "pyreadstat": importlib.metadata.version("pyreadstat"),
        "pyarrow": importlib.metadata.version("pyarrow"),
        "pandas": importlib.metadata.version("pandas"),
        "numpy": importlib.metadata.version("numpy"),
        "system": platform.system(),
        "machine": platform.machine(),
    }
    if observed != EXPECTED_RUNTIME:
        raise SplitR2GateError(
            f"runtime mismatch: expected={EXPECTED_RUNTIME!r} observed={observed!r}"
        )
    return {
        "status": "PASS",
        "observed": observed,
        "combined_imports": imported,
        "single_interpreter": True,
    }


def _hardware() -> Mapping[str, Any]:
    mem = _sysctl("hw.memsize")
    return {
        "hardware_model": _sysctl("hw.model"),
        "cpu_brand": _sysctl("machdep.cpu.brand_string"),
        "memory_bytes": int(mem) if mem and mem.isdigit() else None,
        "architecture": platform.machine(),
        "macos_version": platform.mac_ver()[0] or None,
    }


def _assert_fresh_work_root(work_root: Path) -> Mapping[str, Any]:
    root = work_root.resolve()
    if root.is_symlink():
        raise SplitR2GateError("WORK_ROOT may not be a symlink")
    if root.exists():
        entries = sorted(p.name for p in root.iterdir())
        if entries:
            raise SplitR2GateError(
                f"machine readiness requires a fresh empty WORK_ROOT: {root}: {entries}"
            )
        state = "EXISTS_EMPTY"
    else:
        state = "ABSENT"
    return {"path": str(root), "state": state, "fresh": True}


def machine_readiness(
    *,
    source: str,
    repo_root: Path,
    work_root: Path,
    control_root: Path,
    qualified_control_head: str,
    launcher_path: Path,
    driver_path: Path,
    helper_path: Path,
) -> Mapping[str, Any]:
    if source not in SOURCE_SHA256:
        raise SplitR2GateError(f"unknown source assignment: {source}")
    repo = exact_repo_identity(repo_root)
    runtime = combined_import_abi_gate()
    control_root = control_root.resolve()
    control_head = _git_text(control_root, "rev-parse", "--verify", "HEAD^{commit}")
    if control_head != qualified_control_head:
        raise SplitR2GateError(
            f"unqualified split-control head: expected {qualified_control_head}, got {control_head}"
        )
    fresh = _assert_fresh_work_root(work_root)
    payload = {
        "schema": READINESS_SCHEMA,
        "status": "PASS",
        "assigned_source": source,
        "canonical_source_sha256": SOURCE_SHA256[source],
        "source_bytes_opened": 0,
        "source_hash_passes": 0,
        "decoder_calls": 0,
        "candidate_process_launches": 0,
        "fresh_work_root": fresh,
        "protected_execution": repo,
        "qualified_control": {
            "head": control_head,
            "launcher_sha256": _sha256_file(launcher_path.resolve()),
            "driver_sha256": _sha256_file(driver_path.resolve()),
            "workroot_gates_sha256": _sha256_file(helper_path.resolve()),
        },
        "runtime": runtime["observed"],
        "combined_import_gate": runtime,
        "hardware": _hardware(),
    }
    payload["receipt_identity"] = _semantic_hash(payload)
    return payload


def _verify_self_identity(doc: Mapping[str, Any], schema: str) -> None:
    if doc.get("schema") != schema:
        raise SplitR2GateError(f"receipt schema mismatch: expected {schema}")
    expected = doc.get("receipt_identity")
    material = {k: v for k, v in doc.items() if k != "receipt_identity"}
    got = _semantic_hash(material)
    if expected != got:
        raise SplitR2GateError(f"receipt identity drift for {schema}")


def pair_compatibility(lits: Mapping[str, Any], wvs: Mapping[str, Any]) -> Mapping[str, Any]:
    for doc in (lits, wvs):
        _verify_self_identity(doc, READINESS_SCHEMA)
        if doc.get("status") != "PASS":
            raise SplitR2GateError("machine readiness is not PASS")
        if doc.get("source_bytes_opened") != 0 or doc.get("source_hash_passes") != 0:
            raise SplitR2GateError("machine readiness touched raw source")
        if doc.get("decoder_calls") != 0 or doc.get("candidate_process_launches") != 0:
            raise SplitR2GateError("machine readiness crossed source/candidate boundary")
    by_source = {lits.get("assigned_source"): lits, wvs.get("assigned_source"): wvs}
    if set(by_source) != {"LITS_I", "WVS7"}:
        raise SplitR2GateError("pair readiness must contain exactly LITS_I and WVS7 assignments")
    for source, doc in by_source.items():
        if doc.get("canonical_source_sha256") != SOURCE_SHA256[source]:
            raise SplitR2GateError(f"canonical source identity drift in {source} readiness")
        if not doc.get("fresh_work_root", {}).get("fresh"):
            raise SplitR2GateError(f"{source} readiness lacks fresh work-root proof")

    left, right = by_source["LITS_I"], by_source["WVS7"]
    exact_fields = {
        "runtime": left.get("runtime") == right.get("runtime"),
        "protected_execution": left.get("protected_execution") == right.get("protected_execution"),
        "qualified_control": left.get("qualified_control") == right.get("qualified_control"),
        "hardware_model": left.get("hardware", {}).get("hardware_model") == right.get("hardware", {}).get("hardware_model"),
        "cpu_brand": left.get("hardware", {}).get("cpu_brand") == right.get("hardware", {}).get("cpu_brand"),
        "memory_bytes": left.get("hardware", {}).get("memory_bytes") == right.get("hardware", {}).get("memory_bytes"),
        "architecture": left.get("hardware", {}).get("architecture") == right.get("hardware", {}).get("architecture"),
    }
    bad = sorted(k for k, ok in exact_fields.items() if not ok)
    if bad:
        raise SplitR2GateError(f"prelaunch pair incompatibility: {bad}")
    payload = {
        "schema": PAIR_SCHEMA,
        "status": "PASS__PAIR_COMPATIBLE_BEFORE_MEASUREMENT",
        "members": {
            "LITS_I": left["receipt_identity"],
            "WVS7": right["receipt_identity"],
        },
        "exact_comparison": exact_fields,
        "same_macos_version": (
            left.get("hardware", {}).get("macos_version")
            == right.get("hardware", {}).get("macos_version")
        ),
        "macos_versions": {
            "LITS_I": left.get("hardware", {}).get("macos_version"),
            "WVS7": right.get("hardware", {}).get("macos_version"),
        },
        "absolute_cross_source_physical_metric_comparison_authorized": False,
    }
    payload["receipt_identity"] = _semantic_hash(payload)
    return payload


def verify_pair_member(
    *,
    readiness: Mapping[str, Any],
    pair: Mapping[str, Any],
    source: str,
    repo_root: Path,
    work_root: Path,
    control_root: Path,
    qualified_control_head: str,
    launcher_path: Path,
    driver_path: Path,
    helper_path: Path,
) -> None:
    _verify_self_identity(readiness, READINESS_SCHEMA)
    _verify_self_identity(pair, PAIR_SCHEMA)
    if pair.get("status") != "PASS__PAIR_COMPATIBLE_BEFORE_MEASUREMENT":
        raise SplitR2GateError("pair compatibility receipt is not PASS")
    if source not in SOURCE_SHA256 or readiness.get("assigned_source") != source:
        raise SplitR2GateError("readiness source assignment drift")
    if pair.get("members", {}).get(source) != readiness.get("receipt_identity"):
        raise SplitR2GateError("pair receipt does not bind this readiness receipt")
    repo = exact_repo_identity(repo_root)
    if readiness.get("protected_execution") != repo:
        raise SplitR2GateError("protected execution drift since readiness")
    control_root = control_root.resolve()
    head = _git_text(control_root, "rev-parse", "--verify", "HEAD^{commit}")
    if head != qualified_control_head:
        raise SplitR2GateError("control head drift since readiness")
    observed_control = {
        "head": head,
        "launcher_sha256": _sha256_file(launcher_path.resolve()),
        "driver_sha256": _sha256_file(driver_path.resolve()),
        "workroot_gates_sha256": _sha256_file(helper_path.resolve()),
    }
    if readiness.get("qualified_control") != observed_control:
        raise SplitR2GateError("control implementation bytes drift since readiness")
    if readiness.get("runtime") != combined_import_abi_gate()["observed"]:
        raise SplitR2GateError("runtime drift since readiness")
    if readiness.get("hardware") != _hardware():
        raise SplitR2GateError("hardware fingerprint drift since readiness")
    current_work_root = work_root.resolve()
    if readiness.get("fresh_work_root", {}).get("path") != str(current_work_root):
        raise SplitR2GateError("WORK_ROOT identity drift since readiness")
    _assert_fresh_work_root(current_work_root)


def _write_exact(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if not path.is_file() or path.read_bytes() != data:
            raise SplitR2GateError(f"preprovisioned bytes drift: {path}")
        return
    path.write_bytes(data)


def _prestate_material(repo_root: Path) -> list[Mapping[str, Any]]:
    material: list[Mapping[str, Any]] = []
    for rel, spec in R5_SUPPORT.items():
        protected = repo_root / rel
        observed = "PRESENT" if protected.is_file() else "ABSENT"
        if observed != spec["protected_checkout"]:
            raise SplitR2GateError(
                f"protected R5 support presence drift: {rel}: expected {spec['protected_checkout']} got {observed}"
            )
        if observed == "ABSENT":
            data = _git_show_bytes(repo_root, OWNER_COMMIT, rel)
            blob = _blob_sha1(data)
            if blob != spec["blob"]:
                raise SplitR2GateError(f"R5 support blob drift: {rel}")
            material.append({
                "class": "IMMUTABLE_CANDIDATE_NEUTRAL_SUPPORT",
                "source_path": rel,
                "destination": f"_be1_immutable/{OWNER_COMMIT}/{rel}",
                "git_blob_sha1": blob,
                "sha256": _sha256_bytes(data),
                "bytes": data,
            })
    for candidate, spec in OWNER_SPECS.items():
        data = _git_show_bytes(repo_root, OWNER_COMMIT, spec["path"])
        blob = _blob_sha1(data)
        if blob != spec["blob"]:
            raise SplitR2GateError(f"Candidate-{candidate} owner blob drift")
        material.append({
            "class": "EXACT_OWNER_CODE_BYTES",
            "candidate": candidate,
            "source_path": spec["path"],
            "destination": (
                f"_exact_owner_modules/{OWNER_COMMIT}/{candidate}/"
                f"{Path(spec['path']).name}"
            ),
            "git_blob_sha1": blob,
            "sha256": _sha256_bytes(data),
            "bytes": data,
        })
    return material


def _relative_files(root: Path, prefixes: Sequence[str]) -> list[str]:
    out = []
    for prefix in prefixes:
        base = root / prefix
        if not base.exists():
            continue
        for path in sorted(p for p in base.rglob("*") if p.is_file()):
            out.append(path.relative_to(root).as_posix())
    return out


def provision_joined_prestate(
    *, source: str, repo_root: Path, work_root: Path, output: Path
) -> Mapping[str, Any]:
    if source not in SOURCE_SHA256:
        raise SplitR2GateError(f"unknown source: {source}")
    repo_root = repo_root.resolve()
    work_root = work_root.resolve()
    exact_repo_identity(repo_root)
    for name in FORBIDDEN_PREPROVISION_ROOTS:
        if (work_root / name).exists():
            raise SplitR2GateError(
                f"candidate/source semantic state exists before preprovision: {name}"
            )
    existing_prestate = _relative_files(work_root, ALLOWED_PRESTATE_ROOTS)
    if existing_prestate:
        raise SplitR2GateError(
            f"joined prestate namespaces must be empty before provisioning: {existing_prestate}"
        )
    written = []
    if source == "WVS7":
        for item in _prestate_material(repo_root):
            dest = (work_root / item["destination"]).resolve()
            if work_root != dest and work_root not in dest.parents:
                raise SplitR2GateError("prestate destination escapes work root")
            _write_exact(dest, item["bytes"])
            written.append({k: v for k, v in item.items() if k != "bytes"})
    payload = {
        "schema": PRESTATE_SCHEMA,
        "status": "PASS",
        "source": source,
        "joined_position": (
            "AFTER_COMPLETE_LITS_I_A_B_C_BLOCK" if source == "WVS7"
            else "FRESH_COURT_BEFORE_LITS_I_A"
        ),
        "preprovisioned_objects": written,
        "preprovisioned_object_count": len(written),
        "candidate_neutral_c0_only": True,
        "candidate_owned_semantic_state_prebuilt": False,
        "candidate_owned_carrier_state_prebuilt": False,
        "forbidden_roots_absent": {
            name: not (work_root / name).exists() for name in FORBIDDEN_PREPROVISION_ROOTS
        },
        "raw_source_opened": False,
        "raw_source_hashed": False,
        "decoder_called": False,
        "measurement_performed": False,
    }
    payload["receipt_identity"] = _semantic_hash(payload)
    _atomic_json(output, payload)
    return payload


def verify_joined_prestate(
    *, source: str, repo_root: Path, work_root: Path, receipt_path: Path
) -> Mapping[str, Any]:
    doc = json.loads(receipt_path.read_text(encoding="utf-8"))
    _verify_self_identity(doc, PRESTATE_SCHEMA)
    if doc.get("source") != source or doc.get("status") != "PASS":
        raise SplitR2GateError("joined prestate receipt source/status drift")
    if doc.get("candidate_owned_semantic_state_prebuilt") is not False:
        raise SplitR2GateError("prestate illegally seeded candidate semantic state")
    if doc.get("candidate_owned_carrier_state_prebuilt") is not False:
        raise SplitR2GateError("prestate illegally seeded candidate carrier state")
    expected = _prestate_material(repo_root) if source == "WVS7" else []
    expected_by_dest = {item["destination"]: item for item in expected}
    got = doc.get("preprovisioned_objects", [])
    if {x.get("destination") for x in got} != set(expected_by_dest):
        raise SplitR2GateError("joined prestate object inventory drift")
    actual_prestate = set(_relative_files(work_root, ALLOWED_PRESTATE_ROOTS))
    if actual_prestate != set(expected_by_dest):
        raise SplitR2GateError(
            f"joined prestate namespace has missing/extra files: "
            f"expected={sorted(expected_by_dest)} actual={sorted(actual_prestate)}"
        )
    for dest_rel, item in expected_by_dest.items():
        dest = work_root / dest_rel
        if not dest.is_file() or _sha256_file(dest) != item["sha256"]:
            raise SplitR2GateError(f"joined prestate object missing/drifted: {dest_rel}")
    for name in FORBIDDEN_PREPROVISION_ROOTS:
        if (work_root / name).exists():
            raise SplitR2GateError(f"forbidden prebuilt state appeared: {name}")
    return doc


def _head_live_evidence(repo_root: Path) -> Mapping[str, Any]:
    root = repo_root.resolve()
    raw = _git(root, "ls-tree", "-r", "-z", "HEAD", "--", LIVE_EVIDENCE_REL.as_posix()).stdout
    out: dict[str, Any] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path_b = record.split(b"\t", 1)
        mode, obj_type, blob = meta.decode("ascii").split()
        rel = path_b.decode("utf-8", "surrogateescape")
        data = _git(root, "show", f"HEAD:{rel}").stdout
        out[rel] = {
            "mode": mode,
            "type": obj_type,
            "git_blob_sha1": blob,
            "sha256": _sha256_bytes(data),
            "size": len(data),
        }
    return dict(sorted(out.items()))


def _filesystem_inventory(root: Path) -> Mapping[str, Any]:
    if not root.exists():
        return {}
    out = {}
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        rel = p.relative_to(root).as_posix()
        out[rel] = {"sha256": _sha256_file(p), "size": p.stat().st_size}
    return out


def _ignored_file_inventory(repo_root: Path) -> Mapping[str, Any]:
    raw = _git(
        repo_root, "ls-files", "--others", "-i", "--exclude-standard", "-z"
    ).stdout
    out = {}
    for raw_rel in raw.split(b"\0"):
        if not raw_rel:
            continue
        rel = raw_rel.decode("utf-8", "surrogateescape")
        path = repo_root / rel
        if path.is_file():
            out[rel] = {"sha256": _sha256_file(path), "size": path.stat().st_size}
    return dict(sorted(out.items()))


def _is_python_cache_path(rel: str) -> bool:
    p = Path(rel)
    return p.suffix == ".pyc" and "__pycache__" in p.parts


def capture_repo_prestate_baseline(
    *, repo_root: Path, work_root: Path, source: str, output: Path
) -> Mapping[str, Any]:
    if source not in SOURCE_SHA256:
        raise SplitR2GateError(f"unknown source: {source}")
    repo = exact_repo_identity(repo_root)
    dirty = _git_text(repo_root, "status", "--porcelain", "--untracked-files=all")
    if dirty:
        raise SplitR2GateError("pre-run protected checkout must be clean")
    live = repo_root / LIVE_EVIDENCE_REL
    payload = {
        "schema": BASELINE_SCHEMA,
        "status": "PASS__PRE_MEASUREMENT_BASELINE",
        "source": source,
        "execution": repo,
        "head_tracked_live_evidence": _head_live_evidence(repo_root),
        "filesystem_live_evidence": _filesystem_inventory(live),
        "ignored_file_inventory": _ignored_file_inventory(repo_root),
        "work_root": str(work_root.resolve()),
    }
    payload["receipt_identity"] = _semantic_hash(payload)
    _atomic_json(output, payload)
    return payload


def _status_paths(repo_root: Path) -> list[Mapping[str, str]]:
    raw = _git(repo_root, "status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
    records = raw.split(b"\0")
    out: list[Mapping[str, str]] = []
    i = 0
    while i < len(records):
        rec = records[i]
        i += 1
        if not rec:
            continue
        text = rec.decode("utf-8", "surrogateescape")
        status = text[:2]
        path = text[3:]
        if "R" in status or "C" in status:
            if i >= len(records) or not records[i]:
                raise SplitR2GateError("malformed git porcelain rename/copy record")
            other = records[i].decode("utf-8", "surrogateescape")
            i += 1
            out.append({"status": status, "path": path, "other_path": other})
        else:
            out.append({"status": status, "path": path})
    return out


def _contains_source_stage(value: Any, source: str) -> bool:
    prefix = source + "/"
    if isinstance(value, str):
        return value.startswith(prefix)
    if isinstance(value, Mapping):
        return any(_contains_source_stage(v, source) for v in value.values())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return any(_contains_source_stage(v, source) for v in value)
    return False


def _live_path_allowed(repo_root: Path, rel: str, source: str) -> Mapping[str, Any]:
    live_prefix = LIVE_EVIDENCE_REL.as_posix() + "/"
    if not rel.startswith(live_prefix):
        raise SplitR2GateError(f"governed checkout mutation outside live evidence: {rel}")
    local = rel[len(live_prefix):]
    selected_prefixes = (
        f"cells/{source}__",
        f"learned/{source}__",
        f"persistence/{source}__",
        f"deletion/{source}__",
        f"failures/{source}__",
    )
    if local.startswith(selected_prefixes):
        return {"class": "SELECTED_SOURCE_LIVE_EVIDENCE", "path": rel}
    if local.startswith("court/") or local.startswith("failures/COURT__COMMON__"):
        p = repo_root / rel
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            raise SplitR2GateError(
                f"source-neutral live evidence is not parseable JSON: {rel}"
            ) from exc
        if not _contains_source_stage(doc, source):
            raise SplitR2GateError(
                f"source-neutral live evidence is not attributable to {source}: {rel}"
            )
        other = "WVS7" if source == "LITS_I" else "LITS_I"
        if _contains_source_stage(doc, other):
            raise SplitR2GateError(
                f"source-neutral live evidence contains nonselected source {other}: {rel}"
            )
        return {"class": "SELECTED_SOURCE_COMMON_COURT_ADMIN", "path": rel}
    raise SplitR2GateError(
        f"live evidence mutation is not classified for selected source {source}: {rel}"
    )


def verify_postrun_checkout(
    *, repo_root: Path, work_root: Path, source: str, baseline_path: Path, output: Path
) -> Mapping[str, Any]:
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    _verify_self_identity(baseline, BASELINE_SCHEMA)
    if baseline.get("source") != source:
        raise SplitR2GateError("postrun baseline source drift")
    repo = exact_repo_identity(repo_root)
    if baseline.get("execution") != repo:
        raise SplitR2GateError("postrun execution identity differs from baseline")
    if baseline.get("work_root") != str(work_root.resolve()):
        raise SplitR2GateError("postrun WORK_ROOT differs from baseline")
    head_live = _head_live_evidence(repo_root)
    if head_live != baseline.get("head_tracked_live_evidence"):
        raise SplitR2GateError("tracked HEAD evidence baseline changed")

    statuses = _status_paths(repo_root)
    classified_status = []
    for item in statuses:
        if item["status"] == "!!":
            continue
        if "R" in item["status"] or "C" in item["status"]:
            raise SplitR2GateError(f"rename/copy mutation forbidden in protected checkout: {item}")
        classified_status.append({
            **item,
            **_live_path_allowed(repo_root, item["path"], source),
        })

    live_root = repo_root / LIVE_EVIDENCE_REL
    before = baseline.get("filesystem_live_evidence", {})
    after = _filesystem_inventory(live_root)
    all_paths = sorted(set(before) | set(after))
    live_delta = []
    for local in all_paths:
        if before.get(local) == after.get(local):
            continue
        rel = (LIVE_EVIDENCE_REL / local).as_posix()
        if local not in after:
            raise SplitR2GateError(f"live evidence deletion is forbidden: {rel}")
        classification = _live_path_allowed(repo_root, rel, source)
        live_delta.append({
            "path": rel,
            "change": "CREATED" if local not in before else "MODIFIED",
            "before": before.get(local),
            "after": after.get(local),
            **classification,
        })

    ignored_before = baseline.get("ignored_file_inventory", {})
    ignored_after = _ignored_file_inventory(repo_root)
    cache_delta = []
    for rel in sorted(set(ignored_before) | set(ignored_after)):
        if ignored_before.get(rel) == ignored_after.get(rel):
            continue
        if not _is_python_cache_path(rel):
            raise SplitR2GateError(
                f"unclassified ignored-file mutation in protected checkout: {rel}"
            )
        cache_delta.append({
            "path": rel,
            "change": (
                "CREATED" if rel not in ignored_before
                else "DELETED" if rel not in ignored_after
                else "MODIFIED"
            ),
            "classification": "NON_EVIDENTIARY_PYTHON_RUNTIME_CACHE",
        })

    payload = {
        "schema": POSTRUN_SCHEMA,
        "status": "PASS__ONLY_CLASSIFIED_POSTRUN_MUTATIONS",
        "source": source,
        "execution": repo,
        "baseline_receipt_identity": baseline["receipt_identity"],
        "git_status_mutations": classified_status,
        "live_evidence_delta": live_delta,
        "python_cache_delta": cache_delta,
        "governed_code_or_config_mutation_seen": False,
        "nonselected_source_live_evidence_mutation_seen": False,
        "head_tracked_baseline_distinguished_from_live_state": True,
    }
    payload["receipt_identity"] = _semantic_hash(payload)
    _atomic_json(output, payload)
    return payload


def _load_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise SplitR2GateError(f"JSON object required: {path}")
    return value


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("runtime-gate")

    r = sub.add_parser("readiness")
    r.add_argument("--source", required=True, choices=tuple(SOURCE_SHA256))
    r.add_argument("--repo-root", type=Path, required=True)
    r.add_argument("--work-root", type=Path, required=True)
    r.add_argument("--control-root", type=Path, required=True)
    r.add_argument("--qualified-control-head", required=True)
    r.add_argument("--launcher", type=Path, required=True)
    r.add_argument("--driver", type=Path, required=True)
    r.add_argument("--helper", type=Path, required=True)
    r.add_argument("--output", type=Path, required=True)

    pair = sub.add_parser("pair")
    pair.add_argument("--lits-readiness", type=Path, required=True)
    pair.add_argument("--wvs-readiness", type=Path, required=True)
    pair.add_argument("--output", type=Path, required=True)

    member = sub.add_parser("verify-member")
    member.add_argument("--source", required=True, choices=tuple(SOURCE_SHA256))
    member.add_argument("--readiness", type=Path, required=True)
    member.add_argument("--pair", type=Path, required=True)
    member.add_argument("--repo-root", type=Path, required=True)
    member.add_argument("--work-root", type=Path, required=True)
    member.add_argument("--control-root", type=Path, required=True)
    member.add_argument("--qualified-control-head", required=True)
    member.add_argument("--launcher", type=Path, required=True)
    member.add_argument("--driver", type=Path, required=True)
    member.add_argument("--helper", type=Path, required=True)

    pre = sub.add_parser("preprovision")
    pre.add_argument("--source", required=True, choices=tuple(SOURCE_SHA256))
    pre.add_argument("--repo-root", type=Path, required=True)
    pre.add_argument("--work-root", type=Path, required=True)
    pre.add_argument("--output", type=Path, required=True)

    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "runtime-gate":
        out = combined_import_abi_gate()
    elif args.command == "readiness":
        out = machine_readiness(
            source=args.source,
            repo_root=args.repo_root,
            work_root=args.work_root,
            control_root=args.control_root,
            qualified_control_head=args.qualified_control_head,
            launcher_path=args.launcher,
            driver_path=args.driver,
            helper_path=args.helper,
        )
        _atomic_json(args.output, out)
    elif args.command == "pair":
        out = pair_compatibility(
            _load_json(args.lits_readiness),
            _load_json(args.wvs_readiness),
        )
        _atomic_json(args.output, out)
    elif args.command == "verify-member":
        verify_pair_member(
            readiness=_load_json(args.readiness),
            pair=_load_json(args.pair),
            source=args.source,
            repo_root=args.repo_root,
            work_root=args.work_root,
            control_root=args.control_root,
            qualified_control_head=args.qualified_control_head,
            launcher_path=args.launcher,
            driver_path=args.driver,
            helper_path=args.helper,
        )
        out = {"status": "PASS__PAIR_MEMBER_REVERIFIED", "source": args.source}
    elif args.command == "preprovision":
        out = provision_joined_prestate(
            source=args.source,
            repo_root=args.repo_root,
            work_root=args.work_root,
            output=args.output,
        )
    else:
        raise AssertionError(args.command)
    print(json.dumps(out, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
