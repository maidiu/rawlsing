"""Source-agnostic objective structural-topology contract and producer.

This module carries only exact upstream references.  It does not infer topology,
interpret source payloads, derive semantic labels, select an authority owner, or
mint downstream identities from descriptive text.  A competent upstream owner
must supply every structural reference, semantic-owner provenance reference,
scope reference, and closure-authority reference material exactly.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash

CONTRACT_ID = "PREV3_OBJECTIVE_STRUCTURAL_TOPOLOGY_PRODUCT_CONTRACT_R1@1.0.0"
CLOSURE_CONTRACT_ID = "PREV3_OBJECTIVE_STRUCTURAL_TOPOLOGY_CLOSURE_AUTHORITY_R1@1.0.0"
REPLAY_CONTRACT_ID = "PREV3_OBJECTIVE_STRUCTURAL_TOPOLOGY_REPLAY_R1@1.0.0"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ObjectiveStructuralTopologyIntegrityError(ValueError):
    """An exact structural-topology reference, scope, or authority binding is invalid."""


class ObjectiveStructuralTopologyReplayError(AssertionError):
    """A deterministic topology replay failed exact identity parity."""


def _exact_ref(value: object, name: str) -> ExactRef:
    if not isinstance(value, ExactRef):
        raise ObjectiveStructuralTopologyIntegrityError(f"{name} must be an ExactRef")
    return value


def _authority_ref(value: object, name: str) -> AuthorityRef:
    if not isinstance(value, AuthorityRef):
        raise ObjectiveStructuralTopologyIntegrityError(f"{name} must be an AuthorityRef")
    return value


def _sha256(value: object, name: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise ObjectiveStructuralTopologyIntegrityError(f"{name} must be a lowercase sha256")
    return value


@dataclass(frozen=True, order=True)
class StructuralTopologyScope:
    """Exact scope coordinates supplied by competent upstream owners."""

    claim_scope_ref: ExactRef
    relation_scope_ref: ExactRef
    applicability_scope_ref: ExactRef
    permission_scope_ref: ExactRef

    def __post_init__(self) -> None:
        for field in (
            "claim_scope_ref",
            "relation_scope_ref",
            "applicability_scope_ref",
            "permission_scope_ref",
        ):
            object.__setattr__(self, field, _exact_ref(getattr(self, field), field))

    def as_dict(self) -> dict[str, object]:
        return {
            "claim_scope_ref": self.claim_scope_ref.as_dict(),
            "relation_scope_ref": self.relation_scope_ref.as_dict(),
            "applicability_scope_ref": self.applicability_scope_ref.as_dict(),
            "permission_scope_ref": self.permission_scope_ref.as_dict(),
        }


@dataclass(frozen=True, order=True)
class SemanticOwnerProvenance:
    """Exact semantic-owner and reference-contract provenance; no owner inference."""

    semantic_owner_ref: AuthorityRef
    reference_contract_ref: ExactRef

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "semantic_owner_ref",
            _authority_ref(self.semantic_owner_ref, "semantic_owner_ref"),
        )
        object.__setattr__(
            self,
            "reference_contract_ref",
            _exact_ref(self.reference_contract_ref, "reference_contract_ref"),
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "semantic_owner_ref": self.semantic_owner_ref.as_dict(),
            "reference_contract_ref": self.reference_contract_ref.as_dict(),
        }


def _require_scope(value: object) -> StructuralTopologyScope:
    if not isinstance(value, StructuralTopologyScope):
        raise ObjectiveStructuralTopologyIntegrityError("scope must be StructuralTopologyScope")
    return value


def _require_provenance(value: object) -> SemanticOwnerProvenance:
    if not isinstance(value, SemanticOwnerProvenance):
        raise ObjectiveStructuralTopologyIntegrityError(
            "semantic_owner_provenance must be SemanticOwnerProvenance"
        )
    return value


def topology_payload_projection(
    *,
    source_structural_position_ref: ExactRef,
    structural_channel_ref: ExactRef,
    receiving_structural_position_ref: ExactRef,
    semantic_owner_provenance: SemanticOwnerProvenance,
    scope: StructuralTopologyScope,
) -> dict[str, object]:
    """Return exact pre-closure semantic material; this computes identity, not authority."""

    source_ref = _exact_ref(source_structural_position_ref, "source_structural_position_ref")
    channel_ref = _exact_ref(structural_channel_ref, "structural_channel_ref")
    receiving_ref = _exact_ref(receiving_structural_position_ref, "receiving_structural_position_ref")
    provenance = _require_provenance(semantic_owner_provenance)
    exact_scope = _require_scope(scope)
    return {
        "contract_id": CONTRACT_ID,
        "source_structural_position_ref": source_ref.as_dict(),
        "structural_channel_ref": channel_ref.as_dict(),
        "receiving_structural_position_ref": receiving_ref.as_dict(),
        "semantic_owner_provenance": provenance.as_dict(),
        "scope": exact_scope.as_dict(),
    }


def topology_payload_hash(**kwargs: object) -> str:
    """Compute the content address a competent closure authority must bind."""

    return semantic_hash(topology_payload_projection(**kwargs))


@dataclass(frozen=True)
class ContentAddressedClosureAuthority:
    """Upstream authority binding over one exact topology payload.

    ``authority_owner_ref`` proves who/what supplied the authority identity;
    this generic contract neither selects nor upgrades that owner.
    """

    authority_owner_ref: AuthorityRef
    authority_contract_ref: ExactRef
    source_structural_position_ref: ExactRef
    structural_channel_ref: ExactRef
    receiving_structural_position_ref: ExactRef
    semantic_owner_provenance: SemanticOwnerProvenance
    scope: StructuralTopologyScope
    authorized_topology_payload_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "authority_owner_ref",
            _authority_ref(self.authority_owner_ref, "authority_owner_ref"),
        )
        for field in (
            "authority_contract_ref",
            "source_structural_position_ref",
            "structural_channel_ref",
            "receiving_structural_position_ref",
        ):
            object.__setattr__(self, field, _exact_ref(getattr(self, field), field))
        object.__setattr__(
            self,
            "semantic_owner_provenance",
            _require_provenance(self.semantic_owner_provenance),
        )
        object.__setattr__(self, "scope", _require_scope(self.scope))
        object.__setattr__(
            self,
            "authorized_topology_payload_hash",
            _sha256(self.authorized_topology_payload_hash, "authorized_topology_payload_hash"),
        )
        expected = topology_payload_hash(
            source_structural_position_ref=self.source_structural_position_ref,
            structural_channel_ref=self.structural_channel_ref,
            receiving_structural_position_ref=self.receiving_structural_position_ref,
            semantic_owner_provenance=self.semantic_owner_provenance,
            scope=self.scope,
        )
        if self.authorized_topology_payload_hash != expected:
            raise ObjectiveStructuralTopologyIntegrityError(
                "closure authority payload hash does not match its exact bound topology"
            )

    def semantic_projection(self) -> dict[str, object]:
        return {
            "contract_id": CLOSURE_CONTRACT_ID,
            "authority_owner_ref": self.authority_owner_ref.as_dict(),
            "authority_contract_ref": self.authority_contract_ref.as_dict(),
            "source_structural_position_ref": self.source_structural_position_ref.as_dict(),
            "structural_channel_ref": self.structural_channel_ref.as_dict(),
            "receiving_structural_position_ref": self.receiving_structural_position_ref.as_dict(),
            "semantic_owner_provenance": self.semantic_owner_provenance.as_dict(),
            "scope": self.scope.as_dict(),
            "authorized_topology_payload_hash": self.authorized_topology_payload_hash,
        }

    @property
    def exact_ref(self) -> ExactRef:
        content_hash = semantic_hash(self.semantic_projection())
        return ExactRef(
            kind="OBJECTIVE_STRUCTURAL_TOPOLOGY_CLOSURE_AUTHORITY",
            object_id=f"closure:{content_hash[:24]}",
            content_hash=content_hash,
        )


@dataclass(frozen=True)
class ObjectiveStructuralTopologyProduct:
    """Exact source-position -> channel -> receiving-position objective topology product."""

    source_structural_position_ref: ExactRef
    structural_channel_ref: ExactRef
    receiving_structural_position_ref: ExactRef
    semantic_owner_provenance: SemanticOwnerProvenance
    scope: StructuralTopologyScope
    content_addressed_closure_authority: ContentAddressedClosureAuthority
    topology_payload_hash: str

    def __post_init__(self) -> None:
        for field in (
            "source_structural_position_ref",
            "structural_channel_ref",
            "receiving_structural_position_ref",
        ):
            object.__setattr__(self, field, _exact_ref(getattr(self, field), field))
        object.__setattr__(
            self,
            "semantic_owner_provenance",
            _require_provenance(self.semantic_owner_provenance),
        )
        object.__setattr__(self, "scope", _require_scope(self.scope))
        if not isinstance(self.content_addressed_closure_authority, ContentAddressedClosureAuthority):
            raise ObjectiveStructuralTopologyIntegrityError(
                "content_addressed_closure_authority must be ContentAddressedClosureAuthority"
            )
        object.__setattr__(
            self,
            "topology_payload_hash",
            _sha256(self.topology_payload_hash, "topology_payload_hash"),
        )
        expected_hash = topology_payload_hash(
            source_structural_position_ref=self.source_structural_position_ref,
            structural_channel_ref=self.structural_channel_ref,
            receiving_structural_position_ref=self.receiving_structural_position_ref,
            semantic_owner_provenance=self.semantic_owner_provenance,
            scope=self.scope,
        )
        if self.topology_payload_hash != expected_hash:
            raise ObjectiveStructuralTopologyIntegrityError(
                "product topology_payload_hash does not match exact topology payload"
            )
        closure = self.content_addressed_closure_authority
        if (
            closure.source_structural_position_ref != self.source_structural_position_ref
            or closure.structural_channel_ref != self.structural_channel_ref
            or closure.receiving_structural_position_ref != self.receiving_structural_position_ref
            or closure.semantic_owner_provenance != self.semantic_owner_provenance
            or closure.scope != self.scope
            or closure.authorized_topology_payload_hash != self.topology_payload_hash
        ):
            raise ObjectiveStructuralTopologyIntegrityError(
                "closure authority is not bound to the exact product topology"
            )

    def semantic_projection(self) -> dict[str, object]:
        return {
            **topology_payload_projection(
                source_structural_position_ref=self.source_structural_position_ref,
                structural_channel_ref=self.structural_channel_ref,
                receiving_structural_position_ref=self.receiving_structural_position_ref,
                semantic_owner_provenance=self.semantic_owner_provenance,
                scope=self.scope,
            ),
            "topology_payload_hash": self.topology_payload_hash,
            "content_addressed_closure_authority_ref": (
                self.content_addressed_closure_authority.exact_ref.as_dict()
            ),
        }

    @property
    def exact_ref(self) -> ExactRef:
        content_hash = semantic_hash(self.semantic_projection())
        return ExactRef(
            kind="OBJECTIVE_STRUCTURAL_TOPOLOGY_PRODUCT",
            object_id=f"topology:{content_hash[:24]}",
            content_hash=content_hash,
        )


def produce_objective_structural_topology(
    *,
    source_structural_position_ref: ExactRef,
    structural_channel_ref: ExactRef,
    receiving_structural_position_ref: ExactRef,
    semantic_owner_provenance: SemanticOwnerProvenance,
    scope: StructuralTopologyScope,
    content_addressed_closure_authority: ContentAddressedClosureAuthority,
) -> ObjectiveStructuralTopologyProduct:
    """Produce one exact topology product from already-authorized exact references only."""

    payload_hash = topology_payload_hash(
        source_structural_position_ref=source_structural_position_ref,
        structural_channel_ref=structural_channel_ref,
        receiving_structural_position_ref=receiving_structural_position_ref,
        semantic_owner_provenance=semantic_owner_provenance,
        scope=scope,
    )
    return ObjectiveStructuralTopologyProduct(
        source_structural_position_ref=source_structural_position_ref,
        structural_channel_ref=structural_channel_ref,
        receiving_structural_position_ref=receiving_structural_position_ref,
        semantic_owner_provenance=semantic_owner_provenance,
        scope=scope,
        content_addressed_closure_authority=content_addressed_closure_authority,
        topology_payload_hash=payload_hash,
    )


@dataclass(frozen=True)
class StructuralTopologyReplayReceipt:
    original_product_ref: ExactRef
    replayed_product_ref: ExactRef
    closure_authority_ref: ExactRef
    topology_payload_hash: str
    content_hash: str

    def __post_init__(self) -> None:
        for field in ("original_product_ref", "replayed_product_ref", "closure_authority_ref"):
            object.__setattr__(self, field, _exact_ref(getattr(self, field), field))
        object.__setattr__(
            self,
            "topology_payload_hash",
            _sha256(self.topology_payload_hash, "topology_payload_hash"),
        )
        object.__setattr__(self, "content_hash", _sha256(self.content_hash, "content_hash"))

    def semantic_projection(self) -> dict[str, object]:
        return {
            "contract_id": REPLAY_CONTRACT_ID,
            "original_product_ref": self.original_product_ref.as_dict(),
            "replayed_product_ref": self.replayed_product_ref.as_dict(),
            "closure_authority_ref": self.closure_authority_ref.as_dict(),
            "topology_payload_hash": self.topology_payload_hash,
        }

    @property
    def exact_ref(self) -> ExactRef:
        return ExactRef(
            kind="OBJECTIVE_STRUCTURAL_TOPOLOGY_REPLAY_RECEIPT",
            object_id=f"replay:{self.content_hash[:24]}",
            content_hash=self.content_hash,
        )

    def verify(self) -> None:
        if self.original_product_ref != self.replayed_product_ref:
            raise ObjectiveStructuralTopologyReplayError(
                "replayed topology product identity differs from original"
            )
        if semantic_hash(self.semantic_projection()) != self.content_hash:
            raise ObjectiveStructuralTopologyReplayError(
                "topology replay receipt content hash mismatch"
            )


def replay_objective_structural_topology(
    product: ObjectiveStructuralTopologyProduct,
) -> StructuralTopologyReplayReceipt:
    """Reproduce an exact product from its bound refs and prove identity parity."""

    if not isinstance(product, ObjectiveStructuralTopologyProduct):
        raise ObjectiveStructuralTopologyIntegrityError(
            "product must be ObjectiveStructuralTopologyProduct"
        )
    replayed = produce_objective_structural_topology(
        source_structural_position_ref=product.source_structural_position_ref,
        structural_channel_ref=product.structural_channel_ref,
        receiving_structural_position_ref=product.receiving_structural_position_ref,
        semantic_owner_provenance=product.semantic_owner_provenance,
        scope=product.scope,
        content_addressed_closure_authority=product.content_addressed_closure_authority,
    )
    if replayed.exact_ref != product.exact_ref:
        raise ObjectiveStructuralTopologyReplayError(
            "deterministic replay did not reproduce exact topology product identity"
        )
    projection = {
        "contract_id": REPLAY_CONTRACT_ID,
        "original_product_ref": product.exact_ref.as_dict(),
        "replayed_product_ref": replayed.exact_ref.as_dict(),
        "closure_authority_ref": product.content_addressed_closure_authority.exact_ref.as_dict(),
        "topology_payload_hash": product.topology_payload_hash,
    }
    receipt = StructuralTopologyReplayReceipt(
        original_product_ref=product.exact_ref,
        replayed_product_ref=replayed.exact_ref,
        closure_authority_ref=product.content_addressed_closure_authority.exact_ref,
        topology_payload_hash=product.topology_payload_hash,
        content_hash=semantic_hash(projection),
    )
    receipt.verify()
    return receipt
