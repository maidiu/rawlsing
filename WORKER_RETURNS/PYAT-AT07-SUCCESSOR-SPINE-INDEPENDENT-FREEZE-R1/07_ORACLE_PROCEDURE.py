#!/usr/bin/env python3
"""AT07 independent successor oracle, stdlib only; production files are inert bytes.

Modes: generate (writes within package), verify (read-only), hostiles (read-only).
No imports, evaluation, exec, or calls of production modules or test helpers.
Conserved producer refs are accepted R8 upstream custody, never candidate output.
"""
import argparse
import ast
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ADD = {"discovery_receipt_refs": [], "discovery_frontier_ref": None,
       "recursive_handoff_refs": [], "recursive_lineage_refs": [],
       "joint_component_count": 1, "joint_order_semantics": "SEMANTIC_ORDERED"}
PASS = "PASS_AT07_SUCCESSOR_SPINE_INDEPENDENTLY_FROZEN__INDEPENDENT_REVIEW_REQUIRED"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def canonical(value):
    if value is None or type(value) in (str, bool, int):
        return value
    if type(value) is list:
        return [canonical(v) for v in value]
    if type(value) is dict:
        require(all(type(k) is str for k in value), "NON_STRING_KEY")
        return {k: canonical(value[k]) for k in sorted(value)}
    raise ValueError("NON_JSON_OR_FLOAT_IDENTITY")


def wire(value):
    return json.dumps(canonical(value), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(wire(value)).hexdigest()


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def write(name, value):
    (ROOT / name).write_bytes(json.dumps(value, indent=2, ensure_ascii=False,
                                       allow_nan=False).encode() + b"\n")


def ordered(refs, authority=False):
    keys = ("authority_id", "authority_version", "authority_content_hash") if authority else (
        "kind", "object_id", "content_hash")
    unique = {tuple(r[k] for k in keys): r for r in refs}
    return [unique[k] for k in sorted(unique)]


def ref(kind, object_id, h):
    return {"kind": kind, "object_id": object_id, "content_hash": h}


def local_ref(kind, tag):
    return ref(kind, "urn:test:i03:" + kind.lower() + ":" + tag,
               hashlib.sha256(("i03:" + kind + ":" + tag).encode()).hexdigest())


def public_ref(family, state, authority, replay, fields):
    material = {"schema_id": family, "schema_version": "1.0.0", "typed_state": state,
                "authority_snapshot_refs": [authority], "dependency_refs": [],
                "producer_replay_locator_or_reference_root": replay, "semantic_fields": fields}
    h = digest(material)
    return ref(family + "@1.0.0", "urn:rawlsing:pre553:" + family + ":sha256:" + h, h)


def static_keys(data):
    tree = ast.parse(data.decode("utf-8"))
    cls = next(c for c in tree.body if isinstance(c, ast.ClassDef) and c.name == "AnalyticalCompositionResult")
    method = next(f for f in cls.body if isinstance(f, ast.FunctionDef) and f.name == "identity_material")
    value = next(s.value for s in method.body if isinstance(s, (ast.Return, ast.Assign))
                 and isinstance(s.value, ast.Dict))
    return sorted(k.value for k in value.keys)


def lock_inputs(overrides=None):
    overrides = overrides or {}
    pins = load("01_PINNED_INPUTS.json")
    for x in pins["inputs"]:
        data = overrides.get(x["name"], (ROOT / x["local_path"]).read_bytes())
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blob == x["blob"] and hashlib.sha256(data).hexdigest() == x["sha256"],
                "PINNED_BLOB_DRIFT:" + x["name"])
    manifest = load("02_OLD_NEW_PREIMAGE_FIELD_MANIFEST.json")
    old = static_keys((ROOT / "INPUTS/historical_owner.py").read_bytes())
    new = static_keys((ROOT / "INPUTS/adopted_owner.py").read_bytes())
    require(old == manifest["historical_keys"] and new == manifest["successor_keys"], "FIELD_LAW_DRIFT")
    require(set(new) - set(old) == set(ADD) and not set(old) - set(new), "SIX_KEY_DELTA_DRIFT")
    require(wire(manifest["directly_added_fields"]) == wire(ADD), "DEFAULT_LAW_DRIFT")
    return pins, manifest


def derive(direction):
    spine = load("INPUTS/r8_spine.json")["identity_spine"]
    upstream = spine[direction]
    universe, release = spine["universe_ref"], spine["release_ref"]
    source_receipt = load("INPUTS/input_0.json")
    require(source_receipt["release_ref"] == release and source_receipt["universe_ref"] == universe,
            "SOURCE_RELEASE_CUSTODY_DRIFT")
    entries = load("INPUTS/input_4.json")["authorities"]
    entries += [load("INPUTS/r3_scope.json")["repaired_query_authority"]]
    authorities = {}
    for e in entries:
        a = e["expected_authority_ref"]
        require(digest(e["canonical_material"]) == a["authority_content_hash"], "AUTHORITY_PREIMAGE_DRIFT")
        authorities[a["authority_id"]] = a
    source_auth = authorities["C1-AT07-SOURCE"]
    routing_auth = authorities["C1-AT07-ROUTING"]
    pairing = authorities["C1-AT07-COMPARABILITY"]
    require(authorities["C1-AT07-QUERY"] == spine["query_authority_ref"], "QUERY_AUTHORITY_DRIFT")
    relations = load("INPUTS/input_3.json")
    for family in ("subject_condition_preimages", "predicate_leaf_preimages", "pairing_ground_truth"):
        for entry in relations[family]:
            require(digest(entry["material"]) == entry["ref"]["content_hash"], "RELATION_PREIMAGE_DRIFT")
    forward = direction == "forward"
    subject_role = "POSITION_P1" if forward else "ANSWER_YES"
    leaf_role = "POSITION_EQ_P1" if forward else "ANSWER_EQ_YES"
    def relation(family, role):
        return next(x for x in relations[family] if x["material"]["role"] == role)
    subject = relation("subject_condition_preimages", subject_role)
    leaf = relation("predicate_leaf_preimages", leaf_role)
    pair = relation("pairing_ground_truth", subject_role + "__" + leaf_role)
    predicate = load("INPUTS/input_1.json")["directions"][direction]
    require(digest(predicate["predicate_ast"]) == upstream["producer_predicate_hash"], "PREDICATE_AST_DRIFT")
    require(digest(predicate["predicate_semantic_projection"]) == upstream["producer_predicate_ref"]["content_hash"],
            "PREDICATE_OUTER_DRIFT")
    target = "ANSWER" if forward else "POSITION"
    conditioned = "POSITION" if forward else "ANSWER"
    binding_id = "position" if forward else "answer"
    target_ref = local_ref("QUESTION_NATIVE", "c1-at07-" + target)
    binding = {"binding_id": binding_id, "subject_fact_ref": subject["ref"],
               "empirical_coordinate_ref": local_ref("QUESTION_NATIVE", "c1-at07-" + conditioned),
               "comparability_authority_ref": pairing, "source_universe_ref": universe,
               "release_ref": release, "effective_time_or_interval": None}
    subject_material = {"schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1", "fixture_id": "AT07_BIDIRECTIONAL_100",
                        "role": "FORWARD_POSITION_P1" if forward else "REVERSE_ANSWER_YES", "real_subject": False}
    subject_ref = ref("C1_SYNTHETIC_POSITIONED_SUBJECT@1", "urn:test:c1:at07:positioned-subject:" + (
        "forward-position-p1" if forward else "reverse-answer-yes"), digest(subject_material))
    query_material = {"contract": "POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_QUERY@1",
                      "query_id": "c1-at07-" + ("forward-position-p1-to-answer" if forward else "reverse-answer-yes-to-position"),
                      "purpose": "EMPIRICAL_POSSIBILITY_ONLY", "subject_ref": subject_ref,
                      "target_ref": target_ref, "source_universe_ref": universe, "release_ref": release,
                      "conditioner_bindings": [binding], "requested_projection": {
                          "kind": "C1_AT07_CONDITIONAL_DISTRIBUTION", "direction": (
                              "POSITION_P1_TO_ANSWER" if forward else "ANSWER_YES_TO_POSITION"), "target_role": target}}
    qh = digest(query_material)
    consumer_query_ref = ref(query_material["contract"], "urn:rawlsing:learned-world:positioned-subject-query:sha256:" + qh, qh)
    require(consumer_query_ref == upstream["consumer_query_ref"], "CONSUMER_QUERY_DRIFT")
    witness_material = {"consumer_query_ref": consumer_query_ref, "consumer_binding_material": binding,
        "consumer_binding_fingerprint": digest(binding), "subject_condition_preimage_ref": subject["ref"],
        "subject_condition_preimage_material": subject["material"], "producer_query_ref": upstream["producer_query_ref"],
        "producer_predicate_ref": upstream["producer_predicate_ref"], "producer_predicate_hash": digest(predicate["predicate_ast"]),
        "producer_predicate_leaf_ref": leaf["ref"], "producer_predicate_leaf_projection": leaf["material"],
        "pairing_ground_truth_ref": pair["ref"], "pairing_authority_ref": pairing,
        "source_universe_ref": universe, "release_ref": release, "effective_time_or_interval": None,
        "binding_mode": "EXPLICIT_VALUE_BEARING_RELATION__NO_INFERENCE"}
    witness_ref = ref("C1_CONDITION_VALUE_BINDING_WITNESS@2", "urn:test:c1:at07:condition-value-witness:" + (
        "r6-forward-p1" if forward else "r6-reverse-yes"), digest(witness_material))
    require(witness_ref == upstream["witness_ref"], "WITNESS_DRIFT")
    rows = []
    for group in source_receipt["immutable_inputs"]["fixture_rows"]:
        rows += [{"id": group["prefix"] + format(i, "03d"), "POSITION": group["position"], "ANSWER": group["answer"]}
                 for i in range(1, group["count"] + 1)]
    require(len(rows) == 100, "SOURCE_ROW_COUNT_DRIFT")
    domain = ["no", "yes"] if forward else ["P1", "P2"]
    selected = [r for r in rows if r[conditioned] == ("P1" if forward else "yes")]
    require(len(selected) == (60 if forward else 62), "DENOMINATOR_DRIFT")
    respondent_refs = {}
    for r in rows:
        fields = {"empirical_universe_ref": universe, "respondent_key": r["id"],
                  "source_native_respondent_key_ref_or_typed_absence": local_ref("SOURCE_RESPONDENT", "c1-at07-" + r["id"]),
                  "identity_map_authority_ref_or_typed_absence": {"typed_absence_state": "NOT_APPLICABLE", "detail": None}}
        h = digest({"record_family": "RespondentIdentity", "record_version": "1.0.0", "semantic_fields": fields})
        respondent_refs[r["id"]] = ref("C11Internal:RespondentIdentity", "urn:rawlsing:pre553:c11:RespondentIdentity:sha256:" + h, h)
    risk_ref = local_ref("RISK_SET", "c1-at07-R_ALL_100")
    used = [universe, source_receipt["candidate_replay"]["replay_manifest_ref"]]
    all_members = "-".join(sorted(r["id"] for r in rows))
    for r in rows:
        fields = {"empirical_universe_ref": universe, "scoped_respondent_ref": respondent_refs[r["id"]],
                  "question_or_target_ref": target_ref, "risk_set_ref": risk_ref,
                  "routing_rule_ref": local_ref("ROUTING_RULE", "c1-at07-R_ALL_100-" + target),
                  "applicability_state": "ELIGIBLE_APPLICABLE", "routing_state": "ELIGIBLE_APPLICABLE",
                  "parent_predicate_refs": [], "member_set_replay_ref": local_ref("MEMBER_SET", "c1-at07-R_ALL_100-" + target + "-" + all_members)}
        used.append(public_ref("RoutingEligibilityFact", "ELIGIBLE_APPLICABLE", routing_auth,
            local_ref("REPLAY_ROOT", "routing-c1-at07-R_ALL_100-" + r["id"] + "-" + target), fields))
        for q in [conditioned] + ([target] if r in selected else []):
            fields = {"empirical_universe_ref": universe, "scoped_respondent_ref": respondent_refs[r["id"]],
                      "native_question_ref": local_ref("QUESTION_NATIVE", "c1-at07-" + q),
                      "canonical_question_ref_if_authorized": None, "component_or_subitem_ref": None,
                      "event_group_id": "GROUP-c1-at07-" + r["id"] + "-" + q,
                      "response_event_id_or_deterministic_index": r["id"] + "-" + q,
                      "raw_response_value": r[q], "canonical_response_value_if_authorized": None,
                      "value_transform_authority_ref": None,
                      "response_topology_ref": local_ref("TOPOLOGY", "c1-at07-" + q + "-SCALAR_SINGULAR"),
                      "multiplicity_order_rank_fields": {"kind": "SCALAR_SINGULAR", "index": 0},
                      "response_state": "SUBSTANTIVE_RESPONSE"}
            used.append(public_ref("RespondentEvent", "SUBSTANTIVE_RESPONSE", source_auth,
                local_ref("REPLAY_ROOT", "event-c1-at07-" + r["id"] + "-" + q), fields))
    provenance = ordered([release, *used])
    component = {"target_ref": target_ref, "topology": "SCALAR_SINGULAR", "domain": domain,
                 "target_domain_replay_ref": local_ref("TARGET_DOMAIN", target + "-" + "-".join(domain)),
                 "topology_authority_refs": [source_auth], "response_semantic_authority_refs": [source_auth],
                 "included_states": ["SUBSTANTIVE_RESPONSE"]}
    domain_identity = digest({"components": [{k: component[k] for k in (
        "target_ref", "topology", "domain", "target_domain_replay_ref")}], "joint_order_semantics": "SEMANTIC_ORDERED", "full_domain": domain})
    cells = []
    for value in domain:
        count = sum(r[target] == value for r in selected)
        f = Fraction(count, len(selected))
        cells.append({"cell": value, "cell_state": "OBSERVED_POSITIVE", "raw_numerator_support": count,
                      "weighted_numerator_support_if_authorized": None,
                      "raw_probability_exact_fraction": {"$exact_fraction": [f.numerator, f.denominator]},
                      "weighted_probability_exact_fraction_if_authorized": None})
    require([c["raw_numerator_support"] for c in cells] == ([6,54] if forward else [54,8]), "CELL_ARITHMETIC_DRIFT")
    geometry = {"schema": "C1_POSSIBILITY_SLICE_GEOMETRY@1", "source_fact_ref": upstream["producer_fact_ref"],
                "producer_query_ref": upstream["producer_query_ref"], "condition_predicate_ref": upstream["producer_predicate_ref"],
                "condition_value_witness_ref": witness_ref, "target": {"target_ref": target_ref, "arity": 1,
                    "joint_order_semantics": "SEMANTIC_ORDERED", "component_material": component, "target_domain_identity": domain_identity},
                "denominator": {"risk_set_ref": risk_ref, "risk_set_type": "WHOLE_QUESTION_RISK_SET",
                    "risk_set_member_refs": ordered(list(respondent_refs.values())),
                    "denominator_member_refs": ordered([respondent_refs[r["id"]] for r in selected]),
                    "raw_denominator_support": len(selected), "weighted_denominator_support_if_authorized": None},
                "measure": {"measure_kind": "RAW", "measure_basis_ref": local_ref("MEASURE_BASIS", "RAW"),
                    "weight_basis_id_or_null": None, "weight_design_estimand_context": None}, "cells": cells}
    authority_refs = ordered([source_auth, routing_auth, spine["query_authority_ref"], pairing], True)
    evidence_material = {"schema": "C1_POSITIONED_SUBJECT_SLICE_EVIDENCE_PREIMAGE@1", "contract_id": "C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1",
        "source_universe_ref": universe, "release_ref": release, "target_ref": target_ref,
        "retained_conditioner_ids": [binding_id], "evidence_state": "SUPPORTED", "geometry": geometry,
        "raw_support": len(selected), "uncertainty_state": "UNCERTAINTY_UNQUANTIFIED",
        "provenance_refs": ordered([upstream["producer_fact_ref"], upstream["producer_query_ref"], upstream["producer_predicate_ref"],
                                    upstream["producer_replay_ref"], witness_ref, subject["ref"], pair["ref"]]), "authority_refs": authority_refs}
    eh = digest(evidence_material)
    evidence_ref = ref(evidence_material["contract_id"], "urn:rawlsing:c1:positioned-subject-slice-evidence:sha256:" + eh, eh)
    require(evidence_ref == upstream["evidence_ref"], "EVIDENCE_DRIFT")
    rule = {"contract": "SOURCE_BACKED_POSITIONED_SUBJECT_POSSIBILITY@1.0.0",
            "model_rule_id": "POSITIONED_SUBJECT_EXACT_CONDITIONAL_WITH_GOVERNED_WALKBACK@1.0.0",
            "algorithm_id": "EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION",
            "model_authority_ref": authorities["C1-AT07-MODEL"], "walkback_authority_ref": authorities["C1-AT07-WALKBACK"],
            "source_universe_refs": [universe], "walkback_steps": [], "positive_proxy_authority_refs": [],
            "cross_source_proxy": "FORBIDDEN_IN_V1", "proxy_can_satisfy_exact_request": False, "actor_inference_allowed": False}
    consumer_material = {"contract": "POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_FIELD@1", "query_ref": consumer_query_ref,
        "result_state": "EXACT_SUPPORTED", "exact_lane": {"disposition": "SUPPORTED", "reason": "EXACT_POSITIONED_STRATUM_SUPPORTED",
            "evidence_ref": evidence_ref, "geometry": geometry}, "proxy_lane": None, "fallback_path": [],
        "model_authority_ref": rule["model_authority_ref"], "walkback_authority_ref": rule["walkback_authority_ref"],
        "source_universe_ref": universe, "release_ref": release, "target_ref": target_ref,
        "replay_determinants": ordered([consumer_query_ref, evidence_ref]), "model_rule_hash": digest(rule),
        "epistemic_ceiling": ["PROXY != EXACT FACT != ACTOR BELIEF", "EMPIRICAL_POSSIBILITY != INDIVIDUAL_PREDICTION",
            "EMPIRICAL_POSSIBILITY != NORMATIVE_RECOMMENDATION", "GENERATED_SUBJECT_FACT_IS_QUERY_CRITERION_NOT_UPSTREAM_OWNED_FACT"]}
    old = {"analytical_state": "SUPPORTED", "producer_route": "DIRECT_I03_TO_POSITIONED_SUBJECT",
        "producer_query_ref": upstream["producer_query_ref"], "producer_predicate_ref": upstream["producer_predicate_ref"],
        "producer_fact_ref": upstream["producer_fact_ref"], "producer_fact_state": "SUPPORTED",
        "producer_result_envelope": {"query_ref": upstream["producer_query_ref"], "source_scope_mode": "SINGLE_UNIVERSE",
            "release_refs": [release], "fact_refs": [upstream["producer_fact_ref"]]}, "source_universe_refs": [universe],
        "release_refs": [release], "consumer_query_ref": consumer_query_ref, "consumer_binding_fingerprint": digest(binding),
        "condition_binding_witness_ref_or_hash": witness_ref, "ordered_target_refs": [target_ref],
        "target_arity_and_topology": {"arity": 1, "joint_order_semantics": "SEMANTIC_ORDERED", "components": [component]},
        "target_domain_identity": domain_identity, "risk_set_ref": risk_ref,
        "risk_set_member_refs": geometry["denominator"]["risk_set_member_refs"],
        "denominator_member_refs": geometry["denominator"]["denominator_member_refs"], "raw_denominator_support": len(selected),
        "measure_kind": "RAW", "measure_basis_ref": geometry["measure"]["measure_basis_ref"],
        "weight_basis_id_or_null": None, "weight_design_estimand_context": None, "complete_cell_geometry": cells,
        "uncertainty_state": "UNCERTAINTY_UNQUANTIFIED", "coverage_state": "DIRECT_EXACT_SINGLE_QUERY", "ancestry_refs": [],
        "authority_refs": authority_refs, "provenance_refs": provenance,
        "dependency_refs": ordered([upstream["producer_query_ref"], upstream["producer_predicate_ref"], upstream["producer_replay_ref"], *provenance]),
        "replay_refs": [upstream["producer_replay_ref"]], "possibility_slice_evidence_ref_or_null": evidence_ref,
        "consumer_result_hash_or_null": digest(consumer_material), "consumer_model_rule_hash": digest(rule),
        "subject_condition_preimage_refs": [subject["ref"]], "producer_predicate_leaf_refs": [leaf["ref"]],
        "pairing_ground_truth_refs": [pair["ref"]],
        "slice_projection_schema_hash": "c00e038dd2c1177bfc7842f12febef7b3e30b92bc421df244e2a8e3c4a20b17a"}
    require(digest(old) == upstream["composed_result_identity_hash"], "HISTORICAL_COMPLETE_PREIMAGE_DRIFT:" + direction + ":" + digest(old))
    successor = {**old, **copy.deepcopy(ADD)}
    details = {"consumer_query_preimage": query_material, "binding_preimage": binding, "witness_preimage": witness_material,
               "evidence_preimage": evidence_material, "model_rule_preimage": rule, "consumer_result_preimage": consumer_material,
               "upstream_custody": upstream, "source_rows": rows,
               "upstream_qualification": "Producer query/fact/replay refs conserved from exact R8 spine; no producer execution in this lane"}
    return old, successor, details


def validate_preimage(actual, expected, serialized):
    require(wire(actual) == wire(expected), "COMPLETE_EXPECTED_PREIMAGE_MISMATCH")
    require(serialized == wire(expected), "CANONICAL_BYTE_MISMATCH")


def artifacts():
    pins, manifest = lock_inputs()
    results = {}
    for direction in ("forward", "reverse"):
        old, new, details = derive(direction)
        require(sorted(old) == manifest["historical_keys"] and sorted(new) == manifest["successor_keys"], "COMPLETE_KEYSET_DRIFT")
        results[direction] = (old, new, details)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("generate", "verify", "hostiles"))
    args = parser.parse_args()
    results = artifacts()
    if args.mode == "generate":
        records = {}
        for direction, (old, new, details) in results.items():
            name = "03_FORWARD_SUCCESSOR_PREIMAGE.json" if direction == "forward" else "04_REVERSE_SUCCESSOR_PREIMAGE.json"
            write(name, new)
            (ROOT / (direction.upper() + "_SUCCESSOR_CANONICAL.json")).write_bytes(wire(new))
            (ROOT / (direction.upper() + "_HISTORICAL_CANONICAL.json")).write_bytes(wire(old))
            write(direction.upper() + "_DERIVATION_PREIMAGES.json", details)
            records[direction] = {"preimage_path": name, "canonical_bytes_path": direction.upper() + "_SUCCESSOR_CANONICAL.json",
                                  "successor_sha256": digest(new), "canonical_bytes_length": len(wire(new)),
                                  "historical_sha256_reconstructed": digest(old), "historical_preserved": True,
                                  "conserved_field_count": len(old), "added_field_count": len(ADD)}
        write("05_SUCCESSOR_SPINE.json", {"schema": "PYAT_AT07_C1_02_SUCCESSOR_IDENTITY_SPINE@1.0.0", "status": PASS,
            "selected_law": "A_VERSIONED_SUCCESSOR_SPINE", "historical_spine": {"path": "INPUTS/r8_spine.json",
                "original_path": "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/04_CURRENT_AT07_IDENTITY_SPINE.json",
                "blob": "462bb282ddc2cc9667f1890f2d65f2fae9a3a72c", "role": "Unchanged historical C1-01 evidence"},
            "astra_commit": "a2e7767ecec9ecb6d241861628759f2e933920d5", "adopted_owner_blob": "604c8d591d4cc2b646e9b149cdb233fc9d69cf6b",
            "input_freeze_path": "01_PINNED_INPUTS.json", "field_law_path": "02_OLD_NEW_PREIMAGE_FIELD_MANIFEST.json",
            "directions": records, "independence": "Known candidate forward digest disclosed in pins; never used, compared, or supplied to derivation",
            "downstream": {"consumer_result_and_evidence": "Conserved; bind upstream geometry/witness, not composed identity",
                "provider_or_at17_identities": "Not computed; independent review and HQ adoption plus separately authorized requalification required"},
            "self_adopted": False})
    elif args.mode == "verify":
        spine = load("05_SUCCESSOR_SPINE.json")
        for direction, (old, expected, details) in results.items():
            r = spine["directions"][direction]
            validate_preimage(load(r["preimage_path"]), expected, (ROOT / r["canonical_bytes_path"]).read_bytes())
            require(r["successor_sha256"] == digest(expected) and r["historical_sha256_reconstructed"] == digest(old), "SPINE_DIGEST_DRIFT")
            require((ROOT / (direction.upper() + "_HISTORICAL_CANONICAL.json")).read_bytes() == wire(old), "HISTORICAL_BYTES_DRIFT")
            require(wire(load(direction.upper() + "_DERIVATION_PREIMAGES.json")) == wire(details), "DERIVATION_CUSTODY_DRIFT")
    else:
        cases = []
        def rejection(case_id, operation):
            try:
                operation()
            except ValueError as exc:
                cases.append({"id": case_id, "result": "REJECTED_AS_REQUIRED", "reason": str(exc)})
            else:
                raise ValueError("HOSTILE_FALSE_ACCEPT:" + case_id)
        for direction, (_, expected, _) in results.items():
            for key in ADD:
                bad = copy.deepcopy(expected); bad.pop(key)
                rejection(direction + ":OMIT:" + key, lambda b=bad,e=expected: validate_preimage(b,e,wire(b)))
                bad = copy.deepcopy(expected)
                bad[key] = ["UNAUTHORIZED_REF"] if isinstance(ADD[key], list) else (
                    [] if ADD[key] is None else (True if type(ADD[key]) is int else "CANONICAL_SET_ORDER"))
                rejection(direction + ":WRONG_VALUE:" + key, lambda b=bad,e=expected: validate_preimage(b,e,wire(b)))
            for key in ("release_refs", "source_universe_refs", "condition_binding_witness_ref_or_hash", "authority_refs"):
                bad = copy.deepcopy(expected)
                value = bad[key][0] if isinstance(bad[key],list) else bad[key]
                hash_key = "authority_content_hash" if key == "authority_refs" else "content_hash"
                value[hash_key] = "0" * 64
                rejection(direction + ":MUTATE:" + key, lambda b=bad,e=expected: validate_preimage(b,e,wire(b)))
            pretty = json.dumps(expected,indent=2).encode()
            rejection(direction + ":ALTER_SERIALIZATION", lambda e=expected,b=pretty: validate_preimage(e,e,b))
            unsorted = json.dumps(dict(reversed(list(expected.items()))),separators=(",", ":")).encode()
            rejection(direction + ":ALTER_KEY_ORDER", lambda e=expected,b=unsorted: validate_preimage(e,e,b))
            bad = copy.deepcopy(expected);bad["denominator_member_refs"].reverse()
            rejection(direction + ":ALTER_ARRAY_ORDER", lambda b=bad,e=expected: validate_preimage(b,e,wire(b)))
        rejection("OLD_OWNER_AS_CURRENT", lambda: lock_inputs({"adopted_owner.py": (ROOT / "INPUTS/historical_owner.py").read_bytes()}))
        for name in ("input_0.json", "input_3.json", "input_4.json", "r3_scope.json", "r8_spine.json"):
            data = (ROOT / "INPUTS" / name).read_bytes() + b" "
            rejection("MUTATED_INPUT_BLOB:" + name, lambda n=name,b=data: lock_inputs({n:b}))
        report = {"schema": "PYAT_AT07_INDEPENDENT_ORACLE_HOSTILES@1", "cases": cases,
                  "count": len(cases), "rejected": len(cases), "false_accepts": 0,
                  "method": "Independent derivation and exact byte verifier; every mutation rehashed to prevent stale-hash-only rejection",
                  "production_executed": False}
        print(json.dumps(report,indent=2))
        return
    print(json.dumps({"status": PASS, "mode": args.mode, "directions": {
        d: {"historical_sha256": digest(o), "successor_sha256": digest(n), "canonical_bytes": len(wire(n))}
        for d,(o,n,_) in results.items()}, "production_executed": False},indent=2))


if __name__ == "__main__":
    main()
