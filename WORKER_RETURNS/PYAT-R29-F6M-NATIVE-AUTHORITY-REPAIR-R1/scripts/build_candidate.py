"""Rebuild the bounded F6M producer from the exact original; fail if patch sites drift."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'inherited/F6J/01_STAGED_NATIVE/rawlsing_next'
dest=ROOT/'candidate/rawlsing_next'
dest.mkdir(parents=True,exist_ok=True)
shutil.copyfile(src/'pre553_empirical_objects.py',dest/'pre553_empirical_objects.py')
s=(src/'pre553_heterogeneous_synthesis.py').read_text()
def replace(old,new):
 global s
 assert s.count(old)==1,old[:100]
 s=s.replace(old,new)
replace('distribution. Real use requires an external owner admission callback, including\nscope/operation/permissions verification. Hashes are replay identities, not rights.',
'''distribution. This source-free implementation has NO authenticated owner issuer.
An admission callback is only an unverified integration predicate, never rights.
All output is experimental only, even when callers declare real source origin.
Hashes are replay identities, not rights.''')
replace('METHOD = "PRE553_TARGET_JOINT_STANDARDIZATION@1"','''METHOD = "PRE553_TARGET_JOINT_STANDARDIZATION@1"
IMPLEMENTATION_VERSION = "F6M_NATIVE_DECISION_ADMISSION_REPAIR@1"
REAL_USE_STATUS = "UNVERIFIED_INTEGRATION_BOUNDARY"
ORIGINAL_PRODUCER_BLOB = "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"''')
replace('''    Real summaries need owner-verified admission for baseline AND transport. A
    callback is an integration boundary, not an authentication implementation.
    Unknown overlap excludes the candidate, while lawful baselines survive.''','''    The callback may veto baseline or transport computations but cannot grant
    real-use rights. Caller origin labels are declarations only. Numerical
    output is source-free experimental evidence; real use always fails closed.
    Unknown overlap excludes the candidate, while native baselines survive.''')
replace('"real_source_qualification": "EXTERNAL_REVIEW_REQUIRED",','''"real_source_qualification": REAL_USE_STATUS,
           "implementation_version": IMPLEMENTATION_VERSION,
           "owner_admission_status": REAL_USE_STATUS,
           "real_use_authorized": False,
           "use_scope": "SOURCEFREE_EXPERIMENT_ONLY",
           "origin_classification": ("DECLARED_TEST_ONLY" if all(s["test_origin"] for s in sources)
                                     else "MIXED_TEST_AND_UNVERIFIED" if any(s["test_origin"] for s in sources)
                                     else "UNVERIFIED_SOURCE_INPUT"),
           "support_gate_semantics": "AGGREGATE_SOURCE_STRATUM_RAW_COUNT_NOT_MINORITY_CELL_PROTECTION",''')
replace('"authority_ceiling": "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE"','''"source_id": s["source_id"], "source_hash": b["input_hash"],
            "authority_ceiling": "TEST_ONLY" if s["test_origin"] else "UNVERIFIED"''')
replace('''                "value_ref": "baseline/" + s["source_id"] + "/mapped_joint"})''','''                "producer_ref": s["product_ref"], "source_id": s["source_id"],
                "source_hash": b["input_hash"],
                "authority_ceiling": "TEST_ONLY" if s["test_origin"] else "UNVERIFIED",
                "value_hash": semantic_hash(b["mapped_joint"]),
                "value_ref": "baseline/" + s["source_id"] + "/mapped_joint"})''')
replace('''        denom = sum(weights[s["source_id"]] for s in eligible)
        coverage[z] = {"target_share": str(share), "sources": [], "excluded_sources": [s["source_id"] for s in sources if s not in eligible]}
        if not denom:''','''        # Preserve the planned mixture contribution of a PRESENT source stratum
        # failing the aggregate support gate. Renormalizing its weight onto
        # survivors would silently change the estimand. A source with no table
        # remains outside the inherited stratum-specific mixture definition.
        planned = [s for s in sources if z in s["strata"]]
        denom = sum(weights[s["source_id"]] for s in planned)
        eligible_weight = sum(weights[s["source_id"]] for s in eligible)
        missing_share = share * (1 - eligible_weight / denom) if denom else share
        covered_share = share - missing_share
        uncovered += missing_share
        coverage[z] = {"target_share": str(share), "sources": [],
                       "excluded_sources": [s["source_id"] for s in sources if s not in eligible],
                       "uncovered_target_share": str(missing_share),
                       "support_gate": "AGGREGATE_SOURCE_STRATUM_RAW_COUNT",
                       "minority_cell_protection": False,
                       "exclusion_reasons": {
                           s["source_id"]: ("NO_SOURCE_STRATUM" if z not in s["strata"]
                                            else "AGGREGATE_SUPPORT_OR_MASS_INSUFFICIENT")
                           for s in sources if s not in eligible}}
        if missing_share:
            unknown_variance = True
            for k in keys:
                upper[k] += missing_share
        if not eligible_weight:''')
replace('''            uncovered += share
            unknown_variance = True
            for k in keys:
                upper[k] += share
            continue''','''            continue''')
replace('''            lower[k] += share * min(p[k] for p in distributions)
            upper[k] += share * max(p[k] for p in distributions)''','''            lower[k] += covered_share * min(p[k] for p in distributions)
            upper[k] += covered_share * max(p[k] for p in distributions)''')
replace('"authority_ceiling": "DESCRIPTIVE_SOCIOLOGICAL_MODEL_ONLY"','''"source_hashes": {b["source_id"]: b["input_hash"] for b in baseline},
        "authority_ceiling": "TEST_ONLY" if out["test_origin"] else "UNVERIFIED"''')
replace('''    out["decision"] = "SYNTHETIC_CANDIDATE" if out["test_origin"] else "INFERRED_CANDIDATE_REQUIRES_REVIEW"''','''    out["decision"] = ("PARTIAL_IDENTIFICATION_ONLY" if candidate["distribution"] is None or uncovered > 0
                       else "SYNTHETIC_CANDIDATE" if out["test_origin"]
                       else "INFERRED_CANDIDATE_REQUIRES_REVIEW")
    out["target_joint_status"] = ("NO_COMPLETE_TARGET_JOINT" if candidate["distribution"] is None
                                  else "COMPLETE_EXPERIMENTAL_TARGET_JOINT")''')
replace('def conditional(bundle: dict, conditions: dict[str, str], outcome: str) -> dict:',
'''def conditional(bundle: dict, conditions: dict[str, str], outcome: str,
                *, use: str = "SOURCEFREE_EXPERIMENT") -> dict:''')
replace('''    c = bundle.get("candidate")
    if c is None or c["distribution"] is None:''','''    if use not in ("SOURCEFREE_EXPERIMENT", "REAL_USE"):
        raise SynthesisError("unknown consumer use scope")
    # No bundle field, origin flag, hash or callback authenticates an issuer.
    if use == "REAL_USE":
        return {"state": "UNAVAILABLE", "reason": "UNVERIFIED_OWNER_ADMISSION",
                "real_use_authorized": False, "bundle_hash": bundle["content_hash"]}
    c = bundle.get("candidate")
    if c is None or c["distribution"] is None or _q(c["uncovered_target_mass"]) > 0:''')
replace('''              "evidence_mode": "INFERRED", "conditions": conditions, "outcome": outcome,''','''              "evidence_mode": "INFERRED", "conditions": conditions, "outcome": outcome,
              "use_scope": "SOURCEFREE_EXPERIMENT_ONLY", "real_use_authorized": False,
              "owner_admission_status": REAL_USE_STATUS,''')
(dest/'pre553_heterogeneous_synthesis.py').write_text(s)
print('Built',dest.relative_to(ROOT))
