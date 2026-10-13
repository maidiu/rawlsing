#!/usr/bin/env python3
"""HQ280 PV3 A05 - adversarial court for the independent no-drop oracle.

Every case builds an ADVERSARIALLY MUTATED manifest and asserts the oracle
actually FAILS with the expected failure code. The honest manifest and a stable
reordering must PASS. Exit 0 only if all expectations hold.
"""
import copy, json, sys
from a05_oracle import frozen_universe, honest_manifest, verify, h

U = frozen_universe()
HONEST = honest_manifest(U)
RESULTS = []


def check(case, expect_fail_codes, manifest, expect_pass=False):
    v = verify(U, manifest)
    codes = sorted({f["code"] for f in v.failures})
    if expect_pass:
        ok = v.ok
        detail = "PASS" if ok else f"unexpected failures {codes}"
    else:
        ok = (not v.ok) and all(c in codes for c in expect_fail_codes)
        detail = f"codes={codes}" + ("" if ok else f" expected>={expect_fail_codes}")
    RESULTS.append({"case": case, "expected": "PASS" if expect_pass else f"FAIL{codes if expect_pass else expect_fail_codes}",
                    "oracle_ok": v.ok, "failures": codes, "n_failures": len(v.failures),
                    "held_visible": True, "verdict": "OK" if ok else "ORACLE_INADEQUATE",
                    "detail": detail})
    return ok


def mut(fn):
    m = copy.deepcopy(HONEST)
    fn(m)
    return m


allok = True

# 0. honest control
allok &= check("H0_honest_manifest_passes", [], HONEST, expect_pass=True)

# T1. omission of a legal expected operation (false negative)
def t1(m):
    k = m["jobs"][1]["expected_work_key"]
    m["jobs"] = [j for j in m["jobs"] if j["expected_work_key"] != k]
allok &= check("T1_expected_operation_omitted", ["EXPECTED_OPERATION_OMITTED"], mut(t1))

# T2. missing-B / missing-J2 specifically (B1-R witnesses)
def t2(m):
    for j in list(m["jobs"]):
        if j["expected_work_key"] in (keyB, keyJ2):
            m["jobs"].remove(j)
keyB = next(e["expected_work_key"] for e in U["E"] if e["item"] == "B" and e["op_class"] == "UNARY_DISTRIBUTION")
keyJ2 = next(e["expected_work_key"] for e in U["E"] if e["target"] == "J2")
allok &= check("T2_missing_B_and_J2", ["EXPECTED_OPERATION_OMITTED"], mut(t2))

# T3. injected unauthorized extra job (false positive)
def t3(m):
    m["jobs"].append({"expected_work_key": h({"k": "FAKE"}), "count": 1,
                      "source": "FIXTURE-XOR-4CASE", "wave": "W1", "roles_pair": ("", "")})
    m["results"][h({"k": "FAKE"})] = {"result_type": "MEASURED_POSITIVE", "reported_success": True,
                                      "source_denominator": 8, "null_source": None}
allok &= check("T3_unauthorized_extra_job", ["UNAUTHORIZED_EXTRA_JOB"], mut(t3))

# T4. A-only projection while both source items eligible
def t4(m):
    m["jobs"] = [j for j in m["jobs"] if j["expected_work_key"] != keyB]
allok &= check("T4_A_only_projection", ["EXPECTED_OPERATION_OMITTED"], mut(t4))

# T5. wrong keys, same total count (same-count/different-key substitution)
def t5(m):
    n = len(m["jobs"])
    m["jobs"] = [{"expected_work_key": h({"k": "SUB", "i": i}), "count": 1,
                  "source": "FIXTURE-XOR-4CASE", "wave": "W1", "roles_pair": ("", "")} for i in range(n)]
    m["results"] = {j["expected_work_key"]: {"result_type": "MEASURED_POSITIVE", "reported_success": True,
                    "source_denominator": 8, "null_source": None} for j in m["jobs"]}
    m["products"] = [{"expected_work_key": j["expected_work_key"]} for j in m["jobs"]]
allok &= check("T5_same_count_different_keys", ["EXPECTED_OPERATION_OMITTED", "UNAUTHORIZED_EXTRA_JOB"], mut(t5))

# T6. false empirical null from AUTHORITY_UNAVAILABLE / zero denominator
def t6(m):
    k = m["jobs"][0]["expected_work_key"]
    m["results"][k] = {"result_type": "MEASURED_NULL", "null_source": "AUTHORITY_UNAVAILABLE",
                       "reported_success": True, "source_denominator": 8}
allok &= check("T6_false_null_from_authority_unavailable", ["FALSE_EMPIRICAL_NULL"], mut(t6))

def t6b(m):
    k = m["jobs"][0]["expected_work_key"]
    m["results"][k] = {"result_type": "MEASURED_NULL", "null_source": "ZERO_DENOMINATOR",
                       "reported_success": True, "source_denominator": 0}
allok &= check("T6b_false_null_from_zero_denominator", ["FALSE_EMPIRICAL_NULL"], mut(t6b))

# T7. partial/adaptive unvisited called success
def t7(m):
    k = m["jobs"][0]["expected_work_key"]
    m["results"][k] = {"result_type": "PARTIAL", "reported_success": True,
                       "source_denominator": 8, "null_source": None}
allok &= check("T7_partial_reported_as_success", ["PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS"], mut(t7))
def t7b(m):
    k = m["jobs"][0]["expected_work_key"]
    m["results"][k] = {"result_type": "UNVISITED", "reported_success": True,
                       "source_denominator": 8, "null_source": None}
allok &= check("T7b_unvisited_reported_as_success", ["PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS"], mut(t7b))

# T8. candidate own-_dk approved as co-travel
def t8(m):
    m["jobs"].append({"expected_work_key": h({"k": "DKJOINT"}), "count": 1,
                      "source": "FIXTURE-XOR-4CASE", "wave": "W1",
                      "roles_pair": ("v176", "v176_dk")})
    m["results"][h({"k": "DKJOINT"})] = {"result_type": "MEASURED_POSITIVE", "reported_success": True,
                                         "source_denominator": 8, "null_source": None}
allok &= check("T8_candidate_own_dk_joint", ["CANDIDATE_OWN_DK_JOINT", "UNAUTHORIZED_EXTRA_JOB"], mut(t8))

# T9. expectation derived from the output manifest
def t9(m):
    m["expected_derived_from"] = "EMITTED_MANIFEST"
allok &= check("T9_expected_set_output_derived", ["EXPECTED_SET_OUTPUT_DERIVED"], mut(t9))

# T10. required consumer omitted although the product is present
def t10(m):
    m["consumers"] = m["consumers"][:-1]
allok &= check("T10_required_consumer_omitted", ["REQUIRED_CONSUMER_OMITTED"], mut(t10))

# T11. held obligation executed / not visible (holder schedule excludes held work)
def t11(m):
    m["jobs"].append({"expected_work_key": U["H"][0]["expected_work_key"], "count": 1,
                      "source": "FIXTURE-XOR-4CASE", "wave": "W1", "roles_pair": ("", "")})
allok &= check("T11_held_work_executed", ["HELD_OR_DENIED_WORK_EXECUTED", "UNAUTHORIZED_EXTRA_JOB"], mut(t11))
def t11b(m):
    m["visible_documentary_items"] = []
allok &= check("T11b_held_work_not_visible", ["HELD_OR_DENIED_WORK_NOT_VISIBLE"], mut(t11b))

# T12. backward / wrong source identity
def t12(m):
    for j in m["jobs"]:
        j["source"] = "OTHER-SOURCE"
allok &= check("T12_source_identity_mismatch", ["SOURCE_IDENTITY_MISMATCH"], mut(t12))

# T13. STABLE REORDER must still PASS (order invariance)
def t13(m):
    m["jobs"] = list(reversed(m["jobs"]))
    m["products"] = list(reversed(m["products"]))
    m["consumers"] = list(reversed(m["consumers"]))
allok &= check("T13_stable_reordered_expected_set_passes", [], mut(t13), expect_pass=True)

# T14. multiplicity
def t14(m):
    m["jobs"][0]["count"] = 2
allok &= check("T14_multiplicity_mismatch", ["EXPECTED_MULTIPLICITY_MISMATCH"], mut(t14))

print(json.dumps({"schema": "HQ280_PV3_A05_HOSTILE_RESULTS@1",
                  "universe_frontier_digest": U["frontier_digest"],
                  "expected_runnable_operations": len(U["E"]),
                  "held": len(U["H"]), "denied": len(U["D"]), "source_nonapplicable": len(U["NA"]),
                  "cases": len(RESULTS), "all_expectations_met": bool(allok),
                  "results": RESULTS}, indent=1))
sys.exit(0 if allok else 1)
