from __future__ import annotations

import inspect

import pandas as pd
import pytest

from data.ddm_build_copy import apply_postgres_facet_ready_substrate as db


def _candidate(var_name: str, driver_id: str, mapping_status: str, relation_axis_id: str, *, item_id: str = "") -> dict[str, str]:
    return {
        "source": "LiTS",
        "wave": "III",
        "var_name": var_name,
        "item_id": item_id,
        "display_text": "Sec" if driver_id.startswith("idio::") else "",
        "final_driver_id": driver_id,
        "final_driver_label": "Sec" if driver_id.startswith("idio::") else "DURATION1",
        "final_driver_scope": "idiosyncratic_cluster" if driver_id.startswith("idio::") else "metadata",
        "final_driver_origin": "semantic_cluster" if driver_id.startswith("idio::") else "semantic_master",
        "driver_id": "",
        "driver_facet_id": "" if driver_id.startswith("idio::") else driver_id,
        "question_block_id": "",
        "structural_domain_id": "",
        "relation_axis_id": relation_axis_id,
        "target_entity_id": "" if driver_id.startswith("idio::") else "context_not_applicable",
        "mapping_status": mapping_status,
        "evidence_kind": "" if driver_id.startswith("idio::") else "contextual_metadata",
        "strata_relevance": "",
        "channel_affordances": "",
        "forbidden_inference": "",
        "does_not_measure": "",
        "review_notes": "",
    }


def _rows(*records: dict[str, str]) -> list[tuple[object, ...]]:
    return db.create_question_mapping_rows(pd.DataFrame(records))


def test_real_defect_shape_is_one_uid_normalized_conflict_and_both_are_quarantined():
    records = [
        _candidate("DURATION1", "metadata::semantic_duration1", "accepted_context_only", "context"),
        _candidate("Duration1", "idio::semantic_sec", "accepted_existing_mapping", "", item_id="LiTS_III_Duration1"),
        _candidate("NEIGHBOR", "idio::semantic_neighbor", "accepted_existing_mapping", "", item_id="LiTS_III_Neighbor"),
    ]
    candidates = _rows(*records)
    published, quarantined = db.quarantine_conflicting_question_mapping_rows(candidates)

    assert len(candidates) == 3
    assert quarantined == [("sf_lits_v1", "wv_lits_iii_v1", "DURATION1")]
    assert {row[9] for row in published} == {"NEIGHBOR"}


def test_quarantine_is_independent_of_candidate_order():
    records = [
        _candidate("DURATION1", "metadata::semantic_duration1", "accepted_context_only", "context"),
        _candidate("Duration1", "idio::semantic_sec", "accepted_existing_mapping", ""),
    ]
    first = db.quarantine_conflicting_question_mapping_rows(_rows(*records))
    second = db.quarantine_conflicting_question_mapping_rows(_rows(*reversed(records)))
    assert first[1] == second[1]
    assert first[0] == second[0] == []


def test_case_and_provenance_aliases_with_identical_semantics_are_not_conflicts():
    records = [
        _candidate("ALIAS", "idio::semantic_same", "accepted_existing_mapping", "", item_id="LiTS_III_ALIAS"),
        _candidate("alias", "idio::semantic_same", "accepted_existing_mapping", "", item_id="lits_iii_alias"),
    ]
    candidates = _rows(*records)
    published, quarantined = db.quarantine_conflicting_question_mapping_rows(candidates)
    assert quarantined == []
    assert len(published) == 2


class _Cursor:
    def __init__(self, rows):
        self.rows = rows

    def execute(self, _sql):
        return None

    def fetchall(self):
        return self.rows

    def close(self):
        return None


class _Connection:
    def __init__(self, rows):
        self.cursor_value = _Cursor(rows)

    def cursor(self):
        return self.cursor_value


def _db_row(var_code: str, *, semantic: str) -> tuple[str, ...]:
    values = [
        "sf_test_v1", "wv_test_v1", var_code,
        semantic, semantic, "scope", "origin", semantic, "facet", "block",
        "domain", "axis", "target", "accepted_existing_mapping", "evidence",
        "strata", "channels", "forbidden", "does_not_measure", "notes",
    ]
    return tuple(values)


def test_post_load_assertion_uses_the_same_semantic_equality_law():
    db.assert_no_conflicting_qsm_uid_rows(_Connection([
        _db_row("ALIAS", semantic="same"),
        _db_row("alias", semantic="same"),
    ]))
    with pytest.raises(RuntimeError, match="CONFLICTING_QSM_UID_SEMANTIC_DUPLICATE"):
        db.assert_no_conflicting_qsm_uid_rows(_Connection([
            _db_row("VAR", semantic="first"),
            _db_row("var", semantic="second"),
        ]))


def test_production_quarantine_is_generic_and_does_not_load_proxy_authority():
    source = inspect.getsource(db)
    assert "DURATION1" not in source
    assert "semantic_sec" not in source
    assert "semantic_duration1" not in source
    assert "question_relation_registry.csv" not in source
