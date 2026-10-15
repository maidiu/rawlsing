"""POST-ASTRA R3 PE — source-free fixture builders and two independent law fixtures.

This module is deliberately separate from the candidate service.  It freezes the
exact synthetic source law, the accepted-authority bindings and the expected
canonical results BEFORE any service output is used as expected truth.

Independence argument:

* two genuinely different synthetic source laws are defined here (N100 and
  N110), not read back from the service;
* the expected canonical results are exact arithmetic on those tables;
* the accepted C1-00 authority snapshots and I03 query builders are reused
  unchanged from the existing frozen fixture helpers (read-only reuse, no
  modification of adopted owner code);
* the N9 world dependency is a declared TEST-ONLY immutable selected/asof
  fixture identity — this seam never invents operative N9 current.

Everything here is source-free: synthetic fixture rows, no raw survey file, no
real-source C11 execution, no measured P2X, no Candidate A/B/C, no V3, no actor.
"""
from __future__ import annotations

from typing import Any

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
)
from rawlsing_next.pre553_postastra_pe_generic_world_possibility import (
    N9WorldDependency,
    ROLE_FORWARD,
    ROLE_MULTI,
    ROLE_REVERSE,
)

import rawlsing_next.tests.test_pre553_empirical_query as i03
from rawlsing_next.tests.n10e_empirical_slice_fixture import (
    fixture_authority,
    frozen_at07_source,
    build_model_rule,
)
from rawlsing_next.tests.c1_at08_at13_fixture import (
    build_witness_for_binding,
    make_conditioner_binding,
    make_multi_conditioner_consumer_query,
    make_pairing_authority,
    make_model_rule as make_c1_02_model_rule,
    subject_fact_ref,
)

# ---------------------------------------------------------------------------
# Two independent synthetic source laws
# ---------------------------------------------------------------------------

#: Law A — 100 respondents over POSITION x ANSWER x COHORT.
#:   P1,A: 27 yes / 3 no   (30)  -> 27/30 = 9/10
#:   P1,B: 21 yes / 9 no   (30)  -> 21/30 = 7/10
#:   P2,A: 12 yes / 8 no   (20)  -> 12/20 = 3/5
#:   P2,B:  4 yes / 16 no  (20)  ->  4/20 = 1/5
#: Single forward POSITION=P1 -> ANSWER: 48/60 = 4/5.
#: Reverse ANSWER=yes -> POSITION: 48/64 = 3/4.
LAW_A_ROWS_SPEC = (
    ("P1", "A", 27, 3, "P1AY", "P1AN"),
    ("P1", "B", 21, 9, "P1BY", "P1BN"),
    ("P2", "A", 12, 8, "P2AY", "P2AN"),
    ("P2", "B", 4, 16, "P2BY", "P2BN"),
)

LAW_A_ID = "POSTASTRA_PE_LAW_A_N100"
LAW_A_ORACLE = {
    "fixture_id": LAW_A_ID,
    "fixture_rows": 100,
    "multi_binding": {
        "direction": "POSITION_P1_AND_COHORT_A_TO_ANSWER",
        "denominator": 30,
        "cells": {"yes": 27, "no": 3},
        "expected_fraction_yes": {"$exact_fraction": [9, 10]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
    "multi_binding_alt": {
        "direction": "POSITION_P1_AND_COHORT_B_TO_ANSWER",
        "denominator": 30,
        "cells": {"yes": 21, "no": 9},
        "expected_fraction_yes": {"$exact_fraction": [7, 10]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
    "forward_single": {
        "direction": "POSITION_P1_TO_ANSWER",
        "denominator": 60,
        "cells": {"yes": 48, "no": 12},
        "expected_fraction_yes": {"$exact_fraction": [4, 5]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
    "reverse_single": {
        "direction": "ANSWER_YES_TO_POSITION",
        "denominator": 64,
        "cells": {"P1": 48, "P2": 16},
        "expected_fraction_P1": {"$exact_fraction": [3, 4]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
}

#: Law B — 110 respondents: Law A plus 10 extra ``P1,A,yes`` respondents.
#:   P1,A: 37 yes / 3 no  (40)  -> 37/40
#:   P1,B: 21 yes / 9 no  (30)  -> 21/30 = 7/10
#:   P2,A: 12 yes / 8 no  (20)  -> 12/20 = 3/5
#:   P2,B:  4 yes / 16 no (20)  ->  4/20 = 1/5
#: Multi (P1,A): 37/40; single P1: 58/70 = 29/35; reverse yes: 58/74 = 29/37.
LAW_B_EXTRA_ROWS = 10
LAW_B_ID = "POSTASTRA_PE_LAW_B_N110_CHANGED_SOURCE"
LAW_B_ORACLE = {
    "fixture_id": LAW_B_ID,
    "fixture_rows": 110,
    "multi_binding": {
        "direction": "POSITION_P1_AND_COHORT_A_TO_ANSWER",
        "denominator": 40,
        "cells": {"yes": 37, "no": 3},
        "expected_fraction_yes": {"$exact_fraction": [37, 40]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
    "multi_binding_alt": {
        "direction": "POSITION_P1_AND_COHORT_B_TO_ANSWER",
        "denominator": 30,
        "cells": {"yes": 21, "no": 9},
        "expected_fraction_yes": {"$exact_fraction": [7, 10]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
    "forward_single": {
        "direction": "POSITION_P1_TO_ANSWER",
        "denominator": 70,
        "cells": {"yes": 58, "no": 12},
        "expected_fraction_yes": {"$exact_fraction": [29, 35]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
    "reverse_single": {
        "direction": "ANSWER_YES_TO_POSITION",
        "denominator": 74,
        "cells": {"P1": 58, "P2": 16},
        "expected_fraction_P1": {"$exact_fraction": [29, 37]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
    "expected_relation_to_law_a": {
        "multi_binding_denominator_differs": True,
        "multi_binding_fraction_differs": True,
        "cohort_b_slice_unchanged": True,
    },
}


def law_a_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for position, cohort, yes, no, yprefix, nprefix in LAW_A_ROWS_SPEC:
        rows.extend(
            {
                "id": f"{yprefix}{n:03d}",
                "responses": {"POSITION": position, "COHORT": cohort, "ANSWER": "yes"},
            }
            for n in range(1, yes + 1)
        )
        rows.extend(
            {
                "id": f"{nprefix}{n:03d}",
                "responses": {"POSITION": position, "COHORT": cohort, "ANSWER": "no"},
            }
            for n in range(1, no + 1)
        )
    return rows


def law_b_rows() -> list[dict[str, Any]]:
    extra = [
        {
            "id": f"P1AX{n:03d}",
            "responses": {"POSITION": "P1", "COHORT": "A", "ANSWER": "yes"},
        }
        for n in range(1, LAW_B_EXTRA_ROWS + 1)
    ]
    return law_a_rows() + extra


def _independent_arithmetic(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Exact arithmetic on the row law; never reads service output."""

    def cell(pred):
        return sum(1 for r in rows if pred(r["responses"]))

    multi_a_yes = cell(lambda x: x["POSITION"] == "P1" and x["COHORT"] == "A" and x["ANSWER"] == "yes")
    multi_a_no = cell(lambda x: x["POSITION"] == "P1" and x["COHORT"] == "A" and x["ANSWER"] == "no")
    multi_b_yes = cell(lambda x: x["POSITION"] == "P1" and x["COHORT"] == "B" and x["ANSWER"] == "yes")
    multi_b_no = cell(lambda x: x["POSITION"] == "P1" and x["COHORT"] == "B" and x["ANSWER"] == "no")
    p1_yes = cell(lambda x: x["POSITION"] == "P1" and x["ANSWER"] == "yes")
    p1_no = cell(lambda x: x["POSITION"] == "P1" and x["ANSWER"] == "no")
    yes_p1 = p1_yes
    yes_total = cell(lambda x: x["ANSWER"] == "yes")
    return {
        "multi_a": {"yes": multi_a_yes, "no": multi_a_no, "denominator": multi_a_yes + multi_a_no},
        "multi_b": {"yes": multi_b_yes, "no": multi_b_no, "denominator": multi_b_yes + multi_b_no},
        "single_p1": {"yes": p1_yes, "no": p1_no, "denominator": p1_yes + p1_no},
        "reverse_yes": {"P1": yes_p1, "P2": yes_total - yes_p1, "denominator": yes_total},
    }


# ---------------------------------------------------------------------------
# N9 world dependency fixture (TEST_ONLY; never operative N9 current)
# ---------------------------------------------------------------------------

N9_TEST_SNAPSHOT_STATE = "SELECTED_IMMUTABLE"


def _pe_ref(kind: str, tag: str, material: object) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:test:postastra-pe:{kind.lower()}:{tag}:sha256:{digest}", digest)


def make_n9_world_dependency(
    *,
    tag: str = "law-a",
    snapshot_state: str = N9_TEST_SNAPSHOT_STATE,
    asof_time: str = "2021-06-30",
    request_time: str = "2026-10-14",
) -> N9WorldDependency:
    snapshot_material = {"schema": "POSTASTRA_PE_N9_TEST_SNAPSHOT@1", "tag": tag, "cut": "selected"}
    asof_material = {"schema": "POSTASTRA_PE_N9_TEST_ASOF@1", "tag": tag, "asof_time": asof_time}
    selected_dep = _pe_ref(
        "POSTASTRA_PE_N9_SELECTED_DEPENDENCY@1",
        f"{tag}-selected",
        {"tag": tag, "kind": "selected_dependency"},
    )
    asof_dep = _pe_ref(
        "POSTASTRA_PE_N9_ASOF_DEPENDENCY@1",
        f"{tag}-asof",
        {"tag": tag, "kind": "asof_dependency", "asof_time": asof_time},
    )
    return N9WorldDependency(
        n9_snapshot_ref=_pe_ref("POSTASTRA_PE_N9_TEST_SNAPSHOT@1", f"{tag}-snapshot", snapshot_material),
        n9_asof_ref=_pe_ref("POSTASTRA_PE_N9_TEST_ASOF@1", f"{tag}-asof-ref", asof_material),
        n9_asof_time=asof_time,
        n9_snapshot_state=snapshot_state,
        selected_dependency_refs=(selected_dep,),
        asof_dependency_refs=(asof_dep,),
    )


#: The frozen request-time coordinate for all positive fixtures.
REQUEST_TIME = "2026-10-14"
NATIVE_UNIT = "INDIVIDUAL_RESPONDENT_SAME_RESPONDENT_UNIT"


def make_unit_refs(*, analysis_unit: str = NATIVE_UNIT) -> tuple[ExactRef, ExactRef]:
    native = _pe_ref("POSTASTRA_PE_UNIT_REF@1", "native", {"unit": NATIVE_UNIT})
    if analysis_unit == NATIVE_UNIT:
        return native, native
    analysis = _pe_ref("POSTASTRA_PE_UNIT_REF@1", "analysis", {"unit": analysis_unit})
    return native, analysis


# ---------------------------------------------------------------------------
# Case assembly — producer + consumer + N9 deps through the SAME service shape
# ---------------------------------------------------------------------------


def _pe_model_rule(source_universe_ref: ExactRef, tag: str) -> PositionedSubjectPossibilityModelRule:
    model = AuthorityRef(
        authority_id=f"urn:test:postastra-pe:model-authority:{tag}",
        authority_version="1.0.0",
        authority_content_hash=semantic_hash({"schema": "POSTASTRA_PE_MODEL_AUTHORITY@1", "tag": tag}),
    )
    walkback = AuthorityRef(
        authority_id=f"urn:test:postastra-pe:walkback-authority:{tag}",
        authority_version="1.0.0",
        authority_content_hash=semantic_hash({"schema": "POSTASTRA_PE_WALKBACK_AUTHORITY@1", "tag": tag}),
    )
    return PositionedSubjectPossibilityModelRule(
        model_authority_ref=model,
        walkback_authority_ref=walkback,
        source_universe_refs=(source_universe_ref,),
        walkback_steps=(),
        positive_proxy_authority_refs=(),
    )


def make_role_reversal_authority(tag: str = "reverse") -> AuthorityRef:
    return AuthorityRef(
        authority_id=f"urn:test:postastra-pe:role-reversal-authority:{tag}",
        authority_version="1.0.0",
        authority_content_hash=semantic_hash(
            {"schema": "POSTASTRA_PE_ROLE_REVERSAL_AUTHORITY@1", "tag": tag, "scope": "ANSWER_TO_POSITION"}
        ),
    )


def build_three_consumer_cases(
    *, law_rows: list[dict[str, Any]], law_tag: str
) -> dict[str, dict[str, Any]]:
    """Assemble the three generic consumers over one synthetic source law.

    All three go through the SAME generic request shape and the SAME accepted C1
    composition.  Consumer flavor is a downstream TEST-ONLY scenario label only;
    the request schema carries no parent nouns.
    """
    source_kwargs: dict[str, Any] = {
        "question_namespace": f"postastra-pe-{law_tag}",
        "risk_sets": {
            "R_ALL": {
                "POSITION": {r["id"] for r in law_rows},
                "ANSWER": {r["id"] for r in law_rows},
                "COHORT": {r["id"] for r in law_rows},
            }
        },
        "risk_namespace": f"postastra-pe-{law_tag}",
    }
    source = i03._build_source(f"postastra-pe-{law_tag}", law_rows, **source_kwargs)
    source["risk_refs"]["R"] = source["risk_refs"]["R_ALL"]
    query_auth = i03._query_authority(f"postastra-pe-{law_tag}")
    from rawlsing_next.pre553_empirical_authority import AuthorityRegistry

    registry = AuthorityRegistry((*source["authorities"], query_auth))
    pairing = make_pairing_authority(f"postastra-pe-{law_tag}")
    model_rule = _pe_model_rule(source["universe"].ref, law_tag)
    risk_ref = source["risk_refs"]["R"]
    native_unit, analysis_unit = make_unit_refs()
    denominator_basis = risk_ref

    cases: dict[str, dict[str, Any]] = {}

    # ---- Consumer 1: multi-binding parent-context (TEST_ONLY label) ----
    conditions = [
        ("RESPONSE", "POSITION", "P1"),
        ("RESPONSE", "COHORT", "A"),
    ]
    predicate = i03._predicate(
        source,
        query_auth,
        {
            "op": "AND",
            "children": [
                i03._response_leaf(source, query_auth, "POSITION", "P1"),
                i03._response_leaf(source, query_auth, "COHORT", "A"),
            ],
        },
        tag=f"postastra-pe-{law_tag}-multi",
    )
    producer_query = i03._query(
        source,
        query_auth,
        predicate,
        ("ANSWER",),
        risk="R",
        tag=f"postastra-pe-{law_tag}-multi",
    )
    component = dict(producer_query.target_arity_and_topology["components"][0])
    component["domain"] = ["no", "yes"]
    component["target_domain_replay_ref"] = i03._ref("TARGET_DOMAIN", "ANSWER-no-yes")
    from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec

    producer_query = EmpiricalQuerySpec(
        typed_state=producer_query.typed_state,
        authority_snapshot_refs=producer_query.authority_snapshot_refs,
        dependency_refs=producer_query.dependency_refs,
        producer_replay_locator_or_reference_root=producer_query.producer_replay_locator_or_reference_root,
        target_refs=producer_query.target_refs,
        target_arity_and_topology={
            "arity": 1,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": [component],
        },
        condition_predicate_ref=producer_query.condition_predicate_ref,
        risk_set_ref=producer_query.risk_set_ref,
        empirical_universe_refs=producer_query.empirical_universe_refs,
        scope_refs=producer_query.scope_refs,
        measure_basis_ref=producer_query.measure_basis_ref,
        requested_output_grain=producer_query.requested_output_grain,
        query_authority_refs=producer_query.query_authority_refs,
    )
    bindings = []
    pairs = []
    for binding_id, (_kind, question, value) in zip(("position", "cohort"), conditions):
        bindings.append(
            make_conditioner_binding(
                binding_id=binding_id,
                subject_fact_ref=ExactRef(**subject_fact_ref(source, question, value)),
                empirical_coordinate_ref=source["qrefs"][question],
                comparability_authority_ref=pairing,
                source_universe_ref=source["universe"].ref,
                release_ref=source["release_ref"],
            )
        )
        pairs.append((source["qrefs"][question], value))
    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        f"urn:test:postastra-pe:{law_tag}:multi-subject",
        semantic_hash({"fixture_id": f"{law_tag}-multi", "flavor": "TEST_ONLY_FAMILY_CARE_CONTEXT"}),
    )
    request = _build_request(
        request_id=f"postastra-pe-{law_tag}-multi",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["ANSWER"],
        bindings=bindings,
        role_direction=ROLE_MULTI,
        native_unit_ref=native_unit,
        analysis_unit_ref=analysis_unit,
        denominator_basis_ref=denominator_basis,
        operation_authority_ref=pairing,
        model_rule=model_rule,
        n9_tag=law_tag,
        projection={"kind": "TEST_ONLY_FAMILY_CARE_CONTEXT_MULTI_BINDING", "scenario": "family_care_context"},
    )
    consumer_query = request.derived_positioned_query()
    witness = build_witness_for_binding(
        witness_object_id=f"urn:test:postastra-pe:{law_tag}:multi-witness",
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=predicate,
        bindings=bindings,
        coordinate_value_pairs=pairs,
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        leaf_type="SURVEY_RESPONSE_EVENT",
    )
    cases["multi_binding_parent_context"] = {
        "request": request,
        "model_rule": model_rule,
        "witness": witness,
        "predicate": predicate,
        "empirical_query": producer_query,
        "release_refs": (source["release_ref"],),
        "registry": registry,
        "repository": source["repo"],
        "expected": "multi_binding",
    }

    # ---- Consumer 2: nonparent reverse (lawful role/target reversal) ----
    predicate_r = i03._predicate(
        source,
        query_auth,
        i03._response_leaf(source, query_auth, "ANSWER", "yes"),
        tag=f"postastra-pe-{law_tag}-rev",
    )
    producer_query_r = i03._query(
        source,
        query_auth,
        predicate_r,
        ("POSITION",),
        risk="R",
        tag=f"postastra-pe-{law_tag}-rev",
    )
    component_r = dict(producer_query_r.target_arity_and_topology["components"][0])
    component_r["domain"] = ["P1", "P2"]
    component_r["target_domain_replay_ref"] = i03._ref("TARGET_DOMAIN", "POSITION-P1-P2")
    producer_query_r = EmpiricalQuerySpec(
        typed_state=producer_query_r.typed_state,
        authority_snapshot_refs=producer_query_r.authority_snapshot_refs,
        dependency_refs=producer_query_r.dependency_refs,
        producer_replay_locator_or_reference_root=producer_query_r.producer_replay_locator_or_reference_root,
        target_refs=producer_query_r.target_refs,
        target_arity_and_topology={
            "arity": 1,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": [component_r],
        },
        condition_predicate_ref=producer_query_r.condition_predicate_ref,
        risk_set_ref=producer_query_r.risk_set_ref,
        empirical_universe_refs=producer_query_r.empirical_universe_refs,
        scope_refs=producer_query_r.scope_refs,
        measure_basis_ref=producer_query_r.measure_basis_ref,
        requested_output_grain=producer_query_r.requested_output_grain,
        query_authority_refs=producer_query_r.query_authority_refs,
    )
    binding_r = make_conditioner_binding(
        binding_id="answer",
        subject_fact_ref=ExactRef(**subject_fact_ref(source, "ANSWER", "yes")),
        empirical_coordinate_ref=source["qrefs"]["ANSWER"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    request_r = _build_request(
        request_id=f"postastra-pe-{law_tag}-nonparent-rev",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            f"urn:test:postastra-pe:{law_tag}:rev-subject",
            semantic_hash({"fixture_id": f"{law_tag}-rev", "flavor": "TEST_ONLY_NONPARENT_WORK_CONTEXT"}),
        ),
        target_ref=source["qrefs"]["POSITION"],
        bindings=[binding_r],
        role_direction=ROLE_REVERSE,
        native_unit_ref=native_unit,
        analysis_unit_ref=analysis_unit,
        denominator_basis_ref=denominator_basis,
        operation_authority_ref=pairing,
        model_rule=model_rule,
        n9_tag=law_tag,
        projection={"kind": "TEST_ONLY_NONPARENT_WORK_CONTEXT_REVERSE", "scenario": "work_context"},
        role_reversal_authority_ref=make_role_reversal_authority(f"postastra-pe-{law_tag}"),
    )
    consumer_query_r = request_r.derived_positioned_query()
    witness_r = build_witness_for_binding(
        witness_object_id=f"urn:test:postastra-pe:{law_tag}:rev-witness",
        consumer_query=consumer_query_r,
        producer_query=producer_query_r,
        producer_predicate=predicate_r,
        bindings=[binding_r],
        coordinate_value_pairs=[(source["qrefs"]["ANSWER"], "yes")],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        leaf_type="SURVEY_RESPONSE_EVENT",
    )
    cases["nonparent_reverse"] = {
        "request": request_r,
        "model_rule": model_rule,
        "witness": witness_r,
        "predicate": predicate_r,
        "empirical_query": producer_query_r,
        "release_refs": (source["release_ref"],),
        "registry": registry,
        "repository": source["repo"],
        "expected": "reverse_single",
    }

    # ---- Consumer 3: test-only finite conception-scenario (multi) ----
    conditions_c = [
        ("RESPONSE", "POSITION", "P1"),
        ("RESPONSE", "COHORT", "B"),
    ]
    predicate_c = i03._predicate(
        source,
        query_auth,
        {
            "op": "AND",
            "children": [
                i03._response_leaf(source, query_auth, "POSITION", "P1"),
                i03._response_leaf(source, query_auth, "COHORT", "B"),
            ],
        },
        tag=f"postastra-pe-{law_tag}-conc",
    )
    producer_query_c = i03._query(
        source,
        query_auth,
        predicate_c,
        ("ANSWER",),
        risk="R",
        tag=f"postastra-pe-{law_tag}-conc",
    )
    component_c = dict(producer_query_c.target_arity_and_topology["components"][0])
    component_c["domain"] = ["no", "yes"]
    component_c["target_domain_replay_ref"] = i03._ref("TARGET_DOMAIN", "ANSWER-no-yes-c")
    producer_query_c = EmpiricalQuerySpec(
        typed_state=producer_query_c.typed_state,
        authority_snapshot_refs=producer_query_c.authority_snapshot_refs,
        dependency_refs=producer_query_c.dependency_refs,
        producer_replay_locator_or_reference_root=producer_query_c.producer_replay_locator_or_reference_root,
        target_refs=producer_query_c.target_refs,
        target_arity_and_topology={
            "arity": 1,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": [component_c],
        },
        condition_predicate_ref=producer_query_c.condition_predicate_ref,
        risk_set_ref=producer_query_c.risk_set_ref,
        empirical_universe_refs=producer_query_c.empirical_universe_refs,
        scope_refs=producer_query_c.scope_refs,
        measure_basis_ref=producer_query_c.measure_basis_ref,
        requested_output_grain=producer_query_c.requested_output_grain,
        query_authority_refs=producer_query_c.query_authority_refs,
    )
    bindings_c = []
    pairs_c = []
    for binding_id, (_kind, question, value) in zip(("position", "cohort"), conditions_c):
        bindings_c.append(
            make_conditioner_binding(
                binding_id=binding_id,
                subject_fact_ref=ExactRef(**subject_fact_ref(source, question, value)),
                empirical_coordinate_ref=source["qrefs"][question],
                comparability_authority_ref=pairing,
                source_universe_ref=source["universe"].ref,
                release_ref=source["release_ref"],
            )
        )
        pairs_c.append((source["qrefs"][question], value))
    request_c = _build_request(
        request_id=f"postastra-pe-{law_tag}-conception",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            f"urn:test:postastra-pe:{law_tag}:conc-subject",
            semantic_hash({"fixture_id": f"{law_tag}-conc", "flavor": "TEST_ONLY_FINITE_CONCEPTION_SCENARIO"}),
        ),
        target_ref=source["qrefs"]["ANSWER"],
        bindings=bindings_c,
        role_direction=ROLE_MULTI,
        native_unit_ref=native_unit,
        analysis_unit_ref=analysis_unit,
        denominator_basis_ref=denominator_basis,
        operation_authority_ref=pairing,
        model_rule=model_rule,
        n9_tag=law_tag,
        projection={
            "kind": "TEST_ONLY_FINITE_CONCEPTION_SCENARIO_QUERY",
            "scenario": "finite_conception_scenario_set",
            "note": "TEST_ONLY_CONSUMER_LABEL__NO_PARENT_NOUN_UPSTREAM",
        },
    )
    consumer_query_c = request_c.derived_positioned_query()
    witness_c = build_witness_for_binding(
        witness_object_id=f"urn:test:postastra-pe:{law_tag}:conc-witness",
        consumer_query=consumer_query_c,
        producer_query=producer_query_c,
        producer_predicate=predicate_c,
        bindings=bindings_c,
        coordinate_value_pairs=pairs_c,
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        leaf_type="SURVEY_RESPONSE_EVENT",
    )
    cases["conception_scenario"] = {
        "request": request_c,
        "model_rule": model_rule,
        "witness": witness_c,
        "predicate": predicate_c,
        "empirical_query": producer_query_c,
        "release_refs": (source["release_ref"],),
        "registry": registry,
        "repository": source["repo"],
        "expected": "multi_binding_alt",
    }

    # Frozen exact arithmetic for this law (computed here, not from service).
    cases["_arithmetic"] = _independent_arithmetic(law_rows)
    return cases


def _build_request(
    *,
    request_id: str,
    subject_ref: ExactRef,
    target_ref: ExactRef,
    bindings: list,
    role_direction: str,
    native_unit_ref: ExactRef,
    analysis_unit_ref: ExactRef,
    denominator_basis_ref: ExactRef,
    operation_authority_ref: AuthorityRef,
    model_rule: PositionedSubjectPossibilityModelRule,
    n9_tag: str,
    projection: dict,
    role_reversal_authority_ref: AuthorityRef | None = None,
    snapshot_state: str = N9_TEST_SNAPSHOT_STATE,
    asof_time: str = "2021-06-30",
    request_time: str = REQUEST_TIME,
):
    from rawlsing_next.pre553_postastra_pe_generic_world_possibility import (
        GenericWorldSituatedRequest,
    )

    return GenericWorldSituatedRequest(
        request_id=request_id,
        subject_ref=subject_ref,
        target_ref=target_ref,
        conditioner_bindings=tuple(bindings),
        role_direction=role_direction,
        native_unit_ref=native_unit_ref,
        analysis_unit_ref=analysis_unit_ref,
        denominator_basis_ref=denominator_basis_ref,
        operation_authority_ref=operation_authority_ref,
        model_use_ref=model_rule.model_authority_ref,
        n9_world=make_n9_world_dependency(
            tag=n9_tag, snapshot_state=snapshot_state, asof_time=asof_time, request_time=request_time
        ),
        request_time=request_time,
        role_reversal_authority_ref=role_reversal_authority_ref,
        requested_projection=projection,
    )


def law_a_cases() -> dict[str, dict[str, Any]]:
    return build_three_consumer_cases(law_rows=law_a_rows(), law_tag="law-a")


def law_b_cases() -> dict[str, dict[str, Any]]:
    return build_three_consumer_cases(law_rows=law_b_rows(), law_tag="law-b")


__all__ = [
    "LAW_A_ID",
    "LAW_A_ORACLE",
    "LAW_B_ID",
    "LAW_B_ORACLE",
    "LAW_B_EXTRA_ROWS",
    "REQUEST_TIME",
    "NATIVE_UNIT",
    "law_a_rows",
    "law_b_rows",
    "make_n9_world_dependency",
    "make_unit_refs",
    "make_role_reversal_authority",
    "build_three_consumer_cases",
    "law_a_cases",
    "law_b_cases",
    "_independent_arithmetic",
]
