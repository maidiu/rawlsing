"""General source-exact S04 joint algebra over ONE already-qualified I03 joint.

The scientific workload is not enumerated, benchmark-sized or tied to an
authored list of 1/10/100 queries.  A caller can ask successive, arbitrarily
different projected/conditioned questions, including multidimensional
outputs. Inverted exact cell-state postings and bounded predicate-prefix
intersections are shared across *different* requests without revisiting I03,
C11 or the original respondent corpus.

This is a descriptive full-case SAMPLE algebra. It never merges separate
respondent risks, imputes nonresponse, calculates predictor determinicity or
variance, generates people, or issues original-source authorization.
"""
from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import prod
from json import loads
from typing import Any, Callable, Iterable, Mapping

from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonical_json, canonicalize, semantic_hash,
)
from rawlsing_next.pre553_s04_observed_research import (
    S04ObservedKnowledge, S04KnowledgeError, SAMPLE_GRADE, UNISSUED,
)

CONTRACT = "S04_GENERAL_SOURCE_EXACT_JOINT_PROJECTION@1.0.0"
SCIENTIFIC_GRADE = "SINGLE_ACTUAL_I03_FULL_JOINT__RAW_SAMPLE_ONLY__NO_NEW_ISSUER"


class S04GeneralAlgebraError(ValueError):
    """Requested calculation would change source meaning or qualified scope."""


@dataclass(frozen=True)
class S04Projection:
    """Ordered output axes; arbitrary source-domain conditioner axes.

    Empty output_axes is an exact scalar selected-support query.  Asking for
    the same axis as both condition and output is refused, since it can
    accidentally masquerade as predictive evidence.
    """
    output_axes: tuple[int, ...]
    conditions: Mapping[int, Any]


@dataclass(frozen=True)
class S04ProjectionAnswer:
    payload_json: str
    content_hash: str

    def __post_init__(self) -> None:
        try:
            material = loads(self.payload_json)
            if (type(material) is not dict
                    or material.get("contract") != CONTRACT
                    or canonical_json(material) != self.payload_json
                    or semantic_hash(material) != self.content_hash):
                raise S04GeneralAlgebraError("noncanonical general projection receipt")
        except (TypeError, ValueError, KeyError) as exc:
            raise S04GeneralAlgebraError("malformed general projection receipt") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            CONTRACT,
            f"urn:rawlsing:s04:general-projection:sha256:{self.content_hash}",
            self.content_hash,
        )

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


class S04GeneralJointWorkspace:
    """Reusable on-demand relational algebra over one S04 respondent-coherent joint.

    Data structure is source-sized, not workload-sized. Cache capacity is a
    performance budget; eviction never changes an answer. Multiple output
    projections on the same context reuse the exact selected full-joint rows.
    Larger/indefinite workloads can query incrementally without enumerating
    all candidate combinations or retaining every output.
    """

    def __init__(
        self,
        *,
        knowledge: S04ObservedKnowledge,
        expected_knowledge_ref: ExactRef,
        max_filter_cache_entries: int = 128,
        max_cached_row_ids: int = 65_536,
        current_guard: Callable[[], Any] | None = None,
    ) -> None:
        if type(knowledge) is not S04ObservedKnowledge:
            raise S04GeneralAlgebraError("actual S04 knowledge object required")
        if type(expected_knowledge_ref) is not ExactRef or expected_knowledge_ref != knowledge.ref:
            raise S04GeneralAlgebraError("external expected S04 identity mismatch")
        if (type(max_filter_cache_entries) is not int
                or max_filter_cache_entries < 1
                or type(max_cached_row_ids) is not int
                or max_cached_row_ids < 1):
            raise S04GeneralAlgebraError("positive finite resource budgets required")
        if current_guard is not None and not callable(current_guard):
            raise S04GeneralAlgebraError("CURRENT guard must be callable or absent")
        self._current_guard = current_guard
        self._check_current()
        self._knowledge = knowledge
        self._material = knowledge.material()
        m = self._material
        if (m.get("contract") != "S04_SOURCE_EXACT_OBSERVED_KNOWLEDGE@1.0.0"
                or m.get("source_scope_mode") != "SINGLE_UNIVERSE"
                or m.get("measure_kind") != "RAW"
                or m.get("state") not in ("SUPPORTED_SAMPLE_DESCRIPTIVE", "PRODUCER_TYPED_HELD")):
            raise S04GeneralAlgebraError("unsupported or unqualified original S04 source")
        arity = m.get("target_arity")
        domains = m.get("target_domains")
        if (type(arity) is not int or arity < 1
                or not isinstance(domains, list) or len(domains) != arity):
            raise S04GeneralAlgebraError("missing exact original S04 target topology")
        self._domains: tuple[tuple[Any, ...], ...] = tuple(tuple(d) for d in domains)
        self._domain_keys: tuple[set[str], ...] = tuple(
            {canonical_json(v) for v in domain} for domain in self._domains
        )
        if any(not keys or len(keys) != len(domain)
               for keys, domain in zip(self._domain_keys, self._domains)):
            raise S04GeneralAlgebraError("duplicate or empty source domain")
        if (type(m.get("raw_eligible_condition_denominator")) is not int
                or type(m.get("raw_fully_resolved_joint_n")) is not int
                or not 0 <= m["raw_fully_resolved_joint_n"] <= m["raw_eligible_condition_denominator"]):
            raise S04GeneralAlgebraError("invalid native sample support")

        self._supported = m["state"] == "SUPPORTED_SAMPLE_DESCRIPTIVE"
        if self._supported != (m.get("producer_typed_state") == "SUPPORTED"):
            raise S04GeneralAlgebraError("S04 producer state and supported grade disagree")
        if self._supported and (
            m["raw_fully_resolved_joint_n"] <= 0
            or m["raw_fully_resolved_joint_n"] != m["raw_eligible_condition_denominator"]
        ):
            raise S04GeneralAlgebraError(
                "SUPPORTED full joint requires complete eligible/resolved source risk"
            )
        rows = m.get("complete_cells")
        if type(rows) is not list:
            raise S04GeneralAlgebraError("S04 complete_cells must be an exact list")
        if not self._supported and rows:
            raise S04GeneralAlgebraError("held I03 knowledge cannot furnish full cell counts")

        self._positive_cells: list[tuple[tuple[Any, ...], int]] = []
        postings: dict[tuple[int, str], set[int]] = {}
        seen: set[str] = set()
        total = 0
        for row in rows:
            if (type(row) is not dict or type(row.get("raw_count")) is not int
                    or row["raw_count"] < 0
                    or not isinstance(row.get("cell"), list)
                    or len(row["cell"]) != arity):
                raise S04GeneralAlgebraError("malformed real S04 full cell")
            cell = tuple(row["cell"])
            key = canonical_json(list(cell))
            if key in seen or any(
                canonical_json(value) not in self._domain_keys[i]
                for i, value in enumerate(cell)
            ):
                raise S04GeneralAlgebraError("duplicate or alien joint cell")
            seen.add(key)
            n = row["raw_count"]
            if row.get("cell_state") != (
                "OBSERVED_POSITIVE" if n else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
            ):
                raise S04GeneralAlgebraError("S04 source zero/positive cell state altered")
            total += n
            if n:
                pos = len(self._positive_cells)
                self._positive_cells.append((cell, n))
                for axis, value in enumerate(cell):
                    postings.setdefault((axis, canonical_json(value)), set()).add(pos)
        if self._supported and len(seen) != prod(len(d) for d in self._domains):
            raise S04GeneralAlgebraError("S04 complete joint domain omitted source-declared cells")
        if self._supported and total != m["raw_fully_resolved_joint_n"]:
            raise S04GeneralAlgebraError("S04 full-case cell counts violate source denominator")
        if not self._supported and total:
            raise S04GeneralAlgebraError("held source cannot acquire supported positive cells")
        self._postings = {key: frozenset(ids) for key, ids in postings.items()}
        self._all = frozenset(range(len(self._positive_cells)))
        self._cache: OrderedDict[tuple[tuple[int, str], ...], frozenset[int]] = OrderedDict()
        self._cache_cap = max_filter_cache_entries
        self._row_id_cap = max_cached_row_ids
        self._cached_row_ids = 0
        self._hits = 0
        self._misses = 0
        self._intersections = 0
        self._evictions = 0

    def _selection(
        self, conditions: Mapping[int, Any], output_axes: tuple[int, ...],
    ) -> tuple[tuple[int, str, Any], ...]:
        if not isinstance(conditions, Mapping):
            raise S04GeneralAlgebraError("source-domain conditions must be a mapping")
        selected = []
        for axis, raw in conditions.items():
            if (type(axis) is not int or not 0 <= axis < len(self._domains)
                    or axis in output_axes):
                raise S04GeneralAlgebraError("invalid condition axis or target leakage")
            value = canonicalize(raw)
            key = canonical_json(value)
            if key not in self._domain_keys[axis]:
                raise S04GeneralAlgebraError("condition value outside exact source domain")
            selected.append((axis, key, value))
        return tuple(sorted(selected, key=lambda x: x[0]))

    def _rows_for(self, selected: tuple[tuple[int, str, Any], ...]) -> frozenset[int]:
        rows = self._all
        prefix: tuple[tuple[int, str], ...] = ()
        for axis, key, _ in selected:
            prefix += ((axis, key),)
            hit = self._cache.get(prefix)
            if hit is not None:
                self._hits += 1
                self._cache.move_to_end(prefix)
                rows = hit
                continue
            self._misses += 1
            self._intersections += 1
            rows = rows.intersection(self._postings.get((axis, key), frozenset()))
            if len(rows) <= self._row_id_cap:
                while (self._cache and
                       (len(self._cache) >= self._cache_cap
                        or self._cached_row_ids + len(rows) > self._row_id_cap)):
                    _, evicted = self._cache.popitem(last=False)
                    self._cached_row_ids -= len(evicted)
                    self._evictions += 1
                self._cache[prefix] = rows
                self._cached_row_ids += len(rows)
        return rows

    def _check_current(self) -> None:
        if self._current_guard is not None:
            # A callback is not an issuer. Native integration binds the
            # actual VerifiedDirectEstate._live guard, which can revoke.
            result = self._current_guard()
            # Native _live success returns None and denial raises. Do not
            # treat numeric zero, strings, or other sentinels as grants.
            if result is not None and result is not True:
                raise S04GeneralAlgebraError("CURRENT denied by bound source guard")

    def query(self, request: S04Projection) -> S04ProjectionAnswer:
        self._check_current()
        if type(request) is not S04Projection or type(request.output_axes) is not tuple:
            raise S04GeneralAlgebraError("typed ordered projection required")
        axes = request.output_axes
        if (len(axes) != len(set(axes))
                or any(type(i) is not int or i < 0 or i >= len(self._domains) for i in axes)):
            raise S04GeneralAlgebraError("invalid, duplicated or noninteger output axis")
        selection = self._selection(request.conditions, axes)
        m = self._material
        if self._supported:
            selected_rows = self._rows_for(selection)
            n = sum(self._positive_cells[i][1] for i in selected_rows)
            aggregation: dict[str, int] = {}
            for index in selected_rows:
                values, count = self._positive_cells[index]
                output = [values[axis] for axis in axes]
                key = canonical_json(output)
                aggregation[key] = aggregation.get(key, 0) + count
            possible = product(*(self._domains[axis] for axis in axes))
            cells = []
            for values in possible:
                output = list(values)
                count = aggregation.get(canonical_json(output), 0)
                proportion = Fraction(count, n) if n else None
                cells.append({
                    "output_states": output,
                    "raw_count": count,
                    "raw_fraction_of_selected_full_cases": (
                        {"$exact_fraction": [proportion.numerator, proportion.denominator]}
                        if proportion is not None else None
                    ),
                    "cell_state": (
                        "OBSERVED_POSITIVE" if count
                        else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
                        if n else "ZERO_WITHIN_RESOLVED_FULL_CASES"
                    ),
                })
            if sum(cell["raw_count"] for cell in cells) != n:
                raise S04GeneralAlgebraError("projection lost original full-case support")
            state = "OBSERVED_FULL_CASE_SUPPORT" if n else "ZERO_WITHIN_RESOLVED_FULL_CASES"
        else:
            n, cells, state = None, [], "UPSTREAM_SCIENCE_OR_SOURCE_HELD"

        payload = {
            "contract": CONTRACT,
            "grade": SCIENTIFIC_GRADE,
            "state": state,
            "original_producer_typed_state": m["producer_typed_state"],
            "knowledge_ref": self._knowledge.ref.as_dict(),
            "source_query_ref": m["query_ref"],
            "source_fact_ref": m["fact_ref"],
            "source_release_ref": m["release_ref"],
            "source_universe_ref": m["universe_ref"],
            "source_risk_set_ref": m["risk_set_ref"],
            "source_measure_basis_ref": m["measure_basis_ref"],
            "source_response_semantics_ref": m["response_semantics_ref"],
            "original_source_authenticity": m["source_authenticity"],
            "independent_original_source_issuer": None,
            "source_current_check": (
                "BOUND_GUARD_PRE_POST__NOT_SOURCE_ISSUANCE" if self._current_guard
                else "OFFLINE_SOURCE_CURRENT_UNVERIFIED"
            ),
            "output_axes": [
                {"index": i, "target_ref": m["target_refs"][i]} for i in axes
            ],
            "conditions": [
                {"index": i, "conditioner_ref": m["target_refs"][i], "value": value}
                for i, _, value in selection
            ],
            "raw_source_eligible_n": m["raw_eligible_condition_denominator"],
            "raw_original_full_joint_resolved_n": m["raw_fully_resolved_joint_n"],
            "raw_selected_full_case_n": n,
            "complete_output_cells": cells,
            "comparative_predictor_rank": None,
            "population_variance_or_causal_estimate": None,
            "no_second_i03_or_source_query": True,
            "no_cross_fact_or_cross_risk_pooling": True,
            "unissued": list(UNISSUED),
        }
        self._check_current()
        return S04ProjectionAnswer(canonical_json(payload), semantic_hash(payload))

    def query_many(self, requests: Iterable[S04Projection]) -> Iterable[S04ProjectionAnswer]:
        """Lazy requests with NO artificial cardinality or discovery threshold.

        Each answer is scoped to its existing research fact; this API does
        not itself authenticate source rights or authorize any publication.
        """
        for request in requests:
            yield self.query(request)

    def cache_stats(self) -> dict[str, int]:
        """Nonsemantic local performance evidence, never a scientific claim."""
        return {
            "stored_positive_joint_cells": len(self._positive_cells),
            "indexed_axis_values": len(self._postings),
            "cached_intersections": len(self._cache),
            "cached_row_ids": self._cached_row_ids,
            "filter_cache_hits": self._hits,
            "filter_cache_misses": self._misses,
            "intersection_steps": self._intersections,
            "filter_cache_evictions": self._evictions,
        }


__all__ = [
    "CONTRACT", "SCIENTIFIC_GRADE", "S04GeneralAlgebraError", "S04Projection",
    "S04ProjectionAnswer", "S04GeneralJointWorkspace",
]
