"""Hostile reader tests, deliberately synthetic evidence (NOT real P6 proof)."""
import json,tempfile,unittest
from pathlib import Path
import measure as m
import read_receipts as r
class Attacks(unittest.TestCase):
    def setUp(self):
        x=tempfile.TemporaryDirectory();self.addCleanup(x.cleanup);self.p=Path(x.name)
        (self.p/"attempts").mkdir()
        self.source={f:"a"*64 for f in m.FILES}
        self.man={"schema":m.SCHEMA,"repo_sha":"b"*40,"source_hashes":self.source,
                  "runner_sha256":"c"*64,"python_executable_sha256":"d"*64,"os":"Linux",
                  "state_digest_scheme":m.STATE_DIGEST_SCHEME,
                  "state_logical_scheme":m.STATE_LOGICAL_SCHEME,
                  "env_keys":sorted(m.env_offline()),"env_fingerprint_sha256":"e"*64,
                  "provider_mode":"OFFLINE_VERIFIED_CHILD_ALLOWLIST","network_calls":"UNOBSERVED",
                  "descendant_processes":"UNOBSERVED",
                  "plan":[{"id":n,"args":a,"cold":n=="cold_view"} for n,a in m.PLAN]}
        self.save(self.p/"manifest.json",self.man)
        for i,(n,a) in enumerate(m.PLAN):
            d=self.p/"attempts"/n;d.mkdir()
            args=["/usr/bin/python","/tmp/repo/"+m.P6,"--state",str(self.p/"state"),*a]
            code=2 if i==4 else 0
            o={"status":"REFUSED","reason":"P6_WAIT_DURATION_OUT_OF_RANGE"} if code else {"clock":(248,248,249,249)[i],"mii_surface":{}}
            if i==2:o["admission"]="ADMITTED"
            b=m.data(o);(d/"stdout.bin").write_bytes(b);(d/"stderr.bin").write_bytes(b"")
            self.save(d/"start.json",{"id":n,"source_sha":"b"*40,"argv":args,"state_bytes_before":i*10})
            self.save(d/"receipt.json",{"schema":m.SCHEMA,"id":n,"source_sha":"b"*40,"source_hashes":self.source,
                "argv":args,"child_pid":100+i,"exit_code":code,"timeout":False,"wall_seconds":.2,
                "resources":{"status":"MEASURED","scope":"single_wait4_child_not_process_tree",
                    "cpu_user_s":.01,"cpu_system_s":.01,"ru_maxrss_native":4,
                    "ru_maxrss_native_unit":"KiB","peak_rss_bytes":4096},
                "direct_children_started":1,"descendants":"UNOBSERVED",
                "state_bytes_before":i*10,"state_bytes_after":(i*10 if i==4 else (i+1)*10),
                "stdout_sha256":r.sha(b),"stdout_bytes":len(b),
                "stderr_sha256":r.sha(b""),"stderr_bytes":0,
                "output":{"json":True,"status":o.get("status"),"clock":o.get("clock")},
                "provider_mode":"OFFLINE_VERIFIED_CHILD_ALLOWLIST","provider":m.missing_provider(),
                "cold":n=="cold_view",
                "cold_basis":"separate_python_exec_after_wait" if n=="cold_view" else "NOT_APPLICABLE"})
        # Synthetic state contents, not a physical P6 measurement.
        state=self.p/"state"
        snaps=[m.state_snapshot(state)]
        state.mkdir()
        for size in (10,20,30,40):
            (state/"payload.bin").write_bytes(b"X"*size)
            snaps.append(m.state_snapshot(state))
        for i,(name,_) in enumerate(m.PLAN):
            d=self.p/"attempts"/name
            start=json.loads((d/"start.json").read_text())
            rec=json.loads((d/"receipt.json").read_text())
            start["state_snapshot_before"]=snaps[i]
            rec["state_snapshot_before"]=snaps[i]
            rec["state_snapshot_after"]=snaps[min(i+1,4)]
            rec["state_logical_before"]=snaps[i]
            rec["state_logical_after"]=snaps[min(i+1,4)]
            self.save(d/"start.json",start)
            self.save(d/"receipt.json",rec)
        self.index()
    def save(self,p,x):p.write_bytes(m.data(x))
    def index(self):
        d={"attempts/"+n+"/"+f:r.sha((self.p/"attempts"/n/f).read_bytes())
           for n,_ in m.PLAN for f in ("start.json","receipt.json","stdout.bin","stderr.bin")}
        d["manifest.json"]=r.sha((self.p/"manifest.json").read_bytes())
        self.save(self.p/"index.json",{"schema":m.SCHEMA,"entries":d})
    def mutate(self,n,func,repair_index=True):
        p=self.p/"attempts"/n/"receipt.json";x=json.loads(p.read_text());func(x);self.save(p,x)
        if repair_index:self.index()
    def rejects(self,txt):
        with self.assertRaises(r.Reject) as ex:r.consume(self.p)
        self.assertIn(txt,str(ex.exception))
    def test_valid_synthetic_format_only(self):
        x=r.consume(self.p);self.assertEqual((x["attempts"],x["failed_or_refused"]),(5,1))
        self.assertTrue(x["expected_scenario_pass"])
        self.assertEqual((x["expected_refusals"],x["unexpected_failed_or_refused"]),(1,0))
        self.assertEqual(x["state_net_bytes"],40)
    def test_unexpected_failure_stays_in_denominator(self):
        self.mutate("view",lambda x:x.update(exit_code=3))
        x=r.consume(self.p)
        self.assertEqual((x["attempts"],x["unexpected_failed_or_refused"]),(5,1))
        self.assertFalse(x["expected_scenario_pass"])
    def test_missing_refusal_cannot_reduce_denominator(self):
        (self.p/"attempts/fail_wait/receipt.json").unlink();self.rejects("ATTEMPT_MISSING")
    def test_reduced_plan_rejected(self):
        self.man["plan"].pop();self.save(self.p/"manifest.json",self.man)
        self.index();self.rejects("PLAN_DENOMINATOR_REDUCED")
    def test_edited_receipt_caught_by_index(self):
        self.mutate("wait",lambda x:x.update(exit_code=5),False)
        self.rejects("RAW_EVIDENCE_EDITED")
    def test_source_forgery_even_if_index_recomputed(self):
        self.mutate("wait",lambda x:x.update(source_sha="f"*40))
        self.rejects("MIXED_SOURCE_CUT")
    def test_rss_units_rejected(self):
        self.mutate("wait",lambda x:x["resources"].update(ru_maxrss_native_unit="bytes"))
        self.rejects("RSS_UNITS_FALSE")
    def test_forged_bill_zero_rejected(self):
        self.mutate("wait",lambda x:x["provider"].update(billable_cost=0))
        self.rejects("COUNTER_ZERO_FORGED")
    def test_cold_lie_rejected(self):
        self.mutate("cold_view",lambda x:x.update(cold=False))
        self.rejects("COLD_CLAIM_FORGED")
    def test_stdout_mutation_rejected(self):
        (self.p/"attempts/view/stdout.bin").write_bytes(b"{}")
        self.rejects("RAW_EVIDENCE_EDITED")
    def test_false_stdout_interpretation_rejected(self):
        self.mutate("view",lambda x:x["output"].update(clock=999))
        self.rejects("OUTPUT_CLAIM_FALSE")
    def test_index_external_anchor_rejected(self):
        with self.assertRaisesRegex(r.Reject,"INDEX_EXTERNAL_ANCHOR_MISMATCH"):
            r.consume(self.p,"f"*64)
    def test_env_forged(self):
        self.man["env_keys"].append("SOROK_SITUATED_MODEL_API_KEY")
        self.save(self.p/"manifest.json",self.man);self.index();self.rejects("OFFLINE_OR_PROCESS_CLAIM_FALSE")
    def test_cold_clock_forgery_not_treated_as_success(self):
        path=self.p/"attempts/cold_view/stdout.bin"
        obj=json.loads(path.read_text());obj["clock"]=777;raw=m.data(obj);path.write_bytes(raw)
        receipt=self.p/"attempts/cold_view/receipt.json";row=json.loads(receipt.read_text())
        row["stdout_sha256"]=r.sha(raw);row["stdout_bytes"]=len(raw);row["output"]["clock"]=777
        self.save(receipt,row);self.index()
        self.assertFalse(r.consume(self.p)["expected_scenario_pass"])
    def test_expected_refusal_wrong_reason_not_accepted(self):
        path=self.p/"attempts/fail_wait/stdout.bin"
        obj=json.loads(path.read_text());obj["reason"]="P6_FAKE_OTHER_REFUSAL";raw=m.data(obj);path.write_bytes(raw)
        receipt=self.p/"attempts/fail_wait/receipt.json";row=json.loads(receipt.read_text())
        row["stdout_sha256"]=r.sha(raw);row["stdout_bytes"]=len(raw)
        self.save(receipt,row);self.index()
        self.assertFalse(r.consume(self.p)["expected_scenario_pass"])
    def test_altered_summary_rejected(self):
        report=r.consume(self.p)
        self.save(self.p/"summary.json",{**report,"attempts":4})
        self.rejects("SUMMARY_FORGED")
    def test_duplicate_child_id_rejected(self):
        self.mutate("cold_view",lambda x:x.update(child_pid=100))
        self.rejects("DUPLICATED_CHILD_EXEC_ID")
    def test_unwitnessed_sqlite_logical_digest_cannot_be_invented(self):
        self.mutate("fail_wait",lambda x:x["state_logical_after"].update(sha256="f"*64))
        self.rejects("STATE_FINAL_LOGICAL_MISMATCH")
    def test_dropped_logical_refusal_witness_rejected(self):
        self.mutate("fail_wait",lambda x:x.pop("state_logical_before"))
        self.rejects("STATE_SNAPSHOT_INVALID")
    def test_no_cumulative_rss_fabrication(self):
        self.assertEqual(m.process_usage(None)["status"],"UNOBSERVED")
if __name__=="__main__":unittest.main()
