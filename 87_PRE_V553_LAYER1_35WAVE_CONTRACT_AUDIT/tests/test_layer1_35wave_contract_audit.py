from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pandas as pd

SCRIPT = Path(__file__).resolve().parents[1] / "code" / "run_layer1_35wave_contract_audit.py"
spec = importlib.util.spec_from_file_location("layer1", SCRIPT)
assert spec and spec.loader
layer1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layer1)


def row(**overrides):
    base = {
        "question_implementation_id": "q1",
        "question_concept_id": "c1",
        "source_family": "GSS",
        "wave": "2010",
        "source_variable_code": "VAR1",
        "exact_question_text": "Question",
        "response_topology": "binary_contrast",
        "semantic_lane": "relation",
        "semantic_role": "RELATION_EVIDENCE",
        "semantic_subrole": "certified_directional_subjective_scale",
        "semantic_tags": "relation|attitude",
        "evidence_lane": "relation",
        "current_directional_atom_eligible": True,
        "directional_certification_status": "CERTIFIED",
        "response_binding_status": "bound",
        "authority_status": "source_reviewed",
        "deep_review_status": "COMPLETE",
        "source_text_status": "SOURCE_TEXT_PRESENT",
        "response_contract_hashes": "h1",
        "routing_signal_status": "NO_EXPLICIT_ROUTING_SIGNAL_IN_PACKET",
        "position_conditioning": "no",
        "horizon_affordance": "current_relation_evidence",
    }
    base.update(overrides)
    return base


def test_active_scope_is_exactly_35_and_excludes_asian_w6():
    assert len(layer1.ACTIVE_SCOPES) == 35
    assert ("Asian Barometer", "W6") not in layer1.ACTIVE_SCOPES
    assert ("Asian Barometer", "W5") in layer1.ACTIVE_SCOPES


def test_morphology_tags_overlap_without_collapsing():
    tags = layer1.morphology_tags(row(has_dk=True, position_conditioning="yes"))
    assert "directional_relation" in tags
    assert "binary" in tags
    assert "missingness_semantics" in tags
    assert "position_coordinate" in tags
    assert "pressure_linkage_candidate" in tags


def test_selection_is_deterministic_and_uses_joint_seed():
    rows = []
    topologies = [
        "binary_contrast", "ordinal_context", "nominal_choice", "scalar",
        "multiselect_child", "continuous_context",
    ]
    for i in range(30):
        r = row(
            question_implementation_id=f"q{i:02d}",
            question_concept_id=f"c{i:02d}",
            source_variable_code=f"V{i:02d}",
            response_topology=topologies[i % len(topologies)],
            current_directional_atom_eligible=(i % 2 == 0),
            directional_certification_status="CERTIFIED" if i % 2 == 0 else "NOT_CERTIFIED",
            semantic_role="RELATION_EVIDENCE" if i % 3 else "STRUCTURAL_CONTEXT",
            semantic_lane="relation" if i % 3 else "structural",
            semantic_subrole="derived_or_recoded_context" if i == 7 else "certified_directional_subjective_scale",
            implementation_variant_class="REPEATED_OR_MULTISELECT_GROUP_MEMBER" if i == 8 else "",
            routing_signal_status="ROUTING_OR_INAPPLICABILITY_SIGNAL_PRESENT" if i == 9 else "NO_EXPLICIT_ROUTING_SIGNAL_IN_PACKET",
            response_contract_hashes=f"h{i:02d}",
        )
        rows.append(r)
    df = pd.DataFrame(rows)
    kwargs = dict(
        catalog=df,
        family="GSS",
        wave="2010",
        min_vars=10,
        target_vars=12,
        max_vars=15,
        registry_family_groups=[["V01", "V02", "V03"]],
    )
    first = layer1.select_variables_for_scope(**kwargs)
    second = layer1.select_variables_for_scope(**kwargs)
    assert first[0] == second[0]
    assert first[2]["selection_hash"] == second[2]["selection_hash"]
    assert {"V01", "V02"}.issubset(first[0])
    assert first[2]["joint_family_seed_used"] is True


def test_privacy_filter_excludes_respondent_substrate(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "dest"
    source.mkdir()
    (source / "aggregate.json").write_text(json.dumps({"rows": 5}), encoding="utf-8")
    (source / "v550_shared_respondent_substrate.parquet").write_bytes(b"not parquet")
    inventory, findings = layer1.copy_nonrespondent_artifacts(source, destination)
    assert [r["relative_path"] for r in inventory] == ["aggregate.json"]
    assert any(r["finding"] == "forbidden_path" for r in findings)


def test_redaction_removes_database_credentials():
    value = "DATABASE_URL=postgresql://user:secret@localhost/db\npassword=secret"
    redacted = layer1.redact_text(value)
    assert "secret" not in redacted
    assert "<redacted>" in redacted
