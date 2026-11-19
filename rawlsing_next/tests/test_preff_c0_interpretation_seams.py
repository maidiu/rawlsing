"""C0 joined Codex acc264 sourcefree native predicate/I05/BATCH first-fault tests.

Real saved-estate combined trace remains a separate C1 test. These tiny
tests identify the exact owner when typed unknown would become false, empty,
or a completed Batch response without actual native evidence.
"""
from types import SimpleNamespace

import pytest

from rawlsing_next._pre553_query_predicate import (
    EmpiricalQueryResolutionError, _refuse_unresolved_value_leaf,
)
from rawlsing_next.pre553_discovery_exact import _terminal_fact_class
from rawlsing_next.tests.test_pyat1097_held_integrity_and_i05 import (
    _partial_unresolved_fixture,
)
from rawlsing_next.tests.test_pyat1009_ff01_generic_ingress import _case


def test_unmapped_response_is_never_boolean_false_even_under_not_leaf():
    unknown = SimpleNamespace(typed_state="INVALID_UNRESOLVED")
    # Calling a non-diagnostic response leaf must stop rather than
    # collapsing UNKNOWN into false that NOT could invert into a match.
    for leaf in (
        {"leaf_type": "SURVEY_RESPONSE_EVENT", "operator": "EQ"},
        {"leaf_type": "SURVEY_RESPONSE_EVENT", "operator": "IN"},
        {"leaf_type": "SURVEY_RESPONSE_EVENT", "operator": "STATE_EQ",
         "typed_state": "MISSING"},
        {"leaf_type": "TYPED_RESPONSE_STATE", "typed_state": "MISSING"},
        {"leaf_type": "GOVERNED_PUBLIC_RESPONSE_VALUE"},
    ):
        with pytest.raises(EmpiricalQueryResolutionError, match="UNRESOLVED_CONDITION_MEMBER"):
            _refuse_unresolved_value_leaf(unknown, leaf)
    # A specifically issued typed-diagnostic query may inspect the source
    # state. This is NOT substantive approval for an arbitrary Q/F target.
    _refuse_unresolved_value_leaf(
        unknown, {"leaf_type": "TYPED_RESPONSE_STATE",
                  "typed_state": "INVALID_UNRESOLVED"},
    )
    _refuse_unresolved_value_leaf(
        unknown, {"leaf_type": "SURVEY_RESPONSE_EVENT", "operator": "STATE_EQ",
                  "typed_state": "INVALID_UNRESOLVED"},
    )


def test_source_declared_missing_keeps_its_distinct_typed_state():
    for state in ("MISSING", "NOT_ASKED", "INAPPLICABLE"):
        _refuse_unresolved_value_leaf(
            SimpleNamespace(typed_state=state),
            {"leaf_type": "SURVEY_RESPONSE_EVENT", "operator": "EQ"},
        )


def test_native_i05_terminal_preserves_unknown_distinct_from_valid_empty():
    _, _, _, query, execution = _case()
    original = execution.facts[0]
    _, held_result = _partial_unresolved_fixture()
    unresolved = held_result.facts[0]
    assert unresolved.raw_denominator_support == 4
    assert unresolved.raw_numerator_support == 3
    assert _terminal_fact_class((unresolved,)) == "UNRESOLVED"
    assert _terminal_fact_class((original, unresolved)) == "UNRESOLVED"
    assert _terminal_fact_class((original,)) is None
