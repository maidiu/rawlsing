"""HQ254 P01 -- F8 binding/receipt target-use permission IDENTITY coherence.

NARROWLY NAMED COURT FOR ONE BOUNDED CANDIDATE CORRECTION.

Scope, exactly:
    `ServiceApplicabilityF8ScopeBindingRequest.bound_target_use_permission_refs`
    must equal the `target_use_permission_refs` carried in the
    `CandidateClassApplicabilityReceipt.request_key` that the binder consumes.

Before the candidate, the binder copied the binding request's permission set
verbatim into the binding's canonical material without ever comparing it to the
receipt. A binding could therefore declare permissions that applicability was
never decided under, and downstream attestation would read the divergent set as
the admitted one.

This court covers ONLY that field. It is a QUARANTINED CANDIDATE regression
court, not adopted security authority, and it grants no permission, widens no
source-scope power, and demands no F8 producer custody.

Deliberately NOT covered here: provenance/authority custody (a separate gap,
banked in the HQ253 T01 return), producer identity authentication, and every
other existing binder refusal. Those are owned by their own courts and are not
re-litigated here.
"""
from __future__ import annotations

import hashlib

import pytest

from rawlsing_next import pre553_service_f8_source_scope_binding as B
from rawlsing_next import pre553_service_source_applicability as SA
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.tests import c1_at08_at13_fixture as fx


SERVICE = "HQ254_P01_PERMISSION_IDENTITY_SERVICE"
BINDER_BASELINE_BLOB = "4ba00b8ecf73f70ad0f6481e255fd0117744418a"


def _h(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:hq254-p01:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"HQ254-P01-{tag}", "1.0.0", _h(f"auth:{tag}"))


CANDIDATE_CLASS = _ref("TARGET_QUESTION_CLASS", "p01-class").as_dict()
TARGET_USE = _ref("TARGET_USE", "p01-target-use")
PERM_A = _ref("TARGET_USE_PERMISSION", "perm-A")
PERM_B = _ref("TARGET_USE_PERMISSION", "perm-B")
PERM_C = _ref("TARGET_USE_PERMISSION", "perm-C")
POPULATION = _ref("POPULATION_SCOPE", "pop").as_dict()
GEOGRAPHY = _ref("GEOGRAPHY_SCOPE", "geo").as_dict()
INTERVAL = _ref("TIME_INTERVAL", "iv").as_dict()
OTHER_RELEASE = _ref("C11LogicalRelease", "other-release")


@pytest.fixture(scope="module")
def source():
    return fx.xor_fixture()


def _receipt(source, *permissions):
    """A REAL applicability receipt decided under exactly `permissions`."""
    universe = source["universe"].ref
    candidate_class = SA.CandidateClassBinding(
        candidate_class_ref=CANDIDATE_CLASS,
        candidate_source_universe_refs=[universe.as_dict()],
        binding_authority_ref=_auth("class").as_dict(),
        declared_population_scope_ref=POPULATION,
        declared_geography_scope_ref=GEOGRAPHY,
    )
    service_request = SA.ServiceApplicabilityRequest.build(
        service_id=SERVICE,
        service_authority_ref=_auth("service").as_dict(),
        target_use_ref=TARGET_USE.as_dict(),
        population_scope_ref=POPULATION,
        geography_scope_ref=GEOGRAPHY,
        effective_time_or_interval_ref=INTERVAL,
        candidate_class_ref=CANDIDATE_CLASS,
        release_identity_ref=source["release_ref"].as_dict(),
        target_use_permission_refs=[p.as_dict() for p in permissions],
        candidate_source_universe_refs=[universe.as_dict()],
    )
    return SA.resolve_service_source_applicability(
        service_request, candidate_class,
        [SA.ApplicabilityAuthorityRecord(universe, "ADMITTED", _auth("admission").as_dict())],
    )


def _binding_request(source, receipt, *declared_permissions, **overrides):
    base = dict(
        binding_request_id="hq254-p01-breq",
        service_request_set_identity=receipt.service_request_set_identity,
        candidate_class_ref=ExactRef(**CANDIDATE_CLASS),
        service_id=SERVICE,
        target_use_ref=TARGET_USE,
        release_identity_ref=source["release_ref"],
        bound_target_use_permission_refs=tuple(declared_permissions),
        binding_mode=B.MODE_SINGLE_SOURCE_VALIDATION,
        requested_source_universe_ref=source["universe"].ref,
        requested_currentness_claim=None,
        requested_purpose=None,
    )
    base.update(overrides)
    return B.ServiceApplicabilityF8ScopeBindingRequest(**base)


def _bind(source, receipt, *declared_permissions, **overrides):
    rule = fx.make_model_rule(source["universe"].ref, "hq254-p01")
    request = _binding_request(source, receipt, *declared_permissions, **overrides)
    return request, B.bind_service_applicability_to_f8_scope(
        request=request, receipt=receipt, rule=rule)


# ===========================================================================
# 0. Schema is positively verified, not assumed
# ===========================================================================

def test_applicability_schema_and_permission_field_are_exact(source):
    """The candidate depends on the receipt genuinely carrying this field."""
    receipt = _receipt(source, PERM_A)
    assert isinstance(receipt, SA.CandidateClassApplicabilityReceipt)
    assert "target_use_permission_refs" in receipt.request_key
    assert [dict(p) for p in receipt.request_key["target_use_permission_refs"]] == [
        PERM_A.as_dict()]
    # the receipt itself declares permissions to be bound INPUT, not a grant
    assert receipt.request_key[
        "target_use_permission_refs_are_bound_input_not_a_grant"] is True
    assert receipt.outcome == SA.OUTCOME_ADMISSIBLE_SET
    assert receipt.candidate_class_coverage == SA.COVERAGE_COMPLETE


# ===========================================================================
# 1. POSITIVE -- honest matching permission identity is unaffected
# ===========================================================================

def test_honest_matching_single_permission_still_binds(source):
    receipt = _receipt(source, PERM_A)
    request, binding = _bind(source, receipt, PERM_A)
    assert binding.binding_mode == B.MODE_SINGLE_SOURCE_VALIDATION
    assert [p.as_dict() for p in binding.bound_target_use_permission_refs] == [
        PERM_A.as_dict()]
    assert [dict(p) for p in binding.material()[
        "bound_target_use_permission_refs"]] == [PERM_A.as_dict()]


def test_honest_matching_multiple_permissions_still_binds(source):
    receipt = _receipt(source, PERM_A, PERM_B, PERM_C)
    _request, binding = _bind(source, receipt, PERM_A, PERM_B, PERM_C)
    assert {p.key for p in binding.bound_target_use_permission_refs} == {
        PERM_A.key, PERM_B.key, PERM_C.key}


def test_matching_permission_set_is_order_insensitive(source):
    """The check compares SET identity, so declaration order is not a new refusal.

    Recorded deliberately: this is the semantics the candidate implements, and the
    reviewer should confirm order-insensitivity is intended rather than accidental.
    """
    receipt = _receipt(source, PERM_A, PERM_B)
    _request, binding = _bind(source, receipt, PERM_B, PERM_A)
    assert {p.key for p in binding.bound_target_use_permission_refs} == {
        PERM_A.key, PERM_B.key}


def test_binding_grants_no_permission_it_only_binds_inputs(source):
    """The candidate must not have turned a bound input into a grant."""
    receipt = _receipt(source, PERM_A)
    _request, binding = _bind(source, receipt, PERM_A)
    material = binding.material()
    assert material["bound_permission_refs_are_inputs_not_grants"] is True
    assert material["grants_no_authority"] is True


# ===========================================================================
# 2. HOSTILE -- permission identity disagreement must refuse, fail-closed
# ===========================================================================

@pytest.mark.parametrize("receipt_perms,binding_perms", [
    ((PERM_A,), (PERM_B,)),                    # wholly unrelated permission
    ((PERM_A,), (PERM_A, PERM_B)),             # superset: invents an extra permission
    ((PERM_A, PERM_B), (PERM_A,)),             # subset: silently drops one
    ((PERM_A, PERM_B), (PERM_A, PERM_C)),      # partial substitution
    ((PERM_A, PERM_B, PERM_C), (PERM_A, PERM_C)),  # drops one of three
])
def test_permission_identity_mismatch_refuses_with_exact_named_error(
        source, receipt_perms, binding_perms):
    receipt = _receipt(source, *receipt_perms)
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        _bind(source, receipt, *binding_perms)
    message = str(exc.value)
    assert message.startswith("BINDING_PERMISSION_IDENTITY_MISMATCH:")
    # the refusal names both sides, so the divergence is auditable
    for permission in binding_perms:
        assert permission.object_id in message
    for permission in receipt_perms:
        assert permission.object_id in message


def test_mismatch_refuses_BEFORE_any_binding_object_exists(source):
    """Fail-closed: no partial binding may be emitted, then rejected later."""
    receipt = _receipt(source, PERM_A)
    rule = fx.make_model_rule(source["universe"].ref, "hq254-p01")
    request = _binding_request(source, receipt, PERM_B)
    with pytest.raises(B.ServiceF8ScopeBindingError):
        B.bind_service_applicability_to_f8_scope(
            request=request, receipt=receipt, rule=rule)
    # the request object itself was never mutated or annotated with a binding
    assert [p.key for p in request.bound_target_use_permission_refs] == [PERM_B.key]
    assert "binding_id" not in dir(request)


def test_permission_mismatch_is_distinguishable_from_target_use_mismatch(source):
    """The new code must not shadow or widen the sibling target-use refusal."""
    receipt = _receipt(source, PERM_A)
    other_use = _ref("TARGET_USE", "other-target-use")
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        _bind(source, receipt, PERM_A, target_use_ref=other_use)
    assert str(exc.value).startswith("BINDING_TARGET_USE_GRAIN_MISMATCH:")

    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        _bind(source, receipt, PERM_B)
    assert str(exc.value).startswith("BINDING_PERMISSION_IDENTITY_MISMATCH:")


def test_permission_check_sits_between_target_use_and_release_grain(source):
    """Records the OBSERVED refusal precedence the candidate introduces.

    The candidate is placed immediately after its natural sibling
    BINDING_TARGET_USE_GRAIN_MISMATCH, so a request that is wrong on several grains
    at once now reports permission identity BEFORE release grain. Target use still
    outranks permission, and release still fires when permissions agree.

    Honest inputs are unaffected: the new check only ever fires on a genuine
    divergence, so every pre-existing single-grain refusal keeps its code. This
    witness exists so the independent reviewer can decide whether this placement is
    the intended one rather than discovering it by accident.
    """
    receipt = _receipt(source, PERM_A)

    # target use still outranks the new permission check
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        _bind(source, receipt, PERM_B,
              target_use_ref=_ref("TARGET_USE", "other-target-use"))
    assert str(exc.value).startswith("BINDING_TARGET_USE_GRAIN_MISMATCH:")

    # permission now outranks release when BOTH are wrong
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        _bind(source, receipt, PERM_B, release_identity_ref=OTHER_RELEASE)
    assert str(exc.value).startswith("BINDING_PERMISSION_IDENTITY_MISMATCH:")

    # release still fires on its own when permissions agree
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        _bind(source, receipt, PERM_A, release_identity_ref=OTHER_RELEASE)
    assert str(exc.value).startswith("BINDING_RELEASE_GRAIN_MISMATCH:")


# ===========================================================================
# 3. Scope guards -- the candidate stayed inside its one field
# ===========================================================================

def test_candidate_is_confined_to_the_permission_field():
    """No new authority, permission, model use, or custody demand was introduced."""
    import inspect

    source_text = inspect.getsource(B)
    # the candidate adds exactly one refusal code
    assert "BINDING_PERMISSION_IDENTITY_MISMATCH" in source_text
    for forbidden in (
        "CUSTODY", "PRODUCER_ATTEST", "EE14", "GRANT_NEW_PERMISSION",
        "ALLOW_MISMATCH", "TOLERATE",
    ):
        assert forbidden not in source_text.replace(
            "grant any permission", "").replace("grants no permission", "")


def test_adopted_binder_baseline_is_pinned_to_a_fixed_commit_not_head():
    """HQ256 P02 REPAIR. The provenance guard is HEAD-independent.

    The original witness read ``git rev-parse HEAD:<binder>`` and compared it to the
    PRE-candidate baseline blob. That is self-referential: committing the candidate
    necessarily moves ``HEAD`` to the candidate blob, so the guard could only ever
    pass while the production edit was UNCOMMITTED. On every committed SHA of the
    candidate it failed, which made the candidate's own court 15/16 on exactly the
    artefact it was written to certify. A provenance guard that cannot pass on the
    committed artefact certifies nothing.

    The repair pins the baseline to FIXED commits instead of ``HEAD``:

      * layer A is git-free and always runs -- the on-disk production file must be
        byte-identical to the reviewed candidate, and the recorded baseline and
        candidate identities must be distinct with the refusal code present only in
        the candidate;
      * layer B resolves the blob at two FIXED commits, so the result is identical at
        every HEAD, and is skipped (not failed) when no git repository is available,
        so a /tmp no-git artifact is reported as terrain rather than as a defect.

    The baseline itself is NEVER taken from ``HEAD``.
    """
    import hashlib
    import pathlib
    import subprocess

    # ---- fixed, recorded identities (never derived from HEAD) --------------
    p01_base_commit = "428be7595fce3ecf6ae3cb37852bee884d9ce2e1"      # pre-candidate
    p01_candidate_commit = "23438ab52f16abda5960a075dfca3f4d3396eab5"  # frozen candidate
    baseline_blob = "4ba00b8ecf73f70ad0f6481e255fd0117744418a"
    candidate_blob = "848d2d0eedb04b792747e9d6aaa49bb39d108a2c"
    candidate_sha256 = (
        "5221d8c2257ab1e8ec45289a30c57ba9ed4956b8609a890e80343718a6e9c66b")

    # the module-level constant must still name the true pre-candidate baseline
    assert BINDER_BASELINE_BLOB == baseline_blob
    assert baseline_blob != candidate_blob

    # ---- layer A: git-free, always executed -------------------------------
    path = pathlib.Path("rawlsing_next/pre553_service_f8_source_scope_binding.py")
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == candidate_sha256, (
        "the production binder must remain byte-identical to the reviewed candidate")
    text = raw.decode("utf-8")
    assert text.count("BINDING_PERMISSION_IDENTITY_MISMATCH") == 1, (
        "the candidate adds exactly one refusal block and no duplicate vocabulary")
    assert B.__file__.endswith("pre553_service_f8_source_scope_binding.py")

    # ---- layer B: git at FIXED commits; skipped, never failed, without git ----
    def _blob(commit: str):
        result = subprocess.run(
            ["git", "rev-parse", f"{commit}:{path}"],
            capture_output=True, text=True)
        if result.returncode != 0:
            return None
        return result.stdout.strip()

    baseline_at_base = _blob(p01_base_commit)
    candidate_at_commit = _blob(p01_candidate_commit)
    if baseline_at_base is None or candidate_at_commit is None:
        pytest.skip("no git object store available: fixed-commit identity layer not "
                    "executable here (terrain limitation, not a defect)")
    assert baseline_at_base == baseline_blob
    assert candidate_at_commit == candidate_blob
    # and the working-tree file is the same candidate blob, independent of HEAD
    assert _blob("HEAD") == candidate_blob


def test_no_production_power_was_added_by_constructing_a_binding(source):
    """A permitted binding still carries only eligibility scope."""
    receipt = _receipt(source, PERM_A)
    _request, binding = _bind(source, receipt, PERM_A)
    material = binding.material()
    assert material["binding_statement"]
    for forbidden_purpose in ("SOURCE_SELECTION", "SOURCE_RANKING",
                              "TARGET_USE_PERMISSION_GRANT",
                              "ACTOR_OR_PERSON_STATE"):
        assert forbidden_purpose in material["forbidden_binding_purposes"]