"""Owner-preserving V557/V558 carrier for qualified PRE-V3 objective-position facts.

This module implements only the J04 authority ruling for
PREV3_OBJECTIVE_POSITION_FACT@1.0.0.  It deliberately does not widen the
shared M4 root-family whitelist.  Instead it validates one exact producer-owned
fact against the J04 per-item authority, preserves PREV3POS identity and
canonical dependency closure, and packages that fact through a guarded V557
publication and exact V558 repository/CAS surface.

The current J04 authority contains one concrete item-use mapping: the qualified
Afrobarometer R5 / BEN0002 / Q73A fact may be exposed to M4 CONTEXT only while
retaining its exact source-domain use token.  A bare CONTEXT query is therefore
insufficient.  No M2/M3, causal, population, person/V3, present-day persistence,
or OBL063 authority is created here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash as producer_semantic_hash
from rawlsing_next.prev3_objective_position_materializer import (
    CONTRACT_ID as POSITION_MATERIALIZER_CONTRACT_ID,
    FACT_REF_KIND,
    FACT_SCHEMA_ID,
    POSITIVE_STATE,
    ObjectivePositionFact,
    PositionResultState,
)
from rawlsing_next.m4_v557_v558_publication_repository import (
    M4IntegrityError,
    AuthorityRef as M4AuthorityRef,
    ContextQuery,
    ContextQueryItem,
    ExactRef as M4ExactRef,
    ExternalResolutionBinding,
    ReferenceClassError,
    RepositoryEntry,
    ResolutionResult,
    StructuralObject,
    V557DecisionState,
    V557ExceptionState,
    V557PublicationBundle,
    V557PublicationEntry,
    V558RepositoryBundle,
    _publication_material,
    build_role_authenticated_v558_repository_bundle,
    build_v557_publication_bundle,
    exact_resolution_key,
    govern_v557,
    make_context_query,
    make_external_resolution_binding,
    make_external_stub,
    make_producer_locator,
    make_reference_edge,
    resolve_v558,
    semantic_hash as m4_semantic_hash,
)

CARRIER_CONTRACT_ID = (
    "PREV3_OBJECTIVE_POSITION_FACT_OWNER_PRESERVING_V557_V558_PUBLICATION@1.0.0"
)
CARRIER_CONTRACT_VERSION = "1.0.0"
DEPENDENCY_REFERENCE_SCHEMA = "PREV3_OBJECTIVE_POSITION_DEPENDENCY_EXACT_REF@1.0.0"
DEPENDENCY_REFERENCE_FAMILY = "PREV3_OBJECTIVE_POSITION_DEPENDENCY_EXACT_REF"
SOURCE_STAGE = "K04_J04_OWNER_PRESERVING_POSITION_PUBLICATION"
DEPENDENCY_SOURCE_STAGE = "K04_J04_OBJECTIVE_POSITION_CLOSURE_REFERENCE"

J04_AUTHORITY_ID = (
    "urn:rawlsing:prev3:authority:v557-publication-family:objective-position-fact:r1"
)
J04_AUTHORITY_VERSION = "J04@1.0.0"
J04_AUTHORITY_HASH = "7cd66ca4f8a413c3ad9bf5559a9b83d34103c421251081dad31aac580813c630"
J04_AUTHORITY_REF = M4AuthorityRef(
    J04_AUTHORITY_ID,
    J04_AUTHORITY_VERSION,
    J04_AUTHORITY_HASH,
)

PROVING_FACT_HASH = "c823a816ce6f71431c99b1a466c7313f3766e5d1e7832fc36b6a31f15835dd02"
PROVING_FACT_ID = f"PREV3POS:{PROVING_FACT_HASH}"
SOURCE_DOMAIN_USE = (
    "SECOND_CANARY_CONTRAST_AND_CONDITIONING_POSITION_OPERAND__NATIVE_0_VS_1"
)
M4_CONTEXT_USE = "CONTEXT"

_FORBIDDEN_SEMANTIC_TOKENS = (
    "PERSON_STATE",
    "PERSONA",
    "V3_PERSON",
    "V3_SUBJECT",
    "PSYCH",
    "BELIEF",
    "PREFERENCE",
    "MOTIVE",
    "TRAIT",
    "OBL063",
    "PRESENT_DAY_PERSISTENCE",
    "ACTIVE_CAUSAL",
)


class ObjectivePositionPublicationError(M4IntegrityError):
    """The bounded J04 owner-preserving publication contract failed closed."""


def _plain(value: Any) -> Any:
    """Return canonical JSON-safe producer material without changing semantics."""
    return canonicalize(value)


def _m4_ref(value: Any, name: str) -> M4ExactRef:
    if isinstance(value, M4ExactRef):
        return value
    if not isinstance(value, Mapping) or set(value) != {"kind", "object_id", "content_hash"}:
        raise ObjectivePositionPublicationError(
            f"{name} must contain exactly kind/object_id/content_hash"
        )
    return M4ExactRef(value["kind"], value["object_id"], value["content_hash"])


def _position_ref_as_m4(fact: ObjectivePositionFact) -> M4ExactRef:
    return M4ExactRef(
        fact.fact_ref.kind,
        fact.fact_ref.object_id,
        fact.fact_ref.content_hash,
    )


def _sequence(value: Any, name: str) -> tuple[Any, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise ObjectivePositionPublicationError(f"{name} must be a sequence")
    return tuple(value)


def _exact_ref_sequence(value: Any, name: str, *, nonempty: bool) -> tuple[M4ExactRef, ...]:
    raw = _sequence(value, name)
    refs = tuple(_m4_ref(item, name) for item in raw)
    if nonempty and not refs:
        raise ObjectivePositionPublicationError(f"{name} must not be empty")
    keys = [(ref.kind, ref.object_id, ref.content_hash) for ref in refs]
    if len(keys) != len(set(keys)):
        raise ObjectivePositionPublicationError(f"{name} contains duplicate exact refs")
    return tuple(sorted(refs, key=lambda ref: (ref.kind, ref.object_id, ref.content_hash)))


def _contains_forbidden_semantic_token(value: Any) -> str | None:
    text = repr(value).upper()
    for token in _FORBIDDEN_SEMANTIC_TOKENS:
        if token in text:
            return token
    return None


def _validated_fact_material(fact: ObjectivePositionFact) -> tuple[Mapping[str, Any], tuple[M4ExactRef, ...], M4ExactRef]:
    if not isinstance(fact, ObjectivePositionFact):
        raise ObjectivePositionPublicationError(
            "J04 publication requires exact positive ObjectivePositionFact"
        )
    if fact.state is not PositionResultState.POSITION_FACT_AUTHORIZED:
        raise ObjectivePositionPublicationError("nonpositive position state may not publish")
    if fact.fact_ref.kind != FACT_REF_KIND:
        raise ObjectivePositionPublicationError("objective-position fact ref kind mismatch")

    material = _plain(fact.canonical_material)
    if not isinstance(material, Mapping):
        raise ObjectivePositionPublicationError("canonical fact material must be mapping")
    if material.get("schema") != FACT_SCHEMA_ID:
        raise ObjectivePositionPublicationError("objective-position producer schema mismatch")
    if material.get("state") != POSITIVE_STATE:
        raise ObjectivePositionPublicationError("only POSITION_FACT_AUTHORIZED may publish")

    producer_hash = producer_semantic_hash(material)
    if fact.fact_ref.content_hash != producer_hash:
        raise ObjectivePositionPublicationError("producer content hash differs from canonical fact material")
    if fact.fact_ref.object_id != f"PREV3POS:{producer_hash}":
        raise ObjectivePositionPublicationError("PREV3POS object identity mismatch")

    # J04 is family-level authority with per-item authority required.  The only
    # concrete item-use binding issued in J04 R1 is this independently qualified
    # proving fact.  Other facts fail closed until separately bound.
    if fact.fact_ref.object_id != PROVING_FACT_ID or producer_hash != PROVING_FACT_HASH:
        raise ObjectivePositionPublicationError(
            "no exact J04 per-item publication/use binding for this objective-position fact"
        )

    uses = _sequence(material.get("allowed_uses"), "allowed_uses")
    if uses != (SOURCE_DOMAIN_USE,):
        raise ObjectivePositionPublicationError(
            "J04 R1 requires the exact singleton source-domain use ceiling"
        )

    evidence = _exact_ref_sequence(
        material.get("supporting_evidence_refs"),
        "supporting_evidence_refs",
        nonempty=True,
    )
    provenance = _exact_ref_sequence(
        material.get("provenance_refs"),
        "provenance_refs",
        nonempty=True,
    )
    dependencies = _exact_ref_sequence(
        material.get("dependency_refs"),
        "dependency_refs",
        nonempty=True,
    )
    if not evidence or not provenance:
        raise ObjectivePositionPublicationError("evidence/provenance closure must remain nonempty")

    role_receipt = material.get("position_role_receipt_ref")
    role_na = material.get("position_role_not_applicable_authority_ref")
    if (role_receipt is None) == (role_na is None):
        raise ObjectivePositionPublicationError("J04 preserves exact role-authority XOR semantics")

    negative = _m4_ref(material.get("negative_ceiling_ref"), "negative_ceiling_ref")
    valid_time = _m4_ref(material.get("valid_time_basis_ref"), "valid_time_basis_ref")
    currentness = _m4_ref(material.get("currentness_receipt_ref"), "currentness_receipt_ref")
    dep_keys = {(ref.kind, ref.object_id, ref.content_hash) for ref in dependencies}
    for required, name in (
        (negative, "negative_ceiling_ref"),
        (valid_time, "valid_time_basis_ref"),
        (currentness, "currentness_receipt_ref"),
    ):
        if (required.kind, required.object_id, required.content_hash) not in dep_keys:
            raise ObjectivePositionPublicationError(
                f"{name} must remain a member of canonical dependency closure"
            )

    predecessor = material.get("predecessor_position_fact_ref")
    if predecessor is not None:
        predecessor_ref = _m4_ref(predecessor, "predecessor_position_fact_ref")
        if predecessor_ref.kind != FACT_REF_KIND:
            raise ObjectivePositionPublicationError("predecessor position fact ref kind mismatch")
        if (
            predecessor_ref.kind,
            predecessor_ref.object_id,
            predecessor_ref.content_hash,
        ) not in dep_keys:
            raise ObjectivePositionPublicationError(
                "non-null predecessor position fact must remain closure-bound"
            )

    forbidden = _contains_forbidden_semantic_token(material)
    if forbidden:
        raise ObjectivePositionPublicationError(
            f"objective-world publication material contains forbidden semantic widening token {forbidden}"
        )

    return material, dependencies, negative


@dataclass(frozen=True)
class ObjectivePositionDomainUseBinding:
    fact_ref: M4ExactRef
    source_domain_use: str
    m4_permission_atom: str
    authority_ref: M4AuthorityRef
    binding_hash: str

    @property
    def ref(self) -> M4ExactRef:
        return M4ExactRef(
            "PREV3_OBJECTIVE_POSITION_DOMAIN_USE_BINDING",
            f"PREV3POSUSE:{self.binding_hash}",
            self.binding_hash,
        )


def _domain_use_binding_material(
    fact_ref: M4ExactRef,
    governance_ref: M4ExactRef,
) -> Mapping[str, Any]:
    return {
        "contract_id": CARRIER_CONTRACT_ID,
        "fact_ref": fact_ref.as_dict(),
        "source_domain_use": SOURCE_DOMAIN_USE,
        "m4_permission_atom": M4_CONTEXT_USE,
        "v557_decision_state": V557DecisionState.ALLOW_CONTEXT_ONLY.value,
        "v557_exception_state": V557ExceptionState.NO_EXCEPTION_STATE.value,
        "j04_authority_ref": J04_AUTHORITY_REF.as_dict(),
        "governance_ref": governance_ref.as_dict(),
        "bare_context_sufficient": False,
    }


def _domain_use_binding(
    fact_ref: M4ExactRef,
    governance_ref: M4ExactRef,
) -> ObjectivePositionDomainUseBinding:
    material = _domain_use_binding_material(fact_ref, governance_ref)
    h = m4_semantic_hash(material)
    return ObjectivePositionDomainUseBinding(
        fact_ref,
        SOURCE_DOMAIN_USE,
        M4_CONTEXT_USE,
        J04_AUTHORITY_REF,
        h,
    )


def _carrier_contract_hash() -> str:
    return m4_semantic_hash(
        {
            "contract_id": CARRIER_CONTRACT_ID,
            "contract_version": CARRIER_CONTRACT_VERSION,
            "j04_authority_ref": J04_AUTHORITY_REF.as_dict(),
            "producer_schema": FACT_SCHEMA_ID,
            "producer_family": FACT_REF_KIND,
            "positive_state": POSITIVE_STATE,
            "source_domain_use": SOURCE_DOMAIN_USE,
            "mapped_m4_atom": M4_CONTEXT_USE,
            "owner_preserving": True,
            "generic_m4_root_whitelist_widened": False,
        }
    )


CARRIER_CONTRACT_HASH = _carrier_contract_hash()


@dataclass(frozen=True)
class ObjectivePositionPublicationCarrier:
    fact_ref: M4ExactRef
    root_entry: RepositoryEntry
    publication: V557PublicationBundle
    repository: V558RepositoryBundle
    domain_use_binding: ObjectivePositionDomainUseBinding
    dependency_entries: tuple[RepositoryEntry, ...]
    dependency_external_bindings: tuple[ExternalResolutionBinding, ...]

    @property
    def replay_identity(self) -> Mapping[str, Any]:
        return {
            "fact_ref": self.fact_ref.as_dict(),
            "root_object_ref": self.root_entry.obj.ref.as_dict(),
            "governance_ref": self.root_entry.governance.ref.as_dict(),
            "publication_ref": self.publication.ref.as_dict(),
            "root_locator_ref": self.root_entry.locator.ref.as_dict(),
            "repository_ref": self.repository.ref.as_dict(),
            "domain_use_binding_ref": self.domain_use_binding.ref.as_dict(),
            "dependency_locator_refs": [
                entry.locator.ref.as_dict() for entry in self.dependency_entries
            ],
            "dependency_external_binding_ids": [
                binding.binding_id for binding in self.dependency_external_bindings
            ],
        }


def _guarded_publication_bundle(entry: V557PublicationEntry) -> V557PublicationBundle:
    """Build the exact J04 publication without widening generic M4 root law."""
    if entry.obj.producer_family != FACT_REF_KIND or entry.obj.semantic_class != FACT_REF_KIND:
        raise ReferenceClassError("J04 carrier rejects producer-family re-identification")
    if entry.obj.schema_id != FACT_SCHEMA_ID or entry.obj.schema_version != "1.0.0":
        raise ReferenceClassError("J04 carrier rejects objective-position schema mutation")
    if entry.obj.typed_state != POSITIVE_STATE:
        raise ReferenceClassError("J04 carrier admits only POSITION_FACT_AUTHORIZED")
    if entry.obj.object_id != PROVING_FACT_ID or entry.obj.content_hash != PROVING_FACT_HASH:
        raise ReferenceClassError("J04 per-item authority does not bind mutated PREV3POS identity")
    if entry.governance.decision_state is not V557DecisionState.ALLOW_CONTEXT_ONLY:
        raise ObjectivePositionPublicationError("J04 governance must be ALLOW_CONTEXT_ONLY")
    if entry.governance.exception_state is not V557ExceptionState.NO_EXCEPTION_STATE:
        raise ObjectivePositionPublicationError("J04 governance exception must be NO_EXCEPTION_STATE")
    if entry.governance.v557_allowed_uses != (M4_CONTEXT_USE,):
        raise ObjectivePositionPublicationError("J04 may grant only exact CONTEXT atom")

    entries = (entry,)
    material = _publication_material(entries)
    h = m4_semantic_hash(material)
    return V557PublicationBundle(
        f"V557PUB:{h}",
        h,
        material["schema"],
        entries,
    )


def _dependency_entry(
    ref: M4ExactRef,
    *,
    build_hash: str,
    ordinal: int,
) -> tuple[RepositoryEntry, ExternalResolutionBinding]:
    stub = make_external_stub(
        producer_family=DEPENDENCY_REFERENCE_FAMILY,
        semantic_class=ref.kind,
        object_id=ref.object_id,
        content_hash=ref.content_hash,
        schema_id=DEPENDENCY_REFERENCE_SCHEMA,
        schema_version="1.0.0",
        typed_state="EXACT_REFERENCE_ONLY",
        producer_allowed_uses=(M4_CONTEXT_USE,),
        source_stage=DEPENDENCY_SOURCE_STAGE,
    )
    if stub.ref != ref:
        raise ObjectivePositionPublicationError("dependency reference carrier re-identified exact ref")
    governance = govern_v557(
        stub,
        decision_state=V557DecisionState.ALLOW_CONTEXT_ONLY,
        v557_allowed_uses=(M4_CONTEXT_USE,),
        authority_ref=J04_AUTHORITY_REF,
        exception_state=V557ExceptionState.NO_EXCEPTION_STATE,
    )
    locator = make_producer_locator(
        stub,
        governance,
        logical_collection_kind=DEPENDENCY_REFERENCE_FAMILY,
        authoritative_build_id=f"K04-J04-DEPENDENCY-{ordinal}",
        authoritative_build_hash=build_hash,
        producer_contract_id=CARRIER_CONTRACT_ID,
        producer_contract_version=CARRIER_CONTRACT_VERSION,
        producer_contract_hash=CARRIER_CONTRACT_HASH,
        producer_rule_bindings=(J04_AUTHORITY_REF,),
        storage_locator=f"cas://sha256/{ref.content_hash}",
        provenance_locator=f"audit://K04/J04/dependency/{ref.content_hash}",
    )
    entry = RepositoryEntry(stub, governance, locator)
    binding = make_external_resolution_binding(stub, resolver_authority=J04_AUTHORITY_REF)
    return entry, binding


def publish_objective_position_fact(
    fact: ObjectivePositionFact,
) -> ObjectivePositionPublicationCarrier:
    """Package the exact J04-bound fact without changing its producer identity."""
    material, dependencies, negative = _validated_fact_material(fact)
    fact_ref = _position_ref_as_m4(fact)
    required = tuple(ref for ref in dependencies if ref != negative)

    root = StructuralObject(
        producer_family=FACT_REF_KIND,
        semantic_class=FACT_REF_KIND,
        object_id=fact_ref.object_id,
        content_hash=fact_ref.content_hash,
        schema_id=FACT_SCHEMA_ID,
        schema_version="1.0.0",
        typed_state=POSITIVE_STATE,
        producer_allowed_uses=(M4_CONTEXT_USE,),
        payload=material,
        source_stage=SOURCE_STAGE,
        required_dependency_refs=required,
        negative_dependency_refs=(negative,),
    )
    if root.ref != fact_ref:
        raise ObjectivePositionPublicationError("owner-preserving root changed PREV3POS exact ref")

    governance = govern_v557(
        root,
        decision_state=V557DecisionState.ALLOW_CONTEXT_ONLY,
        v557_allowed_uses=(M4_CONTEXT_USE,),
        authority_ref=J04_AUTHORITY_REF,
        exception_state=V557ExceptionState.NO_EXCEPTION_STATE,
    )
    publication = _guarded_publication_bundle(V557PublicationEntry(root, governance))

    build_material = {
        "contract_id": CARRIER_CONTRACT_ID,
        "fact_ref": fact_ref.as_dict(),
        "j04_authority_ref": J04_AUTHORITY_REF.as_dict(),
        "dependency_refs": [ref.as_dict() for ref in dependencies],
        "negative_ceiling_ref": negative.as_dict(),
    }
    build_hash = m4_semantic_hash(build_material)
    root_locator = make_producer_locator(
        root,
        governance,
        logical_collection_kind=FACT_REF_KIND,
        authoritative_build_id=f"K04-J04:{build_hash}",
        authoritative_build_hash=build_hash,
        producer_contract_id=CARRIER_CONTRACT_ID,
        producer_contract_version=CARRIER_CONTRACT_VERSION,
        producer_contract_hash=CARRIER_CONTRACT_HASH,
        producer_rule_bindings=(J04_AUTHORITY_REF,),
        provenance_locator=f"audit://K04/J04/objective-position/{fact_ref.content_hash}",
    )
    root_entry = RepositoryEntry(root, governance, root_locator)

    dependency_entries: list[RepositoryEntry] = []
    external_bindings: list[ExternalResolutionBinding] = []
    edges = []
    negative_key = (negative.kind, negative.object_id, negative.content_hash)
    for ordinal, dep in enumerate(dependencies, start=1):
        dep_entry, external = _dependency_entry(dep, build_hash=build_hash, ordinal=ordinal)
        dependency_entries.append(dep_entry)
        external_bindings.append(external)
        dep_key = (dep.kind, dep.object_id, dep.content_hash)
        edge_role = "NEGATIVE_LIMIT" if dep_key == negative_key else "REQUIRED_DEPENDENCY"
        edges.append(
            make_reference_edge(
                root_locator,
                dep_entry.locator,
                reference_contract=J04_AUTHORITY_REF,
                edge_role=edge_role,
                requiredness="REQUIRED",
                participant_role="NONE",
                declared_cardinality="1",
                multiplicity_key=str(ordinal),
                order_significant=False,
                semantic_ordinal=None,
            )
        )

    all_entries = (root_entry, *dependency_entries)
    repository = build_role_authenticated_v558_repository_bundle(
        publication,
        all_entries,
        reference_edges=tuple(edges),
        external_bindings=tuple(external_bindings),
    )
    binding = _domain_use_binding(fact_ref, governance.ref)

    carrier = ObjectivePositionPublicationCarrier(
        fact_ref,
        root_entry,
        publication,
        repository,
        binding,
        tuple(dependency_entries),
        tuple(external_bindings),
    )
    validate_objective_position_publication_carrier(carrier)
    return carrier


def validate_objective_position_publication_carrier(
    carrier: ObjectivePositionPublicationCarrier,
) -> ObjectivePositionPublicationCarrier:
    if not isinstance(carrier, ObjectivePositionPublicationCarrier):
        raise ObjectivePositionPublicationError("exact ObjectivePositionPublicationCarrier required")
    root = carrier.root_entry.obj
    if root.producer_family != FACT_REF_KIND or root.semantic_class != FACT_REF_KIND:
        raise ObjectivePositionPublicationError("carrier re-identifies objective-position producer family")
    if root.ref != carrier.fact_ref:
        raise ObjectivePositionPublicationError("carrier root ref differs from exact PREV3POS fact ref")
    if root.schema_id != FACT_SCHEMA_ID or root.schema_version != "1.0.0":
        raise ObjectivePositionPublicationError("carrier producer schema drift")
    if root.typed_state != POSITIVE_STATE:
        raise ObjectivePositionPublicationError("carrier promotes nonpositive position state")
    if root.producer_allowed_uses != (M4_CONTEXT_USE,):
        raise ObjectivePositionPublicationError("carrier root M4 permission must be exact CONTEXT singleton")
    gov = carrier.root_entry.governance
    if (
        gov.authority_ref != J04_AUTHORITY_REF
        or gov.decision_state is not V557DecisionState.ALLOW_CONTEXT_ONLY
        or gov.exception_state is not V557ExceptionState.NO_EXCEPTION_STATE
        or gov.v557_allowed_uses != (M4_CONTEXT_USE,)
    ):
        raise ObjectivePositionPublicationError("carrier governance differs from exact J04 mapping")
    if carrier.publication.entries != (V557PublicationEntry(root, gov),):
        raise ObjectivePositionPublicationError("publication contains non-J04 root or extra roots")
    if carrier.repository.publication_bundle_ref != carrier.publication.ref:
        raise ObjectivePositionPublicationError("V558 repository does not bind exact guarded publication")
    if carrier.domain_use_binding.fact_ref != carrier.fact_ref:
        raise ObjectivePositionPublicationError("source-domain use binding fact ref mismatch")
    if (
        carrier.domain_use_binding.source_domain_use != SOURCE_DOMAIN_USE
        or carrier.domain_use_binding.m4_permission_atom != M4_CONTEXT_USE
        or carrier.domain_use_binding.authority_ref != J04_AUTHORITY_REF
    ):
        raise ObjectivePositionPublicationError("source-domain use binding widened or drifted")
    expected_binding = _domain_use_binding(carrier.fact_ref, gov.ref)
    if carrier.domain_use_binding != expected_binding:
        raise ObjectivePositionPublicationError("source-domain use binding identity/hash mismatch")

    # Generic M4 remains closed to this family.  If this succeeds, somebody has
    # performed the forbidden naked whitelist expansion underneath K04.
    try:
        build_v557_publication_bundle((V557PublicationEntry(root, gov),))
    except ReferenceClassError:
        pass
    else:
        raise ObjectivePositionPublicationError(
            "generic M4 root-family whitelist was widened; guarded carrier invariant violated"
        )
    return carrier


def make_bound_objective_position_context_query(
    carrier: ObjectivePositionPublicationCarrier,
    *,
    requested_source_domain_use: str,
) -> ContextQuery:
    validate_objective_position_publication_carrier(carrier)
    if requested_source_domain_use != SOURCE_DOMAIN_USE:
        raise ObjectivePositionPublicationError(
            "requested source-domain use lacks exact J04 item-use mapping authority"
        )
    item = ContextQueryItem(
        exact_resolution_key(carrier.root_entry.locator),
        (M4_CONTEXT_USE,),
    )
    return make_context_query(
        (item,),
        generated_binding_refs=(carrier.domain_use_binding.ref,),
    )


def require_bound_objective_position_context_query(
    carrier: ObjectivePositionPublicationCarrier,
    query: ContextQuery,
) -> ContextQuery:
    validate_objective_position_publication_carrier(carrier)
    if not isinstance(query, ContextQuery):
        raise ObjectivePositionPublicationError("exact ContextQuery required")
    if len(query.items) != 1:
        raise ObjectivePositionPublicationError("J04 R1 permits one exact proving-fact query item")
    item = query.items[0]
    if item.resolution_key != exact_resolution_key(carrier.root_entry.locator):
        raise ObjectivePositionPublicationError("query re-identifies objective-position V558 root")
    if item.requested_uses != (M4_CONTEXT_USE,):
        raise ObjectivePositionPublicationError(
            "J04 CONTEXT mapping does not authorize REVIEW or ACTIVE_CAUSAL"
        )
    if query.generated_binding_refs != (carrier.domain_use_binding.ref,):
        raise ObjectivePositionPublicationError(
            "bare CONTEXT is insufficient; exact source-domain use binding is required"
        )
    return query


def resolve_bound_objective_position_context(
    carrier: ObjectivePositionPublicationCarrier,
    query: ContextQuery,
    *,
    external_store: Mapping[str, Mapping[str, Any]] | None = None,
) -> ResolutionResult:
    """Enter the frozen V558 resolver only after the J04 item-use guard passes.

    Exact dependency objects remain CAS-bound.  If their immutable bodies are
    unavailable, the inherited V558 resolver fails closed with integrity state;
    this adapter never invents dependency payloads from hashes.
    """
    require_bound_objective_position_context_query(carrier, query)
    return resolve_v558(carrier.repository, query, external_store=external_store)


def replay_objective_position_publication(
    fact: ObjectivePositionFact,
    expected: ObjectivePositionPublicationCarrier,
) -> ObjectivePositionPublicationCarrier:
    replayed = publish_objective_position_fact(fact)
    if replayed.replay_identity != expected.replay_identity:
        raise ObjectivePositionPublicationError("deterministic V557/V558 carrier replay mismatch")
    return replayed


__all__ = [
    "CARRIER_CONTRACT_ID",
    "CARRIER_CONTRACT_VERSION",
    "CARRIER_CONTRACT_HASH",
    "J04_AUTHORITY_ID",
    "J04_AUTHORITY_VERSION",
    "J04_AUTHORITY_HASH",
    "J04_AUTHORITY_REF",
    "PROVING_FACT_HASH",
    "PROVING_FACT_ID",
    "SOURCE_DOMAIN_USE",
    "M4_CONTEXT_USE",
    "ObjectivePositionPublicationError",
    "ObjectivePositionDomainUseBinding",
    "ObjectivePositionPublicationCarrier",
    "publish_objective_position_fact",
    "validate_objective_position_publication_carrier",
    "make_bound_objective_position_context_query",
    "require_bound_objective_position_context_query",
    "resolve_bound_objective_position_context",
    "replay_objective_position_publication",
]
