"""S2-E exact output conservation for the *existing* native I03/I05/Batch owner.

This is a post-execution, read-only conservation court, NOT a query engine, source
issuer, scientific estimator, result archive, or independent receiving decision.
It incrementally fingerprints whole native preimages instead of comparing counts
or storing another complete in-memory output graph. A partial Batch is explicitly
partial; completed receipts never certify omitted outputs.

The caller owns the authoritative current decision and the C11 repository.
This verifier does not open any source, mint any rights, write persisted data,
or infer absence from a missing object.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Mapping

from rawlsing_next._pre553_query_common import QueryExecutionResult, _parse_target_plan
from rawlsing_next.pre553_batch_runner import BatchManifest, UnitExecutionReceipt
from rawlsing_next.pre553_discovery_exact import (
    COVERAGE_CLAIM, I05_CONTRACT_ID, TERMINAL_COVERAGE_STATES,
    ExactBoundedDiscoveryResult,
    _verify_discovery_authority, _catalog_atoms, _catalog_templates,
    _validate_catalog_scope, _compile_frontier, _derived_ref,
    _terminal_fact_class, _support_summary,
    _distribution_differs, _joint_dependence,
    _conditional_reversal, _target_cell_supported,
    ExactBoundedDiscoveryError,
)
from rawlsing_next._pre553_query_common import QUERY_EXECUTION_CONTRACT_ID
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact,
    DiscoveryResultReceipt,
    ExactRef,
    Pre553IntegrityError,
    canonical_json,
    canonicalize,
    exact_ref,
    authority_ref,
    semantic_hash,
)


CONTRACT = "PYAT_S2E_EXACT_NATIVE_OUTPUT_CONSERVATION@1"


class S2EOutputConservationError(Pre553IntegrityError):
    """A native first-consumer output, receipt, or exact preimage was lost."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise S2EOutputConservationError(code)


def _ref_key(value: Any) -> str:
    return exact_ref(value, "S2E exact reference").key


class _BoundedEvidenceHash:
    """Incremental SHA256 with an exact shared proof-transcript byte ceiling."""

    def __init__(self, shared_count: list[int], maximum: int | None):
        self._digest = hashlib.sha256()
        self._shared_count = shared_count
        self._maximum = maximum

    def update(self, data: bytes) -> None:
        candidate = self._shared_count[0] + len(data)
        if self._maximum is not None and candidate > self._maximum:
            raise S2EOutputConservationError("S2E_EXACT_OUTPUT_BYTES_CAP_HOLD")
        self._shared_count[0] = candidate
        self._digest.update(data)

    def hexdigest(self) -> str:
        return self._digest.hexdigest()


def _feed(digest: Any, kind: str, material: Any) -> None:
    """Length-prefix each complete preimage: no concatenation collisions."""
    blob = canonical_json({"kind": kind, "material": material}).encode("utf-8")
    digest.update(len(blob).to_bytes(8, "big"))
    digest.update(blob)


def _object(digest: Any, kind: str, obj: Any) -> None:
    _require(hasattr(obj, "as_dict") and hasattr(obj, "ref"), "S2E_MISSING_OBJECT_PREIMAGE")
    _require(semantic_hash(obj.semantic_projection()) == obj.content_hash,
             "S2E_OBJECT_IDENTITY_DRIFT")
    _require(obj.ref.content_hash == obj.content_hash, "S2E_OBJECT_REF_DRIFT")
    _feed(digest, kind, obj.as_dict())


def _check_fact(fact: EmpiricalFact, *, expected_query: ExactRef | None = None) -> None:
    _require(isinstance(fact, EmpiricalFact), "S2E_WRONG_EMPIRICAL_FACT_TYPE")
    if expected_query is not None:
        _require(_ref_key(fact.empirical_query_spec_ref) == expected_query.key,
                 "S2E_QUERY_FACT_REF_MISMATCH")
    # A fact may legitimately describe only one of several source-indexed
    # universes, but it cannot silently discard every release/universe preimage.
    proven = {_ref_key(ref) for ref in fact.source_empirical_provenance_refs}
    _require(all(_ref_key(ref) in proven for ref in fact.empirical_universe_refs),
             "S2E_FACT_UNIVERSE_PROVENANCE_LOST")
    topology = fact.target_topology
    if not isinstance(topology, Mapping) or "complete_cell_semantic_projection" not in topology:
        # Native typed nonpositive facts have a different, explicitly identified
        # failure preimage. Do not require imaginary risk/cell lists for them.
        _require(fact.typed_state not in {"SUPPORTED", "OBSERVED_ZERO"},
                 "S2E_POSITIVE_WITHOUT_COMPLETE_DOMAIN")
        _require(getattr(fact, "p02_failure_state", None) is not None,
                 "S2E_NONPOSITIVE_WITHOUT_TYPED_REASON")
        return
    cells = topology["complete_cell_semantic_projection"]
    _require(isinstance(cells, (tuple, list)), "S2E_DOMAIN_NOT_ENUMERATED")
    risk = tuple(exact_ref(ref, "risk member") for ref in fact.risk_set_member_refs)
    denominator = tuple(exact_ref(ref, "denominator member") for ref in fact.denominator_member_refs)
    _require(len(set(risk)) == len(risk) and len(set(denominator)) == len(denominator),
             "S2E_DUPLICATE_MEMBER_REF")
    _require(set(denominator).issubset(set(risk)), "S2E_DENOMINATOR_NOT_WITHIN_RISK")
    _require(len(denominator) == fact.raw_denominator_support,
             "S2E_DENOMINATOR_MEMBER_LOSS")
    _require(sum(row["raw_numerator_support"] for row in cells)
             == fact.raw_resolved_target_support,
             "S2E_CELL_SUPPORT_NOT_CONSERVED")
    _require(fact.raw_resolved_target_support == fact.raw_numerator_support,
             "S2E_NUMERATOR_NOT_CONSERVED")
    _require(fact.raw_resolved_target_support <= len(denominator),
             "S2E_RESOLVED_SUPPORT_EXCEEDS_DENOMINATOR")
    seen: set[str] = set()
    for row in cells:
        _require(isinstance(row, Mapping) and "cell" in row and "cell_state" in row,
                 "S2E_DOMAIN_CELL_MISSING")
        identity = semantic_hash(row["cell"])
        _require(identity not in seen, "S2E_DUPLICATE_FULL_DOMAIN_CELL")
        seen.add(identity)
        n = row["raw_numerator_support"]
        _require(type(n) is int and n >= 0, "S2E_INVALID_EXACT_CELL_SUPPORT")
        if n == 0 and denominator and row["cell_state"] != "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET":
            raise S2EOutputConservationError("S2E_TRUE_OBSERVED_ZERO_LOST")
        if n > 0 and row["cell_state"] != "OBSERVED_POSITIVE":
            raise S2EOutputConservationError("S2E_POSITIVE_CELL_MISCLASSIFIED")


def _verify_declared_domain(fact: EmpiricalFact, query: Any, registry: Any) -> None:
    """Compare every executed native cell with the query's complete issued domain.

    The source/authority owner continues to authenticate the query. This checks
    that the fact did not lose zero-valued full-domain cells after execution.
    """
    _require(_ref_key(fact.condition_predicate_ref)
             == _ref_key(query.condition_predicate_ref),
             "S2E_FACT_CONDITION_DIRECTION_MISMATCH")
    plan = _parse_target_plan(query, registry)
    topology = fact.target_topology
    if "complete_cell_semantic_projection" not in topology:
        _require(fact.typed_state not in {"SUPPORTED", "OBSERVED_ZERO"},
                 "S2E_POSITIVE_WITHOUT_DECLARED_DOMAIN")
        return
    _require(topology.get("arity") == plan.arity,
             "S2E_DECLARED_TARGET_ARITY_MISMATCH")
    _require(topology.get("target_domain_identity") == plan.domain_identity
             and getattr(fact, "target_domain_identity", None) == plan.domain_identity,
             "S2E_DECLARED_DOMAIN_IDENTITY_MISMATCH")
    actual = tuple(canonical_json(row["cell"])
                   for row in topology["complete_cell_semantic_projection"])
    declared = tuple(sorted(canonical_json(cell) for cell in plan.full_domain))
    _require(tuple(sorted(actual)) == declared,
             "S2E_INCOMPLETE_OR_FOREIGN_DECLARED_DOMAIN")


def _verify_i05_candidate_receipt(receipt: DiscoveryResultReceipt, output: ExactBoundedDiscoveryResult, unit: Any, *, facts_by_key: Mapping[str, EmpiricalFact]) -> None:
    """Re-derive a native I05 candidate's *inner* hash and replay, not its self-hash.

    The native producer constructs candidate identity in _candidate() and the
    per-candidate replay in execute_exact_bounded_discovery(). We use those
    frozen formulas independently of their supplied hash/ref assertions.
    """
    # The native I05 evaluator emits these exact terminal-fate/type pairs.
    # A self-hashed receipt may not relabel a supported candidate as a typed
    # negative while preserving the rest of the discovery graph.
    native_fate_types = {
        "EVALUATED_SUPPORTED": "DISCOVERED_RESULT_SUPPORTED",
        "EVALUATED_VALID_EMPTY": "VALID_EMPTY",
        "EVALUATED_UNDERPOWERED": "INSUFFICIENT_SUPPORT",
        "EVALUATED_NONCOMPARABLE": "NONCOMPARABLE",
        "EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY": "COVERAGE_LIMITED",
        "EVALUATED_DENIED_BY_EXACT_AUTHORITY": "PRUNED_BY_AUTHORITY",
    }
    _require(native_fate_types.get(receipt.coverage_state) == receipt.typed_state,
             "S2E_I05_CANDIDATE_TERMINAL_FATE_MISMATCH")
    # The native I05 producer is an inert population-science fact consumer.
    # Rehashing an otherwise correct receipt cannot authorize a diagnostic,
    # structural proposition, or actor-state effect, nor silently replace the
    # exact I03 contract underpinning the candidate replay.
    _require(
        all(
            getattr(receipt, field, None) is False
            for field in (
                "diagnostic_score_is_empirical_fact",
                "structural_truth_effect",
                "actor_v3_effect",
            )
        ),
        "S2E_I05_NONPROMOTION_FLAGS_MISMATCH",
    )
    _require(
        getattr(receipt, "exact_query_contract_id", None)
        == QUERY_EXECUTION_CONTRACT_ID,
        "S2E_I05_QUERY_EXECUTION_CONTRACT_MISMATCH",
    )
    ci = receipt.candidate_identity
    _require(isinstance(ci, Mapping), "S2E_I05_CANDIDATE_IDENTITY_MISSING")
    roles = ci.get("query_roles")
    _require(isinstance(roles, (tuple, list)) and bool(roles),
             "S2E_I05_CANDIDATE_ROLE_CLOSURE_MISSING")
    role_material = []
    role_names: set[str] = set()
    for raw in roles:
        _require(isinstance(raw, Mapping) and isinstance(raw.get("role"), str)
                 and bool(raw["role"]), "S2E_I05_CANDIDATE_ROLE_INVALID")
        name = raw["role"]
        _require(name not in role_names, "S2E_I05_DUPLICATE_QUERY_ROLE")
        role_names.add(name)
        role_material.append({
            "role": name,
            "predicate_ref": exact_ref(raw.get("predicate_ref"), "candidate role predicate").as_dict(),
            "query_ref": exact_ref(raw.get("query_ref"), "candidate role query").as_dict(),
        })
    ancestry = tuple(sorted({
        exact_ref(ref, "candidate ancestry") for ref in receipt.branch_or_parent_ancestry_refs
    }, key=lambda ref: ref.key))
    winner = exact_ref(receipt.winning_predicate_ref, "winning predicate")
    mat = {
        "contract": I05_CONTRACT_ID,
        "family": ci.get("family"),
        "rule_id": ci.get("rule_id"),
        "winning_predicate_ref": winner.as_dict(),
        "query_roles": role_material,
        "validation": ci.get("validation"),
        "ancestry_refs": [ref.as_dict() for ref in ancestry],
    }
    candidate_hash = semantic_hash(mat)
    _require(ci.get("candidate_hash") == candidate_hash
             and ci.get("candidate_id") == f"urn:rawlsing:pre553:i05:candidate:sha256:{candidate_hash}",
             "S2E_I05_CANDIDATE_IDENTITY_MISMATCH")

    _require(tuple(sorted(_ref_key(ref) for ref in receipt.validation_fact_refs))
             == tuple(sorted(_ref_key(ref) for ref in receipt.empirical_fact_refs)),
             "S2E_I05_VALIDATION_FACT_CLOSURE_MISMATCH")
    support = receipt.support_uncertainty_state
    role_refs = support.get("query_role_fact_refs") if isinstance(support, Mapping) else None
    _require(isinstance(role_refs, Mapping) and set(role_refs) == role_names,
             "S2E_I05_ROLE_FACT_CLOSURE_MISSING")
    cited: set[str] = set()
    for role in role_material:
        member_refs = role_refs[role["role"]]
        _require(isinstance(member_refs, (list, tuple)) and bool(member_refs),
                 "S2E_I05_ROLE_WITHOUT_FACT")
        for raw in member_refs:
            key = _ref_key(raw)
            _require(key in facts_by_key,
                     "S2E_I05_ROLE_FACT_PREIMAGE_NOT_PRESENT")
            _require(_ref_key(facts_by_key[key].empirical_query_spec_ref)
                     == _ref_key(role["query_ref"]),
                     "S2E_I05_ROLE_FACT_WRONG_QUERY")
            cited.add(key)
    _require(cited == {_ref_key(ref) for ref in receipt.empirical_fact_refs},
             "S2E_I05_ROLE_FACT_CLOSURE_MISMATCH")

    exact_fact_refs = tuple(sorted({
        exact_ref(ref, "candidate empirical fact") for ref in receipt.empirical_fact_refs
    }, key=lambda ref: ref.key))
    replay_material = {
        "contract": I05_CONTRACT_ID,
        "authority_ref": output.discovery_authority_ref.as_dict(),
        "frontier_ref": output.evaluated_frontier_ref.as_dict(),
        "candidate_id": ci["candidate_id"],
        "candidate_hash": ci["candidate_hash"],
        "coverage_state": receipt.coverage_state,
        "fact_refs": [ref.as_dict() for ref in exact_fact_refs],
        "release_refs": [ref.as_dict() for ref in unit.release_refs],
        "query_execution_contract": QUERY_EXECUTION_CONTRACT_ID,
    }
    expected = _derived_ref("PRE553_I05_DISCOVERY_REPLAY", "candidate-replay", replay_material)
    _require(_ref_key(receipt.replay_ref) == expected.key
             and _ref_key(receipt.producer_replay_locator_or_reference_root) == expected.key,
             "S2E_I05_CANDIDATE_REPLAY_MISMATCH")


def _verify_i05_scientific_fate_against_facts(
    receipt: DiscoveryResultReceipt,
    output: ExactBoundedDiscoveryResult,
    unit: Any,
    authority: Any,
    *, facts_by_key: Mapping[str, EmpiricalFact],
) -> None:
    """Falsify an invented terminal discovery fate using the retained native facts.

    Native I05's own validation primitives are invoked on exact I03
    QueryExecutionResult views reconstructed from the already-executed fact
    preimages. This does NOT re-open a source, redo an I03 scan or invent an
    independent scientific estimator. It detects a self-consistent, fully
    rehashed false VALID_EMPTY/SUPPORTED claim that A2 identity/replay checks
    cannot distinguish because candidate identity is fixed *before* evaluation.

    The competent catalogue is required by the caller; without it the census
    explicitly reports declared_frontier_verified=False rather than claiming
    this scientific-result check was performed.
    """
    role_refs = receipt.support_uncertainty_state["query_role_fact_refs"]
    results: dict[str, QueryExecutionResult] = {}
    canonical_role_refs: dict[str, list[dict[str, str]]] = {}
    try:
        for role in receipt.candidate_identity["query_roles"]:
            name = role["role"]
            exact_refs = tuple(exact_ref(ref, "role fact") for ref in role_refs[name])
            facts = tuple(sorted(
                (facts_by_key[ref.key] for ref in exact_refs),
                key=lambda fact: fact.ref.key,
            ))
            _require(bool(facts) and len({f.ref.key for f in facts}) == len(exact_refs),
                     "S2E_I05_CANDIDATE_SCIENTIFIC_FATE_MISMATCH")
            _require(len({f.source_scope_mode for f in facts}) == 1,
                     "S2E_I05_CANDIDATE_SCIENTIFIC_FATE_MISMATCH")
            results[name] = QueryExecutionResult(
                query_ref=exact_ref(role["query_ref"], "role query"),
                facts=facts,
                source_scope_mode=facts[0].source_scope_mode,
                release_refs=unit.release_refs,
            )
            canonical_role_refs[name] = [f.ref.as_dict() for f in facts]

        candidate_facts = tuple(sorted(
            (facts_by_key[_ref_key(ref)] for ref in receipt.empirical_fact_refs),
            key=lambda fact: fact.ref.key,
        ))
        # Native execute_exact_bounded_discovery emits the entire exact
        # dependency and authority closure, not merely a self-hashed subset.
        # B2's scientific recomputation alone would accept a receipt with
        # its scientific inputs/authority provenance silently removed.
        native_dependencies = {
            authority.ref.key,
            exact_ref(authority.candidate_grammar_ref, "issued candidate grammar").key,
            output.evaluated_frontier_ref.key,
            _ref_key(receipt.winning_predicate_ref),
            *(f.ref.key for f in candidate_facts),
        }
        _require(
            {_ref_key(ref) for ref in receipt.dependency_refs} == native_dependencies,
            "S2E_I05_DEPENDENCY_CLOSURE_MISMATCH",
        )
        native_snapshots = {
            authority_ref(ref, "issuer authority snapshot").key
            for ref in (
                *authority.authority_snapshot_refs,
                *(snapshot for fact in candidate_facts
                  for snapshot in fact.authority_snapshot_refs),
            )
        }
        _require(
            {authority_ref(ref, "candidate authority snapshot").key
             for ref in receipt.authority_snapshot_refs} == native_snapshots,
            "S2E_I05_AUTHORITY_SNAPSHOT_CLOSURE_MISMATCH",
        )
        expected_support = dict(_support_summary(candidate_facts))
        expected_support["query_role_fact_refs"] = canonicalize({
            name: canonical_role_refs[name] for name in sorted(canonical_role_refs)
        })
        _require(canonical_json(receipt.support_uncertainty_state)
                 == canonical_json(expected_support),
                 "S2E_I05_CANDIDATE_SUPPORT_PREIMAGE_MISMATCH")

        terminal = _terminal_fact_class(candidate_facts)
        if terminal == "NONCOMPARABLE":
            expected = ("EVALUATED_NONCOMPARABLE", "NONCOMPARABLE")
        elif terminal == "UNAVAILABLE":
            expected = ("EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY", "COVERAGE_LIMITED")
        elif terminal == "VALID_EMPTY":
            expected = ("EVALUATED_VALID_EMPTY", "VALID_EMPTY")
        else:
            limit = authority.support_rules.get("minimum_raw_denominator", 1)
            _require(type(limit) is int and limit >= 0,
                     "S2E_I05_CANDIDATE_SUPPORT_RULE_INVALID")
            primary = tuple(
                f for f in candidate_facts
                if f.typed_state in {"SUPPORTED", "LOW_SUPPORT", "OBSERVED_ZERO"}
            )
            if primary and any(f.raw_denominator_support < limit for f in primary):
                expected = ("EVALUATED_UNDERPOWERED", "INSUFFICIENT_SUPPORT")
            else:
                validation = receipt.candidate_identity["validation"]
                kind = validation["kind"]
                if kind == "DISTRIBUTION_DIFFERS_FROM_BASELINE":
                    supported = _distribution_differs(results["CONDITION"], results["BASELINE"])
                elif kind == "JOINT_NOT_PRODUCT_OF_MARGINALS":
                    supported = _joint_dependence(results)
                elif kind == "CONDITIONAL_REVERSAL":
                    supported = _conditional_reversal(results, validation)
                elif kind == "TARGET_CELL_SUPPORTED":
                    supported = _target_cell_supported(results["BASE"], validation.get("target_cell"))
                else:
                    raise S2EOutputConservationError("S2E_I05_UNKNOWN_NATIVE_VALIDATION")
                expected = (
                    ("EVALUATED_SUPPORTED", "DISCOVERED_RESULT_SUPPORTED")
                    if supported else ("EVALUATED_VALID_EMPTY", "VALID_EMPTY")
                )
        _require((receipt.coverage_state, receipt.typed_state) == expected,
                 "S2E_I05_CANDIDATE_SCIENTIFIC_FATE_MISMATCH")
    except S2EOutputConservationError:
        raise
    except (KeyError, TypeError, ValueError, ExactBoundedDiscoveryError) as exc:
        raise S2EOutputConservationError(
            "S2E_I05_CANDIDATE_SCIENTIFIC_FATE_MISMATCH"
        ) from exc


def _verify_i05_declared_frontier(output: ExactBoundedDiscoveryResult, unit: Any, catalog: Any, registry: Any) -> None:
    """Regenerate authority-declared candidate roster WITHOUT re-running any I03.

    Native I05's own pre-search grammar compiler is the governing source;
    this verifies a complete roster, not just equal claimed receipt counters.
    Does not grant issuer currentness or original respondent/source competence.
    """
    authority = catalog.resolve_discovery_authority_exact(unit.job_ref)
    definition = _verify_discovery_authority(authority, registry)
    atoms = _catalog_atoms(definition, catalog.predicates)
    templates = _catalog_templates(definition, catalog.queries)
    _validate_catalog_scope(authority, atoms, templates)
    candidates = _compile_frontier(definition, atoms, templates)
    grammar_ref = exact_ref(authority.candidate_grammar_ref, "candidate grammar")
    material = {
        "contract": I05_CONTRACT_ID,
        "discovery_authority_ref": authority.ref.as_dict(),
        "candidate_grammar_ref": grammar_ref.as_dict(),
        "query_execution_contract": QUERY_EXECUTION_CONTRACT_ID,
        "candidate_identities": [
            {"candidate_id": c.candidate_id, "candidate_hash": c.candidate_hash}
            for c in candidates
        ],
        "coverage_claim": COVERAGE_CLAIM,
    }
    true_frontier = _derived_ref("PRE553_I05_EVALUATED_FRONTIER", "frontier", material)
    _require(output.evaluated_frontier_ref == true_frontier
             and output.candidate_grammar_ref == grammar_ref
             and output.candidate_count == len(candidates),
             "S2E_I05_DECLARED_FRONTIER_MISMATCH")
    by_id = {
        c.candidate_id: c for c in candidates
    }
    _require(len(by_id) == len(candidates), "S2E_I05_DECLARED_CANDIDATE_DUPLICATION")
    # A correct candidate roster does not excuse an invented or omitted
    # executed predicate/query object. I05 produces exactly the role objects
    # of the compiler's complete pre-search candidate frontier.
    declared_predicates = {
        role.predicate.ref.key
        for candidate in candidates for role in candidate.query_roles
    }
    declared_queries = {
        role.query.ref.key
        for candidate in candidates for role in candidate.query_roles
    }
    _require(
        {predicate.ref.key for predicate in output.executed_predicates}
            == declared_predicates
        and {query.ref.key for query in output.executed_queries}
            == declared_queries,
        "S2E_I05_EXECUTED_OBJECT_CLOSURE_MISMATCH",
    )
    actual_ids = {receipt.candidate_identity["candidate_id"] for receipt in output.receipts}
    _require(actual_ids == set(by_id), "S2E_I05_DECLARED_FRONTIER_MISMATCH")
    for receipt in output.receipts:
        c = by_id[receipt.candidate_identity["candidate_id"]]
        _require(
            receipt.candidate_identity["candidate_hash"] == c.candidate_hash
            and _ref_key(receipt.winning_predicate_ref) == c.winning_predicate.ref.key
            and {_ref_key(ref) for ref in receipt.branch_or_parent_ancestry_refs}
                == {ref.key for ref in c.ancestry_refs}
            and tuple(
                (row["role"], _ref_key(row["predicate_ref"]), _ref_key(row["query_ref"]))
                for row in receipt.candidate_identity["query_roles"]
            ) == tuple(
                (role.role, role.predicate.ref.key, role.query.ref.key)
                for role in c.query_roles
            ),
            "S2E_I05_DECLARED_CANDIDATE_ROLE_OR_ANCESTRY_MISMATCH",
        )


@dataclass(frozen=True)
class S2EOutputCensus:
    contract: str
    manifest_hash: str
    complete: bool
    unit_count: int
    completed_count: int
    unresolved_unit_count: int
    i03_fact_count: int
    i05_fact_count: int
    i05_receipt_count: int
    typed_state_counts: Mapping[str, int]
    declared_domain_verified: bool
    declared_frontier_verified: bool
    canonical_proof_transcript_bytes: int
    per_unit_full_preimage_sha256: Mapping[str, str]
    full_output_sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "contract": self.contract,
            "manifest_hash": self.manifest_hash,
            "complete": self.complete,
            "unit_count": self.unit_count,
            "completed_count": self.completed_count,
            "unresolved_unit_count": self.unresolved_unit_count,
            "i03_fact_count": self.i03_fact_count,
            "i05_fact_count": self.i05_fact_count,
            "i05_receipt_count": self.i05_receipt_count,
            "typed_state_counts": dict(sorted(self.typed_state_counts.items())),
            "declared_domain_verified": self.declared_domain_verified,
            "declared_frontier_verified": self.declared_frontier_verified,
            "canonical_proof_transcript_bytes": self.canonical_proof_transcript_bytes,
            "per_unit_full_preimage_sha256": dict(sorted(self.per_unit_full_preimage_sha256.items())),
            "full_output_sha256": self.full_output_sha256,
        }


def census_native_batch(
    manifest: BatchManifest,
    receipts: tuple[UnitExecutionReceipt, ...],
    outputs_by_unit: Mapping[str, Any],
    *,
    require_complete: bool = False,
    runtime_catalog: Any | None = None,
    max_canonical_output_bytes: int | None = None,
) -> S2EOutputCensus:
    """Audit *all* Batch first-reader outputs at native object/preimage scope.

    No graph reconstruction or new authority. This runs on the existing Batch
    unit manifest, executed I03 facts and I05 discovery result envelopes. Every
    candidate fate and negative fact participates in a full-preimage digest.
    """
    _require(isinstance(manifest, BatchManifest), "S2E_INVALID_BATCH_MANIFEST")
    _require(isinstance(outputs_by_unit, Mapping), "S2E_OUTPUT_MAP_REQUIRED")
    _require(
        max_canonical_output_bytes is None
        or (type(max_canonical_output_bytes) is int and max_canonical_output_bytes > 0),
        "S2E_OUTPUT_BYTES_CAP_INVALID",
    )
    if runtime_catalog is not None:
        from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
        _require(isinstance(runtime_catalog, RuntimeObjectCatalog),
                 "S2E_RUNTIME_CATALOG_REQUIRED")
        registry = runtime_catalog.authority_registry
    else:
        registry = None
    by_unit: dict[str, list[UnitExecutionReceipt]] = {
        unit.unit_ref.key: [] for unit in manifest.units
    }
    for receipt in receipts:
        _require(isinstance(receipt, UnitExecutionReceipt), "S2E_INVALID_BATCH_RECEIPT")
        _require(receipt.manifest_hash == manifest.manifest_hash,
                 "S2E_WRONG_MANIFEST_RECEIPT")
        _require(receipt.unit_ref.key in by_unit, "S2E_FOREIGN_BATCH_RECEIPT")
        by_unit[receipt.unit_ref.key].append(receipt)
    _require(len(by_unit) == len(manifest.units), "S2E_DUPLICATE_BATCH_UNIT")
    _require(set(outputs_by_unit) <= {unit.unit_hash for unit in manifest.units},
             "S2E_FOREIGN_OUTPUT_UNIT")
    totals = {"i03": 0, "i05_fact": 0, "i05_receipt": 0}
    states: dict[str, int] = {}
    per_unit: dict[str, str] = {}
    completed = 0
    transcript_bytes = [0]
    summary = _BoundedEvidenceHash(transcript_bytes, max_canonical_output_bytes)

    for unit in manifest.units:
        history = sorted(by_unit[unit.unit_ref.key], key=lambda r: r.attempt_index)
        _require([r.attempt_index for r in history] == list(range(1, len(history) + 1)),
                 "S2E_RECEIPT_HISTORY_NOT_CONTIGUOUS")
        _require(not any(r.state == "COMPLETED" for r in history[:-1]),
                 "S2E_RETRY_AFTER_COMPLETED")
        final = history[-1] if history else None
        output = outputs_by_unit.get(unit.unit_hash)
        if final is None or final.state != "COMPLETED":
            _require(output is None, "S2E_NONCOMPLETED_UNIT_HAS_POSITIVE_OUTPUT")
            _feed(summary, "UNRESOLVED_UNIT",
                  {"unit": unit.semantic_projection(), "receipts": [r.projection() for r in history],
                   "state": "NOT_RUN" if final is None else final.state})
            continue
        completed += 1
        _require(output is not None, "S2E_COMPLETED_WITHOUT_ACTUAL_OUTPUT")
        _require(final.execution_performed, "S2E_NONEXECUTED_COMPLETED_UNIT")
        digest = _BoundedEvidenceHash(transcript_bytes, max_canonical_output_bytes)
        _feed(digest, "UNIT", unit.semantic_projection())
        _feed(digest, "RECEIPTS", [r.projection() for r in history])

        if unit.job_kind == "QUERY":
            _require(isinstance(output, QueryExecutionResult), "S2E_QUERY_OUTPUT_TYPE")
            _require(output.query_ref == unit.job_ref, "S2E_QUERY_FIRST_READER_MISMATCH")
            _require(bool(output.facts), "S2E_QUERY_WITHOUT_NEGATIVE_OR_POSITIVE_FACT")
            _require(tuple(_ref_key(ref) for ref in output.release_refs)
                     == tuple(ref.key for ref in unit.release_refs),
                     "S2E_QUERY_RELEASE_SCOPE_MISMATCH")
            query = (runtime_catalog.resolve_query_exact(unit.job_ref)
                     if runtime_catalog is not None else None)
            for fact in output.facts:
                _check_fact(fact, expected_query=output.query_ref)
                if query is not None:
                    _verify_declared_domain(fact, query, registry)
                _object(digest, "I03_FACT", fact)
                totals["i03"] += 1
                states["FACT:" + fact.typed_state] = states.get("FACT:" + fact.typed_state, 0) + 1
            _feed(digest, "I03_ENVELOPE", {
                "query_ref": output.query_ref.as_dict(),
                "release_refs": [ref.as_dict() for ref in output.release_refs],
                "source_scope_mode": output.source_scope_mode,
            })
            expected_refs = tuple(f.ref for f in output.facts)
        elif unit.job_kind == "DISCOVERY":
            _require(isinstance(output, ExactBoundedDiscoveryResult), "S2E_DISCOVERY_OUTPUT_TYPE")
            _require(output.discovery_authority_ref == unit.job_ref,
                     "S2E_DISCOVERY_FIRST_READER_MISMATCH")
            _require(output.coverage_claim == COVERAGE_CLAIM,
                     "S2E_DISCOVERY_COVERAGE_FALSE")
            _require(output.candidate_count == output.covered_candidate_count
                     == len(output.receipts), "S2E_MISSING_DISCOVERY_CANDIDATE_FATE")
            # The native I05 executor defines valid_empty from *all terminal
            # candidate fates*. A self-hashed result can otherwise assert
            # absence even when it carries a positive discovery receipt.
            expected_valid_empty = not output.receipts or all(
                receipt.typed_state == "VALID_EMPTY" for receipt in output.receipts
            )
            _require(type(output.valid_empty) is bool
                     and output.valid_empty == expected_valid_empty,
                     "S2E_I05_VALID_EMPTY_CLAIM_MISMATCH")
            _require(tuple(_ref_key(ref) for ref in unit.release_refs),
                     "S2E_DISCOVERY_EMPTY_RELEASE_SCOPE")
            # One O(F) index for all C candidate receipts and fate replays,
            # rather than rebuilding the complete fact map O(C*F).
            facts_by_key = {fact.ref.key: fact for fact in output.empirical_facts}
            seen: set[tuple[str, str]] = set()
            cited_fact_refs: set[str] = set()
            for receipt in output.receipts:
                _require(isinstance(receipt, DiscoveryResultReceipt),
                         "S2E_DISCOVERY_RECEIPT_TYPE")
                _require(receipt.coverage_state in TERMINAL_COVERAGE_STATES,
                         "S2E_UNVISITED_DISCOVERY_BRANCH")
                _require(_ref_key(receipt.discovery_authority_ref) == output.discovery_authority_ref.key
                         and _ref_key(receipt.evaluated_frontier_ref) == output.evaluated_frontier_ref.key,
                         "S2E_DISCOVERY_RECEIPT_WRONG_SCOPE")
                _require(
                    tuple(sorted(_ref_key(ref) for ref in receipt.source_release_refs))
                    == tuple(sorted(ref.key for ref in unit.release_refs)),
                    "S2E_DISCOVERY_RECEIPT_RELEASE_SCOPE_MISMATCH",
                )
                ci = receipt.candidate_identity
                _require(isinstance(ci, Mapping), "S2E_DISCOVERY_CANDIDATE_IDENTITY_MISSING")
                key = (str(ci.get("candidate_id")), str(ci.get("candidate_hash")))
                _require(key not in seen, "S2E_DUPLICATE_DISCOVERY_CANDIDATE_FATE")
                seen.add(key)
                cited_fact_refs.update(_ref_key(ref) for ref in receipt.empirical_fact_refs)
                _verify_i05_candidate_receipt(receipt, output, unit, facts_by_key=facts_by_key)
                _object(digest, "I05_RECEIPT", receipt)
                totals["i05_receipt"] += 1
                states["DISCOVERY:" + receipt.typed_state] = (
                    states.get("DISCOVERY:" + receipt.typed_state, 0) + 1
                )
            _require(cited_fact_refs == {_ref_key(ref) for ref in output.empirical_fact_refs},
                     "S2E_DISCOVERY_FACT_REF_LOSS")
            if runtime_catalog is not None:
                _verify_i05_declared_frontier(output, unit, runtime_catalog, registry)
                issued_authority = runtime_catalog.resolve_discovery_authority_exact(unit.job_ref)
                for candidate_receipt in output.receipts:
                    _verify_i05_scientific_fate_against_facts(
                        candidate_receipt, output, unit, issued_authority,
                        facts_by_key=facts_by_key,
                    )
            # Native execute_exact_bounded_discovery derives the frontier
            # replay from this exact ordered closure. Merely digesting a
            # supplied replay_ref would certify even a replaced/false replay.
            replay_material = {
                "contract": output.contract_id,
                "frontier_ref": output.evaluated_frontier_ref.as_dict(),
                "receipt_refs": [r.ref.as_dict() for r in output.receipts],
                "fact_refs": [ref.as_dict() for ref in output.empirical_fact_refs],
                "valid_empty": expected_valid_empty,
            }
            replay_hash = semantic_hash(replay_material)
            expected_replay = ExactRef(
                "PRE553_I05_FRONTIER_REPLAY",
                f"urn:rawlsing:pre553:i05:frontier-replay:sha256:{replay_hash}",
                replay_hash,
            )
            _require(output.replay_ref == expected_replay,
                     "S2E_I05_FRONTIER_REPLAY_MISMATCH")
            executed_query_by_ref = {
                query.ref.key: query for query in output.executed_queries
            }
            for fact in output.empirical_facts:
                _check_fact(fact)
                if registry is not None:
                    parent_query = executed_query_by_ref.get(
                        _ref_key(fact.empirical_query_spec_ref)
                    )
                    _require(parent_query is not None,
                             "S2E_DISCOVERY_EXECUTED_QUERY_CLOSURE_LOST")
                    _verify_declared_domain(fact, parent_query, registry)
                _object(digest, "I05_FACT", fact)
                totals["i05_fact"] += 1
                states["FACT:" + fact.typed_state] = states.get("FACT:" + fact.typed_state, 0) + 1
            for predicate in output.executed_predicates:
                _object(digest, "I05_PREDICATE", predicate)
            for query in output.executed_queries:
                _object(digest, "I05_QUERY", query)
            _feed(digest, "I05_ENVELOPE", {
                "contract_id": output.contract_id,
                "authority": output.discovery_authority_ref.as_dict(),
                "grammar": output.candidate_grammar_ref.as_dict(),
                "frontier": output.evaluated_frontier_ref.as_dict(),
                "coverage_claim": output.coverage_claim,
                "candidate_count": output.candidate_count,
                "covered_count": output.covered_candidate_count,
                "empirical_fact_refs": [ref.as_dict() for ref in output.empirical_fact_refs],
                "valid_empty": output.valid_empty,
                "replay": output.replay_ref.as_dict(),
            })
            expected_refs = tuple(r.ref for r in output.receipts)
        else:
            raise S2EOutputConservationError("S2E_UNKNOWN_JOB_KIND")
        _require(final.result_refs == expected_refs, "S2E_BATCH_RECEIPT_RESULT_GRAPH_LOSS")
        per_unit[unit.unit_hash] = digest.hexdigest()
        _feed(summary, "COMPLETED_UNIT", {
            "unit": unit.unit_ref.as_dict(), "digest": digest.hexdigest()
        })

    _require(completed == len(outputs_by_unit), "S2E_OUTPUT_CARDINALITY_LOSS")
    complete = completed == len(manifest.units)
    if require_complete:
        _require(complete, "S2E_FULL_MANIFEST_NOT_EXECUTED")
    return S2EOutputCensus(
        contract=CONTRACT,
        manifest_hash=manifest.manifest_hash,
        complete=complete,
        unit_count=len(manifest.units),
        completed_count=completed,
        unresolved_unit_count=len(manifest.units) - completed,
        i03_fact_count=totals["i03"],
        i05_fact_count=totals["i05_fact"],
        i05_receipt_count=totals["i05_receipt"],
        typed_state_counts=dict(sorted(states.items())),
        declared_domain_verified=runtime_catalog is not None,
        declared_frontier_verified=runtime_catalog is not None,
        canonical_proof_transcript_bytes=transcript_bytes[0],
        per_unit_full_preimage_sha256=dict(sorted(per_unit.items())),
        full_output_sha256=summary.hexdigest(),
    )


def require_same_native_output_graph(
    first: S2EOutputCensus, second: S2EOutputCensus,
) -> None:
    """Full native result preimage parity, not row or unit-count equivalence."""
    _require(isinstance(first, S2EOutputCensus) and isinstance(second, S2EOutputCensus),
             "S2E_COMPARATOR_REQUIRES_RECOMPUTED_CENSUSES")
    _require(first.complete and second.complete, "S2E_PARITY_REQUIRES_FULL_MANIFEST")
    _require(first.as_dict() == second.as_dict(), "S2E_SHARED_VS_INDEPENDENT_OUTPUT_DIFF")
