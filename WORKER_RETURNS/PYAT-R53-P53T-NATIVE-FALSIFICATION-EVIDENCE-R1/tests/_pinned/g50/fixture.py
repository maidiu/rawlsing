"""Synthetic frozen SourceDecisionBundle / ScientificGrammarPolicy fixture (TEST_ONLY).

No respondent source is opened. The values below are synthetic witnesses; they
never enter the symbolic E_pre root. This fixture is explicitly proposal-grade.
"""
from __future__ import annotations

from dataclasses import replace

from .types import ItemOccurrence, MeasurePlan, ScientificGrammarPolicy, SourceDecisionBundle

PROPOSAL_OWNER = "M48_PROPOSED_SCIENTIFIC_CONSTITUTION@91f70358a7682e983276e79777bc591841162392"
PROPOSAL_GRADE = "PROPOSED_TEST_ONLY"


def items() -> tuple[ItemOccurrence, ...]:
    def item(item_id, *, unit="adult", topology="SCALAR_SINGULAR", forms=("F",),
             target=True, conditioner=True, route="KNOWN", semantic="UNRESOLVED"):
        return ItemOccurrence(
            item_id=item_id, label=item_id, unit=unit, topology=topology,
            forms=tuple(forms), domain=(0, 1), target_role=target,
            conditioner_role=conditioner, route_state=route,
            semantic_state=semantic, scope="SYNTH-W1",
        )

    return (
        item("A"),
        item("B"),
        item("M"),
        item("Y"),
        item("ID", target=False, conditioner=False, semantic="ADMINISTRATIVE_NONSEMANTIC"),
        item("H", unit="household"),
        item("SET", topology="MULTI_SELECT_SET"),
        item("RANK", topology="RANKED_RESPONSE"),
        item("REP", topology="REPEATED_OCCASION"),
        item("X1", forms=("F1",)),
        item("X2", forms=("F2",)),
        item("RT", route="UNKNOWN"),
        item("DK", semantic="SPECIAL_STATE_PRESERVED"),
    )


def bundle(*, inventory_complete: bool = True) -> SourceDecisionBundle:
    return SourceDecisionBundle(
        bundle_id="SYNTH-G50-BUNDLE-1",
        source_id="SYNTH-SRC-A",
        wave="SYNTH-W1",
        edition="SYNTH-ED-1",
        source_sha256="a" * 64,
        scope="SYNTH-W1",
        items=items(),
        measure_plans=(
            MeasurePlan("M-SAMPLE", "SAMPLE", None, None, "achieved-sample-description", "UNQUANTIFIED_SAMPLE"),
            MeasurePlan("M-POP", "POPULATION", None, None, "target-population-proportion", "NO_DESIGN_VARIANCE"),
        ),
        risk_set_ref="RISK-SYNTH-ALL",
        route_states=("KNOWN", "UNKNOWN"),
        unit_transforms=("ADULT_SELF",),
        state_map={"DK": "DONT_KNOW", "REFUSE": "REFUSED", "MISSING": "NOT_ADMINISTERED"},
        authority_refs=(PROPOSAL_OWNER,),
        current_selection=None,
        inventory_complete=inventory_complete,
        inventory_gaps=() if inventory_complete else ("SYNTH-UNRESOLVED-MODULE-COVERAGE",),
        held=("CURRENT_SOURCE_HOST_PURPOSE_NOT_GRANTED",),
        unresolved=("D2_COMPLETE_ADMINISTERED_OCCURRENCES", "D3_ROUTE_UNIT_STATE_FOR_UNKNOWN", "D5_ISSUED_GRAMMAR_POLICY"),
    )


def policy() -> ScientificGrammarPolicy:
    return ScientificGrammarPolicy(
        policy_id="SYNTH-M48-POLICY-CANDIDATE-1",
        grade=PROPOSAL_GRADE,
        allowed_classes=("DIST", "CONDITIONAL", "JOINT", "CO_TRAVEL", "FORK",
                         "INTERACTION", "REVERSAL", "STATE_ROBUSTNESS"),
        separate_classes=("CROSS_SOURCE", "TEMPORAL", "POSSIBILITY", "STRUCTURAL"),
        target_roles=("A", "B", "M", "Y"),
        conditioner_roles=("A", "B", "M", "Y"),
        denied_roles=("ID",),
        bounds={"J": 3, "K": 2, "D": 2},
        population_requires_weight=True,
        exclusions=("ADMIN_ID_TARGET", "TARGET_LEAKAGE", "UNLINKED_UNIT_JOINT",
                    "UNKNOWN_ROUTE", "DISJOINT_FORMS", "UNSANCTIONED_TOPOLOGY",
                    "POPULATION_WITHOUT_WEIGHT", "REVERSE_ROLE_NOT_AUTHORIZED",
                    "TARGET_ALIAS_AS_CONDITIONER"),
        validation_policy="EXPLORATORY_DESCRIPTIVE_ONLY_UNTIL_COMPETENT_VALIDATION",
        exploration_policy="FINITE_FULL_SYMBOLIC_FRONTIER_NO_UNARY_PRUNE",
        stop_policy="EXACT_COMPLETE_OR_BUDGET_PARTIAL_WITH_PENDING_IDS",
        owner_refs=(PROPOSAL_OWNER,),
        authority_refs=("urn:g50:proposal:policy-candidate-1",),
    )


def synthetic_rows() -> list[dict]:
    """100 synthetic rows: balanced A/B XOR, 10% M minority, correlated admin ID."""

    rows = []
    for i in range(100):
        a = i % 2
        b = (i // 2) % 2
        y = a ^ b
        rows.append({
            "id": f"R{i:03d}",
            "responses": {
                "A": a, "B": b, "M": int(i < 10), "Y": y,
                "ID": y,  # deliberately outcome-correlated administrative column
                "H": a, "SET": i % 2, "RANK": i % 2, "REP": i % 2,
                "X1": i % 2, "X2": 1 - (i % 2), "RT": i % 2, "DK": i % 2,
            },
        })
    return rows


def incomplete_bundle() -> SourceDecisionBundle:
    return replace(bundle(), bundle_id="SYNTH-G50-BUNDLE-INCOMPLETE-1",
                   inventory_complete=False)


__all__ = ["PROPOSAL_OWNER", "PROPOSAL_GRADE", "items", "bundle", "policy",
           "synthetic_rows", "incomplete_bundle"]
