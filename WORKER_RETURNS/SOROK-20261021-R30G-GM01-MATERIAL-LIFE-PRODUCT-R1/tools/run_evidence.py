"""Capture R30G GM01 material-to-product receipts."""
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

from generative_resource import bp2_test_only_resources, candidate_resource
from r30g.assertion import deny_no_material, p01, share_omit as share_omit_assert
from r30g.runner import build, observable
from r30g.scenarios import (
    share_e2, refuse_e2, share_omit, refuse_omit, share_contrary_omit, forged_e2,
)


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _run(root, scenario, perform):
    product, artifacts, producer = build(root, scenario["gm01"])
    try:
        observed = observable(product, perform=perform)
        episodes = [
            {"actor": row["actor_id"], "kind": row["kind"], "clock": row["clock"],
             "hash": row["hash"], "body": row["body"]}
            for row in product.store.episodes("root")
        ]
        state = product.store.latest_state("root")
        return {"observed": observed, "episodes": episodes,
                "c12": product.c12_verify(),
                "world": state["world"]["hash"],
                "artifacts": artifacts.public()}
    finally:
        product.close()
        producer.close()


def main():
    evidence = ROOT / "evidence"
    receipts = ROOT / "receipts"
    evidence.mkdir(exist_ok=True)
    receipts.mkdir(exist_ok=True)
    scenarios = {}
    with tempfile.TemporaryDirectory(prefix="r30g_evidence_") as tmp:
        base = Path(tmp)
        for name, fn, perform in (
            ("share_e2", share_e2, "e2"),
            ("refuse_e2", refuse_e2, "e2"),
            ("share_omit", share_omit, "omit"),
            ("refuse_omit", refuse_omit, "omit"),
            ("contrary_omit", share_contrary_omit, "omit"),
            ("forged_e2", forged_e2, "e2"),
        ):
            scenario = fn()
            run = _run(base / name, scenario, perform)
            scenarios[name] = {
                "gm01": scenario["gm01"],
                "resource_hash": scenario["resource_hash"],
                "p01": p01(run["observed"], scenario["gm01"]),
                "share_omit_assertion": share_omit_assert(run["observed"]),
                "deny_assertion": deny_no_material(run["observed"]),
                "run": run,
            }
        (evidence / "r30g_scenarios.json").write_text(
            json.dumps(scenarios, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf-8")

        # Cold reopen of the positive material product.
        code = (
            "import json,sys;"
            "from r30g.gm01_product import GM01Product;"
            "p=GM01Product.reopen(sys.argv[1]);o=p.observe_verified();"
            "e=p.store.episodes('root');"
            "print(json.dumps({'status':o.get('status'),"
            "'tools':o['self']['state'].get('tools_remaining'),"
            "'completed':o['self']['state'].get('completed_units'),"
            "'material':o['self']['state'].get('material_remaining'),"
            "'episodes':[x['kind'] for x in e],"
            "'bodies':[x['body'] for x in e],"
            "'other':p.other()['public']['completed_units'],"
            "'verify':p.c12_verify()},sort_keys=True,default=str));p.close()")
        env = dict(__import__("os").environ,
                   PYTHONPATH=":".join(str(p) for p in (
                       ROOT, ROOT / "r29m" / "source", ROOT / "candidate",
                       ROOT / "candidate" / "vendor" / "bp2",
                       ROOT / "candidate" / "vendor" / "bp4",
                       ROOT / "r29p", ROOT / "r26e", ROOT / "n1")),
                   PYTHONDONTWRITEBYTECODE="1")
        completed = subprocess.run(
            [sys.executable, "-B", "-c", code,
             str(base / "share_e2" / "product")],
            cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=240)
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr)
        cold = json.loads(completed.stdout.strip().splitlines()[-1])
        (evidence / "r30g_cold.json").write_text(
            json.dumps(cold, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf-8")

    import bp2_joined.bootstrap as bootstrap
    from bp2_joined import ports
    bootstrap.install()
    obj = bp2_test_only_resources(ports, candidate_resource(),
                                  "TEST_ONLY_R30G_A", 10)
    before = ports.production_registries()
    after = ports.production_registries()
    port_receipt = {
        "schema": "R30G_BP2_PORT_RECEIPT@1",
        "rule_a": {"resource_id": obj["rule_a"].resource_id,
                   "issuer_ref": obj["rule_a"].issuer_ref,
                   "content_hash": obj["rule_a"].content_hash,
                   "test_only": obj["rule_a"].test_only,
                   "native_grant": obj["rule_a"].native_grant},
        "rule_t": {"resource_id": obj["rule_t"].resource_id,
                   "issuer_ref": obj["rule_t"].issuer_ref,
                   "content_hash": obj["rule_t"].content_hash,
                   "test_only": obj["rule_t"].test_only,
                   "native_grant": obj["rule_t"].native_grant},
        "grant": obj["grant"],
        "native_issuer": obj["native_issuer"],
        "actual_target_mutations": obj["actual_target_mutations"],
        "production_registry_writes": obj["production_registry_writes"],
        "production_response_rules": before["response_rule_count"],
        "production_target_rules": before["target_rule_count"],
        "after_response_rules": after["response_rule_count"],
        "after_target_rules": after["target_rule_count"],
    }
    (evidence / "bp2_ports.json").write_text(
        json.dumps(port_receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")

    imports = {
        "schema": "R30G_IMPORT_CUSTODY@1",
        "python": sys.version,
        "model": "opencode-go/deepseek-v4.1-flash",
        "harness": "OpenCode",
        "files": {},
    }
    for relative in (
        "r29m/source/generative_resource.py",
        "r30g/gm01_product.py",
        "r30g/runner.py",
        "r30g/assertion.py",
        "candidate/stable_actor_binding.py",
        "candidate/historical_actor_producer.py",
        "r26e/c12_integrity.py",
        "r29p/product.py",
    ):
        path = ROOT / relative
        imports["files"][relative] = {
            "sha256": _sha(path),
            "bytes": path.stat().st_size,
        }
    (evidence / "imports.json").write_text(
        json.dumps(imports, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
