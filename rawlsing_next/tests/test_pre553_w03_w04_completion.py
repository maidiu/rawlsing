"""Focused W04 governed persistence and cache-lifecycle completion tests.

These tests use the existing sourcefree Route B/C11/I03/I05 fixture and real
current consumers.  They do not create a second C11 store, query engine,
statistical oracle, native/source permission, or deployment root grant.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import json
from pathlib import Path
import time

import pytest

from rawlsing_next import _pre553_c11_execution_view as compact
from rawlsing_next._pre553_w04_cache import (
    CACHE_ENVELOPE_KEY,
    CACHE_METADATA_KEY,
    POLICY_ENV,
    STAGING_GRACE_SECONDS,
    load_policy,
    prune,
)
from rawlsing_next import pre553_parquet_carrier as carrier_module
from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier
from rawlsing_next.tests.test_pre553_c11_cold_reopen_i03 import (
    _cold_executor,
    _consumer_material,
)
from rawlsing_next.tests.test_pre553_route_b_production import _execute, _fixture


def _write_policy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    permission: str = "NONRESPONDENT_SOURCEFREE",
    max_bytes: int = 268_435_456,
    max_files: int = 4,
    max_age_seconds: int = 86_400,
    root_mode: int = 0o700,
) -> tuple[Path, Path]:
    root = tmp_path / "accelerator"
    root.mkdir(mode=root_mode, exist_ok=True)
    root.chmod(root_mode)
    policy = {
        "schema": "PYAT_C11_ACCELERATOR_POLICY@1",
        "enabled": True,
        "root": str(root),
        "source_permission": permission,
        "authorization_id": "sourcefree-test-host-owner",
        "retention_budget": {
            "max_bytes": max_bytes,
            "max_files": max_files,
            "max_age_seconds": max_age_seconds,
        },
    }
    policy_path = tmp_path / "accelerator-policy.json"
    policy_path.write_text(json.dumps(policy), encoding="utf-8")
    policy_path.chmod(0o600)
    monkeypatch.setenv(POLICY_ENV, str(policy_path))
    monkeypatch.delenv(compact._CACHE_ENV, raising=False)
    return root, policy_path


def _cache_files(root: Path) -> tuple[Path, ...]:
    return tuple(sorted(root.glob("c11-events-*.parquet")))


def test_w04_cache_policy_authorized_private_root_activates_default(tmp_path, monkeypatch):
    root, _ = _write_policy(tmp_path, monkeypatch)
    fx = _fixture()
    first = _execute(fx)
    files = _cache_files(root)
    assert len(files) == 1
    schema = __import__("pyarrow.parquet", fromlist=["read_schema"]).read_schema(files[0])
    policy = load_policy()
    assert policy is not None
    envelope = json.loads(schema.metadata[CACHE_ENVELOPE_KEY].decode("utf-8"))
    assert schema.metadata[CACHE_METADATA_KEY].decode("ascii") == envelope["key"]
    assert envelope["policy_root"] == policy.trusted_root_id
    assert envelope["authority_root"]
    assert first.c11_release.release_ref
    # A host policy activates the accelerator without a per-workload cache flag.
    assert _execute(fx).c11_release.release_ref == first.c11_release.release_ref
    files[0].unlink()
    assert _execute(fx).c11_release.release_ref == first.c11_release.release_ref
    assert len(_cache_files(root)) == 1


def test_w04_cache_policy_absent_invalid_unowned_or_oversize_refuses_without_write(tmp_path, monkeypatch):
    fx = _fixture()
    monkeypatch.delenv(POLICY_ENV, raising=False)
    monkeypatch.delenv(compact._CACHE_ENV, raising=False)
    _execute(fx)
    absent_root = tmp_path / "absent"
    assert not absent_root.exists()

    monkeypatch.setenv(POLICY_ENV, str(tmp_path / "missing-policy.json"))
    _execute(fx)
    assert not absent_root.exists()

    unauthorized = tmp_path / "unauthorized"
    unauthorized.mkdir(mode=0o755)
    unauthorized.chmod(0o755)
    policy_path = tmp_path / "bad-policy.json"
    policy_path.write_text(json.dumps({
        "schema": "PYAT_C11_ACCELERATOR_POLICY@1",
        "enabled": True,
        "root": str(unauthorized),
        "source_permission": "NONRESPONDENT_SOURCEFREE",
        "authorization_id": "test",
        "retention_budget": {"max_bytes": 1024, "max_files": 1, "max_age_seconds": 60},
    }), encoding="utf-8")
    policy_path.chmod(0o600)
    monkeypatch.setenv(POLICY_ENV, str(policy_path))
    _execute(fx)
    assert not tuple(unauthorized.glob("c11-events-*.parquet"))

    root, _ = _write_policy(tmp_path, monkeypatch, permission="RESPONDENT_SOURCE")
    _execute(fx)
    assert not _cache_files(root)

    root, _ = _write_policy(tmp_path, monkeypatch, max_bytes=1)
    _execute(fx)
    assert not _cache_files(root)


def test_w04_cache_policy_spoofed_test_marker_and_legacy_dir_no_write(tmp_path, monkeypatch):
    legacy_root = tmp_path / "legacy-root"
    legacy_root.mkdir(mode=0o700)
    legacy_root.chmod(0o700)
    monkeypatch.setenv(compact._CACHE_ENV, str(legacy_root))
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "ordinary-process-spoof")
    monkeypatch.delenv(POLICY_ENV, raising=False)
    assert load_policy() is None
    fx = _fixture()
    _execute(fx)
    assert not _cache_files(legacy_root)


def test_w04_cache_invalidation_source_projection_authority_release_replay_schema_bind(tmp_path, monkeypatch):
    root, _ = _write_policy(tmp_path, monkeypatch)
    fx = _fixture()
    result = _execute(fx)
    public = result.c11_release.public_objects
    path, = _cache_files(root)
    schema = __import__("pyarrow.parquet", fromlist=["read_schema"]).read_schema(path)
    key = schema.metadata[CACHE_METADATA_KEY].decode("ascii")
    envelope = json.loads(schema.metadata[CACHE_ENVELOPE_KEY].decode("utf-8"))
    policy = load_policy()
    assert policy is not None
    selectors = public.lane.selectors
    assert compact._read_bodies(path, key, selectors, policy=policy, envelope=envelope) is not None
    for field in ("authority_root", "source", "projection", "release", "release_manifest", "replay", "schema", "policy_root"):
        changed = dict(envelope)
        changed[field] = "tampered-" + field
        assert compact._read_bodies(path, key, selectors, policy=policy, envelope=changed) is None
    changed_key = "f" * 64
    assert compact._read_bodies(path, changed_key, selectors, policy=policy, envelope=envelope) is None
    # The cache remains a safe miss; rebuilding the current exact release restores it.
    assert _execute(fx).c11_release.release_ref == result.c11_release.release_ref
    assert len(_cache_files(root)) == 1


def test_w04_recovery_aborted_cache_publication_keeps_previous_complete_cache(tmp_path, monkeypatch):
    root, _ = _write_policy(tmp_path, monkeypatch)
    fx = _fixture()
    baseline = _execute(fx)
    path, = _cache_files(root)
    original = path.read_bytes()
    changed = {**fx, "stream": replace(fx["stream"], decoder_metadata_digest="e" * 64)}

    def interrupted(_staged, _destination):
        raise OSError("test-only interrupted cache publication")

    with monkeypatch.context() as patch:
        patch.setattr(compact.os, "replace", interrupted)
        observed = _execute(changed)
    assert observed.c11_release.release_ref == baseline.c11_release.release_ref
    assert path.read_bytes() == original
    assert _cache_files(root) == (path,)
    # The in-memory current lane remains exact; a later normal build can cache it.
    assert _execute(changed).c11_release.release_ref == observed.c11_release.release_ref


def test_w04_recovery_concurrent_cache_builders_share_exact_release(tmp_path, monkeypatch):
    root, _ = _write_policy(tmp_path, monkeypatch)
    fx = _fixture()
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda _index: _execute(fx), range(4)))
    refs = {result.c11_release.release_ref.key for result in results}
    assert len(refs) == 1
    files = _cache_files(root)
    assert len(files) == 1
    public = results[0].c11_release.public_objects
    policy = load_policy()
    assert policy is not None
    schema = __import__("pyarrow.parquet", fromlist=["read_schema"]).read_schema(files[0])
    key = schema.metadata[CACHE_METADATA_KEY].decode("ascii")
    envelope = json.loads(schema.metadata[CACHE_ENVELOPE_KEY].decode("utf-8"))
    assert compact._read_bodies(files[0], key, public.lane.selectors, policy=policy, envelope=envelope) is not None
    assert _execute(fx).c11_release.release_ref.key == next(iter(refs))


def test_w04_recovery_cache_directory_fsync_failure_is_safe_miss(tmp_path, monkeypatch):
    root, _ = _write_policy(tmp_path, monkeypatch)
    fx = _fixture()
    baseline = _execute(fx)
    path, = _cache_files(root)
    path.unlink()

    def fail(_path):
        raise OSError("test-only cache directory fsync failure")

    with monkeypatch.context() as patch:
        patch.setattr("rawlsing_next._pre553_w04_cache.fsync_dir", fail)
        observed = _execute(fx)
    assert observed.c11_release.release_ref == baseline.c11_release.release_ref
    assert not _cache_files(root)
    # A later healthy execution restores a validated cache.
    assert _execute(fx).c11_release.release_ref == baseline.c11_release.release_ref
    assert len(_cache_files(root)) == 1


def test_w04_recovery_cache_file_fsync_failure_is_safe_miss(tmp_path, monkeypatch):
    root, _ = _write_policy(tmp_path, monkeypatch)
    fx = _fixture()
    baseline = _execute(fx)
    path, = _cache_files(root)
    path.unlink()

    def fail(_fd):
        raise OSError("test-only cache file fsync failure")

    with monkeypatch.context() as patch:
        patch.setattr(compact.os, "fsync", fail)
        observed = _execute(fx)
    assert observed.c11_release.release_ref == baseline.c11_release.release_ref
    assert not _cache_files(root)
    assert _execute(fx).c11_release.release_ref == baseline.c11_release.release_ref
    assert len(_cache_files(root)) == 1


def test_w04_recovery_carrier_parent_fsync_failure_cleans_only_new_publication(tmp_path, monkeypatch):
    fx = _fixture()
    prior = _execute(fx)
    other = _execute(_fixture(valid_empty=True))
    root = tmp_path / "canonical-fsync"
    carrier = ParquetC11Carrier(root)
    prior_dir = carrier.persist(prior.c11_release)
    calls = []

    def fail_after_replace(path):
        calls.append(Path(path))
        if len(calls) == 2:
            raise OSError("test-only canonical parent fsync failure")

    with monkeypatch.context() as patch:
        patch.setattr(carrier_module, "fsync_dir", fail_after_replace)
        with pytest.raises(OSError):
            carrier.persist(other.c11_release)
    assert not carrier.release_dir(other.c11_release).exists()
    assert carrier.reopen(
        prior.c11_release.source_artifact_ref.content_hash,
        prior.c11_release.release_id,
        prior.c11_release.semantic_release_hash,
    ).release_ref == prior.c11_release.release_ref
    assert carrier.persist(other.c11_release) == carrier.release_dir(other.c11_release)
    assert prior_dir.is_dir()


def test_w04_recovery_retention_prunes_hidden_orphans_without_active_or_canonical_loss(tmp_path, monkeypatch):
    root, _ = _write_policy(tmp_path, monkeypatch, max_files=1, max_age_seconds=1)
    policy = load_policy()
    assert policy is not None
    now = time.time()
    orphan = root / ".c11-events-orphan"
    orphan.write_bytes(b"orphan")
    orphan.chmod(0o600)
    old = now - (STAGING_GRACE_SECONDS + 60)
    __import__("os").utime(orphan, (old, old))
    active = root / ".c11-events-active"
    active.write_bytes(b"active")
    active.chmod(0o600)
    canonical_root = tmp_path / "canonical-retention"
    source = _execute(_fixture())
    carrier = ParquetC11Carrier(canonical_root)
    canonical_dir = carrier.persist(source.c11_release)
    prune(policy, now=now)
    assert not orphan.exists()
    assert active.exists()
    assert canonical_dir.is_dir()
    assert carrier.reopen(
        source.c11_release.source_artifact_ref.content_hash,
        source.c11_release.release_id,
        source.c11_release.semantic_release_hash,
    ).release_ref == source.c11_release.release_ref


def test_w04_recovery_carrier_aborted_publish_leaves_no_partial_canonical_release(tmp_path, monkeypatch):
    fx = _fixture()
    source = _execute(fx)
    root = tmp_path / "canonical-interrupted"
    carrier = ParquetC11Carrier(root)

    def interrupted(_staged, _destination):
        raise OSError("test-only interrupted canonical publication")

    with monkeypatch.context() as patch:
        patch.setattr(carrier_module.os, "replace", interrupted)
        with pytest.raises(OSError):
            carrier.persist(source.c11_release)
    release_dir = carrier.release_dir(source.c11_release)
    assert not release_dir.exists()
    # No partial staging directory is accepted as a canonical release.
    assert not any(path.is_dir() for path in (root / "releases").glob("*/*/*"))
    assert carrier.persist(source.c11_release) == release_dir
    assert carrier.reopen(
        source.c11_release.source_artifact_ref.content_hash,
        source.c11_release.release_id,
        source.c11_release.semantic_release_hash,
    ).release_ref == source.c11_release.release_ref


def test_w04_boundary_canonical_parquet_survives_accelerator_delete(tmp_path, monkeypatch):
    root, _ = _write_policy(tmp_path, monkeypatch)
    fx = _fixture()
    source = _execute(fx)
    baseline = _consumer_material(source.repository_binding.executor, fx)
    canonical_root = tmp_path / "canonical-parquet"
    carrier = ParquetC11Carrier(canonical_root)
    directory = carrier.persist(source.c11_release)
    assert directory.is_dir()
    assert _cache_files(root)
    # The accelerator is disposable; deleting it must not remove or mutate the
    # canonical Parquet release or its actual I03/I05 consumer result.
    import shutil
    shutil.rmtree(root)
    assert not root.exists()
    reopened = _cold_executor(canonical_root, source.c11_release, fx)
    assert _consumer_material(reopened, fx) == baseline
    assert carrier.persist(source.c11_release) == directory
