"""S1-C: independently censused SOURCEFREE operation/fate transport to R03.

This is *not* a second scientific enumerator, issuer, lowering engine, source
reader, or original35 authority. The two frozen inputs are supplied separately:
(1) a source/administration-qualified candidate census and (2) its scientific
eligibility/fate census. Neither is reconstructed from the compiler output.
Only their exact intersection may be sent to the existing ScientificFrontier,
compile_governed_frontier and execute_governed_frontier first consumer.

Native/source rights remain external. This adapter deliberately accepts only
TEST_ONLY_SOURCEFREE evidence and must not be generalized by changing a label.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Callable, Mapping

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_universal_workload import (
    compile_governed_frontier, execute_governed_frontier,
)
from rawlsing_next.universal_grammar.types import (
    ELIGIBILITY_STATES, ScientificFrontier, SourceInventory, GrammarPolicy,
)

SCOPE = "TEST_ONLY_SOURCEFREE"
SCHEMA = "PYAT_R3_S1C_FROZEN_CENSUS@1.0.0"


class CensusRefusal(ValueError):
    """A frozen input, compiler or actual first consumer failed a no-drop join."""

    def __init__(self, code: str, detail: Any = None):
        super().__init__(code if detail is None else f"{code}: {detail}")
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class SourceQualifiedCandidate:
    """Externally supplied candidate; these fields are NOT scientific grants."""

    operation_id: str
    operation_hash: str
    source_id: str
    dataset_id: str | None
    wave: str
    edition: str
    source_sha256: str
    instrument_ref: str | None
    universe_scope: str
    occurrence_ids: tuple[str, ...]
    meaning_ref: str
    source_authority_ref: str
    source_decision_ref: str
    source_grade: str = SCOPE

    def material(self) -> Mapping[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class ScientificFate:
    """Separate supplied U_item/U_unit/U_app/E_pre decision, including negatives."""

    operation_id: str
    operation_hash: str
    disposition: str
    eligibility_decision_ref: str
    u_item_ref: str
    u_unit_ref: str
    u_app_ref: str
    e_pre_ref_or_absence: str
    reason: str
    science_grade: str = SCOPE

    def material(self) -> Mapping[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class FrozenInputCensus:
    """The caller freezes both complete declared inputs BEFORE compiling.

    No method here derives either census from the ScientificFrontier. That
    independence is a caller/issuer obligation; sourcefree tests explicitly
    simulate the two independently supplied lists, then attack an omission.
    """

    scope_id: str
    source_candidates: tuple[SourceQualifiedCandidate, ...]
    scientific_fates: tuple[ScientificFate, ...]
    source_census_ref: str
    science_census_ref: str
    deferred_scope_records: tuple[Mapping[str, Any], ...] = ()
    grade: str = SCOPE

    def material(self) -> Mapping[str, Any]:
        return {
            "schema": SCHEMA, "scope_id": self.scope_id, "grade": self.grade,
            "source_candidates": [x.material() for x in self.source_candidates],
            "scientific_fates": [x.material() for x in self.scientific_fates],
            "source_census_ref": self.source_census_ref,
            "science_census_ref": self.science_census_ref,
            "deferred_scope_records": list(self.deferred_scope_records),
        }

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.material())


def _row_operation_id(row: Any) -> str:
    """ScientificOperation uses op_id; source/fate manifests use operation_id."""
    return row.op_id if hasattr(row, "op_id") else row.operation_id


def _unique(rows: tuple[Any, ...], name: str) -> dict[str, Any]:
    ids = tuple(_row_operation_id(row) for row in rows)
    duplicates = sorted(op for op, count in Counter(ids).items() if count != 1)
    if duplicates:
        raise CensusRefusal("DUPLICATE_" + name, duplicates)
    return {_row_operation_id(row): row for row in rows}


def _same_ids(expected: set[str], actual: set[str], phase: str) -> None:
    if expected != actual:
        raise CensusRefusal(phase + "_ANTI_JOIN", {
            "missing": sorted(expected - actual),
            "unexpected": sorted(actual - expected),
        })


def _nonempty(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CensusRefusal("MISSING_PROVENANCE_" + label)


def verify_frozen_inputs(
    census: FrozenInputCensus, *, inventory: SourceInventory,
    policy: GrammarPolicy, frontier: ScientificFrontier,
) -> Mapping[str, Any]:
    """Join the two source-independent declared sets to the actual input.

    A frozen source candidate absent from the scientific frontier, a scientific
    decision absent from the source census, a count-preserving substitution,
    conflicting eligibility, or mismatched provenance is a hard error before
    any source factory is called.
    """
    if not isinstance(census, FrozenInputCensus) or census.grade != SCOPE:
        raise CensusRefusal("SOURCEFREE_FROZEN_CENSUS_REQUIRED")
    if not isinstance(inventory, SourceInventory) or not isinstance(policy, GrammarPolicy):
        raise CensusRefusal("TYPED_INVENTORY_AND_POLICY_REQUIRED")
    if not isinstance(frontier, ScientificFrontier):
        raise CensusRefusal("TYPED_SCIENTIFIC_FRONTIER_REQUIRED")
    if frontier.original_science_grade != "SOURCEFREE_PROPOSAL_NOT_ORIGINAL":
        raise CensusRefusal("ORIGINAL_SCIENCE_NOT_AUTHORIZED")
    for label, value in (
        ("scope_id", census.scope_id),
        ("source_census_ref", census.source_census_ref),
        ("science_census_ref", census.science_census_ref),
    ):
        _nonempty(value, label)
    if not census.source_candidates or not census.scientific_fates:
        raise CensusRefusal("EMPTY_DECLARED_CENSUS_NOT_ACCEPTED")
    if census.source_census_ref != semantic_hash(
        [row.material() for row in census.source_candidates]
    ):
        raise CensusRefusal("SOURCE_CENSUS_HASH_DRIFT")
    if census.science_census_ref != semantic_hash(
        [row.material() for row in census.scientific_fates]
    ):
        raise CensusRefusal("SCIENCE_CENSUS_HASH_DRIFT")
    if semantic_hash(list(census.deferred_scope_records)) != semantic_hash(
        list(frontier.deferred)
    ):
        raise CensusRefusal("DEFERRED_SCOPE_RECORDS_LOST_OR_FABRICATED")
    sources = _unique(census.source_candidates, "SOURCE_CANDIDATE")
    scientific = _unique(census.scientific_fates, "SCIENTIFIC_FATE")
    _same_ids(set(sources), set(scientific), "SOURCE_VS_SCIENCE")
    operations = _unique(tuple(frontier.operations), "FRONTIER_OPERATION")
    _same_ids(set(sources), set(operations), "FROZEN_VS_FRONTIER")

    if frontier.inventory_hash != inventory.content_hash or frontier.inventory_id != inventory.inventory_id:
        raise CensusRefusal("INVENTORY_CUSTODY_MISMATCH")
    if frontier.policy_hash != policy.content_hash or frontier.policy_id != policy.policy_id:
        raise CensusRefusal("POLICY_CUSTODY_MISMATCH")
    frozen_source = {
        "source_id": inventory.source_id, "wave": inventory.wave,
        "edition": inventory.edition, "source_sha256": inventory.source_sha256,
        "scope": inventory.scope, "current_selection": inventory.current_selection,
    }
    if dict(frontier.source_identity) != frozen_source:
        raise CensusRefusal("SOURCE_IDENTITY_MISMATCH")
    inventory_keys = set(inventory.by_key())
    counts: Counter[str] = Counter()
    for op_id, op in operations.items():
        source = sources[op_id]
        fate = scientific[op_id]
        if source.source_grade != SCOPE or fate.science_grade != SCOPE:
            raise CensusRefusal("NON_SOURCEFREE_AUTHORITY_UNISSUED", op_id)
        if op.canonical_hash != source.operation_hash or op.canonical_hash != fate.operation_hash:
            raise CensusRefusal("OPERATION_IDENTITY_DRIFT", op_id)
        expected_source = (
            op.source_id, op.dataset_id, op.wave, op.edition, op.source_sha256,
            op.instrument_ref, op.scope,
        )
        supplied_source = (
            source.source_id, source.dataset_id, source.wave, source.edition,
            source.source_sha256, source.instrument_ref, source.universe_scope,
        )
        if supplied_source != expected_source or (
            op.source_id != inventory.source_id or op.wave != inventory.wave or
            op.edition != inventory.edition or op.source_sha256 != inventory.source_sha256 or
            op.instrument_ref != inventory.instrument_ref or op.scope != inventory.scope or
            op.dataset_id != inventory.dataset_id
        ):
            raise CensusRefusal("SOURCE_EDITION_UNIVERSE_DRIFT", op_id)
        keys = tuple(key for key in op.targets) + tuple(key for key, _ in op.conditions)
        if any(key not in inventory_keys for key in keys):
            raise CensusRefusal("OCCURRENCE_NOT_IN_INVENTORY", op_id)
        if source.occurrence_ids != tuple(key.key for key in keys):
            raise CensusRefusal("OCCURRENCE_IDENTITY_DRIFT", op_id)
        if source.source_authority_ref not in inventory.authority_refs:
            raise CensusRefusal("SOURCE_AUTHORITY_NOT_IN_FROZEN_INVENTORY", op_id)
        for label, value in (
            ("meaning_ref", source.meaning_ref),
            ("source_authority_ref", source.source_authority_ref),
            ("source_decision_ref", source.source_decision_ref),
            ("eligibility_decision_ref", fate.eligibility_decision_ref),
            ("u_item_ref", fate.u_item_ref),
            ("u_unit_ref", fate.u_unit_ref),
            ("u_app_ref", fate.u_app_ref),
            ("e_pre_ref_or_absence", fate.e_pre_ref_or_absence),
            ("reason", fate.reason),
        ):
            _nonempty(value, label)
        expected_science_roots = (
            frontier.u_item_root or "ABSENT:TEST_ONLY_U_ITEM",
            frontier.u_unit_root or "ABSENT:TEST_ONLY_U_UNIT",
            frontier.u_app_root or "ABSENT:TEST_ONLY_U_APP",
            frontier.e_pre_root or "ABSENT:NO_ORIGINAL_EPRE",
        )
        supplied_science_roots = (
            fate.u_item_ref, fate.u_unit_ref, fate.u_app_ref,
            fate.e_pre_ref_or_absence,
        )
        if supplied_science_roots != expected_science_roots:
            raise CensusRefusal("SCIENTIFIC_U_EPRE_ROOT_DRIFT", op_id)
        if fate.disposition not in ELIGIBILITY_STATES:
            raise CensusRefusal("INVALID_SCIENTIFIC_FATE", op_id)
        if fate.disposition != op.disposition:
            raise CensusRefusal("ELIGIBILITY_DRIFT", op_id)
        counts[op.disposition] += 1
    if dict(counts) != {k: v for k, v in frontier.disposition_counts.items() if v}:
        raise CensusRefusal("FRONTIER_DISPOSITION_COUNT_DRIFT", dict(counts))
    if len(set(frontier.pending_operation_ids)) != len(frontier.pending_operation_ids):
        raise CensusRefusal("DUPLICATE_PENDING_OPERATION_ID")
    if any(op_id not in operations or operations[op_id].disposition != "ELIGIBLE"
           for op_id in frontier.pending_operation_ids):
        raise CensusRefusal("PENDING_OPERATION_OUTSIDE_ELIGIBLE_CENSUS")
    axes = frontier.axis_conservation()
    if not (axes["considered_equals_eligibility"] and
            axes["execution_equals_considered"] and
            axes["result_equals_considered"] and
            axes["eligibility_partition_ok"] and
            axes["execution_partition_ok"] and axes["result_partition_ok"]):
        raise CensusRefusal("FRONTIER_AXIS_NOT_CONSERVED", axes)
    return {
        "source_candidate_count": len(sources),
        "scientific_fate_count": len(scientific),
        "eligible_count": counts.get("ELIGIBLE", 0),
        "fate_counts": dict(sorted(counts.items())),
        "source_census_ref": census.source_census_ref,
        "science_census_ref": census.science_census_ref,
        "frozen_census_hash": census.content_hash,
        "frontier_hash": frontier.content_hash,
        "deferred_scope_count": len(frontier.deferred),
        "deferred_scope_records": list(frontier.deferred),
    }


def execute_censused_sourcefree(
    *, census: FrozenInputCensus, inventory: SourceInventory,
    policy: GrammarPolicy, frontier: ScientificFrontier, bundle: Any,
    as_of: str, host: str, purpose: str, source_factory: Callable[[Any], Any],
) -> Mapping[str, Any]:
    """Real R03 compiler -> TEST_ONLY U43 envelope -> Batch/C11/I05 facts.

    This tests the existing bounded R03 issued first consumer; it does not
    invoke U43's separate normal/resume production executor or mint a CURRENT
    source/science decision. Those remain S1-D and original-issuer boundaries.

    Returns a frozen-scope audit only AFTER both pre-compilation and real
    post-execution anti-joins succeed. Never opens an original source on HOLD.
    """
    audit = verify_frozen_inputs(
        census, inventory=inventory, policy=policy, frontier=frontier,
    )
    before = perf_counter()
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=as_of, host=host, purpose=purpose,
    )
    ids = [record.operation_id for record in compilation.plan.records]
    ids += list(compilation.pending_operation_ids)
    if len(ids) != len(set(ids)):
        raise CensusRefusal("COMPILER_DUPLICATED_OPERATION", ids)
    expected_ids = {row.operation_id for row in census.source_candidates}
    _same_ids(expected_ids, set(ids), "FROZEN_VS_COMPILER")
    supplied_dispositions = {
        row.operation_id: row.disposition for row in census.scientific_fates
    }
    if dict(compilation.operation_dispositions or {}) != supplied_dispositions:
        raise CensusRefusal("COMPILER_ELIGIBILITY_DRIFT")
    expected_supported = set(compilation.expected_operation_ids)
    if (expected_supported | set(compilation.unsupported_operation_ids) |
            set(compilation.not_eligible_operation_ids) |
            set(compilation.pending_operation_ids)) != expected_ids:
        raise CensusRefusal("LOWERING_FATE_LOSS")
    opens = 0

    def counted_factory(source_ref: Any) -> Any:
        nonlocal opens
        opens += 1
        return source_factory(source_ref)

    result = execute_governed_frontier(
        compilation=compilation, source_factory=counted_factory,
    )
    if result.anti_join.get("no_drop_ok") is not True:
        raise CensusRefusal("ISSUED_CANDIDATE_ANTI_JOIN_FAILED", result.anti_join)
    if result.operation_anti_join.get("no_drop_ok") is not True:
        raise CensusRefusal("ISSUED_OPERATION_ANTI_JOIN_FAILED", result.operation_anti_join)
    rows = result.operation_ledger
    if len({row["operation_id"] for row in rows}) != len(rows):
        raise CensusRefusal("DUPLICATE_RESULT_OPERATION")
    _same_ids(expected_ids, {row["operation_id"] for row in rows}, "FROZEN_VS_RECEIPT")
    actual_by_id = {row["operation_id"]: row for row in rows}
    for op_id, fate in supplied_dispositions.items():
        if actual_by_id[op_id].get("eligibility_state", fate) != fate:
            raise CensusRefusal("RECEIPT_SCIENCE_FATE_DRIFT", op_id)
        if fate != "ELIGIBLE" and (
            actual_by_id[op_id]["received_candidate_ids"] or
            actual_by_id[op_id]["fact_refs"]
        ):
            raise CensusRefusal("NONELIGIBLE_WAS_EXECUTED", op_id)
    # The retained pre-existing checkpoint validator independently checks
    # receipts, fact/identity closure, native candidates, and ledger hashes.
    checkpoint = result.freeze_restore_checkpoint()
    return {
        "schema": SCHEMA, "grade": SCOPE, "scope_id": census.scope_id,
        **audit,
        "compiler_hash": compilation.content_hash,
        "checkpoint_hash": checkpoint,
        "declared_operation_count": len(expected_ids),
        "compiled_operation_count": len(ids),
        "supported_operation_count": len(expected_supported),
        "received_operation_count": len(rows),
        "issued_candidate_count": len(result.receipt_refs),
        "native_fact_count": len(result.fact_refs),
        "source_factory_calls": opens,
        "elapsed_seconds": perf_counter() - before,
        "candidate_anti_join": dict(result.anti_join),
        "operation_anti_join": dict(result.operation_anti_join),
        "operation_fates": [
            {
                "operation_id": row["operation_id"],
                "scientific_disposition": supplied_dispositions[row["operation_id"]],
                "lowering_status": row["lowering_status"],
                "execution_state": row["execution_state"],
                "result_state": row["result_state"],
                "received_candidate_ids": list(row["received_candidate_ids"]),
                "missing_candidate_ids": list(row["missing_candidate_ids"]),
                "receipt_refs": list(row["receipt_refs"]),
                "fact_refs": list(row["fact_refs"]),
            } for row in rows
        ],
    }
