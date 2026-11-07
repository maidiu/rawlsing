from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as bridge
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next._pre553_query_common import _parse_target_plan
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_validated_source_backed_c11_release,
    execute_source_backed_empirical_query,
)
from rawlsing_next.tests.test_field_forge_conditional_support import (
    _domain_identity,
    _fixture as ff_fixture,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _auth,
    _branch_predicate,
    _build_source,
    _query,
    _query_authority,
    _ref,
    _registry,
    _run,
)
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import (
    _fixture as facade_fixture,
)

HERE = Path(__file__).resolve().parent
TRACE_JSON = HERE / "R7_EXECUTION_TRACE.json"
TRACE_TSV = HERE / "04_MUTATION_NEGATIVE_COLD_REPLAY.tsv"


def clone(obj, **changes):
    base = dict(
        typed_state=obj.typed_state,
        authority_snapshot_refs=obj.authority_snapshot_refs,
        dependency_refs=obj.dependency_refs,
        producer_replay_locator_or_reference_root=obj.producer_replay_locator_or_reference_root,
    )
    for key in tuple(changes):
        if key in base:
            base[key] = changes.pop(key)
    fields = dict(obj.semantic_fields)
    for key in base:
        fields.pop(key, None)
    fields.update(changes)
    return obj.__class__(**base, **fields)


def fact_record(fact):
    return {
        "typed_state": fact.typed_state,
        "raw_denominator_support": fact.raw_denominator_support,
        "raw_numerator_support": fact.raw_numerator_support,
        "fact_ref": fact.ref.as_dict(),
    }


def authority_record(authority):
    return {
        "authority_ref": authority.authority_ref.as_dict(),
        "authority_kind": authority.authority_kind,
        "typed_state": authority.typed_state,
        "governed_operations": list(authority.governed_operations),
        "governed_object_families": list(authority.governed_object_families),
        "scope_envelope": dict(authority.scope_envelope),
    }


def t01_variants():
    other_universe = _ref("UNIVERSE", "r7-t01-other-universe")
    return {
        "a_denied": clone(
            _auth("r7-t01-denied", "SOURCE_SEMANTICS_TOPOLOGY", families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0")),
            typed_state="DENY",
            decision_state="DENY",
        ),
        "b_wrong_kind_allow": _auth(
            "r7-t01-wrong-kind", "ROUTING_RISK_SET", families=("RoutingEligibilityFact@1.0.0",)
        ),
        "c_wrong_operation_allow": clone(
            _auth("r7-t01-wrong-op", "SOURCE_SEMANTICS_TOPOLOGY", families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0")),
            governed_operations=("WRONG-PERMITTED-OPERATION",),
        ),
        "d_wrong_scope_allow": clone(
            _auth("r7-t01-wrong-scope", "SOURCE_SEMANTICS_TOPOLOGY", families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0")),
            scope_envelope={"source_universe_refs": (other_universe.as_dict(),)},
        ),
    }


def run_t01():
    fx = facade_fixture("r7-t01")
    p = fx["projection"]
    qa = _query_authority("r7-t01")
    pred = _branch_predicate(fx, qa)
    q = _query(fx, qa, pred, ("Y",), tag="r7-t01-base")
    registry = AuthorityRegistry((*fx["authorities"], qa))
    baseline = execute_source_backed_empirical_query(
        source=fx["incidence"], projection=p, query=q, predicate=pred, authority_registry=registry
    ).facts[0]
    out = {"baseline": fact_record(baseline), "variants": {}}
    for name, bad in t01_variants().items():
        record = {"authority": authority_record(bad)}
        new_questions = tuple(
            replace(binding, semantic_authority_ref=bad.authority_ref, topology_authority_ref=bad.authority_ref)
            for binding in p.questions
        )
        new_slots = tuple(
            replace(
                slot,
                question_binding=replace(
                    slot.question_binding,
                    semantic_authority_ref=bad.authority_ref,
                    topology_authority_ref=bad.authority_ref,
                ),
            )
            for slot in p.response_slots
        )
        p2 = replace(
            p,
            questions=new_questions,
            response_slots=new_slots,
            authority_snapshots=(*p.authority_snapshots, bad),
            required_authority_refs=(*p.required_authority_refs, bad.authority_ref),
        )
        try:
            release = build_validated_source_backed_c11_release(fx["incidence"], p2)
            record["release"] = {"accepted": True, "release_ref": release.release_ref.as_dict()}
        except Exception as exc:
            record["release"] = {"accepted": False, "error_type": type(exc).__name__, "error": str(exc)[:500]}
            out["variants"][name] = record
            continue
        registry2 = AuthorityRegistry((*fx["authorities"], qa, bad))
        q_bad = _query(fx, qa, pred, ("Y",), tag=f"r7-t01-{name}", target_authority_refs=(bad.authority_ref,))
        try:
            result = execute_source_backed_empirical_query(
                source=fx["incidence"], projection=p2, query=q_bad, predicate=pred, authority_registry=registry2
            )
            record["bad_reference_query"] = {"accepted": True, "fact": fact_record(result.facts[0])}
        except Exception as exc:
            record["bad_reference_query"] = {"accepted": False, "error_type": type(exc).__name__, "error": str(exc)[:800]}
        try:
            control = execute_source_backed_empirical_query(
                source=fx["incidence"], projection=p2, query=q, predicate=pred, authority_registry=registry2
            )
            record["positive_target_control"] = {"accepted": True, "fact": fact_record(control.facts[0])}
        except Exception as exc:
            record["positive_target_control"] = {
                "accepted": False,
                "error_type": type(exc).__name__,
                "error": str(exc)[:800],
            }
        out["variants"][name] = record
    restore = execute_source_backed_empirical_query(
        source=fx["incidence"], projection=p, query=q, predicate=pred, authority_registry=registry
    ).facts[0]
    out["cold_restore"] = {"fact": fact_record(restore), "matches_baseline": restore.ref == baseline.ref}
    return out


def t02_variants():
    other_universe = _ref("UNIVERSE", "r7-t02-other-universe")
    return {
        "a_denied": clone(
            _auth("r7-t02-denied", "SOURCE_SEMANTICS_TOPOLOGY", families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0")),
            typed_state="DENY",
            decision_state="DENY",
        ),
        "b_wrong_kind_allow": _auth(
            "r7-t02-wrong-kind", "ROUTING_RISK_SET", families=("RoutingEligibilityFact@1.0.0",)
        ),
        "c_wrong_operation_allow": clone(
            _auth("r7-t02-wrong-op", "SOURCE_SEMANTICS_TOPOLOGY", families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0")),
            governed_operations=("WRONG-PERMITTED-OPERATION",),
        ),
        "d_wrong_scope_allow": clone(
            _auth("r7-t02-wrong-scope", "SOURCE_SEMANTICS_TOPOLOGY", families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0")),
            scope_envelope={"source_universe_refs": (other_universe.as_dict(),)},
        ),
    }


def run_t02():
    src = _build_source("r7-t02", [{"id": "R1", "responses": {"Y": 0}}, {"id": "R2", "responses": {"Y": 0}}])
    qa = _query_authority("r7-t02")
    pred = _branch_predicate(src, qa)
    q = _query(src, qa, pred, ("Y",), tag="r7-t02-base")
    baseline = _run(src, qa, pred, q).facts[0]
    out = {"baseline": fact_record(baseline), "variants": {}}
    for name, bad in t02_variants().items():
        record = {"authority": authority_record(bad)}
        q_bad = _query(src, qa, pred, ("Y",), tag=f"r7-t02-{name}", target_authority_refs=(bad.authority_ref,))
        registry = _registry(src, qa, bad)
        try:
            plan = _parse_target_plan(q_bad, registry)
            record["parse_target_plan"] = {"accepted": True, "components": len(plan.components)}
        except Exception as exc:
            record["parse_target_plan"] = {
                "accepted": False,
                "error_type": type(exc).__name__,
                "error": str(exc)[:500],
            }
        try:
            result = execute_empirical_query(
                repository=src["repo"],
                query=q_bad,
                predicate=pred,
                authority_registry=registry,
                release_refs=(src["release_ref"],),
            )
            record["first_consumer"] = {"accepted": True, "fact": fact_record(result.facts[0])}
        except Exception as exc:
            record["first_consumer"] = {"accepted": False, "error_type": type(exc).__name__, "error": str(exc)[:800]}
        out["variants"][name] = record
    restore = _run(src, qa, pred, q).facts[0]
    out["cold_restore"] = {"fact": fact_record(restore), "matches_baseline": restore.ref == baseline.ref}
    return out


def t03():
    risk = ExactRef("RISK_SET", adm.GT2_RISK_SET_ID, adm.GT2_RISK_SET_MEMBER_SET_SHA256)
    q, f, conditioner, target = ff_fixture()

    def build(c_ref, t_ref, c_domain, t_domain):
        components = []
        for comp, ref, domain in zip(q.target_arity_and_topology["components"], (c_ref, t_ref), (c_domain, t_domain)):
            item = dict(comp)
            item["target_ref"] = ref.as_dict()
            item["domain"] = list(domain)
            components.append(item)
        domain_identity = _domain_identity(c_ref, t_ref, c_domain, t_domain)
        q2 = clone(
            q,
            target_refs=(c_ref, t_ref),
            target_arity_and_topology={
                "arity": 2,
                "joint_order_semantics": "SEMANTIC_ORDERED",
                "components": tuple(components),
            },
            risk_set_ref=risk,
        )
        dependencies = tuple((q2.ref if ref == q.ref else ref) for ref in f.dependency_refs)
        target_topology = {**dict(f.target_topology), "target_domain_identity": domain_identity}
        f2 = clone(
            f,
            empirical_query_spec_ref=q2.ref,
            dependency_refs=dependencies,
            target_topology=target_topology,
            target_domain_identity=domain_identity,
            risk_set_ref=risk,
        )
        relation = ff.produce_exact_conditional_support_profile(
            joint_fact=f2,
            joint_query=q2,
            conditioner_ref=c_ref,
            target_ref=t_ref,
            producer_permission_ceiling=("FIELD_FORGE_RELATION_PRODUCTION", adm.GT2_TARGET_USE),
            relation_permission_ceiling=(adm.GT2_TARGET_USE,),
        )
        admitted = bridge.admit_gt12_c_relation(relation)
        return relation, admitted

    baseline_relation, baseline_admitted = build(conditioner, target, ("0", "1", "9"), ("1", "2", "9"))
    other_conditioner = _ref("QUESTION", "Q99B")
    other_target = _ref("QUESTION", "Q99A")
    other_relation, other_admitted = build(other_conditioner, other_target, ("0", "1", "9"), ("1", "2", "9"))
    restored_relation, restored_admitted = build(conditioner, target, ("0", "1", "9"), ("1", "2", "9"))
    return {
        "baseline": {
            "producer_roles": baseline_relation.semantic_projection()["roles"],
            "bridge_decision": baseline_admitted.admission.decision.value,
            "bridge_participants": [
                {"role": p.role, "native_variable": p.native_variable, "participant_ref": p.participant_ref.as_dict()}
                for p in baseline_admitted.evidence.participants
            ],
        },
        "non_q86_direct_call": {
            "relation_ref": other_relation.ref.as_dict(),
            "producer_roles": other_relation.semantic_projection()["roles"],
            "conditioner_ref": other_relation.conditioner_ref.as_dict(),
            "target_ref": other_relation.target_ref.as_dict(),
            "bridge_decision": other_admitted.admission.decision.value,
            "bridge_participants": [
                {"role": p.role, "native_variable": p.native_variable, "participant_ref": p.participant_ref.as_dict()}
                for p in other_admitted.evidence.participants
            ],
        },
        "cold_restore": {
            "relation_ref": restored_relation.ref.as_dict(),
            "matches_baseline_relation": restored_relation.ref == baseline_relation.ref,
            "bridge_decision": restored_admitted.admission.decision.value,
        },
    }


def tsv_rows(trace):
    rows = [
        ["probe", "fixture", "mutation", "authority_ref", "gate", "local_or_release", "first_consumer", "typed_state", "numerator", "denominator", "fact_or_relation_ref", "cold_restore"]
    ]
    t01 = trace["T01"]
    rows.append(["T01", "source-backed C11 Y substantive", "baseline", "", "C11+projection+query", "accepted", "accepted", t01["baseline"]["typed_state"], str(t01["baseline"]["raw_numerator_support"]), str(t01["baseline"]["raw_denominator_support"]), t01["baseline"]["fact_ref"]["object_id"], "yes" if t01["cold_restore"]["matches_baseline"] else "no"])
    for name, record in t01["variants"].items():
        authority = record["authority"]["authority_ref"]["authority_id"]
        release = record["release"]["accepted"]
        bad = record.get("bad_reference_query", {})
        control = record.get("positive_target_control", {})
        if bad.get("accepted"):
            fact = bad["fact"]
            rows.append(["T01", "source-backed C11 Y substantive", name, authority, "C11 release + first consumer", "accepted" if release else "refused", "accepted", fact["typed_state"], str(fact["raw_numerator_support"]), str(fact["raw_denominator_support"]), fact["fact_ref"]["object_id"], "yes" if t01["cold_restore"]["matches_baseline"] else "no"])
        else:
            rows.append(["T01", "source-backed C11 Y substantive", name, authority, "C11 release + first consumer", "accepted" if release else "refused", bad.get("error_type", "refused"), "n/a", "0", "0", "", "yes" if t01["cold_restore"]["matches_baseline"] else "no"])
        if control.get("accepted"):
            fact = control["fact"]
            rows.append(["T01", "source-backed C11 Y substantive", name + " positive-target control", authority, "event-authority guard", "accepted" if release else "refused", "accepted", fact["typed_state"], str(fact["raw_numerator_support"]), str(fact["raw_denominator_support"]), fact["fact_ref"]["object_id"], "yes" if t01["cold_restore"]["matches_baseline"] else "no"])
        else:
            rows.append(["T01", "source-backed C11 Y substantive", name + " positive-target control", authority, "event-authority guard", "accepted" if release else "refused", control.get("error_type", "refused"), "n/a", "0", "0", "", "yes" if t01["cold_restore"]["matches_baseline"] else "no"])
    t02 = trace["T02"]
    rows.append(["T02", "I03 exact sourcefree Y", "baseline", "", "_parse_target_plan+execute_empirical_query", "accepted", "accepted", t02["baseline"]["typed_state"], str(t02["baseline"]["raw_numerator_support"]), str(t02["baseline"]["raw_denominator_support"]), t02["baseline"]["fact_ref"]["object_id"], "yes" if t02["cold_restore"]["matches_baseline"] else "no"])
    for name, record in t02["variants"].items():
        authority = record["authority"]["authority_ref"]["authority_id"]
        local = record["parse_target_plan"]
        consumer = record["first_consumer"]
        if consumer.get("accepted"):
            fact = consumer["fact"]
            rows.append(["T02", "I03 exact sourcefree Y", name, authority, "_parse_target_plan", "accepted" if local.get("accepted") else local.get("error_type", "refused"), "accepted", fact["typed_state"], str(fact["raw_numerator_support"]), str(fact["raw_denominator_support"]), fact["fact_ref"]["object_id"], "yes" if t02["cold_restore"]["matches_baseline"] else "no"])
        else:
            rows.append(["T02", "I03 exact sourcefree Y", name, authority, "_parse_target_plan", "accepted" if local.get("accepted") else local.get("error_type", "refused"), consumer.get("error_type", "refused"), "n/a", "0", "0", "", "yes" if t02["cold_restore"]["matches_baseline"] else "no"])
    t03 = trace["T03"]
    rows.append(["T03", "FF Q86 synthetic same-risk", "baseline Q86B/Q86A", "", "producer+bridge direct", "accepted", "accepted", "ADMITTED", "n/a", "n/a", t03["cold_restore"]["relation_ref"]["object_id"], "yes" if t03["cold_restore"]["matches_baseline_relation"] else "no"])
    rows.append(["T03", "FF Q86 synthetic same-risk", "non-Q86 Q99B/Q99A direct call", "urn:test:i03:question:Q99B", "producer+bridge direct", "accepted", "accepted", "ADMITTED_Q99_REFS_LABELED_Q86", "n/a", "n/a", t03["non_q86_direct_call"]["relation_ref"]["object_id"], "yes" if t03["cold_restore"]["matches_baseline_relation"] else "no"])
    return rows


def main():
    trace = {"T01": run_t01(), "T02": run_t02(), "T03": t03()}
    TRACE_JSON.write_text(json.dumps(trace, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    rows = tsv_rows(trace)
    TRACE_TSV.write_text("\n".join("\t".join(row) for row in rows) + "\n", encoding="utf-8")
    print(json.dumps(trace, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
