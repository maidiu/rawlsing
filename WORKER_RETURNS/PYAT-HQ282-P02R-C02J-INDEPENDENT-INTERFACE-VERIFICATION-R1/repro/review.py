"""Independent synthetic interface checks. FAIL means the named requirement failed.

Run against a Git archive of the pinned candidate, never the launch checkout.
No candidate or accepted-owner changes are made. Each case has fresh fixtures.
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace

from rawlsing_next.repro import c02j_owner_court as F
from rawlsing_next.repro import c02j_mandatory_overlay as O
from rawlsing_next import pre553_learned_product_lifecycle as B
from rawlsing_next import pre553_learned_product_release as M
from rawlsing_next.pre553_b5_owner_held_verifier_candidate import (
    OwnerHeldB5Verifier, PublicationRequest, RevocationLedger, OwnerHeldVerifierError,
)

rows = []
EV = dict(event_authority_ref=F.EVENT_AUTHORITY, event_rule_ref=F.EVENT_RULE)


def fixture(tag="review", **kw):
    repo = M.M2Repository()
    release, subject = F.build_m2(repo, tag=tag, **kw)
    custody = F.custody_for(repo, release, subject, slot="R")
    verifier = verifier_for(repo, custody)
    return repo, release, subject, custody, verifier


def verifier_for(repo, custody, ledger=None):
    return OwnerHeldB5Verifier(m2_repository=repo, custody={"R": custody},
        revocations=ledger, **EV)


def executor(repo, release, subject):
    ex = B.LearnedProductLifecycleExecutor()
    ex.stage_release(F.b5_subject_from_m2(repo, release, subject))
    ex.register_product(release.ref, **EV)
    ex.publish_product(release.ref, **EV)
    return ex


def activate(v):
    O.apply_mandatory_overlay()
    O.register_verifier(v)


def refused(call):
    try:
        call()
    except Exception as exc:
        return dict(rejected=True, error=type(exc).__name__,
                    reason=str(exc), refusal_class=getattr(exc, "refusal_class", None))
    return dict(rejected=False)


def check(name, criterion, call):
    try:
        result = call()
        ok = criterion(result)
        row = dict(case=name, status="PASS" if ok else "FAIL", observed=result)
    except Exception as exc:
        row = dict(case=name, status="FAIL", observed=dict(error=type(exc).__name__, reason=str(exc)))
    finally:
        O.remove_mandatory_overlay()
    rows.append(row)
    print(json.dumps(row, sort_keys=True, default=str), flush=True)


def normal(patched):
    repo, release, subject, custody, v = fixture()
    if patched:
        activate(v)
        receipt = v.publish(PublicationRequest("R"))
        return dict(authorizing=receipt.authorizing, current=receipt.current_selection_performed,
                    registered=bool(receipt.registered_event_key), published=bool(receipt.publication_event_key))
    ex = executor(repo, release, subject)
    return dict(publication=ex.lifecycle_state(release.ref).publication)


check("raw_normal_publication", lambda r: r["publication"] == "PUBLISHED", lambda: normal(False))
check("overlay_normal_non_authorizing", lambda r: r == dict(authorizing=False, current=False, registered=True, published=True), lambda: normal(True))


def mismatch(field):
    repo, release, subject, custody, v = fixture()
    expected = dict(custody.expected_identity)
    expected[field] = ("independent-other",) if isinstance(expected[field], tuple) else "independent-other"
    v = verifier_for(repo, replace(custody, expected_identity=expected))
    activate(v)
    return refused(lambda: v.publish(PublicationRequest("R")))


for field in ("release_key", "release_content_hash", "producer_subject_key", "product_key",
              "selection_scope_key", "authority_snapshot_keys", "permission_ceiling_key", "receipt_keys"):
    check("reject_expected_" + field, lambda r: r["rejected"], lambda field=field: mismatch(field))


def presented(field):
    repo, release, subject, custody, v = fixture()
    value = F.ref("Other", field)
    if field == "authority_snapshot_refs":
        value = (F.auth("other"),)
    elif field == "build_or_release_receipt_refs":
        value = (value,)
    candidate = replace(F.b5_subject_from_m2(repo, release, subject), **{field: value})
    activate(v)
    return refused(lambda: B.LearnedProductLifecycleExecutor().stage_release(candidate))


for field in ("release_ref", "product_ref", "producer_permission_ceiling_ref", "authority_snapshot_refs", "build_or_release_receipt_refs"):
    check("reject_presented_" + field, lambda r: r["rejected"], lambda field=field: presented(field))


def replacement(coordinated):
    original = fixture("original")
    repo, release, subject, custody, v = fixture("replacement")
    if not coordinated:
        v = verifier_for(repo, replace(custody, expected_identity=original[3].expected_identity))
    activate(v)
    result = refused(lambda: v.publish(PublicationRequest("R")))
    result["expectation_replaced"] = coordinated
    return result


check("separate_prior_expectation_rejects_replacement", lambda r: r["rejected"], lambda: replacement(False))
check("independent_authority_required_for_coordinated_replacement", lambda r: r["rejected"], lambda: replacement(True))


def self_declared_permission():
    repo, release, subject, custody, v = fixture()
    expected = dict(custody.expected_identity)
    expected["permission_ceiling_key"] = F.FORGED_CEILING.object_id
    v = verifier_for(repo, replace(custody, producer_permission_ceiling_ref=F.FORGED_CEILING,
                                   expected_identity=expected))
    activate(v)
    return refused(lambda: v.publish(PublicationRequest("R")))


check("independent_permission_required_for_matching_self_declaration", lambda r: r["rejected"], self_declared_permission)


def changed_repo():
    repo, release, subject, custody, v = fixture()
    alias = repo
    det = alias.closure_exact(release.determinant_closure_ref)
    object.__setattr__(det, "member_refs", det.member_refs + (F.ref("Edge", "added"),))
    activate(v)
    result = refused(lambda: v.publish(PublicationRequest("R")))
    result["same_repository"] = alias is v.held_repository()
    return result


check("alias_mutation_rejected_after_freeze", lambda r: r["rejected"] and r["same_repository"], changed_repo)


def event_refs(patched):
    repo, release, subject, custody, v = fixture()
    if patched:
        activate(v)
    ex = executor(repo, release, subject)
    result = refused(lambda: ex.record_recertification(release.ref,
        event_authority_ref=F.ref("EventAuthority", "unapproved"),
        event_rule_ref=F.ref("EventRule", "unapproved"), attestation_ref=F.ref("Attestation", "other")))
    result["events"] = len(ex.events)
    return result


for patched in (False, True):
    check(("overlay" if patched else "raw") + "_reject_unapproved_event_refs", lambda r: r["rejected"], lambda patched=patched: event_refs(patched))


def checkpoint(patched, modification=None, current=False):
    repo, release, subject, custody, v = fixture()
    if patched:
        activate(v)
    ex = executor(repo, release, subject)
    if current:
        key = ex.selection_key(product_family_ref=F.PRODUCT_FAMILY, selection_scope_ref=F.SELECTION_SCOPE,
                               selection_purpose_ref=F.ref("SelectionPurpose", "review"))
        ex.select_current(key.ref, release.ref, expected_previous_receipt_ref=None,
                          selection_attestation_ref=F.ref("Attestation", "review"), **EV)
    ck = json.loads(json.dumps(ex.export_checkpoint()))
    if modification == "truncated":
        ck["checkpoint_payload"]["events"] = ck["checkpoint_payload"]["events"][:1]
    elif modification == "incomplete":
        ck["checkpoint_payload"]["publication"] = []
    elif modification == "altered_state":
        ck["checkpoint_payload"]["publication"][0][1] = "REGISTERED"
    elif modification == "bad_hash":
        ck["checkpoint_hash"] = "0" * 64
    if modification and modification != "bad_hash":
        ck["checkpoint_hash"] = F.semantic_hash(ck["checkpoint_payload"])
    result = refused(lambda: B.LearnedProductLifecycleExecutor.from_checkpoint(ck))
    result["current_saved"] = current
    result["modification"] = modification
    return result


for patched in (False, True):
    prefix = "overlay" if patched else "raw"
    for current in (False, True):
        check(prefix + "_restore_valid_" + ("current" if current else "published"),
              lambda r: not r["rejected"], lambda patched=patched, current=current: checkpoint(patched, current=current))
    for mod in ("truncated", "incomplete", "altered_state", "bad_hash"):
        check(prefix + "_reject_checkpoint_" + mod, lambda r: r["rejected"],
              lambda patched=patched, mod=mod: checkpoint(patched, mod))


def revocation(kind):
    repo, release, subject, custody, v = fixture()
    kwargs = {}
    if kind == "release":
        kwargs["release_keys"] = frozenset([release.ref.object_id])
    elif kind == "authority":
        kwargs["authority_keys"] = frozenset([F.SEMANTIC_AUTH.authority_id])
    elif kind == "consumed":
        kwargs["authority_keys"] = frozenset([F.MODEL_AUTH.object_id])
    else:
        kwargs["replay_closure_keys"] = frozenset([release.replay_reconstruction_ref.object_id])
    v = verifier_for(repo, custody, RevocationLedger(**kwargs))
    activate(v)
    return refused(lambda: v.publish(PublicationRequest("R")))


for kind in ("release", "authority", "consumed", "replay"):
    check("reject_revoked_" + kind, lambda r: r["rejected"] and r["refusal_class"] == "AUTHORITY_REVOKED", lambda kind=kind: revocation(kind))


def replay(grade, complete):
    repo, release, subject, custody, v = fixture(replay_grade=grade)
    if not complete:
        object.__setattr__(repo.closure_exact(release.replay_reconstruction_ref), "complete", False)
    activate(v)
    return refused(lambda: v.publish(PublicationRequest("R")))


check("reject_obsolete_replay_grade", lambda r: r["rejected"], lambda: replay("HISTORICAL_EXPLANATION_ONLY", True))
check("reject_incomplete_replay", lambda r: r["rejected"], lambda: replay("EXACT_DETERMINISTIC_REBUILD", False))


def recert_revoked():
    repo, release, subject, custody, v = fixture()
    ex = executor(repo, release, subject)
    v = verifier_for(repo, custody, RevocationLedger(release_keys=frozenset([release.ref.object_id])))
    activate(v)
    return refused(lambda: ex.record_recertification(release.ref, attestation_ref=F.ref("Attestation", "review"), **EV))


check("recertification_checks_revocation", lambda r: r["rejected"], recert_revoked)


def withdraw_and_select():
    repo, release, subject, custody, v = fixture()
    activate(v)
    ex = executor(repo, release, subject)
    key = ex.selection_key(product_family_ref=F.PRODUCT_FAMILY, selection_scope_ref=F.SELECTION_SCOPE,
                           selection_purpose_ref=F.ref("SelectionPurpose", "review"))
    ex.withdraw_product(release.ref, withdrawal_reason_ref=F.ref("Reason", "review"),
        withdrawal_scope_ref=F.SELECTION_SCOPE, selection_attestation_ref=F.ref("Attestation", "review"), **EV)
    return refused(lambda: ex.select_current(key.ref, release.ref, expected_previous_receipt_ref=None,
        selection_attestation_ref=F.ref("Attestation", "review"), **EV))


check("withdrawn_release_not_selectable", lambda r: r["rejected"], withdraw_and_select)


def no_current_without_registry():
    repo, release, subject, custody, v = fixture()
    ex = executor(repo, release, subject)
    key = ex.selection_key(product_family_ref=F.PRODUCT_FAMILY, selection_scope_ref=F.SELECTION_SCOPE,
                           selection_purpose_ref=F.ref("SelectionPurpose", "review"))
    O.apply_mandatory_overlay()
    return refused(lambda: ex.declare_no_current(key.ref, expected_previous_receipt_ref=None,
        selection_attestation_ref=F.ref("Attestation", "review"), reason_ref=F.ref("Reason", "review"), **EV))


check("no_current_requires_registered_verifier", lambda r: r["rejected"], no_current_without_registry)


def withdraw_without_registry():
    repo, release, subject, custody, v = fixture()
    ex = executor(repo, release, subject)
    O.apply_mandatory_overlay()
    return refused(lambda: ex.withdraw_product(release.ref, withdrawal_reason_ref=F.ref("Reason", "review"),
        withdrawal_scope_ref=F.SELECTION_SCOPE, selection_attestation_ref=F.ref("Attestation", "review"), **EV))


check("withdrawal_requires_registered_verifier", lambda r: r["rejected"], withdraw_without_registry)


def m2_registration(route):
    repo, release, subject, custody, v = fixture()
    foreign = M.M2Repository()
    activate(v)
    if route == "low_level_foreign":
        return refused(lambda: foreign.register_subject(subject))
    return refused(lambda: M.register_producer_subject(repo, subject_ref=F.ref("LearnedSemanticProduct", "new"),
        subject_kind="IMMUTABLE_LEARNED_PRODUCT", producer_contract_ref=subject.producer_contract_ref,
        semantic_anatomy_ref=subject.semantic_anatomy_ref, typed_state="POSITIVE"))


for route in ("low_level_foreign", "new_subject_held_repo"):
    check("m2_restrict_" + route, lambda r: r["rejected"], lambda route=route: m2_registration(route))


def concurrent():
    repo, release, subject, custody, v = fixture()
    activate(v)
    with ThreadPoolExecutor(max_workers=4) as pool:
        receipts = list(pool.map(lambda _: v.publish(PublicationRequest("R")), range(8)))
    return dict(count=len(receipts), all_non_authorizing=all(not r.authorizing for r in receipts),
                same_event_identity=len({r.publication_event_key for r in receipts}) == 1)


check("stable_concurrent_facade_calls", lambda r: r == dict(count=8, all_non_authorizing=True, same_event_identity=True), concurrent)


def as_of(patched, by_checkpoint):
    repo, release, subject, custody, v = fixture()
    ex = executor(repo, release, subject)
    key = ex.selection_key(product_family_ref=F.PRODUCT_FAMILY, selection_scope_ref=F.SELECTION_SCOPE,
                           selection_purpose_ref=F.ref("SelectionPurpose", "review"))
    receipt = ex.select_current(key.ref, release.ref, expected_previous_receipt_ref=None,
        selection_attestation_ref=F.ref("Attestation", "review"), **EV)
    saved = ex.export_checkpoint()
    ex.withdraw_product(release.ref, withdrawal_reason_ref=F.ref("Reason", "review"),
        withdrawal_scope_ref=F.SELECTION_SCOPE, selection_attestation_ref=F.ref("Attestation", "review"),
        current_transitions={key.ref.key: None}, **EV)
    if patched:
        v = verifier_for(repo, custody, RevocationLedger(release_keys=frozenset([release.ref.object_id])))
        activate(v)
    kwargs = dict(as_of_checkpoint=saved) if by_checkpoint else dict(as_of_event_ref=receipt.current_select_event_ref)
    try:
        historical = ex.resolve_current_as_of(key.ref, **kwargs)
        return dict(historical=historical.state, current=ex.resolve_selection_exact(
            key.ref, ex.current_selection_receipt_ref(key.ref)).state, rejected=False)
    except Exception as exc:
        return dict(rejected=True, error=type(exc).__name__, reason=str(exc))


for patched in (False, True):
    for by_checkpoint in (False, True):
        check(("overlay" if patched else "raw") + "_historical_" + ("checkpoint" if by_checkpoint else "event"),
            lambda r: not r["rejected"] and r["historical"] == "CURRENT_SELECTED" and r["current"] == "NO_CURRENT",
            lambda patched=patched, by_checkpoint=by_checkpoint: as_of(patched, by_checkpoint))


def wrapper_unknown(method):
    repo, release, subject, custody, v = fixture()
    ex = executor(repo, release, subject)
    subject_b5 = F.b5_subject_from_m2(repo, release, subject)
    key = ex.selection_key(product_family_ref=F.PRODUCT_FAMILY, selection_scope_ref=F.SELECTION_SCOPE,
                           selection_purpose_ref=F.ref("SelectionPurpose", "review"))
    O.apply_mandatory_overlay()
    calls = {
        "stage_protocol": lambda: B.LearnedProductLifecycleExecutor().stage_protocol(subject_b5),
        "register_product": lambda: ex.register_product(release.ref, **EV),
        "publish_product": lambda: ex.publish_product(release.ref, **EV),
        "select_current": lambda: ex.select_current(key.ref, release.ref, expected_previous_receipt_ref=None,
            selection_attestation_ref=F.ref("Attestation", "review"), **EV),
        "record_recertification": lambda: ex.record_recertification(release.ref,
            attestation_ref=F.ref("Attestation", "review"), **EV),
    }
    return refused(calls[method])


for method in ("stage_protocol", "register_product", "publish_product", "select_current", "record_recertification"):
    check("unknown_registry_" + method, lambda r: r["rejected"] and r["refusal_class"] == "UNKNOWN_RELEASE",
          lambda method=method: wrapper_unknown(method))

for case, reason in (
    ("expiration_clock", "No expiry timestamp or clock gate in the candidate; not implemented."),
    ("concurrent_repository_mutation", "Not exercised; no synchronization demonstrated by stable concurrent reads."),
    ("live_independent_issuers", "No independent expectation, permission or revocation issuer available in this source-free scope."),
):
    row = dict(case=case, status="UNTESTED", reason=reason)
    rows.append(row)
    print(json.dumps(row, sort_keys=True))

counts = {status: sum(r["status"] == status for r in rows) for status in ("PASS", "FAIL", "SKIP", "UNTESTED")}
print(json.dumps(dict(summary=counts), sort_keys=True))
sys.exit(1 if counts["FAIL"] else 0)
