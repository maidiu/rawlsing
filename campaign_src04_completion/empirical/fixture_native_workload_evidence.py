"""Execute the production native workload builder against the labelled SRC04
nonrespondent fixture and write compact aggregate evidence.

This is focused engineering discrimination only.  It never reads the original
SAV and never imports test helper modules.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from campaign_src04_completion.empirical.native_workload import (
    WorkloadPolicy,
    build_native_workload,
    execute_native_workload,
)
from rawlsing_next.pre553_c11_integrity import RespondentIdentity
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    ExactRef,
    authority_ref,
    canonicalize,
    exact_ref,
)
from rawlsing_next.pre553_observed_response import ObservedResponseContract, ObservedResponseTopologyBinding
from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.schema import load_source_config

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "source_pre553_validation/SRC04/fixture.config.json"
FIXTURE_PATH = ROOT / "source_pre553_validation/SRC04/fixture.json"
OUT = ROOT / "campaign_src04_completion/empirical/NATIVE_WORKLOAD_EVIDENCE.json"
ORIGINAL_SHA = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
OPERATION = "PRE553_OBSERVED_RESPONSE_EMPIRICAL_OPERATIONS@1.0.0"
TARGETS = ("q102", "q206", "q236")


def _h(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    digest = _h(f"fixture-native:{kind}:{tag}")
    return ExactRef(kind, f"urn:test:fixture-native:{kind.lower()}:{tag}", digest)


def _auth(tag: str, kind: str, operations, families, scope) -> AuthoritySnapshot:
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"auth-{tag}"),
        authority_id=f"FIXTURE-NATIVE-{tag}",
        authority_version="1.0.0",
        authority_content_hash=_h(f"fixture-native:auth:{tag}"),
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=tuple(operations),
        governed_object_families=tuple(families),
        scope_envelope=scope,
        effective_time_or_interval="NONRESPONDENT_FIXTURE",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"fixture-native:semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", tag),
    )


def main() -> None:
    config = load_source_config(CONFIG_PATH)
    stream = load_fixture_stream(FIXTURE_PATH)
    release = build_validated_c11_release_from_config(config, stream=stream)
    universe = next(o for o in release.public_objects if o.schema_id == "EmpiricalUniverse")
    respondents = sorted(
        (r for r in release.internal_records if isinstance(r, RespondentIdentity)),
        key=lambda r: r.ref.key,
    )
    questions = {q["question_id"]: q for q in config.document["questions"]}
    responses = {r["question_id"]: r for r in config.document["response_slots"]}
    risk_ref = _ref("RISK_SET", "fixture-observed-response")
    auth = _auth(
        "QUERY",
        "PREDICATE_GRAMMAR",
        (OPERATION,),
        ("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
        {
            "fixture_only": True,
            "grade": "NONRESPONDENT_FIXTURE_ONLY",
            "source_id": "SRC04",
            "source_sha256": ORIGINAL_SHA,
            "source_universe_refs": [universe.ref.as_dict()],
            "predicate_or_risk_set_refs": [risk_ref.as_dict()],
        },
    )
    bindings = []
    for qid in TARGETS:
        q = questions[qid]
        occurrence = responses[qid]["values"][0]["occurrences"][0]
        bindings.append(ObservedResponseTopologyBinding(
            target_ref=exact_ref(q["native_question_ref"], "native_question_ref"),
            source_native_topology_ref=exact_ref(occurrence["topology_ref"], "topology_ref"),
            source_native_kind=occurrence["multiplicity_order_rank_fields"]["kind"],
            i03_topology="SCALAR_SINGULAR",
            topology_operation="R157_PREPARE_SOURCE_TOPOLOGY",
            topology_authority_ref=authority_ref(q["topology_authority_ref"], "topology_authority_ref"),
            response_semantic_authority_refs=(
                authority_ref(q["semantic_authority_ref"], "semantic_authority_ref"),
            ),
        ))
    bindings = tuple(sorted(bindings, key=lambda b: b.target_ref.key))
    contract = ObservedResponseContract(
        contract_id="FIXTURE-NATIVE-OBSERVED-RESPONSE-V2",
        contract_version="2.0.0",
        contract_state="AUTHORIZED",
        authority_grade="NONRESPONDENT_FIXTURE_ONLY",
        source_id="SRC04",
        source_sha256=ORIGINAL_SHA,
        source_snapshot_ref=exact_ref(
            config.document["binding"]["source_snapshot_ref"], "source_snapshot_ref"),
        source_artifact_ref=release.source_artifact_ref,
        source_release_manifest_hash=release.source_release_manifest_hash,
        release_ref=release.release_ref,
        universe_ref=universe.ref,
        operation=OPERATION,
        operation_authority_ref=auth.authority_ref,
        risk_set_ref=risk_ref,
        target_refs=tuple(b.target_ref for b in bindings),
        observed_states=("DK", "REFUSAL", "SOURCE_SPECIFIC_SPECIAL", "SUBSTANTIVE_RESPONSE"),
        missing_states=("MISSING",),
        denominator_policies=("CO_OBSERVED_TARGETS", "PER_TARGET_OBSERVED"),
        condition_observation_policy="ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED",
        topology_bindings=bindings,
    )
    registry = AuthorityRegistry((
        *(o for o in release.public_objects if o.schema_id == "AuthoritySnapshot"),
        auth,
    ))
    repository = C11Repository((release,))
    policy = WorkloadPolicy(
        policy_id="FIXTURE-NATIVE-FINITE-FRONTIER",
        families=(
            "UNARY_OBSERVED_DISTRIBUTION",
            "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION",
            "SAME_RESPONDENT_JOINT_DISTRIBUTION",
        ),
        max_arity=2,
    )
    workload = build_native_workload(
        repository=repository,
        release_ref=release.release_ref,
        contract=contract,
        policy=policy,
    )
    executed = execute_native_workload(
        repository=repository,
        release_ref=release.release_ref,
        contract=contract,
        authority_registry=registry,
        policy=policy,
    )
    first_operation_id = workload.operations[0].operation_id if workload.operations else None
    resumed = execute_native_workload(
        repository=repository,
        release_ref=release.release_ref,
        contract=contract,
        authority_registry=registry,
        policy=policy,
        start_after_operation_id=first_operation_id,
    ) if first_operation_id is not None else None
    receipts = executed.receipt()
    # Compact factual assertions from real execution; no respondent rows.
    by_family = {}
    for op in executed.operations:
        by_family.setdefault(op.family, []).append(op)
    unary = {
        op.target_refs[0].object_id: {
            "fact_state": op.fact_state,
            "raw_denominator": op.raw_denominator,
            "raw_numerator": op.raw_numerator,
            "cell_count": len(op.cells),
            "observed_ledger": op.observed_ledger,
        }
        for op in by_family.get("UNARY_OBSERVED_DISTRIBUTION", ())
    }
    joint = [
        {
            "targets": [r.object_id for r in op.target_refs],
            "fact_state": op.fact_state,
            "raw_denominator": op.raw_denominator,
            "raw_numerator": op.raw_numerator,
            "cell_count": len(op.cells),
        }
        for op in by_family.get("SAME_RESPONDENT_JOINT_DISTRIBUTION", ())
    ]
    conditional = [
        {
            "target": op.target_refs[0].object_id,
            "condition_state": op.condition_state,
            "condition_value_ref": op.condition_value_ref.as_dict() if op.condition_value_ref else None,
            "fact_state": op.fact_state,
            "raw_denominator": op.raw_denominator,
            "raw_numerator": op.raw_numerator,
            "observed_ledger": op.observed_ledger,
        }
        for op in by_family.get("BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION", ())
    ]
    evidence = {
        "schema": "PYAT_SRC04_NATIVE_WORKLOAD_EVIDENCE@2.0.0",
        "scope": "SRC04_NONRESPONDENT_FIXTURE_ONLY",
        "fixture": {
            "config_path": str(CONFIG_PATH.relative_to(ROOT)),
            "config_sha256": _sha(CONFIG_PATH),
            "fixture_path": str(FIXTURE_PATH.relative_to(ROOT)),
            "fixture_sha256": _sha(FIXTURE_PATH),
            "source_sha256": stream.source_sha256,
            "respondents": len(respondents),
            "release_ref": release.release_ref.as_dict(),
        },
        "contract_ref": contract.ref.as_dict(),
        "policy": {
            "policy_id": policy.policy_id,
            "families": list(policy.families),
            "max_arity": policy.max_arity,
        },
        "builder": {
            "module": "campaign_src04_completion.empirical.native_workload",
            "public_owner": "rawlsing_next.pre553_empirical_query.execute_empirical_query",
            "operations_built": len(workload.operations),
            "operations_executed": executed.accounting["executed_operations"],
            "operations_refused": executed.accounting["refused_operations"],
            "operations_by_family": executed.accounting["operations_by_family"],
            "operations_by_status": executed.accounting["operations_by_status"],
            "higher_order_requested_not_authorized": executed.accounting["requested_higher_order_not_authorized"],
            "routing_state": "ROUTING_UNKNOWN",
            "routing_conditions_used": 0,
        },
        "operation_receipts": receipts["operations"],
        "actual_results": {
            "unary": unary,
            "joint": joint,
            "conditional": conditional,
            "fact_count": sum(1 for op in executed.operations if op.fact_ref is not None),
            "all_operations_positive_or_typed": all(
                op.fact_state in {"SUPPORTED", "ZERO_SUPPORT", "UNRESOLVED"} for op in executed.operations
            ),
        },
        "resume_check": {
            "start_after_operation_id": first_operation_id,
            "operations_executed_after_resume": resumed.accounting["executed_operations"] if resumed else None,
            "operations_built": len(resumed.operations) if resumed else None,
            "prefix_not_reexecuted": (
                resumed is not None and first_operation_id is not None and
                all(op.operation_id == first_operation_id and op.fact_ref is None
                    for op in resumed.operations[:1])
            ),
        },
        "receipt_sha256": hashlib.sha256(
            json.dumps(canonicalize(receipts), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        ).hexdigest(),
        "limits": [
            "Nonrespondent fixture only; not original SRC04 qualification or scientific issuance.",
            "No original SAV stat/hash/open/decode/read.",
            "No respondent rows or member lists are committed; only aggregate cells and exact refs.",
            "Higher-order triples are not included in this policy; V2 contract max_arity is 2.",
            "q217, q715withoutmorocco and q716withoutmorocco remain residual held fields; ser remains identity-only.",
        ],
    }
    OUT.write_text(json.dumps(canonicalize(evidence), indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "operations_built": len(workload.operations),
        "executed": evidence["builder"]["operations_executed"],
        "refused": evidence["builder"]["operations_refused"],
        "by_family": evidence["builder"]["operations_by_family"],
        "unary": {k: {"d": v["raw_denominator"], "n": v["raw_numerator"]} for k, v in unary.items()},
        "joint": joint,
        "conditional_count": len(conditional),
        "resume": evidence["resume_check"],
        "evidence_sha256": _sha(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
