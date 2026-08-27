#!/usr/bin/env python3
"""Deterministic WVS7 W1-W6 post-batch join/preflight harness.

Lane-12 only. This module never fetches worker branches. It consumes only HQ-supplied,
final-return normalized bundles and frozen accepted law in FROZEN_JOIN_AUTHORITY.json.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, re, sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
AUTHORITY = json.loads((HERE / "FROZEN_JOIN_AUTHORITY.json").read_text())
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

class ValidationError(RuntimeError):
    pass

def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")

def sha256_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def fail(msg: str) -> None:
    raise ValidationError(msg)

def _country_key(x: dict[str, Any]) -> tuple[str,int]:
    return (x.get("country"), x.get("year"))

def _decode_country_token(token: str) -> tuple[str,int]:
    country, year = token.rsplit("|", 1)
    return country, int(year)

def _expected_batch_pairs(bid: str) -> list[tuple[str,int]]:
    return [_decode_country_token(x) for x in AUTHORITY["expected_batches"][bid]]

def _source_present_pairs() -> list[tuple[str,int]]:
    out=[_decode_country_token(x) for x in AUTHORITY["source_present_extra_countries"]]
    for bid in sorted(AUTHORITY["expected_batches"]): out.extend(_expected_batch_pairs(bid))
    return out

def _require_str(obj: dict[str,Any], key: str, ctx: str) -> str:
    v=obj.get(key)
    if not isinstance(v,str) or not v.strip(): fail(f"{ctx}: {key} must be a non-empty string")
    return v

def _require_sha256(v: Any, ctx: str) -> str:
    if not isinstance(v,str) or not HEX64.fullmatch(v): fail(f"{ctx}: expected lowercase sha256")
    return v

def _require_sha40(v: Any, ctx: str) -> str:
    if not isinstance(v,str) or not HEX40.fullmatch(v): fail(f"{ctx}: expected lowercase 40-hex git SHA")
    return v

def validate_authority_pins(req: dict[str,Any]) -> None:
    if req.get("authority_pins") != AUTHORITY["authority_pins"]:
        fail("authority_pins do not exactly match frozen Lane-12 authority")

def validate_batch_manifest(batch: dict[str,Any], bid: str) -> None:
    if batch.get("batch_id") != bid: fail(f"{bid}: batch_id mismatch")
    n=int(bid[1:])
    expected_token=AUTHORITY["terminal_token_template"].format(n=n)
    if batch.get("terminal_token") != expected_token: fail(f"{bid}: final terminal token missing/mismatched")
    _require_sha40(batch.get("final_commit_sha"), f"{bid}.final_commit_sha")
    files=batch.get("required_files")
    if not isinstance(files,dict): fail(f"{bid}: required_files must be object")
    if set(files) != set(AUTHORITY["required_batch_files"]): fail(f"{bid}: required file set mismatch")
    for name,h in files.items(): _require_sha256(h, f"{bid}.required_files[{name}]")

def validate_document(doc: dict[str,Any], country_key: tuple[str,int], seen_ids: set[str]) -> None:
    ctx=f"document[{doc.get('document_id','?')}]"
    for k in ("document_id","identity_key","title","source_owner","locator","provenance_ref","content_status","source_locator"): _require_str(doc,k,ctx)
    if _country_key(doc) != country_key: fail(f"{ctx}: country/year mismatch")
    if doc["document_id"] in seen_ids: fail(f"{ctx}: duplicate document_id within country")
    seen_ids.add(doc["document_id"])
    if doc["content_status"] not in {"CONTENT_RECOVERED","IDENTITY_ONLY","NOT_LOCATED"}: fail(f"{ctx}: illegal content_status")
    ch=doc.get("content_sha256")
    if doc["content_status"] == "CONTENT_RECOVERED": _require_sha256(ch, f"{ctx}.content_sha256")
    elif ch not in (None,""): fail(f"{ctx}: content_sha256 forbidden unless CONTENT_RECOVERED")

def validate_evidence_record(rec: dict[str,Any], country_key: tuple[str,int], *, routing: bool) -> None:
    ctx=f"record[{rec.get('record_id','?')}]"
    _require_str(rec,"record_id",ctx); _require_str(rec,"source_locator",ctx)
    if _country_key(rec) != country_key: fail(f"{ctx}: country/year mismatch")
    state=rec.get("state")
    if state not in AUTHORITY["documentary_states"]: fail(f"{ctx}: illegal documentary state {state!r}")
    docs=rec.get("document_ids")
    if not isinstance(docs,list) or any(not isinstance(x,str) or not x for x in docs): fail(f"{ctx}: document_ids must be string list")
    if routing:
        gap=rec.get("gap_id")
        if gap not in AUTHORITY["documentary_gap_ids"]: fail(f"{ctx}: illegal/worker-forbidden gap_id {gap!r}")
        rule_ids=rec.get("rule_ids")
        if not isinstance(rule_ids,list) or not rule_ids: fail(f"{ctx}: rule_ids required")
        allowed=set(AUTHORITY["gap_rule_map"][gap])
        if not set(rule_ids) <= allowed: fail(f"{ctx}: rule_ids escape frozen Lane-B mapping for {gap}")

def validate_country(country: dict[str,Any], expected: tuple[str,int]) -> None:
    if _country_key(country) != expected: fail(f"country record mismatch: expected {expected}, got {_country_key(country)}")
    docs=country.get("documents")
    if not isinstance(docs,list): fail(f"{expected}: documents must be list")
    seen_doc_ids:set[str]=set()
    for d in docs: validate_document(d,expected,seen_doc_ids)
    universe=country.get("country_universe_record")
    if not isinstance(universe,dict): fail(f"{expected}: country_universe_record required")
    validate_evidence_record(universe,expected,routing=False)
    routing=country.get("routing_documentary_records")
    if not isinstance(routing,list): fail(f"{expected}: routing_documentary_records must be list")
    by_gap={g:0 for g in AUTHORITY["documentary_gap_ids"]}
    record_ids={universe["record_id"]}
    unresolved_record_ids=set()
    if universe["state"] in AUTHORITY["unresolved_states"]: unresolved_record_ids.add(universe["record_id"])
    for r in routing:
        validate_evidence_record(r,expected,routing=True)
        if r["record_id"] in record_ids: fail(f"{expected}: duplicate record_id {r['record_id']}")
        record_ids.add(r["record_id"]); by_gap[r["gap_id"]]+=1
        if r["state"] in AUTHORITY["unresolved_states"]: unresolved_record_ids.add(r["record_id"])
    missing=[g for g,n in by_gap.items() if n==0]
    if missing: fail(f"{expected}: incomplete D01-D12 coverage; documentary gaps absent: {missing}")
    unknowns=country.get("unknowns")
    if not isinstance(unknowns,list): fail(f"{expected}: unknowns must be list")
    unknown_ids=set(); backed=set()
    for u in unknowns:
        ctx=f"unknown[{u.get('unknown_id','?')}]"
        for k in ("unknown_id","record_id","reason","downstream_effect","source_locator"): _require_str(u,k,ctx)
        if _country_key(u) != expected: fail(f"{ctx}: country/year mismatch")
        if u["unknown_id"] in unknown_ids: fail(f"{ctx}: duplicate unknown_id")
        unknown_ids.add(u["unknown_id"])
        if u["record_id"] not in unresolved_record_ids: fail(f"{ctx}: illegal UNKNOWN widening; unknown is not backed by an unresolved evidence record")
        backed.add(u["record_id"])
    missing_unknowns=unresolved_record_ids-backed
    if missing_unknowns: fail(f"{expected}: unresolved records omitted from UNKNOWN ledger: {sorted(missing_unknowns)}")
    contradictions=country.get("contradictions")
    if not isinstance(contradictions,list): fail(f"{expected}: contradictions must be list")
    contradiction_record_ids=set()
    for c in contradictions:
        ctx=f"contradiction[{c.get('contradiction_id','?')}]"
        for k in ("contradiction_id","description","source_locator"): _require_str(c,k,ctx)
        if c.get("requires_hq_adjudication") is not True: fail(f"{ctx}: contradictions must require HQ adjudication")
        rids=c.get("record_ids")
        if not isinstance(rids,list) or not rids or not set(rids)<=record_ids: fail(f"{ctx}: invalid record_ids")
        contradiction_record_ids.update(rids)
    marked={r["record_id"] for r in [universe]+routing if r["state"]=="CONTRADICTORY_SOURCE_OWNER_DOCUMENTS__HQ_ADJUDICATION_REQUIRED"}
    if marked-contradiction_record_ids: fail(f"{expected}: contradictory evidence record lacks contradiction surface")

def validate_batches(req: dict[str,Any]) -> dict[tuple[str,int],dict[str,Any]]:
    batches=req.get("batches")
    if not isinstance(batches,list): fail("batches must be list")
    by_id={}
    for b in batches:
        bid=b.get("batch_id") if isinstance(b,dict) else None
        if bid in by_id: fail(f"duplicate batch {bid}")
        by_id[bid]=b
    expected_ids=set(AUTHORITY["expected_batches"])
    if set(by_id)!=expected_ids: fail(f"missing/extra batch: expected {sorted(expected_ids)}, got {sorted(x for x in by_id if x)}")
    countries={}
    for bid in sorted(expected_ids):
        batch=by_id[bid]; validate_batch_manifest(batch,bid)
        rows=batch.get("countries")
        if not isinstance(rows,list): fail(f"{bid}: countries must be list")
        expected=_expected_batch_pairs(bid)
        got=[_country_key(x) for x in rows]
        if len(got)!=len(set(got)): fail(f"{bid}: duplicate country within batch")
        if set(got)!=set(expected): fail(f"{bid}: expected batch/country coverage mismatch; missing={sorted(set(expected)-set(got))}, extra={sorted(set(got)-set(expected))}")
        for row in rows:
            key=_country_key(row)
            if key in countries: fail(f"duplicate country across batches: {key}")
            validate_country(row,key); countries[key]=row
    expected_union={x for bid in AUTHORITY["expected_batches"] for x in _expected_batch_pairs(bid)}
    if set(countries)!=expected_union: fail("country-universe union mismatch after batch validation")
    return countries

def dedupe_documents(countries: dict[tuple[str,int],dict[str,Any]]) -> tuple[list[dict[str,Any]],list[dict[str,Any]]]:
    by_identity:dict[str,list[dict[str,Any]]]={}
    for key in sorted(countries):
        for doc in countries[key]["documents"]: by_identity.setdefault(doc["identity_key"],[]).append(doc)
    deduped=[]; derived=[]
    for ikey,docs in sorted(by_identity.items()):
        variants={sha256_obj({k:d.get(k) for k in ("title","source_owner","locator","content_status","content_sha256","provenance_ref")}) for d in docs}
        if len(variants)>1:
            cid="JOIN-DOC-CONTRADICTION-"+hashlib.sha256(ikey.encode()).hexdigest()[:20]
            derived.append({"contradiction_id":cid,"kind":"DOCUMENT_IDENTITY_PROVENANCE_CONFLICT","identity_key":ikey,"document_ids":sorted(d["document_id"] for d in docs),"requires_hq_adjudication":True})
        reps={}
        for d in docs:
            sig=sha256_obj({k:d.get(k) for k in ("title","source_owner","locator","content_status","content_sha256","provenance_ref")})
            candidate=copy.deepcopy(d)
            if sig not in reps or canonical_bytes(candidate) < canonical_bytes(reps[sig]): reps[sig]=candidate
        for sig in sorted(reps): deduped.append(reps[sig])
    deduped.sort(key=lambda d:(d["identity_key"],d["country"],d["year"],d["document_id"]))
    return deduped,derived

def collect_contradictions(countries: dict[tuple[str,int],dict[str,Any]], derived: list[dict[str,Any]]) -> list[dict[str,Any]]:
    out=[]
    for key in sorted(countries): out.extend(copy.deepcopy(countries[key]["contradictions"]))
    out.extend(copy.deepcopy(derived))
    ids=[c["contradiction_id"] for c in out]
    if len(ids)!=len(set(ids)): fail("duplicate contradiction_id after join")
    return sorted(out,key=lambda x:x["contradiction_id"])

def collect_unknowns(countries: dict[tuple[str,int],dict[str,Any]]) -> list[dict[str,Any]]:
    out=[]
    for key in sorted(countries): out.extend(copy.deepcopy(countries[key]["unknowns"]))
    ids=[u["unknown_id"] for u in out]
    if len(ids)!=len(set(ids)): fail("duplicate unknown_id after join")
    return sorted(out,key=lambda x:x["unknown_id"])

def validate_hq_surfaces(req: dict[str,Any], unknowns:list[dict[str,Any]], contradictions:list[dict[str,Any]]) -> list[str]:
    blockers=[]
    d03=req.get("d03_adjudication")
    if not isinstance(d03,dict): fail("D03 adjudication input surface missing")
    if sorted(d03.get("covered_targets",[])) != sorted(AUTHORITY["d03_targets"]): fail("D03 covered_targets mismatch")
    if d03.get("status") != "HQ_ADJUDICATED": blockers.append("D03_NOT_HQ_ADJUDICATED")
    else:
        _require_str(d03,"adjudication_ref","D03"); _require_sha256(d03.get("content_sha256"),"D03.content_sha256")
    d11=req.get("d11_country_empirical_universe_bindings")
    if not isinstance(d11,list): fail("D11 bindings must be list")
    expected=set(_source_present_pairs())
    got=[_country_key(x) for x in d11]
    if len(got)!=len(set(got)): fail("D11 duplicate country binding")
    if set(got)!=expected: fail(f"D11 country EmpiricalUniverse coverage mismatch; missing={sorted(expected-set(got))}, extra={sorted(set(got)-expected)}")
    for x in d11:
        ctx=f"D11[{_country_key(x)}]"
        if x.get("status")!="HQ_ACCEPTED": blockers.append(ctx+":NOT_HQ_ACCEPTED"); continue
        _require_str(x,"empirical_universe_ref",ctx); _require_str(x,"authority_ref",ctx); _require_sha256(x.get("content_sha256"),ctx+".content_sha256")
    d12=req.get("d12_respondent_replay_bindings")
    if not isinstance(d12,list) or not d12: fail("D12 replay binding surface missing/empty")
    d12_covered=[]
    for x in d12:
        ctx=f"D12[{x.get('binding_id','?')}]"; _require_str(x,"binding_id",ctx)
        if x.get("status")!="HQ_ACCEPTED": blockers.append(ctx+":NOT_HQ_ACCEPTED"); continue
        _require_str(x,"binding_manifest_ref",ctx); _require_sha256(x.get("binding_manifest_sha256"),ctx+".binding_manifest_sha256")
        _require_sha256(x.get("source_snapshot_sha256"),ctx+".source_snapshot_sha256"); _require_sha256(x.get("row_ordinal_binding_sha256"),ctx+".row_ordinal_binding_sha256")
        cov=x.get("countries_covered")
        if not isinstance(cov,list): fail(ctx+": countries_covered must be list")
        d12_covered.extend(_country_key(c) for c in cov)
    if len(d12_covered)!=len(set(d12_covered)): fail("D12 country coverage overlaps across replay bindings")
    if set(d12_covered)!=expected: fail(f"D12 respondent replay country coverage mismatch; missing={sorted(expected-set(d12_covered))}, extra={sorted(set(d12_covered)-expected)}")
    adjs=req.get("contradiction_adjudications")
    if not isinstance(adjs,dict): fail("contradiction_adjudications must be object")
    known={c["contradiction_id"] for c in contradictions}
    if not set(adjs)<=known: fail("contradiction adjudication references nonexistent contradiction (silent/invented resolution forbidden)")
    for cid in sorted(known):
        a=adjs.get(cid)
        if not isinstance(a,dict) or a.get("status")!="HQ_ADJUDICATED": blockers.append(f"UNRESOLVED_CONTRADICTION:{cid}")
        else:
            _require_str(a,"adjudication_ref",f"contradiction_adjudications[{cid}]"); _require_sha256(a.get("content_sha256"),f"contradiction_adjudications[{cid}].content_sha256")
    uds=req.get("unknown_dispositions")
    if not isinstance(uds,dict): fail("unknown_dispositions must be object")
    known_u={u["unknown_id"] for u in unknowns}
    if set(uds)-known_u: fail("illegal UNKNOWN widening: HQ disposition names unknown not derived from final batch evidence")
    for uid in sorted(known_u):
        d=uds.get(uid)
        if not isinstance(d,dict): blockers.append(f"UNRESOLVED_UNKNOWN:{uid}"); continue
        status=d.get("status")
        if status=="BLOCKING": blockers.append(f"BLOCKING_UNKNOWN:{uid}")
        elif status in {"NONBLOCKING_EXCLUDED","RESOLVED_WITH_ACCEPTED_AUTHORITY"}:
            _require_str(d,"authority_ref",f"unknown_dispositions[{uid}]"); _require_sha256(d.get("content_sha256"),f"unknown_dispositions[{uid}].content_sha256")
        else: fail(f"unknown_dispositions[{uid}]: illegal status")
    return blockers

def build_report(req: dict[str,Any]) -> dict[str,Any]:
    if req.get("schema_name")!="gsr07r3-wvs7-hq-join-request-v1": fail("schema_name mismatch")
    validate_authority_pins(req)
    countries=validate_batches(req)
    docs,derived=dedupe_documents(countries)
    contradictions=collect_contradictions(countries,derived)
    unknowns=collect_unknowns(countries)
    blockers=validate_hq_surfaces(req,unknowns,contradictions)
    routing=[]
    for key in sorted(countries):
        for r in countries[key]["routing_documentary_records"]: routing.append({**copy.deepcopy(r),"frozen_lane_b_rule_ids":sorted(r["rule_ids"])})
    routing.sort(key=lambda r:(r["country"],r["year"],r["gap_id"],r["record_id"]))
    batch_manifest=[]
    for b in sorted(req["batches"],key=lambda x:x["batch_id"]): batch_manifest.append({k:copy.deepcopy(b[k]) for k in ("batch_id","final_commit_sha","terminal_token","required_files")})
    report={
      "schema_name":"wvs7-postbatch-join-report-v1",
      "authority_pins":copy.deepcopy(AUTHORITY["authority_pins"]),
      "batch_input_manifest":batch_manifest,
      "country_union":[{"country":k[0],"year":k[1]} for k in sorted(countries)],
      "source_present_country_universe":[{"country":c,"year":y} for c,y in _source_present_pairs()],
      "document_identity_projection":docs,
      "routing_documentary_join":routing,
      "d03_adjudication":copy.deepcopy(req["d03_adjudication"]),
      "d11_country_empirical_universe_bindings":sorted(copy.deepcopy(req["d11_country_empirical_universe_bindings"]),key=lambda x:(x["country"],x["year"])),
      "d12_respondent_replay_bindings":sorted(copy.deepcopy(req["d12_respondent_replay_bindings"]),key=lambda x:x["binding_id"]),
      "unknown_ledger":unknowns,
      "contradictions":contradictions,
      "preflight":{"status":"PASS" if not blockers else "FAIL_CLOSED","blockers":sorted(set(blockers)),"all_d01_d12_surfaces_present":True,"no_batch_facts_consumed_by_lane12_prep":True},
      "non_authority_notice":"Mechanical join output only. Documentary/HQ fact authority remains in cited final inputs and accepted HQ adjudications."
    }
    package_payload={k:v for k,v in report.items() if k!="package_sha256"}
    report["package_sha256"]=sha256_obj(package_payload)
    return report

def join(req:dict[str,Any]) -> dict[str,Any]:
    report=build_report(req)
    if report["preflight"]["status"]!="PASS": fail("relaunch preflight blocked: "+"; ".join(report["preflight"]["blockers"]))
    return report

def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("request",type=Path)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--report-only",action="store_true",help="write deterministic blocked report instead of requiring relaunch-ready PASS")
    a=p.parse_args(argv)
    try:
        req=json.loads(a.request.read_text())
        out=build_report(req) if a.report_only else join(req)
        a.output.write_bytes(canonical_bytes(out))
        print(json.dumps({"status":out["preflight"]["status"],"package_sha256":out["package_sha256"],"output":str(a.output)},sort_keys=True))
        return 0 if out["preflight"]["status"]=="PASS" else 2
    except (ValidationError,KeyError,TypeError,ValueError,json.JSONDecodeError) as e:
        print(f"FAIL_CLOSED: {e}",file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main())
