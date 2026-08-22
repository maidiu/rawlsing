import hashlib
from pathlib import Path

import pytest

from rawlsing_next.pre553_r5_carrier import (
    R5LongShardedBuilder as V1Builder,
    R5LongShardedReader as V1Reader,
)
from rawlsing_next.pre553_r5_compact_carrier import (
    R5LongShardedBuilder as V2Builder,
    R5LongShardedReader as V2Reader,
)
from rawlsing_next.pre553_r5_codec import canonical_bytes, canonical_json
from rawlsing_next.pre553_r5_model import (
    R5BuildConfig,
    R5CanonicalRow,
    R5IntegrityError,
    R5ReleaseIdentity,
)


def h(value):
    if isinstance(value, str):
        value = value.encode()
    return hashlib.sha256(value).hexdigest()


def identity(tag="compact"):
    return R5ReleaseIdentity(
        release_id=f"REL-{tag}",
        semantic_release_hash=h(f"semantic:{tag}"),
        source_artifact_ref={
            "kind": "SOURCE_ARTIFACT",
            "object_id": f"src:{tag}",
            "content_hash": h(f"source:{tag}"),
        },
        source_release_manifest_hash=h(f"manifest:{tag}"),
        m01_m18_coverage={f"M{i:02d}": (f"proof-{i}",) for i in range(1, 19)},
        decoder_receipt={"decoder": "frozen", "version": "1"},
        compiler_contract_digest=h("compiler"),
        c11_authority_digest=h("c11"),
    )


def generic_rows(n=50):
    for i in range(n):
        payload = {
            "i": i,
            "state": "MISSING" if i % 11 == 0 else "OBSERVED",
            "unique": "u" + str(i) + ("x" * (i % 13)),
        }
        yield R5CanonicalRow(
            "respondent_events" if i % 2 else "empirical_universes",
            "RespondentEvent@1" if i % 2 else "EmpiricalUniverse@1",
            f"urn:r5:{i:08d}",
            h(canonical_json(payload)),
            payload,
        )


def cell_rows(n=10_000, variable_count=613):
    source_sha = h("synthetic-wvs-shaped-source")
    for i in range(n):
        row_no = i // variable_count + 1
        variable_ordinal = i % variable_count
        if i % 7:
            raw_value = {
                "t": "float64_finite",
                "bits": f"{((i * 2654435761) & ((1 << 64) - 1)):016x}",
            }
        else:
            raw_value = {"t": "int", "v": str(i % 11)}
        declaration = None
        if i % 50 == 0:
            declaration = {
                "t": "tuple",
                "v": [{"t": "int", "v": "-1"}],
            }
        label = {"t": "none"} if i % 20 else {"t": "str", "v": "Yes"}
        payload = {
            "seam_version": "PRE553_R5_DECODER_NORMALIZED_SEAM@1.0.0",
            "source_sha256": source_sha,
            "row_ordinal": row_no,
            "variable_ordinal": variable_ordinal,
            "variable_name": f"Q{variable_ordinal}",
            "raw_value": raw_value,
            "missing_state": "OBSERVED" if declaration is None else "USER_MISSING",
            "source_missing_declaration": declaration,
            "raw_value_label": label,
            "explicit_source_coordinates": [row_no, variable_ordinal],
            "source_cell_locator": None,
        }
        yield R5CanonicalRow(
            "source_physical_cells",
            "R5PhysicalCell@1.0.0",
            f"source:{source_sha}:cell:{row_no}:{variable_ordinal}",
            h(canonical_bytes(payload)),
            payload,
        )


def config(**changes):
    values = {
        "run_max_rows": 256,
        "run_max_bytes": 128 * 1024,
        "shard_max_rows": 1024,
        "shard_max_bytes": 512 * 1024,
        "merge_fan_in": 4,
        "verified_spool_memory_bytes": 64 * 1024,
    }
    values.update(changes)
    return R5BuildConfig(**values)


def test_v1_v2_reconstruct_identical_generic_rows_and_logical_digest(tmp_path):
    material = list(generic_rows())
    v1 = tmp_path / "v1"
    v2 = tmp_path / "v2"
    a = V1Builder(config()).build(
        material, release_identity=identity("parity"), target_directory=v1
    )
    b = V2Builder(config()).build(
        material, release_identity=identity("parity"), target_directory=v2
    )
    assert a["logical_stream_digest"] == b["logical_stream_digest"]
    left = list(V1Reader(v1).iter_rows())
    right = list(V2Reader(v2).iter_rows())
    assert left == right == sorted(material, key=lambda row: row.identity_key)


def test_compact_physical_cells_roundtrip_exact_and_recompute_identity(tmp_path):
    material = list(cell_rows(2_000))
    target = tmp_path / "release"
    result = V2Builder(config()).build(
        material, release_identity=identity("cells"), target_directory=target
    )
    reconstructed = list(V2Reader(target).iter_rows())
    assert reconstructed == sorted(material, key=lambda row: row.identity_key)
    assert V2Reader(target).full_audit()["logical_stream_digest"] == result[
        "logical_stream_digest"
    ]


def test_compact_cell_density_synthetic_floor_is_below_wvs_preferred_gate(tmp_path):
    target = tmp_path / "release"
    result = V2Builder().build(
        cell_rows(10_000),
        release_identity=identity("density"),
        target_directory=target,
    )
    # This is only a hostile synthetic regression floor. Authority 63 still
    # requires exact real-WVS prefix measurements before a full-source rerun.
    assert result["canonical_bytes_per_row"] <= 36
    assert result["canonical_steady_state_bytes"] == (
        result["member_bytes"] + result["inventory_bytes"] + result["root_bytes"]
    )


def test_compact_input_reorder_is_byte_deterministic(tmp_path):
    material = list(cell_rows(2_500))
    left = tmp_path / "left"
    right = tmp_path / "right"
    a = V2Builder(config()).build(
        material, release_identity=identity("det"), target_directory=left
    )
    b = V2Builder(config()).build(
        reversed(material), release_identity=identity("det"), target_directory=right
    )
    assert a["logical_stream_digest"] == b["logical_stream_digest"]
    assert a["physical_root_id"] == b["physical_root_id"]
    assert (left / "root.json").read_bytes() == (right / "root.json").read_bytes()
    assert (left / "member_inventory.jsonl").read_bytes() == (
        right / "member_inventory.jsonl"
    ).read_bytes()


def test_compact_relayout_changes_physical_root_not_semantic_stream(tmp_path):
    material = list(cell_rows(2_500))
    left = tmp_path / "left"
    right = tmp_path / "right"
    a = V2Builder(config(shard_max_rows=300)).build(
        material, release_identity=identity("layout"), target_directory=left
    )
    b = V2Builder(config(shard_max_rows=900)).build(
        material, release_identity=identity("layout"), target_directory=right
    )
    assert a["logical_stream_digest"] == b["logical_stream_digest"]
    assert a["physical_root_id"] != b["physical_root_id"]


def test_compact_duplicate_identity_and_member_corruption_fail_closed(tmp_path):
    material = list(cell_rows(100))
    with pytest.raises(R5IntegrityError):
        V2Builder(config()).build(
            material + [material[0]],
            release_identity=identity("dup"),
            target_directory=tmp_path / "duplicate",
        )

    target = tmp_path / "corrupt"
    V2Builder(config()).build(
        material, release_identity=identity("corrupt"), target_directory=target
    )
    reader = V2Reader(target)
    descriptor = next(reader.iter_inventory())
    member = target / "members" / descriptor["member"]
    raw = bytearray(member.read_bytes())
    raw[len(raw) // 2] ^= 1
    member.write_bytes(raw)
    with pytest.raises(R5IntegrityError):
        V2Reader(target).full_audit()


def test_compact_toctou_consumes_authenticated_spool(tmp_path):
    target = tmp_path / "release"
    material = list(cell_rows(100))
    V2Builder(config(shard_max_rows=1000)).build(
        material, release_identity=identity("toctou"), target_directory=target
    )
    mutated = {"done": False}

    def hook(phase, detail):
        if phase == "after_verified_read" and "member-" in detail["path"] and not mutated["done"]:
            path = Path(detail["path"])
            raw = bytearray(path.read_bytes())
            raw[-2] ^= 1
            path.write_bytes(raw)
            mutated["done"] = True

    assert len(list(V2Reader(target, fault_hook=hook).iter_rows())) == len(material)
    with pytest.raises(R5IntegrityError):
        list(V2Reader(target).iter_rows())
