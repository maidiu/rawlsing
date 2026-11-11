"""Focused W03/W04 cold-path, compact-lane and topology tests.

Heavy 100k paired measurement is owned by the benchmark lane; these tests are
small, exact and deterministic.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from rawlsing_next._pre553_c11_execution_view import _CompactPublicObjects
from rawlsing_next._pre553_w04_cache import (
    CACHE_ENVELOPE_KEY,
    CACHE_METADATA_KEY,
    LEGACY_ENV,
    POLICY_ENV,
    load_policy,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import RespondentEvent, canonical_json
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    SourceBackedC11FacadeError,
    build_cold_source_backed_c11_release,
    build_source_backed_c11_repository,
    build_validated_source_backed_c11_release_from_stream,
)
from rawlsing_next.tests.test_pre553_c11_cold_reopen_i03 import _consumer_material
from rawlsing_next.tests.test_pre553_route_b_production import (
    _execute,
    _fixture as _route_fixture,
)
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture as _facade_fixture


def _write_policy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    name: str = "accelerator",
    max_files: int = 4,
    max_bytes: int = 268_435_456,
) -> tuple[Path, Path]:
    root = tmp_path / name
    root.mkdir(mode=0o700, exist_ok=True)
    root.chmod(0o700)
    policy = {
        "schema": "PYAT_C11_ACCELERATOR_POLICY@1",
        "enabled": True,
        "root": str(root),
        "source_permission": "NONRESPONDENT_SOURCEFREE",
        "authorization_id": "sourcefree-coupled-cold-test",
        "retention_budget": {
            "max_bytes": max_bytes,
            "max_files": max_files,
            "max_age_seconds": 86_400,
        },
    }
    policy_path = tmp_path / f"{name}-policy.json"
    policy_path.write_text(json.dumps(policy), encoding="utf-8")
    policy_path.chmod(0o600)
    monkeypatch.setenv(POLICY_ENV, str(policy_path))
    monkeypatch.delenv(LEGACY_ENV, raising=False)
    return root, policy_path


def _cache_files(root: Path) -> tuple[Path, ...]:
    return tuple(sorted(root.glob("c11-events-*.parquet")))


def _stream(fx):
    return ExactPhysicalCellStream(
        fx["source_sha"], fx["incidence"].row_count, lambda: iter(fx["cells"]))


def _compare_eager_cold(stream, projection):
    eager = build_validated_source_backed_c11_release_from_stream(stream, projection)
    cold = build_cold_source_backed_c11_release(stream, projection)
    assert cold.release_ref == eager.release_ref
    assert cold.replay_manifest.ref == eager.replay_manifest.ref
    assert cold.source_release_manifest_hash == eager.source_release_manifest_hash
    assert tuple(x.ref for x in cold.public_objects) == tuple(
        x.ref for x in eager.public_objects)
    assert tuple(x.ref for x in cold.internal_records) == tuple(
        x.ref for x in eager.internal_records)
    assert cold.m01_m18_coverage == eager.m01_m18_coverage
    return eager, cold


def test_cold_release_is_exact_and_compact_for_full_facade_fixture():
    fx = _facade_fixture()
    eager, cold = _compare_eager_cold(_stream(fx), fx["projection"])
    assert isinstance(cold.public_objects, _CompactPublicObjects)
    assert not any(isinstance(obj, RespondentEvent) for obj in cold.public_objects.non_events)
    assert any(isinstance(entry, int) for entry in cold.public_objects.entries)
    assert len(cold.public_objects) == len(eager.public_objects)
    # Materialization is exact, including zero-occurrence and repeated/ranked lanes.
    for left, right in zip(eager.public_objects, cold.public_objects):
        assert left.as_dict() == right.as_dict()
    event_states = {
        obj.response_state for obj in eager.public_objects
        if isinstance(obj, RespondentEvent)
    }
    assert {"SUBSTANTIVE_RESPONSE", "MISSING"} <= event_states
    assert "ORDERED_SEQUENCE" in {
        obj.multiplicity_order_rank_fields["kind"]
        for obj in eager.public_objects
        if isinstance(obj, RespondentEvent)
    }
    assert "REPEATED_EVENT" in {
        obj.multiplicity_order_rank_fields["kind"]
        for obj in eager.public_objects
        if isinstance(obj, RespondentEvent)
    }


def test_cold_repository_is_used_without_disk_cache_and_matches_eager():
    fx = _facade_fixture()
    stream = _stream(fx)
    eager = build_validated_source_backed_c11_release_from_stream(stream, fx["projection"])
    repository, cold = build_source_backed_c11_repository(stream, fx["projection"])
    assert isinstance(cold.public_objects, _CompactPublicObjects)
    assert cold.release_ref == eager.release_ref
    assert repository.release_refs == (eager.release_ref,)
    assert repository.resolve_release_exact(eager.release_ref).release_ref == eager.release_ref


@pytest.mark.parametrize(
    "kwargs",
    ({}, {"missing_weight": True}, {"valid_empty": True}),
    ids=("routed-ordered-repeated", "missing-optional-weight", "valid-empty"),
)
def test_cold_path_matches_eager_route_b_fixture(kwargs):
    fx = _route_fixture(**kwargs)
    _compare_eager_cold(fx["stream"], fx["projection"])


def test_cold_path_refuses_duplicate_physical_row_slot():
    fx = _facade_fixture()
    cells = tuple(fx["cells"]) + (fx["cells"][0],)
    stream = ExactPhysicalCellStream(fx["source_sha"], 3, lambda: iter(cells))
    with pytest.raises(SourceBackedC11FacadeError, match="duplicate physical row/slot"):
        build_cold_source_backed_c11_release(stream, fx["projection"])


def test_cold_path_refuses_incomplete_projected_slot():
    fx = _facade_fixture()
    cells = tuple(cell for cell in fx["cells"] if not (
        cell.variable_ordinal == 1 and cell.row_ordinal == 3))
    stream = ExactPhysicalCellStream(fx["source_sha"], 3, lambda: iter(cells))
    with pytest.raises(SourceBackedC11FacadeError, match="projected slot incomplete"):
        build_cold_source_backed_c11_release(stream, fx["projection"])


def test_cold_path_refuses_wrong_source_sha():
    fx = _facade_fixture()
    stream = ExactPhysicalCellStream("f" * 64, 3, lambda: iter(fx["cells"]))
    with pytest.raises(SourceBackedC11FacadeError, match="source SHA mismatch"):
        build_cold_source_backed_c11_release(stream, fx["projection"])


def test_cold_default_policy_writes_one_cache_and_reuses_exact_release(
    tmp_path, monkeypatch,
):
    root, _ = _write_policy(tmp_path, monkeypatch)
    fx = _facade_fixture()
    stream = _stream(fx)
    eager = build_validated_source_backed_c11_release_from_stream(stream, fx["projection"])

    _, first = build_source_backed_c11_repository(stream, fx["projection"])
    files = _cache_files(root)
    assert len(files) == 1
    assert first.release_ref == eager.release_ref
    mtime = files[0].stat().st_mtime_ns

    # The normal default reads the governed cache rather than rewriting it.
    _, second = build_source_backed_c11_repository(stream, fx["projection"])
    assert second.release_ref == eager.release_ref
    assert len(_cache_files(root)) == 1
    assert _cache_files(root)[0].stat().st_mtime_ns == mtime

    # The eager fallback is still a working governed-cache path in a fresh root.
    eager_root, _ = _write_policy(tmp_path, monkeypatch, name="eager-accelerator")
    _, eager_cached = build_source_backed_c11_repository(
        stream, fx["projection"], cold=False)
    assert eager_cached.release_ref == eager.release_ref
    assert len(_cache_files(eager_root)) == 1


def test_cold_policy_envelope_binds_exact_identity(tmp_path, monkeypatch):
    root, _ = _write_policy(tmp_path, monkeypatch)
    fx = _facade_fixture()
    _, release = build_source_backed_c11_repository(_stream(fx), fx["projection"])
    path, = _cache_files(root)
    import pyarrow.parquet as pq

    schema = pq.read_schema(path)
    envelope = json.loads(schema.metadata[CACHE_ENVELOPE_KEY].decode("utf-8"))
    policy = load_policy()
    assert policy is not None
    assert schema.metadata[CACHE_METADATA_KEY].decode("ascii") == envelope["key"]
    assert envelope["policy_root"] == policy.trusted_root_id
    assert envelope["source"] == release.source_artifact_ref.as_dict()
    assert envelope["release"] == release.release_ref.as_dict()
    assert envelope["replay"] == release.replay_manifest.ref.as_dict()
    assert envelope["release_manifest"] == release.source_release_manifest_hash
    assert envelope["schema"] == "PRE553_I02_EVENT_ACCELERATOR@2"
    assert envelope["member_root"]


def test_cold_policy_absent_or_legacy_dir_does_not_write(tmp_path, monkeypatch):
    legacy_root = tmp_path / "legacy-root"
    legacy_root.mkdir(mode=0o700)
    legacy_root.chmod(0o700)
    monkeypatch.delenv(POLICY_ENV, raising=False)
    monkeypatch.setenv(LEGACY_ENV, str(legacy_root))
    fx = _facade_fixture()
    _, release = build_source_backed_c11_repository(_stream(fx), fx["projection"])
    assert release.release_ref
    assert _cache_files(legacy_root) == ()


def test_cold_corrupt_cache_is_safe_miss_and_rebuilds(tmp_path, monkeypatch):
    root, _ = _write_policy(tmp_path, monkeypatch)
    fx = _facade_fixture()
    stream = _stream(fx)
    _, baseline = build_source_backed_c11_repository(stream, fx["projection"])
    path, = _cache_files(root)
    path.write_bytes(b"not-a-parquet-cache")
    _, rebuilt = build_source_backed_c11_repository(stream, fx["projection"])
    assert rebuilt.release_ref == baseline.release_ref
    files = _cache_files(root)
    assert len(files) == 1
    import pyarrow.parquet as pq

    assert pq.read_schema(files[0]).metadata[CACHE_METADATA_KEY]


def test_cold_fresh_process_reuses_authorized_cache(tmp_path, monkeypatch):
    root, policy_path = _write_policy(tmp_path, monkeypatch)
    fx = _facade_fixture()
    stream = _stream(fx)
    _, baseline = build_source_backed_c11_repository(stream, fx["projection"])
    path, = _cache_files(root)
    mtime = path.stat().st_mtime_ns
    script = """
from rawlsing_next.tests.test_pre553_w03_w04_cold import _facade_fixture, _stream
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
fx = _facade_fixture()
_, release = build_source_backed_c11_repository(_stream(fx), fx["projection"])
print(release.release_ref.content_hash)
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2])
    env[POLICY_ENV] = str(policy_path)
    env.pop(LEGACY_ENV, None)
    completed = subprocess.run(
        [sys.executable, "-c", script],
        text=True, capture_output=True, check=True, timeout=90, env=env,
    )
    assert completed.stdout.strip() == baseline.release_ref.content_hash
    assert len(_cache_files(root)) == 1
    assert _cache_files(root)[0].stat().st_mtime_ns == mtime


def test_cold_revoked_policy_cannot_return_stale_supported(tmp_path, monkeypatch):
    root, policy_path = _write_policy(tmp_path, monkeypatch)
    fx = _facade_fixture()
    stream = _stream(fx)
    _, baseline = build_source_backed_c11_repository(stream, fx["projection"])
    path, = _cache_files(root)
    path.write_bytes(b"corrupt-before-revocation")
    # Revoke by removing the explicit policy.  No legacy root fallback exists.
    policy_path.unlink()
    _, revoked = build_source_backed_c11_repository(stream, fx["projection"])
    assert revoked.release_ref == baseline.release_ref
    assert _cache_files(root) == (path,)
    # Restoring the policy must treat the corrupt cache as a safe miss and
    # rebuild the exact release, never returning stale material.
    _write_policy(tmp_path, monkeypatch)
    _, restored = build_source_backed_c11_repository(stream, fx["projection"])
    assert restored.release_ref == baseline.release_ref
    files = _cache_files(root)
    assert len(files) == 1
    import pyarrow.parquet as pq

    assert pq.read_schema(files[0]).metadata[CACHE_METADATA_KEY]


def test_cold_cache_hit_preserves_full_typed_i03_i05_material(tmp_path, monkeypatch):
    root, _ = _write_policy(tmp_path, monkeypatch)
    fx = _route_fixture()
    first = _execute(fx)
    assert len(_cache_files(root)) == 1
    second = _execute(fx)
    assert second.c11_release.release_ref == first.c11_release.release_ref
    assert canonical_json(_consumer_material(
        first.repository_binding.executor, fx)) == canonical_json(
        _consumer_material(second.repository_binding.executor, fx))
    assert len(_cache_files(root)) == 1
