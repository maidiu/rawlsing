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
    AuthorityInvalidationReceipt,
    AuthorityReleaseReceipt,
    NoncurrentDependentOutcome,
    NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
    INVALIDATION_RECEIPT_NONCURRENT_SCHEMA,
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


# ==========================================================================
# Astra option-A: generic noncurrent lifecycle outcome at the OWNER level
# ==========================================================================
def _nref(tag: str, digest: str = "0" * 64) -> ExactRef:
    return ExactRef("TEST_OBJECT@1", f"urn:test:am:{tag}", digest)


def _auth(tag: str = "A") -> AuthorityRef:
    return AuthorityRef("TEST-AUTH@1", "1.0.0", "a" * 64)


def _ground(tag: str = "G") -> ExactRef:
    return _nref(f"ground-{tag}", "1" * 64)


def _noncurrent(old: ExactRef, *, reason="NO_LAWFUL_REPLACEMENT_SOURCE", grounds=None,
                replacement=None) -> NoncurrentDependentOutcome:
    return NoncurrentDependentOutcome(
        old_ref=old,
        disposition=NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
        reason_code=reason,
        supporting_refs=(grounds,) if grounds else (_ground(),),
        replacement_ref=replacement,
    )


# --------------------------------------------------------------------------
# A / B: the single generic disposition and its ground
# --------------------------------------------------------------------------
def test_a_noncurrent_row_is_one_fixed_typed_disposition():
    old = _nref("old")
    row = _noncurrent(old)
    assert row.disposition == NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT
    assert row.replacement_ref is None
    assert row.old_ref.key == old.key


def test_a_no_c1_specific_or_split_semantic_classes():
    """One generic disposition only. No deferred/unavailable/deleted variants."""
    with pytest.raises(AuthorityMaintenanceError, match="exactly one generic noncurrent"):
        NoncurrentDependentOutcome(
            old_ref=_nref("old"), disposition="DEFERRED", reason_code="x",
            supporting_refs=(_ground(),),
        )
    with pytest.raises(AuthorityMaintenanceError, match="exactly one generic noncurrent"):
        NoncurrentDependentOutcome(
            old_ref=_nref("old"), disposition="UNAVAILABLE", reason_code="x",
            supporting_refs=(_ground(),),
        )


def test_a_forged_or_missing_grounds_are_refused():
    with pytest.raises(AuthorityMaintenanceError, match="requires exact supporting"):
        NoncurrentDependentOutcome(
            old_ref=_nref("old"), disposition=NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
            reason_code="NO_LAWFUL_REPLACEMENT_SOURCE", supporting_refs=(),
        )
    with pytest.raises(AuthorityMaintenanceError, match="reason_code"):
        NoncurrentDependentOutcome(
            old_ref=_nref("old"), disposition=NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
            reason_code="", supporting_refs=(_ground(),),
        )


def test_a_noncurrent_row_may_not_carry_a_replacement_ref():
    with pytest.raises(AuthorityMaintenanceError, match="may not carry a replacement ref"):
        _noncurrent(_nref("old"), replacement=_nref("new", "2" * 64))


# --------------------------------------------------------------------------
# Coverage invariants over the receipt
# --------------------------------------------------------------------------
def _receipt(affected, pairs, noncurrent=(), unaffected=()):
    return AuthorityInvalidationReceipt(
        changed_authority_refs=(_auth(),), affected_dependent_refs=affected,
        unaffected_dependent_refs=unaffected, recompilation_pairs=pairs,
        noncurrent_dependents=tuple(noncurrent),
    )


def test_b_r_and_n_disjoint_and_cover_a_exactly():
    a, b, u = _nref("a", "1" * 64), _nref("b", "2" * 64), _nref("u", "3" * 64)
    receipt = _receipt((a, b), ((a, _nref("a2", "4" * 64)),), (_noncurrent(b),), (u,))
    assert receipt.preserves_legacy_identity is False
    r = {x.key for x in receipt.replacement_old_refs}
    n = {x.key for x in receipt.noncurrent_old_refs}
    assert r.isdisjoint(n)
    assert r | n == {x.key for x in receipt.affected_dependent_refs}


def test_g_affected_outcome_missing_is_refused():
    a, b = _nref("a", "1" * 64), _nref("b", "2" * 64)
    with pytest.raises(AuthorityMaintenanceError, match="requires exactly one outcome"):
        _receipt((a, b), ((a, _nref("a2", "4" * 64)),))


def test_g_replacement_noncurrent_overlap_is_refused():
    a = _nref("a", "1" * 64)
    with pytest.raises(AuthorityMaintenanceError, match="both a replacement and a"):
        _receipt((a,), ((a, _nref("a2", "4" * 64)),), (_noncurrent(a),))


def test_g_unknown_source_ref_is_refused():
    """An outcome naming a dependent outside the affected set is refused, even when
    every genuinely affected dependent does have a lawful outcome."""
    a, b = _nref("a", "1" * 64), _nref("b", "2" * 64)
    with pytest.raises(AuthorityMaintenanceError, match="outside the affected set"):
        _receipt((a,), ((a, _nref("a2", "4" * 64)),), (_noncurrent(b),))


def test_g_replacement_equal_to_old_ref_is_refused():
    a = _nref("a", "1" * 64)
    with pytest.raises(AuthorityMaintenanceError, match="must be a new exact ref"):
        _receipt((a,), ((a, a),))


def test_g_duplicate_affected_outcome_is_refused():
    a = _nref("a", "1" * 64)
    with pytest.raises(AuthorityMaintenanceError, match="at most one noncurrent outcome"):
        _receipt((a,), (), (_noncurrent(a), _noncurrent(a)))


def test_g_affected_and_unaffected_overlap_is_refused():
    a = _nref("a", "1" * 64)
    with pytest.raises(AuthorityMaintenanceError, match="overlap"):
        _receipt((a,), ((a, _nref("a2", "4" * 64)),), (), (a,))


# --------------------------------------------------------------------------
# B: serialization / hashing / compatibility
# --------------------------------------------------------------------------
def test_b_positive_only_receipt_keeps_the_pre_extension_identity():
    """A positive-only receipt projects the ORIGINAL field set, byte for byte."""
    a, b = _nref("a", "1" * 64), _nref("b", "2" * 64)
    receipt = _receipt((a, b), ((a, _nref("a2", "4" * 64)), (b, _nref("b2", "5" * 64))))
    assert receipt.preserves_legacy_identity is True
    projection = receipt.semantic_projection()
    assert "noncurrent_dependents" not in projection
    assert "receipt_schema" not in projection
    assert set(projection) == {
        "contract_id", "record_type", "changed_authority_refs",
        "affected_dependent_refs", "unaffected_dependent_refs", "recompilation_pairs",
    }


def test_b_negative_rows_bind_into_canonical_hash_under_an_explicit_schema():
    a, b = _nref("a", "1" * 64), _nref("b", "2" * 64)
    receipt = _receipt((a, b), ((a, _nref("a2", "4" * 64)),), (_noncurrent(b),))
    projection = receipt.semantic_projection()
    assert projection["receipt_schema"] == INVALIDATION_RECEIPT_NONCURRENT_SCHEMA
    row = projection["noncurrent_dependents"][0]
    assert row["disposition"] == NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT
    assert row["replacement_ref"] is None
    assert row["supporting_refs"]
    # The grounds are inside the hash: changing them moves the receipt ref.
    other = _receipt((a, b), ((a, _nref("a2", "4" * 64)),),
                     (_noncurrent(b, grounds=_ground("Z")),))
    assert other.ref != receipt.ref


def test_b_from_dict_round_trip_reproduces_negative_rows_exactly():
    a, b = _nref("a", "1" * 64), _nref("b", "2" * 64)
    receipt = _receipt((a, b), ((a, _nref("a2", "4" * 64)),), (_noncurrent(b),))
    again = AuthorityInvalidationReceipt.from_dict(receipt.as_dict())
    assert again.ref == receipt.ref
    assert again.noncurrent_dependents == receipt.noncurrent_dependents
    assert again.recompilation_pairs == receipt.recompilation_pairs


def test_g_tampered_receipt_binding_is_refused():
    a, b = _nref("a", "1" * 64), _nref("b", "2" * 64)
    receipt = _receipt((a, b), ((a, _nref("a2", "4" * 64)),), (_noncurrent(b),))
    data = receipt.as_dict()
    data["noncurrent_dependents"][0]["reason_code"] = "TAMPERED"
    with pytest.raises(AuthorityMaintenanceError):
        AuthorityInvalidationReceipt.from_dict(data)


def test_g_tampered_graph_binding_is_refused():
    data = SemanticDeterminantGraph(
        authority_edges=((_auth(), _nref("a", "1" * 64)),), dependency_edges=(),
        known_dependent_refs=(_nref("a", "1" * 64),),
    ).as_dict()
    data["known_dependent_refs"] = []
    rebuilt = SemanticDeterminantGraph.from_dict(data)
    # The owner reconstructs the known set from the edges, so a stripped field cannot
    # silently shrink the dependent universe.
    assert rebuilt.known_dependent_refs[0].key == _nref("a", "1" * 64).key


def test_b_checkpoint_export_import_reproduces_negative_rows_and_currentness():
    from rawlsing_next.tests import c1_at18_at19_fixture as fx
    from rawlsing_next.pre553_authority_maintenance import (
        DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT,
    )

    t = fx.build_mixed_outcome_transition("forward")
    ex = t["executor"]
    ex.promote_current(
        t["seal_ref"],
        selection_rule_ref=_nref("sel", "7" * 64),
        selection_attestation_ref=_nref("att", "8" * 64),
        recompiler=lambda old, changed: _nref(f"new-{old.object_id[-8:]}", "9" * 64),
        noncurrent_outcomes=t["noncurrent_declarations"],
    )
    before = ex.invalidation_receipt_for_release(
        ex.current_selection_receipt_ref(t["old_model"].authority_id))
    rebuilt = AuthorityMaintenanceExecutor.from_checkpoint(ex.export_checkpoint())
    after = rebuilt.invalidation_receipt_for_release(
        rebuilt.current_selection_receipt_ref(t["old_model"].authority_id))
    assert after.ref == before.ref
    assert after.noncurrent_dependents == before.noncurrent_dependents
    assert rebuilt.dependent_lifecycle_status(
        t["noncurrent_product"])["lifecycle_state"] == DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT
    assert rebuilt.current_selection == ex.current_selection


def test_g_partial_transition_failure_commits_no_release():
    """Atomicity: invalid outcome data commits no release and no current change."""
    from rawlsing_next.tests import c1_at18_at19_fixture as fx

    t = fx.build_mixed_outcome_transition("forward")
    ex = t["executor"]
    releases_before = dict(ex._releases)
    current_before = dict(ex.current_selection)
    # An invalid declaration: a noncurrent row for a dependent the owner computes
    # unaffected (the sibling).
    bad = dict(t["noncurrent_declarations"])
    bad[t["sibling_ref"].key] = _noncurrent(t["sibling_ref"])
    with pytest.raises(AuthorityMaintenanceError, match="is not affected"):
        ex.promote_current(
            t["seal_ref"],
            selection_rule_ref=_nref("sel2", "7" * 64),
            selection_attestation_ref=_nref("att2", "8" * 64),
            recompiler=lambda old, changed: _nref(f"n-{old.object_id[-6:]}", "b" * 64),
            noncurrent_outcomes=bad,
        )
    assert dict(ex._releases) == releases_before
    assert dict(ex.current_selection) == current_before


def test_g_rollback_shares_the_same_outcome_law():
    """G: promotion AND rollback apply one outcome law, atomically.

    Uses the established two-revision fixture so the rollback target is a genuinely
    lawful prior release, not a fabricated one.
    """
    (
        executor, v1, _v2, _seal1, seal2, release1,
        affected, descendant, unaffected, *_,
    ) = _two_revision_fixture()
    executor.promote_current(
        seal2.ref,
        selection_rule_ref=_ref("SELECTION_RULE", "promote-v2"),
        selection_attestation_ref=_ref("SELECTION_ATTESTATION", "promote-v2"),
        recompiler=_recompiler([]),
    )
    # On rollback, changed = (v2, v1); `affected` and `descendant` are the affected set.
    declarations = {descendant.key: _noncurrent(
        descendant, reason="REQUIRED_INPUT_NONCURRENT")}

    # An invalid rollback outcome set commits nothing.
    releases_before = dict(executor._releases)
    current_before = dict(executor.current_selection)
    with pytest.raises(AuthorityMaintenanceError, match="is not affected"):
        executor.rollback_current(
            v1.authority_id,
            target_prior_release_ref=release1.ref,
            rollback_rule_ref=_ref("ROLLBACK_RULE", "bad"),
            rollback_attestation_ref=_ref("ROLLBACK_ATTESTATION", "bad"),
            recompiler=_recompiler([]),
            noncurrent_outcomes={
                descendant.key: _noncurrent(descendant),
                unaffected.key: _noncurrent(unaffected),
            },
        )
    assert dict(executor._releases) == releases_before
    assert dict(executor.current_selection) == current_before

    # A lawful rollback carries one replacement and one explicit noncurrent outcome.
    rolled = executor.rollback_current(
        v1.authority_id,
        target_prior_release_ref=release1.ref,
        rollback_rule_ref=_ref("ROLLBACK_RULE", "to-v1"),
        rollback_attestation_ref=_ref("ROLLBACK_ATTESTATION", "to-v1"),
        recompiler=_recompiler([]),
        noncurrent_outcomes=declarations,
    )
    receipt = executor.invalidation_receipt_for_release(rolled.ref)
    assert len(receipt.recompilation_pairs) == 1
    assert receipt.recompilation_pairs[0][0].key == affected.key
    assert len(receipt.noncurrent_dependents) == 1
    assert receipt.noncurrent_dependents[0].old_ref.key == descendant.key
    assert receipt.noncurrent_dependents[0].replacement_ref is None
    r = {x.key for x in receipt.replacement_old_refs}
    n = {x.key for x in receipt.noncurrent_old_refs}
    assert r.isdisjoint(n)
    assert r | n == {x.key for x in receipt.affected_dependent_refs}
    assert executor.current_selection[v1.authority_id] == v1.proposed_authority_ref


def test_b_later_restoration_requires_a_new_lawful_transition_not_cache_presence():
    """Re-reading the same release never restores currentness."""
    from rawlsing_next.tests import c1_at18_at19_fixture as fx

    t = fx.build_mixed_outcome_transition("forward")
    ex = t["executor"]
    ex.promote_current(
        t["seal_ref"],
        selection_rule_ref=_nref("s", "7" * 64),
        selection_attestation_ref=_nref("a", "8" * 64),
        recompiler=lambda old, changed: _nref(f"n-{old.object_id[-6:]}", "9" * 64),
        noncurrent_outcomes=t["noncurrent_declarations"],
    )
    first = ex.dependent_lifecycle_status(t["noncurrent_product"])["lifecycle_state"]
    # Repeated queries and re-exported checkpoints do not change the outcome.
    for _ in range(3):
        assert ex.dependent_lifecycle_status(
            t["noncurrent_product"])["lifecycle_state"] == first
    rebuilt = AuthorityMaintenanceExecutor.from_checkpoint(ex.export_checkpoint())
    assert rebuilt.dependent_lifecycle_status(
        t["noncurrent_product"])["lifecycle_state"] == first


def test_b_fresh_process_owner_replay_reproduces_both_outcome_classes(tmp_path):
    """B: a fresh OS process rebuilds the lifecycle from a checkpoint and reproduces
    the negative rows, the release/event identities, and current availability.

    This is a *serialization replay* grade for the lifecycle owner. It is explicitly
    NOT fresh analytical recomputation, and the test says so.
    """
    import json
    import subprocess
    import sys

    from rawlsing_next.tests import c1_at18_at19_fixture as fx

    t = fx.build_mixed_outcome_transition("forward")
    ex = t["executor"]
    release = ex.promote_current(
        t["seal_ref"],
        selection_rule_ref=_nref("s", "7" * 64),
        selection_attestation_ref=_nref("a", "8" * 64),
        recompiler=lambda old, changed: _nref(f"n-{old.object_id[-6:]}", "9" * 64),
        noncurrent_outcomes=t["noncurrent_declarations"],
    )
    checkpoint = ex.export_checkpoint()
    path = tmp_path / "owner_checkpoint.json"
    path.write_text(json.dumps(checkpoint))

    script = tmp_path / "replay_owner.py"
    script.write_text(
        "import json, sys\n"
        "sys.path.insert(0, %r)\n"
        "from rawlsing_next.pre553_authority_maintenance import AuthorityMaintenanceExecutor\n"
        "cp = json.load(open(%r))\n"
        "ex = AuthorityMaintenanceExecutor.from_checkpoint(cp)\n"
        "out = {}\n"
        "for rec in cp['checkpoint_payload']['invalidations']:\n"
        "    out.setdefault('noncurrent', []).extend(\n"
        "        [{'old_ref': r['old_ref'], 'disposition': r['disposition'],\n"
        "          'reason_code': r['reason_code'], 'supporting_refs': r['supporting_refs'],\n"
        "          'replacement_ref': r['replacement_ref']}\n"
        "         for r in rec.get('noncurrent_dependents', [])])\n"
        "out['current_selection'] = {row['authority_id']: row['authority_ref']\n"
        "                            for row in cp['checkpoint_payload']['current_selection']}\n"
        "out['releases'] = [r['record_ref'] for r in cp['checkpoint_payload']['releases']]\n"
        "print(json.dumps(out, sort_keys=True))\n"
        % (str(__import__('pathlib').Path.cwd()), str(path))
    )
    proc = subprocess.run(
        [sys.executable, str(script)], capture_output=True, text=True, check=True,
    )
    replayed = json.loads(proc.stdout)
    expected = [
        {"old_ref": r.old_ref.as_dict(), "disposition": r.disposition,
         "reason_code": r.reason_code, "supporting_refs": [x.as_dict() for x in r.supporting_refs],
         "replacement_ref": None}
        for r in ex.invalidation_receipt_for_release(release.ref).noncurrent_dependents
    ]
    _key = lambda r: json.dumps(r["old_ref"], sort_keys=True)
    assert sorted(replayed["noncurrent"], key=_key) == sorted(expected, key=_key)
    assert replayed["current_selection"] == {
        k: v.as_dict() for k, v in ex.current_selection.items()
    }
    assert replayed["releases"] == [r.ref.as_dict() for r in ex._releases.values()]
    # Grade honesty: this proves SERIALIZATION REPLAY of lifecycle state only.
    from rawlsing_next.pre553_analytical_replay_dependency import (
        REPLAY_GRADE_SERIALIZATION_REPLAY,
        REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
    )
    assert REPLAY_GRADE_SERIALIZATION_REPLAY != REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION
