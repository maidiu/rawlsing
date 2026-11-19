"""S04 scientific-descriptive research layer BEFORE Field Forge.

Consumes exact I03-owned EmpiricalFact/QueryExecutionResult; never decodes
source, writes C11, invokes an alternative query engine, invents a ranking
estimator, asserts survey representativeness, or creates a Field Forge object.

Each supported product conserves one original full respondent-coherent joint
and lets many conditional research questions be asked from *that same* joint.
This is a sample-descriptive research projection, not scientific authority.
S04's method owner must still issue a valid estimand/rank/uncertainty/search
policy for comparative determinicity or population claims.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from json import loads
from math import prod
from typing import Any, Mapping, Sequence

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact, EmpiricalQuerySpec, ExactRef, authority_ref, canonical_json,
    canonicalize, exact_ref, semantic_hash,
)

CONTRACT = "S04_SOURCE_EXACT_OBSERVED_KNOWLEDGE@1.0.0"
ANSWER_CONTRACT = "S04_SOURCE_EXACT_CONDITIONED_ANSWER@1.0.0"
MAX_CELLS = 16384  # bounding the sourcefree artifact, not a universal capability limit
SAMPLE_GRADE = "RAW_FULLY_RESOLVED_SAME_RESPONDENT_SAMPLE_NOT_POPULATION"
UNISSUED = (
    "COMPARATIVE_DETERMINICITY_METRIC_NOT_ISSUED",
    "SAMPLING_DESIGN_AND_VARIANCE_NOT_ISSUED",
    "MULTIPLICITY_POSTSELECTION_AND_RANK_STABILITY_NOT_ISSUED",
    "DATA_ADAPTIVE_RECURSIVE_MINORITY_STOPPING_NOT_ISSUED",
    "MATERIAL_POWER_CAUSALITY_NOT_INFERRED_FROM_ATTITUDE_COTRAVEL",
    "INTERPERSONAL_RELATIONSHIP_OR_ACTOR_NOT_OBSERVED_BY_SAME_PERSON_SURVEY",
)


class S04KnowledgeError(ValueError):
    """Unqualified input, changed source identity or unsupported science claim."""


@dataclass(frozen=True)
class S04ObservedKnowledge:
    payload_json: str
    content_hash: str

    def __post_init__(self) -> None:
        material = loads(self.payload_json)
        if (canonical_json(material) != self.payload_json
                or material.get("contract") != CONTRACT
                or semantic_hash(material) != self.content_hash):
            raise S04KnowledgeError("S04 knowledge object hash/contract mismatch")

    @property
    def ref(self) -> ExactRef:
        return ExactRef(CONTRACT, f"urn:rawlsing:s04:observed:sha256:{self.content_hash}", self.content_hash)

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


@dataclass(frozen=True)
class S04ResearchAnswer:
    payload_json: str
    content_hash: str

    def __post_init__(self) -> None:
        material = loads(self.payload_json)
        if (canonical_json(material) != self.payload_json
                or material.get("contract") != ANSWER_CONTRACT
                or semantic_hash(material) != self.content_hash):
            raise S04KnowledgeError("S04 answer hash/contract mismatch")

    @property
    def ref(self) -> ExactRef:
        return ExactRef(ANSWER_CONTRACT, f"urn:rawlsing:s04:answer:sha256:{self.content_hash}", self.content_hash)

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


def _exact(value: Any, label: str) -> ExactRef:
    try:
        return exact_ref(value, label)
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise S04KnowledgeError(f"missing or invalid exact {label}") from exc


def _unique_refs(values: Any, label: str) -> tuple[ExactRef, ...]:
    if values is None or isinstance(values, (str, bytes)):
        raise S04KnowledgeError(f"missing exact {label} refs")
    refs = tuple(_exact(x, label) for x in values)
    if len(set(refs)) != len(refs):
        raise S04KnowledgeError(f"duplicate {label} exact identity")
    return refs


def _domains(query: EmpiricalQuerySpec) -> tuple[tuple[ExactRef, ...], tuple[tuple[Any, ...], ...]]:
    targets = _unique_refs(query.target_refs, "target")
    topo = query.target_arity_and_topology
    if not isinstance(topo, Mapping) or not targets or topo.get("arity") != len(targets):
        raise S04KnowledgeError("query has no exact scalar target topology")
    if topo.get("joint_order_semantics") not in ("SEMANTIC_ORDERED", "CANONICAL_SET_ORDER"):
        raise S04KnowledgeError("unsupported target role order")
    if topo.get("joint_order_semantics") == "CANONICAL_SET_ORDER" and targets != tuple(sorted(targets, key=lambda ref: ref.key)):
        raise S04KnowledgeError("canonical set target order not preserved")
    components = topo.get("components")
    if not isinstance(components, (list, tuple)) or len(components) != len(targets):
        raise S04KnowledgeError("target components do not cover selected refs")
    out: list[tuple[Any, ...]] = []
    for ref, raw in zip(targets, components):
        if (not isinstance(raw, Mapping) or _exact(raw.get("target_ref"), "target component") != ref
                or raw.get("topology") != "SCALAR_SINGULAR"):
            raise S04KnowledgeError("repeated/multiselect or changed component role is held")
        _exact(raw.get("target_domain_replay_ref"), "component domain replay")
        values = raw.get("domain")
        if not isinstance(values, (list, tuple)) or not values:
            raise S04KnowledgeError("nonempty source-declared target domain required")
        normalized = tuple(canonicalize(x) for x in values)
        if len({canonical_json(x) for x in normalized}) != len(normalized):
            raise S04KnowledgeError("duplicate source-domain state")
        out.append(normalized)
    if prod(len(x) for x in out) > MAX_CELLS:
        raise S04KnowledgeError("joint domain exceeds bounded sourcefree S04 transport limit")
    return targets, tuple(out)


def receive_s04_i03_research(
    *,
    query: EmpiricalQuerySpec,
    execution: QueryExecutionResult,
) -> S04ObservedKnowledge:
    """Promote no new authority; preserve actual I03 fact and its typed science.

    This is a pure projection over an ALREADY EXECUTED I03 result. A hash-valid
    sourcefree fixture proves internal consistency, not original survey custody.
    """
    if type(query) is not EmpiricalQuerySpec or type(execution) is not QueryExecutionResult:
        raise S04KnowledgeError("actual I03 query/result types required")
    if query.typed_state != "QUERY_AUTHORIZED_RESOLVABLE":
        raise S04KnowledgeError("query not in authorized resolvable state")
    if semantic_hash(query.semantic_projection()) != query.content_hash or query.ref != execution.query_ref:
        raise S04KnowledgeError("I03 query exact identity mismatch")
    if execution.source_scope_mode != "SINGLE_UNIVERSE" or len(execution.release_refs) != 1:
        raise S04KnowledgeError("no sample pooling across independent source releases")
    if len(execution.facts) != 1 or type(execution.facts[0]) is not EmpiricalFact:
        raise S04KnowledgeError("exact one I03-owned source-scoped empirical fact required")
    fact = execution.facts[0]
    if semantic_hash(fact.semantic_projection()) != fact.content_hash:
        raise S04KnowledgeError("I03 fact exact semantic identity mismatch")
    if _exact(fact.empirical_query_spec_ref, "fact query") != query.ref:
        raise S04KnowledgeError("fact belongs to a different query")
    for name, left, right in (
        ("condition predicate", fact.condition_predicate_ref, query.condition_predicate_ref),
        ("risk denominator", fact.risk_set_ref, query.risk_set_ref),
        ("measure basis", fact.measure_basis_ref, query.measure_basis_ref),
    ):
        if _exact(left, name) != _exact(right, name):
            raise S04KnowledgeError(f"{name} changed between query and fact")
    universes = _unique_refs(query.empirical_universe_refs, "universe")
    if len(universes) != 1 or universes != _unique_refs(fact.empirical_universe_refs, "fact universe"):
        raise S04KnowledgeError("fact changed its source universe")
    grain = query.requested_output_grain
    if (not isinstance(grain, Mapping) or grain.get("source_scope_mode") != "SINGLE_UNIVERSE"
            or grain.get("measure_kind") != "RAW" or fact.measure_kind != "RAW"):
        raise S04KnowledgeError("only RAW unpooled sourcefree descriptive science admitted")
    if _exact(fact.response_state_semantics_ref, "response semantics") != _exact(
            grain.get("response_state_semantics_ref"), "query response semantics"):
        raise S04KnowledgeError("response state/routing meaning changed")
    if fact.uncertainty_method_or_typed_state != grain.get("uncertainty_method_or_typed_state"):
        raise S04KnowledgeError("uncertainty claim mismatched its I03 query")
    if fact.weighted_numerator_support_if_authorized is not None or fact.weighted_denominator_support_if_authorized is not None:
        raise S04KnowledgeError("weighted evidence cannot silently become RAW science")
    replay = _exact(fact.replay_ref, "fact replay")
    if replay != _exact(fact.producer_replay_locator_or_reference_root, "replay root"):
        raise S04KnowledgeError("I03 fact replay root mismatch")
    dependencies = set(_unique_refs(fact.dependency_refs, "fact dependencies"))
    provenance = set(_unique_refs(fact.source_empirical_provenance_refs, "source provenance"))
    release = _exact(execution.release_refs[0], "execution release")
    if (not provenance or not provenance.issubset(dependencies)
            or release not in provenance or not {query.ref, release, replay}.issubset(dependencies)):
        raise S04KnowledgeError("source/query/release/fact replay closure absent")
    issuers = {authority_ref(item) for item in query.query_authority_refs}
    authorities = set(fact.authority_snapshot_refs)
    if (not issuers or not authorities or not issuers.issubset(authorities)
            or not set(query.authority_snapshot_refs).issubset(authorities)):
        raise S04KnowledgeError("I03 operation issuer/authority closure absent")
    targets, domains = _domains(query)
    eligible = fact.raw_denominator_support
    resolved = fact.raw_numerator_support
    if type(eligible) is not int or type(resolved) is not int or min(eligible, resolved) < 0 or resolved > eligible:
        raise S04KnowledgeError("negative or impossible eligible/resolved support")

    rows: list[dict[str, Any]] = []
    if fact.typed_state == "SUPPORTED":
        if resolved <= 0:
            raise S04KnowledgeError("SUPPORTED source knowledge needs positive real joint support")
        topology = fact.target_topology
        if (not isinstance(topology, Mapping) or topology.get("arity") != len(targets)
                or topology.get("joint_order_semantics") != query.target_arity_and_topology["joint_order_semantics"]):
            raise S04KnowledgeError("fact target roles/order differ from query")
        raw_rows = topology.get("complete_cell_semantic_projection")
        if not isinstance(raw_rows, (list, tuple)):
            raise S04KnowledgeError("positive joint is missing full cell material")
        expected = (
            {canonical_json([v]) for v in domains[0]}
            if len(targets) == 1
            else {canonical_json(list(combo)) for combo in product(*domains)}
        )
        seen: set[str] = set()
        for row in raw_rows:
            if not isinstance(row, Mapping):
                raise S04KnowledgeError("malformed target cell")
            native_cell = row.get("cell")
            if len(targets) == 1:
                # I03 represents scalar F1 cells as scalar domain values, not
                # one-element tuples. The S04 research ABI stays k-wide.
                if isinstance(native_cell, (list, tuple)):
                    raise S04KnowledgeError("unary scalar source cell is not an array")
                cell = canonicalize([native_cell])
            else:
                if not isinstance(native_cell, (list, tuple)) or len(native_cell) != len(targets):
                    raise S04KnowledgeError("joint cell arity differs from query")
                cell = canonicalize(list(native_cell))
            key = canonical_json(cell)
            n = row.get("raw_numerator_support")
            if (key not in expected or key in seen or type(n) is not int or n < 0):
                raise S04KnowledgeError("duplicate, foreign, incomplete or negative cell")
            if row.get("cell_state") != (
                "OBSERVED_POSITIVE" if n else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
            ):
                raise S04KnowledgeError("source-observed ZERO/positive status changed")
            if row.get("weighted_numerator_support_if_authorized") is not None:
                raise S04KnowledgeError("weighted individual cell smuggled into RAW joint")
            rows.append({"cell": cell, "raw_count": n, "cell_state": row["cell_state"]})
            seen.add(key)
        if seen != expected or sum(row["raw_count"] for row in rows) != resolved:
            raise S04KnowledgeError("incomplete full joint or count/denominator inconsistency")
        risk_members = _unique_refs(fact.risk_set_member_refs, "risk respondents")
        denominator_members = _unique_refs(fact.denominator_member_refs, "eligible respondents")
        if (len(denominator_members) != eligible
                or not set(denominator_members).issubset(set(risk_members))
                or any(x.kind != "C11Internal:RespondentIdentity" for x in (*risk_members, *denominator_members))):
            raise S04KnowledgeError("wrong-kind, duplicated or out-of-risk respondent extent")
    elif fact.typed_state not in {
        "ZERO_SUPPORT", "OBSERVED_ZERO", "ZERO_OVERLAP", "LOW_SUPPORT",
        "NONCOMPARABLE", "NOT_APPLICABLE", "UNAVAILABLE", "UNRESOLVED",
        "VALID_EMPTY", "INTEGRITY_FAILURE", "UNSUPPORTED", "UNCERTAINTY_UNQUANTIFIED"
    }:
        raise S04KnowledgeError("unrecognized I03 nonpositive typed state")
    elif resolved > 0 and fact.typed_state not in {"LOW_SUPPORT", "UNCERTAINTY_UNQUANTIFIED"}:
        raise S04KnowledgeError("typed producer has unexplained positive count")

    publication = {
        "contract": CONTRACT,
        "state": "SUPPORTED_SAMPLE_DESCRIPTIVE" if fact.typed_state == "SUPPORTED" else "PRODUCER_TYPED_HELD",
        "producer_typed_state": fact.typed_state,
        "grade": SAMPLE_GRADE if fact.typed_state == "SUPPORTED" else "I03_NONPOSITIVE_OR_HELD_UNRESOLVED",
        "query_ref": query.ref.as_dict(),
        "fact_ref": fact.ref.as_dict(),
        "replay_ref": replay.as_dict(),
        "release_ref": release.as_dict(),
        "universe_ref": universes[0].as_dict(),
        "risk_set_ref": _exact(fact.risk_set_ref, "risk").as_dict(),
        "measure_basis_ref": _exact(fact.measure_basis_ref, "measure").as_dict(),
        "predicate_ref": _exact(query.condition_predicate_ref, "predicate").as_dict(),
        "response_semantics_ref": _exact(fact.response_state_semantics_ref, "responses").as_dict(),
        "target_refs": [x.as_dict() for x in targets],
        "target_domains": [list(x) for x in domains],
        "full_query_target_topology": canonicalize(query.target_arity_and_topology),
        "native_fact_target_domain_identity": fact.target_domain_identity,
        "joint_order_semantics": query.target_arity_and_topology["joint_order_semantics"],
        "target_arity": len(targets),
        "raw_eligible_condition_denominator": eligible,
        "raw_fully_resolved_joint_n": resolved,
        "risk_set_type": fact.risk_set_type,
        "source_scope_mode": fact.source_scope_mode,
        "measure_kind": fact.measure_kind,
        "producer_uncertainty_state": fact.uncertainty_method_or_typed_state,
        "complete_cells": sorted(rows, key=lambda row: canonical_json(row["cell"])),
        "authority_refs": [x.as_dict() for x in sorted(authorities, key=lambda ref: ref.key)],
        "source_provenance_refs": [x.as_dict() for x in sorted(provenance, key=lambda ref: ref.key)],
        "query_dependency_refs": [
            x.as_dict() for x in _unique_refs(query.dependency_refs, "query dependencies")
        ],
        "nonpositive_positive_count_retained_not_served": (
            resolved if fact.typed_state != "SUPPORTED" else None
        ),
        "not_issued": list(UNISSUED),
        "source_authenticity": "I03_HASH_AND_ISSUER_INTERNAL_CLOSURE__ORIGINAL_SOURCE_RIGHTS_UNVERIFIED",
        "per_cell_respondent_membership": "NOT_IN_AGGREGATE_EMPIRICAL_FACT",
    }
    h = semantic_hash(publication)
    return S04ObservedKnowledge(canonical_json(publication), h)


def _read(knowledge: S04ObservedKnowledge) -> dict[str, Any]:
    if type(knowledge) is not S04ObservedKnowledge:
        raise S04KnowledgeError("actual S04 knowledge object required")
    m = knowledge.material()
    if knowledge.ref.content_hash != semantic_hash(m):
        raise S04KnowledgeError("S04 knowledge identity invalid")
    return m


def _request(m: dict[str, Any], target_index: int, conditions: Mapping[int, Any]) -> tuple[tuple[int, Any], ...]:
    if type(target_index) is not int or not 0 <= target_index < m["target_arity"]:
        raise S04KnowledgeError("unknown exact target dimension")
    if not isinstance(conditions, Mapping):
        raise S04KnowledgeError("conditioners require exact dimension/value mapping")
    output: list[tuple[int, Any]] = []
    for index, raw in conditions.items():
        if type(index) is not int or not (0 <= index < m["target_arity"]) or index == target_index:
            raise S04KnowledgeError("invalid conditioner or target leakage")
        value = canonicalize(raw)
        if canonical_json(value) not in {canonical_json(v) for v in m["target_domains"][index]}:
            raise S04KnowledgeError("condition value absent from source-declared domain")
        output.append((index, value))
    return tuple(sorted(output))


def _answer(material: dict[str, Any]) -> S04ResearchAnswer:
    h = semantic_hash(material)
    return S04ResearchAnswer(canonical_json(material), h)


def ask_s04_exact_condition(
    *,
    knowledge: S04ObservedKnowledge,
    target_index: int,
    conditions: Mapping[int, Any],
) -> S04ResearchAnswer:
    """F1/F2 and k-way exact conditional from a single FULL joint risk.

    The denominator is the count of fully-resolved selected respondents,
    NOT the unconditional risk-eligible respondent count.
    """
    m = _read(knowledge)
    select = _request(m, target_index, conditions)
    counts = {canonical_json(value): 0 for value in m["target_domains"][target_index]}
    if m["state"] == "SUPPORTED_SAMPLE_DESCRIPTIVE":
        for row in m["complete_cells"]:
            if all(row["cell"][i] == v for i, v in select):
                counts[canonical_json(row["cell"][target_index])] += row["raw_count"]
        n = sum(counts.values())
        state = "OBSERVED_FULL_CASE_SUPPORT" if n else "ZERO_WITHIN_RESOLVED_FULL_CASES"
        cells = [{
            "target_state": canonicalize(value),
            "raw_count": counts[canonical_json(value)],
            "raw_fraction_of_selected_full_cases": (
                {"$exact_fraction": [Fraction(counts[canonical_json(value)], n).numerator,
                                     Fraction(counts[canonical_json(value)], n).denominator]}
                if n else None
            ),
        } for value in m["target_domains"][target_index]]
    else:
        n, state, cells = None, "UPSTREAM_SCIENCE_OR_SOURCE_HELD", []
    return _answer({
        "contract": ANSWER_CONTRACT,
        "kind": "SOURCE_EXACT_DESCRIPTIVE_CONDITIONAL",
        "state": state,
        "knowledge_ref": knowledge.ref.as_dict(),
        "source_query_ref": m["query_ref"],
        "source_fact_ref": m["fact_ref"],
        "source_release_ref": m["release_ref"],
        "risk_set_ref": m["risk_set_ref"],
        "target_index": target_index,
        "target_ref": m["target_refs"][target_index],
        "conditions": [
            {"index": i, "conditioner_ref": m["target_refs"][i], "exact_value": v}
            for i, v in select
        ],
        "raw_eligible_source_risk_denominator": m["raw_eligible_condition_denominator"],
        "raw_full_joint_resolved_n": m["raw_fully_resolved_joint_n"],
        "raw_conditioned_full_case_n": n,
        "complete_target_cells": cells,
        "denominator_grade": SAMPLE_GRADE,
        "unissued": list(UNISSUED),
    })


def ask_s04_common_risk_predictor_evidence(
    *,
    knowledge: S04ObservedKnowledge,
    target_index: int,
    candidate_indices: Sequence[int],
    context: Mapping[int, Any],
) -> S04ResearchAnswer:
    """Comparable candidate evidence on a *single exact* respondent-coherent risk.

    No MI, NMI, Cramer V or other estimator is silently selected; scientific
    owner still determines valid comparative metric and uncertainty.
    """
    m = _read(knowledge)
    selected_context = _request(m, target_index, context)
    normalized_context = dict(selected_context)
    if isinstance(candidate_indices, (str, bytes)) or not isinstance(candidate_indices, Sequence):
        raise S04KnowledgeError("candidate predictors must be explicit sequence")
    indices = tuple(candidate_indices)
    if (not indices or any(type(i) is not int or i == target_index or not (0 <= i < m["target_arity"]) for i in indices)
            or len(indices) != len(set(indices))):
        raise S04KnowledgeError("invalid comparable predictor selection")
    if any(i in normalized_context for i in indices):
        raise S04KnowledgeError("candidate predictor cannot be preselected in common context")
    indices = tuple(sorted(indices))
    baseline = ask_s04_exact_condition(
        knowledge=knowledge, target_index=target_index, conditions=normalized_context,
    )
    common_n = baseline.material()["raw_conditioned_full_case_n"]
    tables = []
    if m["state"] == "SUPPORTED_SAMPLE_DESCRIPTIVE":
        for index in indices:
            parts = []
            for value in m["target_domains"][index]:
                req = ask_s04_exact_condition(
                    knowledge=knowledge, target_index=target_index,
                    conditions={**normalized_context, index: value},
                )
                detail = req.material()
                parts.append({
                    "predictor_value": value,
                    "conditioned_answer_ref": req.ref.as_dict(),
                    "raw_conditioned_full_case_n": detail["raw_conditioned_full_case_n"],
                    "target_cells": detail["complete_target_cells"],
                })
            if sum(x["raw_conditioned_full_case_n"] for x in parts) != common_n:
                raise S04KnowledgeError("candidate partition violates common-risk conservation")
            tables.append({
                "candidate_index": index,
                "candidate_ref": m["target_refs"][index],
                "states": parts,
            })
    return _answer({
        "contract": ANSWER_CONTRACT,
        "kind": "COMPARABLE_CONDITIONAL_TABLES_NOT_DETERMINICITY_RANK",
        "state": (
            "COUNTS_AVAILABLE__SCIENTIFIC_METHOD_HELD" if tables and common_n
            else "ZERO_WITHIN_COMPLETE_CASE_CONTEXT" if tables and common_n == 0
            else "SOURCE_OR_SCIENCE_HELD"
        ),
        "knowledge_ref": knowledge.ref.as_dict(),
        "source_release_ref": m["release_ref"],
        "risk_set_ref": m["risk_set_ref"],
        "target_index": target_index,
        "target_ref": m["target_refs"][target_index],
        "candidate_indices": list(indices),
        "common_context": [
            {"index": i, "value": v} for i, v in selected_context
        ],
        "baseline_answer_ref": baseline.ref.as_dict(),
        "common_full_case_n": common_n,
        "tables": tables,
        "ranking": None,
        "variance_or_population_estimate": None,
        "unissued": list(UNISSUED),
    })


__all__ = [
    "CONTRACT", "ANSWER_CONTRACT", "MAX_CELLS",
    "S04KnowledgeError", "S04ObservedKnowledge", "S04ResearchAnswer",
    "receive_s04_i03_research", "ask_s04_exact_condition",
    "ask_s04_common_risk_predictor_evidence",
]
