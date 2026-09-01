from __future__ import annotations

import copy
import json

import pytest

from data.ddm_build_copy.ffx002_r2_local_geometry import (
    DISPOSITION_ROLE,
    METHOD_SCHEMA_VERSION,
    POSITION_ROLE,
    LocalGeometryContractError,
    compile_local_geometric_view,
    compute_common_manifest_hash,
)


def _manifest() -> dict:
    manifest = {
        "manifest_schema_version": "SYNTHETIC_COMMON_MANIFEST_R1",
        "current_execution_sha": "9611a9067ab28e17eb45b565398c7e604a24e77b",
        "observation_substrate_ref": "synthetic://observation#sha256:01",
        "respondent_entity_binding_ref": "synthetic://respondents#sha256:02",
        "exposure_risk_set_ref": "synthetic://risk-set#sha256:03",
        "source_scope_ref": "synthetic://scope",
        "source_native_measurement_refs": ["P1", "P2", "D1", "D2"],
        "qimpl_measurement_binding_refs": ["Q:P1", "Q:P2", "Q:D1", "Q:D2"],
        "response_state_semantics_ref": "synthetic://response-semantics",
        "special_state_semantics_ref": "synthetic://special-states",
        "ttar_execution_sequence": [],
        "post_transform_state_manifest": "synthetic://state-manifest",
        "claim_scope_ref": "synthetic://claim",
        "estimand_ref": "UNWEIGHTED_SAMPLE_RELATIONAL_VIEW",
        "weight_design_refs": "NONE",
        "analytic_role_authority_refs": ["synthetic://pra"],
        "ancestry_disjointness_receipt": "PASS",
        "unresolved_noncomparable_manifest": [],
        "source_native_ancestry_ref": "synthetic://ancestry",
        "loss_profile": [],
        "holdout_generation_inputs_hash": "synthetic-holdout-inputs",
        "canonicalization_spec": {
            "encoding": "UTF-8",
            "hash_algorithm": "SHA-256",
            "set_array_paths": [],
        },
    }
    manifest["manifest_hash"] = compute_common_manifest_hash(manifest)
    return manifest


def _method(*, weighted: bool = False, retained_d: int = 2) -> dict:
    metric = {
        "family": "EXACT_STATE_HAMMING_R1",
        "state_comparison": "EXACT_FROZEN_STATE_IDENTITY_ONLY",
    }
    if weighted:
        metric = {
            "family": "EXACT_STATE_WEIGHTED_HAMMING_R1",
            "state_comparison": "EXACT_FROZEN_STATE_IDENTITY_ONLY",
            "measurement_weights": {"P1": 1.0, "P2": 2.0, "D1": 1.0, "D2": 3.0},
        }
    return {
        "schema_version": METHOD_SCHEMA_VERSION,
        "metric": metric,
        "decomposition": {
            "family": "CLASSICAL_MDS_JACOBI_R1",
            "axis_labels": "NUMERIC_IDS_ONLY",
        },
        "dimensionality": {"rule": "FIXED_R1", "retained_d": retained_d},
        "neighborhood": {"k": 2},
        "compression": {"float_digits": 12},
        "preprocessing": [
            {
                "name": "opaque_state_identity_projection",
                "classification": "IDENTITY_PRESERVING_METHOD",
                "executed_postfork": True,
            }
        ],
    }


def _surface(side: str, role: str, prefix: str, *, components: tuple[str, str] = ("C0", "C0")) -> dict:
    mids = [f"{prefix}1", f"{prefix}2"]
    pairs = [("A", "A"), ("A", "B"), ("B", "B"), ("B", "A")]
    return {
        "side": side,
        "measurements": [
            {
                "measurement_id": mids[0],
                "analytic_role": role,
                "state_ids": [f"{mids[0]}:A", f"{mids[0]}:B"],
                "ancestry_ids": [f"raw:{mids[0]}"],
                "component_id": components[0],
                "display_label": "ignored-label-one",
            },
            {
                "measurement_id": mids[1],
                "analytic_role": role,
                "state_ids": [f"{mids[1]}:A", f"{mids[1]}:B"],
                "ancestry_ids": [f"raw:{mids[1]}"],
                "component_id": components[1],
                "display_label": "ignored-label-two",
            },
        ],
        "rows": [
            {
                "respondent_id": f"R{i}",
                "state_by_measurement": {
                    mids[0]: f"{mids[0]}:{a}",
                    mids[1]: f"{mids[1]}:{b}",
                },
            }
            for i, (a, b) in enumerate(pairs, start=1)
        ],
    }


def _payload() -> dict:
    return {
        "common_manifest": _manifest(),
        "method_manifest": _method(),
        "position_surface": _surface("position", POSITION_ROLE, "P"),
        "disposition_surface": _surface("disposition", DISPOSITION_ROLE, "D"),
    }


def test_core_b_builds_position_and_disposition_geometry_separately() -> None:
    result = compile_local_geometric_view(_payload())
    assert result["arm_id"] == "B"
    assert result["view_family"] == "LOCAL_GEOMETRIC"
    assert result["position_geometry"]["side"] == "position"
    assert result["disposition_geometry"]["side"] == "disposition"
    assert result["position_disposition_dependence_profile"].startswith("NOT_PRODUCED")
    assert result["common_manifest_attestation"]["attestation_status"] == "ATTESTED_EQUAL"
    assert result["invariant_loss_receipt"]["semantic_mutation_count"] == 0
    assert result["claim_ceiling"].endswith("NO_EMPIRICAL_WORLD_OR_SOCIAL_ONTOLOGY")


def test_output_has_numeric_axes_only_and_explicit_local_relations() -> None:
    result = compile_local_geometric_view(_payload())
    component = result["position_geometry"]["components"][0]
    assert component["decomposition"]["dimension_ids"] == ["D1", "D2"]
    assert component["decomposition"]["axis_interpretation"] == "PROHIBITED__NUMERIC_DIMENSION_IDS_ONLY"
    assert component["local_neighborhoods"]
    assert component["local_orders"]
    assert component["local_oppositions"]
    assert component["compression"]["semantic_state_merge_count"] == 0
    assert "SOCIAL_ONTOLOGY" in result["forbidden_claims"]


def test_manifest_tamper_fails_closed() -> None:
    payload = _payload()
    payload["common_manifest"]["claim_scope_ref"] = "tampered-after-hash"
    with pytest.raises(LocalGeometryContractError, match="COMMON_INPUT_ARM_HASH_DIVERGENCE"):
        compile_local_geometric_view(payload)


@pytest.mark.parametrize(
    "forbidden_key",
    [
        "rare_state_merge",
        "ordinal_rebin",
        "category_reorder",
        "analytic_role_override",
        "risk_set_filter",
        "special_state_pool",
    ],
)
def test_postfork_semantic_transform_keys_are_rejected(forbidden_key: str) -> None:
    payload = _payload()
    payload["method_manifest"][forbidden_key] = {"enabled": True}
    with pytest.raises(LocalGeometryContractError, match="FORBIDDEN_UNDECLARED_SEMANTIC_TRANSFORM"):
        compile_local_geometric_view(payload)


def test_unknown_state_id_cannot_be_smuggled_in_as_geometry_preprocessing() -> None:
    payload = _payload()
    payload["position_surface"]["rows"][0]["state_by_measurement"]["P1"] = "P1:MERGED"
    with pytest.raises(LocalGeometryContractError, match="semantic state mutation forbidden"):
        compile_local_geometric_view(payload)


def test_rerole_attempt_fails_closed() -> None:
    payload = _payload()
    payload["position_surface"]["measurements"][0]["analytic_role"] = "SUPPLEMENTARY_POSITION"
    with pytest.raises(LocalGeometryContractError, match="ROLE_RECLASSIFICATION forbidden"):
        compile_local_geometric_view(payload)


def test_cross_side_ancestry_overlap_fails_closed() -> None:
    payload = _payload()
    payload["disposition_surface"]["measurements"][0]["ancestry_ids"] = ["raw:P1"]
    with pytest.raises(LocalGeometryContractError, match="ANCESTRY_CONTAMINATED"):
        compile_local_geometric_view(payload)


def test_risk_set_mutation_fails_closed() -> None:
    payload = _payload()
    payload["disposition_surface"]["rows"] = payload["disposition_surface"]["rows"][:-1]
    with pytest.raises(LocalGeometryContractError, match="COMMON_INPUT_RISK_SET_DIVERGENCE"):
        compile_local_geometric_view(payload)


def test_label_scramble_does_not_change_geometry_or_replay_hash() -> None:
    payload = _payload()
    baseline = compile_local_geometric_view(payload)
    scrambled = copy.deepcopy(payload)
    scrambled["position_surface"]["measurements"][0]["display_label"] = "CLASS"
    scrambled["position_surface"]["measurements"][1]["display_label"] = "RELIGIOSITY"
    scrambled["disposition_surface"]["measurements"][0]["display_label"] = "CAPITAL"
    altered = compile_local_geometric_view(scrambled)
    assert altered == baseline


def test_disconnected_components_never_receive_cross_component_metric() -> None:
    payload = _payload()
    payload["disposition_surface"] = _surface(
        "disposition", DISPOSITION_ROLE, "D", components=("DC1", "DC2")
    )
    result = compile_local_geometric_view(payload)
    assert result["disposition_geometry"]["component_count"] == 2
    assert result["disposition_geometry"]["cross_component_metric"] == "DOES_NOT_REPRESENT"


def test_numeric_replay_is_deterministic_and_versioned() -> None:
    payload = _payload()
    first = compile_local_geometric_view(payload)
    second = compile_local_geometric_view(copy.deepcopy(payload))
    assert json.dumps(first, sort_keys=True, separators=(",", ":")) == json.dumps(
        second, sort_keys=True, separators=(",", ":")
    )
    receipt = first["replay_receipt"]
    assert receipt["receipt_schema_version"] == "FFX002_R2_LOCAL_GEOMETRIC_NUMERIC_REPLAY_R1"
    assert receipt["numeric_comparison_contract"]["absolute_tolerance"] == 1e-10


def test_weighted_method_is_explicit_method_change_not_semantic_change() -> None:
    baseline_payload = _payload()
    weighted_payload = copy.deepcopy(baseline_payload)
    weighted_payload["method_manifest"] = _method(weighted=True)
    baseline = compile_local_geometric_view(baseline_payload)
    weighted = compile_local_geometric_view(weighted_payload)
    assert baseline["frozen_input_attestation"] == weighted["frozen_input_attestation"]
    assert baseline["method_manifest_hash"] != weighted["method_manifest_hash"]
    assert baseline["position_geometry"]["components"][0]["metric"]["distance_matrix"] != weighted[
        "position_geometry"
    ]["components"][0]["metric"]["distance_matrix"]
