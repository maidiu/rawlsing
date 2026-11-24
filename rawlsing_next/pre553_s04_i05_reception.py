"""Upstream S04 reception of I05's exact executed research frontier.

I05 is the existing computational discovery owner. This is NOT a second
discovery engine, a new adaptive search/branch selector or a statistical
significance policy. Selected source-backed role facts remain real I03 facts
even if I05's *particular validation* returns VALID_EMPTY.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from typing import Any, Callable, Mapping

from rawlsing_next._pre553_query_common import QUERY_EXECUTION_CONTRACT_ID, QueryExecutionResult
from rawlsing_next.pre553_discovery_exact import (
    COVERAGE_CLAIM, ExactBoundedDiscoveryResult, I05_CONTRACT_ID, TERMINAL_COVERAGE_STATES,
    _derived_ref as _i05_derived_ref,
)
from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonical_json, canonicalize, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_s04_observed_research import (
    S04ObservedKnowledge, receive_s04_i03_research,
)

CONTRACT = "S04_SOURCE_EXACT_I05_ROLE_RECEPTION@1.0.0"


class S04I05ReceptionError(ValueError):
    """A selected I05 candidate role cannot be sourced to its real I03 fact."""


@dataclass(frozen=True)
class S04I05RoleKnowledge:
    canonical_payload: str
    digest: str

    def __post_init__(self) -> None:
        value = loads(self.canonical_payload)
        if (canonical_json(value) != self.canonical_payload
                or value.get("contract") != CONTRACT
                or semantic_hash(value) != self.digest):
            raise S04I05ReceptionError("role knowledge identity mismatch")

    @property
    def ref(self) -> ExactRef:
        return ExactRef(CONTRACT, f"urn:rawlsing:s04:i05-role:sha256:{self.digest}", self.digest)

    def material(self) -> dict[str, Any]:
        return loads(self.canonical_payload)


def _ref(value: Any, label: str) -> ExactRef:
    try:
        return exact_ref(value, label)
    except (AttributeError, KeyError, ValueError, TypeError) as exc:
        raise S04I05ReceptionError(f"invalid exact {label} ref") from exc


def receive_s04_i05_role(
    *,
    discovery: ExactBoundedDiscoveryResult,
    candidate_receipt_ref: ExactRef,
    query_role: str,
) -> tuple[S04ObservedKnowledge, S04I05RoleKnowledge]:
    """Read an authentic I05-executed role as S04 observed knowledge.

    The query envelope is *reconstructed* from I05's owner-retained original
    fact/query/receipt. No new I03 execution or source-authority issuance occurs.
    """
    if type(discovery) is not ExactBoundedDiscoveryResult:
        raise S04I05ReceptionError("exact I05 original frontier required")
    if type(candidate_receipt_ref) is not ExactRef or not isinstance(query_role, str) or not query_role.strip():
        raise S04I05ReceptionError("exact I05 candidate and nonempty role required")
    candidates = [r for r in discovery.receipts if r.ref == candidate_receipt_ref]
    if len(candidates) != 1:
        raise S04I05ReceptionError("candidate receipt not uniquely present in I05 frontier")
    receipt = candidates[0]
    if (semantic_hash(receipt.semantic_projection()) != receipt.content_hash
            or _ref(receipt.evaluated_frontier_ref, "frontier") != discovery.evaluated_frontier_ref
            or _ref(receipt.discovery_authority_ref, "authority") != discovery.discovery_authority_ref):
        raise S04I05ReceptionError("receipt lost hash/frontier/authority closure")
    if receipt.coverage_state not in TERMINAL_COVERAGE_STATES:
        raise S04I05ReceptionError("I05 candidate has nonterminal frontier coverage")
    identity = receipt.candidate_identity
    if not isinstance(identity, Mapping) or not isinstance(identity.get("query_roles"), (tuple, list)):
        raise S04I05ReceptionError("candidate lacks executed role identities")
    roles = [x for x in identity["query_roles"] if isinstance(x, Mapping) and x.get("role") == query_role]
    if len(roles) != 1:
        raise S04I05ReceptionError("candidate has no unique selected query role")
    role = roles[0]
    query_ref = _ref(role.get("query_ref"), "query")
    predicate_ref = _ref(role.get("predicate_ref"), "predicate")
    queries = [q for q in discovery.executed_queries if q.ref == query_ref]
    predicates = [p for p in discovery.executed_predicates if p.ref == predicate_ref]
    if len(queries) != 1 or len(predicates) != 1:
        raise S04I05ReceptionError("selected role original query/predicate not retained")
    query, predicate = queries[0], predicates[0]
    if (_ref(query.condition_predicate_ref, "query predicate") != predicate.ref
            or semantic_hash(query.semantic_projection()) != query.content_hash
            or semantic_hash(predicate.semantic_projection()) != predicate.content_hash):
        raise S04I05ReceptionError("selected role query/predicate altered")
    support = receipt.support_uncertainty_state
    if not isinstance(support, Mapping) or not isinstance(support.get("query_role_fact_refs"), Mapping):
        raise S04I05ReceptionError("candidate has no source-owned role→fact closure")
    original_fact_refs = support["query_role_fact_refs"].get(query_role)
    if not isinstance(original_fact_refs, (list, tuple)) or len(original_fact_refs) != 1:
        raise S04I05ReceptionError("selected role has no single original source fact")
    fact_ref = _ref(original_fact_refs[0], "I05 owned fact")
    # Canonical I05 receipt fields may deserialize as frozen MappingProxyType
    # dictionaries rather than hashable ExactRef instances. Normalize every
    # source reference through the *existing* exact-ref contract before set
    # membership. Never hash the raw serialized mappings or compare by object id.
    receipt_fact_refs = tuple(
        _ref(value, "candidate empirical fact") for value in receipt.empirical_fact_refs
    )
    frontier_fact_refs = tuple(
        _ref(value, "frontier empirical fact") for value in discovery.empirical_fact_refs
    )
    if (len(set(receipt_fact_refs)) != len(receipt_fact_refs)
            or len(set(frontier_fact_refs)) != len(frontier_fact_refs)):
        raise S04I05ReceptionError("duplicate exact empirical fact identity in I05 custody")
    if fact_ref not in receipt_fact_refs or fact_ref not in frontier_fact_refs:
        raise S04I05ReceptionError("source fact not part of exact validated I05 frontier")
    selected = [f for f in discovery.empirical_facts if f.ref == fact_ref]
    if len(selected) != 1 or _ref(selected[0].empirical_query_spec_ref, "fact query") != query.ref:
        raise S04I05ReceptionError("I05 fact/query original closure lost")
    if _ref(selected[0].condition_predicate_ref, "fact predicate") != predicate.ref:
        raise S04I05ReceptionError("I05 fact condition predicate changed")
    releases = tuple(_ref(x, "source release") for x in receipt.source_release_refs)
    if len(releases) != 1 or releases[0] not in {
            _ref(x, "fact provenance") for x in selected[0].source_empirical_provenance_refs}:
        raise S04I05ReceptionError("I05 original source/release authority absent")
    execution = QueryExecutionResult(
        query_ref=query.ref,
        facts=(selected[0],),
        source_scope_mode="SINGLE_UNIVERSE",
        release_refs=releases,
    )
    observed = receive_s04_i03_research(query=query, execution=execution)
    source = observed.material()
    if _ref(source["fact_ref"], "S04 fact") != fact_ref:
        raise S04I05ReceptionError("S04 fact changed during I05 reception")
    material = {
        "contract": CONTRACT,
        "claim_grade": "REAL_I05_ROLE_FACT_TO_S04__SOURCEFREE_OWNER_RECONCILIATION_HELD",
        "candidate_receipt_ref": receipt.ref.as_dict(),
        "candidate_validation_state": receipt.typed_state,
        "candidate_coverage_state": receipt.coverage_state,
        "candidate_identity": canonicalize(identity),
        "query_role": query_role,
        "query_ref": query.ref.as_dict(),
        "predicate_ref": predicate.ref.as_dict(),
        "fact_ref": fact_ref.as_dict(),
        "source_release_ref": releases[0].as_dict(),
        "discovery_authority_ref": discovery.discovery_authority_ref.as_dict(),
        "discovery_frontier_ref": discovery.evaluated_frontier_ref.as_dict(),
        "discovery_replay_ref": discovery.replay_ref.as_dict(),
        "s04_observed_ref": observed.ref.as_dict(),
        "not_proven": [
            "NO_NEW_I03_EXECUTION__ENVELOPE_RECONSTRUCTED_FROM_I05_OWNER_FACT",
            "VALID_EMPTY_CANDIDATE_IS_NOT_MISSING_EMPIRICAL_JOINT",
            "NO_DATA_ADAPTIVE_RECURSIVE_SEARCH_OR_SCIENTIFIC_STOPPING_ISSUANCE",
            "NO_FIELD_FORGE_OR_ACTOR_AUTHORITY_GRANTED",
        ],
    }
    h = semantic_hash(material)
    return observed, S04I05RoleKnowledge(canonical_json(material), h)


def _require_pinned_frontier(discovery, expected_replay_ref):
    """Recheck the incumbent I05 replay law, not just a supplied ref field.

    The scheduler must not accept an omitted or substituted candidate as a
    sealed unit. This is a byte/identity check against an external pin, not
    independent issuance or a fresh scientific evaluation.
    """
    receipts = discovery.receipts
    if (type(discovery.candidate_count) is not int
            or discovery.candidate_count != len(receipts)
            or discovery.covered_candidate_count != len(receipts)
            or len({r.ref for r in receipts}) != len(receipts)):
        raise S04I05ReceptionError("incomplete or duplicate I05 frontier receipts")
    cited = set()
    candidate_ids = set()
    candidate_hashes = set()
    candidate_identities = []
    cited_queries = set()
    cited_predicates = set()
    for receipt in receipts:
        if (semantic_hash(receipt.semantic_projection()) != receipt.content_hash
                or _ref(receipt.discovery_authority_ref, "authority") != discovery.discovery_authority_ref
                or _ref(receipt.evaluated_frontier_ref, "frontier") != discovery.evaluated_frontier_ref
                or receipt.coverage_state not in TERMINAL_COVERAGE_STATES):
            raise S04I05ReceptionError("nonterminal or altered I05 frontier receipt")
        candidate_id = receipt.candidate_identity.get("candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id or candidate_id in candidate_ids:
            raise S04I05ReceptionError("duplicate or absent I05 candidate identity")
        candidate_ids.add(candidate_id)
        identity = receipt.candidate_identity
        candidate_hash = identity.get("candidate_hash")
        if (not isinstance(candidate_hash, str) or candidate_hash in candidate_hashes
                or candidate_id != f"urn:rawlsing:pre553:i05:candidate:sha256:{candidate_hash}"):
            raise S04I05ReceptionError("invalid or duplicate I05 frontier candidate hash")
        # Reconstruct the native candidate preimage in native role order.
        # The receipt is pinned, but the enclosing grammar field is not
        # independently included in the final replay preimage.
        roles = identity["query_roles"]
        material = {
            "contract": I05_CONTRACT_ID,
            "family": identity["family"],
            "rule_id": identity["rule_id"],
            "winning_predicate_ref": _ref(receipt.winning_predicate_ref, "winner").as_dict(),
            "query_roles": roles,
            "validation": identity["validation"],
            "ancestry_refs": [
                ref.as_dict() for ref in sorted(
                    {_ref(value, "ancestry") for value in receipt.branch_or_parent_ancestry_refs},
                    key=lambda ref: ref.key)
            ],
        }
        if semantic_hash(material) != candidate_hash:
            raise S04I05ReceptionError("I05 frontier candidate preimage changed")
        candidate_hashes.add(candidate_hash)
        candidate_identities.append({"candidate_id": candidate_id, "candidate_hash": candidate_hash})
        for role in roles:
            cited_queries.add(_ref(role["query_ref"], "frontier role query"))
            cited_predicates.add(_ref(role["predicate_ref"], "frontier role predicate"))
        cited.update(_ref(ref, "frontier role fact") for ref in receipt.empirical_fact_refs)
    # Native _compile_frontier orders by candidate_hash, not receipt ref.
    # Reconstruct the original frontier using precisely that ordering and
    # the incumbent I05 reference namespace. No new authority is issued.
    actual_frontier = _i05_derived_ref("PRE553_I05_EVALUATED_FRONTIER", "frontier", {
        "contract": I05_CONTRACT_ID,
        "discovery_authority_ref": discovery.discovery_authority_ref.as_dict(),
        "candidate_grammar_ref": discovery.candidate_grammar_ref.as_dict(),
        "query_execution_contract": QUERY_EXECUTION_CONTRACT_ID,
        "candidate_identities": sorted(candidate_identities, key=lambda item: item["candidate_hash"]),
        "coverage_claim": COVERAGE_CLAIM,
    })
    if (discovery.contract_id != I05_CONTRACT_ID or discovery.coverage_claim != COVERAGE_CLAIM
            or actual_frontier != discovery.evaluated_frontier_ref):
        raise S04I05ReceptionError("I05 frontier grammar or candidate identity changed")
    for objects, expected in ((discovery.executed_queries, cited_queries),
                              (discovery.executed_predicates, cited_predicates)):
        if len(objects) != len(expected) or {obj.ref for obj in objects} != expected:
            raise S04I05ReceptionError("I05 exact frontier role object census changed")
        if any(semantic_hash(obj.semantic_projection()) != obj.content_hash for obj in objects):
            raise S04I05ReceptionError("I05 exact frontier role preimage changed")
    if cited != set(discovery.empirical_fact_refs):
        raise S04I05ReceptionError("I05 frontier fact closure changed")
    if tuple(fact.ref for fact in discovery.empirical_facts) != discovery.empirical_fact_refs:
        raise S04I05ReceptionError("I05 exact frontier fact preimage census changed")
    for fact in discovery.empirical_facts:
        if semantic_hash(fact.semantic_projection()) != fact.content_hash:
            raise S04I05ReceptionError("altered I05 frontier fact preimage")
    empty = not receipts or all(r.typed_state == "VALID_EMPTY" for r in receipts)
    if type(discovery.valid_empty) is not bool or discovery.valid_empty != empty:
        raise S04I05ReceptionError("I05 frontier empty claim contradicts candidate fates")
    # Same native I05 final replay preimage as execute_exact_bounded_discovery.
    digest = semantic_hash({
        "contract": I05_CONTRACT_ID,
        "frontier_ref": discovery.evaluated_frontier_ref.as_dict(),
        "receipt_refs": [r.ref.as_dict() for r in receipts],
        "fact_refs": [r.as_dict() for r in discovery.empirical_fact_refs],
        "valid_empty": empty,
    })
    actual = ExactRef("PRE553_I05_FRONTIER_REPLAY",
                      f"urn:rawlsing:pre553:i05:frontier-replay:sha256:{digest}", digest)
    if actual != expected_replay_ref or actual != discovery.replay_ref:
        raise S04I05ReceptionError("I05 complete frontier replay identity mismatch")


def receive_s04_i05_adaptive_outcome(
    *,
    unit,
    discovery: ExactBoundedDiscoveryResult,
    expected_replay_ref: ExactRef,
    candidate_receipt_ref: ExactRef,
    query_role: str,
    current_guard: Callable[[], Any],
    proposal_units=(),
    parent_handoff=None,
    next_handoff=None,
):
    """Bridge a real sealed I05 frontier into the existing adaptive scheduler.

    This is not a scheduler or an issuer. The caller must obtain the
    expected native replay identity independently and supply already-issued
    units. A selected validation receipt can be VALID_EMPTY while its role
    fact is supported; preserve both states. Child requests must bind the
    actual parent's role receipt AND complete frontier replay identity.
    The existing adaptive scheduler verifies its own rule, generation,
    determinant and frontier bounds; subsequent native execution must still
    validate its separately issued discovery authority.
    """
    from rawlsing_next.pre553_discovery_adaptive import (
        AdaptiveExplorationUnit, AdaptiveUnitOutcome,
    )
    from rawlsing_next.pre553_recursive_handoff import (
        RecursiveBranchHandoff, RECURSIVE_BRANCH_FAMILIES,
    )

    if not callable(current_guard):
        raise S04I05ReceptionError("bound current guard required")

    def check():
        result = current_guard()
        if result is not None and result is not True:
            raise S04I05ReceptionError("source CURRENT denied")

    check()
    if (type(unit) is not AdaptiveExplorationUnit
            or type(discovery) is not ExactBoundedDiscoveryResult
            or type(expected_replay_ref) is not ExactRef
            or expected_replay_ref != discovery.replay_ref
            or discovery.discovery_authority_ref not in unit.determinant_refs):
        raise S04I05ReceptionError("unit/native discovery authority or replay identity mismatch")
    _require_pinned_frontier(discovery, expected_replay_ref)
    observed, role = receive_s04_i05_role(
        discovery=discovery, candidate_receipt_ref=candidate_receipt_ref,
        query_role=query_role,
    )
    receipt = next(r for r in discovery.receipts if r.ref == candidate_receipt_ref)
    releases = tuple(_ref(ref, "release") for ref in receipt.source_release_refs)
    # A resumed recursively issued native operation must actually consume
    # its persisted parent, not merely carry an unconnected hash in the unit.
    ancestral = tuple(_ref(ref, "branch ancestry") for ref in receipt.branch_or_parent_ancestry_refs)
    declared_parents = tuple(ref for ref in unit.determinant_refs
                             if ref.kind == "C11Internal:DiscoveryBranchReplayBinding")
    ancestry_parents = tuple(ref for ref in ancestral
                             if ref.kind == "C11Internal:DiscoveryBranchReplayBinding")
    if declared_parents or ancestry_parents or parent_handoff is not None:
        if (type(parent_handoff) is not RecursiveBranchHandoff
                or parent_handoff.ref not in declared_parents
                or parent_handoff.ref not in ancestral
                or parent_handoff.winning_predicate.ref not in unit.determinant_refs
                or parent_handoff.source_release_refs != releases):
            raise S04I05ReceptionError("recursive unit lost exact issued parent handoff")
    proposals = tuple(proposal_units)
    if proposals and observed.material()["state"] != "SUPPORTED_SAMPLE_DESCRIPTIVE":
        raise S04I05ReceptionError("held role cannot supply positive proposal evidence")
    family = receipt.candidate_identity["family"]
    if next_handoff is not None or (proposals and family in RECURSIVE_BRANCH_FAMILIES):
        if (family not in RECURSIVE_BRANCH_FAMILIES
                or type(next_handoff) is not RecursiveBranchHandoff
                or receipt.typed_state != "DISCOVERED_RESULT_SUPPORTED"
                or next_handoff.receipt_ref != receipt.ref
                or next_handoff.discovery_authority_ref != discovery.discovery_authority_ref
                or next_handoff.evaluated_frontier_ref != discovery.evaluated_frontier_ref
                or next_handoff.source_release_refs != releases
                or next_handoff.branch_replay_binding.candidate_universe_ref_or_typed_absence != discovery.candidate_grammar_ref
                or next_handoff.winning_predicate.ref != _ref(receipt.winning_predicate_ref, "winner")
                or next_handoff.winning_predicate.ref != _ref(role.material()["predicate_ref"], "selected role predicate")):
            raise S04I05ReceptionError("recursive proposal requires native winning handoff and condition role")
    for child in proposals:
        if (type(child) is not AdaptiveExplorationUnit
                or child.parent_unit_ref != unit.unit_ref
                or child.generation != unit.generation + 1
                or expected_replay_ref not in child.determinant_refs
                or role.ref not in child.determinant_refs
                or (next_handoff is not None and (
                    next_handoff.ref not in child.determinant_refs
                    or next_handoff.winning_predicate.ref not in child.determinant_refs))):
            raise S04I05ReceptionError("child proposal must bind exact parent evidence")
    outcome = AdaptiveUnitOutcome(
        unit_ref=unit.unit_ref,
        sealed_result_ref=expected_replay_ref,
        proposal_basis_ref=role.ref,
        # Never report a selected candidate's VALID_EMPTY as emptiness of
        # the complete sealed frontier. The original role receipt retains it.
        unit_result_state="I05_COMPLETE_FRONTIER__SELECTED_" + receipt.typed_state,
        proposal_units=proposals,
    )
    check()
    return observed, role, outcome


__all__ = [
    "CONTRACT", "S04I05ReceptionError", "S04I05RoleKnowledge",
    "receive_s04_i05_role", "receive_s04_i05_adaptive_outcome",
]
