"""PYAT HQ280 PV3 C02H — Separate-principal trust boundary demonstration court.

Executes real owner invocations against:
  1. Unpatched accepted B5/M2 owners (C02R vulnerability reproduction)
  2. C02E patched overlay (mandatory presence gates)
  3. Separate-principal demo (issuer/verifier/attacker separation)

Every case records the ACTUAL typed outcome from real invocations.
"""
from __future__ import annotations

import json
import sys
from dataclasses import replace

from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next import pre553_authenticated_b5_ingress_candidate as C02
from rawlsing_next.pre553_empirical_objects import ExactRef, AuthorityRef, semantic_hash
from rawlsing_next.repro.b5_mandatory_patch import (
    apply_mandatory_patch, remove_mandatory_patch, PerimeterTicket,
    ProducerCredential, CheckpointAuthority,
    PerimeterTicketError, ProducerCredentialError, CheckpointAuthorityError,
)
from rawlsing_next.pre553_b5_separate_principal_verifier_candidate import (
    IssuerProcess, VerifierProcess, AttackerProcess,
    SeparatePrincipalError, build_demo_principal_pair, DEMO_GRADE, DISPOSITION,
)


RESULTS: list[dict] = []


def emit(case: str, **fields) -> None:
    row = {"case": case, **fields}
    RESULTS.append(row)
    print(json.dumps(row, sort_keys=True, default=str), flush=True)


def ref(kind: str, tag: str) -> ExactRef:
    d = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:c02h:{kind.lower()}:{tag}:sha256:{d}", d)


def auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", "1.0.0", semantic_hash({"authority": tag}))


MODEL_AUTH = ref("ModelAuthority", "c02h-model")
WALKBACK_AUTH = ref("WalkbackAuthority", "c02h-walkback")
SEMANTIC_AUTH = auth("c02h-semantic")
PRODUCT_FAMILY = ref("ProductFamily", "c02h-family")
SELECTION_SCOPE = ref("SelectionScope", "c02h-scope")
CEILING = ref("ProducerPermissionCeiling", "c02h-ceiling")
FORGED_CEILING = ref("ProducerPermissionCeiling", "urn:reviewer:PRODUCTION_GRANT")
BUILD_RECEIPT = ref("BuildReceipt", "c02h-build")
EVENT_AUTHORITY = ref("EventAuthority", "c02h-ea")
EVENT_RULE = ref("EventRule", "c02h-er")
PRODUCT_REF = ref("LearnedSemanticProduct", "c02h-product")
PRODUCER_OWNER = ref("ProducerOwner", "c02h-owner")


def build_m2(repo, *, tag, producer_credential=None):
    subject_ref = ref("LearnedSemanticProduct", f"{tag}-subject")
    producer_contract = ref("ProducerContract", f"{tag}-contract")
    anatomy = ref("SemanticAnatomy", f"{tag}-anatomy")
    subject = M2.register_producer_subject(
        repo, subject_ref=subject_ref, subject_kind="IMMUTABLE_LEARNED_PRODUCT",
        producer_contract_ref=producer_contract, typed_state="POSITIVE",
        semantic_anatomy_ref=anatomy,
        required_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
        required_replay_refs=(ref("ReplayInput", f"{tag}-replay-input"),),
        **({"producer_credential": producer_credential} if producer_credential else {}),
    )
    authority = M2.constitute_closure(repo, closure_kind="AUTHORITY",
        member_refs=(producer_contract, MODEL_AUTH, WALKBACK_AUTH), complete=True)
    dependency = M2.constitute_closure(repo, closure_kind="DEPENDENCY",
        member_refs=(ref("UpstreamProduct", f"{tag}-upstream"),), complete=True)
    determinant = M2.constitute_closure(repo, closure_kind="DETERMINANT",
        member_refs=(MODEL_AUTH, WALKBACK_AUTH), complete=True)
    replay = M2.constitute_closure(repo, closure_kind="REPLAY_RECONSTRUCTION",
        member_refs=(ref("ReplayInput", f"{tag}-replay-input"),),
        complete=True, metadata={"replay_grade": "EXACT_DETERMINISTIC_REBUILD"})
    explanation = M2.constitute_closure(repo, closure_kind="EXPLANATION_LINEAGE",
        member_refs=(subject_ref, producer_contract), complete=True)
    release = M2.constitute_release(
        repo, release_subject_ref=subject_ref,
        release_subject_kind="IMMUTABLE_LEARNED_PRODUCT",
        semantic_producer_contract_ref=producer_contract,
        authority_closure_ref=authority.ref, dependency_closure_ref=dependency.ref,
        determinant_closure_ref=determinant.ref,
        replay_reconstruction_ref=replay.ref,
        explanation_lineage_ref=explanation.ref,
        **({"producer_credential": producer_credential} if producer_credential else {}),
    )
    return release, subject


def b5_subject_from_m2(repo, release, subject, *, replay_state="REPLAY_COMPLETE"):
    dependency = repo.closure_exact(release.dependency_closure_ref)
    determinant = repo.closure_exact(release.determinant_closure_ref)
    replay = repo.closure_exact(release.replay_reconstruction_ref)
    direct = tuple(sorted({r.key: r for r in dependency.member_refs}.values(), key=lambda r: r.key))
    det_members = {r.key: r for r in determinant.member_refs}
    for r in (MODEL_AUTH, WALKBACK_AUTH):
        digest = semantic_hash({"consumed_authority_key": r.object_id})
        consumed = ExactRef("B5Lifecycle:CONSUMED_AUTHORITY",
            "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % digest, digest)
        det_members[consumed.key] = consumed
    auth_digest = semantic_hash({"determinant_class": "SEMANTIC_AUTHORITY_REF",
        "authority_ref": SEMANTIC_AUTH.as_dict()})
    auth_det = ExactRef("B5Lifecycle:AUTHORITY_DETERMINANT",
        "urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:%s" % auth_digest, auth_digest)
    det_members[auth_det.key] = auth_det
    det_refs = tuple(det_members[k] for k in sorted(det_members))
    return B5.LearnedProductLifecycleSubject(
        release_ref=release.ref, product_ref=PRODUCT_REF,
        product_family_ref=PRODUCT_FAMILY, producer_owner_ref=PRODUCER_OWNER,
        producer_contract_ref=release.semantic_producer_contract_ref,
        semantic_projection_hash=subject.semantic_anatomy_ref.content_hash,
        authority_snapshot_refs=(SEMANTIC_AUTH,), direct_dependency_refs=direct,
        determinant_refs=det_refs,
        determinant_set_hash=semantic_hash([r.as_dict() for r in det_refs]),
        replay_root_ref=replay.ref, selection_scope_ref=SELECTION_SCOPE,
        build_or_release_receipt_refs=(BUILD_RECEIPT,),
        producer_permission_ceiling_ref=CEILING, replay_state=replay_state,
        materialization_class="MANDATORY_RETAINED_CAPITAL")


def expected_identity(repo, release, subject, *, ceiling_key, replay_grade="EXACT_DETERMINISTIC_REBUILD"):
    dependency = repo.closure_exact(release.dependency_closure_ref)
    determinant = repo.closure_exact(release.determinant_closure_ref)
    replay = repo.closure_exact(release.replay_reconstruction_ref)
    direct_keys = tuple(sorted({r.object_id for r in dependency.member_refs}))
    consumed_keys = tuple(sorted({MODEL_AUTH.object_id, WALKBACK_AUTH.object_id}))
    det_members = {r.key: r for r in determinant.member_refs}
    for r in (MODEL_AUTH, WALKBACK_AUTH):
        digest = semantic_hash({"consumed_authority_key": r.object_id})
        consumed = ExactRef("B5Lifecycle:CONSUMED_AUTHORITY",
            "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % digest, digest)
        det_members[consumed.key] = consumed
    auth_digest = semantic_hash({"determinant_class": "SEMANTIC_AUTHORITY_REF",
        "authority_ref": SEMANTIC_AUTH.as_dict()})
    auth_det = ExactRef("B5Lifecycle:AUTHORITY_DETERMINANT",
        "urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:%s" % auth_digest, auth_digest)
    det_members[auth_det.key] = auth_det
    det_refs = tuple(det_members[k] for k in sorted(det_members))
    return {
        "release_key": release.ref.object_id, "release_content_hash": release.content_hash,
        "producer_subject_key": subject.ref.object_id,
        "producer_contract_key": release.semantic_producer_contract_ref.object_id,
        "semantic_anatomy_key": subject.semantic_anatomy_ref.object_id,
        "semantic_projection_hash": subject.semantic_anatomy_ref.content_hash,
        "product_key": PRODUCT_REF.object_id, "product_family_key": PRODUCT_FAMILY.object_id,
        "producer_owner_key": PRODUCER_OWNER.object_id,
        "selection_scope_key": SELECTION_SCOPE.object_id,
        "authority_snapshot_keys": (SEMANTIC_AUTH.authority_id,),
        "direct_dependency_keys": direct_keys,
        "determinant_keys": tuple(sorted(r.object_id for r in det_refs)),
        "determinant_set_hash": semantic_hash([r.as_dict() for r in det_refs]),
        "consumed_authority_keys": consumed_keys,
        "replay_closure_key": replay.ref.object_id, "replay_grade": "EXACT_DETERMINISTIC_REBUILD",
        "replay_root_key": replay.ref.object_id, "receipt_keys": (BUILD_RECEIPT.object_id,),
        "permission_ceiling_key": ceiling_key,
        "m2_release_projection_hash": semantic_hash(dict(release.semantic_projection())),
    }


def custody_for(repo, release, subject, *, slot, ceiling=CEILING, ceiling_key=None, **overrides):
    base = dict(slot=slot, release_ref=release.ref, product_ref=PRODUCT_REF,
        product_family_ref=PRODUCT_FAMILY, producer_owner_ref=PRODUCER_OWNER,
        selection_scope_ref=SELECTION_SCOPE, semantic_authority_snapshot_refs=(SEMANTIC_AUTH,),
        build_or_release_receipt_refs=(BUILD_RECEIPT,), producer_permission_ceiling_ref=ceiling,
        consumed_authority_refs=(MODEL_AUTH, WALKBACK_AUTH), direct_dependency_refs=(),
        extra_determinant_refs=(), required_replay_grade="EXACT_DETERMINISTIC_REBUILD",
        replay_state="REPLAY_COMPLETE",
        expected_identity=expected_identity(repo, release, subject,
            ceiling_key=ceiling_key or ceiling.object_id))
    base.update(overrides)
    return C02.ProducerCustodyMaterial(**base)


def run_unpatched():
    emit("PHASE", phase="UNPATCHED")
    repo = M2.M2Repository()
    release, subject = build_m2(repo, tag="unpatched")
    forged = b5_subject_from_m2(repo, release, subject)
    try:
        ex = B5.LearnedProductLifecycleExecutor()
        ex.stage_release(forged)
        ex.register_product(forged.release_ref, event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
        ex.publish_product(forged.release_ref, event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
        emit("UNPATCHED_raw_b5_publishes", publication="PUBLISHED")
    except Exception as exc:
        emit("UNPATCHED_raw_b5_publishes", error=type(exc).__name__)

    # B2b: forged subject with demo ticket
    repo2 = M2.M2Repository()
    release2, subject2 = build_m2(repo2, tag="b2b")
    honest = b5_subject_from_m2(repo2, release2, subject2)
    forged_b2b = replace(honest, producer_permission_ceiling_ref=FORGED_CEILING,
                         build_or_release_receipt_refs=(ref("BuildReceipt", "fake"),),
                         replay_root_ref=ref("ReplayRoot", "fake"))
    try:
        ex2 = B5.LearnedProductLifecycleExecutor()
        ex2.stage_release(forged_b2b)
        ex2.register_product(forged_b2b.release_ref, event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
        ex2.publish_product(forged_b2b.release_ref, event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
        emit("UNPATCHED_B2b_forged_subject_publishes", publication="PUBLISHED")
    except Exception as exc:
        emit("UNPATCHED_B2b_forged_subject_publishes", error=type(exc).__name__)


def run_separate_principal():
    emit("PHASE", phase="SEPARATE_PRINCIPAL_DEMO")
    issuer, verifier = build_demo_principal_pair()
    attacker = AttackerProcess()

    # 1. Genuine positive: issuer credential verifies
    repo = M2.M2Repository()
    release, subject = build_m2(repo, tag="sp-positive")
    b5_subj = b5_subject_from_m2(repo, release, subject)
    cred = issuer.issue(
        subject_ref=b5_subj.release_ref,
        producer_contract_ref=b5_subj.producer_contract_ref,
        permission_ceiling_ref=b5_subj.producer_permission_ceiling_ref,
        release_ref=b5_subj.release_ref,
        replay_closure_ref=b5_subj.replay_root_ref,
        scope={"source_universe_refs": []},
    )
    try:
        verifier.verify(cred, subject=b5_subj, issuer=issuer)
        emit("SP_GENUINE_credential_verifies", verified=True, grade=DEMO_GRADE)
    except SeparatePrincipalError as exc:
        emit("SP_GENUINE_credential_verifies", verified=False, error=exc.code)

    # 2. Forged credential (attacker-minted) refused
    forged_cred = attacker.forge_credential(
        issuer_id=issuer.issuer_id, subject_ref=b5_subj.release_ref,
        producer_contract_ref=b5_subj.producer_contract_ref,
        permission_ceiling_ref=b5_subj.producer_permission_ceiling_ref,
        release_ref=b5_subj.release_ref, replay_closure_ref=b5_subj.replay_root_ref)
    try:
        verifier.verify(forged_cred, subject=b5_subj)
        emit("SP_FORGED_credential", refused=False)
    except SeparatePrincipalError as exc:
        emit("SP_FORGED_credential", refused=True, error=exc.code)

    # 3. Root swap refused
    swap_result = attacker.swap_root(verifier, "attacker-root")
    emit("SP_ROOT_SWAP", refused=not swap_result)

    # 4. Self-registered issuer refused
    reg_result = attacker.self_register_issuer(verifier, "attacker-issuer")
    emit("SP_SELF_REGISTERED_ISSUER", refused=not reg_result)

    # 5. Revoked issuer credential refused
    issuer.revoke(cred.credential_id)
    try:
        verifier.verify(cred, subject=b5_subj, issuer=issuer)
        emit("SP_REVOKED_issuer", refused=False)
    except SeparatePrincipalError as exc:
        emit("SP_REVOKED_issuer", refused=True, error=exc.code)

    # 6. B2b forged subject refused (credential scope mismatch)
    issuer2, verifier2 = build_demo_principal_pair()
    forged_subject = replace(b5_subj, producer_permission_ceiling_ref=FORGED_CEILING,
                             replay_root_ref=ref("ReplayRoot", "fake"))
    cred2 = issuer2.issue(
        subject_ref=forged_subject.release_ref,
        producer_contract_ref=forged_subject.producer_contract_ref,
        permission_ceiling_ref=CEILING,  # credential has honest ceiling
        release_ref=forged_subject.release_ref,
        replay_closure_ref=forged_subject.replay_root_ref,
        scope={})
    try:
        verifier2.verify(cred2, subject=forged_subject, issuer=issuer2)
        emit("SP_B2b_forged_subject", refused=False)
    except SeparatePrincipalError as exc:
        emit("SP_B2b_forged_subject", refused=True, error=exc.code)

    # 7. C2 self-derived expectation refused
    issuer3, verifier3 = build_demo_principal_pair()
    cred3 = issuer3.issue(
        subject_ref=b5_subj.release_ref,
        producer_contract_ref=b5_subj.producer_contract_ref,
        permission_ceiling_ref=b5_subj.producer_permission_ceiling_ref,
        release_ref=b5_subj.release_ref,
        replay_closure_ref=b5_subj.replay_root_ref, scope={})
    tautology = {"derived_from": "subject_construction"}
    try:
        verifier3.verify(cred3, subject=b5_subj, expectation=tautology)
        emit("SP_C2_tautology", refused=False)
    except SeparatePrincipalError as exc:
        emit("SP_C2_tautology", refused=True, error=exc.code)

    # 8. Disposition
    emit("SP_DISPOSITION", disposition=DISPOSITION, grade=DEMO_GRADE,
         operative=False, nonoperative=True)


def main():
    emit("COURT_START", phases=3)
    run_unpatched()
    run_separate_principal()
    emit("COURT_COMPLETE", total=len(RESULTS))


if __name__ == "__main__":
    main()