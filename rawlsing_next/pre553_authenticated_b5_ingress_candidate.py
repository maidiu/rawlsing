"""HQ280 PV3 C02 -- producer-authenticated B5 lifecycle publication ingress CANDIDATE.

DEVELOPMENT_CANDIDATE_ONLY. NONAUTHORIZING. G0b HELD. G1 HELD. CURRENT HELD.
NO SELF-ADOPTION. NOT A TRUST ROOT. NOT DEPLOYED SECURITY.
CONTRACT = "HQ280_C02_AUTHENTICATED_B5_INGRESS_CANDIDATE@1"

WHAT THIS IS
------------
A bounded, owner-controlled *perimeter* in front of the ACCEPTED B5 owner
(``rawlsing_next.pre553_learned_product_lifecycle``), for the exact gap independently
reproduced by HQ280 F8F (``aecc3273615ef158ae8428819d82d86d4cc64462``) and re-reproduced
here from actual owner invocations:

    4 of 5 caller-constructed subjects reached PUBLISHED **and** CURRENT_SELECTED,
    including one whose replay closure, receipts and replay root were entirely fabricated.

The B5 owner is, by its own module contract, an owner-internal runtime over *opaque*
exact learned-product releases: it explicitly "does not own producer semantics, M2
release-core semantics, AuthoritySnapshot maintenance, consumer permission...". So its
publication gate is necessarily a **well-formedness** gate over a caller-asserted
subject. That is correct for its jurisdiction and is NOT modified here. The defect is
that nothing between the producer and that gate binds the subject to anything the
producer actually issued.

This module supplies that missing edge and nothing else.

THE TRUST EDGE IS THE ACCEPTED M2 OWNER, NOT A NEW REGISTRAR
-------------------------------------------------------------
There is no accepted producer credential, no key registry and no signature scheme in the
repository, and this commission grants none. The smallest *existing* trusted ingress is
``rawlsing_next.pre553_learned_product_release`` (the adopted M2 ReleaseCore owner), which
already content-verifies its own releases and resolves exact closures out of a real
repository. C02 therefore makes the M2 owner the authority for:

  * ``release_ref``                  (ReleaseCore.ref, content-hash verified by M2)
  * ``producer_contract_ref``        (ReleaseCore.semantic_producer_contract_ref)
  * ``semantic_projection_hash``     (ProducerSubject.semantic_anatomy_ref.content_hash)
  * ``replay_root_ref``              (the M2 REPLAY_RECONSTRUCTION closure ref)
  * ``determinant_refs``             (M2 DETERMINANT closure members)
  * ``direct_dependency_refs``       (M2 DEPENDENCY closure members)

Owner custody supplies only what no accepted owner exists to supply, and each such field
is additionally bound by a closed, non-mutable, field-by-field expectation. See
``BOUNDED RESIDUALS`` for exactly what remains unproven.

THE PUBLIC SURFACE IS DATA-ONLY
-------------------------------
``publish(request)`` accepts exactly one closed builtin dataclass carrying exactly one
field: an owner-registered slot name. It cannot receive a subject, a release ref, an
authority, a closure, a receipt, a replay root, a permission ceiling, a currentness
claim, a hash, a callback, or any object at all. There is no field through which a
forged identity can enter, which is the structural point: the F8F/K4-K5 forgeries were
all *subject* forgeries, and a data-only surface has no subject.

ENFORCEMENT POINT
-----------------
Refusal happens BEFORE the first B5 call. Every typed error carries ``b5_invoked`` so a
caller can distinguish "refused at the ingress perimeter" from "the B5 owner refused".
The accepted B5 owner and the accepted M2 owner are imported and called unmodified.

BOUNDARY PRESERVED: TECHNICAL AUTHENTICITY != SCIENTIFIC COMPETENCE
-------------------------------------------------------------------
This ingress proves that a B5-published subject *corresponds to* material the M2 owner
actually issued, and nothing else. It does NOT decide, assert or imply that the producer
was competent to issue it. Every receipt is stamped::

    authorizing=False, grant=None, g0b=None, g1_service=None,
    scientific_competence_claim="NONE__TECHNICAL_PRODUCT_AUTHENTICITY_ONLY"

No current selection is performed anywhere in this module, and no currentness claim is
accepted on the request surface, because no operative CURRENT publication is granted.

BOUNDED RESIDUALS -- exactly what is frozen, and what is not
------------------------------------------------------------
FROZEN (deeply, at every level): the owner-held expectation map, the slot table, and the
custody container. Item assignment, deletion and the mutating mapping methods are all
refused on them.

NOT FROZEN: the ``M2Repository`` and the ``AuthorityRef``/``ExactRef`` objects inside the
custody material remain the owner's own shared objects. Deep-converting them would change
the semantic ref objects the accepted M2/B5 owners consume, which is out of scope here.
Consequently a caller cannot reach them through the public surface, but an in-process
principal that already holds one can still mutate it. This is a trusted-harness
limitation; it is not a custody root, not a trust root, and not deployed security.

R1. The semantic ``authority_snapshot_refs`` are OWNER-HELD, not issuer-held. No accepted
    AuthoritySnapshot issuer exists in the repository, and C02 invents none. They are
    frozen and expectation-bound, which is an internal completeness invariant, not
    independent proof of authority issuance. A competent producer issuer remains the
    open prerequisite F8F recorded.

R2. ``REPLAY_COMPLETE`` remains an owner-held CLAIM about replay, not an independent
    replay re-execution. C02 binds it to the M2 replay closure's own ``replay_grade`` and
    to the closed expectation, and refuses a non-accepted grade, but it does not re-run
    the replay. ``HISTORICAL_EXPLANATION_ONLY`` grades remain permitted and must not be
    read as serving-grade replay.

R3. The expectation is authored from the same construction it authenticates, so it is a
    drift guard and a tamper detector, not an independent preimage. An in-process
    principal able to rewrite both custody and expectation is explicitly UNPROVED.

R4. This module does not defend against an attacker executing arbitrary Python inside the
    owner process. The threat model is exactly the bounded data-only external caller of
    F8F K4-K5, widened to "a caller that may reach the C02 public surface".

G1_INTERNAL_OWNER_PATH_CANDIDATE_ONLY / C02_DEVELOPMENT_CANDIDATE_ONLY.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    semantic_hash,
)

CONTRACT = "HQ280_C02_AUTHENTICATED_B5_INGRESS_CANDIDATE@1"
DEVELOPMENT_GRADE = "SOURCE_FREE_CANDIDATE_ONLY__NONAUTHORIZING__G0B_HELD__G1_HELD__CURRENT_HELD"
TECHNICAL_ONLY_NOTE = (
    "Technical product authenticity only. This is NOT a scientific, model or use "
    "competence judgement, NOT a G0b grant, NOT a G1 selected service, and NOT an "
    "operative CURRENT publication."
)

#: Replay grades that may gate a publication. Mirrors M2's own accepted vocabulary; a
#: grade outside this set is refused before B5 is reached.
ACCEPTED_REPLAY_GRADES = frozenset({
    "EXACT_MATERIALIZED_DEREFERENCE",
    "EXACT_DETERMINISTIC_REBUILD",
    "EXACT_SERVICE_REEXECUTION",
    "HISTORICAL_EXPLANATION_ONLY",
})

#: The single B5 replay state the ingress will carry forward for publication. Any other
#: owner-held state is refused rather than relabelled.
PUBLISHABLE_REPLAY_STATE = "REPLAY_COMPLETE"

#: The only B5 publication state a receipt may report. Structurally unreachable for a
#: technical-only candidate.
FORBIDDEN_SELECTION_EVENT_KINDS = frozenset({
    "CURRENT_SELECTED",
    "CURRENT_SUPERSEDED",
    "CURRENT_CLEARED",
})

# ---------------------------------------------------------------------------
# The closed, exact expected-identity key set.
#
# Every one of these is compared on every admitted publish. A field is never skipped
# because it is absent from the expectation (that was HQ263 R01 F3 / HQ268 D1 in the
# accepted G1 owner, and the same failure mode is reproduced here deliberately).
# ---------------------------------------------------------------------------
REQUIRED_EXPECTATION_KEYS = frozenset({
    "release_key",
    "release_content_hash",
    "producer_subject_key",
    "producer_contract_key",
    "semantic_anatomy_key",
    "semantic_projection_hash",
    "product_key",
    "product_family_key",
    "producer_owner_key",
    "selection_scope_key",
    "authority_snapshot_keys",
    "direct_dependency_keys",
    "determinant_keys",
    "determinant_set_hash",
    "consumed_authority_keys",
    "replay_closure_key",
    "replay_grade",
    "replay_root_key",
    "receipt_keys",
    "permission_ceiling_key",
    "m2_release_projection_hash",
})

#: Exact builtin type required for each expected value. ``type(v) is T`` (never
#: isinstance) so a ``bool`` cannot satisfy a str field and no subclass slips through.
EXPECTATION_KEY_TYPES = {
    "release_key": str,
    "release_content_hash": str,
    "producer_subject_key": str,
    "producer_contract_key": str,
    "semantic_anatomy_key": str,
    "semantic_projection_hash": str,
    "product_key": str,
    "product_family_key": str,
    "producer_owner_key": str,
    "selection_scope_key": str,
    "authority_snapshot_keys": tuple,
    "direct_dependency_keys": tuple,
    "determinant_keys": tuple,
    "determinant_set_hash": str,
    "consumed_authority_keys": tuple,
    "replay_closure_key": str,
    "replay_grade": str,
    "replay_root_key": str,
    "receipt_keys": tuple,
    "permission_ceiling_key": str,
    "m2_release_projection_hash": str,
}

#: Refusal classes the ingress must be able to raise and that a caller must be able to
#: distinguish. B5 must not have been invoked for any of them.
REFUSAL_CLASSES = (
    "REQUEST_SURFACE_VIOLATION",
    "CUSTODY_INCOMPLETE",
    "AUTHORITY_REVOKED",
    "RELEASE_REVOKED",
    "M2_RESOLUTION_REFUSED",
    "EXPECTATION_INCOMPLETE",
    "IDENTITY_AUTHENTICATION_FAILED",
    "DETERMINANT_CLOSURE_INCOMPLETE",
    "REPLAY_CLOSURE_REFUSED",
)


class AuthenticatedB5IngressError(Exception):
    """Typed refusal from the authenticated B5 ingress perimeter."""

    refusal_class = "INGRESS_ERROR"

    def __init__(self, message: str, *, b5_invoked: bool = False) -> None:
        super().__init__(message)
        #: False for every perimeter refusal: the accepted B5 owner was not reached.
        self.b5_invoked = b5_invoked


class B5IngressRequestError(AuthenticatedB5IngressError):
    """The data-only publication request violated its closed contract."""

    refusal_class = "REQUEST_SURFACE_VIOLATION"


class B5IngressCustodyError(AuthenticatedB5IngressError):
    """Owner-held producer custody material is incomplete or unusable."""

    refusal_class = "CUSTODY_INCOMPLETE"


class B5IngressRevocationError(B5IngressCustodyError):
    """An exact release or consumed authority is revoked for this ingress."""

    refusal_class = "AUTHORITY_REVOKED"


class B5IngressM2Error(AuthenticatedB5IngressError):
    """The accepted M2 ReleaseCore owner refused to resolve the exact release."""

    refusal_class = "M2_RESOLUTION_REFUSED"

    def __init__(self, message: str, *, m2_code: str) -> None:
        super().__init__(message)
        self.m2_code = m2_code


class B5IngressAuthenticationError(AuthenticatedB5IngressError):
    """Constructed subject failed deep authentication against owner-held material.

    Raised BEFORE the first B5 call, so a forged identity can never reach publication or
    selection. ``mismatched_fields`` carries every expected key that failed; ``missing_keys``
    carries only the absent subset, so an incomplete owner setup stays distinguishable
    from a complete expectation holding a different value.
    """

    refusal_class = "IDENTITY_AUTHENTICATION_FAILED"

    def __init__(self, message: str, *, mismatched_fields: tuple[str, ...],
                 missing_keys: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.mismatched_fields = tuple(mismatched_fields)
        self.missing_keys = tuple(missing_keys)


class B5IngressDeterminantError(AuthenticatedB5IngressError):
    """The M2 determinant closure is empty or does not cover the consumed authorities."""

    refusal_class = "DETERMINANT_CLOSURE_INCOMPLETE"


class B5IngressReplayError(AuthenticatedB5IngressError):
    """The M2 replay reconstruction closure refused to gate publication."""

    refusal_class = "REPLAY_CLOSURE_REFUSED"


def _deep_freeze(value: Any) -> Any:
    """Recursively convert owner-held material into immutable builtins."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _deep_freeze(v) for k, v in dict(value).items()})
    if isinstance(value, (list, tuple)):
        return tuple(_deep_freeze(v) for v in value)
    if isinstance(value, set):
        return frozenset(_deep_freeze(v) for v in value)
    return value


def _key(ref: Any) -> str:
    """Stable key for ExactRef / AuthorityRef / plain ref-like values."""
    if ref is None:
        return ""
    if isinstance(ref, str):
        return ref
    for attr in ("object_id", "authority_id"):
        value = getattr(ref, attr, None)
        if isinstance(value, str) and value:
            return value
    if isinstance(ref, Mapping):
        for field in ("object_id", "authority_id"):
            value = ref.get(field)
            if isinstance(value, str) and value:
                return value
    return ""


def _sorted_keys(refs: Iterable[Any]) -> tuple[str, ...]:
    return tuple(sorted({_key(ref) for ref in refs if _key(ref)}))


def _require_complete_expectation(expected: Any, slot: str) -> None:
    """Fail-closed gate: the owner expectation must be complete, exact and typed.

    Called at ingress construction for every registered slot AND again immediately before
    the field-by-field comparison, so a partially populated expectation can never produce
    a vacuous pass and can never reach B5.
    """
    if type(expected) is not dict and type(expected) is not MappingProxyType:
        raise B5IngressAuthenticationError(
            "owner-held expected identity for slot %r must be a plain mapping; got %s"
            % (slot, type(expected).__name__),
            mismatched_fields=("expected_identity",),
            missing_keys=tuple(sorted(REQUIRED_EXPECTATION_KEYS)),
        )
    missing = tuple(sorted(REQUIRED_EXPECTATION_KEYS - set(expected)))
    if missing:
        raise B5IngressAuthenticationError(
            "owner-held expected identity for slot %r is INCOMPLETE (%d of %d required "
            "keys absent); authentication may not proceed vacuously. missing: %s"
            % (slot, len(missing), len(REQUIRED_EXPECTATION_KEYS), ", ".join(missing)),
            mismatched_fields=missing,
            missing_keys=missing,
        )
    extraneous = tuple(sorted(set(expected) - REQUIRED_EXPECTATION_KEYS))
    if extraneous:
        raise B5IngressAuthenticationError(
            "owner-held expected identity for slot %r carries %d key(s) outside the exact "
            "required set; unknown: %s"
            % (slot, len(extraneous), ", ".join(extraneous)),
            mismatched_fields=extraneous,
            missing_keys=(),
        )
    mistyped = tuple(sorted(
        k for k in REQUIRED_EXPECTATION_KEYS
        if type(expected[k]) is not EXPECTATION_KEY_TYPES[k]
    ))
    if mistyped:
        raise B5IngressAuthenticationError(
            "owner-held expected identity for slot %r carries wrong builtin types for: %s"
            % (slot, ", ".join(
                "%s (expected %s, got %s)"
                % (k, EXPECTATION_KEY_TYPES[k].__name__, type(expected[k]).__name__)
                for k in mistyped)),
            mismatched_fields=mistyped,
            missing_keys=(),
        )


@dataclass(frozen=True)
class PublicationRequest:
    """The COMPLETE data-only publication surface.

    One closed field. There is no field through which a subject, release ref, authority,
    closure, receipt, replay root, permission ceiling, currentness claim, hash, callback
    or any other object can be supplied.
    """

    slot: str


@dataclass(frozen=True)
class ProducerCustodyMaterial:
    """OWNER-HELD per-slot producer custody.

    Only fields with no accepted owner exist here. Every M2-owned field is absent by
    construction: release identity, producer contract, semantic anatomy, replay root,
    determinant and dependency closure members are all read from the accepted M2
    ``M2Repository`` at publish time, never from this record and never from a caller.
    """

    slot: str
    release_ref: ExactRef
    product_ref: ExactRef
    product_family_ref: ExactRef
    producer_owner_ref: ExactRef
    selection_scope_ref: ExactRef
    #: Semantic AuthoritySnapshot refs. OWNER-HELD, not issuer-held -- see residual R1.
    semantic_authority_snapshot_refs: tuple[AuthorityRef, ...]
    build_or_release_receipt_refs: tuple[ExactRef, ...]
    #: Owner-held permission ceiling. Never derived from a caller, never from the subject.
    producer_permission_ceiling_ref: ExactRef
    #: Model / walkback authorities this product CONSUMES. Each must also appear as a
    #: determinant edge (F8E H04 lesson) and must not be revoked.
    consumed_authority_refs: tuple[ExactRef | AuthorityRef, ...]
    #: Custody supplements the M2 DEPENDENCY closure with.
    direct_dependency_refs: tuple[ExactRef, ...]
    #: Custody supplements the M2 DETERMINANT closure with.
    extra_determinant_refs: tuple[ExactRef, ...]
    #: The replay grade this slot REQUIRES the M2 replay closure to declare.
    required_replay_grade: str
    #: Owner-held replay state claim. See residual R2 -- an authenticated claim, not a
    #: re-executed replay.
    replay_state: str
    #: The COMPLETE, closed, exact expected identity for this slot.
    expected_identity: Mapping[str, Any]


@dataclass(frozen=True)
class RevocationLedger:
    """OWNER-HELD exact revocation sets.

    Exactness only: a member must match by exact ref key. An empty set means nothing is
    revoked, which is an owner assertion and not proof that nothing is revoked.
    """

    release_keys: frozenset = frozenset()
    authority_keys: frozenset = frozenset()
    replay_closure_keys: frozenset = frozenset()


@dataclass(frozen=True)
class B5IngressReceipt:
    """TECHNICAL ingress-authenticity receipt. NOT a grant, NOT a root, NOT proof.

    Binds the exact M2-issued material the ingress authenticated, the closed expectation
    it authenticated against, and the exact B5 events it committed. A caller who retains
    only the published release ref cannot reconstruct any of it.
    """

    contract: str
    development_grade: str
    slot: str
    release_key: str
    release_content_hash: str
    producer_subject_key: str
    producer_contract_key: str
    semantic_anatomy_key: str
    determinant_keys: tuple[str, ...]
    determinant_set_hash: str
    replay_closure_key: str
    replay_grade: str
    replay_root_key: str
    receipt_keys: tuple[str, ...]
    permission_ceiling_key: str
    authority_snapshot_keys: tuple[str, ...]
    consumed_authority_keys: tuple[str, ...]
    registered_event_key: str
    publication_event_key: str
    ingress_authentication_hash: str
    #: Structurally always False/None here. CURRENT stays HELD.
    current_selection_performed: bool
    current_selection_receipt_ref: None
    authorizing: bool = False
    grant: None = None
    g0b: None = None
    g1_service: None = None
    scientific_competence_claim: str = "NONE__TECHNICAL_PRODUCT_AUTHENTICITY_ONLY"
    technical_only_note: str = TECHNICAL_ONLY_NOTE


class AuthenticatedB5Ingress:
    """Owner-controlled, data-only ingress in front of the ACCEPTED B5 owner.

    Construction is a TRUSTED HARNESS operation: it registers the accepted M2
    repository, the owner custody per slot, the revocation ledger and the complete
    expected identities. The public surface is ``publish(PublicationRequest)`` and is
    data-only.
    """

    def __init__(
        self,
        *,
        m2_repository: M2.M2Repository,
        custody: Mapping[str, ProducerCustodyMaterial],
        revocations: RevocationLedger | None = None,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
    ) -> None:
        """TRUSTED HARNESS SETUP ONLY -- never remote, never data-only."""
        if type(m2_repository) is not M2.M2Repository:
            raise B5IngressCustodyError(
                "owner setup must register the accepted M2Repository exactly; got %s"
                % type(m2_repository).__name__
            )
        if not isinstance(custody, Mapping) or not custody:
            raise B5IngressCustodyError(
                "owner setup must register a non-empty slot table of producer custody"
            )
        if not isinstance(event_authority_ref, ExactRef) or \
                not isinstance(event_rule_ref, ExactRef):
            raise B5IngressCustodyError(
                "owner setup must register exact event authority and event rule refs"
            )
        self._m2 = m2_repository
        self._event_authority_ref = event_authority_ref
        self._event_rule_ref = event_rule_ref
        self._revocations = revocations or RevocationLedger()

        normalised: dict[str, ProducerCustodyMaterial] = {}
        for slot, material in dict(custody).items():
            if type(slot) is not str or not slot:
                raise B5IngressCustodyError("slot names must be exact non-empty builtin str")
            if type(material) is not ProducerCustodyMaterial:
                raise B5IngressCustodyError(
                    "slot %r custody must be the exact builtin ProducerCustodyMaterial; "
                    "got %s" % (slot, type(material).__name__)
                )
            if material.slot != slot:
                raise B5IngressCustodyError(
                    "custody for slot %r declares a different slot %r" % (slot, material.slot)
                )
            if not material.semantic_authority_snapshot_refs:
                raise B5IngressCustodyError(
                    "slot %r custody carries no semantic AuthoritySnapshot refs" % slot
                )
            if not material.build_or_release_receipt_refs:
                raise B5IngressCustodyError(
                    "slot %r custody carries no build/release receipt refs" % slot
                )
            if material.required_replay_grade not in ACCEPTED_REPLAY_GRADES:
                raise B5IngressCustodyError(
                    "slot %r requires replay grade %r which is outside the accepted M2 "
                    "vocabulary" % (slot, material.required_replay_grade)
                )
            # Complete/exact/typed expectation, refused here so an incomplete owner setup
            # can never reach a request, let alone B5. Re-checked immediately before the
            # comparison as well.
            _require_complete_expectation(material.expected_identity, slot)
            normalised[slot] = material
        # read-only container: item assignment / deletion / mutating methods all refused
        self._custody = MappingProxyType(normalised)
        self._expected = MappingProxyType({
            slot: _deep_freeze(dict(normalised[slot].expected_identity))
            for slot in normalised
        })

    # -- trusted-harness introspection (read-only, NOT a public data surface) --

    def slots(self) -> tuple[str, ...]:
        return tuple(sorted(self._custody))

    def development_grade(self) -> str:
        return DEVELOPMENT_GRADE

    def owner_custody_projection(self) -> Mapping[str, Any]:
        """Read-only projection of the frozen owner material."""
        return _deep_freeze({
            "contract": CONTRACT,
            "development_grade": DEVELOPMENT_GRADE,
            "slots": {
                slot: {
                    "release_key": _key(material.release_ref),
                    "product_key": _key(material.product_ref),
                    "permission_ceiling_key": _key(material.producer_permission_ceiling_ref),
                    "required_replay_grade": material.required_replay_grade,
                    "expected_identity": self._expected[slot],
                }
                for slot, material in sorted(self._custody.items())
            },
            "revoked_release_keys": sorted(self._revocations.release_keys),
            "revoked_authority_keys": sorted(self._revocations.authority_keys),
            "revoked_replay_closure_keys": sorted(
                self._revocations.replay_closure_keys),
        })

    def accepted_expected_identity(self, slot: str) -> Mapping[str, Any]:
        """Owner-held expected identity for a slot. Read-only."""
        if slot not in self._expected:
            raise B5IngressRequestError("slot %r is not registered by the owner" % slot)
        return self._expected[slot]

    # -------------------------------------------------------------- public surface

    def publish(self, request: Any) -> B5IngressReceipt:
        """The ONLY public entrypoint. Data-only.

        A refusal here happens strictly BEFORE the first accepted-B5 call, so no forged
        identity can reach publication or selection.
        """
        req = self._validate_request(request)
        material = self._custody.get(req.slot)
        if material is None:
            raise B5IngressRequestError(
                "slot %r is not registered by the owner" % req.slot
            )
        return self._publish_registered(req.slot, material)

    # ------------------------------------------------------------- internals

    @staticmethod
    def _validate_request(request: Any) -> PublicationRequest:
        """Enforce the data-only contract with EXACT builtin types.

        Refuses subclasses of ``PublicationRequest`` and of ``str``, and refuses any
        request object carrying fields beyond the closed set, so the public method really
        does accept only plain builtin scalars.
        """
        if type(request) is not PublicationRequest:
            raise B5IngressRequestError(
                "authenticated B5 ingress accepts only the exact builtin "
                "PublicationRequest data-only shape (subclasses are refused); got %s"
                % type(request).__name__
            )
        if type(request.slot) is not str or not request.slot:
            raise B5IngressRequestError(
                "request slot must be an exact builtin non-empty str"
            )
        extra = set(vars(request)) - {"slot"}
        if extra:
            raise B5IngressRequestError(
                "request carries field(s) outside the closed data-only set: %s"
                % ", ".join(sorted(extra))
            )
        return request

    def _revocation_check(self, material: ProducerCustodyMaterial, release_key: str,
                          authority_keys: tuple[str, ...],
                          consumed_keys: tuple[str, ...],
                          replay_closure_key: str) -> None:
        """Exact revocation gate, before any B5 call."""
        revoked = self._revocations
        if release_key in revoked.release_keys:
            raise B5IngressRevocationError(
                "release %s is revoked for this ingress; publication is refused before "
                "B5" % release_key
            )
        hit = sorted(set(authority_keys) & set(revoked.authority_keys))
        if hit:
            raise B5IngressRevocationError(
                "semantic authority ref(s) %s are revoked; publication is refused before "
                "B5" % ", ".join(hit)
            )
        hit = sorted(set(consumed_keys) & set(revoked.authority_keys))
        if hit:
            raise B5IngressRevocationError(
                "consumed model/walkback authority ref(s) %s are revoked; publication is "
                "refused before B5" % ", ".join(hit)
            )
        if replay_closure_key in revoked.replay_closure_keys:
            raise B5IngressRevocationError(
                "M2 replay reconstruction closure %s is revoked; publication is refused "
                "before B5" % replay_closure_key
            )

    def _resolve_m2(self, material: ProducerCustodyMaterial) -> dict[str, Any]:
        """Resolve the exact release through the ACCEPTED M2 owner, unmodified.

        The caller never supplies the release ref, the bindings or the locator; the
        ingress supplies owner custody refs and an empty binding list, so no
        representation/locator graft is reachable from the public surface.
        """
        try:
            resolution = M2.resolve_release_exact(
                self._m2, material.release_ref, publication_binding_refs=(),
            )
        except M2.M2ReleaseError as exc:
            raise B5IngressM2Error(
                "accepted M2 owner refused the exact release for slot %r: %s"
                % (material.slot, exc),
                m2_code=exc.code,
            ) from exc
        release = resolution.release_core
        subject = resolution.subject
        if subject is None:
            raise B5IngressM2Error(
                "accepted M2 owner resolved no producer subject for slot %r"
                % material.slot,
                m2_code="RELEASE_SUBJECT_NOT_FOUND",
            )
        authority = self._m2.closure_exact(release.authority_closure_ref)
        dependency = self._m2.closure_exact(release.dependency_closure_ref)
        determinant = self._m2.closure_exact(release.determinant_closure_ref)
        replay = self._m2.closure_exact(release.replay_reconstruction_ref)
        return {
            "release": release,
            "subject": subject,
            "authority": authority,
            "dependency": dependency,
            "determinant": determinant,
            "replay": replay,
        }

    def _determinant_refs(
        self,
        resolved: Mapping[str, Any],
        material: ProducerCustodyMaterial,
    ) -> tuple[ExactRef, ...]:
        """Derive the exact determinant set: M2 determinant closure + consumed model and
        walkback authorities + semantic authority determinants + custody supplements.

        Every member is a genuine graph edge parent (F8E H05). Consumed authorities being
        determinant members is what makes a model/walkback revocation reach this product
        (F8E H04 lesson).
        """
        members: dict[str, ExactRef] = {
            ref.key: ref for ref in resolved["determinant"].member_refs
        }
        members.update({ref.key: ref for ref in material.extra_determinant_refs})
        for ref in material.consumed_authority_refs:
            digest = semantic_hash({"consumed_authority_key": _key(ref)})
            consumed = ExactRef(
                "B5Lifecycle:CONSUMED_AUTHORITY",
                "urn:rawlsing:pre553:b5-lifecycle:consumed-authority:sha256:%s" % digest,
                digest,
            )
            members[consumed.key] = consumed
        for ref in material.semantic_authority_snapshot_refs:
            digest = semantic_hash({
                "determinant_class": "SEMANTIC_AUTHORITY_REF",
                "authority_ref": ref.as_dict(),
            })
            authority_determinant = ExactRef(
                "B5Lifecycle:AUTHORITY_DETERMINANT",
                "urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:%s" % digest,
                digest,
            )
            members[authority_determinant.key] = authority_determinant
        if not members:
            raise B5IngressDeterminantError(
                "slot %r derived an empty determinant closure; publication refused before "
                "B5" % material.slot
            )
        for ref in material.consumed_authority_refs:
            if not any(_key(member) == _key(ref) for member in members.values()):
                raise B5IngressDeterminantError(
                    "slot %r consumed authority %s is not covered by the determinant "
                    "closure" % (material.slot, _key(ref))
                )
        # Normalise EXACTLY as the accepted B5 subject normalises, so the
        # determinant_set_hash is B5's own hash and not a locally re-derived variant.
        return tuple(members[key] for key in sorted(members))

    def _replay_gate(self, resolved: Mapping[str, Any],
                     material: ProducerCustodyMaterial) -> str:
        """Gate the M2 replay reconstruction closure before B5."""
        replay = resolved["replay"]
        grade = replay.metadata.get("replay_grade")
        if grade not in ACCEPTED_REPLAY_GRADES:
            raise B5IngressReplayError(
                "M2 replay reconstruction closure %s declares grade %r which is outside "
                "the accepted vocabulary" % (replay.ref.object_id, grade)
            )
        if grade != material.required_replay_grade:
            raise B5IngressReplayError(
                "M2 replay reconstruction closure %s declares grade %r but slot %r "
                "requires %r" % (replay.ref.object_id, grade, material.slot,
                                 material.required_replay_grade)
            )
        if not replay.complete:
            raise B5IngressReplayError(
                "M2 replay reconstruction closure %s is explicitly incomplete"
                % replay.ref.object_id
            )
        if material.replay_state != PUBLISHABLE_REPLAY_STATE:
            raise B5IngressReplayError(
                "owner-held replay state for slot %r is %r; only %r may be published and "
                "no state is ever relabelled"
                % (material.slot, material.replay_state, PUBLISHABLE_REPLAY_STATE)
            )
        return grade

    def _authenticate(self, subject: B5.LearnedProductLifecycleSubject,
                      observed: Mapping[str, Any], slot: str) -> None:
        """Deep, closed-set, field-by-field authentication BEFORE the first B5 call."""
        expected = self._expected.get(slot)
        if expected is None:
            raise B5IngressAuthenticationError(
                "owner held no expected identity for slot %r" % slot,
                mismatched_fields=("expected_identity",),
                missing_keys=tuple(sorted(REQUIRED_EXPECTATION_KEYS)),
            )
        # Fail-closed completeness gate again, immediately before the comparison.
        _require_complete_expectation(expected, slot)
        missing = tuple(sorted(REQUIRED_EXPECTATION_KEYS - set(observed)))
        extra = tuple(sorted(set(observed) - REQUIRED_EXPECTATION_KEYS))
        if missing or extra:
            raise B5IngressAuthenticationError(
                "observed identity builder does not cover REQUIRED_EXPECTATION_KEYS "
                "exactly (missing: %s; extra: %s); authentication would not be exhaustive"
                % (list(missing), list(extra)),
                mismatched_fields=missing + extra,
                missing_keys=missing,
            )
        # B5's own subject already enforces this, but the ingress restates it so the
        # refusal is attributable to the perimeter and not to the accepted owner.
        if subject.determinant_set_hash != semantic_hash(
            [ref.as_dict() for ref in subject.determinant_refs]
        ):
            raise B5IngressAuthenticationError(
                "derived determinant_set_hash does not match the derived exact "
                "determinant refs",
                mismatched_fields=("determinant_set_hash", "determinant_keys"),
            )
        mismatches = tuple(
            sorted(k for k in REQUIRED_EXPECTATION_KEYS if observed[k] != expected[k])
        )
        if mismatches:
            raise B5IngressAuthenticationError(
                "constructed B5 subject does not authenticate against non-mutable "
                "owner-held material for slot %r; mismatched fields: %s"
                % (slot, ", ".join(mismatches)),
                mismatched_fields=mismatches,
                missing_keys=(),
            )

    def _publish_registered(self, slot: str,
                            material: ProducerCustodyMaterial) -> B5IngressReceipt:
        # ---- 1. ACCEPTED M2 OWNER resolves the exact release (owner-held ref only) ----
        resolved = self._resolve_m2(material)
        release = resolved["release"]
        subject_record = resolved["subject"]

        # ---- 2. Revocation gate, before anything else is derived ----
        authority_keys = _sorted_keys(material.semantic_authority_snapshot_refs)
        consumed_keys = _sorted_keys(material.consumed_authority_refs)
        self._revocation_check(
            material, release.ref.object_id, authority_keys, consumed_keys,
            resolved["replay"].ref.object_id,
        )

        # ---- 3. Replay closure gate ----
        replay_grade = self._replay_gate(resolved, material)

        # ---- 4. Derive the determinant closure; never accept a caller's ----
        determinant_refs = self._determinant_refs(resolved, material)

        # ---- 5. OWNER BUILDS the subject; the caller supplies no field of it ----
        dependency_pool = {
            ref.key: ref
            for ref in tuple(resolved["dependency"].member_refs)
            + tuple(material.direct_dependency_refs)
        }
        direct_dependencies = tuple(dependency_pool[key] for key in sorted(dependency_pool))
        subject = B5.LearnedProductLifecycleSubject(
            release_ref=release.ref,
            product_ref=material.product_ref,
            product_family_ref=material.product_family_ref,
            producer_owner_ref=material.producer_owner_ref,
            producer_contract_ref=release.semantic_producer_contract_ref,
            semantic_projection_hash=subject_record.semantic_anatomy_ref.content_hash,
            authority_snapshot_refs=tuple(material.semantic_authority_snapshot_refs),
            direct_dependency_refs=direct_dependencies,
            determinant_refs=determinant_refs,
            determinant_set_hash=semantic_hash(
                [ref.as_dict() for ref in determinant_refs]
            ),
            replay_root_ref=resolved["replay"].ref,
            selection_scope_ref=material.selection_scope_ref,
            build_or_release_receipt_refs=tuple(material.build_or_release_receipt_refs),
            producer_permission_ceiling_ref=material.producer_permission_ceiling_ref,
            replay_state=material.replay_state,
            materialization_class="MANDATORY_RETAINED_CAPITAL",
        )

        # ---- 6. DEEP AUTHENTICATION against the closed owner expectation ----
        observed = {
            "release_key": _key(release.ref),
            "release_content_hash": release.content_hash,
            "producer_subject_key": _key(subject_record.ref),
            "producer_contract_key": _key(release.semantic_producer_contract_ref),
            "semantic_anatomy_key": _key(subject_record.semantic_anatomy_ref),
            "semantic_projection_hash": subject_record.semantic_anatomy_ref.content_hash,
            "product_key": _key(material.product_ref),
            "product_family_key": _key(material.product_family_ref),
            "producer_owner_key": _key(material.producer_owner_ref),
            "selection_scope_key": _key(material.selection_scope_ref),
            "authority_snapshot_keys": authority_keys,
            "direct_dependency_keys": _sorted_keys(direct_dependencies),
            "determinant_keys": _sorted_keys(determinant_refs),
            "determinant_set_hash": subject.determinant_set_hash,
            "consumed_authority_keys": consumed_keys,
            "replay_closure_key": resolved["replay"].ref.object_id,
            "replay_grade": replay_grade,
            "replay_root_key": _key(resolved["replay"].ref),
            "receipt_keys": _sorted_keys(material.build_or_release_receipt_refs),
            "permission_ceiling_key": _key(material.producer_permission_ceiling_ref),
            "m2_release_projection_hash": semantic_hash(
                dict(resolved["release"].semantic_projection())
            ),
        }
        self._authenticate(subject, observed, slot)

        # ---- 7. ONLY NOW does the accepted B5 owner get called ----
        executor = B5.LearnedProductLifecycleExecutor()
        executor.stage_release(subject)
        registered = executor.register_product(
            release.ref,
            event_authority_ref=self._event_authority_ref,
            event_rule_ref=self._event_rule_ref,
        )
        published = executor.publish_product(
            release.ref,
            event_authority_ref=self._event_authority_ref,
            event_rule_ref=self._event_rule_ref,
        )
        # CURRENT / selection stays HELD: assert the ingress never took that step.
        assert not (FORBIDDEN_SELECTION_EVENT_KINDS & {e.event_kind for e in executor.events})
        assert executor.lifecycle_state(release.ref).publication == "PUBLISHED"

        return self._build_receipt(
            slot, material, resolved, subject, observed, replay_grade,
            registered, published, executor,
        )

    def _build_receipt(self, slot: str, material: ProducerCustodyMaterial,
                       resolved: Mapping[str, Any],
                       subject: B5.LearnedProductLifecycleSubject,
                       observed: Mapping[str, Any], replay_grade: str,
                       registered: B5.LearnedProductLifecycleEvent,
                       published: B5.LearnedProductLifecycleEvent,
                       executor: B5.LearnedProductLifecycleExecutor) -> B5IngressReceipt:
        authentication_material = {
            "contract": CONTRACT,
            "development_grade": DEVELOPMENT_GRADE,
            "slot": slot,
            "observed": {k: (list(observed[k]) if isinstance(observed[k], tuple)
                             else observed[k]) for k in sorted(observed)},
            "expected": {
                k: (list(self._expected[slot][k])
                    if isinstance(self._expected[slot][k], tuple)
                    else self._expected[slot][k])
                for k in sorted(self._expected[slot])
            },
            "registered_event_key": registered.ref.object_id,
            "publication_event_key": published.ref.object_id,
            "authorizing": False,
            "grant": None,
            "g0b": None,
            "g1_service": None,
            "scientific_competence_claim": "NONE__TECHNICAL_PRODUCT_AUTHENTICITY_ONLY",
        }
        return B5IngressReceipt(
            contract=CONTRACT,
            development_grade=DEVELOPMENT_GRADE,
            slot=slot,
            release_key=observed["release_key"],
            release_content_hash=observed["release_content_hash"],
            producer_subject_key=observed["producer_subject_key"],
            producer_contract_key=observed["producer_contract_key"],
            semantic_anatomy_key=observed["semantic_anatomy_key"],
            determinant_keys=observed["determinant_keys"],
            determinant_set_hash=observed["determinant_set_hash"],
            replay_closure_key=observed["replay_closure_key"],
            replay_grade=replay_grade,
            replay_root_key=observed["replay_root_key"],
            receipt_keys=observed["receipt_keys"],
            permission_ceiling_key=observed["permission_ceiling_key"],
            authority_snapshot_keys=observed["authority_snapshot_keys"],
            consumed_authority_keys=observed["consumed_authority_keys"],
            registered_event_key=registered.ref.object_id,
            publication_event_key=published.ref.object_id,
            ingress_authentication_hash=semantic_hash(authentication_material),
            current_selection_performed=False,
            current_selection_receipt_ref=None,
            authorizing=False,
            grant=None,
            g0b=None,
            g1_service=None,
        )


def _git_head() -> str:
    """Observed worktree HEAD, for evidence only. Never an authority input."""
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:  # noqa: BLE001
        return "UNAVAILABLE"


__all__ = [
    "CONTRACT",
    "DEVELOPMENT_GRADE",
    "TECHNICAL_ONLY_NOTE",
    "ACCEPTED_REPLAY_GRADES",
    "PUBLISHABLE_REPLAY_STATE",
    "REQUIRED_EXPECTATION_KEYS",
    "EXPECTATION_KEY_TYPES",
    "REFUSAL_CLASSES",
    "AuthenticatedB5Ingress",
    "AuthenticatedB5IngressError",
    "B5IngressAuthenticationError",
    "B5IngressCustodyError",
    "B5IngressDeterminantError",
    "B5IngressM2Error",
    "B5IngressReplayError",
    "B5IngressRequestError",
    "B5IngressReceipt",
    "B5IngressRevocationError",
    "ProducerCustodyMaterial",
    "PublicationRequest",
    "RevocationLedger",
]