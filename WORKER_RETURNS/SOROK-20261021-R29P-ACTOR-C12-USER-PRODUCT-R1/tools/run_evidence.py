"""Run R29P sourcefree product and fault evidence into JSON receipts."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in (
    ROOT, ROOT / "candidate", ROOT / "candidate" / "vendor" / "bp2",
    ROOT / "candidate" / "vendor" / "bp4", ROOT / "r26e", ROOT / "n1",
):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from r29p.faults import seven_trials
from r29p.runner import build_bundle, observable, run_fork, run_m6


def _cold(root: Path, branch: str = "root") -> dict:
    code = (
        "import json,sys;"
        "from r29p.product import R29PProduct;"
        "p=R29PProduct.reopen(sys.argv[1], branch_id=sys.argv[2]);"
        "obs=p.observe_verified();"
        "eps=p.store.episodes(p.branch_id);"
        "out={'status':obs.get('status'),'claims':[c['kind'] for c in obs.get('claims',[])],"
        "'others':[o['actor'] for o in obs.get('others_present',[])],"
        "'tools':obs.get('self',{}).get('state',{}).get('tools_remaining'),"
        "'episodes':[e['kind'] for e in eps],"
        "'b_episodes':[e['kind'] for e in eps if e['actor_id']=='B'],"
        "'verify':p.c12_verify()};"
        "p.close();print(json.dumps(out,sort_keys=True))"
    )
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(str(p) for p in (
        ROOT, ROOT / "candidate", ROOT / "candidate" / "vendor" / "bp2",
        ROOT / "candidate" / "vendor" / "bp4", ROOT / "r26e")),
        PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(
        [sys.executable, "-B", "-c", code, str(root), branch],
        cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=240)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr)
    return json.loads(completed.stdout.strip().splitlines()[-1])


def main() -> int:
    evidence = ROOT / "evidence"
    evidence.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="r29p_evidence_") as tmp:
        base = Path(tmp)
        product, artifacts, producer = build_bundle(base / "baseline")
        try:
            observed = observable(product)
            baseline = {
                "schema": "R29P_BASELINE_RECEIPT@1",
                "observable": observed,
                "artifacts": artifacts.public(),
                "c12_verify": product.c12_verify(),
                "episodes": [
                    {"actor_id": row["actor_id"], "kind": row["kind"],
                     "clock": row["clock"], "hash": row["hash"]}
                    for row in product.store.episodes("root")
                ],
                "c12_path": str(product.store.path),
            }
        finally:
            product.close()
            producer.close()
        cold = _cold(base / "baseline" / "product", "root")
        (evidence / "r29p_baseline.json").write_text(
            json.dumps(baseline, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf-8")
        (evidence / "r29p_cold.json").write_text(
            json.dumps({"schema": "R29P_COLD_RECEIPT@1", "root": cold},
                       indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        fork = run_fork(base / "fork")
        (evidence / "r29p_fork.json").write_text(
            json.dumps(fork, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf-8")
        m6 = run_m6(base / "m6")
        (evidence / "r29p_m6.json").write_text(
            json.dumps(m6, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf-8")
        faults = seven_trials(base / "faults")
        (evidence / "r29p_seven_faults.json").write_text(
            json.dumps(faults, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf-8")
        summary = {
            "schema": "R29P_EVIDENCE_SUMMARY@1",
            "baseline_status": observed.get("status"),
            "baseline_claims": observed.get("claims"),
            "baseline_tools": observed.get("tools"),
            "baseline_a2_other_units": observed.get("a2_other_units"),
            "baseline_c12": baseline["c12_verify"],
            "cold_status": cold.get("status"),
            "cold_verify": cold.get("verify"),
            "fork_shared_before": fork["shared_before"]["equal"],
            "fork_shared_after": fork["shared_after"]["equal"],
            "fork_alt_episodes": fork["alt_verify"]["counts"]["episode"],
            "fork_root_episodes": fork["root_verify"]["counts"]["episode"],
            "m6_before_offscreen": any(
                row[0] == "OFFSCREEN_REPAIR" for row in m6["before_claims"]),
            "m6_after_offscreen": any(
                row[0] == "OFFSCREEN_REPAIR" for row in m6["after_claims"]),
            "seven_all_proved": faults["all_proved"],
            "seven_edges": [row["edge"] for row in faults["trials"]],
            "native": False,
            "grade": "TEST_ONLY_SOURCEFREE_R29P_NOT_NATIVE",
        }
        (evidence / "r29p_evidence_summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
