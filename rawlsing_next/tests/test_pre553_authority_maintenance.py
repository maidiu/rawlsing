from __future__ import annotations

import hashlib

import pytest

from rawlsing_next.pre553_authority_maintenance import (
    AuthorityAdjudicationReceipt,
    AuthorityCandidate,
    AuthorityEvidenceReceipt,
    AuthorityMaintenanceConflict,
    AuthorityMaintenanceError,
    AuthorityMaintenanceExecutor,
    SemanticDeterminantGraph,
)
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef


def _h(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"{kind}:{tag}", _h(f"{kind}:{tag}"))


def _other_authority(tag: str = "other") -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", "1.0.0", _h(f"authority:{tag}:1.0.0"))


def _evidence(tag: str = "base", *, source: ExactRef | None = None) -> AuthorityEvidenceReceipt:
    return AuthorityEvidenceReceipt(
        evidence_role="SEMANTIC_AUTHORITY_EVIDENCE",
        evidence_refs=(_ref("EVIDENCE", tag),),
        provenance_refs=(_ref("PROVENANCE", tag),),
        source_release_refs=() if source is None else (source,),
    )


def _candidate(
    evidence_ref: ExactRef,
    *,
    version: str = "1.0.0",
    semantics: str = "v1",
    authority_id: str = "AUTH-Z06-TEST",
    parent_refs: tuple[AuthorityRef, ...] = (),
    supersession_refs: tuple[AuthorityRef, ...] = (),
    correction_kind: str = "NONE",
    correction_target_refs: tuple[AuthorityRef, ...] = (),
    correction_scope_ref: ExactRef | None = None,
    source_refs: tuple[ExactRef, ...] = (),
    candidate_id: str | None = None,
) -> AuthorityCandidate:
    return AuthorityCandidate(
        candidate_id=candidate_id or f"CAND-{authority_id}-{version}-{semantics}",
        candidate_revision=1,
        authority_id=authority_id,
        authority_version=version,
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        proposed_decision_state="ALLOW",
        governed_operations=("INTERPRET_SOURCE_SEMANTICS",),
        governed_object_families=("EmpiricalUniverse@1.0.0",),
        scope_envelope={
            "source_universe_refs": (_ref("EMPIRICAL_UNIVERSE", "U1"),),
            "target_use_refs": ("SOURCE_INTERPRETATION",),
        },
        effective_time_or_interval="ALL_TIME",
        evidence_receipt_refs=(evidence_ref,),
        proposed_parent_authority_refs=parent_refs,
        proposed_negative_limit_refs=(),
        proposed_supersession_refs=supersession_refs,
        interpretation_semantics={"rule": semantics},
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", "Z06"),
        correction_kind=correction_kind,
        correction_target_refs=correction_target_refs,
        correction_scope_ref=correction_scope_ref,
        source_onboarding_refs=source_refs,
    )


def _approve_and_seal(
    executor: AuthorityMaintenanceExecutor,
    candidate: AuthorityCandidate,
    tag: str,
):
    adjudication = executor.adjudicate_candidate(
        candidate.ref,
        decision="APPROVED",
        adjudicator_ref=_ref("ADJUDICATOR", tag),
        adjudication_authority_ref=_ref("GOVERNING_AUTHORITY", "AUTH40"),
        findings_ref=_ref("FINDINGS", tag),
    )
    seal = executor.seal_revision(
        candidate.ref,
        adjudication.ref,
        seal_attestation_ref=_ref("SEAL_ATTESTATION", tag),
    )
    return adjudication, seal


def _recompiler(calls: list[ExactRef]):
    def rebuild(old_ref: ExactRef, changed: tuple[AuthorityRef, ...]) -> ExactRef:
        calls.append(old_ref)
        tag = old_ref.key + "|" + "|".join(ref.key for ref in changed)
        return _ref("RECOMPILED_DEPENDENT", tag)

    return rebuild


def _two_revision_fixture():
    evidence = _evidence("two-revision")
    v1 = _candidate(evidence.ref, version="1.0.0", semantics="v1")
    v2 = _candidate(
        evidence.ref,
        version="2.0.0",
        semantics="v2",
        parent_refs=(v1.proposed_authority_ref,),
        supersession_refs=(v1.proposed_authority_ref,),
    )
    affected = _ref("DERIVED", "affected")
    descendant = _ref("DERIVED", "affected-child")
    unaffected = _ref("DERIVED", "unaffected")
    graph = SemanticDeterminantGraph(
        authority_edges=(
            (v1.proposed_authority_ref, affected),
            (v2.proposed_authority_ref, affected),
            (_other_authority(), unaffected),
        ),
        dependency_edges=((affected, descendant),),
        known_dependent_refs=(affected, descendant, unaffected),
    )
    executor = AuthorityMaintenanceExecutor(determinant_graph=graph)
    executor.intake_evidence(evidence)
    executor.intake_candidate(v1)
    _, seal1 = _approve_and_seal(executor, v1, "v1")
    release1 = executor.promote_current(
        seal1.ref,
        selection_rule_ref=_ref("SELECTION_RULE", "promote-v1"),
        selection_attestation_ref=_ref("SELECTION_ATTESTATION", "promote-v1"),
        recompiler=_recompiler([]),
    )
    executor.intake_candidate(v2)
    _, seal2 = _approve_and_seal(executor, v2, "v2")
    return executor, v1, v2, seal1, seal2, release1, affected, descendant, unaffected


def test_future_source_onboarding_can_produce_semantic_authority_candidate_without_prebuilt_snapshot():
    executor = AuthorityMaintenanceExecutor()
    source_release = _ref("C11_LOGICAL_RELEASE", "new-wave")
    evidence, candidate = executor.propose_source_onboarding_candidate(
        source_release_ref=source_release,
        source_semantic_evidence_refs=(
            _ref("SOURCE_QUESTIONNAIRE", "new-wave"),
            _ref("MANUAL_SEMANTIC_EVIDENCE", "new-wave"),
        ),
        candidate_id="NEW-WAVE-AUTHORITY-CANDIDATE",
        authority_id="AUTH-NEW-WAVE-SEMANTICS",
        authority_version="1.0.0",
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        proposed_decision_state="ALLOW",
        governed_operations=("INTERPRET_SOURCE_SEMANTICS",),
        governed_object_families=("RespondentEvent@1.0.0",),
        scope_envelope={"source_universe_refs": (_ref("EMPIRICAL_UNIVERSE", "new-wave"),)},
        effective_time_or_interval="2026",
        interpretation_semantics={"question": "Q1", "meaning": "governed-new-terrain"},
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", "new-wave"),
    )

    assert executor.snapshots == ()
    assert source_release in evidence.source_release_refs
    assert source_release in candidate.source_onboarding_refs
    assert executor.candidate_status(candidate.ref) == "PROPOSED"

    adjudication, seal = _approve_and_seal(executor, candidate, "new-wave")
    assert adjudication.decision == "APPROVED"
    assert seal.authority_ref == candidate.proposed_authority_ref
    assert executor.resolve_historical_exact(seal.authority_ref).authority_id == candidate.authority_id


def test_positive_seal_and_promotion_require_explicit_complete_governed_adjudication():
    evidence = _evidence("adjudication")
    candidate = _candidate(evidence.ref)
    executor = AuthorityMaintenanceExecutor()
    executor.intake_evidence(evidence)
    executor.intake_candidate(candidate)

    deferred = executor.adjudicate_candidate(
        candidate.ref,
        decision="DEFERRED",
        adjudicator_ref=_ref("ADJUDICATOR", "defer"),
        adjudication_authority_ref=_ref("GOVERNING_AUTHORITY", "AUTH40"),
        findings_ref=_ref("FINDINGS", "defer"),
    )
    assert executor.candidate_status(candidate.ref) == "DEFERRED"
    with pytest.raises(AuthorityMaintenanceError):
        executor.seal_revision(
            candidate.ref,
            deferred.ref,
            seal_attestation_ref=_ref("SEAL_ATTESTATION", "illegal-defer"),
        )

    approved = executor.adjudicate_candidate(
        candidate.ref,
        decision="APPROVED",
        adjudicator_ref=_ref("ADJUDICATOR", "approve"),
        adjudication_authority_ref=_ref("GOVERNING_AUTHORITY", "AUTH40"),
        findings_ref=_ref("FINDINGS", "approve"),
    )
    seal = executor.seal_revision(
        candidate.ref,
        approved.ref,
        seal_attestation_ref=_ref("SEAL_ATTESTATION", "approve"),
    )
    assert seal.authority_ref == candidate.proposed_authority_ref


def test_approved_adjudication_cannot_hide_candidate_evidence():
    e1 = _evidence("e1")
    e2 = _evidence("e2")
    candidate = AuthorityCandidate(
        **{
            **_candidate(e1.ref).__dict__,
            "candidate_id": "MULTI-EVIDENCE",
            "evidence_receipt_refs": (e1.ref, e2.ref),
        }
    )
    executor = AuthorityMaintenanceExecutor()
    executor.intake_evidence(e1)
    executor.intake_evidence(e2)
    executor.intake_candidate(candidate)

    with pytest.raises(AuthorityMaintenanceError):
        executor.adjudicate_candidate(
            candidate.ref,
            decision="APPROVED",
            adjudicator_ref=_ref("ADJUDICATOR", "partial"),
            adjudication_authority_ref=_ref("GOVERNING_AUTHORITY", "AUTH40"),
            findings_ref=_ref("FINDINGS", "partial"),
            evidence_receipt_refs=(e1.ref,),
        )


def test_rejected_candidate_remains_typed_and_cannot_mint_revision():
    evidence = _evidence("reject")
    candidate = _candidate(evidence.ref, semantics="reject")
    executor = AuthorityMaintenanceExecutor()
    executor.intake_evidence(evidence)
    executor.intake_candidate(candidate)
    rejected = executor.adjudicate_candidate(
        candidate.ref,
        decision="REJECTED",
        adjudicator_ref=_ref("ADJUDICATOR", "reject"),
        adjudication_authority_ref=_ref("GOVERNING_AUTHORITY", "AUTH40"),
        findings_ref=_ref("FINDINGS", "reject"),
    )
    assert isinstance(rejected, AuthorityAdjudicationReceipt)
    assert executor.candidate_status(candidate.ref) == "REJECTED"
    assert executor.snapshots == ()
    with pytest.raises(AuthorityMaintenanceError):
        executor.seal_revision(
            candidate.ref,
            rejected.ref,
            seal_attestation_ref=_ref("SEAL_ATTESTATION", "reject"),
        )
    with pytest.raises(AuthorityMaintenanceError):
        executor.adjudicate_candidate(
            candidate.ref,
            decision="APPROVED",
            adjudicator_ref=_ref("ADJUDICATOR", "illegal-reopen"),
            adjudication_authority_ref=_ref("GOVERNING_AUTHORITY", "AUTH40"),
            findings_ref=_ref("FINDINGS", "illegal-reopen"),
        )


def test_same_id_version_conflicting_content_fails_closed():
    evidence = _evidence("conflict")
    v1 = _candidate(evidence.ref, version="1.0.0", semantics="A")
    executor = AuthorityMaintenanceExecutor()
    executor.intake_evidence(evidence)
    executor.intake_candidate(v1)
    _approve_and_seal(executor, v1, "conflict-v1")

    conflicting = _candidate(
        evidence.ref,
        version="1.0.0",
        semantics="B",
        parent_refs=(v1.proposed_authority_ref,),
        supersession_refs=(v1.proposed_authority_ref,),
    )
    with pytest.raises(AuthorityMaintenanceConflict):
        executor.intake_candidate(conflicting)


def test_latest_default_fuzzy_selector_tokens_are_rejected_and_no_latest_api_exists():
    evidence = _evidence("selector")
    with pytest.raises(AuthorityMaintenanceError):
        _candidate(evidence.ref, version="latest")
    with pytest.raises(AuthorityMaintenanceError):
        _candidate(evidence.ref, authority_id="DEFAULT")
    executor = AuthorityMaintenanceExecutor()
    assert not hasattr(executor, "resolve_latest")
    assert not hasattr(executor, "resolve_default")


@pytest.mark.parametrize("correction_kind", ["COLLISION_RESOLUTION", "SPLIT", "EXCLUSION", "BOUNDARY_CORRECTION"])
def test_correction_requires_exact_target_scope_and_genealogy(correction_kind: str):
    evidence = _evidence(f"correction-{correction_kind}")
    v1 = _candidate(evidence.ref, version="1.0.0", semantics="before")
    executor = AuthorityMaintenanceExecutor()
    executor.intake_evidence(evidence)
    executor.intake_candidate(v1)
    _approve_and_seal(executor, v1, f"{correction_kind}-v1")

    scope = None if correction_kind == "COLLISION_RESOLUTION" else _ref(
        "CORRECTION_SCOPE", correction_kind
    )
    corrected = _candidate(
        evidence.ref,
        version="2.0.0",
        semantics=f"after-{correction_kind}",
        parent_refs=(v1.proposed_authority_ref,),
        supersession_refs=(v1.proposed_authority_ref,),
        correction_kind=correction_kind,
        correction_target_refs=(v1.proposed_authority_ref,),
        correction_scope_ref=scope,
    )
    executor.intake_candidate(corrected)
    _, seal = _approve_and_seal(executor, corrected, f"{correction_kind}-v2")
    snapshot = executor.resolve_historical_exact(seal.authority_ref)
    assert v1.proposed_authority_ref.as_dict() in snapshot.parent_authority_refs
    assert v1.proposed_authority_ref.as_dict() in snapshot.supersession_refs


def test_split_exclusion_or_boundary_without_exact_scope_fails_closed():
    evidence = _evidence("scope")
    for kind in ("SPLIT", "EXCLUSION", "BOUNDARY_CORRECTION"):
        with pytest.raises(AuthorityMaintenanceError):
            _candidate(
                evidence.ref,
                correction_kind=kind,
                correction_target_refs=(_other_authority(kind),),
                correction_scope_ref=None,
            )


def test_correction_target_not_in_parent_or_supersession_genealogy_is_rejected():
    evidence = _evidence("bad-genealogy")
    v1 = _candidate(evidence.ref, version="1.0.0", semantics="before")
    executor = AuthorityMaintenanceExecutor()
    executor.intake_evidence(evidence)
    executor.intake_candidate(v1)
    _approve_and_seal(executor, v1, "bad-genealogy-v1")

    unrelated = _other_authority("unrelated")
    bad = _candidate(
        evidence.ref,
        version="2.0.0",
        semantics="bad",
        parent_refs=(v1.proposed_authority_ref,),
        supersession_refs=(v1.proposed_authority_ref,),
        correction_kind="COLLISION_RESOLUTION",
        correction_target_refs=(unrelated,),
    )
    with pytest.raises(AuthorityMaintenanceError):
        executor.intake_candidate(bad)


def test_evidence_accumulation_is_append_only_and_has_exact_candidate_genealogy():
    e1 = _evidence("accum-1")
    e2 = _evidence("accum-2")
    candidate = _candidate(e1.ref, candidate_id="ACCUMULATING-CANDIDATE")
    executor = AuthorityMaintenanceExecutor()
    executor.intake_evidence(e1)
    executor.intake_evidence(e2)
    executor.intake_candidate(candidate)

    revised = executor.accumulate_candidate_evidence(candidate.ref, e2.ref)
    assert revised.candidate_revision == 2
    assert revised.parent_candidate_ref == candidate.ref
    assert set(revised.evidence_receipt_refs) == {e1.ref, e2.ref}
    assert candidate.ref != revised.ref
    assert executor.candidate_status(candidate.ref) == "PROPOSED"
    assert executor.candidate_status(revised.ref) == "PROPOSED"


def test_promotion_selectively_invalidates_and_recompiles_only_semantic_descendants():
    (
        executor,
        v1,
        v2,
        _seal1,
        seal2,
        _release1,
        affected,
        descendant,
        unaffected,
    ) = _two_revision_fixture()
    calls: list[ExactRef] = []
    release2 = executor.promote_current(
        seal2.ref,
        selection_rule_ref=_ref("SELECTION_RULE", "promote-v2"),
        selection_attestation_ref=_ref("SELECTION_ATTESTATION", "promote-v2"),
        recompiler=_recompiler(calls),
    )
    receipt = executor.invalidation_receipt_for_release(release2.ref)

    assert set(receipt.affected_dependent_refs) == {affected, descendant}
    assert set(receipt.unaffected_dependent_refs) == {unaffected}
    assert set(calls) == {affected, descendant}
    assert unaffected not in calls
    assert executor.resolve_historical_exact(v1.proposed_authority_ref).authority_version == "1.0.0"
    assert executor.resolve_historical_exact(v2.proposed_authority_ref).authority_version == "2.0.0"


def test_failed_recompiler_leaves_current_selection_and_event_chain_unchanged():
    executor, v1, _v2, _seal1, seal2, _release1, *_ = _two_revision_fixture()
    before_current = dict(executor.current_selection)
    before_events = executor.events

    def explode(_old: ExactRef, _changed: tuple[AuthorityRef, ...]) -> ExactRef:
        raise RuntimeError("hostile recompiler failure")

    with pytest.raises(RuntimeError):
        executor.promote_current(
            seal2.ref,
            selection_rule_ref=_ref("SELECTION_RULE", "atomic-fail"),
            selection_attestation_ref=_ref("SELECTION_ATTESTATION", "atomic-fail"),
            recompiler=explode,
        )
    assert dict(executor.current_selection) == before_current
    assert executor.events == before_events
    assert executor.current_selection[v1.authority_id] == v1.proposed_authority_ref


def test_changed_authority_with_affected_dependents_fails_closed_without_recompiler():
    executor, _v1, _v2, _seal1, seal2, _release1, *_ = _two_revision_fixture()
    before = dict(executor.current_selection)
    with pytest.raises(AuthorityMaintenanceError):
        executor.promote_current(
            seal2.ref,
            selection_rule_ref=_ref("SELECTION_RULE", "no-recompiler"),
            selection_attestation_ref=_ref("SELECTION_ATTESTATION", "no-recompiler"),
            recompiler=None,
        )
    assert dict(executor.current_selection) == before


def test_rollback_selects_prior_lawful_release_without_mutating_history():
    (
        executor,
        v1,
        v2,
        _seal1,
        seal2,
        release1,
        *_,
    ) = _two_revision_fixture()
    release2 = executor.promote_current(
        seal2.ref,
        selection_rule_ref=_ref("SELECTION_RULE", "v2"),
        selection_attestation_ref=_ref("SELECTION_ATTESTATION", "v2"),
        recompiler=_recompiler([]),
    )
    v1_before = executor.resolve_historical_exact(v1.proposed_authority_ref)
    v2_before = executor.resolve_historical_exact(v2.proposed_authority_ref)

    rollback = executor.rollback_current(
        v1.authority_id,
        target_prior_release_ref=release1.ref,
        rollback_rule_ref=_ref("ROLLBACK_RULE", "to-v1"),
        rollback_attestation_ref=_ref("ROLLBACK_ATTESTATION", "to-v1"),
        recompiler=_recompiler([]),
    )

    assert rollback.release_kind == "ROLLBACK"
    assert rollback.prior_lawful_release_ref == release1.ref
    assert rollback.previous_current_authority_ref == release2.selected_authority_ref
    assert executor.current_selection[v1.authority_id] == v1.proposed_authority_ref
    assert executor.resolve_historical_exact(v1.proposed_authority_ref) == v1_before
    assert executor.resolve_historical_exact(v2.proposed_authority_ref) == v2_before
    assert len(executor.snapshots) == 2
    selection_ref = executor.current_selection_receipt_ref(v1.authority_id)
    assert selection_ref == rollback.ref
    assert executor.resolve_current_exact(
        v1.authority_id, selection_receipt_ref=selection_ref
    ) == v1_before


def test_rollback_requires_exact_prior_release_not_merely_an_old_snapshot_ref():
    executor, v1, _v2, _seal1, seal2, _release1, *_ = _two_revision_fixture()
    executor.promote_current(
        seal2.ref,
        selection_rule_ref=_ref("SELECTION_RULE", "v2"),
        selection_attestation_ref=_ref("SELECTION_ATTESTATION", "v2"),
        recompiler=_recompiler([]),
    )
    with pytest.raises(AuthorityMaintenanceError):
        executor.rollback_current(
            v1.authority_id,
            target_prior_release_ref=_ref("RELEASE", "invented"),
            rollback_rule_ref=_ref("ROLLBACK_RULE", "invented"),
            rollback_attestation_ref=_ref("ROLLBACK_ATTESTATION", "invented"),
            recompiler=_recompiler([]),
        )


def test_deterministic_checkpoint_restart_and_replay_identity():
    executor, v1, _v2, _seal1, seal2, release1, *_ = _two_revision_fixture()
    executor.promote_current(
        seal2.ref,
        selection_rule_ref=_ref("SELECTION_RULE", "replay-v2"),
        selection_attestation_ref=_ref("SELECTION_ATTESTATION", "replay-v2"),
        recompiler=_recompiler([]),
    )
    executor.rollback_current(
        v1.authority_id,
        target_prior_release_ref=release1.ref,
        rollback_rule_ref=_ref("ROLLBACK_RULE", "replay-v1"),
        rollback_attestation_ref=_ref("ROLLBACK_ATTESTATION", "replay-v1"),
        recompiler=_recompiler([]),
    )

    checkpoint = executor.export_checkpoint()
    restored = AuthorityMaintenanceExecutor.from_checkpoint(checkpoint)
    restored_checkpoint = restored.export_checkpoint()
    assert checkpoint["checkpoint_hash"] == restored_checkpoint["checkpoint_hash"]
    assert executor.events == restored.events
    assert dict(executor.current_selection) == dict(restored.current_selection)

    replay_receipt = executor.audit_replay()
    assert replay_receipt.replay_state == "REPLAY_VERIFIED"
    assert replay_receipt.original_checkpoint_hash == replay_receipt.replayed_checkpoint_hash


def test_later_current_revision_never_reinterprets_exact_historical_authority():
    executor, v1, v2, _seal1, seal2, _release1, *_ = _two_revision_fixture()
    executor.promote_current(
        seal2.ref,
        selection_rule_ref=_ref("SELECTION_RULE", "historical-v2"),
        selection_attestation_ref=_ref("SELECTION_ATTESTATION", "historical-v2"),
        recompiler=_recompiler([]),
    )
    registry = executor.authority_registry()
    old = registry.resolve_exact(v1.proposed_authority_ref).snapshot
    current = registry.resolve_exact(v2.proposed_authority_ref).snapshot
    assert old.authority_version == "1.0.0"
    assert current.authority_version == "2.0.0"
    assert old.authority_ref != current.authority_ref


def test_current_resolution_requires_exact_selection_receipt_not_implicit_latest():
    executor, v1, _v2, _seal1, _seal2, release1, *_ = _two_revision_fixture()
    assert executor.resolve_current_exact(
        v1.authority_id, selection_receipt_ref=release1.ref
    ).authority_ref == v1.proposed_authority_ref
    with pytest.raises(AuthorityMaintenanceError):
        executor.resolve_current_exact(
            v1.authority_id, selection_receipt_ref=_ref("RELEASE", "wrong")
        )
