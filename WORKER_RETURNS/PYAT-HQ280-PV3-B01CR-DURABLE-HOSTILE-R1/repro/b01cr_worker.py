"""HQ280 B01CR kill-target worker: real process, real durability primitives."""
import os, sys, signal, time, json
sys.path.insert(0, os.environ["A04R_REPO"])
from pathlib import Path
from rawlsing_next import pre553_batch_durable_checkpoint_candidate as C

mode, target = sys.argv[1], Path(sys.argv[2])
if mode == "kill_mid_atomic_write":
    # ask the parent to SIGKILL us partway through the atomic write
    print("READY", flush=True)
    time.sleep(float(sys.argv[3]))
    C._atomic_write_bytes(target, b"X" * 4_000_000)
    print("COMPLETED", flush=True)
elif mode == "hold_lock":
    lock = Path(sys.argv[3])
    with C.ledger_lock(lock):
        print("LOCKED", flush=True)
        time.sleep(float(sys.argv[4]))
