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
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
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
class ProducerBundle:
    release: C11LogicalRelease
    query: EmpiricalQuerySpec
    predicate: EmpiricalPredicate
    repository: C11Repository
    authority_registry: AuthorityRegistry
    contract: ProducerContract


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


def consume_native_producer(
    bundle: ProducerBundle,
    *,
    expected_source_id: str,
    requested_claim_ceiling: str = SOURCE_LOCAL_CLAIM,
    use_scope: str = SOURCE_LOCAL_CLAIM,
    replay: bool = True,
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
    if contract.fixture_only or bundle.release.source_artifact_ref.content_hash != contract.source_sha256:
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
    receipt = _oc01_receipt(
        contract=contract,
        producer_ref=fact.ref,
        authority_refs=(_policy_authority(x) for x in fact_authority_values(fact)),
        requested_claim_ceiling=requested_claim_ceiling,
        partial_allowed=True,
    )
    return {
        "schema": "PYAT_SRC04_LANE_D_CONSUMER_PRODUCT@1.0.0",
        "status": "SOURCE_LOCAL_NATIVE_CONSUMER_POSITIVE",
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
        "fixture_only": False,
        "source_value_sensitive": True,
        "canonical_values_emitted": 0,
        "population_claim": False,
        "weights_used": False,
        "ff_v553_adoption": False,
    }


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
