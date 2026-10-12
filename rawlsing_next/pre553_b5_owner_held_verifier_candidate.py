"""PYAT HQ281 C02J — Owner-held B5 verifier CANDIDATE (no tickets, no crypto).

DEVELOPMENT CANDIDATE ONLY. Non-authorizing. G0b HELD. G1 HELD. CURRENT HELD.
No self-adoption. No canonical mutation. No accepted owner modified.

WHAT THIS IS
------------
A verifier-held mandatory ingress in front of the ACCEPTED B5 owner
(``rawlsing_next.pre553_learned_product_lifecycle``) and the ACCEPTED M2 owner
(``rawlsing_next.pre553_learned_product_release``).

The verifier holds, at construction and only at construction:
  * the exact M2Repository object reference (identity, not value),
  * a frozen per-slot expected product identity derived from that repository,
  * a frozen replay/authority scope (accepted grades, required grade, revocations).

The caller supplies ONLY a slot string (data-only). There is NO credential
surface: no ticket, no token, no signature, no hash, no callback. There is
therefore no credential to forge, no root to swap and no issuer to
self-register — the C02H failure class (caller-minted demo ticket accepted) is
structurally absent rather than refused case by case.

Authentication = resolve through the HELD repository + rebuild the observed
identity from HELD repository contents + compare field-by-field against the
FROZEN expectation + verify determinant/replay closures through the HELD
repository. Every step reads owner-held material; no step reads caller input
beyond the slot string.

WHAT IS REAL HERE (owner-authentic, not toy)
--------------------------------------------
1. M2 content-addressing: the accepted M2 owner refuses refs whose content_hash
   does not match stored content. A caller cannot present content for a hash it
   does not hold (SHA-256 preimage resistance). The verifier's expectation keys
   are content hashes read from the held repository.
2. Constructor-held references: the repository object and the frozen maps are
   bound at construction. The data-only caller has no field through which to
   substitute them.
3. Frozen type map: EXPECTATION_KEY_TYPES is a module-level MappingProxyType
   from the first line — the C02R F4 weakening is closed by construction.
4. Re-resolution at publish time: the expectation is re-derived from the held
   repository immediately before comparison, so post-authoring M2 mutation is
   detected (C02R C1a behaviour preserved).

WHAT REMAINS HELD (honest, not solved)
---------------------------------------
H1. Permission ceiling is self-declared in custody (C02R G6). No issuer exists
    to validate it against. Substitution of the ceiling is refused (it must
    equal the frozen expectation), but the declared value itself is unproved.
H2. Expectation tautology (C02R C2): the frozen expectation is derived from the
    same construction it authenticates. Freezing at construction plus
    re-resolution detects post-authoring mutation, but re-derivation after
    mutation still admits it. Only an independent issuer-held expectation would
    close this; none exists (C02G OWNER_ISSUER_HOLD, unchanged).
H3. REPLAY_COMPLETE remains an owner-held claim, gated by the M2 replay
    closure's own replay_grade; not an independent replay re-execution.
H4. Semantic AuthoritySnapshot refs are OWNER-HELD, not issuer-held.
H5. G0b / G1 / CURRENT / V3: all HELD. This module never selects current.
"""

from __future__ import annotations

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


CONTRACT = "HQ281_C02J_OWNER_HELD_B5_VERIFIER_CANDIDATE@1"
DEVELOPMENT_GRADE = (
    "SOURCE_FREE_CANDIDATE_ONLY__NONAUTHORIZING__"
    "G0B_HELD__G1_HELD__CURRENT_HELD"
)

ACCEPTED_REPLAY_GRADES = frozenset({
    "EXACT_MATERIALIZED_DEREFERENCE",
    "EXACT_DETERMINISTIC_REBUILD",
    "EXACT_SERVICE_REEXECUTION",
    "HISTORICAL_EXPLANATION_ONLY",
})
PUBLISHABLE_REPLAY_STATE = "REPLAY_COMPLETE"

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

#: Frozen at module import. There is no mutable type map to weaken (C02R F4
#: closed by construction, not by a runtime freeze step that could be skipped).
EXPECTATION_KEY_TYPES: Mapping[str, type] = MappingProxyType({
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
})

REFUSAL_CLASSES = (
    "REQUEST_SURFACE_VIOLATION",
    "CUSTODY_INCOMPLETE",
    "AUTHORITY_REVOKED",
    "M2_RESOLUTION_REFUSED",
    "EXPECTATION_INCOMPLETE",
    "IDENTITY_AUTHENTICATION_FAILED",
    "DETERMINANT_CLOSURE_INCOMPLETE",
    "REPLAY_CLOSURE_REFUSED",
    "UNKNOWN_RELEASE",
    "UNREGISTERED_REPOSITORY",
    "CHECKPOINT_UNRESOLVED",
)


class OwnerHeldVerifierError(Exception):
    """Typed refusal from the owner-held B5 verifier."""

    refusal_class = "VERIFIER_ERROR"

    def __init__(self, message: str, *, b5_invoked: bool = False) -> None:
        super().__init__(message)
        self.b5_invoked = b5_invoked


class VerifierRequestError(OwnerHeldVerifierError):
    refusal_class = "REQUEST_SURFACE_VIOLATION"


class VerifierCustodyError(OwnerHeldVerifierError):
    refusal_class = "CUSTODY_INCOMPLETE"


class VerifierRevocationError(VerifierCustodyError):
    refusal_class = "AUTHORITY_REVOKED"


class VerifierM2Error(OwnerHeldVerifierError):
    refusal_class = "M2_RESOLUTION_REFUSED"

    def __init__(self, message: str, *, m2_code: str) -> None:
        super().__init__(message)
        self.m2_code = m2_code


class VerifierAuthenticationError(OwnerHeldVerifierError):
    refusal_class = "IDENTITY_AUTHENTICATION_FAILED"

    def __init__(self, message: str, *, mismatched_fields: tuple[str, ...],
                 missing_keys: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.mismatched_fields = tuple(mismatched_fields)
        self.missing_keys = tuple(missing_keys)


class VerifierDeterminantError(OwnerHeldVerifierError):
    refusal_class = "DETERMINANT_CLOSURE_INCOMPLETE"


class VerifierReplayError(OwnerHeldVerifierError):
    refusal_class = "REPLAY_CLOSURE_REFUSED"


class VerifierUnknownReleaseError(OwnerHeldVerifierError):
    """The presented release is not registered with any verifier."""

    refusal_class = "UNKNOWN_RELEASE"


class VerifierUnregisteredRepositoryError(OwnerHeldVerifierError):
    """The M2 repository is not held by any registered verifier."""

    refusal_class = "UNREGISTERED_REPOSITORY"


class VerifierCheckpointError(OwnerHeldVerifierError):
    """A checkpointed subject does not resolve through a held repository."""

    refusal_class = "CHECKPOINT_UNRESOLVED"


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({k: _deep_freeze(v) for k, v in dict(value).items()})
    if isinstance(value, (list, tuple)):
        return tuple(_deep_freeze(v) for v in value)
    if isinstance(value, set):
        return frozenset(_deep_freeze(v) for v in value)
    return value


def _key(ref: Any) -> str:
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
    if type(expected) is not dict and type(expected) is not MappingProxyType:
        raise VerifierAuthenticationError(
            "owner-held expected identity for slot %r must be a plain mapping; got %s"
            % (slot, type(expected).__name__),
            mismatched_fields=("expected_identity",),
            missing_keys=tuple(sorted(REQUIRED_EXPECTATION_KEYS)),
        )
    missing = tuple(sorted(REQUIRED_EXPECTATION_KEYS - set(expected)))
    if missing:
        raise VerifierAuthenticationError(
            "owner-held expected identity for slot %r is INCOMPLETE (%d of %d required "
            "keys absent); authentication may not proceed vacuously. missing: %s"
            % (slot, len(missing), len(REQUIRED_EXPECTATION_KEYS), ", ".join(missing)),
            mismatched_fields=missing,
            missing_keys=missing,
        )
    extraneous = tuple(sorted(set(expected) - REQUIRED_EXPECTATION_KEYS))
    if extraneous:
        raise VerifierAuthenticationError(
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
        raise VerifierAuthenticationError(
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
    """The COMPLETE data-only publication surface: one closed field.

    No subject, release ref, authority, closure, receipt, replay root,
    permission ceiling, currentness claim, hash, credential, ticket, token,
    signature or callback can arrive. There is no credential surface at all.
    """

    slot: str


@dataclass(frozen=True)
class SlotCustody:
    """OWNER-HELD per-slot custody. M2-owned fields are absent by construction."""

    slot: str
    release_ref: ExactRef
    product_ref: ExactRef
    product_family_ref: ExactRef
    producer_owner_ref: ExactRef
    selection_scope_ref: ExactRef
    semantic_authority_snapshot_refs: tuple[AuthorityRef, ...]
    build_or_release_receipt_refs: tuple[ExactRef, ...]
    producer_permission_ceiling_ref: ExactRef
    consumed_authority_refs: tuple[ExactRef | AuthorityRef, ...]
    direct_dependency_refs: tuple[ExactRef, ...]
    extra_determinant_refs: tuple[ExactRef, ...]
    required_replay_grade: str
    replay_state: str
    expected_identity: Mapping[str, Any]


@dataclass(frozen=True)
class RevocationLedger:
    release_keys: frozenset = frozenset()
    authority_keys: frozenset = frozenset()
    replay_closure_keys: frozenset = frozenset()


@dataclass(frozen=True)
class VerifierReceipt:
    contract: str
    development_grade: str
    slot: str
    release_key: str
    registered_event_key: str
    publication_event_key: str
    verifier_authentication_hash: str
    current_selection_performed: bool = False
    current_selection_receipt_ref: None = None
    authorizing: bool = False
    scientific_competence_claim: str = "NONE__TECHNICAL_PRODUCT_AUTHENTICITY_ONLY"


class OwnerHeldB5Verifier:
    """Owner-held, data-only verifier in front of the ACCEPTED B5 owner.

    Construction is a TRUSTED HARNESS operation: it registers the accepted M2
    repository object, the owner custody per slot, the revocation ledger and the
    complete expected identities. The public surface is ``publish(slot)`` plus
    the ``verify_*`` methods the mandatory overlay calls. All of them read
    held material; none of them accepts caller objects.
    """

    def __init__(
        self,
        *,
        m2_repository: M2.M2Repository,
        custody: Mapping[str, SlotCustody],
        revocations: RevocationLedger | None = None,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
    ) -> None:
        if type(m2_repository) is not M2.M2Repository:
            raise VerifierCustodyError(
                "owner setup must register the accepted M2Repository exactly; got %s"
                % type(m2_repository).__name__
            )
        if not isinstance(custody, Mapping) or not custody:
            raise VerifierCustodyError(
                "owner setup must register a non-empty slot table of owner custody"
            )
        if not isinstance(event_authority_ref, ExactRef) or \
                not isinstance(event_rule_ref, ExactRef):
            raise VerifierCustodyError(
                "owner setup must register exact event authority and event rule refs"
            )
        self._m2 = m2_repository
        self._event_authority_ref = event_authority_ref
        self._event_rule_ref = event_rule_ref
        self._revocations = revocations or RevocationLedger()

        normalised: dict[str, SlotCustody] = {}
        for slot, material in dict(custody).items():
            if type(slot) is not str or not slot:
                raise VerifierCustodyError("slot names must be exact non-empty builtin str")
            if type(material) is not SlotCustody:
                raise VerifierCustodyError(
                    "slot %r custody must be the exact builtin SlotCustody; got %s"
                    % (slot, type(material).__name__)
                )
            if material.slot != slot:
                raise VerifierCustodyError(
                    "custody for slot %r declares a different slot %r" % (slot, material.slot)
                )
            if not material.semantic_authority_snapshot_refs:
                raise VerifierCustodyError(
                    "slot %r custody carries no semantic AuthoritySnapshot refs" % slot
                )
            if not material.build_or_release_receipt_refs:
                raise VerifierCustodyError(
                    "slot %r custody carries no build/release receipt refs" % slot
                )
            if material.required_replay_grade not in ACCEPTED_REPLAY_GRADES:
                raise VerifierCustodyError(
                    "slot %r requires replay grade %r which is outside the accepted M2 "
                    "vocabulary" % (slot, material.required_replay_grade)
                )
            _require_complete_expectation(material.expected_identity, slot)
            normalised[slot] = material
        self._custody = MappingProxyType(normalised)
        self._expected = MappingProxyType({
            slot: _deep_freeze(dict(normalised[slot].expected_identity))
            for slot in normalised
        })

    # -- trusted-harness introspection (read-only, NOT a public data surface) --

    def slots(self) -> tuple[str, ...]:
        return tuple(sorted(self._custody))

    def held_repository(self) -> M2.M2Repository:
        """The exact held repository object. Identity, not value."""
        return self._m2

    def verify_release_registered(self, release_ref: ExactRef) -> str:
        """Return the slot whose custody names this release, or refuse."""
        for slot, material in self._custody.items():
            if material.release_ref == release_ref:
                return slot
        raise VerifierUnknownReleaseError(
            "release %s is not registered with this verifier" % release_ref.key
        )

    # -- public data-only surface --

    def publish(self, request: Any) -> VerifierReceipt:
        """The ONLY public entrypoint. Data-only: one slot string."""
        if type(request) is not PublicationRequest:
            raise VerifierRequestError(
                "owner-held verifier accepts only the exact builtin PublicationRequest; got %s"
                % type(request).__name__
            )
        if type(request.slot) is not str or not request.slot:
            raise VerifierRequestError("request slot must be an exact builtin non-empty str")
        extra = set(vars(request)) - {"slot"}
        if extra:
            raise VerifierRequestError(
                "request carries field(s) outside the closed data-only set: %s"
                % ", ".join(sorted(extra))
            )
        material = self._custody.get(request.slot)
        if material is None:
            raise VerifierRequestError(
                "slot %r is not registered by the owner" % request.slot
            )
        return self._publish_registered(request.slot, material)

    # -- overlay entrypoints (called by the mandatory overlay, never by callers) --

    def verify_subject_for_release(
        self, subject: B5.LearnedProductLifecycleSubject, release_ref: ExactRef
    ) -> str:
        """Check a caller-presented subject against held material. Returns slot.

        Used by the mandatory overlay for direct B5 calls. Refuses unknown
        releases, mismatched subjects, revoked material and replay violations —
        all before any B5 call.
        """
        slot = self.verify_release_registered(release_ref)
        material = self._custody[slot]
        if subject.release_ref != material.release_ref:
            raise VerifierAuthenticationError(
                "presented subject release does not match the registered release",
                mismatched_fields=("release_key",),
            )
        observed = self._observed_identity(material)
        self._revocation_check(material, observed)
        grade = self._replay_gate(material)
        self._authenticate(subject, observed, slot)
        return slot

    def verify_checkpoint_subject(
        self, subject: B5.LearnedProductLifecycleSubject
    ) -> str:
        """Check a rehydrated subject resolves through the HELD repository."""
        try:
            stored = self._m2.subject_exact(subject.release_ref)
        except Exception as exc:
            raise VerifierCheckpointError(
                "checkpoint subject release is absent from the held M2 repository: %s"
                % exc
            ) from exc
        void = stored
        del void
        slot = self.verify_release_registered(subject.release_ref)
        material = self._custody[slot]
        observed = self._observed_identity(material)
        self._revocation_check(material, observed)
        self._replay_gate(material)
        self._authenticate(subject, observed, slot)
        return slot

    # -- internals --

    def _revocation_check(self, material: SlotCustody, observed: Mapping[str, Any]) -> None:
        revoked = self._revocations
        if observed["release_key"] in revoked.release_keys:
            raise VerifierRevocationError(
                "release %s is revoked for this verifier; publication is refused before "
                "B5" % observed["release_key"]
            )
        hit = sorted(set(observed["authority_snapshot_keys"]) & set(revoked.authority_keys))
        if hit:
            raise VerifierRevocationError(
                "semantic authority ref(s) %s are revoked; publication is refused before "
                "B5" % ", ".join(hit)
            )
        hit = sorted(set(observed["consumed_authority_keys"]) & set(revoked.authority_keys))
        if hit:
            raise VerifierRevocationError(
                "consumed model/walkback authority ref(s) %s are revoked; publication is "
                "refused before B5" % ", ".join(hit)
            )
        if observed["replay_closure_key"] in revoked.replay_closure_keys:
            raise VerifierRevocationError(
                "M2 replay reconstruction closure %s is revoked; publication is refused "
                "before B5" % observed["replay_closure_key"]
            )

    def _resolve_m2(self, material: SlotCustody) -> dict[str, Any]:
        try:
            resolution = M2.resolve_release_exact(
                self._m2, material.release_ref, publication_binding_refs=(),
            )
        except M2.M2ReleaseError as exc:
            raise VerifierM2Error(
                "accepted M2 owner refused the exact release for slot %r: %s"
                % (material.slot, exc),
                m2_code=exc.code,
            ) from exc
        release = resolution.release_core
        subject = resolution.subject
        if subject is None:
            raise VerifierM2Error(
                "accepted M2 owner resolved no producer subject for slot %r"
                % material.slot,
                m2_code="RELEASE_SUBJECT_NOT_FOUND",
            )
        authority = self._m2.closure_exact(release.authority_closure_ref)
        dependency = self._m2.closure_exact(release.dependency_closure_ref)
        determinant = self._m2.closure_exact(release.determinant_closure_ref)
        replay = self._m2.closure_exact(release.replay_reconstruction_ref)
        return {
            "release": release, "subject": subject, "authority": authority,
            "dependency": dependency, "determinant": determinant, "replay": replay,
        }

    def _determinant_refs(
        self, resolved: Mapping[str, Any], material: SlotCustody
    ) -> tuple[ExactRef, ...]:
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
            raise VerifierDeterminantError(
                "slot %r derived an empty determinant closure; publication refused before "
                "B5" % material.slot
            )
        for ref in material.consumed_authority_refs:
            if not any(_key(member) == _key(ref) for member in members.values()):
                raise VerifierDeterminantError(
                    "slot %r consumed authority %s is not covered by the determinant "
                    "closure" % (material.slot, _key(ref))
                )
        return tuple(members[key] for key in sorted(members))

    def _replay_gate(self, material: SlotCustody) -> str:
        resolved = self._resolve_m2(material)
        replay = resolved["replay"]
        grade = replay.metadata.get("replay_grade")
        if grade not in ACCEPTED_REPLAY_GRADES:
            raise VerifierReplayError(
                "M2 replay reconstruction closure %s declares grade %r which is outside "
                "the accepted vocabulary" % (replay.ref.object_id, grade)
            )
        if grade != material.required_replay_grade:
            raise VerifierReplayError(
                "M2 replay reconstruction closure %s declares grade %r but slot %r "
                "requires %r" % (replay.ref.object_id, grade, material.slot,
                                 material.required_replay_grade)
            )
        if not replay.complete:
            raise VerifierReplayError(
                "M2 replay reconstruction closure %s is explicitly incomplete"
                % replay.ref.object_id
            )
        if material.replay_state != PUBLISHABLE_REPLAY_STATE:
            raise VerifierReplayError(
                "owner-held replay state for slot %r is %r; only %r may be published and "
                "no state is ever relabelled"
                % (material.slot, material.replay_state, PUBLISHABLE_REPLAY_STATE)
            )
        return grade

    def _observed_identity(self, material: SlotCustody) -> dict[str, Any]:
        resolved = self._resolve_m2(material)
        release = resolved["release"]
        subject_record = resolved["subject"]
        replay_grade = self._replay_gate(material)
        determinant_refs = self._determinant_refs(resolved, material)
        dependency_pool = {
            ref.key: ref
            for ref in tuple(resolved["dependency"].member_refs)
            + tuple(material.direct_dependency_refs)
        }
        direct_dependencies = tuple(dependency_pool[key] for key in sorted(dependency_pool))
        authority_keys = _sorted_keys(material.semantic_authority_snapshot_refs)
        consumed_keys = _sorted_keys(material.consumed_authority_refs)
        return {
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
            "determinant_set_hash": semantic_hash(
                [ref.as_dict() for ref in determinant_refs]
            ),
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

    def _authenticate(self, subject: B5.LearnedProductLifecycleSubject,
                      observed: Mapping[str, Any], slot: str) -> None:
        expected = self._expected.get(slot)
        if expected is None:
            raise VerifierAuthenticationError(
                "owner held no expected identity for slot %r" % slot,
                mismatched_fields=("expected_identity",),
                missing_keys=tuple(sorted(REQUIRED_EXPECTATION_KEYS)),
            )
        _require_complete_expectation(expected, slot)
        missing = tuple(sorted(REQUIRED_EXPECTATION_KEYS - set(observed)))
        extra = tuple(sorted(set(observed) - REQUIRED_EXPECTATION_KEYS))
        if missing or extra:
            raise VerifierAuthenticationError(
                "observed identity builder does not cover REQUIRED_EXPECTATION_KEYS "
                "exactly (missing: %s; extra: %s); authentication would not be exhaustive"
                % (list(missing), list(extra)),
                mismatched_fields=missing + extra,
                missing_keys=missing,
            )
        if subject.determinant_set_hash != semantic_hash(
            [ref.as_dict() for ref in subject.determinant_refs]
        ):
            raise VerifierAuthenticationError(
                "derived determinant_set_hash does not match the derived exact "
                "determinant refs",
                mismatched_fields=("determinant_set_hash", "determinant_keys"),
            )
        mismatches = tuple(
            sorted(k for k in REQUIRED_EXPECTATION_KEYS if observed[k] != expected[k])
        )
        if mismatches:
            raise VerifierAuthenticationError(
                "constructed B5 subject does not authenticate against non-mutable "
                "owner-held material for slot %r; mismatched fields: %s"
                % (slot, ", ".join(mismatches)),
                mismatched_fields=mismatches,
                missing_keys=(),
            )

    def _publish_registered(self, slot: str, material: SlotCustody) -> VerifierReceipt:
        resolved = self._resolve_m2(material)
        release = resolved["release"]
        subject_record = resolved["subject"]
        authority_keys = _sorted_keys(material.semantic_authority_snapshot_refs)
        consumed_keys = _sorted_keys(material.consumed_authority_refs)
        observed = self._observed_identity(material)
        self._revocation_check(material, observed)
        replay_grade = self._replay_gate(material)
        determinant_refs = self._determinant_refs(resolved, material)
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
        self._authenticate(subject, observed, slot)

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
        assert executor.lifecycle_state(release.ref).publication == "PUBLISHED"

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
        }
        return VerifierReceipt(
            contract=CONTRACT,
            development_grade=DEVELOPMENT_GRADE,
            slot=slot,
            release_key=observed["release_key"],
            registered_event_key=registered.ref.object_id,
            publication_event_key=published.ref.object_id,
            verifier_authentication_hash=semantic_hash(authentication_material),
            current_selection_performed=False,
            current_selection_receipt_ref=None,
            authorizing=False,
        )


__all__ = [
    "CONTRACT",
    "DEVELOPMENT_GRADE",
    "ACCEPTED_REPLAY_GRADES",
    "PUBLISHABLE_REPLAY_STATE",
    "REQUIRED_EXPECTATION_KEYS",
    "EXPECTATION_KEY_TYPES",
    "REFUSAL_CLASSES",
    "OwnerHeldVerifierError",
    "VerifierRequestError",
    "VerifierCustodyError",
    "VerifierRevocationError",
    "VerifierM2Error",
    "VerifierAuthenticationError",
    "VerifierDeterminantError",
    "VerifierReplayError",
    "VerifierUnknownReleaseError",
    "VerifierUnregisteredRepositoryError",
    "VerifierCheckpointError",
    "PublicationRequest",
    "SlotCustody",
    "RevocationLedger",
    "VerifierReceipt",
    "OwnerHeldB5Verifier",
]
