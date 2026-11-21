"""Pure, measured (not projected by source science) storage economics comparison.

All values are derived from actual report stage time, permanent bytes and
1/10/100 distinct physical observation operations. No default winner;
the exact original I03/authority and downstream gate is separate.
"""
from __future__ import annotations

from statistics import median

from .stores import ARMS

def _warm(report):
    matrix=report.get("query_report",{}).get("steady_state_matrix",[])
    available=[row for row in matrix if row.get("status")=="PHYSICAL_ONLY_NO_SCIENTIFIC_ISSUANCE"]
    if not available:
        return None
    return max(available,key=lambda x:x["distinct_requested"])

def measured_economics(reports, *, source_bytes: int, committed_original_source: bool = True):
    rows={}
    for name in ARMS:
        r=reports.get(name)
        if r is None or r.get("status")!="COMPLETED_PHYSICAL_AND_NATIVE_WHERE_ISSUED":
            rows[name]={"status":"INCOMPLETE_NO_ECONOMIC_JUDGMENT"}
            continue
        st=r["stages_s"]
        m=r["metrics"]
        raw=r.get("query_report",{})
        warm=_warm(r)
        cold=[x["elapsed_s"] for x in raw.get("fresh_process_probes",[])
              if x.get("grade")=="PHYSICAL_REOPEN_NOT_SOURCE_AUTHORIZED_NATIVE_I03"]
        rebuild=st["build_from_already_saved_c11"]+st.get("publish_commit",0)
        audit=st.get("full_corpus_body_audit",0)
        permanent=m["required_permanent_bytes"]
        number=warm["distinct_requested"] if warm else 0
        warm_total_ms=warm["total_ms"] if warm else None
        avg_ms=warm_total_ms/number if number else None
        count=m.get("objects",0)
        rows[name]={
            "status":"MEASURED_PHYSICAL_ONLY",
            "one_time_build_s":round(rebuild,4),
            "one_time_full_body_audit_s":round(audit,4),
            "build_plus_audit_s":round(rebuild+audit,4),
            "retained_bytes_required_for_queries":permanent,
            "retained_bytes_per_canonical_record":round(permanent/count,3) if count else None,
            "original_parquet_required_after_build":name=="H",
            "observed_distinct_questions":number,
            "observed_distinct_warm_query_total_ms":warm_total_ms,
            "mean_warm_physical_query_ms":round(avg_ms,4) if avg_ms is not None else None,
            "fresh_process_physical_open_plus_probe_s_median":round(median(cold),4) if cold else None,
            "cold_process_count":len(cold),
            "evidence_reference_sample_grade":"EXACT_REF_AND_CANONICAL_BODY_NOT_NATIVE_FACT",
            "native_scientific_claim":"NOT_ESTABLISHED_BY_PHYSICAL_ECONOMICS",
        }
    h=rows.get("H",{})
    if h.get("status")=="MEASURED_PHYSICAL_ONLY":
        for name in ("S1","S2","S3"):
            candidate=rows[name]
            if candidate.get("status")!="MEASURED_PHYSICAL_ONLY":
                continue
            diff_build=(candidate["build_plus_audit_s"]-h["build_plus_audit_s"])
            diff_query=(h["mean_warm_physical_query_ms"]-
                        candidate["mean_warm_physical_query_ms"])/1000 if (
                            h["mean_warm_physical_query_ms"] is not None
                            and candidate["mean_warm_physical_query_ms"] is not None) else None
            if diff_query is None or not candidate["observed_distinct_questions"]:
                be="UNAVAILABLE_NO_COMPARABLE_DISTINCT_PHYSICAL_QUERIES"
            elif diff_query>0 and diff_build>0:
                from math import ceil
                be=ceil(diff_build/diff_query)
            elif diff_query>0 and diff_build<=0:
                be=0
            elif diff_query<=0 and diff_build>0:
                be="NO_QUERY_COUNT_BREAK_EVEN_AT_MEASURED_PHYSICAL_RATE"
            else:
                be="ALREADY_FASTER_BUILD_BUT_SLOWER_QUERY_OR_EQUAL"
            candidate["versus_H"]={
                "saved_retained_bytes":h["retained_bytes_required_for_queries"]-
                                       candidate["retained_bytes_required_for_queries"],
                "extra_build_plus_audit_s":round(diff_build,4),
                "saved_seconds_per_physical_query":round(diff_query,6)
                         if diff_query is not None else None,
                "physical_query_break_even_count":be,
                "warning":"PHYSICAL_PROFILE_ONLY; source-first native I03, cold proof and source rights excluded",
            }
    valid=[x for x in rows.values() if x.get("status")=="MEASURED_PHYSICAL_ONLY"]
    return {
        "kind":"NONAUTHORITATIVE_PHYSICAL_STORAGE_ECONOMICS",
        "all_four_measured":len(valid)==4,
        "original_c11_source_bytes_retained":source_bytes,
        "original_source_shared_not_charged_four_times":committed_original_source,
        "individual_arm_costs":rows,
        "storage_selection":"HELD_UNTIL_NATIVE_ISSUER_ALL13_FAMILIES_SOURCE_SCIENCE_AND_DOWNSTREAM_PARITY",
    }
