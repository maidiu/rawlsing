"""Native-ready input ports for the BP2 joined actor/event/rule/action producer.

These ports are the *receiving* side for authority that this worker may not
issue:

    ADP010 AVAILABLE -> OPPORTUNITY -> ENCOUNTER   (encounter owner)
    ADP019 external admission of the E1 occurrence (external admission court)
    CAN008 concrete RULE_A response resource       (CAN008 R2 rule issuer)
    CAN011 separate RULE_T target resource + grant (separate target owner)
    later performed E2 owner receipt               (actuator/occurrence owner)

Every port is fail-closed and typed. A resource that is absent, unissued,
stale, expired, revoked, wrongly versioned, bound to a foreign owner or lacking
its required readset is refused with an exact code. The production registries
are empty by construction: no rule, grant, encounter, admission or performed
action is minted here.

The only resources these ports will bind in this return are explicit
``TEST_ONLY_`` fixture resources created for source-free engineering proof. A
TEST_ONLY resource can never satisfy the native release gate and never becomes
an ADP/CAN/Pyat grant.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Any, Mapping

TEST_ONLY_PREFIX = "TEST_ONLY"
TEST_ONLY_GRADE = "TEST_ONLY_SOURCEFREE_TECHNICAL"
NATIVE_GRADE = "NATIVE_OWNER_ISSUED"
UNISSUED_GRADE = "UNISSUED"
NATIVE_GRANT_NOT_GRANTED = "NOT_GRANTED"

PORT_SCHEMA = "BP2_NATIVE_READY_RESOURCE@1"
BINDING_SCHEMA = "BP2_NATIVE_READY_BINDING@1"


class PortRefusal(Exception):
    """A typed refusal from a native-ready port. Never a governance grant."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


class Currentness(str, Enum):
    CURRENT = "CURRENT"
    UNISSUED = "UNISSUED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"
    NOT_YET_EFFECTIVE = "NOT_YET_EFFECTIVE"
    STALE = "STALE"
    FOREIGN_OWNER = "FOREIGN_OWNER"
    VERSION_MISMATCH = "VERSION_MISMATCH"
    HASH_MISMATCH = "HASH_MISMATCH"
    MISSING_READSET = "MISSING_READSET"


@dataclass(frozen=True)
class Resource:
    """One externally issued authority resource, as presented to a port.

    ``content_hash`` is the exact identity of the resource body. ``version`` and
    ``rule_version`` style fields are kept distinct from ``currentness_as_of``
    because an old-but-valid rule and a stale binding are different failures.
    """

    resource_id: str
    schema: str
    version: str
    content_hash: str
    issuer_ref: str
    issuer_grade: str
    source_owner: str
    permission_ref: str
    effective_from: int
    expires_at: int | None
    revoked: bool
    readset_refs: tuple[str, ...]
    currentness_as_of: int
    body: Mapping[str, Any]
    native_grant: str = NATIVE_GRANT_NOT_GRANTED
    schema_id: str = PORT_SCHEMA

    @property
    def test_only(self) -> bool:
        return self.issuer_grade == TEST_ONLY_GRADE

    def check(
        self,
        *,
        now: int,
        required_readset: tuple[str, ...] = (),
        expected_hash: str = "",
        expected_version: str = "",
        permitted_owners: tuple[str, ...] = (),
    ) -> Currentness:
        """Return the typed currentness of this resource at ``now``."""
        if not self.content_hash or self.issuer_grade == UNISSUED_GRADE:
            return Currentness.UNISSUED
        if self.revoked:
            return Currentness.REVOKED
        if expected_hash and self.content_hash != expected_hash:
            return Currentness.HASH_MISMATCH
        if expected_version and self.version != expected_version:
            return Currentness.VERSION_MISMATCH
        if self.currentness_as_of > now:
            return Currentness.STALE
        if self.effective_from > now:
            return Currentness.NOT_YET_EFFECTIVE
        if isinstance(self.expires_at, int) and now >= self.expires_at:
            return Currentness.EXPIRED
        if permitted_owners and self.source_owner not in permitted_owners:
            return Currentness.FOREIGN_OWNER
        missing = [ref for ref in required_readset if ref not in self.readset_refs]
        if missing:
            return Currentness.MISSING_READSET
        return Currentness.CURRENT

    def require(self, **kwargs: Any) -> "Resource":
        state = self.check(**kwargs)
        if state is not Currentness.CURRENT:
            raise PortRefusal("RESOURCE_" + state.value, self.resource_id)
        return self


def _issued_test_only(
    *,
    resource_id: str,
    version: str,
    body: Mapping[str, Any],
    issuer_ref: str,
    source_owner: str,
    permission_ref: str,
    effective_from: int,
    readset_refs: tuple[str, ...],
    currentness_as_of: int,
    expires_at: int | None = None,
    revoked: bool = False,
) -> Resource:
    from candidate.canon import digest

    if not resource_id.startswith(TEST_ONLY_PREFIX):
        raise PortRefusal("TEST_ONLY_RESOURCE_ID_REQUIRED", resource_id)
    if not issuer_ref.startswith(TEST_ONLY_PREFIX):
        raise PortRefusal("TEST_ONLY_ISSUER_NAMESPACE_REQUIRED", issuer_ref)
    return Resource(
        resource_id=resource_id,
        schema=PORT_SCHEMA,
        version=version,
        content_hash=digest(dict(body)),
        issuer_ref=issuer_ref,
        issuer_grade=TEST_ONLY_GRADE,
        source_owner=source_owner,
        permission_ref=permission_ref,
        effective_from=effective_from,
        expires_at=expires_at,
        revoked=revoked,
        readset_refs=tuple(readset_refs),
        currentness_as_of=currentness_as_of,
        body=dict(body),
    )


# ---------------------------------------------------------------------------
# ADP010 — availability / opportunity / encounter
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class EncounterBinding:
    """One bound encounter stage. Never created by this worker."""

    stage: str
    status: str
    subject_ref: str
    resource_ref: str
    native_grant: str = NATIVE_GRANT_NOT_GRANTED


class ADP010EncounterPort:
    """Receiving port for ADP010 AVAILABLE -> OPPORTUNITY -> ENCOUNTER.

    ``AVAILABLE`` is the only stage a source-free world fixture may declare on
    its own: a material/practice opportunity exists in the world. ``OPPORTUNITY``
    and ``ENCOUNTER`` require an externally issued resource for the exact
    subject. With no resource the port returns a typed HOLD; it never promotes
    structural availability to an encounter.
    """

    ORDER = ("AVAILABLE", "OPPORTUNITY", "ENCOUNTER")

    def __init__(self, world_ref: str) -> None:
        self.world_ref = world_ref

    def availability(self) -> EncounterBinding:
        return EncounterBinding(
            stage="AVAILABLE",
            status="WORLD_OPPORTUNITY_AVAILABLE_NOT_ACTOR_ENCOUNTER",
            subject_ref="",
            resource_ref=self.world_ref,
        )

    def opportunity(self, *, subject_ref: str, resource: Resource | None,
                    now: int) -> EncounterBinding:
        if resource is None:
            raise PortRefusal("ADP010_OPPORTUNITY_UNISSUED", subject_ref)
        resource.require(now=now, permitted_owners=(resource.source_owner,))
        return EncounterBinding(
            stage="OPPORTUNITY",
            status="TEST_ONLY_DECLARED_OPPORTUNITY" if resource.test_only else "OPPORTUNITY_BOUND",
            subject_ref=subject_ref,
            resource_ref=resource.resource_id,
        )

    def encounter(self, *, subject_ref: str, resource: Resource | None,
                  now: int) -> EncounterBinding:
        if resource is None:
            raise PortRefusal("ADP010_ENCOUNTER_UNISSUED", subject_ref)
        resource.require(now=now)
        return EncounterBinding(
            stage="ENCOUNTER",
            status="TEST_ONLY_DECLARED_ENCOUNTER" if resource.test_only else "ENCOUNTER_BOUND",
            subject_ref=subject_ref,
            resource_ref=resource.resource_id,
        )


# ---------------------------------------------------------------------------
# ADP019 — external admission of the E1 occurrence
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class E1Binding:
    """The E1 occurrence binding actually consumed by C9R."""

    occurrence_id: str
    identity_digest: str
    state_digest: str
    commit_receipt_id: str
    writer_version: int
    event_time: int
    admission_status: str
    adp019_admission_receipt: str
    native_grant: str = NATIVE_GRANT_NOT_GRANTED

    def as_dict(self) -> dict:
        return {
            "occurrence_id": self.occurrence_id,
            "identity_digest": self.identity_digest,
            "state_digest": self.state_digest,
            "commit_receipt_id": self.commit_receipt_id,
            "writer_version": self.writer_version,
            "event_time": self.event_time,
            "admission_status": self.admission_status,
            "adp019_admission_receipt": self.adp019_admission_receipt,
            "native_grant": self.native_grant,
        }


class ADP019EventPort:
    """Receiving port for ADP019 external admission of the precipitating event.

    The port binds a *verified committed C8 occurrence* as the E1 witness and
    records, without euphemism, that no ADP019 admission receipt exists. It has
    no method that can mint one: ``admit_native`` requires an externally issued
    ``Resource`` whose body carries the owner's admission receipt, and even then
    the port only records what the owner supplied.
    """

    def __init__(self) -> None:
        self.adp019_admission_receipt = "ADP019_ADMISSION_RECEIPT_ABSENT"

    def bind_test_only_e1(
        self, *, occurrence: Mapping[str, Any], event_time: int,
        verified_proof: bool,
    ) -> E1Binding:
        if not verified_proof:
            raise PortRefusal("ADP019_E1_PROOF_UNVERIFIED")
        occurrence_id = occurrence.get("occurrence_id")
        identity = occurrence.get("identity_digest")
        if not isinstance(occurrence_id, str) or not occurrence_id:
            raise PortRefusal("ADP019_E1_OCCURRENCE_MISSING")
        if not isinstance(identity, str) or not identity:
            raise PortRefusal("ADP019_E1_IDENTITY_MISSING")
        return E1Binding(
            occurrence_id=occurrence_id,
            identity_digest=identity,
            state_digest=str(occurrence.get("_state_digest", "")),
            commit_receipt_id=str(occurrence.get("_commit_receipt_id", "")),
            writer_version=int(occurrence.get("_writer_version", 0)),
            event_time=int(event_time),
            admission_status="TEST_ONLY_E1_BOUND_ADP019_NOT_ISSUED",
            adp019_admission_receipt=self.adp019_admission_receipt,
        )

    def admit_native(self, *, resource: Resource | None, now: int) -> E1Binding:
        if resource is None or resource.issuer_grade != NATIVE_GRADE:
            raise PortRefusal(
                "ADP019_ADMISSION_RECEIPT_ABSENT",
                "V3 External Admission Court must issue the owner receipt",
            )
        resource.require(now=now)
        body = dict(resource.body)
        receipt = body.get("adp019_admission_receipt")
        if not isinstance(receipt, Mapping):
            raise PortRefusal("ADP019_ADMISSION_RECEIPT_MALFORMED")
        return E1Binding(
            occurrence_id=str(body.get("occurrence_id", "")),
            identity_digest=str(body.get("identity_digest", "")),
            state_digest=str(body.get("state_digest", "")),
            commit_receipt_id=str(body.get("commit_receipt_id", "")),
            writer_version=int(body.get("writer_version", 0)),
            event_time=int(body.get("event_time", 0)),
            admission_status="NATIVE_ADP019_ADMISSION_BOUND",
            adp019_admission_receipt="ADP019_ADMISSION_RECEIPT_PRESENT",
        )


# ---------------------------------------------------------------------------
# CAN008 — concrete RULE_A response resource
# ---------------------------------------------------------------------------
class CAN008RulePort:
    """Receiving port for one concrete CAN008 RULE_A response resource."""

    def __init__(self) -> None:
        self.registry = None  # production registry: empty

    def bind(self, *, rule: Resource | None, subject: str, conditioning_class: str,
             now: int) -> Resource:
        from candidate.canon import digest

        if rule is None:
            raise PortRefusal("CAN008_RULE_A_UNISSUED", subject)
        rule.require(
            now=now,
            required_readset=(conditioning_class,),
        )
        body = dict(rule.body)
        semantics = body.get("rule_semantics")
        if not isinstance(semantics, Mapping) or body.get("rule_content_hash") != digest(
            dict(semantics)
        ):
            raise PortRefusal("CAN008_RULE_A_CONTENT_HASH_MISMATCH")
        if subject not in tuple(semantics.get("allowed_subjects", ())):
            raise PortRefusal("CAN008_RULE_A_SUBJECT_NOT_ALLOWED", subject)
        if body.get("grade") != rule.issuer_grade:
            raise PortRefusal("CAN008_RULE_A_GRADE_MISMATCH")
        if body.get("issuer_ref") != rule.issuer_ref:
            raise PortRefusal("CAN008_RULE_A_ISSUER_MISMATCH")
        return rule


# ---------------------------------------------------------------------------
# CAN011 — separate RULE_T target resource + grant
# ---------------------------------------------------------------------------
class CAN011TargetPort:
    """Receiving port for a separately owned CAN011 RULE_T and its grant.

    The target owner must be distinct from the response owner. The grant must
    bind the exact response hash, the actor, the rule content hash and the
    before-target state; a grant is refused when revoked, expired, stale,
    foreign, self-issued or bound to a different response.
    """

    def __init__(self, *, response_owner: str) -> None:
        self.response_owner = response_owner

    def bind_rule(self, *, rule: Resource | None, now: int) -> Resource:
        from candidate.canon import digest

        if rule is None:
            raise PortRefusal("CAN011_RULE_T_UNISSUED")
        rule.require(now=now)
        body = dict(rule.body)
        semantics = body.get("rule_semantics")
        if not isinstance(semantics, Mapping) or body.get("rule_t_content_hash") != digest(
            dict(semantics)
        ):
            raise PortRefusal("CAN011_RULE_T_CONTENT_HASH_MISMATCH")
        if body.get("rule_content_hash") != semantics.get("response_rule_content_hash"):
            raise PortRefusal("CAN011_RULE_T_DEPENDENCY_MISMATCH")
        if rule.source_owner == self.response_owner:
            raise PortRefusal("CAN011_TARGET_OWNER_NOT_SEPARATE", rule.source_owner)
        if rule.issuer_ref == self.response_owner:
            raise PortRefusal("CAN011_TARGET_ISSUER_NOT_SEPARATE", rule.issuer_ref)
        return rule

    def bind_grant(
        self,
        *,
        grant: Resource | None,
        rule: Resource,
        actor_id: str,
        response_hash: str,
        before_target_hash: str,
        now: int,
    ) -> Resource:
        if grant is None:
            raise PortRefusal("CAN011_TARGET_GRANT_UNISSUED")
        grant.require(
            now=now,
            required_readset=(response_hash, before_target_hash),
        )
        body = dict(grant.body)
        if body.get("actor_id") != actor_id:
            raise PortRefusal("CAN011_GRANT_ACTOR_MISMATCH")
        if body.get("rule_content_hash") != rule.body.get("rule_content_hash"):
            raise PortRefusal("CAN011_GRANT_RULE_MISMATCH")
        if body.get("rule_t_content_hash") != rule.body.get("rule_t_content_hash"):
            raise PortRefusal("CAN011_GRANT_RULE_T_MISMATCH")
        if body.get("response_hash") != response_hash:
            raise PortRefusal("CAN011_GRANT_RESPONSE_MISMATCH")
        if body.get("before_target_hash") != before_target_hash:
            raise PortRefusal("CAN011_GRANT_PRESTATE_MISMATCH")
        if grant.source_owner == self.response_owner:
            raise PortRefusal("CAN011_GRANT_OWNER_NOT_SEPARATE")
        return grant


# ---------------------------------------------------------------------------
# later E2 — independently performed action owner receipt
# ---------------------------------------------------------------------------
class E2OwnerPort:
    """Receiving port for an independently performed later E2 action receipt."""

    def bind(
        self,
        *,
        receipt: Resource | None,
        actor_id: str,
        act: str,
        consumed_state_hash: str,
        target_commit_time: int,
        now: int,
    ) -> Resource:
        if receipt is None:
            raise PortRefusal("E2_OWNER_RECEIPT_UNISSUED", actor_id)
        receipt.require(now=now)
        body = dict(receipt.body)
        if body.get("actor_id") != actor_id:
            raise PortRefusal("E2_RECEIPT_ACTOR_MISMATCH")
        if body.get("act") != act:
            raise PortRefusal("E2_RECEIPT_ACT_MISMATCH")
        if body.get("actuator_ref") == actor_id:
            raise PortRefusal("E2_ACTUATOR_SELF_BOUND", actor_id)
        if body.get("occurrence_ref") == actor_id:
            raise PortRefusal("E2_OCCURRENCE_SELF_BOUND", actor_id)
        if body.get("consumed_state_hash") != consumed_state_hash:
            raise PortRefusal("E2_RECEIPT_CONSUMED_STATE_MISMATCH")
        if int(body.get("action_time", -1)) < target_commit_time:
            raise PortRefusal("E2_ACTION_BEFORE_TARGET_COMMIT")
        if receipt.source_owner == actor_id:
            raise PortRefusal("E2_RECEIPT_NOT_INDEPENDENT", actor_id)
        return receipt


# ---------------------------------------------------------------------------
# production-empty registries
# ---------------------------------------------------------------------------
def production_registries() -> dict:
    """Return the empty-by-construction production registries.

    This is a *receiving* statement, not a denial: a competent issuer populates
    them by an owner action. No method here can add a rule.
    """
    from candidate import ResponseRuleRegistry, TargetRuleRegistry

    response = ResponseRuleRegistry.production()
    target = TargetRuleRegistry.production()
    if response.rules or target.rules:
        raise PortRefusal("PRODUCTION_REGISTRY_NOT_EMPTY")
    return {
        "response": response,
        "target": target,
        "response_rule_count": len(response.rules),
        "target_rule_count": len(target.rules),
        "status": "PRODUCTION_RULE_REGISTRIES_EMPTY_AWAITING_COMPETENT_ISSUER",
    }


def test_only_rule_resource(
    *,
    resource_id: str,
    version: str,
    body: Mapping[str, Any],
    issuer_ref: str,
    source_owner: str,
    permission_ref: str,
    effective_from: int,
    readset_refs: tuple[str, ...],
    currentness_as_of: int,
    expires_at: int | None = None,
    revoked: bool = False,
) -> Resource:
    """Explicit TEST_ONLY fixture resource constructor (never native authority)."""
    return _issued_test_only(
        resource_id=resource_id,
        version=version,
        body=body,
        issuer_ref=issuer_ref,
        source_owner=source_owner,
        permission_ref=permission_ref,
        effective_from=effective_from,
        readset_refs=readset_refs,
        currentness_as_of=currentness_as_of,
        expires_at=expires_at,
        revoked=revoked,
    )


def revoke(resource: Resource, *, now: int | None = None) -> Resource:
    """Return a revoked copy of a resource (owner revocation)."""
    updated = replace(resource, revoked=True)
    if now is not None:
        updated = replace(updated, currentness_as_of=now)
    return updated


__all__ = [
    "ADP010EncounterPort",
    "ADP019EventPort",
    "CAN008RulePort",
    "CAN011TargetPort",
    "Currentness",
    "E1Binding",
    "E2OwnerPort",
    "EncounterBinding",
    "NATIVE_GRADE",
    "NATIVE_GRANT_NOT_GRANTED",
    "PortRefusal",
    "Resource",
    "TEST_ONLY_GRADE",
    "UNISSUED_GRADE",
    "production_registries",
    "revoke",
    "test_only_rule_resource",
]
