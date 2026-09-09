#!/usr/bin/env python3
"""Materialize the 66 WVS7 D12 source scopes as source-local EmpiricalUniverse objects.

Population certification is deliberately outside this materializer.  The only
positive claim here is exact source-scope existence under D12 replay identity.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_c11_integrity import validate_public_carrier_object
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_source_local_universe_admission import (
    ADMISSION_OPERATION,
    AUTHORITY_KIND,
    CLAIM_CEILING,
    CONTRACT_ID as SOURCE_LOCAL_CONTRACT_ID,
    DocumentaryField,
    REQUIRED_NEGATIVE_LIMIT_REFS,
    SourceLocalUniverseSpec,
    materialize_source_local_universe,
    validate_source_local_universe,
)

BUILD_CONTRACT_ID = "WVS7_D11_SOURCE_LOCAL_66_MATERIALIZER_R1@1.0.0"
EXPECTED_SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
EXPECTED_LEDGER_PRODUCER_SHA256 = "cf0dfaae7a2f0f19b34ccc536b93e6aedbf37bf047d5d864e5c812fe9602d6a9"
EXPECTED_LEDGER_CHECKOUT_SHA256 = "cd17c8efbe7492dd23e9654fa4a507b56edb8984b62272e58596a432ad34a8a4"
EXPECTED_LEDGER_GIT_BLOB_SHA1 = "4875b9499dee06dfaa6dd6182656c3d55c2c4ce1"
EXPECTED_SCOPE_COUNT = 66
EXPECTED_ROW_COUNT = 97220
EXPECTED_D12_REPLAY_ID = (
    "urn:rawlsing:pre553:gsr07:wvs7:d12-scoped-respondent-replay:"
    "sha256:9d44d5097258b96c5c49faf968b85701f80ecd75df6b214a528abb6fb15ef44b"
)
EXPECTED_D12_REPLAY_HASH = "9d44d5097258b96c5c49faf968b85701f80ecd75df6b214a528abb6fb15ef44b"
SCOPE_CONTRACT = "PRE553_WVS7_SOURCE_SCOPE_MEMBER_SET@1.0.0"
IDENTITY_PROTOCOL = "SOURCE_SHA256_PLUS_SOURCE_ROW_ORDINAL"
SCOPE_KEY = "S025_PLUS_B_COUNTR_PLUS_A_YEAR"


class WVS7SourceLocalBuildError(ValueError):
    pass


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha_file(path: Path) -> str:
    return _sha_bytes(path.read_bytes())


def _git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\\x00"
    return hashlib.sha1(header + data).hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(
        kind,
        f"urn:rawlsing:pre553:wvs7:d11-source-local:{namespace}:sha256:{digest}",
        digest,
    )


def _source_ref() -> ExactRef:
    return ExactRef(
        "SOURCE_ARTIFACT",
        f"urn:rawlsing:pre553:wvs7:wave7-sav:sha256:{EXPECTED_SOURCE_SHA256}",
        EXPECTED_SOURCE_SHA256,
    )


def _d12_replay_ref() -> ExactRef:
    return ExactRef(
        "SCOPED_RESPONDENT_REPLAY",
        EXPECTED_D12_REPLAY_ID,
        EXPECTED_D12_REPLAY_HASH,
    )


def _protocol_ref() -> ExactRef:
    material = {
        "build_contract": BUILD_CONTRACT_ID,
        "source_local_contract": SOURCE_LOCAL_CONTRACT_ID,
        "identity_protocol": IDENTITY_PROTOCOL,
        "scope_key": SCOPE_KEY,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "d12_replay_ref": _d12_replay_ref().as_dict(),
    }
    return _ref("REPLAY_PROTOCOL", "materializer-protocol", material)


def _scope_ref(row: Mapping[str, str]) -> ExactRef:
    return ExactRef(
        "SOURCE_SCOPE_MEMBER_SET",
        row["source_scope_member_set_ref"],
        row["source_scope_member_set_hash"],
    )


def _scope_material(row: Mapping[str, str]) -> Mapping[str, Any]:
    return {
        "S025": int(row["S025"]),
        "B_COUNTR": int(row["B_COUNTR"]),
        "A_YEAR": int(row["A_YEAR"]),
        "source_row_ordinal_first": int(row["source_row_ordinal_first"]),
        "source_row_ordinal_last": int(row["source_row_ordinal_last"]),
        "member_count": int(row["member_count"]),
        "ordered_member_binding_digest": row["ordered_member_binding_digest"],
        "source_scope_member_set_ref": _scope_ref(row).as_dict(),
    }


def _authority_for_scope(
    row: Mapping[str, str],
    *,
    source_ref: ExactRef,
    replay_ref: ExactRef,
    ledger_ref: ExactRef,
) -> AuthoritySnapshot:
    scope_ref = _scope_ref(row)
    scope_material = _scope_material(row)
    dependencies = tuple(sorted(
        {source_ref, scope_ref, replay_ref, ledger_ref},
        key=lambda ref: ref.key,
    ))
    scope_envelope = {
        "claim_ceiling": CLAIM_CEILING,
        "population_generalization": "DENIED_UNLESS_SEPARATELY_AUTHORIZED",
        "default_measure_ceiling": "RAW_ONLY",
        "source_artifact_ref": source_ref,
        "respondent_scope_ref": scope_ref,
        "replay_scope_ref": replay_ref,
        "source_native_scope_identity": {
            "scope_key": SCOPE_KEY,
            "S025": scope_material["S025"],
            "B_COUNTR": scope_material["B_COUNTR"],
            "A_YEAR": scope_material["A_YEAR"],
        },
    }
    authority_id = (
        "WVS7-D11-SOURCE-LOCAL-"
        f"S025-{scope_material['S025']}-"
        f"B-{scope_material['B_COUNTR']}-"
        f"Y-{scope_material['A_YEAR']}"
    )
    authority_material = {
        "build_contract": BUILD_CONTRACT_ID,
        "source_local_contract": SOURCE_LOCAL_CONTRACT_ID,
        "authority_id": authority_id,
        "authority_kind": AUTHORITY_KIND,
        "operation": ADMISSION_OPERATION,
        "governed_family": "EmpiricalUniverse@1.0.0",
        "scope_envelope": scope_envelope,
        "dependencies": [ref.as_dict() for ref in dependencies],
        "negative_limit_refs": [
            ref.as_dict() for ref in REQUIRED_NEGATIVE_LIMIT_REFS
        ],
        "d12_scope_material": scope_material,
    }
    authority_hash = semantic_hash(authority_material)
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=dependencies,
        producer_replay_locator_or_reference_root=_ref(
            "AUTHORITY_REPLAY_ROOT",
            f"authority-{scope_material['S025']}",
            authority_material,
        ),
        authority_id=authority_id,
        authority_version="1.0.0",
        authority_content_hash=authority_hash,
        authority_kind=AUTHORITY_KIND,
        decision_state="ALLOW",
        governed_operations=(ADMISSION_OPERATION,),
        governed_object_families=("EmpiricalUniverse@1.0.0",),
        scope_envelope=scope_envelope,
        effective_time_or_interval={"A_YEAR": scope_material["A_YEAR"]},
        parent_authority_refs=(),
        negative_limit_refs=REQUIRED_NEGATIVE_LIMIT_REFS,
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash({
            "authority_material": authority_material,
            "population_permission": False,
            "weighted_population_permission": False,
            "pooling_permission": False,
            "backfill_permission": False,
        }),
        replay_protocol_ref=_protocol_ref(),
    )


def _spec_for_scope(
    row: Mapping[str, str],
    *,
    source_ref: ExactRef,
    replay_ref: ExactRef,
    ledger_ref: ExactRef,
) -> SourceLocalUniverseSpec:
    scope_ref = _scope_ref(row)
    scope = _scope_material(row)
    source_native = {
        "scope_key": SCOPE_KEY,
        "S025": scope["S025"],
        "B_COUNTR": scope["B_COUNTR"],
        "A_YEAR": scope["A_YEAR"],
        "claim_ceiling": "SOURCE_NATIVE_SCOPE_IDENTITY_ONLY",
    }
    lineage = {
        "build_contract": BUILD_CONTRACT_ID,
        "d12_worker_tip": "e404bc097f48a09265f1aec06e3d011a892f69c4",
        "source_artifact_ref": source_ref.as_dict(),
        "scope_ledger_ref": ledger_ref.as_dict(),
        "source_scope_member_set_ref": scope_ref.as_dict(),
        "d12_replay_ref": replay_ref.as_dict(),
        "source_row_ordinal_first": scope["source_row_ordinal_first"],
        "source_row_ordinal_last": scope["source_row_ordinal_last"],
        "member_count": scope["member_count"],
        "ordered_member_binding_digest": scope["ordered_member_binding_digest"],
        "identity_protocol": IDENTITY_PROTOCOL,
    }
    return SourceLocalUniverseSpec(
        raw_source_identity=f"WVS Wave 7.sav@sha256:{EXPECTED_SOURCE_SHA256}",
        source_family="WVS",
        study_product_release=(
            f"WVS/WAVE7/S025={scope['S025']}/"
            f"B_COUNTR={scope['B_COUNTR']}/A_YEAR={scope['A_YEAR']}"
        ),
        instrument_release="WVS_WAVE7_SOURCE_LOCAL_BASE_R1",
        country_geography=source_native,
        sampling_geography={
            "scope_key": SCOPE_KEY,
            "B_COUNTR": scope["B_COUNTR"],
            "claim_ceiling": "SOURCE_NATIVE_SCOPE_IDENTITY_ONLY",
        },
        raw_wave="7",
        canonical_wave_if_governed=None,
        field_or_reference_time={"A_YEAR": scope["A_YEAR"]},
        respondent_namespace=(
            "PRE553_WVS7_SCOPED_RESPONDENT@1.0.0|"
            + scope_ref.object_id
        ),
        source_artifact_import_lineage=lineage,
        source_artifact_ref=source_ref,
        respondent_scope_ref=scope_ref,
        replay_scope_ref=replay_ref,
        target_population_and_sample_frame=DocumentaryField.not_population_certified(
            "WVS7_D11_SOURCE_LOCAL_BASE__POPULATION_TARGET_FRAME_REQUIRES_SEPARATE_OVERLAY"
        ),
        sampling_design_regime=DocumentaryField.not_population_certified(
            "WVS7_D11_SOURCE_LOCAL_BASE__SAMPLING_DESIGN_REQUIRES_SEPARATE_OVERLAY"
        ),
        additional_dependency_refs=(ledger_ref,),
    )


def _load_inputs(
    root: Path,
) -> tuple[list[dict[str, str]], Mapping[str, Any], str, str, str, str]:
    ledger_path = root / "D12_COUNTRY_SOURCE_SCOPE_ROW_RANGES.csv"
    manifest_path = root / "D12_SCOPED_RESPONDENT_REPLAY_MANIFEST.json"

    # D12 recorded the CSV SHA from Python csv.DictWriter's CRLF worktree
    # bytes before Git normalized text to LF on commit.  Preserve both exact
    # identities rather than pretending the producer receipt and Git blob are
    # the same byte representation.
    ledger_checkout_bytes = ledger_path.read_bytes()
    ledger_checkout_sha = _sha_bytes(ledger_checkout_bytes)
    if ledger_checkout_sha != EXPECTED_LEDGER_CHECKOUT_SHA256:
        raise WVS7SourceLocalBuildError(
            f"D12 normalized checkout SHA mismatch: {ledger_checkout_sha}"
        )
    ledger_git_blob_sha1 = _git_blob_sha1(ledger_checkout_bytes)
    if ledger_git_blob_sha1 != EXPECTED_LEDGER_GIT_BLOB_SHA1:
        raise WVS7SourceLocalBuildError(
            f"D12 Git blob identity mismatch: {ledger_git_blob_sha1}"
        )
    if b"\\r" in ledger_checkout_bytes:
        raise WVS7SourceLocalBuildError(
            "D12 Git-normalized ledger unexpectedly contains carriage returns"
        )
    ledger_producer_bytes = ledger_checkout_bytes.replace(b"\\n", b"\\r\\n")
    ledger_producer_sha = _sha_bytes(ledger_producer_bytes)
    if ledger_producer_sha != EXPECTED_LEDGER_PRODUCER_SHA256:
        raise WVS7SourceLocalBuildError(
            f"D12 producer-worktree ledger SHA mismatch: {ledger_producer_sha}"
        )

    manifest_bytes = manifest_path.read_bytes()
    manifest_sha = _sha_bytes(manifest_bytes)
    manifest = json.loads(manifest_bytes)
    source = manifest["source"]
    if (
        source["source_sha256"] != EXPECTED_SOURCE_SHA256
        or int(source["rows"]) != EXPECTED_ROW_COUNT
    ):
        raise WVS7SourceLocalBuildError("D12 compact manifest source identity drift")
    partition = manifest["source_scope_partition"]
    if (
        partition["scope_key"] != SCOPE_KEY
        or int(partition["scope_count"]) != EXPECTED_SCOPE_COUNT
        or int(partition["row_count"]) != EXPECTED_ROW_COUNT
        or partition["ledger_sha256"] != EXPECTED_LEDGER_PRODUCER_SHA256
        or partition["coverage"] != "EXACTLY_ALL_SOURCE_ROWS_ONCE"
    ):
        raise WVS7SourceLocalBuildError("D12 source-scope partition drift")
    replay = manifest["replay_ref"]
    if (
        replay["object_id"] != EXPECTED_D12_REPLAY_ID
        or replay["content_hash"] != EXPECTED_D12_REPLAY_HASH
    ):
        raise WVS7SourceLocalBuildError("D12 replay identity drift")

    with ledger_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != EXPECTED_SCOPE_COUNT:
        raise WVS7SourceLocalBuildError("D12 ledger scope count drift")

    rows.sort(key=lambda row: int(row["source_row_ordinal_first"]))
    expected_first = 1
    total = 0
    seen_scope_refs: set[str] = set()
    for row in rows:
        first = int(row["source_row_ordinal_first"])
        last = int(row["source_row_ordinal_last"])
        count = int(row["member_count"])
        if first != expected_first or last - first + 1 != count:
            raise WVS7SourceLocalBuildError("D12 ledger row-range partition drift")
        expected_first = last + 1
        total += count
        scope_key = _scope_ref(row).key
        if scope_key in seen_scope_refs:
            raise WVS7SourceLocalBuildError("duplicate D12 source scope ref")
        seen_scope_refs.add(scope_key)
    if expected_first != EXPECTED_ROW_COUNT + 1 or total != EXPECTED_ROW_COUNT:
        raise WVS7SourceLocalBuildError("D12 ledger does not cover all rows exactly once")
    return (
        rows,
        manifest,
        ledger_producer_sha,
        ledger_checkout_sha,
        ledger_git_blob_sha1,
        manifest_sha,
    )


def build(output_dir: Path) -> Mapping[str, Any]:
    root = Path(__file__).resolve().parent
    (
        rows,
        manifest,
        ledger_producer_sha,
        ledger_checkout_sha,
        ledger_git_blob_sha1,
        manifest_sha,
    ) = _load_inputs(root)
    output_dir.mkdir(parents=True, exist_ok=True)

    source_ref = _source_ref()
    replay_ref = _d12_replay_ref()
    ledger_ref = ExactRef(
        "WVS7_D12_SOURCE_SCOPE_LEDGER",
        f"urn:rawlsing:pre553:wvs7:d12-source-scope-ledger:sha256:{ledger_producer_sha}",
        ledger_producer_sha,
    )

    authority_rows: list[Mapping[str, Any]] = []
    universe_rows: list[Mapping[str, Any]] = []
    total_members = 0

    for row in rows:
        scope = _scope_material(row)
        authority = _authority_for_scope(
            row,
            source_ref=source_ref,
            replay_ref=replay_ref,
            ledger_ref=ledger_ref,
        )
        registry = AuthorityRegistry((authority,))
        spec = _spec_for_scope(
            row,
            source_ref=source_ref,
            replay_ref=replay_ref,
            ledger_ref=ledger_ref,
        )
        universe = materialize_source_local_universe(
            spec=spec,
            admission_authority=authority,
            authority_registry=registry,
        )
        validate_source_local_universe(universe, registry)
        validate_public_carrier_object(universe, registry)

        authority_rows.append({
            "scope": scope,
            "authority": authority.as_dict(),
        })
        universe_rows.append({
            "scope": scope,
            "universe": universe.as_dict(),
        })
        total_members += scope["member_count"]

    if len(authority_rows) != EXPECTED_SCOPE_COUNT or len(universe_rows) != EXPECTED_SCOPE_COUNT:
        raise WVS7SourceLocalBuildError("output scope count drift")
    if total_members != EXPECTED_ROW_COUNT:
        raise WVS7SourceLocalBuildError("output member count drift")

    authorities_path = output_dir / "SOURCE_LOCAL_ADMISSION_AUTHORITIES.json"
    universes_path = output_dir / "SOURCE_LOCAL_EMPIRICAL_UNIVERSES.json"
    _write_json(authorities_path, {
        "schema": "wvs7-d11-source-local-admission-authorities-r1",
        "build_contract": BUILD_CONTRACT_ID,
        "source_local_contract": SOURCE_LOCAL_CONTRACT_ID,
        "scope_count": EXPECTED_SCOPE_COUNT,
        "authorities": authority_rows,
    })
    _write_json(universes_path, {
        "schema": "wvs7-d11-source-local-empirical-universes-r1",
        "build_contract": BUILD_CONTRACT_ID,
        "source_local_contract": SOURCE_LOCAL_CONTRACT_ID,
        "scope_count": EXPECTED_SCOPE_COUNT,
        "total_members": total_members,
        "universes": universe_rows,
    })

    authority_refs = [
        row["authority"]["object_id"] + "|" + row["authority"]["content_hash"]
        for row in authority_rows
    ]
    universe_refs = [
        row["universe"]["object_id"] + "|" + row["universe"]["content_hash"]
        for row in universe_rows
    ]
    receipt = {
        "schema": "wvs7-d11-source-local-66-build-receipt-r1",
        "build_contract": BUILD_CONTRACT_ID,
        "source_local_contract": SOURCE_LOCAL_CONTRACT_ID,
        "qualification_state": "SINGLE_BUILD__OUTER_PROCESS_PARITY_REQUIRED",
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "d12_ledger_producer_sha256": ledger_producer_sha,
        "d12_ledger_checkout_sha256": ledger_checkout_sha,
        "d12_ledger_git_blob_sha1": ledger_git_blob_sha1,
        "d12_compact_manifest_sha256": manifest_sha,
        "d12_replay_ref": replay_ref.as_dict(),
        "scope_count": len(universe_rows),
        "total_members": total_members,
        "authority_ref_set_hash": semantic_hash(authority_refs),
        "universe_ref_set_hash": semantic_hash(universe_refs),
        "authorities_file_sha256": _sha_file(authorities_path),
        "universes_file_sha256": _sha_file(universes_path),
        "materializer_sha256": _sha_file(Path(__file__).resolve()),
        "required_negative_limit_refs": [
            ref.as_dict() for ref in REQUIRED_NEGATIVE_LIMIT_REFS
        ],
        "population_generalization_permissions": 0,
        "weighted_population_permissions": 0,
        "pooling_permissions": 0,
        "backfill_permissions": 0,
        "harmonization_permissions": 0,
    }
    _write_json(output_dir / "SOURCE_LOCAL_66_REPLAY_PARITY_RECEIPT.json", receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    receipt = build(args.output_dir)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
