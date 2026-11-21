"""PF-025: absent source event is NOT an observed empty target collection.

This is a sourcefree first-fault test of the real I03 target component reader,
using only a controlled zero-event selector. It does not issue a new legitimate
administered-empty semantics contract or establish original-source science.
"""
from types import SimpleNamespace

import pytest

import rawlsing_next._pre553_query_eval as query_eval


TOPOLOGIES = (
    "SCALAR_SINGULAR",
    "ROUTED_RESPONSE",
    "COMPONENTIZED_RESPONSE",
    "UNORDERED_MULTISELECT_SET",
    "UNORDERED_MULTISELECT",
    "MULTISELECT",
    "ORDERED_SEQUENCE",
    "RANKED_RESPONSE",
    "REPEATED_EVENT",
    "REPEATED_MEASUREMENT",
)


@pytest.mark.parametrize("topology", TOPOLOGIES)
def test_absent_exact_event_is_unresolved_not_observed_empty(monkeypatch, topology):
    """A routed eligible case with no exact target event cannot form a cell."""
    seen = []

    def select(index, respondent_key, target_ref, *,
               include_component, states):
        assert respondent_key == "respondent-sourcefree"
        assert target_ref == "sourcefree-target"
        assert include_component is True
        assert states == frozenset({"SUBSTANTIVE_RESPONSE"})
        seen.append((respondent_key, target_ref))
        return iter(())

    monkeypatch.setattr(query_eval, "_select_respondent_events", select)
    respondent = SimpleNamespace(
        ref=SimpleNamespace(key="respondent-sourcefree"),
    )
    component = SimpleNamespace(
        target_ref="sourcefree-target",
        topology=topology,
        included_states=frozenset({"SUBSTANTIVE_RESPONSE"}),
    )
    used = []
    used_auth = []
    admitted, value = query_eval._target_component_value(
        respondent, object(), component, object(), used, used_auth,
    )
    assert (admitted, value) == (False, None)
    assert seen == [("respondent-sourcefree", "sourcefree-target")]
    assert used == [] and used_auth == []


@pytest.mark.parametrize("topology", TOPOLOGIES[3:])
def test_absent_multi_response_component_blocks_full_joint(monkeypatch, topology):
    """No missing component can become an empty but SUPPORTED joint coordinate."""
    monkeypatch.setattr(
        query_eval, "_select_respondent_events",
        lambda *_args, **_kwargs: iter(()),
    )
    component = SimpleNamespace(
        target_ref="sourcefree-target", topology=topology,
        included_states=frozenset({"SUBSTANTIVE_RESPONSE"}),
    )
    plan = SimpleNamespace(components=(component,), arity=1)
    admitted, joint = query_eval._target_configuration(
        SimpleNamespace(ref=SimpleNamespace(key="respondent-sourcefree")),
        object(), plan=plan, registry=object(), used=[], used_auth=[],
    )
    assert admitted is False
    assert joint is None
