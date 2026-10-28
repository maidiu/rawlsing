"""Bounded SRC04 lane-D downstream consumer bridge.

This module consumes stable existing PRE553 native products only:
``C11LogicalRelease``, ``EmpiricalQuerySpec@1.0.0``,
``EmpiricalPredicate@1.0.0`` and ``EmpiricalFact@1.0.0``.  It never converts a
D1 descriptive tally into an ``EmpiricalFact`` and never opens SRC04 source
bytes.  The downstream recipient is the existing OC01 bounded-evidence
consumer in ``rawlsing_next.objective_consumer_bounded_evidence``.

Two modes are explicit:

* ``consume_native_producer`` -- real native producer bundle (release/query/
  predicate/repository/authority registry) through the existing
  ``execute_empirical_query``/``replay_empirical_query`` owners.
* ``consume_retained_b0_fixture`` -- the retained B0 SRC09 P0 nonrespondent
  fixture positive, used only as engineering evidence.  It is fixture/test-only
  and never claimed as a source-local SRC04 product.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from rawlsing_next.objective_consumer_bounded_evidence import (
    ClaimCeiling,
    EvidenceKind,
    EvidenceTier,
    ExactRef as PolicyExactRef,
    PolicyInput,
    evaluate_oc01_pre553_source_local,
)
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, C11Repository
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_effective_n import compute_effective_n
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    DiscoveryAuthority,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    authority_ref,
    exact_ref,
)
from rawlsing_next.pre553_empirical_query import (
    execute_empirical_query,
    replay_empirical_query,
)

B0_FIXTURE_SHA256 = "947b4950ade82dc7d1c5a80d5a2f2b54e7b918ce331e8e3ee1d64cbbd554c532"
B0_SCOPE = "SRC09_P0_NONRESPONDENT_FIXTURE_ONLY__NOT_ORIGINAL_NOT_SRC04"
D1_TALLY_SCHEMA_PREFIX = "PYAT_D1_SRC04_OBSERVED_SAMPLE_TALLY"
SOURCE_LOCAL_CLAIM = "SOURCE_LOCAL_STATISTIC"
SUPPORTED_COMPONENT_CLAIM = "SUPPORTED_COMPONENT_ONLY"
OBSERVED_RESPONSE_STATUS = "OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION"
OBSERVED_LEDGER_FIELDS = frozenset({
    "contract_ref",
    "risk_set_type",
    "denominator_policy",
    "condition_observation_policy",
    "not_eligible_population_estimate",
    "scoped_respondents",
    "target_observed",
    "target_unobserved",
    "condition_unobserved",
    "condition_false",
    "denominator",
    "resolved_targets",
    "unresolved_after_denominator",
    "risk_member_count",
    "denominator_member_count",
})


class ConsumerRefusal(ValueError):
    """Typed refusal before any consumer success is claimed."""

    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConsumerRefusal(f"{name.upper()}_REQUIRED")
    return value.strip()


def _sha(value: Any, name: str) -> str:
    text = _text(value, name)
    if len(text) != 64 or text.lower() != text or any(c not in "0123456789abcdef" for c in text):
        raise ConsumerRefusal(f"{name.upper()}_SHA256_REQUIRED")
    return text


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _sha_material(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _plain(value: Any) -> Any:
    """Convert immutable owner objects into JSON-safe evidence material."""
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    as_dict = getattr(value, "as_dict", None)
    if callable(as_dict):
        return _plain(as_dict())
    return value


def _native_ref(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Exception as exc:
        raise ConsumerRefusal("EXACT_REF_REQUIRED", f"{name}: {exc}") from exc


def _native_authority(value: Any, name: str) -> AuthorityRef:
    try:
        return authority_ref(value, name)
    except Exception as exc:
        raise ConsumerRefusal("AUTHORITY_REF_REQUIRED", f"{name}: {exc}") from exc


def _policy_ref(value: ExactRef) -> PolicyExactRef:
    return PolicyExactRef(value.kind, value.object_id, value.content_hash)


def _policy_authority(value: AuthorityRef) -> PolicyExactRef:
    return PolicyExactRef(
        "AUTHORITY_SNAPSHOT",
        f"urn:rawlsing:authority:{value.authority_id}:{value.authority_version}",
        value.authority_content_hash,
    )


def _policy_grade(value: Mapping[str, Any]) -> PolicyExactRef:
    """Exact policy-level identity of a retained authority-grade record.

    B0's retained fixture receipt carries grade records without native versions;
    this is deliberately a policy-record identity, not a claim that the native
    authority hash was resolved.
    """
    material = {
        "authority_id": value.get("authority_id"),
        "authority_kind": value.get("authority_kind"),
        "decision_state": value.get("decision_state"),
        "grade": value.get("grade"),
        "retained_by": "B0_FIXTURE_POSITIVE",
    }
    digest = _sha_material(material)
    return PolicyExactRef(
        "AUTHORITY_GRADE_RECORD",
        f"urn:rawlsing:campaign-b0:authority-grade:{value.get('authority_id')}",
        digest,
    )


@dataclass(frozen=True)
class ProducerContract:
    source_id: str
    source_sha256: str
    source_rows: int
    release_ref: ExactRef
    query_ref: ExactRef
    predicate_ref: ExactRef
    fact_ref: ExactRef
    producer_family: tuple[str, ...]
    evidence_tier: str
    claim_ceiling: str
    use_scopes: tuple[str, ...]
    native_authority_refs: tuple[AuthorityRef, ...] = ()
    policy_authority_refs: tuple[PolicyExactRef, ...] = ()
    fixture_only: bool = False

    def __post_init__(self) -> None:
        _text(self.source_id, "source_id")
        _sha(self.source_sha256, "source_sha256")
        if not isinstance(self.source_rows, int) or isinstance(self.source_rows, bool) or self.source_rows < 1:
            raise ConsumerRefusal("SOURCE_ROWS_REQUIRED")
        for name in ("release_ref", "query_ref", "predicate_ref", "fact_ref"):
            if not isinstance(getattr(self, name), ExactRef):
                raise ConsumerRefusal(f"{name.upper()}_EXACT_REF_REQUIRED")
        if not self.producer_family:
            raise ConsumerRefusal("PRODUCER_FAMILY_REQUIRED")
        if self.evidence_tier not in {x.value for x in EvidenceTier}:
            raise ConsumerRefusal("EVIDENCE_TIER_INVALID", self.evidence_tier)
        if self.claim_ceiling not in {x.value for x in ClaimCeiling}:
            raise ConsumerRefusal("CLAIM_CEILING_INVALID", self.claim_ceiling)
        if not self.use_scopes:
            raise ConsumerRefusal("USE_SCOPE_REQUIRED")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_sha256": self.source_sha256,
            "source_rows": self.source_rows,
            "release_ref": self.release_ref.as_dict(),
            "query_ref": self.query_ref.as_dict(),
            "predicate_ref": self.predicate_ref.as_dict(),
            "fact_ref": self.fact_ref.as_dict(),
            "producer_family": list(self.producer_family),
            "evidence_tier": self.evidence_tier,
            "claim_ceiling": self.claim_ceiling,
            "use_scopes": list(self.use_scopes),
            "native_authority_refs": [x.as_dict() for x in self.native_authority_refs],
            "policy_authority_refs": [x.as_dict() for x in self.policy_authority_refs],
            "fixture_only": self.fixture_only,
        }


@dataclass(frozen=True)
class DiscoveryConsumer:
    """Exact existing discovery owner inputs for substantive value consumption.

    The wrapper does not implement discovery.  It invokes
    ``rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery`` with
    the exact authority, predicates and query templates supplied by the producer.
    """

    authority: DiscoveryAuthority
    authority_snapshot: Any
    predicate_catalog: tuple[EmpiricalPredicate, ...]
    query_template_catalog: tuple[EmpiricalQuerySpec, ...]
    scope: str

    def __post_init__(self) -> None:
        if not isinstance(self.authority, DiscoveryAuthority):
            raise ConsumerRefusal("DISCOVERY_AUTHORITY_REQUIRED")
        if self.authority_snapshot is None:
            raise ConsumerRefusal("DISCOVERY_AUTHORITY_SNAPSHOT_REQUIRED")
        if not self.predicate_catalog or not self.query_template_catalog:
            raise ConsumerRefusal("DISCOVERY_CATALOG_REQUIRED")
        _text(self.scope, "discovery_scope")


@dataclass(frozen=True)
class ProducerBundle:
    release: C11LogicalRelease
    query: EmpiricalQuerySpec
    predicate: EmpiricalPredicate
    repository: C11Repository
    authority_registry: AuthorityRegistry
    contract: ProducerContract
    discovery: DiscoveryConsumer | None = None
    weight_facts: tuple[Any, ...] = ()
    authorized_weight_scope_ref: ExactRef | None = None


def _producer_family_refused(contract: ProducerContract) -> None:
    joined = " ".join(contract.producer_family).lower()
    if "d1" in joined or "tally" in joined:
        raise ConsumerRefusal(
            "PRODUCER_FAMILY_REFUSED__D1_TALLY_NOT_EMPIRICAL_FACT",
            "the D1 descriptive tally is not an EmpiricalFact and is never converted",
        )
    required = {
        "C11LogicalRelease",
        "EmpiricalQuerySpec@1.0.0",
        "EmpiricalPredicate@1.0.0",
        "EmpiricalFact@1.0.0",
    }
    if not required.issubset(set(contract.producer_family)):
        raise ConsumerRefusal(
            "PRODUCER_FAMILY_INCOMPLETE",
            f"required {sorted(required)}; got {sorted(contract.producer_family)}",
        )


def validate_contract(
    contract: ProducerContract,
    *,
    expected_source_id: str,
    requested_claim_ceiling: str,
    use_scope: str,
) -> None:
    _producer_family_refused(contract)
    if contract.source_id != expected_source_id:
        raise ConsumerRefusal("WRONG_SOURCE_ID", f"{contract.source_id}!={expected_source_id}")
    if contract.release_ref.kind != "C11LogicalRelease":
        raise ConsumerRefusal("WRONG_RELEASE_KIND", contract.release_ref.kind)
    if contract.query_ref.kind != "EmpiricalQuerySpec@1.0.0":
        raise ConsumerRefusal("WRONG_QUERY_KIND", contract.query_ref.kind)
    if contract.predicate_ref.kind != "EmpiricalPredicate@1.0.0":
        raise ConsumerRefusal("WRONG_PREDICATE_KIND", contract.predicate_ref.kind)
    if contract.fact_ref.kind != "EmpiricalFact@1.0.0":
        raise ConsumerRefusal("WRONG_FACT_KIND", contract.fact_ref.kind)
    if not contract.native_authority_refs and not contract.policy_authority_refs:
        raise ConsumerRefusal("MISSING_AUTHORITY")
    if use_scope not in contract.use_scopes:
        raise ConsumerRefusal("WRONG_USE_SCOPE", f"{use_scope} not in {contract.use_scopes}")
    if requested_claim_ceiling != contract.claim_ceiling:
        raise ConsumerRefusal(
            "CLAIM_CEILING_NOT_AUTHORIZED",
            f"{requested_claim_ceiling}!={contract.claim_ceiling}",
        )
    if contract.fixture_only and requested_claim_ceiling != SUPPORTED_COMPONENT_CLAIM:
        raise ConsumerRefusal(
            "FIXTURE_AUTHORITY_CANNOT_CLAIM_SOURCE_LOCAL",
            "fixture/test-only evidence requires SUPPORTED_COMPONENT_ONLY",
        )
    if not contract.fixture_only and contract.evidence_tier != EvidenceTier.SOURCE_LOCAL_CERTIFIED.value:
        raise ConsumerRefusal(
            "SOURCE_LOCAL_EVIDENCE_TIER_REQUIRED",
            contract.evidence_tier,
        )
    if not contract.fixture_only and not contract.native_authority_refs:
        raise ConsumerRefusal("NATIVE_AUTHORITY_REFS_REQUIRED")


def _oc01_receipt(
    *,
    contract: ProducerContract,
    producer_ref: ExactRef,
    authority_refs: Iterable[PolicyExactRef],
    requested_claim_ceiling: str,
    partial_allowed: bool,
) -> Mapping[str, Any]:
    ceiling = ClaimCeiling(requested_claim_ceiling)
    tier = EvidenceTier(contract.evidence_tier)
    inp = PolicyInput(
        input_id=f"{contract.source_id}:{producer_ref.object_id}",
        required=True,
        available=True,
        evidence_kind=EvidenceKind.EMPIRICAL,
        evidence_tier=tier,
        claim_ceiling=ceiling,
        producer_ref=_policy_ref(producer_ref),
        authority_refs=tuple(authority_refs),
    )
    receipt = evaluate_oc01_pre553_source_local(
        operation_id=contract.query_ref.object_id,
        inputs=[inp],
        requested_claim_ceiling=ceiling,
        partial_allowed=partial_allowed,
    )
    payload = receipt.as_dict()
    if payload["state"] != "SUPPORTED_OBJECTIVE_RESULT" or not payload["positive_completion"]:
        raise ConsumerRefusal(
            "OC01_NOT_POSITIVE",
            f"state={payload['state']} reasons={payload['refusal_reasons']}",
        )
    return payload


def _query_observed_contract_ref(query: EmpiricalQuerySpec) -> ExactRef | None:
    grain = query.requested_output_grain
    if not isinstance(grain, Mapping):
        return None
    raw = grain.get("observed_response_contract_ref")
    if raw is None:
        return None
    return _native_ref(raw, "query.observed_response_contract_ref")


def _observed_response_projection(
    fact: EmpiricalFact,
    query: EmpiricalQuerySpec,
) -> dict[str, Any] | None:
    """Preserve the exact observed-response projection required by the query grain.

    Non-observed profiles return ``None`` and keep their existing behavior.  An
    observed profile must carry the exact status, non-population flag, contract
    ref and full ledger produced by the existing C/I03 owner; this wrapper does
    not synthesize or relabel any observed material.
    """
    expected_ref = _query_observed_contract_ref(query)
    topology = getattr(fact, "target_topology", None)
    projection = (
        topology.get("observed_response")
        if isinstance(topology, Mapping)
        else None
    )
    if expected_ref is None:
        if projection is not None:
            raise ConsumerRefusal(
                "OBSERVED_RESPONSE_PROJECTION_WITHOUT_QUERY_GRAIN",
                "fact carries observed_response but query grain has no observed-response contract",
            )
        return None
    if not isinstance(projection, Mapping):
        raise ConsumerRefusal(
            "OBSERVED_RESPONSE_PROJECTION_MISSING",
            "observed-response query grain requires target_topology.observed_response",
        )
    if projection.get("status") != OBSERVED_RESPONSE_STATUS:
        raise ConsumerRefusal(
            "OBSERVED_RESPONSE_STATUS_INVALID",
            str(projection.get("status")),
        )
    if projection.get("not_eligible_population_estimate") is not True:
        raise ConsumerRefusal(
            "OBSERVED_RESPONSE_POPULATION_CLAIM_REFUSED",
            "observed-response projection must not be an eligible population estimate",
        )
    try:
        projection_ref = _native_ref(
            projection.get("contract_ref"), "observed_response.contract_ref"
        )
    except ConsumerRefusal as exc:
        raise ConsumerRefusal(
            "OBSERVED_RESPONSE_CONTRACT_REF_INVALID", exc.detail
        ) from exc
    if projection_ref.key != expected_ref.key:
        raise ConsumerRefusal(
            "OBSERVED_RESPONSE_CONTRACT_REF_MISMATCH",
            f"{projection_ref.key}!={expected_ref.key}",
        )
    ledger = projection.get("ledger")
    if not isinstance(ledger, Mapping):
        raise ConsumerRefusal(
            "OBSERVED_RESPONSE_LEDGER_MISSING",
            "observed-response projection requires a full ledger",
        )
    missing = sorted(OBSERVED_LEDGER_FIELDS - set(ledger))
    if missing:
        raise ConsumerRefusal(
            "OBSERVED_RESPONSE_LEDGER_INCOMPLETE",
            f"missing {missing}",
        )
    try:
        ledger_ref = _native_ref(
            ledger.get("contract_ref"), "observed_response.ledger.contract_ref"
        )
    except ConsumerRefusal as exc:
        raise ConsumerRefusal(
            "OBSERVED_RESPONSE_LEDGER_CONTRACT_REF_INVALID", exc.detail
        ) from exc
    if ledger_ref.key != expected_ref.key:
        raise ConsumerRefusal(
            "OBSERVED_RESPONSE_LEDGER_CONTRACT_REF_MISMATCH",
            f"{ledger_ref.key}!={expected_ref.key}",
        )
    if ledger.get("not_eligible_population_estimate") is not True:
        raise ConsumerRefusal(
            "OBSERVED_RESPONSE_LEDGER_POPULATION_CLAIM_REFUSED",
            "observed-response ledger must not be an eligible population estimate",
        )
    return _plain(projection)


def _run_downstream_discovery(
    bundle: ProducerBundle,
    contract: ProducerContract,
) -> dict[str, Any] | None:
    discovery = bundle.discovery
    if discovery is None:
        return None
    try:
        result = execute_exact_bounded_discovery(
            repository=bundle.repository,
            discovery_authority=discovery.authority,
            authority_registry=bundle.authority_registry,
            release_refs=(contract.release_ref,),
            predicate_catalog=discovery.predicate_catalog,
            query_template_catalog=discovery.query_template_catalog,
        )
    except Exception as exc:  # noqa: BLE001 - report the exact owner failure
        raise ConsumerRefusal(
            "DOWNSTREAM_DISCOVERY_REFUSED",
            f"{type(exc).__name__}: {exc}",
        ) from exc
    supported = sum(
        1 for receipt in result.receipts
        if receipt.typed_state == "DISCOVERED_RESULT_SUPPORTED"
    )
    if supported < 1:
        raise ConsumerRefusal(
            "DOWNSTREAM_DISCOVERY_NOT_POSITIVE",
            f"supported_candidates={supported}",
        )
    queries = {query.ref.key: query for query in result.executed_queries}
    facts = []
    for fact in result.empirical_facts:
        query = queries.get(exact_ref(fact.empirical_query_spec_ref).key)
        if query is None:
            raise ConsumerRefusal(
                "DOWNSTREAM_DISCOVERY_QUERY_MISSING",
                fact.ref.key,
            )
        topology = fact.target_topology if isinstance(fact.target_topology, Mapping) else {}
        observed_response = _observed_response_projection(fact, query)
        item = {
            "fact_ref": fact.ref.as_dict(),
            "typed_state": fact.typed_state,
            "raw_numerator_support": fact.raw_numerator_support,
            "raw_denominator_support": fact.raw_denominator_support,
            "cells": _plain(topology.get("complete_cell_semantic_projection", ())),
        }
        if observed_response is not None:
            item["observed_response"] = observed_response
        facts.append(item)
    receipts = []
    for receipt in result.receipts:
        candidate = receipt.candidate_identity if isinstance(receipt.candidate_identity, Mapping) else {}
        receipts.append({
            "receipt_ref": receipt.ref.as_dict(),
            "typed_state": receipt.typed_state,
            "coverage_state": receipt.coverage_state,
            "candidate_id": candidate.get("candidate_id"),
            "candidate_hash": candidate.get("candidate_hash"),
            "family": candidate.get("family"),
            "rule_id": candidate.get("rule_id"),
            "validation": _plain(candidate.get("validation")),
            "empirical_fact_refs": [_plain(ref) for ref in receipt.empirical_fact_refs],
            "support_uncertainty_state": _plain(receipt.support_uncertainty_state),
        })
    return {
        "owner": "rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery",
        "status": "SUBSTANTIVE_DOWNSTREAM_DISCOVERY_POSITIVE",
        "scope": discovery.scope,
        "authority_ref": discovery.authority.ref.as_dict(),
        "authority_snapshot_ref": discovery.authority_snapshot.authority_ref.as_dict(),
        "candidate_count": result.candidate_count,
        "covered_candidate_count": result.covered_candidate_count,
        "coverage_claim": result.coverage_claim,
        "supported_candidate_count": supported,
        "valid_empty": result.valid_empty,
        "empirical_fact_refs": [_plain(ref) for ref in result.empirical_fact_refs],
        "empirical_facts": facts,
        "receipts": receipts,
        "effect": "DISTRIBUTION_DIFFERS_FROM_BASELINE",
        "diagnostic_or_ranking_effect": False,
        "structural_or_ff_adoption": False,
    }


def _validate_value_sensitivity(
    evidence: Mapping[str, Any] | None,
    *,
    case: str | None,
    fixture_only: bool,
    contract: ProducerContract,
    fact: EmpiricalFact,
    discovery: Mapping[str, Any] | None,
) -> dict[str, Any]:
    expected_scope = "NONRESPONDENT_FIXTURE_ONLY" if fixture_only else "SOURCE_LOCAL_CERTIFIED"
    if evidence is None:
        return {
            "schema": "PYAT_SRC04_LANE_D_VALUE_SENSITIVITY@1.0.0",
            "status": "NOT_DEMONSTRATED",
            "scope": expected_scope,
            "measured": False,
            "changed": False,
            "restored": False,
            "case": case,
        }
    if not isinstance(evidence, Mapping):
        raise ConsumerRefusal("VALUE_SENSITIVITY_EVIDENCE_INVALID")
    if evidence.get("schema") != "PYAT_SRC04_LANE_D_VALUE_SENSITIVITY@1.0.0":
        raise ConsumerRefusal("VALUE_SENSITIVITY_SCHEMA_MISMATCH")
    if evidence.get("scope") != expected_scope:
        raise ConsumerRefusal("VALUE_SENSITIVITY_SCOPE_MISMATCH")
    if evidence.get("measured") is not True or evidence.get("changed") is not True:
        raise ConsumerRefusal("VALUE_SENSITIVITY_NOT_MEASURED_POSITIVE")
    if evidence.get("restored") is not True:
        raise ConsumerRefusal("VALUE_SENSITIVITY_RESTORE_NOT_PROVEN")
    original = evidence.get("original")
    mutated = evidence.get("mutated")
    restored_result = evidence.get("restored_result")
    if not all(isinstance(item, Mapping) for item in (original, mutated, restored_result)):
        raise ConsumerRefusal("VALUE_SENSITIVITY_COMPARISON_REQUIRED")
    if _plain(original) == _plain(mutated):
        raise ConsumerRefusal("VALUE_SENSITIVITY_NO_CHANGE")
    if _plain(restored_result) != _plain(original):
        raise ConsumerRefusal("VALUE_SENSITIVITY_RESTORE_MISMATCH")
    if case not in {"original", "mutated", "restored"}:
        raise ConsumerRefusal("VALUE_SENSITIVITY_CASE_REQUIRED")
    result_key = "restored_result" if case == "restored" else case
    observed = evidence.get(result_key)
    if not isinstance(observed, Mapping):
        raise ConsumerRefusal("VALUE_SENSITIVITY_RESULT_MISSING", result_key)
    if _plain(observed.get("fact_ref")) != contract.fact_ref.as_dict():
        raise ConsumerRefusal("VALUE_SENSITIVITY_FACT_MISMATCH", result_key)
    if observed.get("raw_numerator_support") != fact.raw_numerator_support:
        raise ConsumerRefusal("VALUE_SENSITIVITY_NUMERATOR_MISMATCH", result_key)
    if observed.get("raw_denominator_support") != fact.raw_denominator_support:
        raise ConsumerRefusal("VALUE_SENSITIVITY_DENOMINATOR_MISMATCH", result_key)
    if discovery is not None:
        if observed.get("discovery_supported_candidate_count") != discovery["supported_candidate_count"]:
            raise ConsumerRefusal("VALUE_SENSITIVITY_DISCOVERY_STATE_MISMATCH", result_key)
        expected_refs = [ref["content_hash"] for ref in discovery["empirical_fact_refs"]]
        observed_refs = observed.get("discovery_empirical_fact_refs")
        if not isinstance(observed_refs, list) or observed_refs != expected_refs:
            raise ConsumerRefusal("VALUE_SENSITIVITY_DISCOVERY_FACT_MISMATCH", result_key)
    return {
        "schema": "PYAT_SRC04_LANE_D_VALUE_SENSITIVITY@1.0.0",
        "status": "MEASURED_FIXTURE_ONLY" if fixture_only else "MEASURED_SOURCE_LOCAL",
        "scope": expected_scope,
        "measured": True,
        "changed": True,
        "restored": True,
        "case": case,
        "upstream_change": evidence.get("upstream_change"),
        "original": _plain(evidence.get("original")),
        "mutated": _plain(evidence.get("mutated")),
        "restored_result": _plain(evidence.get("restored_result")),
    }


def consume_native_producer(
    bundle: ProducerBundle,
    *,
    expected_source_id: str,
    requested_claim_ceiling: str = SOURCE_LOCAL_CLAIM,
    use_scope: str = SOURCE_LOCAL_CLAIM,
    replay: bool = True,
    allow_fixture_engineering: bool = False,
    value_sensitivity_evidence: Mapping[str, Any] | None = None,
    value_sensitivity_case: str | None = None,
) -> dict[str, Any]:
    if not isinstance(bundle, ProducerBundle):
        raise ConsumerRefusal("PRODUCER_BUNDLE_REQUIRED")
    contract = bundle.contract
    validate_contract(
        contract,
        expected_source_id=expected_source_id,
        requested_claim_ceiling=requested_claim_ceiling,
        use_scope=use_scope,
    )
    if contract.fixture_only and not allow_fixture_engineering:
        raise ConsumerRefusal(
            "FIXTURE_NATIVE_PATH_REQUIRES_ENGINEERING_LABEL",
            "fixture-native execution must be explicitly labelled engineering-only",
        )
    if bundle.release.source_artifact_ref.content_hash != contract.source_sha256:
        raise ConsumerRefusal("NATIVE_SOURCE_IDENTITY_MISMATCH")
    if bundle.release.release_ref.key != contract.release_ref.key:
        raise ConsumerRefusal("WRONG_RELEASE_IDENTITY")
    if bundle.query.ref.key != contract.query_ref.key:
        raise ConsumerRefusal("WRONG_QUERY_IDENTITY")
    if bundle.predicate.ref.key != contract.predicate_ref.key:
        raise ConsumerRefusal("WRONG_PREDICATE_IDENTITY")
    if exact_ref(bundle.query.condition_predicate_ref).key != contract.predicate_ref.key:
        raise ConsumerRefusal("QUERY_PREDICATE_MISMATCH")
    result = execute_empirical_query(
        repository=bundle.repository,
        query=bundle.query,
        predicate=bundle.predicate,
        authority_registry=bundle.authority_registry,
        release_refs=(contract.release_ref,),
    )
    facts = {fact.ref.key: fact for fact in result.facts}
    if set(facts) != {contract.fact_ref.key}:
        raise ConsumerRefusal(
            "FACT_SET_MISMATCH",
            f"expected only {contract.fact_ref.key}; got {sorted(facts)}",
        )
    fact = facts[contract.fact_ref.key]
    if fact.typed_state != "SUPPORTED":
        raise ConsumerRefusal("FACT_NOT_SUPPORTED", fact.typed_state)
    if fact.raw_denominator_support <= 0 or fact.raw_numerator_support > fact.raw_denominator_support:
        raise ConsumerRefusal("FACT_SUPPORT_INVALID")
    if exact_ref(fact.empirical_query_spec_ref).key != contract.query_ref.key:
        raise ConsumerRefusal("FACT_QUERY_IDENTITY_MISMATCH")
    if exact_ref(fact.condition_predicate_ref).key != contract.predicate_ref.key:
        raise ConsumerRefusal("FACT_PREDICATE_MISMATCH")
    if contract.release_ref.key not in {exact_ref(x).key for x in fact.source_empirical_provenance_refs}:
        raise ConsumerRefusal("FACT_RELEASE_PROVENANCE_MISSING")
    fact_authorities = {x.key: x for x in fact.authority_snapshot_refs}
    for ref in contract.native_authority_refs:
        if ref.key not in fact_authorities:
            raise ConsumerRefusal("CONTRACT_AUTHORITY_NOT_IN_FACT", ref.key)
        bundle.authority_registry.resolve_exact(ref)
    if replay:
        replay_empirical_query(
            repository=bundle.repository,
            query=bundle.query,
            predicate=bundle.predicate,
            authority_registry=bundle.authority_registry,
            release_refs=(contract.release_ref,),
            expected_fact_refs=(contract.fact_ref,),
        )
    observed_response = _observed_response_projection(fact, bundle.query)
    try:
        effective_n = compute_effective_n(
            fact=fact,
            query=bundle.query,
            weight_facts=bundle.weight_facts,
            authority_registry=bundle.authority_registry,
            release_refs=(contract.release_ref,),
            authorized_weight_scope_ref=bundle.authorized_weight_scope_ref,
        )
    except Exception as exc:  # noqa: BLE001 - report the exact owner failure
        raise ConsumerRefusal(
            "DOWNSTREAM_EFFECTIVE_N_REFUSED",
            f"{type(exc).__name__}: {exc}",
        ) from exc
    effective_n_document = _plain(effective_n.as_dict())
    discovery_document = _run_downstream_discovery(bundle, contract)
    if discovery_document is not None:
        downstream_owner = discovery_document["owner"]
        downstream_effect = "SUBSTANTIVE_DISCOVERY_RESULT_SUPPORTED"
    elif effective_n.typed_state == "SUPPORTED":
        downstream_owner = "rawlsing_next.pre553_effective_n.compute_effective_n"
        downstream_effect = "EFFECTIVE_N_SUPPORTED"
    else:
        raise ConsumerRefusal(
            "DOWNSTREAM_VALUE_CONSUMER_REQUIRED",
            f"no discovery product and effective-N is {effective_n.typed_state}; "
            "policy admission alone is not an empirical value effect",
        )
    if not contract.fixture_only and downstream_effect not in {
        "SUBSTANTIVE_DISCOVERY_RESULT_SUPPORTED",
        "EFFECTIVE_N_SUPPORTED",
    }:
        raise ConsumerRefusal("DOWNSTREAM_VALUE_EFFECT_NOT_SUBSTANTIVE", downstream_effect)
    sensitivity = _validate_value_sensitivity(
        value_sensitivity_evidence,
        case=value_sensitivity_case,
        fixture_only=contract.fixture_only,
        contract=contract,
        fact=fact,
        discovery=discovery_document,
    )
    measured = sensitivity.get("measured") is True and sensitivity.get("changed") is True
    source_value_sensitive = bool(not contract.fixture_only and measured)
    fixture_value_sensitive = bool(contract.fixture_only and measured)
    receipt = _oc01_receipt(
        contract=contract,
        producer_ref=fact.ref,
        authority_refs=(_policy_authority(x) for x in authority_fact_values(fact)),
        requested_claim_ceiling=requested_claim_ceiling,
        partial_allowed=True,
    )
    status = (
        "FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE"
        if contract.fixture_only
        else "SOURCE_LOCAL_NATIVE_CONSUMER_POSITIVE"
    )
    limits = [
        "Native execution is through the existing I03 and value-consuming downstream owners.",
        "No D1 tally was converted into EmpiricalFact.",
        "No FF/V553 semantic adoption, population or weight claim was made.",
    ]
    if contract.fixture_only:
        limits.insert(0, "Nonrespondent/test-only B0 SRC09 fixture; not original SRC04 and not source-local proof.")
        limits.append("Effective-N is NOT_APPLICABLE for the RAW fixture grain; discovery supplies the substantive value effect.")
    else:
        limits.append("Source-local claim remains pending actual original-source producer issuance and value-sensitivity proof.")
    if observed_response is not None:
        limits.append(
            "Observed-response status, contract ref and full ledger are preserved unchanged; "
            "the projection is not an eligible population estimate."
        )
    product = {
        "schema": "PYAT_SRC04_LANE_D_CONSUMER_PRODUCT@1.1.0",
        "status": status,
        "source_id": contract.source_id,
        "source_sha256": contract.source_sha256,
        "source_rows": contract.source_rows,
        "release_ref": contract.release_ref.as_dict(),
        "query_ref": contract.query_ref.as_dict(),
        "predicate_ref": contract.predicate_ref.as_dict(),
        "fact_ref": contract.fact_ref.as_dict(),
        "fact_typed_state": fact.typed_state,
        "raw_numerator_support": fact.raw_numerator_support,
        "raw_denominator_support": fact.raw_denominator_support,
        "support_rate": {"numerator": fact.raw_numerator_support, "denominator": fact.raw_denominator_support},
        "contract": contract.to_dict(),
        "oc01_receipt": receipt,
        "native_execution": True,
        "downstream_value_consumer": downstream_owner,
        "downstream_value_effect": downstream_effect,
        "downstream_discovery": discovery_document,
        "effective_n_product": effective_n_document,
        "fixture_only": contract.fixture_only,
        "source_local_claim": not contract.fixture_only,
        "source_value_sensitive": source_value_sensitive,
        "fixture_value_sensitive": fixture_value_sensitive,
        "value_sensitivity": sensitivity,
        "canonical_values_emitted": 0,
        "population_claim": False,
        "weights_used": bool(bundle.weight_facts),
        "ff_v553_adoption": False,
        "limits": limits,
    }
    if observed_response is not None:
        product["observed_response"] = observed_response
    return product


def authority_fact_values(fact: EmpiricalFact) -> tuple[AuthorityRef, ...]:
    return tuple(fact.authority_snapshot_refs)


def b0_fixture_contract(receipt: Mapping[str, Any]) -> ProducerContract:
    """Build the exact policy contract for the retained B0 fixture receipt."""
    if receipt.get("schema") != "PYAT_CAMPAIGN_B0_QUALIFIED_FIXTURE_POSITIVE@1.0.0":
        raise ConsumerRefusal("B0_RECEIPT_SCHEMA_MISMATCH")
    if receipt.get("scope") != B0_SCOPE:
        raise ConsumerRefusal("B0_SCOPE_MISMATCH", str(receipt.get("scope")))
    if receipt.get("fixture_only", True) is not True and receipt.get("scope") != B0_SCOPE:
        raise ConsumerRefusal("B0_FIXTURE_SCOPE_REQUIRED")
    if receipt.get("original_source_or_release_read") is not False:
        raise ConsumerRefusal("B0_ORIGINAL_READ_FLAG_INVALID")
    if receipt.get("test_only_query_authority_used") is not True:
        raise ConsumerRefusal("B0_TEST_ONLY_AUTHORITY_REQUIRED")
    if receipt.get("product_positive") is not True:
        raise ConsumerRefusal("B0_PRODUCT_NOT_POSITIVE")
    execution = receipt.get("execution") or {}
    if execution.get("status") != "EXECUTED_SUPPORTED" or execution.get("fact_count") != 1:
        raise ConsumerRefusal("B0_EXECUTION_NOT_SUPPORTED")
    if execution.get("typed_states") != ["SUPPORTED"]:
        raise ConsumerRefusal("B0_TYPED_STATE_INVALID")
    numerator = execution.get("raw_numerator_support")
    denominator = execution.get("raw_denominator_support")
    if not (isinstance(numerator, list) and len(numerator) == 1 and isinstance(denominator, list) and len(denominator) == 1):
        raise ConsumerRefusal("B0_SUPPORT_VECTOR_INVALID")
    if numerator[0] <= 0 or numerator[0] != denominator[0]:
        raise ConsumerRefusal("B0_SUPPORT_NOT_POSITIVE")
    grades = receipt.get("authority_grades") or []
    if not grades:
        raise ConsumerRefusal("B0_AUTHORITY_GRADES_MISSING")
    return ProducerContract(
        source_id="SRC09",
        source_sha256=_sha(receipt.get("fixture_source_sha256"), "fixture_source_sha256"),
        source_rows=int((receipt.get("independent_count_check") or {}).get("source_fixture_rows") or 0),
        release_ref=_native_ref(receipt.get("fixture_release_ref"), "fixture_release_ref"),
        query_ref=_native_ref(receipt.get("query_ref"), "query_ref"),
        predicate_ref=_native_ref(receipt.get("predicate_ref"), "predicate_ref"),
        fact_ref=_native_ref(execution.get("fact_ref"), "fact_ref"),
        producer_family=("C11LogicalRelease", "EmpiricalQuerySpec@1.0.0", "EmpiricalPredicate@1.0.0", "EmpiricalFact@1.0.0"),
        evidence_tier=EvidenceTier.PARTIAL_AUTHORITY.value,
        claim_ceiling=ClaimCeiling.SUPPORTED_COMPONENT_ONLY.value,
        use_scopes=(SUPPORTED_COMPONENT_CLAIM,),
        policy_authority_refs=tuple(_policy_grade(x) for x in grades),
        fixture_only=True,
    )


def consume_retained_receipt(
    receipt: Mapping[str, Any],
    contract: ProducerContract,
    *,
    expected_source_id: str = "SRC09",
    requested_claim_ceiling: str = SUPPORTED_COMPONENT_CLAIM,
    use_scope: str = SUPPORTED_COMPONENT_CLAIM,
) -> dict[str, Any]:
    """Consume a retained nonrespondent producer receipt under an exact contract.

    No native re-execution is claimed here.  The receipt's exact fact/release
    identity is checked, and the existing OC01 consumer policy is invoked.
    """
    validate_contract(
        contract,
        expected_source_id=expected_source_id,
        requested_claim_ceiling=requested_claim_ceiling,
        use_scope=use_scope,
    )
    if not contract.fixture_only:
        raise ConsumerRefusal("RETAINED_RECEIPT_REQUIRES_FIXTURE_SCOPE")
    execution = receipt.get("execution") or {}
    checks = {
        "release_ref": contract.release_ref.key == _native_ref(receipt.get("fixture_release_ref"), "fixture_release_ref").key,
        "query_ref": contract.query_ref.key == _native_ref(receipt.get("query_ref"), "query_ref").key,
        "predicate_ref": contract.predicate_ref.key == _native_ref(receipt.get("predicate_ref"), "predicate_ref").key,
        "fact_ref": contract.fact_ref.key == _native_ref(execution.get("fact_ref"), "fact_ref").key,
        "source_sha256": contract.source_sha256 == _sha(receipt.get("fixture_source_sha256"), "fixture_source_sha256"),
    }
    for name, ok in checks.items():
        if not ok:
            raise ConsumerRefusal(f"RETAINED_{name.upper()}_MISMATCH")
    if not contract.policy_authority_refs:
        raise ConsumerRefusal("MISSING_AUTHORITY")
    receipt_oc01 = _oc01_receipt(
        contract=contract,
        producer_ref=contract.fact_ref,
        authority_refs=contract.policy_authority_refs,
        requested_claim_ceiling=SUPPORTED_COMPONENT_CLAIM,
        partial_allowed=True,
    )
    numerator = execution["raw_numerator_support"][0]
    denominator = execution["raw_denominator_support"][0]
    return {
        "schema": "PYAT_SRC04_LANE_D_CONSUMER_PRODUCT@1.0.0",
        "status": "FIXTURE_ONLY_ENGINEERING_POSITIVE__NOT_SOURCE_LOCAL_PROOF",
        "source_id": contract.source_id,
        "source_sha256": contract.source_sha256,
        "source_rows": contract.source_rows,
        "release_ref": contract.release_ref.as_dict(),
        "query_ref": contract.query_ref.as_dict(),
        "predicate_ref": contract.predicate_ref.as_dict(),
        "fact_ref": contract.fact_ref.as_dict(),
        "fact_typed_state": execution["typed_states"][0],
        "raw_numerator_support": numerator,
        "raw_denominator_support": denominator,
        "support_rate": {"numerator": numerator, "denominator": denominator},
        "contract": contract.to_dict(),
        "oc01_receipt": receipt_oc01,
        "native_execution": False,
        "retained_b0_receipt": True,
        "retained_b0_scope": B0_SCOPE,
        "fixture_only": True,
        "source_value_sensitive": False,
        "source_local_claim": False,
        "canonical_values_emitted": 0,
        "population_claim": False,
        "weights_used": False,
        "ff_v553_adoption": False,
        "limits": [
            "Retained B0 SRC09 P0 nonrespondent/test-only fixture positive, used only for engineering wiring.",
            "Not an SRC04 source-local product; no source-value-sensitive original proof is claimed.",
            "No D1 tally was converted into EmpiricalFact.",
        ],
    }


def consume_retained_b0_fixture(
    path: str | Path,
    *,
    expected_source_id: str = "SRC09",
    requested_claim_ceiling: str = SUPPORTED_COMPONENT_CLAIM,
    use_scope: str = SUPPORTED_COMPONENT_CLAIM,
) -> dict[str, Any]:
    path = Path(path)
    try:
        raw = path.read_bytes()
        receipt = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ConsumerRefusal("B0_RECEIPT_UNREADABLE", str(exc)) from exc
    digest = hashlib.sha256(raw).hexdigest()
    if digest != B0_FIXTURE_SHA256:
        raise ConsumerRefusal("B0_RECEIPT_SHA_MISMATCH", digest)
    contract = b0_fixture_contract(receipt)
    product = consume_retained_receipt(
        receipt,
        contract,
        expected_source_id=expected_source_id,
        requested_claim_ceiling=requested_claim_ceiling,
        use_scope=use_scope,
    )
    product["retained_b0_receipt_sha256"] = digest
    return product


def refuse_d1_tally(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    try:
        raw = path.read_bytes()
        tally = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ConsumerRefusal("D1_TALLY_UNREADABLE", str(exc)) from exc
    schema = str(tally.get("schema") or "")
    field_count = tally.get("field_count")
    is_ref = schema == "PYAT_SRC04_LANE_D_D1_TALLY_REF@1.0.0"
    is_full = schema.startswith(D1_TALLY_SCHEMA_PREFIX) or (
        isinstance(field_count, int) and "fields" in tally
    )
    if not (is_ref or is_full):
        raise ConsumerRefusal("D1_TALLY_IDENTITY_MISMATCH", schema)
    return {
        "schema": "PYAT_SRC04_LANE_D_NEGATIVE@1.0.0",
        "negative_id": "D1_TALLY_IS_NOT_EMPIRICAL_FACT",
        "status": "REFUSED",
        "error_type": "ConsumerRefusal",
        "error_code": "PRODUCER_FAMILY_REFUSED__D1_TALLY_NOT_EMPIRICAL_FACT",
        "d1_tally_path": str(path),
        "d1_tally_ref_sha256": hashlib.sha256(raw).hexdigest(),
        "d1_artifact_sha256": tally.get("sha256"),
        "d1_artifact_commit": tally.get("artifact_commit"),
        "d1_artifact_path": tally.get("path"),
        "d1_schema": schema,
        "d1_field_count": field_count,
        "source_id": tally.get("source_id"),
        "release_ref": tally.get("release_ref"),
        "reason": "D1 descriptive tally is not an EmpiricalFact and must not be converted into one",
        "consumer_invoked": False,
        "source_value_sensitive": False,
    }
