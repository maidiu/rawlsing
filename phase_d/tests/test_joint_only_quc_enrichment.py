from __future__ import annotations

import pandas as pd

from data.ddm_build_copy.ddm_v550_shared_respondent_substrate import (
    enrich_shared_respondent_substrate_with_question_use_contract,
    resolve_shared_substrate_requirements,
)


def test_joint_only_members_resolve_from_full_mapping_and_enrich_without_base_expansion():
    base = pd.DataFrame([{"source": "Arab Barometer", "wave": "I", "country_code": "YE", "var_code": "Q101", "question_id": "Q101"}])
    full = pd.concat(
        [
            base,
            pd.DataFrame([
                {"source": "Arab Barometer", "wave": "I", "country_code": "YE", "var_code": "Q2571", "question_id": "Q2571"},
                {"source": "Arab Barometer", "wave": "I", "country_code": "YE", "var_code": "Q2572", "question_id": "Q2572"},
            ]),
        ],
        ignore_index=True,
    )
    registry = {
        "status": "approved",
        "source_family": "Arab Barometer",
        "p3_authority_release_id": "P3-AUTHORITY-2026-08-02-R184",
        "joint_configuration_authority_release_id": "V550J-BOUNDED-AUTHORITY-2026-08-02-R1",
        "families": [{
            "joint_configuration_id": "JCFG-AB-I",
            "source_family": "Arab Barometer",
            "eligible_waves": ["I"],
            "items": [
                {"var_code": "Q2571", "item_role": "context"},
                {"var_code": "Q2572", "item_role": "context"},
            ],
        }],
    }
    selection = resolve_shared_substrate_requirements(
        base,
        registry,
        source="Arab Barometer",
        canonical_wave="I",
        full_question_rows=full,
    )
    assert len(selection["base_question_rows"]) == 1
    assert selection["joint_only_var_codes"] == ["Q2571", "Q2572"]
    assert set(selection["union_var_codes"]) == {"Q101", "Q2571", "Q2572"}
    substrate = pd.DataFrame([
        {"var_code": "Q101", "question_id": "Q101", "country_code": "YE", "response_value_norm": "1"},
        {"var_code": "Q2571", "question_id": "Q2571", "country_code": "YE", "response_value_norm": "1"},
        {"var_code": "Q2572", "question_id": "Q2572", "country_code": "YE", "response_value_norm": "1"},
    ])
    quc = pd.DataFrame([
        {"var_code": "Q101", "question_id": "Q101", "country_code": "YE", "semantic_role": "base"},
        {"var_code": "Q2571", "question_id": "Q2571", "country_code": "YE", "semantic_role": "context", "v551_evidence_role": "none"},
        {"var_code": "Q2572", "question_id": "Q2572", "country_code": "YE", "semantic_role": "context", "v551_evidence_role": "none"},
    ])
    enriched, report = enrich_shared_respondent_substrate_with_question_use_contract(substrate, quc, country_code="YE")
    assert report["unjoined_row_count"] == 0
    assert set(enriched.loc[enriched["var_code"].isin(["Q2571", "Q2572"]), "question_use_contract_joined"]) == {True}
