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

FIRST_DRAFT = "AUTHOR_PROPOSED_SCOPED_INTEGRATED_FIRST_DRAFT"

def construction_view(c):
    """Scope accounting, not an aggregate percentage or a new inventory."""
    clusters = []
    for o in c["obligations"]:
        rows = []
        for q in o["criteria"]:
            draft = q.get("construction_first_draft")
            rows.append({"id":q["id"], "acceptance_candidate":q["acceptance_candidate"],
                         "construction_status":FIRST_DRAFT if draft else "NOT_YET_ADJUDICATED_FOR_FIRST_DRAFT",
                         "prior_evidence_status":q["criterion_status"],
                         "first_draft":draft,"remaining_boundary":q["remaining_boundary"]})
        clusters.append({"id":o["id"],"title":o["title"],"criteria":rows,
                         "scoped_first_drafts":sum(r["first_draft"] is not None for r in rows)})
    n = sum(x["scoped_first_drafts"] for x in clusters)
    return {"mode":"BOUNDED_CONSTRUCTION_ACCOUNTING_NOT_COMPLETION_PERCENTAGE",
            "clusters":len(clusters),"criteria":sum(len(x["criteria"]) for x in clusters),
            "scoped_first_draft_candidates":n,
            "not_yet_adjudicated":sum(len(x["criteria"]) for x in clusters)-n,
            "whole_clusters_closed":0,"obligations":clusters}

def check_first_draft(q, obs):
    d = q.get("construction_first_draft")
    if d is None:
        return
    require(d["status"] == FIRST_DRAFT and d["authority"] ==
            "NO_CRITERION_CLOSURE_NO_INDEPENDENT_REVIEW_NO_PROTECTED_RECEIVING", "FIRST_DRAFT_FALSE_PROMOTION")
    require(q["criterion_status"] != "RELATED_EXECUTION_AFFECTED_BY_REJECTED_DEPENDENCY", "FIRST_DRAFT_REJECTED_DEPENDENCY")
    require(bool(d["scope"]) and d["remaining_boundary"] == q["remaining_boundary"], "FIRST_DRAFT_BOUNDARY")
    test = obs[d["joined_pr"]]["test"]
    require(test["executed_sha"] == d["executed_sha"] == obs[d["joined_pr"]]["head_sha"] and
            test["receipt"] == d["receipt"] and test["applied_to_head"] is True and
            test["normal"] > 0 and test["optimized"] > 0, "FIRST_DRAFT_EXECUTION_DRIFT")
    t = d["consumer_test"]
    require(t["path"].startswith("SEAM/") and t["path"].endswith(".py") and
            len(t["blob"]) == 40 and all(ch in "0123456789abcdef" for ch in t["blob"]) and
            bool(t["positive"]) and bool(t["negative"]), "FIRST_DRAFT_CONSUMER_MISSING")

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
            check_first_draft(q, obs)
            require(set(q["dimensions"]) == dimensions, "EVIDENCE_DIMENSIONS")
            require(q["dimensions"]["received"] == "NOT_RECEIVED_AS_CIC_CRITERION", "FALSE_RECEIVING")
            require(q["dimensions"]["demonstrated"] == "NO_NEW_CRITERION_EXECUTION", "FALSE_EXECUTION")
            require(q["dimensions"]["independent_review"] == "NOT_ISSUED_FOR_CIC_CRITERION", "FALSE_INDEPENDENT_REVIEW")
            require(all(q["dimensions"][k] == "NO_NEW_GRANT" for k in ("source_authority","actor_authority","human_authority")), "FALSE_AUTHORITY")
            require(bool(q["acceptance_candidate"] and q["remaining_boundary"] and q["falsifier"] and (q["evidence"] or q.get("requirement_origin",{}).get("kind") == "HOME_DERIVED_INDEPENDENT_OF_RETURN")), "EMPTY_COURT")
            require("requirement_origin" not in q or "refines" in q, "HOME_REFINEMENT_SOURCE_DRIFT")
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
        if "requirement_origin" in q:
            origin = q["requirement_origin"]
            lane = obligations[oid]["lane"]
            home = c["homes"][lane]
            require(origin.get("kind") == "HOME_DERIVED_INDEPENDENT_OF_RETURN" and origin.get("lane") == lane and origin.get("home_commit") == home["commit"] and origin.get("home_blob") == home["blob"] and origin.get("home_path") == home["path"] and bool(origin.get("source_basis")) and origin.get("status") == "PROVISIONAL_HOME_INTERPRETATION__OWNER_RECEIVING_HELD", "HOME_REFINEMENT_SOURCE_DRIFT")
            require("scoped_return" not in q and q["criterion_status"] == "CRITERION_EQUIVALENCE_UNRECONCILED" and q["dimensions"]["current_implementation"] == "UNRECONCILED_AT_CRITERION_SCOPE", "HOME_REFINEMENT_FALSE_PROMOTION")
            require(bool(q.get("whole_organism_navigation",{}).get("existing_capital")) and bool(q["whole_organism_navigation"].get("next_owner_work")), "HOME_REFINEMENT_NAVIGATION_DROP")
            continue
        sr = q["scoped_return"]
        source = obs[sr["pr"]]
        require(sr["pr"] == q["evidence"][0]["pr"] and sr["execution_sha"] == source["test"]["executed_sha"] and sr["execution_grade"] == source["test"]["grade"] and sr["receipt"] == source["test"]["receipt"] and sr["first_consumer"] == source["first_consumer"], "REFINEMENT_RETURN_DRIFT")
        require(sr["source_bodies"] == [{"path": b["path"], "blob": b["blob"]} for b in source["exact_source_bodies"]], "REFINEMENT_SOURCE_BODY_DRIFT")
        require(sr["criterion_execution"] == "NOT_RUN_AS_COMPLETE_CIC_CRITERION" and sr["review"] == "NOT_INDEPENDENTLY_REVIEWED_AT_CRITERION_SCOPE", "REFINEMENT_FALSE_PROMOTION")
    rounds = c.get("refinement_rounds", [])
    require(bool(rounds), "REFINEMENT_DENOMINATOR_DRIFT")
    added = set()
    count = len(criteria) - len(refined)
    for r in rounds:
        new = r["added_criterion_ids"]
        require(r["prior_criterion_count"] == count and len(set(new)) == len(new) and not added.intersection(new), "REFINEMENT_DENOMINATOR_DRIFT")
        added.update(new)
        count += len(new)
    require(added == set(refined) and count == len(criteria), "REFINEMENT_DENOMINATOR_DRIFT")
    u = c["source_contract"]["upstream_elasticity_candidate"]
    require(u["status"] == "USER_DIRECTION_RECORDED__HOME_AND_PROTECTED_SEMANTIC_RECEIVING_HELD", "UPSTREAM_FALSE_RECEIVING")
    require({x["pr"] for x in u["candidate_prs"]} == {1330,1331,1332,1333}, "UPSTREAM_SOURCE_DROP")
    for x in u["candidate_prs"]:
        r = obs[x["pr"]]
        require(x["head"] == r["head_sha"] and x["sources"] == r["exact_source_bodies"] and not r["test"]["executed_sha"], "UPSTREAM_SOURCE_DRIFT")
    require(set(u["criteria"]) == {"CO-CIC-023.04","CO-CIC-023.05","CO-CIC-007.04","NEIGHBOR-CIC-006.06"} and set(u["criteria"]) <= set(criteria) and set(u["implementation_prs"]) == {1329,1335}, "UPSTREAM_CRITERION_DRIFT")
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
    check(lambda x:next(q for o in x["obligations"] for q in o["criteria"] if q["evidence"] and q["evidence"][0]["pr"]==1300).update(criterion_status="PASS"),"R30_FALSE_PROMOTION")
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
    check(lambda x:x["refinement_rounds"][-1].update(prior_criterion_count=0),"REFINEMENT_DENOMINATOR_DRIFT")
    check(lambda x:x["refinement_rounds"][-1]["added_criterion_ids"].append(x["refinement_rounds"][0]["added_criterion_ids"][0]),"REFINEMENT_DENOMINATOR_DRIFT")
    check(lambda x:x["source_contract"]["upstream_elasticity_candidate"].update(status="RECEIVED"),"UPSTREAM_FALSE_RECEIVING")
    check(lambda x:x["source_contract"]["upstream_elasticity_candidate"]["candidate_prs"].pop(),"UPSTREAM_SOURCE_DROP")
    check(lambda x:x["source_contract"]["upstream_elasticity_candidate"]["candidate_prs"][0].update(head="0"*40),"UPSTREAM_SOURCE_DRIFT")
    check(lambda x:x["source_contract"]["upstream_elasticity_candidate"]["criteria"].pop(),"UPSTREAM_CRITERION_DRIFT")
    def homechild(x):
        return next(q for o in x["obligations"] for q in o["criteria"] if "requirement_origin" in q)
    check(lambda x:homechild(x)["requirement_origin"].update(home_blob="0"*40),"HOME_REFINEMENT_SOURCE_DRIFT")
    check(lambda x:homechild(x).update(scoped_return={"criterion_execution":"PASS"}),"HOME_REFINEMENT_FALSE_PROMOTION")
    check(lambda x:homechild(x).update(criterion_status="PASS"),"HOME_REFINEMENT_FALSE_PROMOTION")
    check(lambda x:homechild(x)["requirement_origin"].update(source_basis=""),"HOME_REFINEMENT_SOURCE_DRIFT")
    check(lambda x:homechild(x)["whole_organism_navigation"].pop("existing_capital"),"HOME_REFINEMENT_NAVIGATION_DROP")
    def draft(x):
        return next(q["construction_first_draft"] for o in x["obligations"] for q in o["criteria"] if "construction_first_draft" in q)
    if construction_view(c)["scoped_first_draft_candidates"]:
        check(lambda x:draft(x).update(executed_sha="0"*40),"FIRST_DRAFT_EXECUTION_DRIFT")
        check(lambda x:draft(x).update(remaining_boundary=""),"FIRST_DRAFT_BOUNDARY")
        check(lambda x:draft(x).update(authority="RECEIVED"),"FIRST_DRAFT_FALSE_PROMOTION")
        return 33
    return 30
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--function")
    p.add_argument("--construction-view",action="store_true")
    p.add_argument("--obligation")
    a=p.parse_args()
    c=load(CIC.name);l=load("LIVE_RECEIVING_LEDGER.json");r=load("01_SOURCE_OF_TRUTH_REGISTRY.json")
    result=validate(c,l,r)
    if a.self_test: result["adversaries_refused"]=selftest(c,l,r)
    if a.construction_view: result["construction"]=construction_view(c)
    if a.function or a.obligation:
        result["obligations"]=[o for o in c["obligations"] if (not a.function or a.function in o["function_refs"]) and (not a.obligation or a.obligation==o["id"])]
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
