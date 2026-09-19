"""ASTRA-D10-R1 exact M10-M01 28-cell candidate-envelope assembly.

This artifact only assembles already accepted D05/D06/D07/D08/D09 and Q01/R02
material into the frozen S03 generic batch interface.  It does not select rule
currentness, calibrate numeric values, or materialize actor/application facts.
"""
from __future__ import annotations

import json
from typing import Any

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.sdtf_r4_generic_batch_adapter import (
    BATCH_KIND,
    CANDIDATE_ROW_KIND,
    GENERIC_CONTRACT_REF,
)

SCHEMA = "ASTRA_D10_R1_M10_M01_CONCRETE_CANDIDATE_ENVELOPE_R1"
CANDIDATE_NAMESPACE = "PSC06"
CANDIDATE_ID = "M10-M01"
BATCH_NAMESPACE = "PSC06"
BATCH_ID = "M10-M01:D10-R1"


def _r(kind: str, object_id: str, content_hash: str) -> dict[str, str]:
    return {"kind": kind, "object_id": object_id, "content_hash": content_hash}


def _cell(
    ordinal: int,
    value: Any,
    *,
    state: str = "SATISFIED_CURRENT",
    na_basis_ref: dict[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "determinant_id": f"GBE-R4-{ordinal:03d}",
        "state": state,
        "resolved_value": value,
        "candidate_material_refs": [],
        "blocker_refs": [],
        "na_basis_ref": na_basis_ref,
        "basis_text": None,
    }


CONSTITUTION_REF = _r(
    "SDTF_R4_CONSTITUTION_CURRENT_SELECTION",
    "SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0:HQ_RUNTIME_ADOPTION_R1",
    "141260a47d7540229722646dff41c4886dc02240fbcde96f1810c75be15e851d",
)
SOURCE_REF = _r(
    "SDTF_DOCUMENTARY_SOURCE",
    "WRIGHT_CLASSES_1985:M10_SOURCE_LEDGER_R1",
    "051472e4d013b93df75acd0dfe0c6816dd657337fbfb62a79fdf9890fe712b4b",
)
CLAIM_REFS = [
    _r("SDTF_SOURCE_CLAIM", "M10-M01:WRIGHT_CLASSES_CH3:857-909",
       "258a87bf37989e19533ccff373fa6c58250f3f0620601f09c4c4b2ef482c830f"),
    _r("SDTF_SOURCE_CLAIM", "M10-M01:WRIGHT_CLASSES_CH3:951-959",
       "75196a71a20e7df1b3fa1f39e66764f3d23c8bff7daf5d63076e313da9d3dcbe"),
    _r("SDTF_SOURCE_CLAIM", "M10-M01:WRIGHT_CLASSES_CH3:978-996",
       "cf45e539ca3d6f2a06e7fb74868d22e01cadef174996362e162601b72378e8b6"),
]
EVIDENCE_REF = _r(
    "SDTF_SOURCE_EVIDENCE_STATUS",
    "M10-M01:WRIGHT_CLASSES:EVIDENCE_STATUS@1.0.0",
    "b93456af810957275b178df555147eddc15433158da5abd2352717e0ea213fae",
)
NORMALIZED_REF = _r(
    "SDTF_R4_NORMALIZED_MECHANISM",
    "M10-M01:PROPERTY_SEPARATION_WAGE_DEPENDENCY:R1",
    "0b69f9d04c09fad479ab05582c9bcf8d21951c6f7ea94e2f8c7c3ab3545e3411",
)
SHAPE_REF = _r(
    "SDTF_R4_PERMITTED_RULE_SHAPE",
    "M10-M01:CONJUNCTIVE_OBJECTIVE_STRUCTURAL_DEPENDENCY_DERIVATION:R1",
    "bf8ce59029360280ad7a08c8c50e5a3200c0298cb6248d4cd1b75435f3a7588e",
)
REQUIRED_INPUTS_REF = _r(
    "SDTF_REQUIRED_OBJECTIVE_INPUT_BINDINGS",
    "M10-M01:PROPERTY_SEPARATION_WAGE_DEPENDENCY@1.0.0",
    "c013ce882a9c4b72f334b8ac2479e5dda066a2752f6df41bbc5127a48630b983",
)
QUALIFICATION_REF = _r(
    "M10_M01_QUALIFICATION_REALIZATION_PROOF_CONTRACT",
    "PSC06:M10-M01:PKG-E:QUALIFICATION@1.0.0",
    "b6c17d2dd3066cba78b4c0f7c3235bb0799684799716db540db29badc3ecf165",
)
TEMPORAL_REF = _r(
    "M10_M01_TEMPORAL_CURRENTNESS_CONTRACT",
    "PSC06:M10-M01:PKG-E:TEMPORAL@1.0.0",
    "c2abce28a839e8117980ae55e87cbd80ee8e613ef98624fcbd3c8999616a1dcf",
)
PORTABILITY_REF = _r(
    "M10_M01_PORTABILITY_CEILING",
    "PSC06:M10-M01:PKG-E:PORTABILITY@1.0.0",
    "0dde948815f73d348f0003caded013360cbfc4e0a3e195d578073956a0879b59",
)
CURRENTNESS_CEILING_REF = _r(
    "SDTF_CURRENTNESS_CEILING",
    "M10-M01:R4_NONCOLLAPSE@1.0.0",
    "ebbb00e6f756fc593709187cc250e93091b18a4154380e780277658ff60a874c",
)
HISTORICAL_REF = _r(
    "SDTF_HISTORICAL_INSTITUTIONAL_VALIDITY",
    "M10-M01:WRIGHT_CLASSES_PROPERTY_ASSET_RULE_CONTEXT@1.0.0",
    "8fc7f01a3d8f77f9f17ccbaa010662db3eadc1d6fa2c17567c16fcafc3ab4874",
)
NEGATIVE_REF = _r(
    "SDTF_NEGATIVE_CEILING",
    "M10-M01:TRACE_NEGATIVE_CEILING@1.0.0",
    "60719b44275ff50741b65c9172ef8524445774da5e8379ddca52035e516e73ad",
)
V3_STOP_REF = _r(
    "SDTF_V3_STOP_BOUNDARY",
    "M10-M01:PREV3_OBJECTIVE_WORLD_ONLY@1.0.0",
    "ffd46991761765c5d0a59678f49fe46ffdf1d24d7b2e7c6144678c04fad0a0f6",
)

RULE_OWNER_SCOPE = _r(
    "SDTF_RULE_OWNER_SCOPE", "M10-M01:RULE_OWNER",
    "b6f0bb622158e797aaf4a90b609497ae94c089986e93356532241a64732f4e12",
)
RULE_OWNER_SELECTION = _r(
    "SDTF_RULE_OWNER_CURRENT_SELECTION_EVIDENCE", "M10-M01:RULE_OWNER:Q01_R1",
    "4d62f67ede66fe0b3b60d46b16934c90024048716d7cc460095807762f14f9b5",
)
RULE_OWNER = {
    "role": "RULE_OWNER",
    "disposition": "BOUND",
    "scope_or_na_ref": RULE_OWNER_SCOPE,
    "authority_ref": {
        "authority_id": "RAWLSING_HQ_PREV3_SDTF_M10_M01_RULE_OWNER",
        "authority_version": "1.0.0",
        "authority_content_hash": "80fd8e9a59b76e36392872c13536cdebf7de6273e5233d6bd285c1d0027a7289",
    },
    "current_selection_evidence_refs": [RULE_OWNER_SELECTION],
}
CAUSAL_SCOPE = _r(
    "SDTF_CAUSAL_USE_SCOPE", "M10-M01:CAUSAL_USE",
    "e102456438f4441f6e3f3057c4008e4a68a3f25bf78012154ab490a5b88dee56",
)
CAUSAL_SELECTION = _r(
    "SDTF_CAUSAL_USE_CURRENT_SELECTION_EVIDENCE", "M10-M01:CAUSAL_USE:R02_R1",
    "6687e9b20795c905b2bbf5c8edc99dcdbf4ed3fc7c649b1f7037a923b5351c2a",
)
CAUSAL_USE = {
    "role": "CAUSAL_USE",
    "disposition": "BOUND",
    "scope_or_na_ref": CAUSAL_SCOPE,
    "authority_ref": {
        "authority_id": "RAWLSING_HQ_PREV3_SDTF_M10_M01_CAUSAL_USE",
        "authority_version": "1.0.0",
        "authority_content_hash": "ebd9554437a9e14905b5a8fe8d75e20660805a9d481909856509576ba5958c07",
    },
    "current_selection_evidence_refs": [CAUSAL_SELECTION],
}
MEASUREMENT_NA = _r(
    "SDTF_M10_M01_AUXILIARY_AUTHORITY_NA_BASIS",
    "M10-M01:MEASUREMENT:NA_BASIS:D06_R1",
    "665822d53f07e0192f35cf7010fbc5a39c60fe578e0573c9bffcd5088eff1276",
)
ESTIMAND_NA = _r(
    "SDTF_M10_M01_AUXILIARY_AUTHORITY_NA_BASIS",
    "M10-M01:ESTIMAND:NA_BASIS:D06_R1",
    "d385ef2b5ff5340bdcc8bd522519bd9d1fd325f7c63753b26817d976833eafb9",
)
IDENTIFICATION_NA = _r(
    "SDTF_M10_M01_AUXILIARY_AUTHORITY_NA_BASIS",
    "M10-M01:IDENTIFICATION:NA_BASIS:D06_R1",
    "b0cf46082e4f0304f734a6af4cb6543c17df23d7dad894c973e72596578b1ebf",
)
CALIBRATION_NA = _r(
    "SDTF_M10_M01_CALIBRATION_AUTHORITY_NA_BASIS",
    "M10-M01:CALIBRATION:NA_BASIS:D09_R1",
    "0a72c9453ad55f1934f1e9953c3557a56893083ec32efb8e9a7fc03d0bb6244e",
)

CELLS = [
    _cell(1, "SDTF_R4_M10_M01_PROPERTY_SEPARATION_WAGE_DEPENDENCY"),
    _cell(2, "1.0.0"),
    _cell(3, "7d6efc3c36be0caff06022c0d951e5b4f535d6900c5c06751b3accacd48b39c8"),
    _cell(4, ["P1 MATERIAL_ACCESS_DEPENDENCY"]),
    _cell(5, CONSTITUTION_REF),
    _cell(6, [SOURCE_REF]),
    _cell(7, CLAIM_REFS),
    _cell(8, EVIDENCE_REF),
    _cell(9, NORMALIZED_REF),
    _cell(10, SHAPE_REF),
    _cell(11, REQUIRED_INPUTS_REF),
    _cell(12, QUALIFICATION_REF),
    _cell(13, TEMPORAL_REF),
    _cell(14, PORTABILITY_REF),
    _cell(15, CURRENTNESS_CEILING_REF),
    _cell(16, HISTORICAL_REF),
    _cell(17, NEGATIVE_REF),
    _cell(18, V3_STOP_REF),
    _cell(19, RULE_OWNER),
    _cell(20, None, state="NOT_APPLICABLE", na_basis_ref=MEASUREMENT_NA),
    _cell(21, None, state="NOT_APPLICABLE", na_basis_ref=ESTIMAND_NA),
    _cell(22, None, state="NOT_APPLICABLE", na_basis_ref=IDENTIFICATION_NA),
    _cell(23, CAUSAL_USE),
    _cell(24, None, state="NOT_APPLICABLE", na_basis_ref=CALIBRATION_NA),
    _cell(25, "NONNUMERIC"),
    _cell(26, "CANDIDATE_NOT_CURRENT"),
    _cell(27, []),
    _cell(28, []),
]

PROVENANCE_REFS = sorted(
    [
        GENERIC_CONTRACT_REF.as_dict(),
        _r("SDTF_R4_PKG_A_RULE_IDENTITY_SHAPE_VALUE_CLASS", "M10-M01:PKG-A:R1",
           "7773eedaabcdbd6f5e887144d249dbf29bdddf8b989b257675f6272f73420c2b"),
        _r("ASTRA_D06_M10_M01_AUXILIARY_AUTHORITY_DISPOSITIONS", "M10-M01:PKG-C:D06_R1",
           "9559c52b39fe9948eba65bede9410b89f1a38e43241d1c8a184c4b939e8264f7"),
        _r("SDTF_R4_GENERIC_BATCH_PKG_D_TRACE_EXACT_REF_LIFT", "M10-M01:PKG-D@1.0.0",
           "260344e38287523593ec5fe6aecf96fccbec19c250d859c8bd4d5fc398ba6f05"),
        QUALIFICATION_REF,
        TEMPORAL_REF,
        PORTABILITY_REF,
        _r("ASTRA_D09_M10_M01_CALIBRATION_DISPOSITION", "M10-M01:PKG-C:D09_R1",
           "321827ab4fe01b91204cb40c10e13688cd4100229423f3078ee0d836c3fce8cc"),
        RULE_OWNER_SCOPE,
        RULE_OWNER_SELECTION,
        CAUSAL_SCOPE,
        CAUSAL_SELECTION,
        _r("SDTF_M10_SOURCE_CLAIM", "M10-M01:PROPERTY_SEPARATION_WAGE_DEPENDENCY",
           "a6f984b0b9cfd17d8c0892ac976b5858339dcd048fbfa9dd37ca7980b2c7ad05"),
    ],
    key=lambda x: f"{x['kind']}|{x['object_id']}|{x['content_hash']}",
)

ROW_IDENTITY = {
    "contract_ref": GENERIC_CONTRACT_REF.as_dict(),
    "key": {"candidate_namespace": CANDIDATE_NAMESPACE, "candidate_id": CANDIDATE_ID},
    "row_generation": 0,
    "predecessor_row_ref": None,
    "requirement_cells": [
        {k: c[k] for k in (
            "determinant_id", "state", "resolved_value",
            "candidate_material_refs", "blocker_refs", "na_basis_ref"
        )}
        for c in CELLS
    ],
    "provenance_refs": PROVENANCE_REFS,
}
ROW_REF = ExactRef(
    CANDIDATE_ROW_KIND,
    f"{CANDIDATE_NAMESPACE}:{CANDIDATE_ID}:g0",
    semantic_hash(ROW_IDENTITY),
).as_dict()
assert ROW_REF["content_hash"] == "d8888ed404b68b5679f9742a77e3e12a9af0a6d397e227a826afa48fe3dc3115"

CANDIDATE_ROW = {
    "contract_ref": GENERIC_CONTRACT_REF.as_dict(),
    "key": {"candidate_namespace": CANDIDATE_NAMESPACE, "candidate_id": CANDIDATE_ID},
    "snapshot": {
        "row_generation": 0,
        "predecessor_row_ref": None,
        "requirement_cells": CELLS,
        "provenance_refs": PROVENANCE_REFS,
    },
    "ref": ROW_REF,
}
BATCH_MATERIAL = {
    "contract_ref": GENERIC_CONTRACT_REF.as_dict(),
    "batch_namespace": BATCH_NAMESPACE,
    "batch_id": BATCH_ID,
    "candidate_row_refs": [ROW_REF],
    "batch_provenance_refs": PROVENANCE_REFS,
}
BATCH_REF = ExactRef(
    BATCH_KIND,
    f"{BATCH_NAMESPACE}:{BATCH_ID}",
    semantic_hash(BATCH_MATERIAL),
).as_dict()
assert BATCH_REF["content_hash"] == "90ff2bf3edfe955ebfd113ae77a0e8f04ac19d9dd96a1e04d370e0ff4dbb2546"

BATCH_ENVELOPE = {
    "contract_ref": GENERIC_CONTRACT_REF.as_dict(),
    "batch_namespace": BATCH_NAMESPACE,
    "batch_id": BATCH_ID,
    "candidate_rows": [CANDIDATE_ROW],
    "candidate_row_refs": [ROW_REF],
    "batch_provenance_refs": PROVENANCE_REFS,
    "ref": BATCH_REF,
}

EXPECTED = {
    "candidate_row_ref": ROW_REF,
    "batch_ref": BATCH_REF,
    "runtime_binding_ref": _r(
        "SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING",
        "SDTF_R4_M10_M01_PROPERTY_SEPARATION_WAGE_DEPENDENCY@1.0.0",
        "f4094d73cc2f6e0c3a40d5f5eb94e86a69d32863026cb1844c1d18b854fcf370",
    ),
    "candidate_receipt_ref": _r(
        "SDTF_R4_GENERIC_BATCH_CANDIDATE_RECEIPT", "PSC06:M10-M01:g0",
        "ce4aefa2e59975556b30d1c906538179b450b5fb7965ba2b358823386f9c55bb",
    ),
    "batch_receipt_ref": _r(
        "SDTF_R4_GENERIC_BATCH_ADAPTER_RECEIPT", "PSC06:M10-M01:D10-R1",
        "5b1af74948c14bce32bd64d0ddeed1a8e01f80f08a9590289f1cc0f14299991c",
    ),
    "runtime_projection_state": "ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT",
    "current_selection_state": "ELIGIBLE_FOR_SEPARATE_SELECTION",
}


def artifact() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "schema_version": "1.0.0",
        "candidate": {
            "candidate_id": CANDIDATE_ID,
            "candidate_name": "PROPERTY SEPARATION / WAGE DEPENDENCY",
            "value_mode": "NONNUMERIC",
            "rule_currentness": "CANDIDATE_NOT_CURRENT",
        },
        "expected_projection": EXPECTED,
        "boundaries": {
            "numeric_calibration_inferred": False,
            "rule_current_accepted_issued": False,
            "current_actor_or_world_application_fact_created": False,
            "occupant_or_witness_created": False,
            "topology_created": False,
            "v3_person_state_created": False,
            "obl063_used": False,
        },
        "batch_envelope": BATCH_ENVELOPE,
    }


if __name__ == "__main__":
    print(json.dumps(artifact(), sort_keys=True, separators=(",", ":"), ensure_ascii=False))
