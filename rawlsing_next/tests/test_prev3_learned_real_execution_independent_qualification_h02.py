import inspect

from rawlsing_next import _pre553_query_eval as canonical_i03
from rawlsing_next import prev3_learned_real_execution_r2 as g02


Q301_2_SOURCE_COUNTS = {1: 4501, 2: 7141, 3: 6460, 4: 7631, 5: 3054, 6: 137, 7: 62, None: 16}
Q301_7_SOURCE_COUNTS = {1: 4324, 2: 7820, 3: 6070, 4: 7135, 5: 3388, 6: 100, 7: 145, None: 20}


def _synthetic_records(target):
    rows = []
    for value in (1, 2, 3, 4, 5, 6, 7, None):
        row = {"q301_2": 1, "q301_7": 1, "q310": 1, "q311": 1}
        row[target] = value
        rows.append(row)
    return rows


def test_exact_source_q301_2_has_215_denominator_members_outside_frozen_substantive_domain():
    assert sum(Q301_2_SOURCE_COUNTS.values()) == 29002
    substantive = sum(Q301_2_SOURCE_COUNTS[x] for x in range(1, 6))
    excluded = Q301_2_SOURCE_COUNTS[6] + Q301_2_SOURCE_COUNTS[7] + Q301_2_SOURCE_COUNTS[None]
    assert substantive == 28787
    assert excluded == 215
    assert substantive + excluded == 29002


def test_exact_source_q301_7_has_265_denominator_members_outside_frozen_substantive_domain():
    assert sum(Q301_7_SOURCE_COUNTS.values()) == 29002
    substantive = sum(Q301_7_SOURCE_COUNTS[x] for x in range(1, 6))
    excluded = Q301_7_SOURCE_COUNTS[6] + Q301_7_SOURCE_COUNTS[7] + Q301_7_SOURCE_COUNTS[None]
    assert substantive == 28737
    assert excluded == 265
    assert substantive + excluded == 29002


def test_g02_query_uses_all_selected_rows_as_denominator_but_projects_only_1_to_5_q301_2():
    result = g02._query(_synthetic_records("q301_2"), "T_Q301_2_RAW", ["A000"])
    assert result["raw_denominator_support"] == 8
    assert result["raw_complete_cell_support"] == 5
    assert set(result["complete_cell_counts"]) == {"1", "2", "3", "4", "5"}


def test_g02_query_uses_all_selected_rows_as_denominator_but_projects_only_1_to_5_q301_7():
    result = g02._query(_synthetic_records("q301_7"), "T_Q301_7_RAW", ["A000"])
    assert result["raw_denominator_support"] == 8
    assert result["raw_complete_cell_support"] == 5
    assert set(result["complete_cell_counts"]) == {"1", "2", "3", "4", "5"}


def test_canonical_i03_requires_unresolved_when_resolved_target_support_differs_from_denominator():
    source = inspect.getsource(canonical_i03._evaluate_index_group)
    assert 'elif raw_resolved != raw_denominator:' in source
    assert 'state = "UNRESOLVED"' in source
    assert 'positive denominator exists but exact target configuration is unresolved for one or more denominator members' in source


def test_h02_smallest_blocker_hits_required_p0_before_any_broader_lane_claim():
    # P0 uses A000 + T_Q301_2_RAW for each required target cell 1..5.
    # The exact carrier therefore has denominator 29002 but only 28787 rows
    # inside D02's frozen q301_2 substantive target domain 1..5.
    denominator = sum(Q301_2_SOURCE_COUNTS.values())
    resolved = sum(Q301_2_SOURCE_COUNTS[x] for x in range(1, 6))
    assert denominator == 29002
    assert resolved == 28787
    assert resolved != denominator
    assert g02.LANE_EXPECTATIONS["P0"] == {
        "rule_id": "D02_P0_REAL_POSITIVE_CONTROL",
        "candidate_count": 5,
        "query_role_count": 5,
    }
