#!/usr/bin/env python3
"""HQ280 B01DR - independent attacks on the B01D fail-closed idempotence repair."""
import json, os, subprocess, signal, sys, time, hashlib
from pathlib import Path
REPO="/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-b01dr"
sys.path.insert(0, REPO)
from rawlsing_next import pre553_batch_durable_checkpoint_candidate as cp
import importlib
T = importlib.import_module("rawlsing_next.tests.test_pre553_batch_durable_checkpoint_candidate")
OUT={"schema":"HQ280_PV3_B01DR_HOSTILES@1","cases":[]}
def rec(i,what,observed,verdict): OUT["cases"].append({"id":i,"what":what,"observed":observed,"verdict":verdict})

man = T._manifest(3)
ident = T._identity(man)
# build an INTENT-only checkpoint carrying a real durable START intent
rec0 = cp.UnitRecord(unit_key=ident.unit_keys[0], unit_ref=cp.ExactRef("Unit","urn:x",hashlib.sha256(b"u").hexdigest()),
                     state=cp.UNIT_STATE_INTENT, attempt_index=1, intent_hash=hashlib.sha256(b"i").hexdigest(),
                     receipt_projection=None, receipt_hash=None)
ck = cp.DurableCheckpoint(identity=ident, records=(rec0,), sequence=1) if "sequence" in cp.DurableCheckpoint.__dataclass_fields__ else cp.DurableCheckpoint(identity=ident, records=(rec0,))

def plan(proof):
    return cp.plan_recovery(ck, idempotence_proof=proof)

# ---- A: forged proofs of many shapes must NEVER yield RERUN_SAFE ----
SHAPES = {
 "empty_string": {"<K>": ""},
 "whitespace": {"<K>": "   "},
 "nonempty_string": {"<K>": "owner-approved-idempotent"},
 "dict_value": {"<K>": {"issuer":"me","signature":"deadbeef"}},
 "bool_true": {"<K>": True},
 "cross_unit": {"<OTHER_UNIT>": "valid-looking"},
 "manifest_derived": {"<K>": hashlib.sha256(b"manifest").hexdigest()},
 "nested": {"<K>": {"proof": {"signature": "x"}}},
}
findings=[]
for name, raw in SHAPES.items():
    proof = { (ident.unit_keys[0] if k=="<K>" else ident.unit_keys[1] if k=="<OTHER_UNIT>" else k): v for k,v in raw.items() }
    p = plan(proof)
    d = p.dispositions if hasattr(p,"dispositions") else {}
    vals = set(d.values()) if d else set()
    got_rerun = any(str(v).endswith("RERUN_SAFE") for v in vals)
    disregarded = getattr(p, "disregarded_caller_proofs", None)
    findings.append({"shape":name,"rerun_safe_granted":got_rerun,
                     "dispositions":sorted(str(v) for v in vals),
                     "disregarded_recorded":bool(disregarded)})
rec("A","forged idempotence proofs of 8 shapes",
    {"shapes":findings,"any_rerun_safe":any(f["rerun_safe_granted"] for f in findings)},
    "PASS__fail_closed" if not any(f["rerun_safe_granted"] for f in findings) else "FAIL__promotion_possible")

# ---- B: UNKNOWN_OUTCOME held on the intent unit ----
p = plan(None); d = p.dispositions if hasattr(p,"dispositions") else {}
held_ok = str(d.get(ident.unit_keys[0])) .endswith("UNKNOWN_OUTCOME")
rec("B","UNKNOWN_OUTCOME held without proof",{"disposition":str(d.get(ident.unit_keys[0]))},
    "PASS__held" if held_ok else "FAIL")

# ---- C: any other code path to RERUN_SAFE? ----
src = Path(REPO,"rawlsing_next/pre553_batch_durable_checkpoint_candidate.py").read_text()
assign = [l.strip() for l in src.splitlines() if "RERUN_SAFE" in l and "=" in l and "==" not in l and "!=" not in l]
rec("C","alternate code paths assigning RERUN_SAFE",{"assignments":assign},
    "PASS__none" if not assign else "REVIEW")

# ---- D: real-SIGKILL-after-intent resume ----
# This reviewer's own B01CR lane already executed a REAL SIGKILL against the
# shared durability primitives (W1: kill -9 mid atomic write -> rc -9, never a
# torn file at the final path) and B01D's own suite includes
# test_real_sigkill_after_durable_intent_leaves_checkpoint_and_holds.
# Reproducing that here would duplicate it rather than add evidence, so it is
# recorded as NOT_EXECUTED_IN_THIS_SCRIPT rather than claimed as a PASS.
rec("D","real SIGKILL after durable intent + fresh-process resume with forged proof",
    {"status":"NOT_EXECUTED_IN_THIS_SCRIPT",
     "covered_elsewhere":["reviewer B01CR W1 real SIGKILL atomicity (rc -9, no torn final file)",
                          "B01D suite test_real_sigkill_after_durable_intent_leaves_checkpoint_and_holds"]},
    "NOT_EXECUTED__NOT_CLAIMED_AS_PASS")

OUT["summary"]={"rerun_safe_reachable":any(f["rerun_safe_granted"] for f in findings),
 "unknown_outcome_held":held_ok,"real_crash_held":"NOT_EXECUTED_IN_THIS_SCRIPT (see B01CR W1 + B01D suite)",
 "verdict":"FAIL_CLOSED_REPAIR_CONFIRMED" if (not any(f["rerun_safe_granted"] for f in findings) and held_ok ) else "REPAIR_INCOMPLETE"}
print(json.dumps(OUT,indent=1))
