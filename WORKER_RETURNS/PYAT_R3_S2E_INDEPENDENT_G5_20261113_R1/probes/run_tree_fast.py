"""Fast process-tree RSS sampler: pgrep children + one ps lookup per sample."""
import json
import subprocess
import sys
import time

cmd = sys.argv[1:]
start = time.time()
proc = subprocess.Popen(cmd)
max_tree = 0
max_single = 0
samples = 0
max_live = 0

def children(pid):
    try:
        out = subprocess.run(["pgrep", "-P", str(pid)], capture_output=True, text=True, timeout=2).stdout
    except subprocess.TimeoutExpired:
        return []
    return [int(x) for x in out.split() if x.strip().isdigit()]

while proc.poll() is None:
    pids = [proc.pid]
    frontier = [proc.pid]
    for _depth in range(8):
        nxt = []
        for p in frontier:
            nxt.extend(children(p))
        frontier = [p for p in nxt if p not in pids]
        pids.extend(frontier)
        if not frontier:
            break
    if pids:
        try:
            out = subprocess.run(
                ["ps", "-o", "rss=", "-p", ",".join(map(str, pids))],
                capture_output=True, text=True, timeout=2,
            ).stdout
            values = [int(x) for x in out.split() if x.strip().isdigit()]
        except subprocess.TimeoutExpired:
            values = []
        if values:
            max_tree = max(max_tree, sum(values))
            max_single = max(max_single, max(values))
            max_live = max(max_live, len(values))
            samples += 1
    time.sleep(0.05)

rc = proc.wait()
print("S2E_TREE_MONITOR_JSON=" + json.dumps({
    "schema": "PYAT_S2E_PROCESS_TREE_RSS@1",
    "exit": rc,
    "wall_seconds": round(time.time() - start, 3),
    "samples": samples,
    "max_process_tree_rss_kib": max_tree,
    "max_process_tree_rss_mib": round(max_tree / 1024, 1),
    "max_single_process_rss_kib": max_single,
    "max_live_processes": max_live,
}, sort_keys=True))
sys.exit(rc)
