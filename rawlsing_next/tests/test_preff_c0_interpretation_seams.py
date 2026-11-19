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


def test_compound_predicate_unknown_conserves_conclusive_membership_and_not(monkeypatch):
    """Actual native AST control flow, with only its terminal leaf substituted.

    False AND UNKNOWN and True OR UNKNOWN are determinate; the inverse
    combinations and NOT UNKNOWN are not. Non-interpretation errors propagate.
    """
    import rawlsing_next._pre553_query_predicate as native

    visited = []

    def leaf(node, **kwargs):
        state = node["synthetic_epistemic_state"]
        visited.append(state)
        if state == "UNKNOWN":
            raise native.EmpiricalQueryResolutionError(
                "UNRESOLVED_CONDITION_MEMBER: observed physical value uninterpreted"
            )
        if state == "AUTHORITY_ERROR":
            raise native.EmpiricalQueryResolutionError("AUTHORITY_DENIED")
        return state == "TRUE"

    def leaf_node(state):
        return {"op": "LEAF", "synthetic_epistemic_state": state}

    def evaluate(ast):
        return native._eval_predicate(
            ast, respondent=None, index=None, registry=None,
            used=[], used_auth=[], derived_branch_memberships=None,
        )

    with monkeypatch.context() as patch:
        patch.setattr(native, "_leaf_match", leaf)
        for op, conclusive, result in (
            ("AND", "FALSE", False),
            ("OR", "TRUE", True),
        ):
            for order in ("left", "right"):
                nodes = [leaf_node(conclusive), leaf_node("UNKNOWN")]
                if order == "right":
                    nodes.reverse()
                visited.clear()
                assert evaluate({"op": op, "children": nodes}) is result
                assert len(visited) == 2  # no silently hidden source obligation

        for op, other in (("AND", "TRUE"), ("OR", "FALSE")):
            with pytest.raises(native.EmpiricalQueryResolutionError,
                               match="UNRESOLVED_CONDITION_MEMBER"):
                evaluate({"op": op, "children": [leaf_node(other), leaf_node("UNKNOWN")]})
        with pytest.raises(native.EmpiricalQueryResolutionError,
                           match="UNRESOLVED_CONDITION_MEMBER"):
            evaluate({"op": "NOT", "children": [leaf_node("UNKNOWN")]})
        with pytest.raises(native.EmpiricalQueryResolutionError,
                           match="UNRESOLVED_CONDITION_MEMBER"):
            evaluate({"op": "NOT", "children": [
                {"op": "OR", "children": [leaf_node("FALSE"), leaf_node("UNKNOWN")]}
            ]})
        assert evaluate({"op": "NOT", "children": [
            {"op": "OR", "children": [leaf_node("TRUE"), leaf_node("UNKNOWN")]}
        ]}) is False
        for op in ("AND", "OR"):
            with pytest.raises(native.EmpiricalQueryResolutionError,
                               match="AUTHORITY_DENIED"):
                evaluate({"op": op, "children": [
                    leaf_node("FALSE" if op == "AND" else "TRUE"),
                    leaf_node("AUTHORITY_ERROR"),
                ]})



def test_multi_response_same_leaf_known_positive_survives_unknown(monkeypatch):
    """A leaf is itself an OR of approved repeated response events.

    One known affirmative + one uninterpreted is conclusive TRUE;
    one known negative + one uninterpreted is UNKNOWN. Every event is
    still authority-checked, recorded and retained as source evidence.
    """
    from types import SimpleNamespace
    import rawlsing_next._pre553_query_predicate as native
    from rawlsing_next.tests import test_pre553_empirical_query as fixture

    source = fixture._build_source(
        "PREFF-LEAF-UNKNOWN", [
            {"id": "R1", "responses": {"X": 1}},
        ],
    )
    auth = source["source_auth"].authority_ref
    question = source["qrefs"]["X"]
    registry = fixture._registry(source, fixture._query_authority("PREFF-LEAF-UNKNOWN"))
    row_ref = source["universe"].ref
    fake_respondent = SimpleNamespace(ref=row_ref)
    fake_index = SimpleNamespace(universe=source["universe"])
    node = {
        "leaf_type": "SURVEY_RESPONSE_EVENT",
        "question_semantic_ref": question,
        "component_or_event_selector_ref": question,
        "response_value_or_state_ref": question,
        "response_topology_authority_ref": auth,
        "response_semantic_authority_ref": auth,
        "operator": "STATE_EQ",
        "typed_state": "SUBSTANTIVE_RESPONSE",
    }
    known = SimpleNamespace(
        typed_state="SUBSTANTIVE_RESPONSE",
        authority_snapshot_refs=(auth,),
        ref=question,
    )
    unknown = SimpleNamespace(
        typed_state="INVALID_UNRESOLVED",
        authority_snapshot_refs=(auth,),
        ref=question,
    )
    negative = SimpleNamespace(
        typed_state="MISSING",
        authority_snapshot_refs=(auth,),
        ref=question,
    )
    captured = []
    with monkeypatch.context() as patch:
        patch.setattr(
            native, "_validate_public_object_authorities",
            lambda event, registry: (auth,),
        )
        patch.setattr(
            native, "_select_respondent_events",
            lambda *args, **kwargs: iter((known, unknown)),
        )
        assert native._leaf_match(
            node, respondent=fake_respondent, index=fake_index,
            registry=registry, used=captured, used_auth=[],
        ) is True
        assert captured == [known, unknown]
        captured.clear()
        patch.setattr(
            native, "_select_respondent_events",
            lambda *args, **kwargs: iter((negative, unknown)),
        )
        with pytest.raises(
            native.UnresolvedConditionMember,
            match="UNRESOLVED_CONDITION_MEMBER",
        ):
            native._leaf_match(
                node, respondent=fake_respondent, index=fake_index,
                registry=registry, used=captured, used_auth=[],
            )
        assert captured == [negative, unknown]
