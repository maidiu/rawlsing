"""HQ280 PV3 C02R -- reviewer-authored independent hostile attacks on the C02
producer-authenticated B5 perimeter.

This script is NOT derived from C02's own suite. It attacks the candidate from the
outside: raw accepted owners, the perimeter's public surface, multi-slot custody,
revocation, checkpoint rehydration and CURRENT state.

Every case invokes real accepted owners and records the ACTUAL typed outcome.
Output: one JSON object per line on stdout, plus a summary.

Usage: python3 hostile_c02r.py <sealed_tree_root>
"""
from __future__ import annotations

import json
import subprocess
import sys
import traceback
from dataclasses import replace

ROOT = sys.argv[1]
sys.path.insert(0, ROOT)

from rawlsing_next import pre553_learned_product_lifecycle as B5  # noqa: E402
from rawlsing_next import pre553_learned_product_release as M2  # noqa: E402
from rawlsing_next import (  # noqa: E402
    pre553_authenticated_b5_ingress_candidate as C02,
)
from rawlsing_next.pre553_empirical_objects import (  # noqa: E402
    AuthorityRef,
    ExactRef,
    semantic_hash,
)

RESULTS: list[dict] = []


def emit(case: str, **fields) -> None:
    row = {"case": case, **fields}
    RESULTS.append(row)
    print(json.dumps(row, sort_keys=True, default=str), flush=True)


def ref(kind: str, tag: str) -> ExactRef:
    d = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:c02r:{kind.lower()}:{tag}:sha256:{d}", d)


def auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", "1.0.0", semantic_hash({"authority": tag}))


MODEL_AUTH = ref("ModelAuthority", "c02r-model")
WALKBACK_AUTH = ref("WalkbackAuthority", "c02r-walkback")
SEMANTIC_AUTH = auth("c02r-semantic")
PRODUCT_FAMILY = ref("ProductFamily", "c02r-family")
SELECTION_SCOPE = ref("SelectionScope", "c02r-scope")
CEILING = ref("ProducerPermissionCeiling", "c02r-ceiling")
BUILD_RECEIPT = ref("BuildReceipt", "c02r-build")
EVENT_AUTHORITY = ref("EventAuthority", "c02r-ea")
EVENT_RULE = ref("EventRule", "c02r-er")
PRODUCT_REF = ref("LearnedSemanticProduct", "c02r-product")
PRODUCER_OWNER = ref("ProducerOwner", "c02r-owner")


def build_m2(repo: M2.M2Repository, *, tag: str,
             replay_grade: str = "EXACT_DETERMINISTIC_REBUILD",
             replay_complete: bool = True,
             determinant_refs=None, authority_members=None):
    subject_ref = ref("LearnedSemanticProduct", f"{tag}-subject")
    producer_contract = ref("ProducerContract", f"{tag}-contract")
    anatomy = ref("SemanticAnatomy", f"{tag}-anatomy")
    subject = M2.register_producer_subject(
        repo,
        subject_ref=subject_ref,
        subject_kind="IMMUTABLE_LEARNED_PRODUCT",
        producer_contract_ref=producer_contract,
        typed_state="POSITIVE",
        semantic_anatomy_ref=anatomy,
        required_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
        required_replay_refs=(ref("ReplayInput", f"{tag}-replay-input"),),
    )
    authority = M2.constitute_closure(
        repo, closure_kind="AUTHORITY",
        member_refs=tuple(authority_members)
        if authority_members is not None
        else (producer_contract, MODEL_AUTH, WALKBACK_AUTH),
        complete=True,
    )
    dependency = M2.constitute_closure(
        repo, closure_kind="DEPENDENCY",
        member_refs=(ref("UpstreamProduct", f"{tag}-upstream"),), complete=True,
    )
    determinant = M2.constitute_closure(
        repo, closure_kind="DETERMINANT",
        member_refs=(MODEL_AUTH, WALKBACK_AUTH) if determinant_refs is None
        else tuple(determinant_refs),
        complete=True,
    )
    replay = M2.constitute_closure(
        repo, closure_kind="REPLAY_RECONSTRUCTION",
        member_refs=(ref("ReplayInput", f"{tag}-replay-input"),),
        complete=replay_complete, metadata={"replay_grade": replay_grade},
    )
    explanation = M2.constitute_closure(
        repo, closure_kind="EXPLANATION_LINEAGE",
        member_refs=(subject_ref, producer_contract), complete=True,
    )
    release = M2.constitute_release(
        repo,
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


def expected_identity(repo, release, subject, *, ceiling_key: str,
                      replay_grade: str = "EXACT_DETERMINISTIC_REBUILD"):
    """Owner-side expected identity, authored from real M2 output (C02 R3 mode)."""
    dependency = repo.closure_exact(release.dependency_closure_ref)
    determinant = repo.closure_exact(release.determinant_closure_ref)
    replay = repo.closure_exact(release.replay_reconstruction_ref)

    members = {r.key: r for r in determinant.member_refs}
    for r in (MODEL_AUTH, WALKBACK_AUTH):
        d = semantic_hash({"consumed_authority_key": r.object_id})
        consumed = ExactRef(
            "B5Lifecycle:CONSUMED_AUTHORITY",
            "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % d, d)
        members[consumed.key] = consumed
    d = semantic_hash({"determinant_class": "SEMANTIC_AUTHORITY_REF",
                       "authority_ref": SEMANTIC_AUTH.as_dict()})
    ad = ExactRef("B5Lifecycle:AUTHORITY_DETERMINANT",
                  "urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:%s" % d, d)
    members[ad.key] = ad
    det_refs = tuple(members[k] for k in sorted(members))

    return {
        "release_key": release.ref.object_id,
        "release_content_hash": release.content_hash,
        "producer_subject_key": subject.ref.object_id,
        "producer_contract_key": release.semantic_producer_contract_ref.object_id,
        "semantic_anatomy_key": subject.semantic_anatomy_ref.object_id,
        "semantic_projection_hash": subject.semantic_anatomy_ref.content_hash,
        "product_key": PRODUCT_REF.object_id,
        "product_family_key": PRODUCT_FAMILY.object_id,
        "producer_owner_key": PRODUCER_OWNER.object_id,
        "selection_scope_key": SELECTION_SCOPE.object_id,
        "authority_snapshot_keys": (SEMANTIC_AUTH.authority_id,),
        "direct_dependency_keys": tuple(
            sorted({r.object_id for r in dependency.member_refs})),
        "determinant_keys": tuple(sorted(r.object_id for r in det_refs)),
        "determinant_set_hash": semantic_hash([r.as_dict() for r in det_refs]),
        "consumed_authority_keys": tuple(
            sorted({MODEL_AUTH.object_id, WALKBACK_AUTH.object_id})),
        "replay_closure_key": replay.ref.object_id,
        "replay_grade": replay_grade,
        "replay_root_key": replay.ref.object_id,
        "receipt_keys": (BUILD_RECEIPT.object_id,),
        "permission_ceiling_key": ceiling_key,
        "m2_release_projection_hash": semantic_hash(dict(release.semantic_projection())),
    }


def custody_for(repo, release, subject, *, slot: str, ceiling=CEILING,
                replay_grade="EXACT_DETERMINISTIC_REBUILD",
                ceiling_key=None, **overrides):
    base = dict(
        slot=slot,
        release_ref=release.ref,
        product_ref=PRODUCT_REF,
        product_family_ref=PRODUCT_FAMILY,
        producer_owner_ref=PRODUCER_OWNER,
        selection_scope_ref=SELECTION_SCOPE,
        semantic_authority_snapshot_refs=(SEMANTIC_AUTH,),
        build_or_release_receipt_refs=(BUILD_RECEIPT,),
        producer_permission_ceiling_ref=ceiling,
        consumed_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
        direct_dependency_refs=(),
        extra_determinant_refs=(),
        required_replay_grade=replay_grade,
        replay_state="REPLAY_COMPLETE",
        expected_identity=expected_identity(
            repo, release, subject,
            ceiling_key=ceiling_key if ceiling_key is not None else ceiling.object_id,
            replay_grade=replay_grade),
    )
    base.update(overrides)
    return C02.ProducerCustodyMaterial(**base)


def ingress_for(repo, custody_map, revocations=None):
    return C02.AuthenticatedB5Ingress(
        m2_repository=repo,
        custody=custody_map,
        revocations=revocations or C02.RevocationLedger(),
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
    )


def genuine_rig(tag="base", *, replay_grade="EXACT_DETERMINISTIC_REBUILD",
                replay_complete=True, determinant_refs=None):
    repo = M2.M2Repository()
    release, subject = build_m2(repo, tag=tag, replay_grade=replay_grade,
                                replay_complete=replay_complete,
                                determinant_refs=determinant_refs)
    custody = custody_for(repo, release, subject, slot=f"{tag}-slot",
                          replay_grade=replay_grade)
    return repo, release, subject, custody


def b5_subject_from_m2(repo, release, subject, *, replay_state="REPLAY_COMPLETE"):
    """Build an accepted-B5 subject directly from real M2 output (caller side)."""
    dependency = repo.closure_exact(release.dependency_closure_ref)
    determinant = repo.closure_exact(release.determinant_closure_ref)
    replay = repo.closure_exact(release.replay_reconstruction_ref)

    members = {r.key: r for r in determinant.member_refs}
    for r in (MODEL_AUTH, WALKBACK_AUTH):
        d = semantic_hash({"consumed_authority_key": r.object_id})
        consumed = ExactRef(
            "B5Lifecycle:CONSUMED_AUTHORITY",
            "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % d, d)
        members[consumed.key] = consumed
    d = semantic_hash({"determinant_class": "SEMANTIC_AUTHORITY_REF",
                       "authority_ref": SEMANTIC_AUTH.as_dict()})
    ad = ExactRef("B5Lifecycle:AUTHORITY_DETERMINANT",
                  "urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:%s" % d, d)
    members[ad.key] = ad
    det_refs = tuple(members[k] for k in sorted(members))
    direct = tuple(
        {r.key: r for r in dependency.member_refs}[k]
        for k in sorted({r.key: r for r in dependency.member_refs})
    )
    return B5.LearnedProductLifecycleSubject(
        release_ref=release.ref,
        product_ref=PRODUCT_REF,
        product_family_ref=PRODUCT_FAMILY,
        producer_owner_ref=PRODUCER_OWNER,
        producer_contract_ref=release.semantic_producer_contract_ref,
        semantic_projection_hash=subject.semantic_anatomy_ref.content_hash,
        authority_snapshot_refs=(SEMANTIC_AUTH,),
        direct_dependency_refs=direct,
        determinant_refs=det_refs,
        determinant_set_hash=semantic_hash([r.as_dict() for r in det_refs]),
        replay_root_ref=replay.ref,
        selection_scope_ref=SELECTION_SCOPE,
        build_or_release_receipt_refs=(BUILD_RECEIPT,),
        producer_permission_ceiling_ref=CEILING,
        replay_state=replay_state,
        materialization_class="MANDATORY_RETAINED_CAPITAL",
    )


def direct_executor_publish(subject):
    """The F8F K4 route: raw accepted B5 executor, caller-built subject."""
    ex = B5.LearnedProductLifecycleExecutor()
    ex.stage_release(subject)
    ex.register_product(subject.release_ref, event_authority_ref=EVENT_AUTHORITY,
                        event_rule_ref=EVENT_RULE)
    ev = ex.publish_product(subject.release_ref, event_authority_ref=EVENT_AUTHORITY,
                            event_rule_ref=EVENT_RULE)
    return ex, ev


# ===========================================================================
# A. BASELINE: the candidate's own positive path really works
# ===========================================================================
repo, release, subject, custody = genuine_rig("base")
ingress = ingress_for(repo, {custody.slot: custody})
try:
    receipt = ingress.publish(C02.PublicationRequest(slot=custody.slot))
    emit("A1_perimeter_positive", published=True,
         release_key=receipt.release_key,
         current_selection_performed=receipt.current_selection_performed,
         authorizing=receipt.authorizing, grant=receipt.grant, g0b=receipt.g0b,
         g1_service=receipt.g1_service,
         scientific_claim=receipt.scientific_competence_claim)
except Exception as exc:  # noqa: BLE001
    emit("A1_perimeter_positive", published=False, exception=type(exc).__name__,
         message=str(exc)[:200])

# ===========================================================================
# B. THE PERIMETER IS BYPASSABLE: raw accepted B5 executor, no perimeter
# ===========================================================================
repo2, release2, subject2, custody2 = genuine_rig("raw")
forged = b5_subject_from_m2(repo2, release2, subject2, replay_state="REPLAY_COMPLETE")
try:
    ex2, _ev = direct_executor_publish(forged)
    state = ex2.lifecycle_state(forged.release_ref)
    emit("B1_raw_executor_k4_bypass", bypassed=True,
         publication=state.publication,
         event_kinds=[e.event_kind for e in ex2.events],
         perimeter_consulted=False,
         note="accepted B5 reached directly; C02 perimeter never called")
except Exception as exc:  # noqa: BLE001
    emit("B1_raw_executor_k4_bypass", bypassed=False,
         exception=type(exc).__name__, message=str(exc)[:200])

# B2: full K4+K5 forgery -- forged replay_state, ceiling, receipts, replay root
repo3, release3, subject3, custody3 = genuine_rig("k5")
fake_ceiling = ExactRef("ProducerPermissionCeiling",
                        "urn:c02r:PRODUCTION_GRANT", semantic_hash({"prod": True}))
fake_receipt = ExactRef("BuildReceipt", "urn:c02r:fake-receipt",
                        semantic_hash({"fake": 1}))
fake_root = ExactRef("ReplayRoot", "urn:c02r:fake-root", semantic_hash({"fake": 2}))
fully_forged = replace(
    b5_subject_from_m2(repo3, release3, subject3),
    producer_permission_ceiling_ref=fake_ceiling,
    build_or_release_receipt_refs=(fake_receipt,),
    replay_root_ref=fake_root,
)
try:
    ex3, _ = direct_executor_publish(fully_forged)
    state3 = ex3.lifecycle_state(fully_forged.release_ref)
    stored = ex3._subject(fully_forged.release_ref).producer_permission_ceiling_ref.key
    emit("B2_raw_executor_full_k5_forgery_bypass", bypassed=True,
         publication=state3.publication,
         event_kinds=[e.event_kind for e in ex3.events],
         stored_ceiling=stored,
         ceiling_is_forged=(stored == fake_ceiling.key))
except Exception as exc:  # noqa: BLE001
    emit("B2_raw_executor_full_k5_forgery_bypass", bypassed=False,
         exception=type(exc).__name__, message=str(exc)[:200])

# B3: CURRENT_SELECTED through the raw executor on a forged subject. Uses an
# honestly replayed subject for publication, then a forged one for selection.
repo3b, release3b, subject3b, custody3b = genuine_rig("current")
try:
    honest = b5_subject_from_m2(repo3b, release3b, subject3b)
    forged_sel = replace(honest, producer_permission_ceiling_ref=fake_ceiling,
                         replay_root_ref=fake_root)
    ex4 = B5.LearnedProductLifecycleExecutor()
    ex4.stage_release(forged_sel)
    ex4.register_product(forged_sel.release_ref, event_authority_ref=EVENT_AUTHORITY,
                         event_rule_ref=EVENT_RULE)
    ex4.publish_product(forged_sel.release_ref, event_authority_ref=EVENT_AUTHORITY,
                        event_rule_ref=EVENT_RULE)
    key = ex4.selection_key(
        product_family_ref=PRODUCT_FAMILY, selection_scope_ref=SELECTION_SCOPE,
        selection_purpose_ref=ref("SelectionPurpose", "c02r-purpose"),
    )
    ex4.select_current(
        key.ref, forged_sel.release_ref,
        expected_previous_receipt_ref=None,
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
        selection_attestation_ref=ref("SelectionAttestation", "c02r-att"),
    )
    state4 = ex4.lifecycle_state(forged_sel.release_ref)
    emit("B3_raw_executor_current_selection_bypass", bypassed=True,
         publication=state4.publication,
         event_kinds=[e.event_kind for e in ex4.events],
         perimeter_consulted=False)
except Exception as exc:  # noqa: BLE001
    emit("B3_raw_executor_current_selection_bypass", bypassed=False,
         exception=type(exc).__name__, message=str(exc)[:250])

# ===========================================================================
# C. EXPECTATION IS DERIVED FROM THE SAME CONSTRUCTION (R3 made executable)
# ===========================================================================
# C1: mutate the LIVE M2 repository closure after the ingress was built. The
# expectation captured the closure at AUTHORING time, so drift is detected --
# but that is a snapshot check, NOT producer authenticity.
repoC, releaseC, subjectC, custodyC = genuine_rig("mutate")
ingressC = ingress_for(repoC, {custodyC.slot: custodyC})
det_c = repoC.closure_exact(releaseC.determinant_closure_ref)
extra = ref("InjectedEdge", "c02r-injected")
try:
    object.__setattr__(det_c, "member_refs", tuple(det_c.member_refs) + (extra,))
    try:
        ingressC.publish(C02.PublicationRequest(slot=custodyC.slot))
        emit("C1a_post_authoring_repo_mutation", detected=False, published=True,
             note="mutated closure still admitted")
    except C02.AuthenticatedB5IngressError as exc:
        emit("C1a_post_authoring_repo_mutation", detected=True, published=False,
             refusal_class=exc.refusal_class,
             mismatched=getattr(exc, "mismatched_fields", None))
except Exception as exc:  # noqa: BLE001
    emit("C1a_post_authoring_repo_mutation", mutated=False,
         exception=type(exc).__name__, message=str(exc)[:200])

# C2: the same mutated repository, with the expectation RE-AUTHORED from it.
# The perimeter admits the injected material: its "authentication" re-derives the
# expected side from the very construction it authenticates (C02's own R3).
repoC2, releaseC2, subjectC2, _ = genuine_rig("mutate2")
det_c2 = repoC2.closure_exact(releaseC2.determinant_closure_ref)
try:
    object.__setattr__(det_c2, "member_refs", tuple(det_c2.member_refs) + (extra,))
    custodyC2 = custody_for(repoC2, releaseC2, subjectC2, slot="mutate2-slot")
    ingressC2 = ingress_for(repoC2, {custodyC2.slot: custodyC2})
    r = ingressC2.publish(C02.PublicationRequest(slot="mutate2-slot"))
    emit("C2_reauthorized_mutation_admitted", admitted=True,
         injected_edge_present=any(extra.object_id in k for k in r.determinant_keys),
         determinant_count=len(r.determinant_keys),
         note="expectation authored from mutated construction; tautology admits it")
except C02.AuthenticatedB5IngressError as exc:
    emit("C2_reauthorized_mutation_admitted", admitted=False,
         refusal_class=exc.refusal_class,
         mismatched=getattr(exc, "mismatched_fields", None))
except Exception as exc:  # noqa: BLE001
    emit("C2_reauthorized_mutation_admitted", admitted=None,
         exception=type(exc).__name__, message=str(exc)[:250])

# C3: shared ref object class (residual R4 note: ExactRef is frozen but shared)
emit("C3_shared_ref_class", ref_type=type(subjectC.semantic_anatomy_ref).__name__,
     frozen=type(subjectC.semantic_anatomy_ref).__dataclass_params__.frozen,
     note="ExactRef frozen dataclass; in-process principal can bypass with "
          "object.__setattr__, and the M2Repository itself is never frozen")

# ===========================================================================
# D. M2 'CONTENT VERIFICATION' PROVES WELL-FORMEDNESS, NOT PRODUCER ISSUANCE
# ===========================================================================
# D1: an attacker-authored release, minted through the PUBLIC M2 owner API, is
# published by the perimeter. Nothing binds it to a producer.
repoE = M2.M2Repository()
attacker_release, attacker_subject = build_m2(repoE, tag="attacker-minted")
attacker_custody = custody_for(repoE, attacker_release, attacker_subject,
                               slot="attacker-slot")
attacker_ingress = ingress_for(repoE, {attacker_custody.slot: attacker_custody})
try:
    r = attacker_ingress.publish(C02.PublicationRequest(slot="attacker-slot"))
    emit("D1_attacker_minted_release_published", published=True,
         release_key=r.release_key,
         release_content_hash=r.release_content_hash,
         producer_subject_key=r.producer_subject_key,
         note="caller-authored M2 release minted via public M2 API; perimeter "
              "authenticates it as 'producer-issued' with no issuer in existence")
except Exception as exc:  # noqa: BLE001
    emit("D1_attacker_minted_release_published", published=False,
         exception=type(exc).__name__, message=str(exc)[:200])

# D2: does M2 verify stored content against the ref's content_hash on resolution?
repoF = M2.M2Repository()
relF, subF = build_m2(repoF, tag="tamper")
tamper_result = {"attempted": True}
try:
    core = repoF.release(relF.ref) if hasattr(repoF, "release") else None
    tamper_result["release_attr"] = type(core).__name__ if core is not None else None
except Exception as exc:  # noqa: BLE001
    tamper_result["lookup_exception"] = type(exc).__name__
    tamper_result["message"] = str(exc)[:200]
# Try a ref whose content_hash does not match the stored release content
mismatched = ExactRef(relF.ref.kind, relF.ref.object_id, semantic_hash({"not": "the-release"}))
try:
    res = M2.resolve_release_exact(repoF, mismatched, publication_binding_refs=())
    tamper_result["mismatched_ref_resolved"] = True
    tamper_result["resolved_content_hash"] = res.release_core.content_hash
except Exception as exc:  # noqa: BLE001
    tamper_result["mismatched_ref_resolved"] = False
    tamper_result["mismatched_exception"] = type(exc).__name__
    tamper_result["mismatched_message"] = str(exc)[:200]
emit("D2_m2_content_binding_probe", **tamper_result)

# ===========================================================================
# E. REVOCATION, RELEASE REVOCATION, STALE/GRADE GATES
# ===========================================================================
repoG, releaseG, subjectG, custodyG = genuine_rig("revoke")
for name, rev, expect in (
    ("E1_release_revoked", C02.RevocationLedger(release_keys=frozenset({releaseG.ref.object_id})), "RELEASE"),
    ("E2_authority_revoked", C02.RevocationLedger(authority_keys=frozenset({SEMANTIC_AUTH.authority_id})), "AUTHORITY"),
    ("E3_consumed_authority_revoked", C02.RevocationLedger(authority_keys=frozenset({MODEL_AUTH.object_id})), "CONSUMED"),
):
    ing = ingress_for(repoG, {custodyG.slot: custodyG}, rev)
    try:
        ing.publish(C02.PublicationRequest(slot=custodyG.slot))
        emit(name, refused=False, published=True, expected_class=expect)
    except C02.AuthenticatedB5IngressError as exc:
        emit(name, refused=True, refusal_class=exc.refusal_class,
             b5_invoked=getattr(exc, "b5_invoked", None), expected_class=expect)
    except Exception as exc:  # noqa: BLE001
        emit(name, refused=False, exception=type(exc).__name__, message=str(exc)[:200])

# E4: revoked authority that is NOT consumed and NOT a semantic snapshot ref
unrelated_rev = C02.RevocationLedger(
    authority_keys=frozenset({ref("ModelAuthority", "unrelated").object_id}))
ing = ingress_for(repoG, {custodyG.slot: custodyG}, unrelated_rev)
try:
    r = ing.publish(C02.PublicationRequest(slot=custodyG.slot))
    emit("E4_unrelated_revocation_ignored", published=True,
         note="correct: exactness only, unrelated ref does not block")
except Exception as exc:  # noqa: BLE001
    emit("E4_unrelated_revocation_ignored", published=False,
         exception=type(exc).__name__, message=str(exc)[:200])

# E5: required replay grade mismatch
repoH, releaseH, subjectH, _ = genuine_rig(
    "grade", replay_grade="HISTORICAL_EXPLANATION_ONLY")
custodyH = custody_for(repoH, releaseH, subjectH, slot="grade-slot",
                       replay_grade="EXACT_DETERMINISTIC_REBUILD")
ingH = ingress_for(repoH, {custodyH.slot: custodyH})
try:
    ingH.publish(C02.PublicationRequest(slot="grade-slot"))
    emit("E5_grade_mismatch", refused=False, published=True)
except C02.AuthenticatedB5IngressError as exc:
    emit("E5_grade_mismatch", refused=True, refusal_class=exc.refusal_class,
         b5_invoked=getattr(exc, "b5_invoked", None))

# ===========================================================================
# F. MULTI-SLOT SUBSTITUTION / CROSS-SLOT CLAIMS
# ===========================================================================
repoI = M2.M2Repository()
rel1, sub1 = build_m2(repoI, tag="slot1")
rel2, sub2 = build_m2(repoI, tag="slot2")
c1 = custody_for(repoI, rel1, sub1, slot="s1")
c2 = custody_for(repoI, rel2, sub2, slot="s2")
ingI = ingress_for(repoI, {"s1": c1, "s2": c2})
try:
    r1 = ingI.publish(C02.PublicationRequest(slot="s1"))
    r2 = ingI.publish(C02.PublicationRequest(slot="s2"))
    emit("F1_two_slots_independent", ok=True, r1_release=r1.release_key,
         r2_release=r2.release_key, distinct=r1.release_key != r2.release_key,
         note="receipts bind their own slot's release")
except Exception as exc:  # noqa: BLE001
    emit("F1_two_slots_independent", ok=False, exception=type(exc).__name__,
         message=str(exc)[:200])

# F2: custody whose expected_identity was authored for the OTHER slot's release
try:
    swapped = replace(c1, expected_identity=c2.expected_identity)
    ing_sw = ingress_for(repoI, {"s1": swapped})
    ing_sw.publish(C02.PublicationRequest(slot="s1"))
    emit("F2_cross_slot_expectation", admitted=True,
         note="BUG: cross-slot expectation admitted")
except C02.AuthenticatedB5IngressError as exc:
    emit("F2_cross_slot_expectation", admitted=False, refusal_class=exc.refusal_class,
         mismatched=getattr(exc, "mismatched_fields", None)[:6]
         if getattr(exc, "mismatched_fields", None) else None)
except Exception as exc:  # noqa: BLE001
    emit("F2_cross_slot_expectation", admitted=None, exception=type(exc).__name__,
         message=str(exc)[:200])

# ===========================================================================
# G. REQUEST SURFACE + PERMISSION CEILING
# ===========================================================================
repoJ, releaseJ, subjectJ, custodyJ = genuine_rig("surface")
ingJ = ingress_for(repoJ, {custodyJ.slot: custodyJ})
fake_req_ceiling = ExactRef("ProducerPermissionCeiling",
                            "urn:c02r:PRODUCTION_GRANT", semantic_hash({"prod": True}))
surfaces = {
    "G1_caller_subject_field": {"slot": custodyJ.slot, "subject": subjectJ},
    "G2_caller_ceiling_field": {"slot": custodyJ.slot,
                                "producer_permission_ceiling_ref": fake_req_ceiling},
    "G3_caller_currentness_field": {"slot": custodyJ.slot, "select_current": True},
    "G4_plain_string": custodyJ.slot,
    "G5_attacker_dataclass": type("Evil", (), {"slot": custodyJ.slot})(),
}
for name, payload in surfaces.items():
    try:
        ingJ.publish(payload)
        emit(name, refused=False, admitted=True)
    except C02.AuthenticatedB5IngressError as exc:
        emit(name, refused=True, refusal_class=exc.refusal_class,
             b5_invoked=getattr(exc, "b5_invoked", None))
    except Exception as exc:  # noqa: BLE001
        emit(name, refused=False, exception=type(exc).__name__, message=str(exc)[:160])

# G6: the permission ceiling is never validated, only compared to itself
repoK = M2.M2Repository()
relK, subK = build_m2(repoK, tag="ceiling")
fake_ceiling_k = ExactRef("ProducerPermissionCeiling",
                          "urn:c02r:TOTAL_CONTROL", semantic_hash({"all": True}))
custodyK = custody_for(repoK, relK, subK, slot="ceil-slot", ceiling=fake_ceiling_k)
ingK = ingress_for(repoK, {custodyK.slot: custodyK})
try:
    r = ingK.publish(C02.PublicationRequest(slot="ceil-slot"))
    emit("G6_arbitrary_ceiling_accepted", published=True,
         ceiling_key=r.permission_ceiling_key,
         note="owner custody may declare ANY ceiling; nothing validates it")
except Exception as exc:  # noqa: BLE001
    emit("G6_arbitrary_ceiling_accepted", published=False,
         exception=type(exc).__name__, message=str(exc)[:200])

# ===========================================================================
# H. CHECKPOINT REHYDRATION: forged hash, self-consistent payload
# ===========================================================================
repoL, releaseL, subjectL, custodyL = genuine_rig("ckpt")
ingL = ingress_for(repoL, {custodyL.slot: custodyL})
try:
    r = ingL.publish(C02.PublicationRequest(slot=custodyL.slot))
    emit("H0_perimeter_publish_for_checkpoint", published=True,
         publication_event_key=r.publication_event_key)
except Exception as exc:  # noqa: BLE001
    emit("H0_perimeter_publish_for_checkpoint", published=False,
         exception=type(exc).__name__, message=str(exc)[:200])

# H1: hand-authored checkpoint payload, hash recomputed by the caller.
# Here the payload is round-tripped but the HASH is caller-computed; the check is
# self-referential (checkpoint_hash == semantic_hash(payload)).
try:
    ex_build = B5.LearnedProductLifecycleExecutor()
    ex_build.stage_release(b5_subject_from_m2(repoL, releaseL, subjectL))
    ex_build.register_product(releaseL.ref, event_authority_ref=EVENT_AUTHORITY,
                              event_rule_ref=EVENT_RULE)
    ex_build.publish_product(releaseL.ref, event_authority_ref=EVENT_AUTHORITY,
                             event_rule_ref=EVENT_RULE)
    ckpt = ex_build.export_checkpoint()
    payload = ckpt["checkpoint_payload"]
    evil_payload = json.loads(json.dumps(payload))
    evil_ckpt = {"checkpoint_payload": evil_payload,
                 "checkpoint_hash": semantic_hash(evil_payload)}
    ex_re = B5.LearnedProductLifecycleExecutor.from_checkpoint(evil_ckpt)
    emit("H1_checkpoint_self_hash", rehydrated=True,
         n_subjects=len(ex_re._repository_subjects),
         hash_is_self_referential=True,
         note="checkpoint_hash == semantic_hash(payload); a caller who can supply "
              "the checkpoint controls the hash, so the check cannot authenticate it")
except Exception as exc:  # noqa: BLE001
    emit("H1_checkpoint_self_hash", rehydrated=False, exception=type(exc).__name__,
         message=str(exc)[:250])

# H2: caller-authored checkpoint that rehydrates to CURRENT_SELECTED WITHOUT the
# perimeter. The payload is assembled from a genuinely selected executor and a
# caller-chosen attestation, then the caller computes the hash itself.
try:
    ex_sel = B5.LearnedProductLifecycleExecutor()
    subj_sel = b5_subject_from_m2(repoL, releaseL, subjectL)
    ex_sel.stage_release(subj_sel)
    ex_sel.register_product(releaseL.ref, event_authority_ref=EVENT_AUTHORITY,
                            event_rule_ref=EVENT_RULE)
    ex_sel.publish_product(releaseL.ref, event_authority_ref=EVENT_AUTHORITY,
                           event_rule_ref=EVENT_RULE)
    key_sel = ex_sel.selection_key(
        product_family_ref=PRODUCT_FAMILY, selection_scope_ref=SELECTION_SCOPE,
        selection_purpose_ref=ref("SelectionPurpose", "c02r-ckpt-purpose"))
    ex_sel.select_current(
        key_sel.ref, releaseL.ref, expected_previous_receipt_ref=None,
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
        selection_attestation_ref=ref("SelectionAttestation", "c02r-ckpt-att"))
    ckpt_sel = ex_sel.export_checkpoint()
    p2 = json.loads(json.dumps(ckpt_sel["checkpoint_payload"]))
    caller_ckpt = {"checkpoint_payload": p2, "checkpoint_hash": semantic_hash(p2)}
    ex_re2 = B5.LearnedProductLifecycleExecutor.from_checkpoint(caller_ckpt)
    state_re = ex_re2.lifecycle_state(releaseL.ref)
    sel_kinds = [e.event_kind for e in ex_re2.events]
    emit("H2_checkpoint_rehydrates_current", rehydrated=True,
         publication=state_re.publication,
         current_selected_event_present=("CURRENT_SELECTED" in sel_kinds),
         perimeter_consulted=False,
         note="caller-computed checkpoint hash accepted; rehydration path bypasses "
              "the perimeter entirely")
except Exception as exc:  # noqa: BLE001
    emit("H2_checkpoint_rehydrates_current", rehydrated=False,
         exception=type(exc).__name__, message=str(exc)[:250])

# H3: is there ANY accepted producer credential / signature / key verification
# in the sealed tree? (narrow pattern; the broad "signature" word appears in
# unrelated governance modules, so the probe is deliberately specific)
grep = subprocess.run(
    ["grep", "-rlE",
     "def verify_signature|public_key|private_key|hmac\\.|keyring|"
     "credential_store|producer_credential|signing_key|"
     "verify_producer_signature|issuer_credential",
     f"{ROOT}/rawlsing_next"],
    capture_output=True, text=True)
hits = [h.replace(ROOT + "/", "") for h in grep.stdout.split() if h.strip()]
m2_issuer = subprocess.run(
    ["grep", "-cE", "issuer|credential|signature|authoriz",
     f"{ROOT}/rawlsing_next/pre553_learned_product_release.py"],
    capture_output=True, text=True)
emit("H3_issuer_or_crypto_search", verification_modules=len(hits),
     unresolved_hits=hits[:8],
     m2_issuer_credential_lines=(m2_issuer.stdout.strip() or "0"),
     note="no accepted producer credential, signature scheme or issuer exists; "
          "M2 registration is unauthenticated by construction")

# ===========================================================================
# I. EXTERNAL/OTHER-PROCESS REHYDRATION VIA THE PERIMETER
# ===========================================================================
repoM, releaseM, subjectM, custodyM = genuine_rig("xproc")
ingM = ingress_for(repoM, {custodyM.slot: custodyM})
try:
    r1 = ingM.publish(C02.PublicationRequest(slot=custodyM.slot))
    r2 = ingM.publish(C02.PublicationRequest(slot=custodyM.slot))
    emit("I1_repeated_publish_same_ingress", both_published=True,
         same_publication_event=(r1.publication_event_key == r2.publication_event_key))
except Exception as exc:  # noqa: BLE001
    emit("I1_repeated_publish_same_ingress", both_published=False,
         exception=type(exc).__name__, message=str(exc)[:200])

# I2: fresh ingress over the SAME M2 repo (models restart/rehydrate)
try:
    ingM2 = ingress_for(repoM, {custodyM.slot: custodyM})
    r3 = ingM2.publish(C02.PublicationRequest(slot=custodyM.slot))
    emit("I2_fresh_ingress_same_repo", published=True,
         publication_event_key=r3.publication_event_key,
         deterministic=True)
except Exception as exc:  # noqa: BLE001
    emit("I2_fresh_ingress_same_repo", published=False,
         exception=type(exc).__name__, message=str(exc)[:200])

# ===========================================================================
# J. INCOMPLETE / EMPTY / EXTRA EXPECTATION KEYS (fail-closed gate)
# ===========================================================================
repoN, releaseN, subjectN, custodyN = genuine_rig("incomplete")
for name, mutate in (
    ("J1_empty_expectation", lambda e: {}),
    ("J2_dropped_key", lambda e: {k: v for k, v in e.items()
                                  if k != "permission_ceiling_key"}),
    ("J3_extra_key", lambda e: {**e, "extra_unknown_key": "x"}),
    ("J4_bool_for_str", lambda e: {**e, "release_key": True}),
):
    bad = mutate(dict(custodyN.expected_identity))
    try:
        c = replace(custodyN, expected_identity=bad)
        ingress_for(repoN, {c.slot: c})
        emit(name, refused=False, constructed=True)
    except C02.AuthenticatedB5IngressError as exc:
        emit(name, refused=True, refusal_class=exc.refusal_class,
             missing=getattr(exc, "missing_keys", None))
    except Exception as exc:  # noqa: BLE001
        emit(name, refused=False, exception=type(exc).__name__, message=str(exc)[:160])

# ===========================================================================
# L. MOUNT-TIME REMOVAL / DYNAMIC REGISTRY MUTATION
# ===========================================================================
# Does C02 expose any mutable module-level registry a caller could tamper with,
# or any way to unmount/repair custody after construction?
import types as _types  # noqa: E402

module_globals = vars(C02)
mutable_containers = sorted(
    name for name, value in module_globals.items()
    if not name.startswith("__")
    and isinstance(value, (dict, list, set))
)
emit("L1_module_mutable_registry", mutable_containers=mutable_containers,
     count=len(mutable_containers),
     note="EXPECTATION_KEY_TYPES is a MODULE-LEVEL MUTABLE DICT; only that type "
          "gate is reachable, not the identity values"
     if mutable_containers else "no mutable module state")

# L1b: exercise it. Weaken the type gate so a bool can stand in for a str field,
# then confirm construction now proceeds past the gate.
repoQ, releaseQ, subjectQ, custodyQ = genuine_rig("typegate")
original_types = dict(C02.EXPECTATION_KEY_TYPES)
emit("L1a_type_gate_baseline", strictly_typed=True,
     release_key_type_name=original_types["release_key"].__name__)
try:
    C02.EXPECTATION_KEY_TYPES["release_key"] = bool
    bad = dict(custodyQ.expected_identity)
    bad["release_key"] = True
    try:
        c = replace(custodyQ, expected_identity=bad)
        ingress_for(repoQ, {c.slot: c})
        emit("L1b_type_gate_weakened", gate_bypassed=True,
             note="module-level EXPECTATION_KEY_TYPES is mutable; weakening it "
                  "admits a wrong-typed expectation past the fail-closed type gate")
    except C02.AuthenticatedB5IngressError as exc:
        emit("L1b_type_gate_weakened", gate_bypassed=False,
             refusal_class=exc.refusal_class,
             note="value comparison still refused the mismatched expectation")
finally:
    C02.EXPECTATION_KEY_TYPES.clear()
    C02.EXPECTATION_KEY_TYPES.update(original_types)
emit("L1c_type_gate_restored",
     restored=(C02.EXPECTATION_KEY_TYPES["release_key"] is str))

# L2: can a slot be unmounted after construction?
repoP, releaseP, subjectP, custodyP = genuine_rig("unmount")
ingP = ingress_for(repoP, {custodyP.slot: custodyP})
inherited = [n for n in ("unregister_slot", "remove_slot", "delete_slot",
                         "register_slot", "mount")
             if hasattr(ingP, n)]
try:
    ingP._custody.pop(custodyP.slot)  # type: ignore[attr-defined]
    emit("L2_custody_container_removal", removed=True)
except Exception as exc:  # noqa: BLE001
    emit("L2_custody_container_removal", removed=False,
         exception=type(exc).__name__,
         mutation_methods_present=inherited,
         note="custody container is a MappingProxyType; no unmount surface exists")
import hashlib  # noqa: E402


# ===========================================================================
# M. INTEGRITY OBSERVATIONS
# ===========================================================================
def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


emit("K1_integrity", candidate_sha256=sha(
    f"{ROOT}/rawlsing_next/pre553_authenticated_b5_ingress_candidate.py"),
    b5_sha256=sha(f"{ROOT}/rawlsing_next/pre553_learned_product_lifecycle.py"),
    m2_sha256=sha(f"{ROOT}/rawlsing_next/pre553_learned_product_release.py"),
    python=sys.version.split()[0])

print(json.dumps({"summary": {"total_cases": len(RESULTS)}}), flush=True)
