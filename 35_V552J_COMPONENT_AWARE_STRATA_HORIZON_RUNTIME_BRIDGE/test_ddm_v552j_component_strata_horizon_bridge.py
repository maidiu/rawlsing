import json
from pathlib import Path

import pandas as pd
import pytest

from ddm_v552j_component_strata_horizon_bridge import (
    AUTHORITY_FIELDS,
    build_component_bridge,
    build_qsh_indexes,
    enrich_packet_index,
)


def qsh(rows):
    out = []
    for row in rows:
        record = {"source": "GSS", "wave": "2010", "country_code": "US", "question_id": "", "var_code": ""}
        record.update({field: "" for field in AUTHORITY_FIELDS})
        record.update(row)
        out.append(record)
    columns = ["source", "wave", "country_code", "question_id", "var_code", *AUTHORITY_FIELDS]
    return pd.DataFrame(out, columns=columns)


def packets(vector, **extra):
    row = {
        "packet_id": "p1",
        "source": "GSS",
        "wave": "2010",
        "canonical_wave": "2010",
        "country_code": "US",
        "component_response_vector_json": json.dumps(vector),
    }
    row.update(extra)
    return pd.DataFrame([row])


def comp(order, question_id, var="x"):
    return {
        "item_order": order,
        "v551_question_id": question_id,
        "v551_var_code": var,
        "v550j_item_response_value_normalized": "1",
    }


def test_complete_homogeneous_and_scalar_projection():
    packet = packets([comp(1, "q1", "a"), comp(2, "q2", "b")])
    hierarchy = qsh([
        {"question_id": "q1", "var_code": "a", "stratum_id": "s", "horizon_type": "absolute"},
        {"question_id": "q2", "var_code": "b", "stratum_id": "s", "horizon_type": "absolute"},
    ])
    components, summary, report = build_component_bridge(packet, hierarchy)
    assert len(components) == 2 and report["matched_component_rows"] == 2
    assert summary.loc[0, "component_strata_horizon_authority_status"] == "COMPLETE_HOMOGENEOUS_COMPONENT_AUTHORITY"
    assert summary.loc[0, "packet_stratum_id"] == "s"


def test_heterogeneous_never_scalar_flattens():
    packet = packets([comp(1, "q1", "a"), comp(2, "q2", "b")])
    hierarchy = qsh([
        {"question_id": "q1", "var_code": "a", "stratum_id": "s1"},
        {"question_id": "q2", "var_code": "b", "stratum_id": "s2"},
    ])
    _, summary, _ = build_component_bridge(packet, hierarchy)
    assert summary.loc[0, "component_strata_horizon_authority_status"] == "COMPLETE_HETEROGENEOUS_COMPONENT_AUTHORITY"
    assert summary.loc[0, "packet_stratum_id"] == ""


def test_partial_coverage_never_scalar_flattens():
    packet = packets([comp(1, "q1", "a"), comp(2, "missing", "b")])
    hierarchy = qsh([{"question_id": "q1", "var_code": "a", "stratum_id": "s"}])
    _, summary, report = build_component_bridge(packet, hierarchy)
    assert report["unmatched_component_rows"] == 1
    assert summary.loc[0, "component_strata_horizon_authority_status"] == "PARTIAL_COMPONENT_STRATA_HORIZON_AUTHORITY"
    assert summary.loc[0, "packet_stratum_id"] == ""


def test_scope_var_fallback():
    packet = packets([comp(1, "unknown", "A")])
    hierarchy = qsh([{"question_id": "q1", "var_code": "a", "stratum_id": "s"}])
    components, _, _ = build_component_bridge(packet, hierarchy)
    assert components.loc[0, "qsh_match_status"] == "MATCHED_BY_SCOPE_VAR"


def test_duplicate_normalized_qsh_question_fails():
    hierarchy = qsh([{"question_id": "q1", "var_code": "a"}, {"question_id": " Q1 ", "var_code": "b"}])
    with pytest.raises(ValueError, match="duplicate normalized QSH question_id"):
        build_qsh_indexes(hierarchy)


def test_duplicate_scope_var_fails():
    hierarchy = qsh([{"question_id": "q1", "var_code": "a"}, {"question_id": "q2", "var_code": " A "}])
    with pytest.raises(ValueError, match="duplicate normalized QSH scope/var key"):
        build_qsh_indexes(hierarchy)


def test_duplicate_packet_id_fails():
    packet = packets([comp(1, "q1")])
    packet = pd.concat([packet, packet], ignore_index=True)
    with pytest.raises(ValueError, match="duplicate normalized packet_id"):
        build_component_bridge(packet, qsh([{"question_id": "q1", "var_code": "x"}]))


def test_invalid_json_fails():
    packet = packets([comp(1, "q1")])
    packet.loc[0, "component_response_vector_json"] = "{"
    with pytest.raises(ValueError, match="invalid component_response_vector_json"):
        build_component_bridge(packet, qsh([{"question_id": "q1", "var_code": "x"}]))


def test_empty_vector_fails():
    with pytest.raises(ValueError, match="non-empty list"):
        build_component_bridge(packets([]), qsh([]))


def test_duplicate_item_order_fails():
    with pytest.raises(ValueError, match="positive and unique"):
        build_component_bridge(packets([comp(1, "q1"), comp(1, "q2")]), qsh([]))


def test_component_without_identity_fails():
    with pytest.raises(ValueError, match="neither question id nor variable code"):
        build_component_bridge(packets([{"item_order": 1}]), qsh([]))


def test_packet_cardinality_and_order_preserved():
    first = packets([comp(1, "q1")])
    second = first.copy()
    second.loc[0, "packet_id"] = "p2"
    packet_index = pd.concat([second, first], ignore_index=True)
    _, summary, _ = build_component_bridge(packet_index, qsh([{"question_id": "q1", "var_code": "x"}]))
    enriched = enrich_packet_index(packet_index, summary)
    assert list(enriched.packet_id) == ["p2", "p1"] and len(enriched) == 2


def test_enrichment_rejects_blank_ids():
    packet_index = pd.DataFrame([{"packet_id": ""}])
    packet_summary = pd.DataFrame([{"packet_id": "p1", "x": "1"}])
    with pytest.raises(ValueError, match="blank packet index"):
        enrich_packet_index(packet_index, packet_summary)


def test_enrichment_rejects_normalized_duplicate_ids():
    packet_index = pd.DataFrame([{"packet_id": "p1"}, {"packet_id": " P1 "}])
    packet_summary = pd.DataFrame([{"packet_id": "p1", "x": "1"}])
    with pytest.raises(ValueError, match="duplicate normalized packet index"):
        enrich_packet_index(packet_index, packet_summary)


def test_enrichment_rejects_orphan_summary():
    packet_index = pd.DataFrame([{"packet_id": "p1"}])
    packet_summary = pd.DataFrame([{"packet_id": "p1", "x": "1"}, {"packet_id": "p2", "x": "2"}])
    with pytest.raises(ValueError, match="orphan packet summary"):
        enrich_packet_index(packet_index, packet_summary)


def test_enrichment_rejects_missing_summary():
    packet_index = pd.DataFrame([{"packet_id": "p1"}, {"packet_id": "p2"}])
    packet_summary = pd.DataFrame([{"packet_id": "p1", "x": "1"}])
    with pytest.raises(ValueError, match="missing packet summary"):
        enrich_packet_index(packet_index, packet_summary)


def test_enrichment_rejects_column_collision():
    packet_index = pd.DataFrame([{"packet_id": "p1", "packet_stratum_id": "existing"}])
    packet_summary = pd.DataFrame([{"packet_id": "p1", "packet_stratum_id": "s"}])
    with pytest.raises(ValueError, match="column collisions"):
        enrich_packet_index(packet_index, packet_summary)


def test_real_gss_2010_recovered_artifacts():
    base = Path(__file__).resolve().parent / 'runtime_test_inputs'
    packet_index = pd.read_csv(base / 'v551j_certified_packet_index.csv', dtype=str, keep_default_na=False)
    hierarchy = pd.read_csv(base / 'gss8__GSS_2010_US_question_semantic_hierarchy.csv', dtype=str, keep_default_na=False)
    components, summary, report = build_component_bridge(packet_index, hierarchy)
    assert len(summary) == 19
    assert len(components) == sum(len(json.loads(value)) for value in packet_index.component_response_vector_json)
    assert report['unmatched_component_rows'] == 0
    assert set(summary.component_strata_horizon_authority_status) == {'COMPLETE_HOMOGENEOUS_COMPONENT_AUTHORITY'}
    assert summary.component_match_coverage.eq(1.0).all()
    enriched = enrich_packet_index(packet_index, summary)
    assert len(enriched) == len(packet_index)
