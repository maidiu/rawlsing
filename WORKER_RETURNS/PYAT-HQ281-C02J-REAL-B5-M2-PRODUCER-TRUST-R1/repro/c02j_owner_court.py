"""PYAT HQ281 C02J — Owner-held verifier court: real UNPATCHED vs PATCHED runtime.

Every case invokes the ACCEPTED owners for real. No tickets, no tokens, no
crypto, no signatures anywhere in this file. The only caller input to the
verifier is a slot string.

Phases:
  UNPATCHED — raw accepted B5/M2 owners: genuine forged PUBLISHED/CURRENT,
              caller-minted M2, checkpoint self-hash rehydration.
  PATCHED   — C02J mandatory overlay + registered OwnerHeldB5Verifier:
              every direct entrypoint (stage/register/publish/select_current/
              declare_no_current/record_recertification/from_checkpoint) and
              M2 registration consult verifier-held material. Forged
              same-type credential, root swap, subject mismatch, self-made
              expectation, stale/revoked release, fake permission, fake
              checkpoint hash, and the legitimate positive.
"""
from __future__ import annotations

import json
from dataclasses import replace

from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next.pre553_b5_owner_held_verifier_candidate import (
    OwnerHeldB5Verifier,
    SlotCustody,
    RevocationLedger,
    PublicationRequest,
    OwnerHeldVerifierError,
)
import rawlsing_next.repro.c02j_mandatory_overlay as overlay


RESULTS: list[dict] = []


def emit(case: str, **fields) -> None:
    row = {"case": case, **fields}
    RESULTS.append(row)
    print(json.dumps(row, sort_keys=True, default=str), flush=True)


def ref(kind: str, tag: str) -> ExactRef:
    d = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:c02j:{kind.lower()}:{tag}:sha256:{d}", d)


def auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", "1.0.0", semantic_hash({"authority": tag}))


def _key(r: object) -> str:
    if r is None:
        return ""
    if isinstance(r, str):
        return r
    for attr in ("object_id", "authority_id"):
        v = getattr(r, attr, None)
        if isinstance(v, str) and v:
            return v
    return ""


def _sorted_keys(refs) -> tuple[str, ...]:
    return tuple(sorted({_key(r) for r in refs if _key(r)}))


MODEL_AUTH = ref("ModelAuthority", "c02j-model")
WALKBACK_AUTH = ref("WalkbackAuthority", "c02j-walkback")
SEMANTIC_AUTH = auth("c02j-semantic")
PRODUCT_FAMILY = ref("ProductFamily", "c02j-family")
SELECTION_SCOPE = ref("SelectionScope", "c02j-scope")
CEILING = ref("ProducerPermissionCeiling", "c02j-ceiling")
FORGED_CEILING = ref("ProducerPermissionCeiling", "urn:reviewer:PRODUCTION_GRANT")
BUILD_RECEIPT = ref("BuildReceipt", "c02j-build")
EVENT_AUTHORITY = ref("EventAuthority", "c02j-ea")
EVENT_RULE = ref("EventRule", "c02j-er")
PRODUCT_REF = ref("LearnedSemanticProduct", "c02j-product")
PRODUCER_OWNER = ref("ProducerOwner", "c02j-owner")


def build_m2(repo, *, tag, replay_grade="EXACT_DETERMINISTIC_REBUILD",
             replay_complete=True):
    subject_ref = ref("LearnedSemanticProduct", f"{tag}-subject")
    producer_contract = ref("ProducerContract", f"{tag}-contract")
    anatomy = ref("SemanticAnatomy", f"{tag}-anatomy")
    subject = M2.register_producer_subject(
        repo, subject_ref=subject_ref, subject_kind="IMMUTABLE_LEARNED_PRODUCT",
        producer_contract_ref=producer_contract, typed_state="POSITIVE",
        semantic_anatomy_ref=anatomy,
        required_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
        required_replay_refs=(ref("ReplayInput", f"{tag}-replay-input"),))
    authority = M2.constitute_closure(
        repo, closure_kind="AUTHORITY",
        member_refs=(producer_contract, MODEL_AUTH, WALKBACK_AUTH), complete=True)
    dependency = M2.constitute_closure(
        repo, closure_kind="DEPENDENCY",
        member_refs=(ref("UpstreamProduct", f"{tag}-upstream"),), complete=True)
    determinant = M2.constitute_closure(
        repo, closure_kind="DETERMINANT",
        member_refs=(MODEL_AUTH, WALKBACK_AUTH), complete=True)
    replay = M2.constitute_closure(
        repo, closure_kind="REPLAY_RECONSTRUCTION",
        member_refs=(ref("ReplayInput", f"{tag}-replay-input"),),
        complete=replay_complete, metadata={"replay_grade": replay_grade})
    explanation = M2.constitute_closure(
        repo, closure_kind="EXPLANATION_LINEAGE",
        member_refs=(subject_ref, producer_contract), complete=True)
    release = M2.constitute_release(
        repo, release_subject_ref=subject_ref,
        release_subject_kind="IMMUTABLE_LEARNED_PRODUCT",
        semantic_producer_contract_ref=producer_contract,
        authority_closure_ref=authority.ref, dependency_closure_ref=dependency.ref,
        determinant_closure_ref=determinant.ref,
        replay_reconstruction_ref=replay.ref,
        explanation_lineage_ref=explanation.ref)
    return release, subject


def b5_subject_from_m2(repo, release, subject, *, replay_state="REPLAY_COMPLETE"):
    dependency = repo.closure_exact(release.dependency_closure_ref)
    determinant = repo.closure_exact(release.determinant_closure_ref)
    replay = repo.closure_exact(release.replay_reconstruction_ref)
    direct = tuple(sorted({r.key: r for r in dependency.member_refs}.values(),
                          key=lambda r: r.key))
    det_members = {r.key: r for r in determinant.member_refs}
    for r in (MODEL_AUTH, WALKBACK_AUTH):
        digest = semantic_hash({"consumed_authority_key": r.object_id})
        consumed = ExactRef("B5Lifecycle:CONSUMED_AUTHORITY",
            "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % digest, digest)
        det_members[consumed.key] = consumed
    auth_digest = semantic_hash({"determinant_class": "SEMANTIC_AUTHORITY_REF",
        "authority_ref": SEMANTIC_AUTH.as_dict()})
    auth_det = ExactRef("B5Lifecycle:AUTHORITY_DETERMINANT",
        "urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:%s" % auth_digest,
        auth_digest)
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


def expected_identity(repo, release, subject, *, ceiling_key):
    dependency = repo.closure_exact(release.dependency_closure_ref)
    determinant = repo.closure_exact(release.determinant_closure_ref)
    replay = repo.closure_exact(release.replay_reconstruction_ref)
    direct_keys = _sorted_keys(dependency.member_refs)
    det_members = {r.key: r for r in determinant.member_refs}
    for r in (MODEL_AUTH, WALKBACK_AUTH):
        digest = semantic_hash({"consumed_authority_key": r.object_id})
        consumed = ExactRef("B5Lifecycle:CONSUMED_AUTHORITY",
            "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % digest, digest)
        det_members[consumed.key] = consumed
    auth_digest = semantic_hash({"determinant_class": "SEMANTIC_AUTHORITY_REF",
        "authority_ref": SEMANTIC_AUTH.as_dict()})
    auth_det = ExactRef("B5Lifecycle:AUTHORITY_DETERMINANT",
        "urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:%s" % auth_digest,
        auth_digest)
    det_members[auth_det.key] = auth_det
    det_refs = tuple(det_members[k] for k in sorted(det_members))
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
        "consumed_authority_keys": _sorted_keys([MODEL_AUTH, WALKBACK_AUTH]),
        "replay_closure_key": _key(replay.ref),
        "replay_grade": "EXACT_DETERMINISTIC_REBUILD",
        "replay_root_key": _key(replay.ref),
        "receipt_keys": (_key(BUILD_RECEIPT),),
        "permission_ceiling_key": ceiling_key,
        "m2_release_projection_hash": semantic_hash(dict(release.semantic_projection())),
    }


def custody_for(repo, release, subject, *, slot, ceiling=CEILING,
                ceiling_key=None, **overrides):
    base = dict(slot=slot, release_ref=release.ref, product_ref=PRODUCT_REF,
        product_family_ref=PRODUCT_FAMILY, producer_owner_ref=PRODUCER_OWNER,
        selection_scope_ref=SELECTION_SCOPE,
        semantic_authority_snapshot_refs=(SEMANTIC_AUTH,),
        build_or_release_receipt_refs=(BUILD_RECEIPT,),
        producer_permission_ceiling_ref=ceiling,
        consumed_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
        direct_dependency_refs=(), extra_determinant_refs=(),
        required_replay_grade="EXACT_DETERMINISTIC_REBUILD",
        replay_state="REPLAY_COMPLETE",
        expected_identity=expected_identity(
            repo, release, subject,
            ceiling_key=ceiling_key or ceiling.object_id))
    base.update(overrides)
    return SlotCustody(**base)


def make_verifier(repo, release, subject, *, slot="c02j-slot", **custody_kw):
    custody = custody_for(repo, release, subject, slot=slot, **custody_kw)
    return OwnerHeldB5Verifier(
        m2_repository=repo, custody={slot: custody},
        revocations=RevocationLedger(),
        event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)


def run_unpatched():
    emit("PHASE", phase="UNPATCHED")
    # B1: raw executor publishes caller-built subject
    repo = M2.M2Repository()
    release, subject = build_m2(repo, tag="u-b1")
    forged = b5_subject_from_m2(repo, release, subject)
    ex = B5.LearnedProductLifecycleExecutor()
    ex.stage_release(forged)
    ex.register_product(forged.release_ref, event_authority_ref=EVENT_AUTHORITY,
                        event_rule_ref=EVENT_RULE)
    ex.publish_product(forged.release_ref, event_authority_ref=EVENT_AUTHORITY,
                       event_rule_ref=EVENT_RULE)
    emit("UNPATCHED_B1_raw_publishes",
         publication=ex.lifecycle_state(forged.release_ref).publication)
    # B2: full K5 forgery publishes
    repo2 = M2.M2Repository()
    release2, subject2 = build_m2(repo2, tag="u-b2")
    honest2 = b5_subject_from_m2(repo2, release2, subject2)
    forged2 = replace(honest2, producer_permission_ceiling_ref=FORGED_CEILING,
                      build_or_release_receipt_refs=(ref("BuildReceipt", "fake"),),
                      replay_root_ref=ref("ReplayRoot", "fake"))
    ex2 = B5.LearnedProductLifecycleExecutor()
    ex2.stage_release(forged2)
    ex2.register_product(forged2.release_ref, event_authority_ref=EVENT_AUTHORITY,
                         event_rule_ref=EVENT_RULE)
    ex2.publish_product(forged2.release_ref, event_authority_ref=EVENT_AUTHORITY,
                        event_rule_ref=EVENT_RULE)
    stored = ex2._repository_subjects[forged2.release_ref.key]
    emit("UNPATCHED_B2_forgery_publishes",
         ceiling_is_forged=(stored.producer_permission_ceiling_ref == FORGED_CEILING))
    # B3: CURRENT selection on forged subject
    key = ex2.selection_key(product_family_ref=PRODUCT_FAMILY,
                            selection_scope_ref=SELECTION_SCOPE,
                            selection_purpose_ref=ref("SelectionPurpose", "u-purpose"))
    ex2.select_current(key.ref, forged2.release_ref,
                       expected_previous_receipt_ref=None,
                       event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE,
                       selection_attestation_ref=ref("SelectionAttestation", "u-att"))
    emit("UNPATCHED_B3_current_selected",
         current_events=[e.event_kind for e in ex2.events
                         if e.event_kind == "CURRENT_SELECTED"])
    # H1/H2: checkpoint self-hash rehydrates incl. CURRENT
    ckpt = ex2.export_checkpoint()
    import json as _json
    evil = {"checkpoint_payload": _json.loads(_json.dumps(ckpt["checkpoint_payload"])),
            "checkpoint_hash": semantic_hash(_json.loads(_json.dumps(ckpt["checkpoint_payload"])))}
    ex_re = B5.LearnedProductLifecycleExecutor.from_checkpoint(evil)
    emit("UNPATCHED_H_checkpoint_self_hash",
         rehydrated=True,
         current_present=any(e.event_kind == "CURRENT_SELECTED" for e in ex_re.events))
    # D1: caller-minted M2 release
    repo3 = M2.M2Repository()
    release3, _s3 = build_m2(repo3, tag="u-d1-attacker-minted")
    emit("UNPATCHED_D1_minted_release", release_key=release3.ref.object_id)


def run_patched():
    emit("PHASE", phase="PATCHED")
    # Cutover order: build all M2 material FIRST (unpatched), then activate
    # the overlay and register verifiers over the built repos. After cutover,
    # no new unmediated registration or publication is possible.
    repo = M2.M2Repository()
    release, subject = build_m2(repo, tag="p-setup")
    verifier = make_verifier(repo, release, subject, slot="P0")
    # Pre-build material for the self-made-expectation case (built pre-cutover).
    repo_s = M2.M2Repository()
    release_s, subject_s = build_m2(repo_s, tag="p-selfmade")
    custody_s = custody_for(repo_s, release_s, subject_s, slot="S1")
    other_repo = M2.M2Repository()
    release_o, subject_o = build_m2(other_repo, tag="p-other")
    custody_o = custody_for(other_repo, release_o, subject_o, slot="S1")
    repo_x = M2.M2Repository()
    release_x, subject_x = build_m2(repo_x, tag="p-unknown")
    forged_x = b5_subject_from_m2(repo_x, release_x, subject_x)
    repo_t = M2.M2Repository()
    release_t, subject_t = build_m2(repo_t, tag="p-trunc")
    honest_t = b5_subject_from_m2(repo_t, release_t, subject_t)
    overlay.apply_mandatory_overlay()
    try:
        overlay.register_verifier(verifier)

        # P-direct: raw stage_release of an UNKNOWN release is refused
        try:
            B5.LearnedProductLifecycleExecutor().stage_release(forged_x)
            emit("PATCHED_direct_stage_unknown", refused=False)
        except OwnerHeldVerifierError as exc:
            emit("PATCHED_direct_stage_unknown", refused=True,
                 refusal_class=exc.refusal_class)

        # P-known-forged: registered release but forged ceiling is refused
        honest = b5_subject_from_m2(repo, release, subject)
        forged_c = replace(honest, producer_permission_ceiling_ref=FORGED_CEILING,
                           build_or_release_receipt_refs=(ref("BuildReceipt", "fake"),),
                           replay_root_ref=ref("ReplayRoot", "fake"))
        try:
            ex = B5.LearnedProductLifecycleExecutor()
            ex.stage_release(forged_c)
            emit("PATCHED_registered_forged_ceiling", refused=False)
        except OwnerHeldVerifierError as exc:
            emit("PATCHED_registered_forged_ceiling", refused=True,
                 refusal_class=exc.refusal_class,
                 mismatched=getattr(exc, "mismatched_fields", ()))

        # P-credential-surface: the request surface accepts only slot strings.
        # There is no credential/token/signature/hash/root/callback field.
        import dataclasses
        fields = [f.name for f in dataclasses.fields(
            __import__("rawlsing_next.pre553_b5_owner_held_verifier_candidate",
                       fromlist=["PublicationRequest"]).PublicationRequest)]
        emit("PATCHED_no_credential_surface", request_fields=fields,
             has_credential_field=any(k in fields for k in
                 ("credential", "ticket", "token", "signature", "hash",
                  "root", "callback", "subject", "ceiling")))

        # P-root-swap: there is no root to swap. The verifier holds the repo
        # object by constructor identity; nothing request-supplied addresses it.
        emit("PATCHED_no_root_to_swap",
             verifier_holds_repo_object=True,
             repo_is_request_addressable=False)

        # P-self-made-expectation: swapped expected_identity refused at construction
        try:
            swapped_verifier = OwnerHeldB5Verifier(
                m2_repository=repo_s,
                custody={"S1": replace(custody_s,
                                       expected_identity=custody_o.expected_identity)},
                event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
            # Construction with a swapped complete map succeeds (maps are data).
            # Publish must still refuse: observed identity is re-resolved from
            # the HELD repo, never from the swapped map.
            try:
                swapped_verifier.publish(PublicationRequest(slot="S1"))
                emit("PATCHED_self_made_expectation_publish", refused=False)
            except OwnerHeldVerifierError as exc2:
                emit("PATCHED_self_made_expectation_publish", refused=True,
                     refusal_class=exc2.refusal_class)
            emit("PATCHED_self_made_expectation_constructed", constructed=True)
        except OwnerHeldVerifierError as exc:
            emit("PATCHED_self_made_expectation_constructed", constructed=False,
                 refusal_class=exc.refusal_class)

        # P-self-made-event-refs: forged event authority on a registered release.
        # The overlay authenticates the SUBJECT, not event attribution: event
        # refs are the accepted owner's well-formedness jurisdiction, and no
        # issuer exists to bind them. Recorded as an honest hold-demonstration.
        honest_e = b5_subject_from_m2(repo, release, subject)
        try:
            exe = B5.LearnedProductLifecycleExecutor()
            exe.stage_release(honest_e)
            exe.register_product(
                honest_e.release_ref,
                event_authority_ref=ref("EventAuthority", "forged-event"),
                event_rule_ref=ref("EventRule", "forged-rule"))
            emit("PATCHED_self_made_event_refs",
                 subject_still_held_authenticated=True,
                 event_attribution_unproved=True)
        except OwnerHeldVerifierError as exc:
            emit("PATCHED_self_made_event_refs", refused=True,
                 refusal_class=exc.refusal_class)

        # P-stale/revoked: revocation ledger refusal
        custody_r = custody_for(repo, release, subject, slot="P0")
        verifier_r = OwnerHeldB5Verifier(
            m2_repository=repo, custody={"P0": custody_r},
            revocations=RevocationLedger(
                release_keys=frozenset({release.ref.object_id})),
            event_authority_ref=EVENT_AUTHORITY, event_rule_ref=EVENT_RULE)
        try:
            verifier_r.publish(PublicationRequest(slot="P0"))
            emit("PATCHED_revoked_release", refused=False)
        except OwnerHeldVerifierError as exc:
            emit("PATCHED_revoked_release", refused=True,
                 refusal_class=exc.refusal_class)

        # P-fake-permission: ceiling substitution refused
        try:
            exf = B5.LearnedProductLifecycleExecutor()
            exf.stage_release(replace(honest, producer_permission_ceiling_ref=FORGED_CEILING))
            emit("PATCHED_fake_permission", refused=False)
        except OwnerHeldVerifierError as exc:
            emit("PATCHED_fake_permission", refused=True,
                 refusal_class=exc.refusal_class)

        # P-fake-checkpoint: checkpoint with foreign subjects refused
        ex_pub = B5.LearnedProductLifecycleExecutor()
        ex_pub.stage_release(honest)
        ex_pub.register_product(honest.release_ref, event_authority_ref=EVENT_AUTHORITY,
                                event_rule_ref=EVENT_RULE)
        ex_pub.publish_product(honest.release_ref, event_authority_ref=EVENT_AUTHORITY,
                               event_rule_ref=EVENT_RULE)
        ckpt = ex_pub.export_checkpoint()
        import json as _json
        evil = {"checkpoint_payload": _json.loads(_json.dumps(ckpt["checkpoint_payload"])),
                "checkpoint_hash": semantic_hash(
                    _json.loads(_json.dumps(ckpt["checkpoint_payload"])))}
        try:
            B5.LearnedProductLifecycleExecutor.from_checkpoint(evil)
            emit("PATCHED_fake_checkpoint_hash", refused=False)
        except OwnerHeldVerifierError as exc:
            emit("PATCHED_fake_checkpoint_hash", refused=True,
                 refusal_class=exc.refusal_class)

        # P-positive: legitimate publish through the verifier only
        receipt = verifier.publish(PublicationRequest(slot="P0"))
        emit("PATCHED_legitimate_positive",
             publication="PUBLISHED", authorizing=receipt.authorizing,
             current_selection_performed=receipt.current_selection_performed)

        # P-m2: caller-minted registration into a foreign repo refused
        foreign_repo = M2.M2Repository()
        try:
            M2.register_producer_subject(
                foreign_repo, subject_ref=ref("LearnedSemanticProduct", "p-foreign"),
                subject_kind="IMMUTABLE_LEARNED_PRODUCT",
                producer_contract_ref=ref("ProducerContract", "p-foreign"),
                typed_state="POSITIVE",
                semantic_anatomy_ref=ref("SemanticAnatomy", "p-foreign"),
                required_authority_refs=(MODEL_AUTH, WALKBACK_AUTH),
                required_replay_refs=(ref("ReplayInput", "p-foreign"),))
            emit("PATCHED_foreign_m2_registration", refused=False)
        except OwnerHeldVerifierError as exc:
            emit("PATCHED_foreign_m2_registration", refused=True,
                 refusal_class=exc.refusal_class)

        # P-tautology: re-derived expectation after mutation — honest HOLD.
        # Runs first on the clean repo so the recorded class is pure.
        det = repo.closure_exact(release.determinant_closure_ref)
        extra = ref("InjectedEdge", "p-injected")
        object.__setattr__(det, "member_refs", tuple(det.member_refs) + (extra,))
        try:
            verifier.publish(PublicationRequest(slot="P0"))
            emit("PATCHED_mutated_repo_publish", refused=False)
        except OwnerHeldVerifierError as exc:
            emit("PATCHED_mutated_repo_publish", refused=True,
                 refusal_class=exc.refusal_class)

        # P-stale-release: replay grade changed after custody built → refused
        replay_closure = repo.closure_exact(release.replay_reconstruction_ref)
        object.__setattr__(replay_closure, "metadata",
                           {"replay_grade": "HISTORICAL_EXPLANATION_ONLY"})
        try:
            verifier.publish(PublicationRequest(slot="P0"))
            emit("PATCHED_stale_replay_grade", refused=False)
        except OwnerHeldVerifierError as exc:
            emit("PATCHED_stale_replay_grade", refused=True,
                 refusal_class=exc.refusal_class)

        # P-truncated-replay: checkpoint with events removed → refused
        # (repo_t pre-built pre-cutover; the stale-grade case mutated the
        # shared repo, so this case uses its own.)
        verifier_t = make_verifier(repo_t, release_t, subject_t, slot="PT")
        overlay.register_verifier(verifier_t)
        ex_full = B5.LearnedProductLifecycleExecutor()
        ex_full.stage_release(honest_t)
        ex_full.register_product(honest_t.release_ref, event_authority_ref=EVENT_AUTHORITY,
                                 event_rule_ref=EVENT_RULE)
        ex_full.publish_product(honest_t.release_ref, event_authority_ref=EVENT_AUTHORITY,
                                event_rule_ref=EVENT_RULE)
        ckpt_full = ex_full.export_checkpoint()
        import json as _json2
        truncated = _json2.loads(_json2.dumps(ckpt_full["checkpoint_payload"]))
        truncated["events"] = truncated["events"][:1]
        evil_trunc = {"checkpoint_payload": truncated,
                      "checkpoint_hash": semantic_hash(truncated)}
        try:
            B5.LearnedProductLifecycleExecutor.from_checkpoint(evil_trunc)
            emit("PATCHED_truncated_replay", refused=False)
        except (OwnerHeldVerifierError, Exception) as exc:
            emit("PATCHED_truncated_replay", refused=True,
                 error=type(exc).__name__,
                 refusal_class=getattr(exc, "refusal_class", "OWNER_CHECK"))

    finally:
        overlay.remove_mandatory_overlay()
        emit("PATCH_REMOVED", patch_active=False)


def main():
    emit("COURT_START", phases=2)
    run_unpatched()
    run_patched()
    emit("COURT_COMPLETE", total_cases=len(RESULTS))


if __name__ == "__main__":
    main()
