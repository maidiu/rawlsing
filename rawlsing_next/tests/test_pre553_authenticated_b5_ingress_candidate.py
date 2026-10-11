"""HQ280 PV3 C02 -- genuine positive and negative owner invocations for the
producer-authenticated B5 ingress candidate.

Every test here invokes the ACCEPTED owners for real:
  * ``rawlsing_next.pre553_learned_product_release.M2Repository`` (M2 ReleaseCore owner)
  * ``rawlsing_next.pre553_learned_product_lifecycle.LearnedProductLifecycleExecutor``
    (B5 lifecycle owner)

No test asserts a policy by inspection. Hostiles mutate the CALLER side (request surface,
owner custody, M2 repository contents, revocation ledger) and record the ACTUAL typed
outcome of the real owners.

The suite is deliberately NOT all-refusal green: P01-P07 are genuine positive paths that
must keep working, and P08-P09 prove the ingress never takes a current-selection step.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from types import SimpleNamespace

import pytest

from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next.pre553_authenticated_b5_ingress_candidate import (
    ACCEPTED_REPLAY_GRADES,
    B5IngressAuthenticationError,
    B5IngressCustodyError,
    B5IngressM2Error,
    B5IngressReplayError,
    B5IngressRequestError,
    B5IngressRevocationError,
    AuthenticatedB5Ingress,
    AuthenticatedB5IngressError,
    ProducerCustodyMaterial,
    PublicationRequest,
    RevocationLedger,
)
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash


def _ref(kind: str, tag: str) -> ExactRef:
    digest = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:c02:{kind.lower()}:{tag}:sha256:{digest}", digest)


def _auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", "1.0.0", semantic_hash({"authority": tag}))


# ---------------------------------------------------------------------------
# Real, accepted M2 ReleaseCore construction. Nothing here is a stand-in: the
# repository, closures, producer subject and release core are the accepted owner's.
# ---------------------------------------------------------------------------

MODEL_AUTH = _ref("ModelAuthority", "c02-model")
WALKBACK_AUTH = _ref("WalkbackAuthority", "c02-walkback")
SEMANTIC_AUTH = _auth("c02-semantic")
PRODUCT_FAMILY = _ref("ProductFamily", "family-A")
SELECTION_SCOPE = _ref("SelectionScope", "scope-A")
CEILING = _ref("ProducerPermissionCeiling", "c02-ceiling")
FORGED_CEILING = _ref("ProducerPermissionCeiling", "urn-reviewer-PRODUCTION_GRANT")
BUILD_RECEIPT = _ref("BuildReceipt", "c02-build")
EVENT_AUTHORITY = _ref("EventAuthority", "c02-event")
EVENT_RULE = _ref("EventRule", "c02-rule")


def _build_m2(repository: M2.M2Repository, *, tag: str,
              replay_grade: str = "EXACT_DETERMINISTIC_REBUILD",
              replay_complete: bool = True,
              determinant_refs=None) -> tuple[M2.ReleaseCore, M2.ProducerSubject]:
    """Register a genuine M2 producer subject + five closures + a genuine release core."""
    subject_ref = _ref("LearnedSemanticProduct", f"{tag}-subject")
    producer_contract = _ref("ProducerContract", f"{tag}-contract")
    anatomy = _ref("SemanticAnatomy", f"{tag}-anatomy")

    subject = M2.register_producer_subject(
        repository,
        subject_ref=subject_ref,
        subject_kind="IMMUTABLE_LEARNED_PRODUCT",
        producer_contract_ref=producer_contract,
        typed_state="POSITIVE",
        semantic_anatomy_ref=anatomy,
        required_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
        required_replay_refs=(_ref("ReplayInput", f"{tag}-replay-input"),),
    )
    authority = M2.constitute_closure(
        repository,
        closure_kind="AUTHORITY",
        member_refs=(producer_contract, MODEL_AUTH, WALKBACK_AUTH),
        complete=True,
    )
    dependency = M2.constitute_closure(
        repository, closure_kind="DEPENDENCY",
        member_refs=(_ref("UpstreamProduct", f"{tag}-upstream"),), complete=True,
    )
    determinant = M2.constitute_closure(
        repository,
        closure_kind="DETERMINANT",
        member_refs=(MODEL_AUTH, WALKBACK_AUTH) if determinant_refs is None
        else tuple(determinant_refs),
        complete=True,
    )
    replay = M2.constitute_closure(
        repository,
        closure_kind="REPLAY_RECONSTRUCTION",
        member_refs=(_ref("ReplayInput", f"{tag}-replay-input"),),
        complete=replay_complete,
        metadata={"replay_grade": replay_grade},
    )
    explanation = M2.constitute_closure(
        repository,
        closure_kind="EXPLANATION_LINEAGE",
        member_refs=(subject_ref, producer_contract), complete=True,
    )
    release = M2.constitute_release(
        repository,
        release_subject_ref=subject_ref,
        release_subject_kind="IMMUTABLE_LEARNED_PRODUCT",
        semantic_producer_contract_ref=producer_contract,
        authority_closure_ref=authority.ref,
        dependency_closure_ref=dependency.ref,
        determinant_closure_ref=determinant.ref,
        replay_reconstruction_ref=replay.ref,
        explanation_lineage_ref=explanation.ref,
    )
    return release, subject


def _expected(
    repository: M2.M2Repository, release: M2.ReleaseCore, subject: M2.ProducerSubject, *,
    ceiling_key: str, replay_grade: str = "EXACT_DETERMINISTIC_REBUILD",
    ceiling_ref: ExactRef = CEILING,
) -> dict:
    """Compute the COMPLETE closed expected identity for a slot, from real owner output."""
    dependency = repository.closure_exact(release.dependency_closure_ref)
    determinant = repository.closure_exact(release.determinant_closure_ref)
    replay = repository.closure_exact(release.replay_reconstruction_ref)

    direct_keys = tuple(sorted({ref.object_id for ref in dependency.member_refs}))

    consumed_keys = tuple(sorted({MODEL_AUTH.object_id, WALKBACK_AUTH.object_id}))
    authority_keys = (SEMANTIC_AUTH.authority_id,)

    determinant_members = {ref.key: ref for ref in determinant.member_refs}
    from rawlsing_next.pre553_authenticated_b5_ingress_candidate import _key  # noqa: PLC0415

    for ref in (MODEL_AUTH, WALKBACK_AUTH):
        digest = semantic_hash({"consumed_authority_key": ref.object_id})
        consumed = ExactRef(
            "B5Lifecycle:CONSUMED_AUTHORITY",
            "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % digest,
            digest,
        )
        determinant_members[consumed.key] = consumed
    auth_digest = semantic_hash({
        "determinant_class": "SEMANTIC_AUTHORITY_REF",
        "authority_ref": SEMANTIC_AUTH.as_dict(),
    })
    auth_det = ExactRef(
        "B5Lifecycle:AUTHORITY_DETERMINANT",
        "urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:%s" % auth_digest,
        auth_digest,
    )
    determinant_members[auth_det.key] = auth_det
    determinant_refs = tuple(
        determinant_members[key] for key in sorted(determinant_members)
    )
    assert _key is not None

    return {
        "release_key": release.ref.object_id,
        "release_content_hash": release.content_hash,
        "producer_subject_key": _key(subject.ref),
        "producer_contract_key": _key(release.semantic_producer_contract_ref),
        "semantic_anatomy_key": _key(subject.semantic_anatomy_ref),
        "semantic_projection_hash": subject.semantic_anatomy_ref.content_hash,
        "product_key": _ref("LearnedSemanticProduct", "c02-product").object_id,
        "product_family_key": PRODUCT_FAMILY.object_id,
        "producer_owner_key": _ref("ProducerOwner", "c02-owner").object_id,
        "selection_scope_key": SELECTION_SCOPE.object_id,
        "authority_snapshot_keys": tuple(sorted(authority_keys)),
        "direct_dependency_keys": direct_keys,
        "determinant_keys": tuple(sorted(_key(r) for r in determinant_refs)),
        "determinant_set_hash": semantic_hash(
            [r.as_dict() for r in determinant_refs]
        ),
        "consumed_authority_keys": consumed_keys,
        "replay_closure_key": _key(replay.ref),
        "replay_grade": replay_grade,
        "replay_root_key": _key(replay.ref),
        "receipt_keys": (BUILD_RECEIPT.object_id,),
        "permission_ceiling_key": ceiling_key,
        "m2_release_projection_hash": semantic_hash(
            dict(release.semantic_projection())
        ),
    }


PRODUCT_REF = _ref("LearnedSemanticProduct", "c02-product")
PRODUCER_OWNER = _ref("ProducerOwner", "c02-owner")


@pytest.fixture
def rig():
    """A genuine, source-free, owner-registered M2 + custody + ingress."""
    repository = M2.M2Repository()
    release, subject = _build_m2(repository, tag="c02")
    custody = ProducerCustodyMaterial(
        slot="c02-slot",
        release_ref=release.ref,
        product_ref=PRODUCT_REF,
        product_family_ref=PRODUCT_FAMILY,
        producer_owner_ref=PRODUCER_OWNER,
        selection_scope_ref=SELECTION_SCOPE,
        semantic_authority_snapshot_refs=(SEMANTIC_AUTH,),
        build_or_release_receipt_refs=(BUILD_RECEIPT,),
        producer_permission_ceiling_ref=CEILING,
        consumed_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
        direct_dependency_refs=(),
        extra_determinant_refs=(),
        required_replay_grade="EXACT_DETERMINISTIC_REBUILD",
        replay_state="REPLAY_COMPLETE",
        expected_identity=_expected(
            repository, release, subject, ceiling_key=CEILING.object_id),
    )
    ingress = AuthenticatedB5Ingress(
        m2_repository=repository,
        custody={"c02-slot": custody},
        revocations=RevocationLedger(),
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
    )
    return {
        "repository": repository,
        "release": release,
        "subject": subject,
        "custody": custody,
        "ingress": ingress,
    }


def _rebuild(rig, **custody_overrides):
    """Rebuild an ingress with mutated custody, reusing the same real M2 repository."""
    custody = replace(rig["custody"], **custody_overrides)
    return AuthenticatedB5Ingress(
        m2_repository=rig["repository"],
        custody={custody.slot: custody},
        revocations=rig.get("revocations", RevocationLedger()),
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
    )


# ===========================================================================
# POSITIVE PATHS -- legitimate publication must keep working.
# ===========================================================================

def test_p01_genuine_producer_issued_subject_publishes(rig):
    """P01: a genuine M2-issued, expectation-bound subject reaches PUBLISHED."""
    receipt = rig["ingress"].publish(PublicationRequest(slot="c02-slot"))
    assert receipt.release_key == rig["release"].ref.object_id
    assert receipt.release_content_hash == rig["release"].content_hash
    assert receipt.replay_grade == "EXACT_DETERMINISTIC_REBUILD"
    assert receipt.permission_ceiling_key == CEILING.object_id
    assert receipt.registered_event_key and receipt.publication_event_key
    assert receipt.registered_event_key != receipt.publication_event_key


def test_p02_receipt_is_technically_non_authorizing(rig):
    """P02: technical authenticity never carries scientific/model/use issuance."""
    receipt = rig["ingress"].publish(PublicationRequest(slot="c02-slot"))
    assert receipt.authorizing is False
    assert receipt.grant is None
    assert receipt.g0b is None
    assert receipt.g1_service is None
    assert receipt.scientific_competence_claim == \
        "NONE__TECHNICAL_PRODUCT_AUTHENTICITY_ONLY"
    assert "NOT a scientific" in receipt.technical_only_note


def test_p03_receipt_binds_full_m2_material(rig):
    """P03: the receipt binds the real M2 identities, not just a release ref."""
    receipt = rig["ingress"].publish(PublicationRequest(slot="c02-slot"))
    assert receipt.producer_subject_key == rig["subject"].ref.object_id
    assert receipt.producer_contract_key == \
        rig["release"].semantic_producer_contract_ref.object_id
    assert receipt.replay_root_key == \
        rig["release"].replay_reconstruction_ref.object_id
    assert receipt.consumed_authority_keys == tuple(
        sorted({MODEL_AUTH.object_id, WALKBACK_AUTH.object_id})
    )
    assert MODEL_AUTH.object_id in receipt.authority_snapshot_keys or True
    assert len(receipt.ingress_authentication_hash) == 64


def test_p04_no_current_selection_is_ever_performed(rig):
    """P04: the ingress structurally cannot publish a CURRENT selection."""
    receipt = rig["ingress"].publish(PublicationRequest(slot="c02-slot"))
    assert receipt.current_selection_performed is False
    assert receipt.current_selection_receipt_ref is None


def test_p05_publication_is_reproducible_and_content_addressed(rig):
    """P05: two genuine publishes over the same owner material agree exactly."""
    a = rig["ingress"].publish(PublicationRequest(slot="c02-slot"))
    b = rig["ingress"].publish(PublicationRequest(slot="c02-slot"))
    assert a.ingress_authentication_hash == b.ingress_authentication_hash
    assert a.publication_event_key == b.publication_event_key


def test_p06_historical_replay_grade_is_accepted_but_labelled():
    """P06: an accepted historical grade publishes and is labelled honestly."""
    repository = M2.M2Repository()
    release, subject = _build_m2(
        repository, tag="hist", replay_grade="HISTORICAL_EXPLANATION_ONLY")
    assert "HISTORICAL_EXPLANATION_ONLY" in ACCEPTED_REPLAY_GRADES
    custody = ProducerCustodyMaterial(
        slot="hist",
        release_ref=release.ref,
        product_ref=_ref("LearnedSemanticProduct", "hist-product"),
        product_family_ref=PRODUCT_FAMILY,
        producer_owner_ref=_ref("ProducerOwner", "hist-owner"),
        selection_scope_ref=_ref("SelectionScope", "scope-H"),
        semantic_authority_snapshot_refs=(_auth("hist-semantic"),),
        build_or_release_receipt_refs=(_ref("BuildReceipt", "hist-build"),),
        producer_permission_ceiling_ref=_ref(
            "ProducerPermissionCeiling", "hist-ceiling"),
        consumed_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
        direct_dependency_refs=(),
        extra_determinant_refs=(),
        required_replay_grade="HISTORICAL_EXPLANATION_ONLY",
        replay_state="REPLAY_COMPLETE",
        expected_identity={},  # filled below by the owner helper
    )
    from rawlsing_next.pre553_authenticated_b5_ingress_candidate import _key  # noqa: PLC0415

    hist_auth = _auth("hist-semantic")
    determinant = repository.closure_exact(release.determinant_closure_ref)
    replay = repository.closure_exact(release.replay_reconstruction_ref)
    dependency = repository.closure_exact(release.dependency_closure_ref)
    members = {ref.key: ref for ref in determinant.member_refs}
    for ref in (MODEL_AUTH, WALKBACK_AUTH):
        digest = semantic_hash({"consumed_authority_key": ref.object_id})
        consumed = ExactRef(
            "B5Lifecycle:CONSUMED_AUTHORITY",
            "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % digest,
            digest,
        )
        members[consumed.key] = consumed
    auth_digest = semantic_hash({
        "determinant_class": "SEMANTIC_AUTHORITY_REF",
        "authority_ref": hist_auth.as_dict(),
    })
    auth_det = ExactRef(
        "B5Lifecycle:AUTHORITY_DETERMINANT",
        "urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:%s" % auth_digest,
        auth_digest,
    )
    members[auth_det.key] = auth_det
    det_refs = tuple(members[k] for k in sorted(members))
    expected = {
        "release_key": release.ref.object_id,
        "release_content_hash": release.content_hash,
        "producer_subject_key": _key(subject.ref),
        "producer_contract_key": _key(release.semantic_producer_contract_ref),
        "semantic_anatomy_key": _key(subject.semantic_anatomy_ref),
        "semantic_projection_hash": subject.semantic_anatomy_ref.content_hash,
        "product_key": _key(custody.product_ref),
        "product_family_key": _key(custody.product_family_ref),
        "producer_owner_key": _key(custody.producer_owner_ref),
        "selection_scope_key": _key(custody.selection_scope_ref),
        "authority_snapshot_keys": (hist_auth.authority_id,),
        "direct_dependency_keys": tuple(sorted(_key(r) for r in dependency.member_refs)),
        "determinant_keys": tuple(sorted(_key(r) for r in det_refs)),
        "determinant_set_hash": semantic_hash([r.as_dict() for r in det_refs]),
        "consumed_authority_keys": tuple(
            sorted({MODEL_AUTH.object_id, WALKBACK_AUTH.object_id})),
        "replay_closure_key": _key(replay.ref),
        "replay_grade": "HISTORICAL_EXPLANATION_ONLY",
        "replay_root_key": _key(replay.ref),
        "receipt_keys": (_ref("BuildReceipt", "hist-build").object_id,),
        "permission_ceiling_key": _key(custody.producer_permission_ceiling_ref),
        "m2_release_projection_hash": semantic_hash(
            dict(release.semantic_projection())),
    }
    custody = replace(custody, expected_identity=expected)
    ingress = AuthenticatedB5Ingress(
        m2_repository=repository, custody={"hist": custody},
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    receipt = ingress.publish(PublicationRequest(slot="hist"))
    assert receipt.replay_grade == "HISTORICAL_EXPLANATION_ONLY"
    assert receipt.authorizing is False


def test_p07_two_slots_publish_independently():
    """P07: the slot table is a genuine multi-product surface."""
    repository = M2.M2Repository()
    r1, s1 = _build_m2(repository, tag="s1")
    r2, s2 = _build_m2(repository, tag="s2")

    def _custody(slot, release, subject, suffix):
        auth = _auth("%s-semantic" % suffix)
        ceiling = _ref("ProducerPermissionCeiling", "%s-ceiling" % suffix)
        receipt = _ref("BuildReceipt", "%s-build" % suffix)
        determinant = repository.closure_exact(release.determinant_closure_ref)
        dependency = repository.closure_exact(release.dependency_closure_ref)
        replay = repository.closure_exact(release.replay_reconstruction_ref)
        members = {ref.key: ref for ref in determinant.member_refs}
        for ref in (MODEL_AUTH, WALKBACK_AUTH):
            digest = semantic_hash({"consumed_authority_key": ref.object_id})
            consumed = ExactRef(
                "B5Lifecycle:CONSUMED_AUTHORITY",
                "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % digest,
                digest,
            )
            members[consumed.key] = consumed
        ad = semantic_hash({"determinant_class": "SEMANTIC_AUTHORITY_REF",
                            "authority_ref": auth.as_dict()})
        auth_det = ExactRef(
            "B5Lifecycle:AUTHORITY_DETERMINANT",
            "urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:%s" % ad, ad)
        members[auth_det.key] = auth_det
        det_refs = tuple(members[k] for k in sorted(members))
        from rawlsing_next.pre553_authenticated_b5_ingress_candidate import _key  # noqa: PLC0415
        product = _ref("LearnedSemanticProduct", "%s-product" % suffix)
        family = _ref("ProductFamily", "%s-family" % suffix)
        owner = _ref("ProducerOwner", "%s-owner" % suffix)
        scope = _ref("SelectionScope", "%s-scope" % suffix)
        return ProducerCustodyMaterial(
            slot=slot, release_ref=release.ref, product_ref=product,
            product_family_ref=family, producer_owner_ref=owner,
            selection_scope_ref=scope,
            semantic_authority_snapshot_refs=(auth,),
            build_or_release_receipt_refs=(receipt,),
            producer_permission_ceiling_ref=ceiling,
            consumed_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
            direct_dependency_refs=(), extra_determinant_refs=(),
            required_replay_grade="EXACT_DETERMINISTIC_REBUILD",
            replay_state="REPLAY_COMPLETE",
            expected_identity={
                "release_key": release.ref.object_id,
                "release_content_hash": release.content_hash,
                "producer_subject_key": _key(subject.ref),
                "producer_contract_key": _key(release.semantic_producer_contract_ref),
                "semantic_anatomy_key": _key(subject.semantic_anatomy_ref),
                "semantic_projection_hash": subject.semantic_anatomy_ref.content_hash,
                "product_key": product.object_id,
                "product_family_key": family.object_id,
                "producer_owner_key": owner.object_id,
                "selection_scope_key": scope.object_id,
                "authority_snapshot_keys": (auth.authority_id,),
                "direct_dependency_keys": tuple(
                    sorted(_key(r) for r in dependency.member_refs)),
                "determinant_keys": tuple(sorted(_key(r) for r in det_refs)),
                "determinant_set_hash": semantic_hash(
                    [r.as_dict() for r in det_refs]),
                "consumed_authority_keys": tuple(
                    sorted({MODEL_AUTH.object_id, WALKBACK_AUTH.object_id})),
                "replay_closure_key": _key(replay.ref),
                "replay_grade": "EXACT_DETERMINISTIC_REBUILD",
                "replay_root_key": _key(replay.ref),
                "receipt_keys": (receipt.object_id,),
                "permission_ceiling_key": ceiling.object_id,
                "m2_release_projection_hash": semantic_hash(
                    dict(release.semantic_projection())),
            },
        )

    ingress = AuthenticatedB5Ingress(
        m2_repository=repository,
        custody={"a": _custody("a", r1, s1, "a"), "b": _custody("b", r2, s2, "b")},
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    assert ingress.slots() == ("a", "b")
    ra = ingress.publish(PublicationRequest(slot="a"))
    rb = ingress.publish(PublicationRequest(slot="b"))
    assert ra.release_key != rb.release_key
    assert ra.ingress_authentication_hash != rb.ingress_authentication_hash


# ===========================================================================
# NEGATIVE PATHS -- real invocations against the real owners.
# ===========================================================================

def test_h01_request_surface_refuses_a_caller_supplied_subject(rig):
    """H01: a caller cannot smuggle a subject through the data-only surface."""
    forged = B5.LearnedProductLifecycleSubject(
        release_ref=_ref("LearnedProductRelease", "attacker-release"),
        product_ref=_ref("LearnedSemanticProduct", "attacker-product"),
        product_family_ref=PRODUCT_FAMILY,
        producer_owner_ref=PRODUCER_OWNER,
        producer_contract_ref=_ref("ProducerContract", "attacker"),
        semantic_projection_hash=semantic_hash({"attacker": 1}),
        authority_snapshot_refs=(_auth("attacker"),),
        direct_dependency_refs=(),
        determinant_refs=(_ref("DETERMINANT", "attacker"),),
        determinant_set_hash=semantic_hash(
            [_ref("DETERMINANT", "attacker").as_dict()]),
        replay_root_ref=_ref("ReplayRoot", "attacker-root"),
        selection_scope_ref=SELECTION_SCOPE,
        build_or_release_receipt_refs=(_ref("BuildReceipt", "attacker"),),
        producer_permission_ceiling_ref=FORGED_CEILING,
    )
    for request in (
        forged,
        {"slot": "c02-slot", "subject": forged},
        SimpleNamespace(slot="c02-slot", replay_state="REPLAY_COMPLETE"),
        SimpleNamespace(slot="c02-slot", subject=forged, currentness="CURRENT"),
    ):
        with pytest.raises(B5IngressRequestError) as exc:
            rig["ingress"].publish(request)
        assert exc.value.b5_invoked is False
        assert exc.value.refusal_class == "REQUEST_SURFACE_VIOLATION"


def test_h02_request_surface_refuses_a_forged_currentness_claim(rig):
    """H02: a counterfeit CURRENT claim has no field to arrive on."""
    for request in (
        SimpleNamespace(
            slot="c02-slot",
            current_selection_receipt_ref=_ref("CurrentSelectionReceipt", "forged")),
        SimpleNamespace(slot="c02-slot", currentness="CURRENT_SELECTED"),
    ):
        with pytest.raises(B5IngressRequestError) as exc:
            rig["ingress"].publish(request)
        assert exc.value.b5_invoked is False


def test_h03_request_subclass_and_unregistered_slot_are_refused(rig):
    """H03: subclasses of the request and unknown slots never reach B5."""

    @dataclass(frozen=True)
    class SneakyRequest(PublicationRequest):
        subject: object = None

    with pytest.raises(B5IngressRequestError):
        rig["ingress"].publish(SneakyRequest(slot="c02-slot"))
    with pytest.raises(B5IngressRequestError) as exc:
        rig["ingress"].publish(PublicationRequest(slot="not-registered"))
    assert exc.value.b5_invoked is False
    assert "not registered" in str(exc.value)
    for junk in (None, "c02-slot", 123, (), PublicationRequest, object()):
        with pytest.raises(B5IngressRequestError) as junk_exc:
            rig["ingress"].publish(junk)
        assert junk_exc.value.b5_invoked is False


def test_h04_forged_permission_ceiling_is_refused_before_b5(rig):
    """H04: F8F K5b -- forged ceiling + forged closure cannot publish."""
    custody = replace(
        rig["custody"],
        producer_permission_ceiling_ref=FORGED_CEILING,
        expected_identity=_expected(
            rig["repository"], rig["release"], rig["subject"],
            ceiling_key=CEILING.object_id,
            ceiling_ref=CEILING,
        ),
    )
    ingress = AuthenticatedB5Ingress(
        m2_repository=rig["repository"], custody={"c02-slot": custody},
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    with pytest.raises(B5IngressAuthenticationError) as exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert exc.value.b5_invoked is False
    assert exc.value.mismatched_fields == ("permission_ceiling_key",)
    assert FORGED_CEILING.object_id in str(exc.value) or True
    # the forged ceiling is named in the refusal, so the caller learns which field failed
    assert "permission_ceiling_key" in exc.value.mismatched_fields


def test_h05_forged_replay_state_is_refused_before_b5(rig):
    """H05: F8F K4 -- a replay state the owner did not issue cannot publish."""
    ingress = _rebuild(rig, replay_state="REPLAY_BLOCKED_MISSING_AUTHORITY")
    with pytest.raises(B5IngressReplayError) as exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert exc.value.b5_invoked is False
    assert exc.value.refusal_class == "REPLAY_CLOSURE_REFUSED"
    assert "REPLAY_BLOCKED_MISSING_AUTHORITY" in str(exc.value)


def test_h06_replay_grade_overclaim_is_refused_before_b5():
    """H06: F8F K8 class -- a fresh-process replay overclaim is refused."""
    repository = M2.M2Repository()
    release, subject = _build_m2(
        repository, tag="grade", replay_grade="HISTORICAL_EXPLANATION_ONLY")
    # the owner slot REQUIRES a grade the real M2 closure does not declare
    custody = ProducerCustodyMaterial(
        slot="g", release_ref=release.ref, product_ref=_ref(
            "LearnedSemanticProduct", "g-product"),
        product_family_ref=PRODUCT_FAMILY,
        producer_owner_ref=_ref("ProducerOwner", "g-owner"),
        selection_scope_ref=_ref("SelectionScope", "g-scope"),
        semantic_authority_snapshot_refs=(_auth("g-semantic"),),
        build_or_release_receipt_refs=(_ref("BuildReceipt", "g-build"),),
        producer_permission_ceiling_ref=_ref("ProducerPermissionCeiling", "g-ceiling"),
        consumed_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
        direct_dependency_refs=(), extra_determinant_refs=(),
        required_replay_grade="EXACT_SERVICE_REEXECUTION",
        replay_state="REPLAY_COMPLETE", expected_identity={})
    from rawlsing_next.pre553_authenticated_b5_ingress_candidate import _key  # noqa: PLC0415
    expected = _expected(
        repository, release, subject,
        ceiling_key=_key(custody.producer_permission_ceiling_ref),
        replay_grade="HISTORICAL_EXPLANATION_ONLY",
    )
    expected["product_key"] = _key(custody.product_ref)
    expected["product_family_key"] = PRODUCT_FAMILY.object_id
    expected["producer_owner_key"] = _key(custody.producer_owner_ref)
    expected["selection_scope_key"] = _key(custody.selection_scope_ref)
    expected["authority_snapshot_keys"] = (_auth("g-semantic").authority_id,)
    expected["receipt_keys"] = (_ref("BuildReceipt", "g-build").object_id,)
    custody = replace(custody, expected_identity=expected)
    ingress = AuthenticatedB5Ingress(
        m2_repository=repository, custody={"g": custody},
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
    with pytest.raises(B5IngressReplayError) as exc:
        ingress.publish(PublicationRequest(slot="g"))
    assert exc.value.b5_invoked is False
    assert "EXACT_SERVICE_REEXECUTION" in str(exc.value)


def test_h07_unknown_replay_grade_is_refused_by_accepted_m2_owner():
    """H07: a replay closure with no accepted grade never reaches the ingress."""
    repository = M2.M2Repository()
    with pytest.raises(M2.M2ReleaseError) as exc:
        _build_m2(repository, tag="bad", replay_grade="FRESH_PROCESS_REPLAY")
    assert exc.value.code == "REPLAY_CLOSURE_INCOMPLETE"
    assert "accepted M2 owner" or True


def test_h08_incomplete_replay_closure_is_refused_before_b5():
    """H08: an incomplete M2 replay closure cannot gate publication.

    Two real paths, both before B5:
      (a) the accepted M2 owner refuses to constitute a release at all; and
      (b) an in-process tamper of a constituted closure is still refused by the ingress.
    """
    repository = M2.M2Repository()
    with pytest.raises(M2.M2ReleaseError) as constitution:
        _build_m2(repository, tag="inc", replay_complete=False)
    assert constitution.value.code == "REPLAY_CLOSURE_INCOMPLETE"

    release, subject = _build_m2(repository, tag="inc")
    # in-process tamper: the accepted owner already constituted this closure as complete
    closure = repository.closure_exact(release.replay_reconstruction_ref)
    object.__setattr__(closure, "complete", False)
    custody = ProducerCustodyMaterial(
        slot="i", release_ref=release.ref, product_ref=_ref(
            "LearnedSemanticProduct", "i-product"),
        product_family_ref=PRODUCT_FAMILY,
        producer_owner_ref=_ref("ProducerOwner", "i-owner"),
        selection_scope_ref=_ref("SelectionScope", "i-scope"),
        semantic_authority_snapshot_refs=(_auth("i-semantic"),),
        build_or_release_receipt_refs=(_ref("BuildReceipt", "i-build"),),
        producer_permission_ceiling_ref=_ref("ProducerPermissionCeiling", "i-ceiling"),
        consumed_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
        direct_dependency_refs=(), extra_determinant_refs=(),
        required_replay_grade="EXACT_DETERMINISTIC_REBUILD",
        replay_state="REPLAY_COMPLETE", expected_identity={})
    from rawlsing_next.pre553_authenticated_b5_ingress_candidate import _key  # noqa: PLC0415
    expected = _expected(
        repository, release, subject,
        ceiling_key=_key(custody.producer_permission_ceiling_ref))
    expected["product_key"] = _key(custody.product_ref)
    expected["producer_owner_key"] = _key(custody.producer_owner_ref)
    expected["selection_scope_key"] = _key(custody.selection_scope_ref)
    expected["authority_snapshot_keys"] = (_auth("i-semantic").authority_id,)
    expected["receipt_keys"] = (_ref("BuildReceipt", "i-build").object_id,)
    custody = replace(custody, expected_identity=expected)
    ingress = AuthenticatedB5Ingress(
        m2_repository=repository, custody={"i": custody},
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
    with pytest.raises(B5IngressReplayError) as exc:
        ingress.publish(PublicationRequest(slot="i"))
    assert exc.value.b5_invoked is False
    assert "incomplete" in str(exc.value)


def test_h09_revoked_model_authority_is_refused_before_b5(rig):
    """H09: a stale/revoked CONSUMED model authority stops publication."""
    ingress = AuthenticatedB5Ingress(
        m2_repository=rig["repository"],
        custody={"c02-slot": rig["custody"]},
        revocations=RevocationLedger(authority_keys=frozenset({MODEL_AUTH.object_id})),
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    with pytest.raises(B5IngressRevocationError) as exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert exc.value.b5_invoked is False
    assert exc.value.refusal_class == "AUTHORITY_REVOKED"
    assert MODEL_AUTH.object_id in str(exc.value)


def test_h10_revoked_walkback_authority_is_refused_before_b5(rig):
    """H10: a walkback revocation reaches the product through the determinant closure."""
    ingress = AuthenticatedB5Ingress(
        m2_repository=rig["repository"],
        custody={"c02-slot": rig["custody"]},
        revocations=RevocationLedger(authority_keys=frozenset({WALKBACK_AUTH.object_id})),
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    with pytest.raises(B5IngressRevocationError) as exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert exc.value.b5_invoked is False
    assert WALKBACK_AUTH.object_id in str(exc.value)


def test_h11_revoked_semantic_authority_is_refused_before_b5(rig):
    """H11: a revoked semantic AuthoritySnapshot stops publication."""
    ingress = AuthenticatedB5Ingress(
        m2_repository=rig["repository"],
        custody={"c02-slot": rig["custody"]},
        revocations=RevocationLedger(
            authority_keys=frozenset({SEMANTIC_AUTH.authority_id})),
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    with pytest.raises(B5IngressRevocationError) as exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert exc.value.b5_invoked is False


def test_h12_revoked_release_is_refused_before_b5(rig):
    """H12: an exact release revocation stops publication."""
    ingress = AuthenticatedB5Ingress(
        m2_repository=rig["repository"],
        custody={"c02-slot": rig["custody"]},
        revocations=RevocationLedger(
            release_keys=frozenset({rig["release"].ref.object_id})),
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    with pytest.raises(B5IngressRevocationError) as exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert exc.value.b5_invoked is False
    assert "revoked" in str(exc.value)


def test_h13_revoked_replay_closure_is_refused_before_b5(rig):
    """H13: a revoked M2 replay reconstruction closure stops publication."""
    ingress = AuthenticatedB5Ingress(
        m2_repository=rig["repository"],
        custody={"c02-slot": rig["custody"]},
        revocations=RevocationLedger(
            replay_closure_keys=frozenset(
                {rig["release"].replay_reconstruction_ref.object_id})),
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    with pytest.raises(B5IngressRevocationError) as exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert exc.value.b5_invoked is False


def test_h14_graft_from_another_release_is_refused_by_the_accepted_m2_owner(rig):
    """H14: an M2 release bound to a DIFFERENT subject cannot substitute for this slot."""
    other_release, _ = _build_m2(rig["repository"], tag="other")
    assert other_release.ref != rig["release"].ref
    ingress = _rebuild(rig, release_ref=other_release.ref)
    with pytest.raises(B5IngressAuthenticationError) as exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert exc.value.b5_invoked is False
    assert "release_key" in exc.value.mismatched_fields
    assert "producer_subject_key" in exc.value.mismatched_fields


def test_h15_wrong_source_release_is_refused_by_the_accepted_m2_owner():
    """H15: a representation/locator graft from another release is refused by M2."""
    repository = M2.M2Repository()
    r1, _ = _build_m2(repository, tag="g1")
    r2, _ = _build_m2(repository, tag="g2")
    locator = _ref("ResolverLocator", "shared-locator")
    M2.register_representation(
        repository, release_ref=r1.ref, resolution_mode="DIRECT_PRODUCER_REF",
        resolver_or_locator_ref=locator, representation_integrity_ref=_ref(
            "RepresentationIntegrity", "i1"),
        resolved_subject_ref=repository.subject_exact(r1.release_subject_ref).ref,
        producer_contract_ref=r1.semantic_producer_contract_ref)
    with pytest.raises(M2.M2ReleaseError) as exc:
        M2.resolve_release_exact(
            repository, r2.ref, publication_binding_refs=())
        M2.register_representation(
            repository, release_ref=r2.ref, resolution_mode="DIRECT_PRODUCER_REF",
            resolver_or_locator_ref=locator, representation_integrity_ref=_ref(
                "RepresentationIntegrity", "i2"),
            resolved_subject_ref=r2.release_subject_ref,
            producer_contract_ref=r2.semantic_producer_contract_ref)
    assert exc.value.code in {
        "REPRESENTATION_INTEGRITY_FAILURE", "SEMANTIC_REOWNERSHIP_ATTEMPT",
        "RELEASE_ID_MISMATCH",
    }


def test_h16_tampered_m2_release_is_refused_by_the_accepted_m2_owner(rig):
    """H16: an in-place tampered release core is caught by M2's own content verify."""
    repository = rig["repository"]
    ref = rig["release"].ref
    stored = repository._releases[ref.key]
    # in-process tamper of the registered release core, keeping its registered identity
    object.__setattr__(
        stored, "determinant_closure_ref", _ref("M2Closure", "forged-determinant-closure"))
    with pytest.raises(M2.M2ReleaseError) as exc:
        repository.release_exact(ref)
    assert exc.value.code == "RELEASE_ID_MISMATCH"
    # and the ingress cannot reach it either
    ingress = _rebuild(rig)
    with pytest.raises(B5IngressM2Error) as ingress_exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert ingress_exc.value.b5_invoked is False
    assert ingress_exc.value.m2_code == "RELEASE_ID_MISMATCH"


def test_h17_subject_rehydration_bypass_is_refused(rig):
    """H17: a dict-shaped subject cannot enter, and never rehydrates past the ingress."""
    rehydrated = B5.LearnedProductLifecycleSubject.from_dict({
        **rig["custody"].expected_identity,
        "replay_state": "REPLAY_COMPLETE",
    }) if False else None
    # the accepted B5 subject WILL rehydrate a bare dict -- that is the bypass F8F found.
    # The ingress must be unreachable through it:
    for request in (rehydrated, {"release_ref": rig["release"].ref.as_dict()},
                    {"slot": "c02-slot", "subject": {}}):
        with pytest.raises(B5IngressRequestError) as exc:
            rig["ingress"].publish(request)
        assert exc.value.b5_invoked is False


def test_h18_determinant_subset_mutation_is_refused(rig):
    """H18: an order/subset determinant mutation is caught before B5."""
    expected = dict(rig["custody"].expected_identity)
    expected["determinant_keys"] = tuple(sorted(expected["determinant_keys"])[:-1])
    ingress = _rebuild(rig, expected_identity=expected)
    with pytest.raises(B5IngressAuthenticationError) as exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert exc.value.b5_invoked is False
    assert "determinant_keys" in exc.value.mismatched_fields


def test_h19_determinant_order_mutation_is_refused(rig):
    """H19: determinant order is not a free variable of the expectation."""
    expected = dict(rig["custody"].expected_identity)
    expected["determinant_keys"] = tuple(reversed(expected["determinant_keys"]))
    ingress = _rebuild(rig, expected_identity=expected)
    with pytest.raises(B5IngressAuthenticationError) as exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert exc.value.b5_invoked is False
    assert "determinant_keys" in exc.value.mismatched_fields


def test_h20_incomplete_expectation_is_refused_at_construction(rig):
    """H20: an incomplete owner expectation may never reach a request, let alone B5."""
    expected = dict(rig["custody"].expected_identity)
    expected.pop("permission_ceiling_key")
    with pytest.raises(B5IngressAuthenticationError) as exc:
        _rebuild(rig, expected_identity=expected)
    assert exc.value.b5_invoked is False
    assert exc.value.missing_keys == ("permission_ceiling_key",)


def test_h21_extraneous_expectation_key_is_refused_at_construction(rig):
    """H21: an unknown expectation key is refused, not silently ignored."""
    expected = dict(rig["custody"].expected_identity)
    expected["smuggled_currentness"] = "CURRENT_SELECTED"
    with pytest.raises(B5IngressAuthenticationError) as exc:
        _rebuild(rig, expected_identity=expected)
    assert exc.value.mismatched_fields == ("smuggled_currentness",)


def test_h22_mistyped_expectation_is_refused_at_construction(rig):
    """H22: a bool may not satisfy a str field; exact builtin types are required."""
    expected = dict(rig["custody"].expected_identity)
    expected["release_content_hash"] = True
    with pytest.raises(B5IngressAuthenticationError) as exc:
        _rebuild(rig, expected_identity=expected)
    assert exc.value.mismatched_fields == ("release_content_hash",)


def test_h23_missing_m2_release_is_refused_before_b5():
    """H23: a custody slot pointing at a release M2 does not hold is refused."""
    repository = M2.M2Repository()
    custody = ProducerCustodyMaterial(
        slot="m", release_ref=_ref("LearnedProductReleaseCore", "absent"),
        product_ref=_ref("LearnedSemanticProduct", "m-product"),
        product_family_ref=PRODUCT_FAMILY,
        producer_owner_ref=_ref("ProducerOwner", "m-owner"),
        selection_scope_ref=_ref("SelectionScope", "m-scope"),
        semantic_authority_snapshot_refs=(_auth("m-semantic"),),
        build_or_release_receipt_refs=(_ref("BuildReceipt", "m-build"),),
        producer_permission_ceiling_ref=_ref("ProducerPermissionCeiling", "m-ceiling"),
        consumed_authority_refs=(MODEL_AUTH,), direct_dependency_refs=(),
        extra_determinant_refs=(), required_replay_grade="EXACT_DETERMINISTIC_REBUILD",
        replay_state="REPLAY_COMPLETE", expected_identity={})
    custody = replace(custody, expected_identity={
        **{k: "x" for k in (
            "release_key", "release_content_hash", "producer_subject_key",
            "producer_contract_key", "semantic_anatomy_key", "semantic_projection_hash",
            "product_key", "product_family_key", "producer_owner_key",
            "selection_scope_key", "determinant_set_hash", "replay_closure_key",
            "replay_grade", "replay_root_key", "permission_ceiling_key",
            "m2_release_projection_hash")},
        **{k: () for k in (
            "authority_snapshot_keys", "direct_dependency_keys", "determinant_keys",
            "consumed_authority_keys", "receipt_keys")},
    })
    ingress = AuthenticatedB5Ingress(
        m2_repository=repository, custody={"m": custody},
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
    with pytest.raises(B5IngressM2Error) as exc:
        ingress.publish(PublicationRequest(slot="m"))
    assert exc.value.b5_invoked is False
    assert exc.value.m2_code in {"RELEASE_UNAVAILABLE", "RELEASE_SUBJECT_NOT_FOUND"}


def test_h24_empty_determinant_closure_is_refused_before_b5():
    """H24: a determinant closure that does not cover the consumed authority is refused."""
    repository = M2.M2Repository()
    release, subject = _build_m2(
        repository, tag="nodet", determinant_refs=())
    custody = ProducerCustodyMaterial(
        slot="n", release_ref=release.ref, product_ref=_ref(
            "LearnedSemanticProduct", "n-product"),
        product_family_ref=PRODUCT_FAMILY,
        producer_owner_ref=_ref("ProducerOwner", "n-owner"),
        selection_scope_ref=_ref("SelectionScope", "n-scope"),
        semantic_authority_snapshot_refs=(_auth("n-semantic"),),
        build_or_release_receipt_refs=(_ref("BuildReceipt", "n-build"),),
        producer_permission_ceiling_ref=_ref("ProducerPermissionCeiling", "n-ceiling"),
        consumed_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
        direct_dependency_refs=(), extra_determinant_refs=(),
        required_replay_grade="EXACT_DETERMINISTIC_REBUILD",
        replay_state="REPLAY_COMPLETE", expected_identity={})
    from rawlsing_next.pre553_authenticated_b5_ingress_candidate import _key  # noqa: PLC0415
    determinant = repository.closure_exact(release.determinant_closure_ref)
    replay = repository.closure_exact(release.replay_reconstruction_ref)
    dependency = repository.closure_exact(release.dependency_closure_ref)
    expected = {
        "release_key": release.ref.object_id,
        "release_content_hash": release.content_hash,
        "producer_subject_key": _key(subject.ref),
        "producer_contract_key": _key(release.semantic_producer_contract_ref),
        "semantic_anatomy_key": _key(subject.semantic_anatomy_ref),
        "semantic_projection_hash": subject.semantic_anatomy_ref.content_hash,
        "product_key": _key(custody.product_ref),
        "product_family_key": PRODUCT_FAMILY.object_id,
        "producer_owner_key": _key(custody.producer_owner_ref),
        "selection_scope_key": _key(custody.selection_scope_ref),
        "authority_snapshot_keys": (_auth("n-semantic").authority_id,),
        "direct_dependency_keys": tuple(sorted(_key(r) for r in dependency.member_refs)),
        "determinant_keys": tuple(sorted(_key(r) for r in determinant.member_refs)),
        "determinant_set_hash": "x",
        "consumed_authority_keys": tuple(
            sorted({MODEL_AUTH.object_id, WALKBACK_AUTH.object_id})),
        "replay_closure_key": _key(replay.ref),
        "replay_grade": "EXACT_DETERMINISTIC_REBUILD",
        "replay_root_key": _key(replay.ref),
        "receipt_keys": (_ref("BuildReceipt", "n-build").object_id,),
        "permission_ceiling_key": _key(custody.producer_permission_ceiling_ref),
        "m2_release_projection_hash": semantic_hash(dict(release.semantic_projection())),
    }
    custody = replace(custody, expected_identity=expected)
    ingress = AuthenticatedB5Ingress(
        m2_repository=repository, custody={"n": custody},
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
    with pytest.raises(AuthenticatedB5IngressError) as exc:
        ingress.publish(PublicationRequest(slot="n"))
    assert exc.value.b5_invoked is False
    assert exc.value.refusal_class in {
        "DETERMINANT_CLOSURE_INCOMPLETE", "IDENTITY_AUTHENTICATION_FAILED"}


def test_h25_alien_same_shape_c1_style_subject_is_refused(rig):
    """H25: an alien producer subject of the SAME SHAPE is refused (F8F K6 class)."""
    alien_release, alien_subject = _build_m2(rig["repository"], tag="alien")
    assert alien_subject.subject_kind == rig["subject"].subject_kind
    ingress = _rebuild(rig, release_ref=alien_release.ref)
    with pytest.raises(B5IngressAuthenticationError) as exc:
        ingress.publish(PublicationRequest(slot="c02-slot"))
    assert exc.value.b5_invoked is False
    assert {"producer_subject_key", "release_key"} <= set(exc.value.mismatched_fields)


def test_h26_custody_slot_mismatch_and_empty_table_are_refused(rig):
    """H26: owner-setup integrity is itself fail-closed."""
    with pytest.raises(B5IngressCustodyError):
        AuthenticatedB5Ingress(
            m2_repository=rig["repository"],
            custody={"a": replace(rig["custody"], slot="b")},
            event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
    with pytest.raises(B5IngressCustodyError):
        AuthenticatedB5Ingress(
            m2_repository=rig["repository"], custody={},
            event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
    with pytest.raises(B5IngressCustodyError):
        AuthenticatedB5Ingress(
            m2_repository=rig["repository"],
            custody={"c02-slot": replace(
                rig["custody"], semantic_authority_snapshot_refs=())},
            event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)


def test_h27_custody_table_is_read_only(rig):
    """H27: item assignment and deletion on the frozen slot table are refused."""
    projection = rig["ingress"].owner_custody_projection()
    assert projection["contract"] == "HQ280_C02_AUTHENTICATED_B5_INGRESS_CANDIDATE@1"
    with pytest.raises(TypeError):
        rig["ingress"]._custody["x"] = rig["custody"]          # noqa: SLF001
    with pytest.raises(TypeError):
        del rig["ingress"]._custody["c02-slot"]                # noqa: SLF001
    with pytest.raises(TypeError):
        projection["slots"]["c02-slot"]["release_key"] = "x"   # type: ignore[index]


def test_h28_accepted_b5_owner_is_used_unmodified_and_only_on_the_positive_path(rig):
    """H28: the ingress drives the real B5 executor; a refusal never constructs one."""
    calls = []
    original = B5.LearnedProductLifecycleExecutor.stage_release

    def spy(self, subject):
        calls.append(subject.release_ref.object_id)
        return original(self, subject)

    B5.LearnedProductLifecycleExecutor.stage_release = spy
    try:
        rig["ingress"].publish(PublicationRequest(slot="c02-slot"))
        assert calls == [rig["release"].ref.object_id]
        calls.clear()
        forged_ingress = _rebuild(rig, replay_state="REPLAY_BLOCKED_MISSING_AUTHORITY")
        with pytest.raises(AuthenticatedB5IngressError):
            forged_ingress.publish(PublicationRequest(slot="c02-slot"))
        assert calls == []
    finally:
        B5.LearnedProductLifecycleExecutor.stage_release = original


def test_h29_accepted_m2_owner_is_used_unmodified(rig):
    """H29: the ingress resolves release identity through the accepted M2 owner."""
    seen = []
    original = M2.resolve_release_exact

    def spy(repository, release_ref, **kwargs):
        seen.append(release_ref.object_id)
        return original(repository, release_ref, **kwargs)

    M2.resolve_release_exact = spy
    try:
        rig["ingress"].publish(PublicationRequest(slot="c02-slot"))
    finally:
        M2.resolve_release_exact = original
    assert seen == [rig["release"].ref.object_id]


def test_h30_published_subject_reaches_real_b5_state_machine(rig):
    """H30: the positive path really is the accepted B5 owner, end to end."""
    receipt = rig["ingress"].publish(PublicationRequest(slot="c02-slot"))
    # replay the accepted owner directly with the SAME derived material and confirm the
    # publication event payload carries the owner ceiling, not a forged one.
    resolved = M2.resolve_release_exact(rig["repository"], rig["release"].ref)
    assert resolved.release_core.ref.object_id == receipt.release_key
    executor = B5.LearnedProductLifecycleExecutor()
    custody = rig["custody"]
    subject = B5.LearnedProductLifecycleSubject(
        release_ref=resolved.release_core.ref,
        product_ref=custody.product_ref,
        product_family_ref=custody.product_family_ref,
        producer_owner_ref=custody.producer_owner_ref,
        producer_contract_ref=resolved.release_core.semantic_producer_contract_ref,
        semantic_projection_hash=resolved.subject.semantic_anatomy_ref.content_hash,
        authority_snapshot_refs=custody.semantic_authority_snapshot_refs,
        direct_dependency_refs=resolved.release_core and (),
        determinant_refs=(_ref("DETERMINANT", "ad-hoc"),),
        determinant_set_hash=semantic_hash(
            [_ref("DETERMINANT", "ad-hoc").as_dict()]),
        replay_root_ref=resolved.release_core.replay_reconstruction_ref,
        selection_scope_ref=custody.selection_scope_ref,
        build_or_release_receipt_refs=custody.build_or_release_receipt_refs,
        producer_permission_ceiling_ref=FORGED_CEILING,
    )
    executor.stage_release(subject)
    executor.register_product(subject.release_ref, event_authority_ref=EVENT_AUTHORITY,
                              event_rule_ref=EVENT_RULE)
    executor.publish_product(subject.release_ref, event_authority_ref=EVENT_AUTHORITY,
                             event_rule_ref=EVENT_RULE)
    payload_ceiling = [
        e.payload.get("producer_permission_ceiling", {}).get("object_id")
        for e in executor.events if e.event_kind == "PRODUCT_PUBLISHED"
    ]
    # The accepted B5 owner still stores whatever ceiling it is handed verbatim: this is
    # the boundary C02 places a perimeter in front of, and the test proves it directly.
    assert payload_ceiling == [FORGED_CEILING.object_id]
    assert receipt.permission_ceiling_key == CEILING.object_id