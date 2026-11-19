"""S04 FF01 -> existing N10E exact first-consumer conservation bridge.

This is a strong *cross-read*, NOT a replacement possibility provider. It
requires that the independently executed accepted C1/N10E provider's actual
sample slice equals the selected conditioning slice of a real FF01 joint
from the SAME released respondents/risk/measure/semantics. It never fabricates
PossibilitySliceEvidence, models, actors or ranks. It currently invokes the
two accepted reader paths separately: repeated I03 work remains a cost hold.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from typing import Any, Mapping

from rawlsing_next.field_forge_generic_empirical_ingress import FF01ObservedJoint
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalPredicate, EmpiricalQuerySpec, ExactRef, canonical_json,
    canonicalize, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_empirical_possibility_provider import (
    EmpiricalPossibilitySliceProviderResult,
    PROVIDER_STATE_EXACT,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    PositionedSubjectPossibilityQuery,
)

CONTRACT = "S04_FF01_TO_N10E_EXACT_CROSSREAD@1.0.0"
CROSSREAD_GRADE = "SOURCEFREE_SAME_RELEASE_OBSERVED_COUNTS__NO_NEW_MODEL"
LIMITS = (
    "NOT_FF01_ISSUED_N10E_GEOMETRY__INDEPENDENT_OWNER_RECOMPUTATION",
    "NOT_ECONOMICAL_SINGLE_PASS__I03_MAY_EXECUTE_TWICE",
    "NOT_SOURCE_NATIVE_OR_SCIENTIFICALLY_REPRESENTATIVE",
    "NOT_FF02_N9_N10W_V3_OR_SOROK_AUTHORITY",
)


class FF01N10ECrossreadError(ValueError):
    """Source/query/condition/reader conservation was not demonstrated."""


@dataclass(frozen=True)
class FF01N10ECrossread:
    canonical_payload: str
    content_hash: str

    def __post_init__(self) -> None:
        content = loads(self.canonical_payload)
        if (canonical_json(content) != self.canonical_payload
                or content.get("contract") != CONTRACT
                or semantic_hash(content) != self.content_hash):
            raise FF01N10ECrossreadError("crossread hash/contract mismatch")

    @property
    def ref(self) -> ExactRef:
        return ExactRef(CONTRACT, f"urn:rawlsing:ff01:n10e-crossread:sha256:{self.content_hash}", self.content_hash)

    def material(self) -> dict[str, Any]:
        return loads(self.canonical_payload)


def _exact(value: Any, label: str) -> ExactRef:
    try:
        return exact_ref(value, label)
    except (TypeError, ValueError, AttributeError, KeyError) as exc:
        raise FF01N10ECrossreadError(f"missing or invalid {label}") from exc


def _actual_condition_leaf(predicate: EmpiricalPredicate) -> tuple[ExactRef, Any]:
    ast = predicate.predicate_ast
    if (not isinstance(ast, Mapping) or ast.get("op") != "LEAF"
            or ast.get("leaf_type") != "SURVEY_RESPONSE_EVENT"
            or ast.get("operator") != "EQ"):
        raise FF01N10ECrossreadError("only exact source-observed response-EQ conditioner bound by C1 is supported")
    return _exact(ast.get("question_semantic_ref"), "condition question"), canonicalize(ast.get("exact_value"))


def conserve_ff01_n10e_actual_read(
    *,
    ff01: FF01ObservedJoint,
    provider: EmpiricalPossibilitySliceProviderResult,
    n10e_empirical_query: EmpiricalQuerySpec,
    n10e_predicate: EmpiricalPredicate,
    n10e_consumer_query: PositionedSubjectPossibilityQuery,
) -> FF01N10ECrossread:
    """Require FF01 joint-conditioned counts == existing N10E generated geometry.

    In a k>2 joint this sums over other FULLY RESOLVED target axes.
    No implicit cross-universe/survey pooling; different asked/resolved risk
    sets refuse rather than quietly deliver a misleading equality.
    """
    if (type(ff01) is not FF01ObservedJoint
            or type(provider) is not EmpiricalPossibilitySliceProviderResult
            or type(n10e_empirical_query) is not EmpiricalQuerySpec
            or type(n10e_predicate) is not EmpiricalPredicate
            or type(n10e_consumer_query) is not PositionedSubjectPossibilityQuery):
        raise FF01N10ECrossreadError("actual FF01 / accepted C1 query and output types required")
    material = ff01.semantic_projection()
    if ff01.ref.content_hash != semantic_hash(material):
        raise FF01N10ECrossreadError("FF01 source receipt identity mismatch")
    if material["producer_state"] != "SUPPORTED":
        raise FF01N10ECrossreadError("unissued or nonpositive FF01 cannot support a positive N10E crossread")
    if provider.provider_state != PROVIDER_STATE_EXACT:
        raise FF01N10ECrossreadError("N10E producer is a refusal, not an exact current possibility")
    comp = provider.composition_result
    if comp.producer_route != "DIRECT_I03_TO_POSITIONED_SUBJECT":
        raise FF01N10ECrossreadError("bounded crossread requires actual direct C1/I03 route")
    if comp.producer_query_ref != n10e_empirical_query.ref or comp.producer_predicate_ref != n10e_predicate.ref:
        raise FF01N10ECrossreadError("N10E query/predicate identity mismatch")
    if comp.consumer_query_ref != n10e_consumer_query.ref:
        raise FF01N10ECrossreadError("N10E consumer query substitution")
    if (len(comp.source_universe_refs) != 1 or len(comp.release_refs) != 1
            or comp.source_universe_refs[0] != _exact(material["universe_ref"], "FF01 universe")
            or comp.release_refs[0] != _exact(material["release_ref"], "FF01 release")):
        raise FF01N10ECrossreadError("source/release are not identical and cannot be pooled")
    if comp.risk_set_ref != _exact(material["risk_set_ref"], "FF01 risk"):
        raise FF01N10ECrossreadError("N10E risk set differs from FF01 complete-coexposure scope")
    if comp.measure_kind != "RAW" or comp.measure_basis_ref != _exact(material["measure_basis_ref"], "FF01 measure"):
        raise FF01N10ECrossreadError("RAW measure / weight scope changed")
    if comp.uncertainty_state != material["uncertainty_state"]:
        raise FF01N10ECrossreadError("uncertainty method/typed state changed")
    if n10e_consumer_query.source_universe_ref != comp.source_universe_refs[0] or n10e_consumer_query.release_ref != comp.release_refs[0]:
        raise FF01N10ECrossreadError("consumer uses different source/release")
    if len(n10e_empirical_query.target_refs) != 1:
        raise FF01N10ECrossreadError("selected C1 direct producer must have exact single target")
    target_ref = _exact(n10e_empirical_query.target_refs[0], "N10E target")
    if n10e_consumer_query.target_ref != target_ref:
        raise FF01N10ECrossreadError("consumer target role differs from producer")
    if not n10e_consumer_query.conditioner_bindings or len(n10e_consumer_query.conditioner_bindings) != 1:
        raise FF01N10ECrossreadError("exact one condition-value witness required")
    conditioner = n10e_consumer_query.conditioner_bindings[0].empirical_coordinate_ref
    condition_question, condition_value = _actual_condition_leaf(n10e_predicate)
    if condition_question != conditioner:
        raise FF01N10ECrossreadError("N10E predicate's question differs from positioned conditioner")
    target_refs = [_exact(x, "FF01 target") for x in material["target_refs"]]
    if target_refs.count(conditioner) != 1 or target_refs.count(target_ref) != 1:
        raise FF01N10ECrossreadError("FF01 joint lacks unique source conditioner or target")
    condition_index = target_refs.index(conditioner)
    target_index = target_refs.index(target_ref)
    if condition_index == target_index or material["conditioner_index"] != condition_index:
        raise FF01N10ECrossreadError("conditioner/target direction changed at FF01 boundary")
    if (_exact(n10e_empirical_query.risk_set_ref, "N10E risk") != comp.risk_set_ref
            or _exact(n10e_empirical_query.measure_basis_ref, "N10E measure") != comp.measure_basis_ref
            or n10e_empirical_query.requested_output_grain.get("measure_kind") != "RAW"
            or n10e_empirical_query.requested_output_grain.get("response_state_semantics_ref") is None):
        raise FF01N10ECrossreadError("N10E query risk/measure/response origin mismatch")

    evidence = provider.generated_evidence_or_null
    consumer = provider.consumer_result_or_null
    if evidence is None or consumer is None or consumer.result_state != "EXACT_SUPPORTED":
        raise FF01N10ECrossreadError("N10E not consumed as exact supported evidence")
    if consumer.exact_evidence_ref != evidence.evidence_ref or evidence.geometry is None:
        raise FF01N10ECrossreadError("N10E consumer does not bind generated evidence")
    if evidence.raw_support != comp.raw_denominator_support:
        raise FF01N10ECrossreadError("N10E support denominator changed")
    if comp.producer_result is None or len(comp.producer_result.facts) != 1:
        raise FF01N10ECrossreadError("N10E did not actually retain direct I03 evidence")
    if comp.producer_result.facts[0].ref != comp.producer_fact_ref:
        raise FF01N10ECrossreadError("N10E fact ref contradicts actual direct I03 result")
    if n10e_empirical_query.ref != comp.producer_result.query_ref:
        raise FF01N10ECrossreadError("N10E direct I03 query was not executed as claimed")
    if (n10e_empirical_query.requested_output_grain.get("response_state_semantics_ref")
            != comp.producer_result.facts[0].response_state_semantics_ref):
        raise FF01N10ECrossreadError("N10E response-state meaning changed")

    exact_counts: dict[str, int] = {}
    conditioner_domain = {canonical_json(row["cell"][condition_index]) for row in material["complete_cells"]}
    if canonical_json(condition_value) not in conditioner_domain:
        raise FF01N10ECrossreadError("N10E predicate value outside exact FF01 domain")
    # Include every target-domain cell, including source-observed zeros.
    for row in material["complete_cells"]:
        exact_counts.setdefault(canonical_json(row["cell"][target_index]), 0)
    for row in material["complete_cells"]:
        if row["cell"][condition_index] == condition_value:
            key = canonical_json(row["cell"][target_index])
            exact_counts[key] += row["raw_support"]
    if comp.raw_denominator_support != sum(exact_counts.values()):
        raise FF01N10ECrossreadError("N10E condition-selected denominator differs from FF01 same-person slice")

    actual_n10e_counts: dict[str, int] = {}
    geometry = canonicalize(evidence.geometry)
    if geometry.get("denominator", {}).get("raw_denominator_support") != sum(exact_counts.values()):
        raise FF01N10ECrossreadError("N10E generated geometry contradicts FF01 denominator")
    for row in geometry.get("cells", ()):
        key = canonical_json(row["cell"])
        if key in actual_n10e_counts:
            raise FF01N10ECrossreadError("N10E generated duplicate target state")
        actual_n10e_counts[key] = row["raw_numerator_support"]
    if exact_counts != actual_n10e_counts:
        raise FF01N10ECrossreadError("FF01 complete joint and generated N10E target cells disagree")
    if sum(actual_n10e_counts.values()) != comp.producer_result.facts[0].raw_numerator_support:
        raise FF01N10ECrossreadError("N10E fact resolved-target total differs from actual cells")

    receipt = {
        "contract": CONTRACT,
        "claim_grade": CROSSREAD_GRADE,
        "ff01_ref": ff01.ref.as_dict(),
        "ff01_joint_fact_ref": material["producer_fact_ref"],
        "ff01_joint_query_ref": material["producer_query_ref"],
        "n10e_provider_ref": provider.receipt_ref.as_dict(),
        "n10e_provider_identity": provider.result_identity_hash,
        "n10e_composition_hash": comp.composed_result_identity_hash,
        "n10e_producer_fact_ref": comp.producer_fact_ref.as_dict(),
        "n10e_generated_evidence_ref": evidence.evidence_ref.as_dict(),
        "n10e_consumer_result_hash": consumer.result_hash,
        "source_release_ref": material["release_ref"],
        "source_risk_ref": material["risk_set_ref"],
        "conditioner_ref": conditioner.as_dict(),
        "conditioner_value": condition_value,
        "target_ref": target_ref.as_dict(),
        "raw_condition_denominator": sum(exact_counts.values()),
        "conserved_target_cells": [
            {"target_state": loads(key), "raw_numerator_support": n}
            for key, n in sorted(exact_counts.items())
        ],
        "residual_limits": list(LIMITS),
    }
    return FF01N10ECrossread(canonical_json(receipt), semantic_hash(receipt))


__all__ = [
    "CONTRACT", "CROSSREAD_GRADE", "FF01N10ECrossreadError",
    "FF01N10ECrossread", "conserve_ff01_n10e_actual_read",
]
