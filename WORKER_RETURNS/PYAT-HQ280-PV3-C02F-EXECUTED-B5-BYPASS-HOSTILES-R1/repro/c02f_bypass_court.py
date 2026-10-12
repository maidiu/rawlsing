"""HQ280 PV3 C02F -- Executed B5 bypass court: real mandatory boundary hostile runtime.

Reuses the C02R attack surface (K4/K5/K7, B1/B2/B3, H1/H2, C2, D1, G6) and the C02E
test-only mandatory patch overlay. Every case invokes the ACCEPTED owners for real.

FIX vs C02E: the C02E fixture attempted to instantiate the abstract
``LearnedProductReleaseProtocol`` (a ``runtime_checkable`` Protocol), which Python 3.11
refuses. This court constructs ``B5.LearnedProductLifecycleSubject`` DIRECTLY -- the
concrete frozen dataclass -- never through a Protocol. No abstract type is ever
instantiated.

Two phases per case:
  UNPATCHED -- demonstrate the real vulnerability exists (C02R reproduction)
  PATCHED   -- apply the C02E test-only overlay and demonstrate enforcement

Every case records the ACTUAL typed outcome. No policy is asserted by inspection.
"""
from __future__ import annotations

import contextlib
import json
import sys
from dataclasses import dataclass, replace
from types import MappingProxyType

from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next import pre553_authenticated_b5_ingress_candidate as C02
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash

import rawlsing_next.repro.b5_mandatory_patch as patch_module
from rawlsing_next.repro.b5_mandatory_patch import (
    PerimeterTicket,
    ProducerCredential,
    CheckpointAuthority,
    PerimeterTicketError,
    ProducerCredentialError,
    CheckpointAuthorityError,
    apply_mandatory_patch,
    remove_mandatory_patch,
)


RESULTS: list[dict] = []


def emit(case: str, **fields) -> None:
    row = {"case": case, **fields}
    RESULTS.append(row)
    print(json.dumps(row, sort_keys=True, default=str), flush=True)


def ref(kind: str, tag: str) -> ExactRef:
    d = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:c02f:{kind.lower()}:{tag}:sha256:{d}", d)


def auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", "1.0.0", semantic_hash({"authority": tag}))


def _key(ref: Any) -> str:
    if ref is None:
        return ""
    if isinstance(ref, str):
        return ref
    for attr in ("object_id", "authority_id"):
        value = getattr(ref, attr, None)
        if isinstance(value, str) and value:
            return value
    return ""


def _sorted_keys(refs) -> tuple[str, ...]:
    return tuple(sorted({_key(r) for r in refs if _key(r)}))


MODEL_AUTH = ref("ModelAuthority", "c02f-model")
WALKBACK_AUTH = ref("WalkbackAuthority", "c02f-walkback")
SEMANTIC_AUTH = auth("c02f-semantic")
PRODUCT_FAMILY = ref("ProductFamily", "c02f-family")
SELECTION_SCOPE = ref("SelectionScope", "c02f-scope")
CEILING = ref("ProducerPermissionCeiling", "c02f-ceiling")
FORGED_CEILING = ref("ProducerPermissionCeiling", "urn:reviewer:PRODUCTION_GRANT")
BUILD_RECEIPT = ref("BuildReceipt", "c02f-build")
EVENT_AUTHORITY = ref("EventAuthority", "c02f-ea")
EVENT_RULE = ref("EventRule", "c02f-er")
PRODUCT_REF = ref("LearnedSemanticProduct", "c02f-product")
PRODUCER_OWNER = ref("ProducerOwner", "c02f-owner")


# ---------------------------------------------------------------------------
# Concrete M2/B5 factories -- NO Protocol instantiation
# ---------------------------------------------------------------------------


def build_m2(repo: M2.M2Repository, *, tag: str,
             replay_grade: str = "EXACT_DETERMINISTIC_REBUILD",
             replay_complete: bool = True,
             determinant_refs=None,
             producer_credential=None) -> tuple:
    """Register a genuine M2 producer subject + five closures + a genuine release core."""
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
        **({"producer_credential": producer_credential} if producer_credential is not None else {}),
    )
    authority = M2.constitute_closure(
        repo, closure_kind="AUTHORITY",
        member_refs=(producer_contract, MODEL_AUTH, WALKBACK_AUTH), complete=True,
    )
    dependency = M2.constitute_closure(
        repo, closure_kind="DEPENDENCY",
        member_refs=(ref("UpstreamProduct", f"{tag}-upstream"),), complete=True,
    )
    determinant = M2.constitute_closure(
        repo, closure_kind="DETERMINANT",
        member_refs=(MODEL_AUTH, WALKBACK_AUTH) if determinant_refs is None
        else tuple(determinant_refs), complete=True,
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
        **({"producer_credential": producer_credential} if producer_credential is not None else {}),
    )
    return release, subject


def b5_subject_from_m2(repo, release, subject, *, replay_state="REPLAY_COMPLETE"):
    """Build a B5.LearnedProductLifecycleSubject DIRECTLY from real M2 output.

    This is the C02R/K4 bypass construction: a caller builds the B5 subject
    entirely from M2-resolved material, with no producer involvement.
    """
    dependency = repo.closure_exact(release.dependency_closure_ref)
    determinant = repo.closure_exact(release.determinant_closure_ref)
    replay = repo.closure_exact(release.replay_reconstruction_ref)

    direct = tuple(sorted({r.key: r for r in dependency.member_refs}.values(),
                          key=lambda r: r.key))

    det_members = {r.key: r for r in determinant.member_refs}
    for r in (MODEL_AUTH, WALKBACK_AUTH):
        digest = semantic_hash({"consumed_authority_key": r.object_id})
        consumed = ExactRef(
            "B5Lifecycle:CONSUMED_AUTHORITY",
            "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % digest, digest,
        )
        det_members[consumed.key] = consumed
    auth_digest = semantic_hash({
        "determinant_class": "SEMANTIC_AUTHORITY_REF",
        "authority_ref": SEMANTIC_AUTH.as_dict(),
    })
    auth_det = ExactRef(
        "B5Lifecycle:AUTHORITY_DETERMINANT",
        "urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:%s" % auth_digest,
        auth_digest,
    )
    det_members[auth_det.key] = auth_det
    det_refs = tuple(det_members[k] for k in sorted(det_members))

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


def expected_identity(repo, release, subject, *, ceiling_key, replay_grade="EXACT_DETERMINISTIC_REBUILD"):
    """Compute the COMPLETE closed expected identity for a slot, from real owner output."""
    dependency = repo.closure_exact(release.dependency_closure_ref)
    determinant = repo.closure_exact(release.determinant_closure_ref)
    replay = repo.closure_exact(release.replay_reconstruction_ref)

    direct_keys = _sorted_keys(dependency.member_refs)
    consumed_keys = _sorted_keys([MODEL_AUTH, WALKBACK_AUTH])
    determinant_members = {r.key: r for r in determinant.member_refs}
    for r in (MODEL_AUTH, WALKBACK_AUTH):
        digest = semantic_hash({"consumed_authority_key": r.object_id})
        consumed = ExactRef(
            "B5Lifecycle:CONSUMED_AUTHORITY",
            "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % digest, digest,
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
    det_refs = tuple(determinant_members[k] for k in sorted(determinant_members))

    return {
        "release_key": release.ref.object_id,
        "release_content_hash": release.content_hash,
        "producer_subject_key": _key(subject.ref),
        "producer_contract_key": _key(release.semantic_producer_contract_ref),
        "semantic_anatomy_key": _key(subject.semantic_anatomy_ref),
        "semantic_projection_hash": subject.semantic_anatomy_ref.content_hash,
        "product_key": PRODUCT_REF.object_id,
        "product_family_key": PRODUCT_FAMILY.object_id,
        "producer_owner_key": PRODUCER_OWNER.object_id,
        "selection_scope_key": SELECTION_SCOPE.object_id,
        "authority_snapshot_keys": (SEMANTIC_AUTH.authority_id,),
        "direct_dependency_keys": direct_keys,
        "determinant_keys": _sorted_keys(det_refs),
        "determinant_set_hash": semantic_hash([r.as_dict() for r in det_refs]),
        "consumed_authority_keys": consumed_keys,
        "replay_closure_key": _key(replay.ref),
        "replay_grade": "EXACT_DETERMINISTIC_REBUILD",
        "replay_root_key": _key(replay.ref),
        "receipt_keys": (_key(BUILD_RECEIPT),),
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
        required_replay_grade="EXACT_DETERMINISTIC_REBUILD",
        replay_state="REPLAY_COMPLETE",
        expected_identity=expected_identity(
            repo, release, subject,
            ceiling_key=ceiling_key if ceiling_key is not None else ceiling.object_id,
            replay_grade=replay_grade),
    )
    base.update(overrides)
    return C02.ProducerCustodyMaterial(**base)


def direct_executor_publish(subject):
    """The K4 bypass route: raw B5 executor, no perimeter."""
    ex = B5.LearnedProductLifecycleExecutor()
    ex.stage_release(subject)
    ex.register_product(subject.release_ref, event_authority_ref=EVENT_AUTHORITY,
                        event_rule_ref=EVENT_RULE)
    ev = ex.publish_product(subject.release_ref, event_authority_ref=EVENT_AUTHORITY,
                            event_rule_ref=EVENT_RULE)
    return ex, ev


def make_ticket(slot: str = "c02f-slot") -> PerimeterTicket:
    return PerimeterTicket(
        slot=slot,
        issuance_hash="test-ticket",
        perimeter_ref=ref("Perimeter", "c02f-perimeter"),
        authority_snapshot_refs=(SEMANTIC_AUTH,),
        expected_identity_hash="test-expected",
        issued_at_event_ref=ref("Event", "c02f-event"),
    )


def make_credential(subject_ref) -> ProducerCredential:
    return ProducerCredential(
        subject_ref=subject_ref,
        producer_issuer_ref=auth("c02f-issuer"),
        issuance_hash="test-credential",
        credential_ref=ref("Credential", "c02f-credential"),
    )


def make_checkpoint_authority(payload) -> CheckpointAuthority:
    return CheckpointAuthority(
        checkpoint_hash=semantic_hash(payload),
        verifying_authority_ref=auth("c02f-checkpoint-validator"),
        verification_hash=semantic_hash(payload),
        verification_ref=ref("CheckpointVerification", "c02f-verification"),
    )


# ---------------------------------------------------------------------------
# UNPATCHED phase -- demonstrate the real vulnerability exists
# ---------------------------------------------------------------------------


def run_unpatched():
    emit("PHASE", phase="UNPATCHED", patch_active=patch_module._PATCH_ACTIVE)

    # -- A1: perimeter positive (baseline) --
    repoA = M2.M2Repository()
    releaseA, subjectA = build_m2(repoA, tag="A1")
    custodyA = custody_for(repoA, releaseA, subjectA, slot="A1")
    ingressA = C02.AuthenticatedB5Ingress(
        m2_repository=repoA, custody={"A1": custodyA},
        revocations=C02.RevocationLedger(),
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    receiptA = ingressA.publish(C02.PublicationRequest(slot="A1"))
    emit("A1_perimeter_positive", published=True,
         authorizing=receiptA.authorizing, current_selection_performed=receiptA.current_selection_performed,
         perimeter_consulted=True, patch_active=patch_module._PATCH_ACTIVE)

    # -- B1: raw executor K4 bypass --
    repoB = M2.M2Repository()
    releaseB, subjectB = build_m2(repoB, tag="B1")
    forgedB = b5_subject_from_m2(repoB, releaseB, subjectB)
    try:
        exB, evB = direct_executor_publish(forgedB)
        stateB = exB.lifecycle_state(forgedB.release_ref)
        emit("B1_raw_executor_k4_bypass", bypassed=True,
             publication=stateB.publication, perimeter_consulted=False,
             patch_active=patch_module._PATCH_ACTIVE)
    except Exception as exc:
        emit("B1_raw_executor_k4_bypass", bypassed=False,
             error=type(exc).__name__, detail=str(exc), patch_active=patch_module._PATCH_ACTIVE)

    # -- B2: raw executor full K5 forgery --
    repoB2 = M2.M2Repository()
    releaseB2, subjectB2 = build_m2(repoB2, tag="B2")
    honestB2 = b5_subject_from_m2(repoB2, releaseB2, subjectB2)
    fake_ceiling = ref("ProducerPermissionCeiling", "urn:reviewer:PRODUCTION_GRANT")
    fake_receipt = ref("BuildReceipt", "urn:c02f:fake-receipt")
    fake_root = ref("ReplayRoot", "urn:c02f:fake-root")
    fully_forged = replace(honestB2, producer_permission_ceiling_ref=fake_ceiling,
                          build_or_release_receipt_refs=(fake_receipt,),
                          replay_root_ref=fake_root)
    try:
        exB2 = B5.LearnedProductLifecycleExecutor()
        exB2.stage_release(fully_forged)
        exB2.register_product(fully_forged.release_ref, event_authority_ref=EVENT_AUTHORITY,
                             event_rule_ref=EVENT_RULE)
        exB2.publish_product(fully_forged.release_ref, event_authority_ref=EVENT_AUTHORITY,
                             event_rule_ref=EVENT_RULE)
        stored_ceiling = exB2._repository_subjects[fully_forged.release_ref.key].producer_permission_ceiling_ref
        emit("B2_raw_executor_full_k5_forgery", bypassed=True,
             ceiling_is_forged=stored_ceiling == fake_ceiling,
             perimeter_consulted=False, patch_active=patch_module._PATCH_ACTIVE)
    except Exception as exc:
        emit("B2_raw_executor_full_k5_forgery", bypassed=False,
             error=type(exc).__name__, detail=str(exc), patch_active=patch_module._PATCH_ACTIVE)

    # -- B3: raw executor CURRENT selection bypass --
    repoB3 = M2.M2Repository()
    releaseB3, subjectB3 = build_m2(repoB3, tag="B3")
    honestB3 = b5_subject_from_m2(repoB3, releaseB3, subjectB3)
    forged_sel = replace(honestB3, producer_permission_ceiling_ref=fake_ceiling,
                         replay_root_ref=fake_root)
    try:
        exB3 = B5.LearnedProductLifecycleExecutor()
        exB3.stage_release(forged_sel)
        exB3.register_product(forged_sel.release_ref, event_authority_ref=EVENT_AUTHORITY,
                             event_rule_ref=EVENT_RULE)
        exB3.publish_product(forged_sel.release_ref, event_authority_ref=EVENT_AUTHORITY,
                             event_rule_ref=EVENT_RULE)
        keyB3 = exB3.selection_key(
            product_family_ref=PRODUCT_FAMILY, selection_scope_ref=SELECTION_SCOPE,
            selection_purpose_ref=ref("SelectionPurpose", "c02f-purpose"),
        )
        exB3.select_current(
            keyB3.ref, forged_sel.release_ref, expected_previous_receipt_ref=None,
            event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
            selection_attestation_ref=ref("SelectionAttestation", "c02f-att"),
        )
        current_events = [e.event_kind for e in exB3.events if e.event_kind == "CURRENT_SELECTED"]
        emit("B3_raw_executor_current_selection_bypass", bypassed=True,
             current_selected_event_present=bool(current_events),
             perimeter_consulted=False, patch_active=patch_module._PATCH_ACTIVE)
    except Exception as exc:
        emit("B3_raw_executor_current_selection_bypass", bypassed=False,
             error=type(exc).__name__, detail=str(exc), patch_active=patch_module._PATCH_ACTIVE)

    # -- D1: attacker-minted M2 release published via perimeter --
    repoD = M2.M2Repository()
    releaseD, subjectD = build_m2(repoD, tag="D1-attacker-minted")
    custodyD = custody_for(repoD, releaseD, subjectD, slot="D1")
    ingressD = C02.AuthenticatedB5Ingress(
        m2_repository=repoD, custody={"D1": custodyD},
        revocations=C02.RevocationLedger(),
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    receiptD = ingressD.publish(C02.PublicationRequest(slot="D1"))
    emit("D1_attacker_minted_release_published", published=True,
         authorizing=receiptD.authorizing, patch_active=patch_module._PATCH_ACTIVE)

    # -- G6: arbitrary ceiling accepted --
    repoG = M2.M2Repository()
    releaseG, subjectG = build_m2(repoG, tag="G6")
    total_ceiling = ref("ProducerPermissionCeiling", "urn:c02f:TOTAL_CONTROL")
    custodyG = custody_for(repoG, releaseG, subjectG, slot="G6",
                           ceiling=total_ceiling, ceiling_key=total_ceiling.object_id)
    ingressG = C02.AuthenticatedB5Ingress(
        m2_repository=repoG, custody={"G6": custodyG},
        revocations=C02.RevocationLedger(),
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    receiptG = ingressG.publish(C02.PublicationRequest(slot="G6"))
    emit("G6_arbitrary_ceiling_accepted", published=True,
         ceiling=total_ceiling.object_id, authorizing=receiptG.authorizing,
         patch_active=patch_module._PATCH_ACTIVE)

    # -- H1: checkpoint self-hash bypass --
    repoH = M2.M2Repository()
    releaseH, subjectH = build_m2(repoH, tag="H1")
    exH = B5.LearnedProductLifecycleExecutor()
    exH.stage_release(b5_subject_from_m2(repoH, releaseH, subjectH))
    exH.register_product(releaseH.ref, event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
    exH.publish_product(releaseH.ref, event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
    ckptH = exH.export_checkpoint()
    evil_payload = json.loads(json.dumps(ckptH["checkpoint_payload"]))
    evil_ckpt = {"checkpoint_payload": evil_payload, "checkpoint_hash": semantic_hash(evil_payload)}
    try:
        ex_re = B5.LearnedProductLifecycleExecutor.from_checkpoint(evil_ckpt)
        emit("H1_checkpoint_self_hash", rehydrated=True,
             hash_is_self_referential=True, perimeter_consulted=False,
             patch_active=patch_module._PATCH_ACTIVE)
    except Exception as exc:
        emit("H1_checkpoint_self_hash", rehydrated=False,
             error=type(exc).__name__, detail=str(exc), patch_active=patch_module._PATCH_ACTIVE)

    # -- H2: checkpoint rehydrates CURRENT --
    repoH2 = M2.M2Repository()
    releaseH2, subjectH2 = build_m2(repoH2, tag="H2")
    exH2 = B5.LearnedProductLifecycleExecutor()
    honestH2 = b5_subject_from_m2(repoH2, releaseH2, subjectH2)
    exH2.stage_release(honestH2)
    exH2.register_product(honestH2.release_ref, event_authority_ref=EVENT_AUTHORITY,
                          event_rule_ref=EVENT_RULE)
    exH2.publish_product(honestH2.release_ref, event_authority_ref=EVENT_AUTHORITY,
                         event_rule_ref=EVENT_RULE)
    keyH2 = exH2.selection_key(
        product_family_ref=PRODUCT_FAMILY, selection_scope_ref=SELECTION_SCOPE,
        selection_purpose_ref=ref("SelectionPurpose", "c02f-h2-purpose"),
    )
    exH2.select_current(
        keyH2.ref, honestH2.release_ref, expected_previous_receipt_ref=None,
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
        selection_attestation_ref=ref("SelectionAttestation", "c02f-h2-att"),
    )
    ckptH2 = exH2.export_checkpoint()
    p2 = json.loads(json.dumps(ckptH2["checkpoint_payload"]))
    caller_ckpt = {"checkpoint_payload": p2, "checkpoint_hash": semantic_hash(p2)}
    try:
        ex_re2 = B5.LearnedProductLifecycleExecutor.from_checkpoint(caller_ckpt)
        current_present = any(e.event_kind == "CURRENT_SELECTED" for e in ex_re2.events)
        emit("H2_checkpoint_rehydrates_current", rehydrated=True,
             current_selected_event_present=current_present,
             perimeter_consulted=False, patch_active=patch_module._PATCH_ACTIVE)
    except Exception as exc:
        emit("H2_checkpoint_rehydrates_current", rehydrated=False,
             error=type(exc).__name__, detail=str(exc), patch_active=patch_module._PATCH_ACTIVE)

    # -- L1b: mutable type gate weakened --
    repoL = M2.M2Repository()
    releaseL, subjectL = build_m2(repoL, tag="L1b")
    custodyL = custody_for(repoL, releaseL, subjectL, slot="L1b")
    e_base = custodyL.expected_identity
    original_type = C02.EXPECTATION_KEY_TYPES["release_key"]
    C02.EXPECTATION_KEY_TYPES["release_key"] = bool
    bad_e = {**e_base, "release_key": True}
    try:
        bad_custody = replace(custodyL, expected_identity=bad_e)
        C02.AuthenticatedB5Ingress(
            m2_repository=repoL, custody={"L1b": bad_custody},
            event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
        )
        gate_bypassed = True
    except Exception:
        gate_bypassed = False
    C02.EXPECTATION_KEY_TYPES["release_key"] = original_type
    emit("L1b_type_gate_weakened", gate_bypassed=gate_bypassed, patch_active=patch_module._PATCH_ACTIVE)

    # -- C2: reauthorized mutation admitted (tautology) --
    repoC = M2.M2Repository()
    releaseC, subjectC = build_m2(repoC, tag="C2")
    custodyC = custody_for(repoC, releaseC, subjectC, slot="C2")
    det_c = repoC.closure_exact(releaseC.determinant_closure_ref)
    extra_ref = ref("InjectedEdge", "c02f-injected")
    object.__setattr__(det_c, "member_refs", tuple(det_c.member_refs) + (extra_ref,))
    custodyC2 = custody_for(repoC, releaseC, subjectC, slot="C2")
    ingressC2 = C02.AuthenticatedB5Ingress(
        m2_repository=repoC, custody={"C2": custodyC2},
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    receiptC2 = ingressC2.publish(C02.PublicationRequest(slot="C2"))
    emit("C2_reauthorized_mutation_admitted", admitted=True,
         injected_edge_present=True, authorizing=receiptC2.authorizing,
         patch_active=patch_module._PATCH_ACTIVE)

    # -- H3: no issuer exists --
    import subprocess
    result = subprocess.run(
        ["grep", "-rlE", "def verify_signature|public_key|private_key|hmac\\.|keyring|credential_store|producer_credential|signing_key|verify_producer_signature|issuer_credential",
         "rawlsing_next/"],
        capture_output=True, text=True,
    )
    verification_modules = len([x for x in result.stdout.strip().split("\n") if x])
    emit("H3_issuer_or_crypto_search", verification_modules=verification_modules,
         patch_active=patch_module._PATCH_ACTIVE)


# ---------------------------------------------------------------------------
# PATCHED phase -- apply C02E overlay, demonstrate enforcement
# ---------------------------------------------------------------------------


def run_patched():
    emit("PHASE", phase="PATCHED", patch_active=patch_module._PATCH_ACTIVE)
    apply_mandatory_patch()
    emit("PATCH_APPLIED", patch_active=patch_module._PATCH_ACTIVE)

    ticket = make_ticket()
    credential = make_credential(ref("LearnedSemanticProduct", "patched-subject"))

    # -- B1 PATCHED: raw executor requires ticket --
    try:
        B5.LearnedProductLifecycleExecutor()
        emit("B1_patched_raw_executor", refused=False, patch_active=patch_module._PATCH_ACTIVE)
    except PerimeterTicketError as exc:
        emit("B1_patched_raw_executor", refused=True, error=exc.code,
             patch_active=patch_module._PATCH_ACTIVE)

    # -- B2 PATCHED: raw executor with forged ceiling still requires ticket --
    repoB2p = M2.M2Repository()
    releaseB2p, subjectB2p = build_m2(repoB2p, tag="B2-patched", producer_credential=make_credential(ref("LearnedSemanticProduct", "B2-patched-subject")))
    honestB2p = b5_subject_from_m2(repoB2p, releaseB2p, subjectB2p)
    fully_forged_p = replace(honestB2p, producer_permission_ceiling_ref=FORGED_CEILING,
                             build_or_release_receipt_refs=(ref("BuildReceipt", "fake"),),
                             replay_root_ref=ref("ReplayRoot", "fake"))
    try:
        exB2p = B5.LearnedProductLifecycleExecutor(perimeter_ticket=ticket)
        exB2p.stage_release(fully_forged_p)
        exB2p.register_product(fully_forged_p.release_ref, event_authority_ref=EVENT_AUTHORITY,
                              event_rule_ref=EVENT_RULE)
        exB2p.publish_product(fully_forged_p.release_ref, event_authority_ref=EVENT_AUTHORITY,
                              event_rule_ref=EVENT_RULE)
        emit("B2_patched_full_k5_forgery", refused=False, patch_active=patch_module._PATCH_ACTIVE)
    except Exception as exc:
        emit("B2_patched_full_k5_forgery", refused=True,
             error=type(exc).__name__, code=getattr(exc, "code", ""),
             patch_active=patch_module._PATCH_ACTIVE)

    # -- B3 PATCHED: select_current requires ticket --
    try:
        exB3p = B5.LearnedProductLifecycleExecutor(perimeter_ticket=ticket)
        keyB3p = exB3p.selection_key(
            product_family_ref=PRODUCT_FAMILY, selection_scope_ref=SELECTION_SCOPE,
            selection_purpose_ref=ref("SelectionPurpose", "c02f-patched-purpose"),
        )
        emit("B3_patched_select_current", refused=False, patch_active=patch_module._PATCH_ACTIVE)
    except Exception as exc:
        emit("B3_patched_select_current", refused=True,
             error=type(exc).__name__, code=getattr(exc, "code", ""),
             patch_active=patch_module._PATCH_ACTIVE)

    # -- D1 PATCHED: M2 registration requires ProducerCredential --
    repoDp = M2.M2Repository()
    subject_ref_dp = ref("LearnedSemanticProduct", "patched-minted")
    try:
        M2.register_producer_subject(
            repoDp, subject_ref=subject_ref_dp, subject_kind="IMMUTABLE_LEARNED_PRODUCT",
            producer_contract_ref=ref("ProducerContract", "patched-contract"),
            typed_state="POSITIVE", semantic_anatomy_ref=ref("SemanticAnatomy", "patched-anatomy"),
            required_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
            required_replay_refs=(ref("ReplayInput", "patched-replay"),),
        )
        emit("D1_patched_M2_minted", refused=False, patch_active=patch_module._PATCH_ACTIVE)
    except ProducerCredentialError as exc:
        emit("D1_patched_M2_minted", refused=True, error=exc.code, patch_active=patch_module._PATCH_ACTIVE)

    # -- B2b PATCHED: demo ticket does NOT authenticate forged subject --
    # Key finding: a caller-supplied demo-fixture ticket satisfies the mandatory
    # constructor but does NOT authenticate the subject against owner-held material.
    # The C02 perimeter's expectation comparison is still required for that.
    repoB2b = M2.M2Repository()
    releaseB2b, subjectB2b = build_m2(repoB2b, tag="B2b-patched",
                                       producer_credential=make_credential(ref("LearnedSemanticProduct", "B2b-patched-subject")))
    honestB2b = b5_subject_from_m2(repoB2b, releaseB2b, subjectB2b)
    forged_b2b = replace(honestB2b, producer_permission_ceiling_ref=FORGED_CEILING,
                         build_or_release_receipt_refs=(ref("BuildReceipt", "fake-b2b"),),
                         replay_root_ref=ref("ReplayRoot", "fake-b2b"))
    try:
        exB2b = B5.LearnedProductLifecycleExecutor(perimeter_ticket=ticket)
        exB2b.stage_release(forged_b2b)
        exB2b.register_product(forged_b2b.release_ref, event_authority_ref=EVENT_AUTHORITY,
                               event_rule_ref=EVENT_RULE)
        exB2b.publish_product(forged_b2b.release_ref, event_authority_ref=EVENT_AUTHORITY,
                              event_rule_ref=EVENT_RULE)
        emit("B2b_patched_demo_ticket_forged_subject", bypassed=True,
             note="demo-fixture ticket is NOT issuer authentication; "
                  "C02 perimeter expectation comparison still required",
             patch_active=patch_module._PATCH_ACTIVE)
    except Exception as exc:
        emit("B2b_patched_demo_ticket_forged_subject", bypassed=False,
             error=type(exc).__name__, code=getattr(exc, "code", ""),
             patch_active=patch_module._PATCH_ACTIVE)

    # -- D1b PATCHED: M2 registration WITH credential succeeds --
    repoDp2 = M2.M2Repository()
    subject_ref_dp2 = ref("LearnedSemanticProduct", "patched-minted-2")
    cred_dp2 = make_credential(subject_ref_dp2)
    try:
        M2.register_producer_subject(
            repoDp2, subject_ref=subject_ref_dp2, subject_kind="IMMUTABLE_LEARNED_PRODUCT",
            producer_contract_ref=ref("ProducerContract", "patched-contract-2"),
            typed_state="POSITIVE", semantic_anatomy_ref=ref("SemanticAnatomy", "patched-anatomy-2"),
            required_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
            required_replay_refs=(ref("ReplayInput", "patched-replay-2"),),
            producer_credential=cred_dp2,
        )
        emit("D1b_patched_M2_minted_with_credential", refused=False, patch_active=patch_module._PATCH_ACTIVE)
    except Exception as exc:
        emit("D1b_patched_M2_minted_with_credential", refused=True,
             error=type(exc).__name__, code=getattr(exc, "code", ""),
             patch_active=patch_module._PATCH_ACTIVE)

    # -- G6 PATCHED: arbitrary ceiling in custody --
    repoGp = M2.M2Repository()
    releaseGp, subjectGp = build_m2(repoGp, tag="G6-patched", producer_credential=make_credential(ref("LearnedSemanticProduct", "G6-patched-subject")))
    total_ceiling_p = ref("ProducerPermissionCeiling", "urn:c02f:TOTAL_CONTROL")
    custodyGp = custody_for(repoGp, releaseGp, subjectGp, slot="G6-patched",
                            ceiling=total_ceiling_p, ceiling_key=total_ceiling_p.object_id)
    try:
        C02.AuthenticatedB5Ingress(
            m2_repository=repoGp, custody={"G6-patched": custodyGp},
            event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
        )
        emit("G6_patched_arbitrary_ceiling", refused=False, patch_active=patch_module._PATCH_ACTIVE)
    except Exception as exc:
        emit("G6_patched_arbitrary_ceiling", refused=True,
             error=type(exc).__name__, code=getattr(exc, "code", ""),
             patch_active=patch_module._PATCH_ACTIVE)

    # -- H1 PATCHED: checkpoint self-hash rejected --
    repoHp = M2.M2Repository()
    releaseHp, subjectHp = build_m2(repoHp, tag="H1-patched", producer_credential=make_credential(ref("LearnedSemanticProduct", "H1-patched-subject")))
    exHp = B5.LearnedProductLifecycleExecutor(perimeter_ticket=ticket)
    exHp.stage_release(b5_subject_from_m2(repoHp, releaseHp, subjectHp))
    exHp.register_product(releaseHp.ref, event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
    exHp.publish_product(releaseHp.ref, event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
    ckptHp = exHp.export_checkpoint()
    evil_p = json.loads(json.dumps(ckptHp["checkpoint_payload"]))
    evil_ck = {"checkpoint_payload": evil_p, "checkpoint_hash": semantic_hash(evil_p)}
    try:
        B5.LearnedProductLifecycleExecutor.from_checkpoint(evil_ck)
        emit("H1_patched_checkpoint_self_hash", refused=False, patch_active=patch_module._PATCH_ACTIVE)
    except CheckpointAuthorityError as exc:
        emit("H1_patched_checkpoint_self_hash", refused=True, error=exc.code,
             patch_active=patch_module._PATCH_ACTIVE)

    # -- H2 PATCHED: checkpoint with independent authority succeeds --
    good_auth = make_checkpoint_authority(ckptHp["checkpoint_payload"])
    try:
        ex_re_hp = B5.LearnedProductLifecycleExecutor.from_checkpoint(
            ckptHp, checkpoint_authority=good_auth
        )
        emit("H2_patched_checkpoint_with_authority", refused=False, patch_active=patch_module._PATCH_ACTIVE)
    except Exception as exc:
        emit("H2_patched_checkpoint_with_authority", refused=True,
             error=type(exc).__name__, code=getattr(exc, "code", ""),
             patch_active=patch_module._PATCH_ACTIVE)

    # -- L1b PATCHED: EXPECTATION_KEY_TYPES frozen --
    from types import MappingProxyType
    is_frozen = isinstance(C02.EXPECTATION_KEY_TYPES, MappingProxyType)
    try:
        C02.EXPECTATION_KEY_TYPES["release_key"] = bool
        mutation_succeeded = True
    except (TypeError, AttributeError):
        mutation_succeeded = False
    emit("L1b_patched_type_gate_frozen", frozen=is_frozen,
         mutation_succeeded=mutation_succeeded, patch_active=patch_module._PATCH_ACTIVE)

    # -- C2 PATCHED: reauthorized mutation still admitted (tautology unclosed) --
    repoCp = M2.M2Repository()
    releaseCp, subjectCp = build_m2(repoCp, tag="C2-patched", producer_credential=make_credential(ref("LearnedSemanticProduct", "C2-patched-subject")))
    custodyCp = custody_for(repoCp, releaseCp, subjectCp, slot="C2-patched")
    det_cp = repoCp.closure_exact(releaseCp.determinant_closure_ref)
    extra_ref_p = ref("InjectedEdge", "c02f-injected-patched")
    object.__setattr__(det_cp, "member_refs", tuple(det_cp.member_refs) + (extra_ref_p,))
    custodyCp2 = custody_for(repoCp, releaseCp, subjectCp, slot="C2-patched")
    ingressCp2 = C02.AuthenticatedB5Ingress(
        m2_repository=repoCp, custody={"C2-patched": custodyCp2},
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
    )
    receiptCp2 = ingressCp2.publish(C02.PublicationRequest(slot="C2-patched"))
    emit("C2_patched_reauthorized_mutation", admitted=True,
         authorizing=receiptCp2.authorizing, patch_active=patch_module._PATCH_ACTIVE)

    remove_mandatory_patch()
    emit("PATCH_REMOVED", patch_active=patch_module._PATCH_ACTIVE)


# ---------------------------------------------------------------------------
# Genuine positive: honest M2 + PUBLISHED under permitted ticket
# ---------------------------------------------------------------------------


def run_genuine_positive():
    """One genuine sourcefree legal positive: honest accepted M2 release
    construction + lifecycle PUBLISHED under a test-only permitted ticket.
    Graded DEMO FIXTURE, not operative credentials (no competent issuer exists).
    """
    ticket = make_ticket("positive-slot")
    cred = make_credential(ref("LearnedSemanticProduct", "positive-subject"))

    repo = M2.M2Repository()
    release, subject = build_m2(repo, tag="positive",
                                producer_credential=cred)

    # B5 lifecycle with ticket (permitted under patch)
    ex = B5.LearnedProductLifecycleExecutor(perimeter_ticket=ticket)
    honest = b5_subject_from_m2(repo, release, subject)
    ex.stage_release(honest)
    ex.register_product(honest.release_ref, event_authority_ref=EVENT_AUTHORITY,
                        event_rule_ref=EVENT_RULE)
    ex.publish_product(honest.release_ref, event_authority_ref=EVENT_AUTHORITY,
                      event_rule_ref=EVENT_RULE)
    state = ex.lifecycle_state(honest.release_ref)
    emit("POSITIVE_genuine_m2_published", publication=state.publication,
         authorizing=False, grade="DEMO_FIXTURE__NOT_OPERATIVE_CREDENTIALS",
         patch_active=patch_module._PATCH_ACTIVE)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    emit("COURT_START", total_phases=3, patch_module="rawlsing_next.repro.b5_mandatory_patch")
    run_unpatched()
    run_patched()
    apply_mandatory_patch()
    run_genuine_positive()
    remove_mandatory_patch()

    passed = sum(1 for r in RESULTS if r.get("case") and not r.get("error"))
    total = len(RESULTS)
    emit("COURT_COMPLETE", total_cases=total, passed=passed,
         patch_active=patch_module._PATCH_ACTIVE)


if __name__ == "__main__":
    main()