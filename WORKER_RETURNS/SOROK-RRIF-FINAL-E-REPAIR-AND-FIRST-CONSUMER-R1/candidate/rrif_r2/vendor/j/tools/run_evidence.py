"""Capture R31J pre-C9 source and product receipts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "r29m" / "source", ROOT / "candidate",
             ROOT / "candidate" / "vendor" / "bp2",
             ROOT / "candidate" / "vendor" / "bp4",
             ROOT / "r29p", ROOT / "r26e", ROOT / "n1"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from r31j.assertion import p01, share_omit as share_omit_assert
from r31j.build import c9_only, product
from r31j.scenarios import evaluated


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _run_product(root, scenario, perform):
    product_obj, built, producer = product(
        root, gm01=scenario["gm01"], case=scenario["case"],
        need_e2=True, perform=perform)
    try:
        a0 = product_obj.observe_verified()
        action = (product_obj.material_inspect() if perform == "e2"
                  else product_obj.record_omission())
        waited = product_obj.wait(30)
        other = product_obj.other()
        state = product_obj.store.latest_state("root")
        episodes = product_obj.store.episodes("root")
        source = next(e for e in episodes if e["kind"] == "GM01_SOURCE")["body"]["gm01_source"]
        decision = producer.pipeline.decision
        target_body = producer.c9.read_target_state(decision.target_id) if decision else None
        return {
            "gm01": scenario["gm01"],
            "resource_hash": scenario["resource_hash"],
            "source": source,
            "c8_payload_gm01": producer.out9.event.get("payload", {}).get("gm01_pre_c9_source"),
            "c8_state_digest": built["c8_state_digest"],
            "c8_content_hash": producer.out9.event.get("content_hash"),
            "e1_event_hash": built["e1_event_hash"],
            "c9": {
                "target_branch": decision.branch.value if decision else "",
                "target_reason": decision.reason.value if decision else "",
                "target_id": decision.target_id if decision else "",
                "record_hash": decision.record_hash if decision else "",
                "causal_parent_refs": list((decision.record_body or {}).get("causal_parent_refs", []))
                if decision else [],
                "response_hash": producer.response_hash,
                "rule_a_hash": dict(producer.rule_a.body)["rule_content_hash"],
                "rule_t_hash": dict(producer.rule_t.body)["rule_t_content_hash"],
                "grant_hash": producer.grant.content_hash,
            },
            "target_body": target_body,
            "a0": {
                "tools": a0["self"]["state"].get("tools_remaining"),
                "material": a0["self"]["state"].get("material_remaining"),
                "completed": a0["self"]["state"].get("completed_units"),
                "claims": [c["kind"] for c in a0.get("claims", [])],
                "c12_verify": a0.get("c12_verify"),
            },
            "action": action,
            "wait": waited,
            "other_units": other["public"]["completed_units"],
            "after": state["world"]["actor_state"]["A"],
            "episodes": [{"actor": e["actor_id"], "kind": e["kind"],
                          "clock": e["clock"], "hash": e["hash"],
                          "body": e["body"]} for e in episodes],
            "p01": p01({
                "status": a0.get("status"), "claims": [c["kind"] for c in a0.get("claims", [])],
                "tools_before": a0["self"]["state"].get("tools_remaining"),
                "tools_after": state["world"]["actor_state"]["A"].get("tools_remaining"),
                "completed_before": a0["self"]["state"].get("completed_units"),
                "completed_after": state["world"]["actor_state"]["A"].get("completed_units"),
                "material_before": a0["self"]["state"].get("material_remaining"),
                "material_after": state["world"]["actor_state"]["A"].get("material_remaining"),
                "action": action, "a2_other_units": other["public"]["completed_units"],
                "a2_offscreen": [product_obj.store.world_event("root", e)["kind"]
                                 for e in waited.get("offscreen_events", [])],
                "source_episode": {"body": {"gm01_source": source}},
                "c12_verify": a0.get("c12_verify"),
                "c8_state_digest": built["c8_state_digest"],
            }, scenario["gm01"]),
        }
    finally:
        product_obj.close()
        producer.close()


def main():
    evidence = ROOT / "evidence"
    receipts = ROOT / "receipts"
    evidence.mkdir(exist_ok=True)
    receipts.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="r31j_evidence_") as tmp:
        base = Path(tmp)
        share = evaluated(share=True, e2=True)
        refuse = evaluated(share=False, e2=True)
        omit = evaluated(share=True, e2=False)
        share_run = _run_product(base / "share", share, "e2")
        omit_run = _run_product(base / "omit", omit, "omit")
        partial, producer = c9_only(base / "refuse", gm01=refuse["gm01"],
                                    case=refuse["case"])
        try:
            refuse_receipt = {
                "gm01": refuse["gm01"], "resource_hash": refuse["resource_hash"],
                "c8_state_digest": partial["c8_state_digest"],
                "e1_event_hash": partial["e1_event_hash"],
                "c8_payload_gm01": producer.out9.event.get("payload", {}).get("gm01_pre_c9_source"),
                "c9": partial["c9"], "material_access": partial["material_access"],
            }
        finally:
            producer.close()
        cold_code = (
            "import json,sys;from r31j.product import R31JProduct;"
            "p=R31JProduct.reopen(sys.argv[1]);o=p.observe_verified();"
            "e=p.store.episodes('root');print(json.dumps({'status':o.get('status'),"
            "'tools':o['self']['state'].get('tools_remaining'),"
            "'completed':o['self']['state'].get('completed_units'),"
            "'material':o['self']['state'].get('material_remaining'),"
            "'episodes':[x['kind'] for x in e],"
            "'source':[x['body']['gm01_source'] for x in e if x['kind']=='GM01_SOURCE'],"
            "'c8':o.get('c8'),'target':o.get('c9'),'verify':p.c12_verify()},sort_keys=True,default=str));p.close()")
        import os
        env = dict(os.environ, PYTHONPATH=":".join(str(p) for p in (
            ROOT, ROOT / "r29m" / "source", ROOT / "candidate",
            ROOT / "candidate" / "vendor" / "bp2",
            ROOT / "candidate" / "vendor" / "bp4",
            ROOT / "r29p", ROOT / "r26e", ROOT / "n1")),
            PYTHONDONTWRITEBYTECODE="1")
        completed = subprocess.run(
            [sys.executable, "-B", "-c", cold_code,
             str(base / "share" / "product")],
            cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=240)
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr)
        cold = json.loads(completed.stdout.strip().splitlines()[-1])
        payload = {
            "schema": "R31J_NATIVE_CHAIN@1",
            "share_e2": share_run,
            "share_omit": omit_run,
            "refuse_c9": refuse_receipt,
            "cold": cold,
        }
        (evidence / "r31j_chain.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
