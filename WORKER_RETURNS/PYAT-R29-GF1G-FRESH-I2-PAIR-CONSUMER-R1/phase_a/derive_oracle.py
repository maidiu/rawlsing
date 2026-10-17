"""GF1G Phase A — independent oracle derivation.

Runs the PRE-GF1E R17 court (producer + fixture + frozen spec) with the GF1G
independent reference consumer, derives genuine 2x2 relations and hostile
rehashed relations, and emits 01_FROZEN_ORACLE.json.

This script is executed BEFORE the GF1E consumer or evidence is read.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path

FIELD = "0" * 64


def blob_sha1(data: bytes) -> str:
    h = hashlib.sha1()
    h.update(b"blob " + str(len(data)).encode() + b"\0" + data)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--court", required=True,
                    help="R17 return dir extracted at pre-GF1E 9f4a23ce")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    court = Path(args.court).resolve()
    repro = court / "court" / "repro"
    rt = court / "court" / "runtime_root"
    os.chdir(repro)
    sys.path[:0] = [str(repro), str(rt)]

    import gf1_bootstrap as GB                                    # noqa: E402
    import gf1_native as N                                        # noqa: E402
    import generic_native_pair_relation as G                      # noqa: E402
    from rawlsing_next._pre553_query_common import ExactRef       # noqa: E402
    from gf1_pair_support_consumer import compute_pair_support_signature as CONS  # noqa: E402

    assert G.__file__ == str((rt / "generic_native_pair_relation.py"))
    assert CONS.__module__ == "gf1_pair_support_consumer"
    assert str(Path(CONS.__code__.co_filename).resolve()).startswith(str(court))

    def cells(relation) -> dict:
        out = {}
        for row in relation.conditional_count_profile:
            for t in row["target_counts"]:
                out[f"{row['condition_state']}{t['target_state']}"] = t["joint_support_count"]
        return out

    def zero_map(relation) -> dict:
        out = {}
        for row in relation.conditional_count_profile:
            for t in row["target_counts"]:
                if t["joint_support_count"] == 0:
                    out[f"{row['condition_state']}|{t['target_state']}"] = t["joint_cell_state"]
        return out

    def snapshot(label, relation, *, extra=None):
        res = CONS(relation)
        d = {
            "label": label,
            "relation_object_id": relation.object_id,
            "relation_content_hash": relation.content_hash,
            "typed_state": relation.typed_state,
            "producer_state_blocking": relation.producer_state_blocking,
            "operation_role_order": relation.operation_role_order,
            "roles": {
                "CONDITIONER": {
                    "source_native_variable": relation.conditioner_source_native_variable,
                    "ref_object_id": G._ref_dict(relation.conditioner_ref).get("object_id"),
                    "domain": list(relation.conditioner_domain),
                },
                "TARGET": {
                    "source_native_variable": relation.target_source_native_variable,
                    "ref_object_id": G._ref_dict(relation.target_ref).get("object_id"),
                    "domain": list(relation.target_domain),
                },
            },
            "native_component_order": list(relation.native_component_order),
            "target_domain_identity": relation.target_domain_identity,
            "cells_00_01_10_11": cells(relation),
            "conditional_profile": [
                {
                    "condition_state": row["condition_state"],
                    "condition_denominator_support": row["condition_denominator_support"],
                    "targets": {t["target_state"]: t["joint_support_count"]
                                for t in row["target_counts"]},
                    "states": {t["target_state"]: t["joint_cell_state"]
                               for t in row["target_counts"]},
                }
                for row in relation.conditional_count_profile
            ],
            "eligible_joint_risk_total": relation.eligible_joint_risk_total,
            "excluded_ineligible_target_count": relation.excluded_ineligible_target_count,
            "joint_support_total": sum(cells(relation).values()),
            "zero_cell_semantics": zero_map(relation),
            "relation_permission_ceiling": list(relation.relation_permission_ceiling),
            "consumer": {
                "decision_state": res["decision_state"],
                "separation_class": res["separation_class"],
                "separation_signature": res["separation_signature"],
                "support_vectors": res["support_vectors"],
                "zero_cell_semantics": res["zero_cell_semantics"],
                "joint_support_total": res["joint_support_total"],
                "condition_states_with_positive_denominator":
                    res["condition_states_with_positive_denominator"],
                "eligible_joint_risk_total": res["eligible_joint_risk_total"],
                "result_hash": res["result_hash"],
                "generic_native_semantics_hold": res["generic_native_semantics_hold"],
                "downstream_value_produced": res["downstream_value_produced"],
                "read_relation_object_id": res["read_relation_object_id"],
                "read_relation_content_hash": res["read_relation_content_hash"],
                "read_relation_owner": res["read_relation_owner"],
                "is_population_evidence_not_actor_fact":
                    res["is_population_evidence_not_actor_fact"],
                "makes_no_causal_or_psychological_claim":
                    res["makes_no_causal_or_psychological_claim"],
                "production_owner_commit": res["production_owner_commit"],
            },
        }
        if extra:
            d.update(extra)
        return d

    # ---------------------------------------------------------- genuine chain
    genuine = {}
    all_runs = {}
    for profile in ("BASELINE", "R2_Y1", "R1_Y0"):
        bundle = N.run_native(profile=profile, root=GB.RT / f"gf1g_{profile.lower()}")
        items, _proofs = N.collect_link_material(bundle)
        rows = []
        for item in items:
            gen = G.produce_generic_native_pair_relation(
                joint_fact=item["fact"], joint_query=item["query"],
                conditioner_ref=item["query"].target_refs[0],
                target_ref=item["query"].target_refs[1],
                producer_permission_ceiling=("SOURCE_FREE_DEV",))
            res = snapshot(f"{profile}::{item['kind']}::{item['work_key']}", gen)
            res["work_key"] = item["work_key"]
            res["consumer_kind"] = item["kind"]
            rows.append(res)
            all_runs[(profile, item["work_key"], "forward")] = dict(
                gen=gen, fact=item["fact"], query=item["query"], item=item)
        genuine[profile] = rows

    # reverse X|Y under its own grant, baseline PAIR slot
    base_pair = next(r for r in genuine["BASELINE"]
                     if r["consumer_kind"] == "QUERY"
                     and r["roles"]["CONDITIONER"]["source_native_variable"] == "m01-X")
    rev_src = all_runs[("BASELINE", base_pair["work_key"], "forward")]
    reverse = G.produce_generic_native_pair_relation(
        joint_fact=rev_src["fact"], joint_query=rev_src["query"],
        conditioner_ref=rev_src["query"].target_refs[1],
        target_ref=rev_src["query"].target_refs[0],
        producer_permission_ceiling=("SOURCE_FREE_DEV",),
        reverse_pair_grant=G.REVERSE_PAIR_GRANT_ID)
    reverse_snap = snapshot("BASELINE::REVERSE_X_GIVEN_Y", reverse)
    reverse_snap["forward_object_id"] = base_pair["relation_object_id"]
    reverse_snap["forward_roles"] = base_pair["roles"]
    reverse_snap["forward_operation_role_order"] = base_pair["operation_role_order"]
    reverse_snap["roles_are_swapped"] = (
        reverse.conditioner_source_native_variable
        == base_pair["roles"]["TARGET"]["source_native_variable"]
        and reverse.target_source_native_variable
        == base_pair["roles"]["CONDITIONER"]["source_native_variable"])
    reverse_snap["object_id_differs_from_forward"] = \
        reverse.object_id != base_pair["relation_object_id"]

    # ---------------------------------------------------------- rehashed relations
    template = rev_src["gen"]
    template_fields = dict(template.__dict__)
    template_fields.pop("content_hash")
    template_fields.pop("object_id")

    def rebuild(*, profile_rows, typed="SUPPORTED", eligible=2,
                provenance=(), authority=()):
        f = dict(template_fields)
        f["conditional_count_profile"] = tuple(profile_rows)
        f["typed_state"] = typed
        f["producer_state_blocking"] = typed != "SUPPORTED"
        f["eligible_joint_risk_total"] = eligible
        if provenance:
            f["producer_provenance_refs"] = tuple(provenance)
        if authority:
            f["producer_authority_refs"] = tuple(authority)
        digest = G.semantic_hash(G._projection(f))
        return G.GenericNativePairRelation(
            **f, content_hash=digest,
            object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{digest}")

    def profile_of(counts, denoms=None, *, zero_state="ZERO_SUPPORT"):
        cdom = list(template.conditioner_domain)
        tdom = list(template.target_domain)
        rows = []
        for c in cdom:
            tcs = []
            for t in tdom:
                n = counts.get(f"{c}{t}", 0)
                tcs.append({
                    "target_state": t,
                    "source_native_target": template.target_source_native_variable,
                    "joint_support_count": n,
                    "joint_cell_state": "OBSERVED_POSITIVE" if n else zero_state,
                })
            rows.append({
                "condition_state": c,
                "source_native_conditioner": template.conditioner_source_native_variable,
                "condition_denominator_support": (
                    (denoms or {}).get(f"{c}", sum(x["joint_support_count"] for x in tcs))),
                "target_counts": tuple(tcs),
            })
        return rows

    synthetic = {}
    cases = {
        "collapsed_same_point_mass": dict(counts={"00": 1, "10": 1}),
        "nontrivial_partial": dict(counts={"00": 2, "01": 1, "10": 1, "11": 2}, eligible=6),
        "nontrivial_exact": dict(counts={"00": 2, "11": 2}, eligible=4),
        "observed_zeros_supported": dict(counts={"00": 1, "11": 1}),
        "all_zero_observed_zero": dict(
            counts={}, eligible=2, zero_state="OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"),
        "zero_support_typed": dict(counts={}, eligible=2, typed="ZERO_SUPPORT",
                                   zero_state="ZERO_SUPPORT"),
        "no_eligible_risk": dict(counts={}, eligible=0),
        "missing_target_state": dict(counts={}, eligible=0, typed="MISSING_TARGET_STATE"),
        "unresolved_target_state": dict(counts={}, eligible=0, typed="UNRESOLVED_TARGET_STATE"),
        "nonresponse": dict(counts={}, eligible=0, typed="NONRESPONSE"),
        "inconsistent_denominator": dict(
            counts={"00": 1, "11": 1}, denoms={"0": 2, "1": 1}),
        "support_exceeds_risk": dict(counts={"00": 1, "11": 1}, eligible=1),
    }
    for name, spec in cases.items():
        rows = [] if spec.get("typed", "SUPPORTED") != "SUPPORTED" else profile_of(
            spec["counts"], spec.get("denoms"),
            zero_state=spec.get("zero_state", "ZERO_SUPPORT"))
        rel = rebuild(profile_rows=rows, typed=spec.get("typed", "SUPPORTED"),
                      eligible=spec.get("eligible", 2))
        synthetic[name] = snapshot(f"SYNTHETIC::{name}", rel)

    # fully rehashed, internally consistent, externally unauthenticated relation
    forged_prov = ExactRef("GF1G_FORGED_PROVENANCE", "urn:gf1g:forged:provenance", FIELD)
    forged_auth = ExactRef("GF1G_FORGED_AUTHORITY", "urn:gf1g:forged:authority", FIELD)
    rows = profile_of({"00": 1, "11": 1})
    forged = rebuild(profile_rows=rows, eligible=2,
                     provenance=(forged_prov,), authority=(forged_auth,))
    forged_snap = snapshot("SYNTHETIC::fully_rehashed_self_authenticated", forged)
    forged_snap["forged_identity"] = {
        "producer_provenance_is_self_declared": True,
        "producer_authority_is_self_declared": True,
        "external_signature_present": False,
        "content_hash_recomputed_by_attacker": True,
        "required_consumer_privilege": "TEST_ONLY__NO_REAL_SOURCE_PRIVILEGE",
    }

    body = {
        "schema": "PYAT_R29_GF1G_PHASE_A_FROZEN_ORACLE@1",
        "status": "FROZEN_BEFORE_GF1E_INSPECTION",
        "author_class": "FRESH_INDEPENDENT_REVIEWER_NOT_GF1E_NOT_GF1F",
        "derivation": {
            "authority": [
                "R17 precommitted generic native pair oracle (contract level)",
                "R23 GF1C recovered consumer contract GF1_PAIR_SUPPORT_SIGNATURE_CONSUMER_TEST_ONLY@1.0.0",
                "unchanged original 44 frozen specification",
                "pre-GF1E generic producer generic_native_pair_relation.py",
                "GF1G independent reference consumer implemented from the above",
            ],
            "not_used": [
                "GF1E implementation source", "GF1E executed evidence",
                "GF1F expected results", "GF1E/GF1F conversation",
            ],
            "reference_44_result": "44 passed with the GF1G reference consumer in a "
                                   "pre-GF1E court copy (9f4a23cef + reference consumer only)",
        },
        "provenance": {
            "pre_gf1e_commit": "9f4a23cef1482e0a81afb1e7a65df90879931465",
            "court_root": str(court),
            "native_reattested": GB.REATTESTED,
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "imports": GB.import_custody()["imports"],
            "reference_consumer_sha256": hashlib.sha256(
                Path(CONS.__code__.co_filename).read_bytes()).hexdigest(),
            "reference_consumer_git_blob_sha1_of_pre_gf1e_court": blob_sha1(
                (rt / "generic_native_pair_relation.py").read_bytes()),
            "producer_sha256": hashlib.sha256(
                (rt / "generic_native_pair_relation.py").read_bytes()).hexdigest(),
            "frozen_spec_sha256": hashlib.sha256(
                (repro / "test_gf1_generic_pair.py").read_bytes()).hexdigest(),
            "accepted_owner_sha256": hashlib.sha256(
                (rt / "rawlsing_next/field_forge_conditional_support.py").read_bytes()).hexdigest(),
        },
        "separation_class_definition_frozen": {
            "EXACT_PAIR_SEPARATION": "every condition state with a positive denominator is a "
                                     "point mass on one target state and the point-mass targets "
                                     "differ across states",
            "NO_PAIR_SEPARATION": "positive risk and support exist but the profile is not an "
                                  "exact deterministic separation (identical or partial "
                                  "conditional distributions)",
            "UNDETERMINED_NO_ELIGIBLE_RISK": "at least one condition state has zero eligible "
                                             "denominator (and no zero-support determination "
                                             "takes precedence)",
            "UNDETERMINED_ZERO_SUPPORT_RISK": "eligible risk exists but observed joint support "
                                              "is zero, or the producer typed state is a zero "
                                              "state; a zero count is never silently promoted "
                                              "and never confused with missing/unresolved",
            "typed_refusals": "inconsistent per-condition denominator vs sum(target_counts), "
                              "support exceeding eligible risk, negative/noninteger counts, "
                              "zero/positive cell-state inconsistency => typed rejection before "
                              "any separation_class is computed",
        },
        "genuine_native_relations": genuine,
        "reverse_x_given_y": reverse_snap,
        "rehashed_test_only_relations": synthetic,
        "fully_rehashed_unauthenticated": forged_snap,
        "frozen_expectations": {
            "baseline_forward": "EXACT_PAIR_SEPARATION, cells 00/01/10/11 = 1/0/0/1, "
                                "per-condition denominators 1/1, joint eligible risk 2, "
                                "joint support total 2, zero cells stay "
                                "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET",
            "baseline_reverse": "EXACT_PAIR_SEPARATION under REVERSE_GRANTED with roles swapped "
                                "and a DIFFERENT relation object identity; same counts",
            "intervention_R2_Y0_to_1": "PAIR slot NO_ELIGIBLE_RISK (one condition has no "
                                       "eligible denominator); B slot reaches the frozen "
                                       "intervention cell set and is NO_PAIR_SEPARATION",
            "intervention_R1_Y1_to_0": "PAIR slot reaches frozen intervention cell set and is "
                                       "NO_PAIR_SEPARATION; B slot NO_ELIGIBLE_RISK",
            "discovery": "distinct eligible risk 1, different cells, not oracle constrained",
            "missing_unresolved_nonresponse": "typed HOLD, no separation class computed, no "
                                              "downstream value, generic hold retained",
            "zero_support": "UNDETERMINED_ZERO_SUPPORT_RISK, no positive promotion",
            "inconsistent_denominator": "typed rejection before classification",
            "support_exceeds_risk": "typed rejection before classification",
            "fully_rehashed": "structurally acceptable self-authenticated TEST_ONLY relation; "
                              "consumer MUST NOT grant real-source privilege; external issuer "
                              "authentication is NOT expressible in the relation schema",
        },
        "normative_scope": {
            "relation_identity_hashes": "NORMATIVE — derived from the pre-GF1E producer and real "
                                        "native chain; GF1E must reproduce bit-identical "
                                        "content_hash/object_id for the same inputs",
            "consumer_result_hashes": "REFERENCE_RELATIVE — the frozen contract does not fix a "
                                      "cross-implementation canonical result payload; GF1E must "
                                      "be deterministic, self-consistent and distinct across "
                                      "distinct semantics, but equality to the GF1G reference "
                                      "hash is not required",
            "separation_classes_and_counts": "NORMATIVE — fixed by the frozen spec and the "
                                             "pre-GF1E oracle, independently recomputed here",
        },
    }
    out = Path(args.out)
    out.write_text(json.dumps(body, indent=1, sort_keys=False) + "\n")
    print("wrote", out, "bytes", out.stat().st_size)
    print("reference consumer sha256", body["provenance"]["reference_consumer_sha256"])
    print("baseline class", genuine["BASELINE"][0]["consumer"]["separation_class"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
