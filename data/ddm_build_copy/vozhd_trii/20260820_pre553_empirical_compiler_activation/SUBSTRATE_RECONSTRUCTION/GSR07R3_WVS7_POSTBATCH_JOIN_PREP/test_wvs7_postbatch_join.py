import copy, hashlib, unittest
from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("joinmod",HERE/"wvs7_postbatch_join.py")
M=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)
A=M.AUTHORITY

def h(s): return hashlib.sha256(s.encode()).hexdigest()
def build_good():
    req={"schema_name":"gsr07r3-wvs7-hq-join-request-v1","authority_pins":copy.deepcopy(A["authority_pins"]),"batches":[],"d03_adjudication":{"status":"HQ_ADJUDICATED","covered_targets":copy.deepcopy(A["d03_targets"]),"adjudication_ref":"SYNTHETIC_ONLY:D03","content_sha256":h('d03'),"input_refs":["NON_AUTHORITATIVE_SYNTHETIC_ONLY"]},"d11_country_empirical_universe_bindings":[],"d12_respondent_replay_bindings":[],"contradiction_adjudications":{},"unknown_dispositions":{}}
    for bid in sorted(A["expected_batches"]):
        n=int(bid[1:]); b={"batch_id":bid,"final_commit_sha":h(bid)[:40],"terminal_token":A["terminal_token_template"].format(n=n),"required_files":{f:h(bid+f) for f in A["required_batch_files"]},"countries":[]}
        for token in A["expected_batches"][bid]:
            c,y=M._decode_country_token(token); docid=f"SYNTH-{bid}-{c}-{y}"; recbase=f"{bid}:{c}:{y}"
            doc={"document_id":docid,"identity_key":docid,"country":c,"year":y,"title":"NON_AUTHORITATIVE_SYNTHETIC_ONLY","source_owner":"SYNTHETIC_ONLY","locator":"synthetic://fixture","provenance_ref":"NON_AUTHORITATIVE_SYNTHETIC_ONLY","content_status":"CONTENT_RECOVERED","content_sha256":h(docid),"source_locator":"SYNTHETIC_TEST#doc"}
            uni={"record_id":recbase+":U","country":c,"year":y,"state":"RECOVERED_SOURCE_OWNER_AUTHORITY","document_ids":[docid],"source_locator":"SYNTHETIC_TEST#universe","payload":{"fixture":"NON_AUTHORITATIVE_SYNTHETIC_ONLY"}}
            routing=[]
            for gap in A["documentary_gap_ids"]:
                routing.append({"record_id":recbase+":"+gap,"country":c,"year":y,"gap_id":gap,"state":"NOT_APPLICABLE_TO_CLAIM","rule_ids":[A["gap_rule_map"][gap][0]],"document_ids":[docid],"source_locator":"SYNTHETIC_TEST#routing","payload":{"fixture":"NON_AUTHORITATIVE_SYNTHETIC_ONLY"}})
            b["countries"].append({"country":c,"year":y,"documents":[doc],"country_universe_record":uni,"routing_documentary_records":routing,"unknowns":[],"contradictions":[]})
        req["batches"].append(b)
    source_present=[{"country":c,"year":y} for c,y in M._source_present_pairs()]
    for x in source_present:
        req["d11_country_empirical_universe_bindings"].append({"country":x["country"],"year":x["year"],"status":"HQ_ACCEPTED","empirical_universe_ref":"SYNTHETIC_ONLY:EU:"+x["country"],"authority_ref":"SYNTHETIC_ONLY","content_sha256":h('eu'+x["country"]+str(x["year"]))})
    req["d12_respondent_replay_bindings"].append({"binding_id":"SYNTHETIC-D12","status":"HQ_ACCEPTED","binding_manifest_ref":"SYNTHETIC_ONLY","binding_manifest_sha256":h('manifest'),"source_snapshot_sha256":h('source'),"row_ordinal_binding_sha256":h('rows'),"countries_covered":copy.deepcopy(source_present)})
    return req

def country(req,bid='W1',idx=0): return next(b for b in req['batches'] if b['batch_id']==bid)['countries'][idx]

class JoinTests(unittest.TestCase):
    def test_synthetic_fixture_passes_and_is_deterministic(self):
        a=build_good(); r1=M.join(a); a['batches'].reverse(); r2=M.join(a)
        self.assertEqual(r1['package_sha256'],r2['package_sha256']); self.assertEqual(r1['preflight']['status'],'PASS')
    def test_missing_batch_fail_closed(self):
        a=build_good(); a['batches']=[b for b in a['batches'] if b['batch_id']!='W6']
        with self.assertRaisesRegex(M.ValidationError,'missing/extra batch'): M.join(a)
    def test_missing_country_fail_closed(self):
        a=build_good(); next(b for b in a['batches'] if b['batch_id']=='W2')['countries'].pop()
        with self.assertRaisesRegex(M.ValidationError,'coverage mismatch'): M.join(a)
    def test_duplicate_country_fail_closed(self):
        a=build_good(); b=next(b for b in a['batches'] if b['batch_id']=='W1'); b['countries'][1]=copy.deepcopy(b['countries'][0])
        with self.assertRaisesRegex(M.ValidationError,'duplicate country|coverage mismatch'): M.join(a)
    def test_malformed_provenance_fail_closed(self):
        a=build_good(); country(a)['documents'][0]['provenance_ref']=''
        with self.assertRaisesRegex(M.ValidationError,'provenance_ref'): M.join(a)
    def test_unresolved_contradiction_fail_closed(self):
        a=build_good(); c=country(a); r=c['routing_documentary_records'][0]; r['state']='CONTRADICTORY_SOURCE_OWNER_DOCUMENTS__HQ_ADJUDICATION_REQUIRED'; c['unknowns']=[{"unknown_id":"SYNTH-U","record_id":r['record_id'],"country":c['country'],"year":c['year'],"reason":"NON_AUTHORITATIVE_SYNTHETIC_ONLY","downstream_effect":"BLOCK","source_locator":"SYNTHETIC_TEST#unknown"}]; c['contradictions']=[{"contradiction_id":"SYNTH-C","record_ids":[r['record_id']],"description":"NON_AUTHORITATIVE_SYNTHETIC_ONLY","source_locator":"SYNTHETIC_TEST#contradiction","requires_hq_adjudication":True}]; a['unknown_dispositions']['SYNTH-U']={"status":"NONBLOCKING_EXCLUDED","authority_ref":"SYNTHETIC_ONLY","content_sha256":h('u')}
        with self.assertRaisesRegex(M.ValidationError,'UNRESOLVED_CONTRADICTION'): M.join(a)
    def test_illegal_unknown_widening_fail_closed(self):
        a=build_good(); a['unknown_dispositions']['INVENTED-UNKNOWN']={"status":"BLOCKING"}
        with self.assertRaisesRegex(M.ValidationError,'illegal UNKNOWN widening'): M.join(a)
    def test_unbacked_batch_unknown_fail_closed(self):
        a=build_good(); c=country(a); c['unknowns']=[{"unknown_id":"SYNTH-U","record_id":c['routing_documentary_records'][0]['record_id'],"country":c['country'],"year":c['year'],"reason":"NON_AUTHORITATIVE_SYNTHETIC_ONLY","downstream_effect":"BLOCK","source_locator":"SYNTHETIC_TEST#unknown"}]
        with self.assertRaisesRegex(M.ValidationError,'illegal UNKNOWN widening'): M.join(a)
    def test_incomplete_d01_d12_coverage_fail_closed(self):
        a=build_good(); c=country(a); c['routing_documentary_records']=[r for r in c['routing_documentary_records'] if r['gap_id']!='D09']
        with self.assertRaisesRegex(M.ValidationError,'incomplete D01-D12 coverage'): M.join(a)
    def test_unresolved_unknown_blocks(self):
        a=build_good(); c=country(a); r=c['routing_documentary_records'][0]; r['state']='DOCUMENT_NOT_LOCATED'; c['unknowns']=[{"unknown_id":"SYNTH-U","record_id":r['record_id'],"country":c['country'],"year":c['year'],"reason":"NON_AUTHORITATIVE_SYNTHETIC_ONLY","downstream_effect":"BLOCK","source_locator":"SYNTHETIC_TEST#unknown"}]
        with self.assertRaisesRegex(M.ValidationError,'UNRESOLVED_UNKNOWN'): M.join(a)

if __name__=='__main__': unittest.main(verbosity=2)
