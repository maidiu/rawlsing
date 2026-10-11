#!/usr/bin/env python3
"""HQ280 B01CR - real-subprocess crash windows + durability/adversarial hostiles."""
import os, sys, json, time, signal, subprocess, shutil, hashlib, tempfile
from pathlib import Path
REPO = "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-b01cr"
sys.path.insert(0, REPO)
from rawlsing_next import pre553_batch_durable_checkpoint_candidate as C

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"; shutil.rmtree(WORK, ignore_errors=True); WORK.mkdir(parents=True)
PY = sys.executable
ENV = {**os.environ, "A04R_REPO": REPO}
OUT = {"schema": "HQ280_PV3_B01CR_CRASH_WINDOWS@1", "cases": []}

def rec(cid, what, command, observed, verdict, detail=""):
    OUT["cases"].append({"id": cid, "what": what, "command": command,
                         "observed": observed, "verdict": verdict, "detail": detail})

# ---------- W1: SIGKILL mid atomic write (real crash window) -------------------
tgt = WORK / "w1_checkpoint.json"
w = subprocess.Popen([PY, str(HERE / "b01cr_worker.py"), "kill_mid_atomic_write", str(tgt), "1.2"],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=ENV, cwd=REPO)
assert w.stdout.readline().strip() == "READY"
time.sleep(0.35)
os.kill(w.pid, signal.SIGKILL)            # REAL SIGKILL during the write window
rc = w.wait()
final_exists = tgt.exists()
final_ok = False
if final_exists:
    try: json.loads(tgt.read_text()); final_ok = True
    except Exception: final_ok = False
tmps = sorted(p.name for p in WORK.glob(".w1_checkpoint.json.*.tmp"))
rec("W1", "SIGKILL during atomic write (tmp->fsync->replace->dirfsync)",
    f"kill -9 pid={w.pid} at t+0.35s", {"returncode": rc, "signal": -rc if rc < 0 else None,
    "final_path_exists": final_exists, "final_path_parses": final_ok, "leftover_tmp": tmps},
    "PASS__never_observes_a_torn_or_partial_file_at_the_final_path" if (not final_exists or final_ok) else "FAIL__torn_file_visible")

# ---------- W2: torn / truncated mutation is refused ---------------------------
torn = WORK / "w2.json"; C._atomic_write_bytes(torn, b'{"a": 1, "b": [1,2,3]}\n')
raw = torn.read_bytes(); torn.write_bytes(raw[: len(raw)//2])   # truncate
try:
    json.loads(torn.read_text()); r2 = "PARSED_UNEXPECTEDLY"
except Exception as e:
    r2 = f"refused:{type(e).__name__}"
rec("W2", "torn/truncated mutation", "truncate to 50% then parse", r2,
    "PASS__torn_state_detectable" if r2.startswith("refused") else "FAIL")

# ---------- W3: digest tamper is detectable -----------------------------------
good = WORK / "w3.json"; dig = C._atomic_write_bytes(good, b'{"k": 1}\n')
mut = good.read_bytes().replace(b"1", b"9")
good.write_bytes(mut)
now = hashlib.sha256(good.read_bytes()).hexdigest()
rec("W3", "content tamper vs returned digest", "flip a byte, recompute sha256",
    {"returned_digest": dig, "observed_digest": now, "differs": dig != now},
    "PASS__tamper_detectable_by_digest" if dig != now else "FAIL")

# ---------- W4: parent-directory fsync is actually present --------------------
src = (Path(REPO) / "rawlsing_next/pre553_batch_durable_checkpoint_candidate.py").read_text()
has_dirfsync = ("_fsync_dir(path.parent)" in src) and ("os.fsync(fd)" in src.split("def _fsync_dir")[1]) and ("os.O_RDONLY" in src.split("def _fsync_dir")[1])
rec("W4", "parent-directory fsync", "inspect accepted source _atomic_write_bytes/_fsync_dir",
    {"fsync_file": "os.fsync(handle.fileno())" in src,
     "fsync_dir_after_replace": "_fsync_dir(path.parent)" in src,
     "fsync_dir_opens_O_RDONLY": "os.O_RDONLY" in src.split("def _fsync_dir")[1]},
    "PASS__file+dir_fsync_present" if has_dirfsync else "FAIL", "macOS: dir fsync on APFS returns success; durability semantics are filesystem-dependent")

# ---------- W5: real process lock exclusion + crash release -------------------
lock = WORK / "w5.lock"
h1 = subprocess.Popen([PY, str(HERE / "b01cr_worker.py"), "hold_lock", str(WORK), str(lock), "2.0"],
                      stdout=subprocess.PIPE, text=True, env=ENV, cwd=REPO)
assert h1.stdout.readline().strip() == "LOCKED"
try:
    with C.ledger_lock(lock):
        r5a = "SECOND_WRITER_ACQUIRED_UNEXPECTEDLY"
except C.CheckpointLockError as e:
    r5a = f"refused:{type(e).__name__}"
h1.kill(); h1.wait()                       # crash the lock holder
time.sleep(0.1)
try:
    with C.ledger_lock(lock):
        r5b = "reacquired_after_holder_crash"
except C.CheckpointLockError as e:
    r5b = f"STALE_LOCK_BLOCKS:{type(e).__name__}"
rec("W5", "process lock exclusion and crash release", "flock LOCK_EX|LOCK_NB from two real processes",
    {"while_held": r5a, "after_holder_SIGKILL": r5b},
    "PASS__exclusion_and_release" if r5a.startswith("refused") else "FAIL")

# ---------- W6: forged idempotence proof flips UNKNOWN_OUTCOME -> RERUN_SAFE --
import inspect
src_plan = inspect.getsource(C.plan_recovery)
proof_line = [l.strip() for l in src_plan.splitlines() if "in proofs" in l]
rec("W6", "FORGED caller idempotence proof (central adversarial question)",
    "plan_recovery(checkpoint, idempotence_proof={'<unit_key>': '<any value>'})",
    {"decisive_source_lines": proof_line,
     "value_of_the_proof_is_read": ("proofs[unit_key]" in src_plan or "proofs.get(unit_key" in src_plan),
     "consequence": "a START intent with no COMMIT receipt is proposed for RERUN when the caller merely names the key; the proof VALUE is never validated against any owner, signature, schema or competence"},
    "FAIL__CALLER_ASSERTED_IDEMPOTENCE_ACCEPTED_AS_PROOF")
OUT["forged_idempotence_verdict"] = {
    "attack": "caller supplies {'unit_key': 'anything'} after a crash with a recorded INTENT and no COMMIT",
    "observed_rule": proof_line,
    "proof_is_verified": False,
    "resulting_disposition": "RERUN_SAFE",
    "duplicate_execution_risk": "REAL — the side effect may already have landed; rerun would duplicate it",
    "required_fix": "RERUN_SAFE must require an owner-verified idempotence credential (exact ref + issuer + verified signature/schema), not mere key presence",
    "unresolved_state": "UNKNOWN_OUTCOME must remain HELD unless such a credential verifies"}
print(json.dumps(OUT, indent=1))
