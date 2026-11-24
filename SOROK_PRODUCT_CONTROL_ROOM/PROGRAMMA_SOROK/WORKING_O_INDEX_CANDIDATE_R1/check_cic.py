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
            for e in q["evidence"]:
                k = (e["pr"], e["original_id"])
                require(k in links and e["observed_head"] == obs[e["pr"]]["head_sha"] and e["relationship_grade"] == links[k]["grade"], "EVIDENCE_SCOPE_DRIFT")
                if e["pr"] in (1298,1300):
                    require(q["criterion_status"] == "RELATED_EXECUTION_AFFECTED_BY_REJECTED_DEPENDENCY", "R30_FALSE_PROMOTION")
                require(e["pr"] != 1294, "REJECTED_R30_AS_POSITIVE")
    require(len(criteria) == c["counts"]["criteria"], "CRITERION_COUNT")
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
    for j in c["whole_organism_acceptance_candidates"]:
        require(set(j["obligation_ids"]) <= set(obligations) and set(j["criterion_ids"]) <= set(criteria), "JOIN_REFERENCES")
        require(j["state"] == "HELD_CRITERION_SPECIFIC_WHOLE_TRAJECTORY", "FALSE_WHOLE_TRAJECTORY")
    return {"obligations":len(obligations),"criteria":len(criteria),"routed_source_blocks":len(seen),"mode":"DOCUMENTARY_CORRESPONDENCE_NOT_SEMANTIC_OR_RUNTIME_ACCEPTANCE"}

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
    return 9
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
