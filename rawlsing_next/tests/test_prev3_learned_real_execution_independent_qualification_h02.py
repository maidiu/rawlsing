import inspect

from rawlsing_next import _pre553_query_eval as canonical_i03
from rawlsing_next import prev3_learned_real_execution_r2 as g02


# Exact independent direct-carrier counts from Library file
# file_0000000036dc81f8b8b546e356590a03 / LITS-2006-data.dta
# SHA-256 7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09
Q301_2_SOURCE_COUNTS = {1: 4377, 2: 6440, 3: 5226, 4: 6972, 5: 1882, 6: 1774, 7: 2327, None: 4}
Q301_7_SOURCE_COUNTS = {1: 2889, 2: 6112, 3: 6511, 4: 10334, 5: 2479, 6: 224, 7: 442, None: 11}


def _synthetic_records(target):
    rows = []
    for value in (1, 2, 3, 4, 5, 6, 7, None):
        row = {"q301_2": 1, "q301_7": 1, "q310": 1, "q311": 1}
        row[target] = value
        rows.append(row)
    return rows


def test_exact_source_q301_2_has_4105_denominator_members_outside_g02_projected_domain():
    assert sum(Q301_2_SOURCE_COUNTS.values()) == 29002
    projected = sum(Q301_2_SOURCE_COUNTS[x] for x in range(1, 6))
    outside = Q301_2_SOURCE_COUNTS[6] + Q301_2_SOURCE_COUNTS[7] + Q301_2_SOURCE_COUNTS[None]
    assert projected == 24897
    assert outside == 4105
    assert projected + outside == 29002


def test_exact_source_q301_7_has_677_denominator_members_outside_g02_projected_domain():
    assert sum(Q301_7_SOURCE_COUNTS.values()) == 29002
    projected = sum(Q301_7_SOURCE_COUNTS[x] for x in range(1, 6))
    outside = Q301_7_SOURCE_COUNTS[6] + Q301_7_SOURCE_COUNTS[7] + Q301_7_SOURCE_COUNTS[None]
    assert projected == 28325
    assert outside == 677
    assert projected + outside == 29002


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
    # G02 counts all 29,002 selected source rows in the denominator but only
    # emits target cells 1..5, whose exact carrier support sums to 24,897.
    denominator = sum(Q301_2_SOURCE_COUNTS.values())
    projected = sum(Q301_2_SOURCE_COUNTS[x] for x in range(1, 6))
    assert denominator == 29002
    assert projected == 24897
    assert projected != denominator
    assert g02.LANE_EXPECTATIONS["P0"] == {
        "rule_id": "D02_P0_REAL_POSITIVE_CONTROL",
        "candidate_count": 5,
        "query_role_count": 5,
    }
