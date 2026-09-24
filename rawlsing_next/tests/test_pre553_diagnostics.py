from decimal import Decimal

import pytest

from rawlsing_next.pre553_diagnostics import (
    Pre553DiagnosticAuthorityLeakError,
    Pre553DiagnosticError,
    assert_diagnostic_only_use,
    produce_governed_diagnostics,
    replay_governed_diagnostics,
)
from rawlsing_next.pre553_discovery_exact import ExactBoundedCoverageError
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry, Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact,
    Pre553SemanticCollapseError,
)
from rawlsing_next.pre553_structural_admission import (
    StructuralAdmissionError,
    evaluate_structural_empirical_admission,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom,
    _d_auth,
    _discovery_authority,
    _execute,
    _grammar,
    _qt,
    _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _build_source,
    _query,
    _query_authority,
    _ref,
    _registry,
    _run,
)


def _joint_fixture(tag="i01-diagnostics"):
    source = _build_source(tag, [
        {"id": "R00a", "responses": {"X": 0, "Y": 0}},
        {"id": "R00b", "responses": {"X": 0, "Y": 0}},
        {"id": "R11a", "responses": {"X": 1, "Y": 1}},
        {"id": "R11b", "responses": {"X": 1, "Y": 1}},
    ])
    qauth = _query_authority(tag)
    predicate = _branch_predicate(source, qauth, tag="all")
    query = _query(source, qauth, predicate, ("X", "Y"), tag="joint")
    registry = _registry(source, qauth)
    fact = _run(source, qauth, predicate, query, registry=registry).facts[0]
    return source, qauth, predicate, query, registry, fact


def _negative_clone(fact, state):
    fields = dict(fact.semantic_fields)
    topology = dict(fact.target_topology)
    topology["complete_cell_semantic_projection"] = [
        {
            **dict(row),
            "cell_state": "ZERO_SUPPORT",
            "raw_numerator_support": 0,
            "weighted_numerator_support_if_authorized": None,
        }
        for row in fact.target_topology["complete_cell_semantic_projection"]
    ]
    replay = _ref("PRE553_I03_QUERY_REPLAY", f"i01-negative-{state}")
    fields.update({
        "target_topology": topology,
        "raw_numerator_support": 0,
        "raw_denominator_support": 0,
        "weighted_numerator_support_if_authorized": None,
        "weighted_denominator_support_if_authorized": None,
        "replay_ref": replay,
        "raw_resolved_target_support": 0,
        "execution_detail": f"hostile typed state fixture: {state}",
    })
    dependencies = tuple(
        ref for ref in fact.dependency_refs if ref.kind != "PRE553_I03_QUERY_REPLAY"
    ) + (replay,)
    return EmpiricalFact(
        typed_state=state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=dependencies,
        producer_replay_locator_or_reference_root=replay,
        **fields,
    )


def _product(**overrides):
    source, qauth, predicate, query, registry, fact = _joint_fixture()
    kwargs = {
        "fact": fact,
        "query": query,
        "authority_registry": registry,
        "release_refs": (source["release_ref"],),
    }
    kwargs.update(overrides)
    return source, qauth, predicate, query, registry, fact, produce_governed_diagnostics(**kwargs)


def test_exact_f012_metrics_are_computed_from_governed_joint_fact_only():
    source, _qauth, _predicate, query, registry, fact, product = _product()

    assert product.typed_state == "SUPPORTED"
    assert product.source_fact_ref == fact.ref
    assert product.source_query_ref == query.ref
    assert product.source_release_refs == (source["release_ref"],)
    assert product.ref.kind == "PRE553_DIAGNOSTIC_PRODUCT"
    assert product.ref.kind != "EmpiricalFact@1.0.0"

    for metric_name in (
        "entropy_reduction",
        "mutual_information",
        "normalized_mutual_information",
        "cramers_v",
    ):
        assert abs(Decimal(product.metrics[metric_name]) - Decimal("1")) < Decimal("1e-40")

    cells = {tuple(row["cell"]): row for row in product.metrics["uplift_lift"]}
    assert tuple(cells[("0", "0")]["uplift"]["$exact_fraction"]) == (1, 2)
    assert tuple(cells[("0", "0")]["lift"]["$exact_fraction"]) == (2, 1)
    assert tuple(cells[("0", "1")]["uplift"]["$exact_fraction"]) == (-1, 2)
    assert tuple(cells[("0", "1")]["lift"]["$exact_fraction"]) == (0, 1)

    assert product.metrics["joint_confidence"] is None
    assert product.metric_states["JOINT_CONFIDENCE"] == "UNCERTAINTY_UNQUANTIFIED"
    assert product.diagnostic_only is True
    assert product.empirical_truth_effect is False
    assert product.frontier_control_effect is False
    assert product.structural_authority_effect is False
    assert product.semantic_interpretation_effect is False
    with pytest.raises(TypeError):
        product.metrics["mutual_information"] = "0"

    replayed = replay_governed_diagnostics(
        product,
        fact=fact,
        query=query,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
    )
    assert replayed.ref == product.ref
    assert replayed.replay_ref == product.replay_ref


def test_f018_joint_confidence_is_explicit_diagnostic_and_identity_bound():
    source, _qauth, _predicate, query, registry, fact = _joint_fixture("i01-confidence")
    determinant = _ref("F018_CONFIDENCE_DETERMINANT", "exact-components")
    components = {
        "focus_cell": ["0", "0"],
        "support_ratio": "2",
        "completion_rate": "4/5",
        "effective_n_ratio": "3/4",
        "pattern_probability": "1/2",
    }
    with_confidence = produce_governed_diagnostics(
        fact=fact,
        query=query,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        joint_confidence_components=components,
        joint_confidence_determinant_refs=(determinant,),
    )
    without_confidence = produce_governed_diagnostics(
        fact=fact,
        query=query,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
    )
    with pytest.raises(Pre553DiagnosticError, match="requires exact determinant refs"):
        produce_governed_diagnostics(
            fact=fact,
            query=query,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            joint_confidence_components=components,
        )

    assert with_confidence.metrics["joint_confidence"]["score_0_100"] == "76.25"
    assert with_confidence.metrics["joint_confidence"]["determinant_refs"] == (
        determinant.as_dict(),
    )
    assert with_confidence.metric_states["JOINT_CONFIDENCE"] == "AVAILABLE_DIAGNOSTIC_ONLY"
    assert with_confidence.ref != without_confidence.ref
    assert with_confidence.replay_ref != without_confidence.replay_ref

    changed = {**components, "pattern_probability": "1/4"}
    with pytest.raises(Pre553DiagnosticError, match="replay identity mismatch"):
        replay_governed_diagnostics(
            with_confidence,
            fact=fact,
            query=query,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            joint_confidence_components=changed,
            joint_confidence_determinant_refs=(determinant,),
        )


@pytest.mark.parametrize(
    "state",
    ["NONCOMPARABLE", "UNAVAILABLE", "UNRESOLVED", "INTEGRITY_FAILURE", "VALID_EMPTY"],
)
def test_typed_negative_i03_states_are_preserved_and_never_coerced_to_scores(state):
    source, _qauth, _predicate, query, registry, fact = _joint_fixture(f"i01-negative-{state.lower()}")
    negative = _negative_clone(fact, state)
    product = produce_governed_diagnostics(
        fact=negative,
        query=query,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
    )
    assert product.typed_state == state
    assert set(product.metric_states.values()) == {state}
    assert product.metrics["entropy_reduction"] is None
    assert product.metrics["mutual_information"] is None
    assert product.metrics["normalized_mutual_information"] is None
    assert product.metrics["cramers_v"] is None
    assert product.metrics["uplift_lift"] is None
    assert product.metrics["joint_confidence"] is None


def test_underpowered_state_requires_exact_determinant_and_preserves_diagnostic_values():
    source, _qauth, _predicate, query, registry, fact = _joint_fixture("i01-underpowered")
    support_ref = _ref("GOVERNED_SUPPORT_DETERMINANT", "underpowered")

    with pytest.raises(Pre553DiagnosticError, match="UNDERPOWERED requires exact support determinant"):
        produce_governed_diagnostics(
            fact=fact,
            query=query,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            support_state="UNDERPOWERED",
        )

    product = produce_governed_diagnostics(
        fact=fact,
        query=query,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        support_state="UNDERPOWERED",
        support_determinant_refs=(support_ref,),
    )
    assert product.typed_state == "UNDERPOWERED"
    assert product.metric_states["MUTUAL_INFORMATION"] == "AVAILABLE_UNDERPOWERED_DIAGNOSTIC_ONLY"
    assert abs(Decimal(product.metrics["mutual_information"]) - Decimal("1")) < Decimal("1e-40")
    assert tuple(product.source_replay_determinants["support_determinant_refs"]) == (
        support_ref.as_dict(),
    )


def test_uncertainty_unquantified_preserves_state_but_not_point_diagnostic_loss():
    source, _qauth, _predicate, query, registry, fact = _joint_fixture("i01-uncertainty")
    uncertain = EmpiricalFact(
        typed_state="UNCERTAINTY_UNQUANTIFIED",
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **dict(fact.semantic_fields),
    )
    product = produce_governed_diagnostics(
        fact=uncertain,
        query=query,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
    )
    assert product.typed_state == "UNCERTAINTY_UNQUANTIFIED"
    assert product.metric_states["MUTUAL_INFORMATION"] == "AVAILABLE_DIAGNOSTIC_ONLY"
    assert product.metric_states["JOINT_CONFIDENCE"] == "UNCERTAINTY_UNQUANTIFIED"
    assert abs(Decimal(product.metrics["mutual_information"]) - Decimal("1")) < Decimal("1e-40")
    assert product.metrics["joint_confidence"] is None


def test_missing_exact_authority_and_fact_query_mismatch_fail_closed():
    source, qauth, predicate, query, _registry_obj, fact = _joint_fixture("i01-authority")
    registry_missing_query_authority = AuthorityRegistry(source["authorities"])
    with pytest.raises(Pre553AuthorityError):
        produce_governed_diagnostics(
            fact=fact,
            query=query,
            authority_registry=registry_missing_query_authority,
            release_refs=(source["release_ref"],),
        )

    other_query = _query(source, qauth, predicate, ("X", "Y"), tag="other-exact-query")
    with pytest.raises(Pre553DiagnosticError, match="fact/query exact identity mismatch"):
        produce_governed_diagnostics(
            fact=fact,
            query=other_query,
            authority_registry=_registry(source, qauth),
            release_refs=(source["release_ref"],),
        )


def test_positive_unary_fact_is_typed_not_applicable_not_zero_association():
    source = _build_source("i01-unary", [
        {"id": "R1", "responses": {"Y": 0}},
        {"id": "R2", "responses": {"Y": 1}},
    ])
    qauth = _query_authority("i01-unary")
    predicate = _branch_predicate(source, qauth, tag="all")
    query = _query(source, qauth, predicate, ("Y",), tag="unary")
    registry = _registry(source, qauth)
    fact = _run(source, qauth, predicate, query, registry=registry).facts[0]

    product = produce_governed_diagnostics(
        fact=fact,
        query=query,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
    )
    assert product.typed_state == "NOT_APPLICABLE"
    assert set(product.metric_states.values()) == {"NOT_APPLICABLE"}
    for metric_name in (
        "entropy_reduction",
        "mutual_information",
        "normalized_mutual_information",
        "cramers_v",
        "uplift_lift",
        "joint_confidence",
    ):
        assert product.metrics[metric_name] is None


def test_malformed_positive_joint_projection_fails_closed():
    source, _qauth, _predicate, query, registry, fact = _joint_fixture("i01-malformed")
    fields = dict(fact.semantic_fields)
    topology = dict(fact.target_topology)
    rows = [dict(row) for row in topology["complete_cell_semantic_projection"]]
    rows.append(dict(rows[0]))
    topology["complete_cell_semantic_projection"] = rows
    fields["target_topology"] = topology
    malformed = EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **fields,
    )
    with pytest.raises(Pre553DiagnosticError, match="duplicate joint cell"):
        produce_governed_diagnostics(
            fact=malformed,
            query=query,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
        )


def test_exact_release_provenance_is_required_and_no_fallback_is_permitted():
    _source, _qauth, _predicate, query, registry, fact = _joint_fixture("i01-release")
    wrong_release = _ref("C11_SOURCE_RELEASE", "not-in-i03-provenance")
    with pytest.raises(Pre553DiagnosticError, match="not present in exact I03 provenance"):
        produce_governed_diagnostics(
            fact=fact,
            query=query,
            authority_registry=registry,
            release_refs=(wrong_release,),
        )


def test_diagnostic_product_cannot_masquerade_as_i03_empirical_truth():
    _source, _qauth, _predicate, _query_obj, _registry_obj, fact, product = _product()
    assert product.ref.kind != fact.ref.kind

    with pytest.raises(Pre553SemanticCollapseError, match="diagnostic score cannot masquerade"):
        EmpiricalFact(
            typed_state=fact.typed_state,
            authority_snapshot_refs=fact.authority_snapshot_refs,
            dependency_refs=fact.dependency_refs,
            producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
            **dict(fact.semantic_fields),
            diagnostic_kind="NMI",
        )

    with pytest.raises(Pre553DiagnosticAuthorityLeakError):
        assert_diagnostic_only_use(product, purpose="I03_TRUTH")


@pytest.mark.parametrize(
    "purpose",
    [
        "I05_FRONTIER_MEMBERSHIP",
        "STRUCTURAL_AUTHORITY",
        "STRUCTURAL_ADMISSION",
        "SEMANTIC_INTERPRETATION",
        "SOURCE_SEMANTICS",
    ],
)
def test_hostile_authority_roles_are_rejected(purpose):
    *_context, product = _product()
    with pytest.raises(Pre553DiagnosticAuthorityLeakError):
        assert_diagnostic_only_use(product, purpose=purpose)

    assert assert_diagnostic_only_use(product, purpose="REPORTING") is product
    assert assert_diagnostic_only_use(product, purpose="RANKING_NONCONTROLLING") is product


def test_actual_structural_admission_owner_rejects_diagnostic_product_as_fact():
    _source, qauth, _predicate, query, registry, _fact, product = _product()
    with pytest.raises(
        StructuralAdmissionError,
        match="I04 requires exact I01 EmpiricalQuerySpec and EmpiricalFact objects",
    ):
        evaluate_structural_empirical_admission(
            query=query,
            fact=product,
            requested_admission_authority_ref=qauth.authority_ref,
            rule=None,
            request=None,
            authority_registry=registry,
            producer_replay_locator_or_reference_root=_ref(
                "REPLAY_ROOT", "i01-hostile-structural"
            ),
        )


def test_actual_i05_frontier_cannot_be_controlled_by_computed_diagnostic_score():
    source, qauth, predicate, query, _registry_obj, _fact, product = _product()
    dauth = _d_auth("i01-frontier")
    grammar = _grammar(
        operation="I03-OP-i01-frontier",
        atoms=[_atom("ALL", predicate, "BRANCH")],
        templates=[_qt("XY", query)],
        rules=[_rule(
            "joint-cell",
            "BOUNDED_K_WAY_RESPONSE_CONFIGURATION",
            "BASE_QUERY",
            baseline_atom_id="ALL",
            query_template_id="XY",
            target_cells=(("0", "0"),),
            validation={"kind": "TARGET_CELL_SUPPORTED"},
        )],
    )
    authority = _discovery_authority(
        source,
        grammar,
        dauth,
        ranking={
            "kind": "NMI",
            "diagnostic_product_ref": product.ref.as_dict(),
            "score": product.metrics["normalized_mutual_information"],
            "controls_frontier": True,
        },
    )
    with pytest.raises(ExactBoundedCoverageError, match="may not control exact frontier"):
        _execute(
            source,
            qauth,
            dauth,
            grammar,
            (predicate,),
            (query,),
            authority=authority,
        )

    with pytest.raises(Pre553DiagnosticAuthorityLeakError):
        assert_diagnostic_only_use(
            product,
            purpose="RANKING_NONCONTROLLING",
            controls_frontier=True,
        )
