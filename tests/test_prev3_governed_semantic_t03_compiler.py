from __future__ import annotations

import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next._prev3_structural_batch_base import CandidateKind, CandidateOutcome
from rawlsing_next.prev3_governed_semantic_t03_compiler import (
    CarrierKind,
    CurrentnessBlockedError,
    CurrentnessState,
    EpistemicClass,
    EquivalenceAuthority,
    EquivalenceDecision,
    FixtureSchemaError,
    GovernedSemanticCapitalRecord,
    SemanticAuthorityState,
    SemanticJurisdiction,
    FINAL_RELEASE_HOLD,
    adapt_fqra_fixture,
    adapt_negative_block_fixture,
    adapt_qsmv2_fixture,
    adapt_response_semantics_fixture,
    adapt_typed_relation_fixture,
    compile_governed_semantic_batch,
    compile_governed_semantic_capital,
)


def h(value):
    return semantic_hash({"fixture": value})


def r(kind, object_id):
    return ExactRef(kind, object_id, h(f"{kind}:{object_id}"))


def a(name="AUTH", version="R1"):
    return AuthorityRef(name, version, h(f"{name}:{version}"))


def eq(decision=EquivalenceDecision.AUTHORIZED, tag="eq"):
    return EquivalenceAuthority(
        r("REL", tag),
        decision,
        r("REL_DECISION", f"{tag}:{decision.value}"),
        a("EQAUTH"),
    )


def rec(
    *,
    carrier=CarrierKind.FQRA,
    state=SemanticAuthorityState.POSITIVE,
    current=CurrentnessState.CURRENT,
    core=None,
    jur=SemanticJurisdiction.SOURCE_SEMANTIC,
    epi=EpistemicClass.MANUAL_ADJUDICATED,
    tag="x",
    equivs=(),
):
    return GovernedSemanticCapitalRecord(
        carrier_kind=carrier,
        carrier_locator_ref=r("CARRIER", carrier.value),
        carrier_row_ref=r("ROW", tag),
        source_family_ref=r("FAMILY", "fam"),
        source_release_ref=r("RELEASE", "rel"),
        source_question_ref=r("QUESTION", f"q-{tag}"),
        implementation_ref_or_exact_na=r("IMPL", f"i-{tag}"),
        authority_ref=a(f"AUTH-{tag}"),
        authority_snapshot_ref=r("AUTH_SNAPSHOT", tag),
        epistemic_class=epi,
        jurisdiction=jur,
        authority_state=state,
        currentness_state=current,
        currentness_ref=(
            None
            if current is CurrentnessState.MISSING
            else r("CURRENTNESS", f"{tag}:{current.value}")
        ),
        noncurrent_disposition_ref=(
            r("NONCURRENT", tag)
            if current is CurrentnessState.HISTORICAL_NONCURRENT
            else None
        ),
        response_category_semantics_ref=r("RESPONSE", tag),
        routing_applicability_ref=r("ROUTING", tag),
        structural_use_ceiling_ref=r("CEILING", tag),
        semantic_core_ref=core or r("CORE", tag),
        semantic_schema_ref=r("SCHEMA", "s1"),
        negative_ceiling_ref=r("NEG_CEILING", "n1"),
        type_class_ceiling_ref=r("TYPE_CEILING", "t1"),
        evidence_admission_refs=(r("EVIDENCE", tag),),
        provenance_refs=(r("PROVENANCE", tag),),
        equivalence_authorities=tuple(equivs),
        candidate_kind=CandidateKind.STRUCTURAL_POSITION,
    )


def align_reduction_semantics(target, source):
    """Keep source identity distinct while making compiler-local reduction fields equal."""
    object.__setattr__(
        target,
        "response_category_semantics_ref",
        source.response_category_semantics_ref,
    )
    object.__setattr__(target, "routing_applicability_ref", source.routing_applicability_ref)
    object.__setattr__(target, "structural_use_ceiling_ref", source.structural_use_ceiling_ref)
    return target


def fixture_material(record):
    return {
        "carrier_locator_ref": record.carrier_locator_ref.as_dict(),
        "carrier_row_ref": record.carrier_row_ref.as_dict(),
        "source_family_ref": record.source_family_ref.as_dict(),
        "source_release_ref": record.source_release_ref.as_dict(),
        "source_question_ref": record.source_question_ref.as_dict(),
        "implementation_ref_or_exact_na": record.implementation_ref_or_exact_na.as_dict(),
        "authority_ref": record.authority_ref.as_dict(),
        "authority_snapshot_ref": record.authority_snapshot_ref.as_dict(),
        "epistemic_class": record.epistemic_class.value,
        "jurisdiction": record.jurisdiction.value,
        "authority_state": record.authority_state.value,
        "currentness_state": record.currentness_state.value,
        "currentness_ref": (
            None if record.currentness_ref is None else record.currentness_ref.as_dict()
        ),
        "noncurrent_disposition_ref": (
            None
            if record.noncurrent_disposition_ref is None
            else record.noncurrent_disposition_ref.as_dict()
        ),
        "response_category_semantics_ref": record.response_category_semantics_ref.as_dict(),
        "routing_applicability_ref": record.routing_applicability_ref.as_dict(),
        "structural_use_ceiling_ref": record.structural_use_ceiling_ref.as_dict(),
        "semantic_core_ref": record.semantic_core_ref.as_dict(),
        "semantic_schema_ref": record.semantic_schema_ref.as_dict(),
        "negative_ceiling_ref": record.negative_ceiling_ref.as_dict(),
        "type_class_ceiling_ref": record.type_class_ceiling_ref.as_dict(),
        "evidence_admission_refs": [
            item.as_dict() for item in record.evidence_admission_refs
        ],
        "provenance_refs": [item.as_dict() for item in record.provenance_refs],
        "equivalence_authorities": [
            {
                "relation_ref": item.relation_ref.as_dict(),
                "decision": item.decision.value,
                "decision_ref": item.decision_ref.as_dict(),
                "authority_ref": item.authority_ref.as_dict(),
            }
            for item in record.equivalence_authorities
        ],
        "candidate_kind": record.candidate_kind.value,
    }


@pytest.mark.parametrize(
    "adapter,kind",
    [
        (adapt_fqra_fixture, CarrierKind.FQRA),
        (adapt_qsmv2_fixture, CarrierKind.QSMV2),
        (adapt_negative_block_fixture, CarrierKind.NEGATIVE_BLOCK),
        (adapt_response_semantics_fixture, CarrierKind.RESPONSE_SEMANTICS),
        (adapt_typed_relation_fixture, CarrierKind.TYPED_RELATION),
    ],
)
def test_five_bounded_carrier_adapters_preserve_exact_material(adapter, kind):
    original = rec(carrier=kind, tag=kind.value)
    adapted = adapter(fixture_material(original))
    assert adapted.carrier_kind is kind
    assert adapted.authority_ref == original.authority_ref
    assert adapted.semantic_core_ref == original.semantic_core_ref
    assert adapted.response_category_semantics_ref == original.response_category_semantics_ref
    assert adapted.routing_applicability_ref == original.routing_applicability_ref
    assert adapted.structural_use_ceiling_ref == original.structural_use_ceiling_ref


@pytest.mark.parametrize(
    "state,outcome",
    [
        (SemanticAuthorityState.POSITIVE, CandidateOutcome.CANDIDATE_ONLY),
        (SemanticAuthorityState.NEGATIVE_FORBIDDEN, CandidateOutcome.CANDIDATE_ONLY),
        (SemanticAuthorityState.BLOCKED, CandidateOutcome.BLOCKED),
        (SemanticAuthorityState.REVIEW_REQUIRED, CandidateOutcome.BLOCKED),
    ],
)
def test_authority_states_conserved_without_laundering(state, outcome):
    out = compile_governed_semantic_capital(rec(state=state, tag=state.value))
    assert out.authority_state is state
    assert out.status.outcome is outcome
    assert (out.blocker is not None) is (outcome is CandidateOutcome.BLOCKED)


def test_superseded_is_historical_noncurrent_not_current():
    out = compile_governed_semantic_capital(
        rec(
            state=SemanticAuthorityState.SUPERSEDED,
            current=CurrentnessState.HISTORICAL_NONCURRENT,
            tag="old",
        )
    )
    assert out.authority_state is SemanticAuthorityState.SUPERSEDED
    assert out.currentness_state is CurrentnessState.HISTORICAL_NONCURRENT
    assert out.status.outcome is CandidateOutcome.HISTORICAL_NONCURRENT
    assert out.status.noncurrent_disposition_refs


@pytest.mark.parametrize("jur", list(SemanticJurisdiction))
def test_jurisdiction_conserved(jur):
    assert compile_governed_semantic_capital(rec(jur=jur, tag=jur.value)).jurisdiction is jur


@pytest.mark.parametrize("epi", list(EpistemicClass))
def test_epistemic_class_conserved(epi):
    assert compile_governed_semantic_capital(rec(epi=epi, tag=epi.value)).epistemic_class is epi


def test_exact_provenance_authority_response_routing_and_ceiling_retained():
    record = rec(tag="prov")
    out = compile_governed_semantic_capital(record)
    pkeys = {item.key for item in out.semantic_candidate.provenance_refs}
    assert record.provenance_refs[0].key in pkeys
    assert record.carrier_locator_ref.key in pkeys
    assert record.carrier_row_ref.key in pkeys
    assert record.authority_snapshot_ref.key in pkeys
    assert record.source_family_ref.key in pkeys
    assert record.source_release_ref.key in pkeys
    assert record.source_question_ref.key in pkeys
    assert record.implementation_ref_or_exact_na.key in pkeys
    assert out.authority_ref == record.authority_ref
    assert out.response_category_semantics_ref == record.response_category_semantics_ref
    assert out.routing_applicability_ref == record.routing_applicability_ref
    assert out.structural_use_ceiling_ref == record.structural_use_ceiling_ref


def test_only_positive_equivalence_enters_admission_but_all_decisions_remain_provenance():
    allow = eq(EquivalenceDecision.AUTHORIZED, "allow")
    deny = eq(EquivalenceDecision.DENIED, "deny")
    unknown = eq(EquivalenceDecision.UNKNOWN_AUTHORITY, "unknown")
    out = compile_governed_semantic_capital(
        rec(tag="eqs", equivs=(allow, deny, unknown))
    )
    ekeys = {item.key for item in out.semantic_candidate.evidence_admission_refs}
    pkeys = {item.key for item in out.semantic_candidate.provenance_refs}
    assert allow.relation_ref.key in ekeys
    assert deny.relation_ref.key not in ekeys
    assert unknown.relation_ref.key not in ekeys
    for item in (allow, deny, unknown):
        assert item.relation_ref.key in pkeys
        assert item.decision_ref.key in pkeys
    assert out.positive_equivalence_refs == (allow.relation_ref,)


def test_exact_equal_core_dedup_retains_all_candidate_evidence_and_provenance():
    core = r("CORE", "shared")
    one = rec(core=core, tag="one")
    two = align_reduction_semantics(rec(core=core, tag="two"), one)
    batch = compile_governed_semantic_batch((one, two))
    assert batch.final_release_hold == FINAL_RELEASE_HOLD
    assert len(batch.reduction_groups) == 1
    assert len(batch.reduction.aggregates) == 1
    aggregate = batch.reduction.aggregates[0]
    ekeys = {item.key for item in aggregate.evidence_admission_refs}
    pkeys = {item.key for item in aggregate.provenance_refs}
    assert len(aggregate.candidate_refs) == 2
    assert one.evidence_admission_refs[0].key in ekeys
    assert two.evidence_admission_refs[0].key in ekeys
    assert one.provenance_refs[0].key in pkeys
    assert two.provenance_refs[0].key in pkeys


def test_deterministic_replay_and_order_independent_batch_reduction():
    core = r("CORE", "shared-replay")
    one = rec(core=core, tag="r1")
    two = align_reduction_semantics(rec(core=core, tag="r2"), one)
    first = compile_governed_semantic_capital(one)
    replay = compile_governed_semantic_capital(one)
    assert first.ref == replay.ref
    assert first.semantic_candidate.ref == replay.semantic_candidate.ref
    assert first.source_local_intake.ref == replay.source_local_intake.ref
    batch_one = compile_governed_semantic_batch((one, two))
    batch_two = compile_governed_semantic_batch((two, one))
    assert [item.ref for item in batch_one.reduction.aggregates] == [
        item.ref for item in batch_two.reduction.aggregates
    ]
    assert [group.key for group in batch_one.reduction_groups] == [
        group.key for group in batch_two.reduction_groups
    ]


@pytest.mark.parametrize(
    "field",
    [
        "authority_state",
        "jurisdiction",
        "epistemic_class",
        "response_category_semantics_ref",
        "routing_applicability_ref",
        "structural_use_ceiling_ref",
    ],
)
def test_dedup_never_collapses_distinct_governed_dimensions(field):
    core = r("CORE", f"partition-{field}")
    one = rec(core=core, tag=f"{field}-a")
    two = align_reduction_semantics(rec(core=core, tag=f"{field}-b"), one)
    if field == "authority_state":
        object.__setattr__(two, field, SemanticAuthorityState.NEGATIVE_FORBIDDEN)
    elif field == "jurisdiction":
        object.__setattr__(two, field, SemanticJurisdiction.RAWLSING_SEMANTIC)
    elif field == "epistemic_class":
        object.__setattr__(two, field, EpistemicClass.DETERMINISTIC_DERIVATION)
    else:
        object.__setattr__(two, field, r("DISTINCT_GOVERNED_FIELD", field))
    batch = compile_governed_semantic_batch((one, two))
    assert len(batch.reduction_groups) == 2
    assert len(batch.reduction.aggregates) == 2


def test_current_and_historical_noncurrent_never_dedup():
    core = r("CORE", "currentness-partition")
    current = rec(core=core, tag="cur")
    historical = align_reduction_semantics(
        rec(core=core, tag="hist", current=CurrentnessState.HISTORICAL_NONCURRENT),
        current,
    )
    batch = compile_governed_semantic_batch((current, historical))
    assert len(batch.reduction_groups) == 2
    assert len(batch.reduction.aggregates) == 2


def test_same_logical_candidate_conflict_is_quarantined_before_partitioning():
    core = r("CORE", "same-logical")
    positive = rec(core=core, tag="logical")
    negative = rec(
        core=core,
        tag="logical",
        state=SemanticAuthorityState.NEGATIVE_FORBIDDEN,
    )
    batch = compile_governed_semantic_batch((positive, negative))
    assert not batch.reduction.aggregates
    assert len(batch.reduction.quarantines) == 2


@pytest.mark.parametrize(
    "currentness",
    [CurrentnessState.MISSING, CurrentnessState.AMBIGUOUS],
)
def test_missing_or_ambiguous_currentness_fails_closed(currentness):
    record = rec(current=currentness, tag=currentness.value)
    if currentness is CurrentnessState.AMBIGUOUS:
        object.__setattr__(record, "currentness_ref", r("CURRENTNESS", "ambiguous"))
    with pytest.raises(CurrentnessBlockedError):
        compile_governed_semantic_capital(record)


def test_missing_currentness_ref_fails_closed_even_when_state_says_current():
    record = rec(tag="no-ref")
    object.__setattr__(record, "currentness_ref", None)
    with pytest.raises(CurrentnessBlockedError):
        compile_governed_semantic_capital(record)


def test_superseded_current_contradiction_fails_closed():
    with pytest.raises(CurrentnessBlockedError):
        compile_governed_semantic_capital(
            rec(
                state=SemanticAuthorityState.SUPERSEDED,
                current=CurrentnessState.CURRENT,
                tag="bad",
            )
        )


def test_historical_without_noncurrent_disposition_fails_closed():
    record = rec(current=CurrentnessState.HISTORICAL_NONCURRENT, tag="missing-disp")
    object.__setattr__(record, "noncurrent_disposition_ref", None)
    with pytest.raises(CurrentnessBlockedError):
        compile_governed_semantic_capital(record)


def test_fixture_adapter_rejects_free_text_or_inferred_semantics_fields():
    material = fixture_material(rec(tag="strict"))
    material["question_text"] = "infer me"
    material.pop("semantic_core_ref")
    with pytest.raises(FixtureSchemaError) as exc:
        adapt_fqra_fixture(material)
    assert "semantic_core_ref" in str(exc.value)
    assert "question_text" in str(exc.value)


def test_negative_forbidden_remains_negative_state_and_not_empirical_negative():
    record = rec(state=SemanticAuthorityState.NEGATIVE_FORBIDDEN, tag="neg")
    out = compile_governed_semantic_capital(record)
    assert out.authority_state is SemanticAuthorityState.NEGATIVE_FORBIDDEN
    assert out.semantic_candidate.negative_ceiling_ref == record.negative_ceiling_ref
    assert out.status.outcome is CandidateOutcome.CANDIDATE_ONLY


def test_compiler_never_emits_current_t03_outcome():
    out = compile_governed_semantic_capital(rec(tag="not-selector"))
    assert out.status.outcome is CandidateOutcome.CANDIDATE_ONLY
    assert out.status.current_selection_refs
    assert out.status.outcome is not CandidateOutcome.CURRENT
