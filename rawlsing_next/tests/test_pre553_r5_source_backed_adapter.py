"""Bounded parity and hostile tests for the Route-A R5 -> C05R2A adapter."""
from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from rawlsing_next.pre553_r5_codec import canonical_bytes
from rawlsing_next.pre553_r5_compact_carrier import (
    R5BuildConfig,
    R5CanonicalRow,
    R5LongShardedBuilder,
    R5LongShardedReader,
    R5ReleaseIdentity,
)
from rawlsing_next.pre553_r5_seam import iter_source_native_rows
from rawlsing_next.pre553_r5_source_backed_adapter import (
    R5SourceBackedAdapterError,
    build_r5_source_backed_c11_repository,
    prepare_r5_exact_physical_cell_stream,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_validated_source_backed_c11_release,
)
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture


def _h(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def _identity(fx, *, tag: str, source_sha: str | None = None) -> R5ReleaseIdentity:
    native = build_validated_source_backed_c11_release(fx["incidence"], fx["projection"])
    source_ref = native.source_artifact_ref.as_dict()
    if source_sha is not None:
        source_ref = {**source_ref, "content_hash": source_sha}
    return R5ReleaseIdentity(
        release_id=native.release_id,
        semantic_release_hash=native.semantic_release_hash,
        source_artifact_ref=source_ref,
        source_release_manifest_hash=native.source_release_manifest_hash,
        m01_m18_coverage={k: tuple(v) for k, v in native.m01_m18_coverage.items()},
        decoder_receipt={"bounded_fixture": tag},
        compiler_contract_digest=_h(f"compiler:{tag}"),
        c11_authority_digest=_h(f"c11:{tag}"),
    )


def _reader(tmp_path, fx, *, rows=None, identity=None, name="r5"):
    target = tmp_path / name
    rows = tuple(iter_source_native_rows(fx["incidence"])) if rows is None else tuple(rows)
    telemetry = R5LongShardedBuilder(
        R5BuildConfig(
            run_max_rows=4,
            run_max_bytes=4096,
            shard_max_rows=8,
            shard_max_bytes=16384,
            merge_fan_in=2,
            verified_spool_memory_bytes=4096,
        )
    ).build(
        rows,
        release_identity=identity or _identity(fx, tag=name),
        target_directory=target,
    )
    return R5LongShardedReader(
        target, expected_physical_root_id=telemetry["physical_root_id"]
    )


def _replace_first_cell(rows, mutation):
    output = []
    done = False
    for row in rows:
        if not done and row.relation == "source_physical_cells":
            payload = dict(row.payload)
            mutation(payload)
            output.append(
                R5CanonicalRow(
                    row.relation,
                    row.object_family,
                    row.object_id,
                    hashlib.sha256(canonical_bytes(payload)).hexdigest(),
                    payload,
                )
            )
            done = True
        else:
            output.append(row)
    assert done
    return tuple(output)


def test_r5_reopened_cells_match_decoder_cells_and_c05r2a_release_replay_exactly(tmp_path):
    fx = _fixture("r5-route-a-parity")
    reader = _reader(tmp_path, fx)
    stream, descriptor = prepare_r5_exact_physical_cell_stream(
        reader, expected_source_sha256=fx["source_sha"]
    )
    assert descriptor.source_sha256 == fx["source_sha"]
    assert descriptor.row_count == fx["incidence"].row_count
    assert descriptor.variable_count == len(fx["incidence"].variables)
    assert tuple(stream.iter_cells()) == fx["cells"]

    native = build_validated_source_backed_c11_release(
        fx["incidence"], fx["projection"]
    )
    repo, adapted, descriptor2 = build_r5_source_backed_c11_repository(
        reader, fx["projection"]
    )
    assert descriptor2 == descriptor
    assert adapted.release_ref == native.release_ref
    assert adapted.replay_manifest.ref == native.replay_manifest.ref
    assert tuple(x.ref for x in adapted.public_objects) == tuple(
        x.ref for x in native.public_objects
    )
    assert tuple(x.ref for x in adapted.internal_records) == tuple(
        x.ref for x in native.internal_records
    )
    assert repo.resolve_release_exact(adapted.release_ref).release_ref == native.release_ref


def test_two_independent_bounded_r5_builds_replay_to_identical_c11_identities(tmp_path):
    fx = _fixture("r5-route-a-replay")
    shared_identity = _identity(fx, tag="replay")
    left = _reader(tmp_path, fx, name="left", identity=shared_identity)
    right = _reader(tmp_path, fx, name="right", identity=shared_identity)
    _, lrelease, ldesc = build_r5_source_backed_c11_repository(left, fx["projection"])
    _, rrelease, rdesc = build_r5_source_backed_c11_repository(right, fx["projection"])
    assert ldesc.physical_root_id == rdesc.physical_root_id
    assert ldesc.logical_stream_digest == rdesc.logical_stream_digest
    assert lrelease.release_ref == rrelease.release_ref
    assert lrelease.replay_manifest.ref == rrelease.replay_manifest.ref


def test_source_identity_mismatch_fails_closed_before_c05r2a(tmp_path):
    fx = _fixture("r5-route-a-stale")
    bad_sha = _h("wrong-source")
    reader = _reader(
        tmp_path,
        fx,
        identity=_identity(fx, tag="stale", source_sha=bad_sha),
    )
    with pytest.raises(R5SourceBackedAdapterError):
        prepare_r5_exact_physical_cell_stream(reader)
    with pytest.raises(R5SourceBackedAdapterError):
        build_r5_source_backed_c11_repository(reader, fx["projection"])


def test_noncanonical_typed_raw_value_fails_closed(tmp_path):
    fx = _fixture("r5-route-a-noncanonical")
    rows = tuple(iter_source_native_rows(fx["incidence"]))
    rows = _replace_first_cell(
        rows, lambda p: p.__setitem__("raw_value", {"t": "none", "junk": 1})
    )
    reader = _reader(tmp_path, fx, rows=rows)
    stream, _ = prepare_r5_exact_physical_cell_stream(reader)
    with pytest.raises(R5SourceBackedAdapterError):
        tuple(stream.iter_cells())


def test_unknown_physical_state_fails_closed_during_audit(tmp_path):
    fx = _fixture("r5-route-a-state")
    rows = tuple(iter_source_native_rows(fx["incidence"]))
    rows = _replace_first_cell(
        rows, lambda p: p.__setitem__("missing_state", "BOGUS_STATE")
    )
    reader = _reader(tmp_path, fx, rows=rows)
    with pytest.raises(R5SourceBackedAdapterError):
        prepare_r5_exact_physical_cell_stream(reader)


def test_missing_physical_cell_fails_closed_on_geometry_binding(tmp_path):
    fx = _fixture("r5-route-a-incomplete")
    rows = list(iter_source_native_rows(fx["incidence"]))
    dropped = False
    kept = []
    for row in rows:
        if not dropped and row.relation == "source_physical_cells":
            dropped = True
            continue
        kept.append(row)
    assert dropped
    reader = _reader(tmp_path, fx, rows=kept)
    with pytest.raises(R5SourceBackedAdapterError):
        prepare_r5_exact_physical_cell_stream(reader)


def test_wrong_cell_family_under_physical_relation_fails_closed(tmp_path):
    fx = _fixture("r5-route-a-family")
    rows = list(iter_source_native_rows(fx["incidence"]))
    for index, row in enumerate(rows):
        if row.relation == "source_physical_cells":
            rows[index] = R5CanonicalRow(
                row.relation,
                "WrongPhysicalCell@1.0.0",
                row.object_id,
                row.content_hash,
                row.payload,
            )
            break
    reader = _reader(tmp_path, fx, rows=rows)
    with pytest.raises(R5SourceBackedAdapterError):
        prepare_r5_exact_physical_cell_stream(reader)


def test_projection_source_mismatch_fails_closed(tmp_path):
    fx = _fixture("r5-route-a-projection-mismatch")
    reader = _reader(tmp_path, fx)
    bad_sha = _h("projection-mismatch")
    bad_projection = replace(
        fx["projection"],
        expected_source_sha256=bad_sha,
        source_snapshot_retention_ref=replace(
            fx["projection"].source_snapshot_retention_ref,
            content_hash=bad_sha,
        ),
    )
    with pytest.raises(R5SourceBackedAdapterError):
        build_r5_source_backed_c11_repository(reader, bad_projection)
