from __future__ import annotations

import copy
import math

import pytest

from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState, Framework, Stratum
from v3.psyche.gating import DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS, compute_baseline_load


class TrackingDomains(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_calls: list[str] = []

    def get(self, key, default=None):
        self.get_calls.append(key)
        return super().get(key, default)


def _make_state() -> BackboneState:
    state = BackboneState()
    state.domains = TrackingDomains(state.domains)
    for domain in state.domains.values():
        domain.A = 80.0
        domain.V = 80.0
        domain.expression_rate = 41.0
        domain.activation_threshold = 63.0
        domain.affect_channel = "quiet_organizing"
    state.frameworks = [Framework(id="f1", weight=12.0)]
    state.rendered_output = {"chat": {"surface": "hello"}}
    state.child_model = {"voice": "narrative"}
    return state


def _make_strata(high_levels: set[int]) -> list[Stratum]:
    strata: list[Stratum] = []
    for level in range(9):
        is_high = level in high_levels
        strata.append(
            Stratum(
                level=level,
                name=f"stratum_{level}",
                provision_strength=10.0 if is_high else 95.0,
                coercion_strength=80.0 if is_high else 5.0,
                contradiction_load=70.0 if is_high else 5.0,
                visibility_of_complicity=60.0 if is_high else 5.0,
                salience=50.0 if is_high else 5.0,
            )
        )
    return strata


@pytest.mark.parametrize(
    ("level", "target", "comparison"),
    [
        (7, "family_household", "body_self"),
        (8, "body_self", "family_household"),
        (1, "empire_occupation", "family_household"),
        (4, "sect_class_ethnicity", "family_household"),
    ],
)
def test_late_strata_map_to_the_owner_approved_domains(level: int, target: str, comparison: str) -> None:
    state = _make_state()
    state.strata_stack = _make_strata({level})

    compute_baseline_load(state)

    assert state.domains[target].baseline_load > state.domains[comparison].baseline_load
    assert state.domains[target].baseline_load > 0.0


def test_level_eight_pressure_is_not_silently_discarded() -> None:
    control = _make_state()
    control.strata_stack = _make_strata(set())
    compute_baseline_load(control)

    state = _make_state()
    state.strata_stack = _make_strata({8})
    compute_baseline_load(state)

    assert state.domains["body_self"].baseline_load > control.domains["body_self"].baseline_load
    assert state.domains["family_household"].baseline_load > control.domains["family_household"].baseline_load
    assert state.domains["empire_occupation"].baseline_load > control.domains["empire_occupation"].baseline_load


def test_compute_baseline_load_does_not_use_positional_zip_behavior() -> None:
    state = _make_state()
    state.strata_stack = [
        Stratum(
            level=7,
            name="family",
            provision_strength=10.0,
            coercion_strength=80.0,
            contradiction_load=70.0,
            visibility_of_complicity=60.0,
            salience=50.0,
        ),
        Stratum(
            level=8,
            name="self",
            provision_strength=10.0,
            coercion_strength=80.0,
            contradiction_load=70.0,
            visibility_of_complicity=60.0,
            salience=50.0,
        ),
    ]

    compute_baseline_load(state)

    assert state.domains.get_calls == list(DOMAIN_NAMES) + list(DOMAIN_NAMES)
    assert state.domains["family_household"].baseline_load > 0.0
    assert state.domains["body_self"].baseline_load > 0.0


def test_compute_baseline_load_only_changes_baseline_load_fields() -> None:
    state = _make_state()
    state.strata_stack = _make_strata({4, 7, 8})

    before_domains = {name: copy.deepcopy(domain) for name, domain in state.domains.items()}
    before_frameworks = copy.deepcopy(state.frameworks)
    before_rendered_output = copy.deepcopy(state.rendered_output)
    before_child_model = copy.deepcopy(state.child_model)

    compute_baseline_load(state)

    for name in DOMAIN_NAMES:
        before = before_domains[name]
        after = state.domains[name]
        assert after.A == before.A
        assert after.S == before.S
        assert after.V == before.V
        assert after.affect_channel == before.affect_channel
        assert after.expressed_aim == before.expressed_aim
        assert after.expression_rate == before.expression_rate
        assert after.activation_threshold == before.activation_threshold

    assert state.frameworks == before_frameworks
    assert state.rendered_output == before_rendered_output
    assert state.child_model == before_child_model


def test_baseline_load_weights_sum_to_one_and_cover_all_levels() -> None:
    covered_levels: set[int] = set()
    for domain_name, weights in DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS.items():
        assert math.isclose(sum(weights.values()), 1.0, rel_tol=1e-9, abs_tol=1e-9), domain_name
        covered_levels.update(weights)

    assert covered_levels == set(range(9))
