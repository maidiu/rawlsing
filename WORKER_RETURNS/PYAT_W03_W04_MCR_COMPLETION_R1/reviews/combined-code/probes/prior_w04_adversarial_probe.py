#!/usr/bin/env python3
"""Unanticipated adversarial probes for W04 policy/invalidation/lifecycle.

Run with TMPDIR under the review lease. Uses only sourcefree fixtures.
No production/test-existing/author/HQ/peer/protected writes.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import tempfile
import time
from unittest import mock

from rawlsing_next._pre553_w04_cache import (
    LEGACY_ENV,
    POLICY_ENV,
    atomic_replace,
    fsync_dir,
    load_policy,
    prune,
)
from rawlsing_next.tests.test_pre553_route_b_production import _execute, _fixture


BASE = Path(tempfile.mkdtemp(prefix="w04-adversarial-"))
OUTSIDE_TEMP = Path(__file__).resolve().parents[1] / "outside-temp"
RESULTS = {}


def _env_clear() -> None:
    for name in (POLICY_ENV, LEGACY_ENV, "PYTEST_CURRENT_TEST"):
        os.environ.pop(name, None)


def _private_dir(name: str, mode: int = 0o700) -> Path:
    path = BASE / name
    path.mkdir(mode=mode, exist_ok=True)
    path.chmod(mode)
    return path


def _policy(root: Path, *, permission: str = "NONRESPONDENT_SOURCEFREE") -> Path:
    path = BASE / ("policy-" + root.name + ".json")
    path.write_text(json.dumps({
        "schema": "PYAT_C11_ACCELERATOR_POLICY@1",
        "enabled": True,
        "root": str(root),
        "source_permission": permission,
        "authorization_id": "adversarial-probe",
        "retention_budget": {"max_bytes": 268435456, "max_files": 4, "max_age_seconds": 86400},
    }), encoding="utf-8")
    path.chmod(0o600)
    return path


def main() -> int:
    _env_clear()
    RESULTS["no_policy_no_legacy"] = load_policy() is None

    legacy_root = _private_dir("legacy-no-pytest")
    os.environ[LEGACY_ENV] = str(legacy_root)
    RESULTS["legacy_without_pytest"] = load_policy() is None

    os.environ["PYTEST_CURRENT_TEST"] = "ordinary-process masquerade probe"
    policy = load_policy()
    RESULTS["legacy_with_pytest_env_only"] = None if policy is None else {
        "accepted": True,
        "authorization_id": policy.authorization_id,
        "source_permission": policy.source_permission,
        "root": str(policy.root),
    }

    # Demonstrate actual write through the legacy fallback from a plain process.
    write_root = BASE / "legacy-write"
    os.environ[LEGACY_ENV] = str(write_root)
    fx = _fixture()
    _execute(fx)
    RESULTS["legacy_actual_cache_writes"] = len(tuple(write_root.glob("c11-events-*.parquet")))

    _env_clear()

    # Final-component symlink root must not be accepted.
    real = _private_dir("real-root")
    link = BASE / "root-link"
    link.symlink_to(real, target_is_directory=True)
    os.environ[POLICY_ENV] = str(_policy(link))
    RESULTS["policy_root_symlink_rejected"] = load_policy() is None

    # Policy-file symlink must not be accepted.
    _env_clear()
    real_policy = _policy(real)
    policy_link = BASE / "policy-link.json"
    policy_link.symlink_to(real_policy)
    os.environ[POLICY_ENV] = str(policy_link)
    RESULTS["policy_file_symlink_rejected"] = load_policy() is None

    # Group/world-accessible root must not be accepted.
    _env_clear()
    open_root = _private_dir("open-root", mode=0o755)
    os.environ[POLICY_ENV] = str(_policy(open_root))
    RESULTS["policy_root_0755_rejected"] = load_policy() is None

    # Simulated owner mismatch (no privileged chown): code compares os.getuid().
    _env_clear()
    owner_root = _private_dir("owner-root")
    os.environ[POLICY_ENV] = str(_policy(owner_root))
    with mock.patch("rawlsing_next._pre553_w04_cache.os.getuid", return_value=os.getuid() + 1):
        RESULTS["owner_mismatch_simulated_rejected"] = load_policy() is None

    # Relative/missing policy roots and world-writable policy file must reject.
    _env_clear()
    relative_policy = BASE / "relative-policy.json"
    relative_policy.write_text(json.dumps({
        "schema": "PYAT_C11_ACCELERATOR_POLICY@1", "enabled": True, "root": "relative/root",
        "source_permission": "NONRESPONDENT_SOURCEFREE", "authorization_id": "probe",
        "retention_budget": {"max_bytes": 1, "max_files": 1, "max_age_seconds": 1},
    }), encoding="utf-8")
    relative_policy.chmod(0o600)
    os.environ[POLICY_ENV] = str(relative_policy)
    RESULTS["policy_root_relative_rejected"] = load_policy() is None

    _env_clear()
    missing_policy = BASE / "missing-root-policy.json"
    missing_policy.write_text(json.dumps({
        "schema": "PYAT_C11_ACCELERATOR_POLICY@1", "enabled": True, "root": str(BASE / "missing-root"),
        "source_permission": "NONRESPONDENT_SOURCEFREE", "authorization_id": "probe",
        "retention_budget": {"max_bytes": 1, "max_files": 1, "max_age_seconds": 1},
    }), encoding="utf-8")
    missing_policy.chmod(0o600)
    os.environ[POLICY_ENV] = str(missing_policy)
    RESULTS["policy_root_missing_rejected"] = load_policy() is None

    _env_clear()
    writable_policy = _policy(_private_dir("writable-policy-root"))
    writable_policy.chmod(0o666)
    os.environ[POLICY_ENV] = str(writable_policy)
    RESULTS["policy_file_group_world_writable_rejected"] = load_policy() is None

    _env_clear()
    no_auth = BASE / "no-auth-policy.json"
    no_auth.write_text(json.dumps({
        "schema": "PYAT_C11_ACCELERATOR_POLICY@1", "enabled": True,
        "root": str(_private_dir("no-auth-root")),
        "source_permission": "NONRESPONDENT_SOURCEFREE", "authorization_id": "   ",
        "retention_budget": {"max_bytes": 1024, "max_files": 1, "max_age_seconds": 60},
    }), encoding="utf-8")
    no_auth.chmod(0o600)
    os.environ[POLICY_ENV] = str(no_auth)
    RESULTS["authorization_id_missing_rejected"] = load_policy() is None

    _env_clear()
    no_budget = BASE / "no-budget-policy.json"
    no_budget.write_text(json.dumps({
        "schema": "PYAT_C11_ACCELERATOR_POLICY@1", "enabled": True,
        "root": str(_private_dir("no-budget-root")),
        "source_permission": "NONRESPONDENT_SOURCEFREE", "authorization_id": "probe",
    }), encoding="utf-8")
    no_budget.chmod(0o600)
    os.environ[POLICY_ENV] = str(no_budget)
    RESULTS["retention_budget_missing_rejected"] = load_policy() is None

    # Legacy root outside the platform temp root must not be accepted.
    _env_clear()
    outside = OUTSIDE_TEMP
    outside.mkdir(mode=0o700, exist_ok=True)
    outside.chmod(0o700)
    os.environ[LEGACY_ENV] = str(outside)
    os.environ["PYTEST_CURRENT_TEST"] = "probe outside-temp"
    RESULTS["legacy_root_outside_temp_rejected"] = load_policy() is None

    # An explicit invalid configured policy must not fall back to legacy.
    _env_clear()
    os.environ[POLICY_ENV] = str(BASE / "missing-policy.json")
    os.environ[LEGACY_ENV] = str(_private_dir("legacy-fallback-should-not-run"))
    os.environ["PYTEST_CURRENT_TEST"] = "probe fallback"
    RESULTS["invalid_configured_policy_no_legacy_fallback"] = load_policy() is None

    # Retention max_age/max_files on disposable cache files.
    _env_clear()
    retention_root = _private_dir("retention-root")
    retention_policy = BASE / "retention-policy.json"
    retention_policy.write_text(json.dumps({
        "schema": "PYAT_C11_ACCELERATOR_POLICY@1", "enabled": True, "root": str(retention_root),
        "source_permission": "NONRESPONDENT_SOURCEFREE", "authorization_id": "retention-probe",
        "retention_budget": {"max_bytes": 1_000_000, "max_files": 1, "max_age_seconds": 60},
    }), encoding="utf-8")
    retention_policy.chmod(0o600)
    os.environ[POLICY_ENV] = str(retention_policy)
    retention = load_policy()
    if retention is not None:
        import time
        old = retention_root / "c11-events-a.parquet"
        new = retention_root / "c11-events-b.parquet"
        old.write_bytes(b"old")
        new.write_bytes(b"new")
        old.chmod(0o600)
        new.chmod(0o600)
        now = time.time()
        os.utime(old, (now - 120, now - 120))
        os.utime(new, (now, now))
        prune(retention, now=now)
        RESULTS["retention_files_after_prune"] = len(tuple(retention_root.glob("c11-events-*.parquet")))
    else:
        RESULTS["retention_files_after_prune"] = None

    # Crash-orphan staging file is hidden from CACHE_GLOB and survives prune.
    _env_clear()
    orphan_root = _private_dir("orphan-root")
    orphan_policy = BASE / "orphan-policy.json"
    orphan_policy.write_text(json.dumps({
        "schema": "PYAT_C11_ACCELERATOR_POLICY@1", "enabled": True, "root": str(orphan_root),
        "source_permission": "NONRESPONDENT_SOURCEFREE", "authorization_id": "orphan-probe",
        "retention_budget": {"max_bytes": 1000, "max_files": 1, "max_age_seconds": 1},
    }), encoding="utf-8")
    orphan_policy.chmod(0o600)
    os.environ[POLICY_ENV] = str(orphan_policy)
    orphan_policy_obj = load_policy()
    orphan = orphan_root / ".c11-events-orphan"
    orphan.write_bytes(b"orphan")
    orphan.chmod(0o600)
    old = time.time() - 3600
    os.utime(orphan, (old, old))
    prune(orphan_policy_obj, now=time.time())
    RESULTS["hidden_staging_orphan_remains"] = orphan.exists()

    # Directory fsync failure is swallowed by fsync_dir; demonstrate behavior.
    _env_clear()
    fsync_target = _private_dir("fsync-target")
    staged = BASE / "staged-cache"
    destination = fsync_target / "c11-events-probe.parquet"
    staged.write_bytes(b"probe")
    with mock.patch("rawlsing_next._pre553_w04_cache.os.fsync", side_effect=OSError("probe fsync failure")):
        raised = False
        try:
            fsync_dir(fsync_target)
            atomic_replace(staged, destination)
        except OSError:
            raised = True
    RESULTS["dir_fsync_failure_swallowed"] = {
        "raised": raised,
        "destination_exists": destination.exists(),
    }

    OUT = Path(__file__).resolve().parent / "adversarial_probe.json"
    OUT.write_text(json.dumps(RESULTS, indent=2, sort_keys=True) + "\n")
    print(json.dumps(RESULTS, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    finally:
        shutil.rmtree(BASE, ignore_errors=True)
        shutil.rmtree(OUTSIDE_TEMP, ignore_errors=True)
