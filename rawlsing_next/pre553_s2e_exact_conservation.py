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
    COVERAGE_CLAIM,
    TERMINAL_COVERAGE_STATES,
    ExactBoundedDiscoveryResult,
)
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact,
    DiscoveryResultReceipt,
    ExactRef,
    Pre553IntegrityError,
    canonical_json,
    exact_ref,
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
            _require(tuple(_ref_key(ref) for ref in unit.release_refs),
                     "S2E_DISCOVERY_EMPTY_RELEASE_SCOPE")
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
                _object(digest, "I05_RECEIPT", receipt)
                totals["i05_receipt"] += 1
                states["DISCOVERY:" + receipt.typed_state] = (
                    states.get("DISCOVERY:" + receipt.typed_state, 0) + 1
                )
            _require(cited_fact_refs == {_ref_key(ref) for ref in output.empirical_fact_refs},
                     "S2E_DISCOVERY_FACT_REF_LOSS")
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
