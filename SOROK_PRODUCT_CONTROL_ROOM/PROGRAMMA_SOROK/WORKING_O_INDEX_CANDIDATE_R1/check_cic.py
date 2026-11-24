"""CIC documentary correspondence validation; no scientific/runtime authority."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CIC = ROOT / "CONSTITUTIVE_IMPLEMENTATION_COVERAGE_R1.json"
def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))
def require(ok, reason):
    if not ok:
        raise ValueError(reason)
def git_blob(path):
    b = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
REVIEW_DIMENSIONS = ["architectural_fidelity","implementation_correctness","causal_adequacy","integration","computational_economy","historical_inheritance","independent_review"]
REVIEW_STATES = {"NOT_REVIEWED", "PARTIALLY_REVIEWED", "REVIEWED_AT_SHA"}
def check_review_entry(entry):
    require(entry["status"] in REVIEW_STATES, "INVALID_REVIEW_STATE")
    require(isinstance(entry["reviewed_scope"], list), "REVIEW_SCOPE")
    require(bool(entry["outstanding_scope"]) or entry["status"] == "REVIEWED_AT_SHA", "DROPPED_DEFERRED_REVIEW")
    if entry["status"] == "NOT_REVIEWED":
        require(not entry["reviewed_scope"] and not entry["receipts"] and entry["refinement_disposition"] == "OPEN_CONSERVED", "FALSE_REVIEW_PROMOTION")
    else:
        require(bool(entry["reviewed_scope"]) and bool(entry["receipts"]), "REVIEW_RECEIPT_REQUIRED")
        for receipt in entry["receipts"]:
            require(all(receipt.get(k) for k in ("reviewer", "source_sha", "scope", "method_depth", "verdict", "limits", "evidence", "independence")), "REVIEW_RECEIPT_REQUIRED")
        if entry["status"] == "REVIEWED_AT_SHA":
            require(not entry["outstanding_scope"] and entry["refinement_disposition"] == "DISCHARGED_WITH_RECEIPT", "UNREVIEWED_RESIDUAL")
        else:
            require(entry["refinement_disposition"] == "OPEN_CONSERVED", "DROPPED_DEFERRED_REVIEW")

def validate(c, ledger, registry, pinned=True):
    ids = {r["id"] for r in registry["rows"]}
    obs = {r["pr"]: r for r in ledger["records"]}
    links = {(r["pr"], f["original_id"]): f for r in ledger["records"] for f in r.get("functional_relationships", [])}
    require(len(ids) == 144, "ORIGINAL_FUNCTION_DENOMINATOR")
    if pinned:
        require(c["source_contract"]["o_index"]["ledger_blob"] == git_blob(ROOT / "LIVE_RECEIVING_LEDGER.json"), "LEDGER_DRIFT_HOLD")
        require(c["source_contract"]["o_index"]["registry_blob"] == git_blob(ROOT / "01_SOURCE_OF_TRUTH_REGISTRY.json"), "REGISTRY_DRIFT_HOLD")
    obligations = {o["id"]:o for o in c["obligations"]}
    require(len(obligations) == len(c["obligations"]) == c["counts"]["obligations"], "OBLIGATION_ID")
    criteria = {}
    debt_ids = set()
    debt_refs = []
    review_counts = {}
    dimensions = {"theory_interpretation", "historical_inheritance", "current_implementation", "actual_consumer", "integrated", "demonstrated", "independent_review", "scientific_fidelity", "source_authority", "actor_authority", "human_authority", "received"}
    for oid, o in obligations.items():
        require(set(o["function_refs"]) <= ids and bool(o["function_refs"]), "UNKNOWN_FUNCTION")
        require(o["function_refs"] == o["programme09_ids"] == o["programme19_function_ids"], "FUNCTION_CROSSWALK")
        require(o["lane"] in c["homes"], "UNKNOWN_HOME")
        for q in o["criteria"]:
            require(q["id"] not in criteria and q["id"].startswith(oid+"."), "CRITERION_ID")
            criteria[q["id"]] = q
            require(set(q["dimensions"]) == dimensions, "EVIDENCE_DIMENSIONS")
            require(q["dimensions"]["received"] == "NOT_RECEIVED_AS_CIC_CRITERION", "FALSE_RECEIVING")
            require(q["dimensions"]["demonstrated"] == "NO_NEW_CRITERION_EXECUTION", "FALSE_EXECUTION")
            require(q["dimensions"]["independent_review"] == "NOT_ISSUED_FOR_CIC_CRITERION", "FALSE_INDEPENDENT_REVIEW")
            require(all(q["dimensions"][k] == "NO_NEW_GRANT" for k in ("source_authority","actor_authority","human_authority")), "FALSE_AUTHORITY")
            require(bool(q["acceptance_candidate"] and q["remaining_boundary"] and q["falsifier"] and q["evidence"]), "EMPTY_COURT")
            rv = q["review_coverage"]
            require(rv["implementation_coverage"] == q["dimensions"]["current_implementation"] and rv["execution_coverage"] == q["dimensions"]["demonstrated"], "COVERAGE_AXIS_DRIFT")
            require(set(rv["dimensions"]) == set(REVIEW_DIMENSIONS), "REVIEW_DIMENSION_DROP")
            require(rv["status"] == "NOT_REVIEWED", "FALSE_CRITERION_REVIEW_PROMOTION")
            require(len(rv["related_evidence"]) == len(q["evidence"]), "PRIOR_REVIEW_RECEIPT_DROP")
            for related, e in zip(rv["related_evidence"], q["evidence"]):
                require(e["observed_head"] == obs[e["pr"]]["head_sha"], "EVIDENCE_SCOPE_DRIFT")
                prior = obs[e["pr"]]["review"]
                require(related["lookup"] == e["lookup"] and related["source_head"] == e["observed_head"] and related["prior_review_sha"] == prior.get("sha") and related["prior_review_verdict"] == prior.get("verdict","UNKNOWN"), "PRIOR_REVIEW_RECEIPT_DRIFT")
            for entry in rv["dimensions"].values():
                check_review_entry(entry)
                review_counts[entry["status"]] = review_counts.get(entry["status"],0)+1
                require(entry["status"] == "NOT_REVIEWED", "NEW_REVIEW_NOT_RECEIVED_IN_THIS_CUT")
            for debt in rv["deferred_source_scopes"]:
                require(debt["id"] not in debt_ids, "DUPLICATE_REVIEW_DEBT")
                debt_ids.add(debt["id"])
                debt_refs.extend(debt["related_criterion_ids"])
                require(debt["dimension"] in REVIEW_DIMENSIONS and bool(debt["scope"]) and debt["source"]["head"] and debt["source"]["comment"] and debt["source"]["consumer"], "REVIEW_SOURCE_SCOPE")
                # Named debt has a single outstanding text; use same structural checks.
                check_review_entry(debt)
                require(debt["status"] == "NOT_REVIEWED", "NEW_REVIEW_NOT_RECEIVED_IN_THIS_CUT")
            for e in q["evidence"]:
                k = (e["pr"], e["original_id"])
                require(k in links and e["observed_head"] == obs[e["pr"]]["head_sha"] and e["relationship_grade"] == links[k]["grade"], "EVIDENCE_SCOPE_DRIFT")
                if e["pr"] in (1298,1300):
                    require(q["criterion_status"] == "RELATED_EXECUTION_AFFECTED_BY_REJECTED_DEPENDENCY", "R30_FALSE_PROMOTION")
                require(e["pr"] != 1294, "REJECTED_R30_AS_POSITIVE")
    require(len(criteria) == c["counts"]["criteria"], "CRITERION_COUNT")
    rc = c["counts"]["review_coverage"]
    require(review_counts == rc["criterion_dimension_status_counts"] and sum(review_counts.values()) == len(criteria)*len(REVIEW_DIMENSIONS) == rc["dimension_count"], "REVIEW_COUNT_DRIFT")
    required_debts = ["R33-FORMATION","R33-COACTION","R32-REVALUATION","R31-REINSTATEMENT","R33-ANONYMOUS","R33-P6-MIII","R33-GEOMETRY","R33-ATTENTION","R33-ECONOMY","R6-SENSORY","R6-MII-PRIVATE","R6-RELATIONSHIP","R6-ROOT-FORK","R33-JOIN","R6-ENCOUNTER","R6-ECONOMY"]
    require(set(required_debts) <= debt_ids and len(debt_ids) == rc["explicit_deferred_source_scopes"], "DROPPED_NAMED_REVIEW_DEBT")
    require(set(debt_refs) <= set(criteria), "REVIEW_CRITERION_LINK")
    require(len(links) == c["source_contract"]["o_index"]["relationships"], "RELATIONSHIP_COUNT_DRIFT")
    seen = set()
    for lane, rows in c["paragraph_routes"].items():
        require(len(rows) == c["counts"]["active_source_blocks"][lane], "SOURCE_ROUTE_COUNT")
        last=0
        for row in rows:
            require(row["source_anchor"] not in seen, "DUPLICATE_SOURCE_ANCHOR")
            seen.add(row["source_anchor"])
            require(last < row["start_line"] <= row["end_line"] <= c["homes"][lane]["active_end_line"], "SOURCE_RANGE")
            last=row["end_line"]
            require(row["route_grade"].startswith("PROVISIONAL_RANGE_ROUTE"), "FALSE_SEMANTIC_RECEIVING")
            require(bool(row["exact_opening"]) and row["characters"] >= len(row["exact_opening"]), "EMPTY_SOURCE_ROUTE")
            require(bool(row["obligation_ids"]), "UNROUTED_SOURCE")
            for oid in row["obligation_ids"]:
                require(oid in obligations and obligations[oid]["lane"] == lane, "WRONG_ROUTE_HOME")
                rr=obligations[oid]["home_range"]
                require(rr["start_line"] <= row["start_line"] <= row["end_line"] <= rr["end_line"], "WRONG_ROUTE_RANGE")
    for lane in c["homes"]:
        ranges=sorted((o["home_range"]["start_line"],o["home_range"]["end_line"]) for o in obligations.values() if o["lane"]==lane)
        require(ranges[0][0] == 1 and ranges[-1][1] == c["homes"][lane]["active_end_line"], "HOME_RANGE_BOUNDARY")
        require(all(a[1]+1==b[0] for a,b in zip(ranges,ranges[1:])), "HOME_RANGE_GAP")
    route_by_anchor = {r["source_anchor"]: r for rows in c["paragraph_routes"].values() for r in rows}
    refined = {q["id"]: q for q in criteria.values() if "refines" in q}
    for qid, q in refined.items():
        oid = qid.rsplit(".", 1)[0]
        require(q["refines"] in criteria and q["refines"].rsplit(".", 1)[0] == oid and q["refines"] not in refined, "REFINEMENT_PARENT_DRIFT")
        require(bool(q["paragraph_anchors"]) and all(a in route_by_anchor and oid in route_by_anchor[a]["obligation_ids"] for a in q["paragraph_anchors"]), "REFINEMENT_SOURCE_ANCHOR_DRIFT")
        require(all(e["original_id"] in obligations[oid]["function_refs"] for e in q["evidence"]), "REFINEMENT_FUNCTION_CROSSWALK")
        sr = q["scoped_return"]
        source = obs[sr["pr"]]
        require(sr["pr"] == q["evidence"][0]["pr"] and sr["execution_sha"] == source["test"]["executed_sha"] and sr["execution_grade"] == source["test"]["grade"] and sr["receipt"] == source["test"]["receipt"] and sr["first_consumer"] == source["first_consumer"], "REFINEMENT_RETURN_DRIFT")
        require(sr["source_bodies"] == [{"path": b["path"], "blob": b["blob"]} for b in source["exact_source_bodies"]], "REFINEMENT_SOURCE_BODY_DRIFT")
        require(sr["criterion_execution"] == "NOT_RUN_AS_COMPLETE_CIC_CRITERION" and sr["review"] == "NOT_INDEPENDENTLY_REVIEWED_AT_CRITERION_SCOPE", "REFINEMENT_FALSE_PROMOTION")
    rounds = c.get("refinement_rounds", [])
    require(len(rounds) == 1 and set(rounds[0]["added_criterion_ids"]) == set(refined) and rounds[0]["prior_criterion_count"] + len(refined) == len(criteria), "REFINEMENT_DENOMINATOR_DRIFT")
    for j in c["whole_organism_acceptance_candidates"]:
        require(set(j["obligation_ids"]) <= set(obligations) and set(j["criterion_ids"]) <= set(criteria), "JOIN_REFERENCES")
        require(j["state"] == "HELD_CRITERION_SPECIFIC_WHOLE_TRAJECTORY", "FALSE_WHOLE_TRAJECTORY")
    return {"obligations":len(obligations),"criteria":len(criteria),"routed_source_blocks":len(seen),"review_dimensions":sum(review_counts.values()),"named_open_review_scopes":len(debt_ids),"mode":"DOCUMENTARY_CORRESPONDENCE_NOT_SEMANTIC_OR_RUNTIME_ACCEPTANCE"}

def selftest(c,ledger,registry):
    def check(mut,code):
        x=copy.deepcopy(c);mut(x)
        try: validate(x,ledger,registry,pinned=False)
        except ValueError as e: require(str(e)==code,"WRONG_REFUSAL:"+str(e));return
        raise ValueError("MUTANT_ACCEPTED:"+code)
    check(lambda x:x["obligations"][0]["function_refs"].append("INVENTED_FUNCTION"),"UNKNOWN_FUNCTION")
    check(lambda x:x["obligations"][0]["criteria"][0]["dimensions"].update(received="RECEIVED"),"FALSE_RECEIVING")
    check(lambda x:x["obligations"][0]["criteria"][0]["dimensions"].update(demonstrated="PASS"),"FALSE_EXECUTION")
    check(lambda x:x["obligations"][0]["criteria"][0]["evidence"][0].update(observed_head="0"*40),"EVIDENCE_SCOPE_DRIFT")
    check(lambda x:x["paragraph_routes"]["CO"].pop(),"SOURCE_ROUTE_COUNT")
    check(lambda x:x["paragraph_routes"]["CO"][0].update(obligation_ids=["NEIGHBOR-CIC-001"]),"WRONG_ROUTE_HOME")
    check(lambda x:x["paragraph_routes"]["CO"][0].update(route_grade="ACCEPTED"),"FALSE_SEMANTIC_RECEIVING")
    check(lambda x:next(q for o in x["obligations"] for q in o["criteria"] if q["evidence"][0]["pr"]==1300).update(criterion_status="PASS"),"R30_FALSE_PROMOTION")
    check(lambda x:x["whole_organism_acceptance_candidates"][0].update(state="PASS"),"FALSE_WHOLE_TRAJECTORY")
    check(lambda x:x["obligations"][0]["criteria"][0]["review_coverage"]["dimensions"].pop("integration"),"REVIEW_DIMENSION_DROP")
    check(lambda x:x["obligations"][0]["criteria"][0]["review_coverage"]["dimensions"]["integration"].update(outstanding_scope=[]),"DROPPED_DEFERRED_REVIEW")
    check(lambda x:x["obligations"][0]["criteria"][0]["review_coverage"]["dimensions"]["integration"].update(status="REVIEWED_AT_SHA"),"REVIEW_RECEIPT_REQUIRED")
    check(lambda x:x["obligations"][0]["criteria"][0]["review_coverage"]["related_evidence"][0].update(prior_review_sha="0"*40),"PRIOR_REVIEW_RECEIPT_DRIFT")
    check(lambda x:next(q for o in x["obligations"] for q in o["criteria"] if q["review_coverage"]["deferred_source_scopes"])["review_coverage"]["deferred_source_scopes"].pop(),"DROPPED_NAMED_REVIEW_DEBT")
    check(lambda x:x["obligations"][0]["criteria"][0]["review_coverage"].update(execution_coverage="PASS"),"COVERAGE_AXIS_DRIFT")
    def child(x):
        return next(q for o in x["obligations"] for q in o["criteria"] if "refines" in q)
    check(lambda x:child(x).update(refines="NEIGHBOR-CIC-017.01"),"REFINEMENT_PARENT_DRIFT")
    check(lambda x:child(x).update(paragraph_anchors=["NEIGHBOR-L0309"]),"REFINEMENT_SOURCE_ANCHOR_DRIFT")
    check(lambda x:child(x)["scoped_return"].update(execution_sha="0"*40),"REFINEMENT_RETURN_DRIFT")
    check(lambda x:child(x)["scoped_return"].update(criterion_execution="PASS"),"REFINEMENT_FALSE_PROMOTION")
    return 19
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--function")
    p.add_argument("--obligation")
    a=p.parse_args()
    c=load(CIC.name);l=load("LIVE_RECEIVING_LEDGER.json");r=load("01_SOURCE_OF_TRUTH_REGISTRY.json")
    result=validate(c,l,r)
    if a.self_test: result["adversaries_refused"]=selftest(c,l,r)
    if a.function or a.obligation:
        result["obligations"]=[o for o in c["obligations"] if (not a.function or a.function in o["function_refs"]) and (not a.obligation or a.obligation==o["id"])]
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
