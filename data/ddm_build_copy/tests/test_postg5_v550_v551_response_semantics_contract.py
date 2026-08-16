from __future__ import annotations

import hashlib
import json
import pandas as pd
import pytest

from data.ddm_build_copy.ddm_v550_response_semantics_authority import (
    BINDING_MANIFEST_PATH,
    BINDING_PATH,
    EXPECTED_ACTIVE_BINDINGS,
    EXPECTED_DISTINCT_CONTRACTS,
    assert_v551_applicable_contract_compatibility,
    bind_governed_response_semantics_contracts,
    load_response_semantics_contract_bindings,
    load_v551_registry_key_set,
    lookup_governed_response_semantics_contract,
    response_option_map_content_sha256,
)
from data.ddm_build_copy.ddm_v550_response_options import response_semantics_contract_hash


LEGACY_SEMANTIC_COLUMNS = [
    "source",
    "wave",
    "canonical_wave",
    "var_name",
    "var_code",
    "value_code_normalized",
    "value_label_clean",
    "option_group",
    "is_substantive",
    "is_missing",
    "is_dk",
    "is_refusal",
    "is_iap",
    "is_not_asked",
    "is_inapplicable",
    "response_family",
    "response_direction",
    "response_intensity",
    "polarity",
    "ordinal_rank",
    "scale_min",
    "scale_max",
    "scale_direction",
    "directionality_status",
    "normalization_confidence",
]


def _legacy_whole_frame_response_semantics_hash(frame: pd.DataFrame) -> str:
    if frame.empty:
        payload = {"rows": 0, "columns": []}
    else:
        available = [column for column in LEGACY_SEMANTIC_COLUMNS if column in frame.columns]
        semantic_frame = frame.loc[:, available].copy() if available else pd.DataFrame()
        if not semantic_frame.empty:
            semantic_frame = semantic_frame.fillna("").astype(str)
            semantic_frame = semantic_frame.sort_values(list(semantic_frame.columns)).reset_index(drop=True)
            payload = {
                "rows": int(len(semantic_frame)),
                "columns": list(semantic_frame.columns),
                "records": semantic_frame.to_dict(orient="records"),
            }
        else:
            payload = {"rows": int(len(frame)), "columns": list(frame.columns)}
    raw = json.dumps(
        payload, sort_keys=True, ensure_ascii=False, default=str
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


AFRO_R1 = {
    "dememp": "44c656ab1aeccb1e0e7b1254f01360f985fbd8dc99be9c8751bac37bd43ba1ab",
    "pfeerd": "6556e971af90c8fd34f037d246a831f830210b9afce8c9bc5f98056219711c02",
    "pfgmp": "d336e6df62d10a1ab7f7a95d8e10570cdf2cf710f6d33a84b469e2c5e53c9fc6",
    "pfpcrm": "cc4b9b3bd5b9a2fc7baac282806293339a97700c472905b1dbc881aba82dd5c1",
    "pfpsaf": "4f866275c55d455e06c7de56d7e7f93f767473e98e5abaa0394ff459c0fae2e1",
    "pfrass": "5c1fda086920cdd45776a9e5ecbce63c67358c2c45525fbd3e1f5247c2f553a3",
}


def _rows(var_code: str, substantive_count: int, *, special: int = 0) -> pd.DataFrame:
    rows = []
    for idx in range(substantive_count):
        rows.append(
            {
                "source": "Afrobarometer",
                "source_family": "Afrobarometer",
                "wave": "R1",
                "canonical_wave": "R1",
                "var_name": var_code,
                "var_code": var_code,
                "question_id": f"Afrobarometer:R1:{var_code}",
                "value_code_normalized": str(idx + 1),
                "value_label_clean": f"substantive {idx + 1}",
                "option_group": "substantive",
                "is_substantive": True,
                "is_missing": False,
                "response_direction": "negative" if idx < substantive_count / 2 else "positive",
                "response_intensity": str(idx / max(substantive_count - 1, 1)),
                "response_family": "ordinal_scale",
                "response_semantics_contract_hash": "",
                "response_semantics_status": "",
                "response_semantics_source": "",
                "manual_review_flag": False,
                "manual_review_reason": "",
            }
        )
    for idx in range(special):
        rows.append(
            {
                "source": "Afrobarometer",
                "source_family": "Afrobarometer",
                "wave": "R1",
                "canonical_wave": "R1",
                "var_name": var_code,
                "var_code": var_code,
                "question_id": f"Afrobarometer:R1:{var_code}",
                "value_code_normalized": str(90 + idx),
                "value_label_clean": "don't know",
                "option_group": "special",
                "is_substantive": False,
                "is_missing": True,
                "response_direction": "",
                "response_intensity": "",
                "response_family": "ordinal_scale",
                "response_semantics_contract_hash": "",
                "response_semantics_status": "",
                "response_semantics_source": "",
                "manual_review_flag": False,
                "manual_review_reason": "",
            }
        )
    return pd.DataFrame(rows)


def test_binding_authority_matches_frozen_v551_registry_key_set_mechanically():
    bindings = load_response_semantics_contract_bindings()
    registry_keys = load_v551_registry_key_set()

    emitted = {binding.response_semantics_contract_hash for binding in bindings.values()}
    assert len(bindings) == EXPECTED_ACTIVE_BINDINGS == 236
    assert len(emitted) == EXPECTED_DISTINCT_CONTRACTS == 145
    assert emitted == set(registry_keys)


def test_legacy_live_build_whole_frame_hash_cannot_be_v551_exact_contract_key():
    frame = pd.concat([_rows("dememp", 4), _rows("pfeerd", 5)], ignore_index=True)
    legacy_hash = _legacy_whole_frame_response_semantics_hash(frame)
    legacy_stamped = frame.copy()
    legacy_stamped["response_semantics_contract_hash"] = legacy_hash

    assert legacy_stamped["response_semantics_contract_hash"].nunique() == 1
    assert legacy_hash not in load_v551_registry_key_set()
    assert legacy_hash not in {AFRO_R1["dememp"], AFRO_R1["pfeerd"]}
    assert AFRO_R1["dememp"] != AFRO_R1["pfeerd"]


def test_whole_frame_content_hash_is_artifact_identity_not_v551_contract_key():
    frame = pd.concat([_rows("dememp", 4), _rows("pfeerd", 5)], ignore_index=True)
    whole_frame_hash = response_option_map_content_sha256(frame)

    assert whole_frame_hash not in load_v551_registry_key_set()
    assert whole_frame_hash not in set(AFRO_R1.values())
    assert response_semantics_contract_hash(frame) == ""


def test_live_binding_attaches_exact_frozen_contract_identity():
    frame = _rows("dememp", 4, special=3)
    bound, summary = bind_governed_response_semantics_contracts(frame, live_build=True)

    assert summary["bound_groups"] == 1
    assert set(bound["response_semantics_contract_hash"]) == {AFRO_R1["dememp"]}
    assert set(bound["response_semantics_authority_status"]) == {"CERTIFIED"}
    assert set(bound["response_semantics_status"]) == {"CERTIFIED_GOVERNED_CONTRACT"}


def test_special_rows_inherit_packet_identity_without_creating_scale_contract():
    frame = _rows("dememp", 4, special=2)
    bound, _ = bind_governed_response_semantics_contracts(frame, live_build=True)

    specials = bound[~bound["is_substantive"]]
    assert len(specials) == 2
    assert set(specials["response_semantics_contract_hash"]) == {AFRO_R1["dememp"]}
    assert specials["response_direction"].eq("").all()
    assert specials["response_intensity"].eq("").all()


def test_unknown_or_incomplete_governed_semantics_fail_closed():
    frame = _rows("dememp", 3)
    bound, summary = bind_governed_response_semantics_contracts(frame, live_build=True)

    assert summary["review_required_groups"] == 1
    assert bound["response_semantics_contract_hash"].eq("").all()
    assert bound["manual_review_flag"].all()
    assert set(bound["response_semantics_authority_status"]) == {"REVIEW_REQUIRED"}
    assert bound["manual_review_reason"].str.contains(
        "governed_response_semantics_substantive_count_mismatch"
    ).all()


def test_prebuilt_exact_governed_identity_is_preserved():
    frame = _rows("dememp", 4, special=1)
    frame["response_semantics_contract_hash"] = AFRO_R1["dememp"]
    frame["response_semantics_authority_status"] = "CERTIFIED"

    bound, summary = bind_governed_response_semantics_contracts(frame, live_build=False)

    assert summary["preserved_groups"] == 1
    assert summary["unresolved_groups"] == 0
    assert set(bound["response_semantics_contract_hash"]) == {AFRO_R1["dememp"]}


def test_bound_applicable_rows_pass_mechanical_v551_consumer_key_check():
    frame = pd.concat([_rows("dememp", 4), _rows("pfeerd", 5)], ignore_index=True)
    bound, summary = bind_governed_response_semantics_contracts(frame, live_build=True)
    assert summary["unresolved_groups"] == 0

    result = assert_v551_applicable_contract_compatibility(bound)
    assert result == {"applicable_groups": 2, "unresolved_groups": 0}


def test_prebuilt_conflicting_identity_fails_closed_instead_of_family_fallback():
    frame = _rows("dememp", 4)
    frame["response_semantics_contract_hash"] = AFRO_R1["pfeerd"]

    bound, summary = bind_governed_response_semantics_contracts(frame, live_build=False)

    assert summary["review_required_groups"] == 1
    assert bound["response_semantics_contract_hash"].eq("").all()
    assert bound["manual_review_flag"].all()


def test_distinct_governed_contracts_do_not_collapse_and_lookup_is_deterministic():
    dememp = lookup_governed_response_semantics_contract("Afrobarometer", "R1", "dememp")
    pfeerd = lookup_governed_response_semantics_contract("Afrobarometer", "R1", "pfeerd")
    dememp_again = lookup_governed_response_semantics_contract(
        "Afrobarometer", "R1", "dememp"
    )

    assert dememp is not None and pfeerd is not None
    assert dememp.response_semantics_contract_hash == AFRO_R1["dememp"]
    assert pfeerd.response_semantics_contract_hash == AFRO_R1["pfeerd"]
    assert dememp.response_semantics_contract_hash != pfeerd.response_semantics_contract_hash
    assert dememp_again == dememp


def test_authority_packet_identity_can_be_shared_without_being_inferred_from_family():
    bindings = list(load_response_semantics_contract_bindings().values())
    counts: dict[str, int] = {}
    for binding in bindings:
        counts[binding.response_semantics_contract_hash] = (
            counts.get(binding.response_semantics_contract_hash, 0) + 1
        )
    repeated = {key for key, count in counts.items() if count > 1}
    assert repeated
    assert repeated.issubset(load_v551_registry_key_set())


def test_binding_manifest_keeps_artifact_hash_separate_from_semantic_identity():
    manifest = json.loads(BINDING_MANIFEST_PATH.read_text(encoding="utf-8"))
    artifact_hash = manifest["binding_file_sha256"]
    semantic_hashes = {
        binding.response_semantics_contract_hash
        for binding in load_response_semantics_contract_bindings().values()
    }

    assert len(artifact_hash) == 64
    assert artifact_hash not in semantic_hashes
    actual = hashlib.sha256(BINDING_PATH.read_bytes()).hexdigest()
    assert artifact_hash == actual


def test_afrobarometer_r1_preflight_has_exact_six_certified_registry_keys():
    manifest = json.loads(BINDING_MANIFEST_PATH.read_text(encoding="utf-8"))
    preflight = manifest["afrobarometer_r1_preflight"]

    assert preflight["active_contract_rows"] == 6
    assert preflight["var_codes"] == list(AFRO_R1)
    assert preflight["response_semantics_contract_hashes"] == list(AFRO_R1.values())
    assert set(preflight["response_semantics_contract_hashes"]).issubset(
        load_v551_registry_key_set()
    )


def test_scoped_serialization_preserves_exact_contract_identities_when_pyarrow_available(tmp_path):
    pytest.importorskip("pyarrow")
    frame = pd.concat(
        [_rows("dememp", 4, special=1), _rows("pfeerd", 5, special=1)],
        ignore_index=True,
    )
    bound, summary = bind_governed_response_semantics_contracts(frame, live_build=True)
    assert summary["unresolved_groups"] == 0

    path = tmp_path / "response_option_map.parquet"
    bound.to_parquet(path, index=False)
    loaded = pd.read_parquet(path)

    assert loaded["response_semantics_contract_hash"].tolist() == bound[
        "response_semantics_contract_hash"
    ].tolist()
    assert set(loaded["response_semantics_contract_hash"]) == {
        AFRO_R1["dememp"],
        AFRO_R1["pfeerd"],
    }
