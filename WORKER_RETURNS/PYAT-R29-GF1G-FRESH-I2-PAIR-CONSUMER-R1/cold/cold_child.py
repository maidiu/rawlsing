"""GF1G cold child — one real OS process, imports the staged GF1E consumer."""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

RET = Path(sys.argv[1]).resolve()
REPRO = RET / "court" / "repro"
RT = RET / "court" / "runtime_root"
os.chdir(REPRO)
sys.path[:0] = [str(REPRO), str(RT)]

import gf1_bootstrap as GB                                        # noqa: E402
import gf1_native as N                                            # noqa: E402
import generic_native_pair_relation as G                          # noqa: E402
import gf1_pair_support_consumer as C                             # noqa: E402

bundle = N.run_native(profile="BASELINE", root=GB.RT / f"gf1g_cold_{os.getpid()}")
items = N.collect_link_material(bundle)[0]
pair = next(i for i in items if i["kind"] == "QUERY"
            and G._ref_dict(i["query"].target_refs[0])["object_id"].endswith("m01-X"))
rel = G.produce_generic_native_pair_relation(
    joint_fact=pair["fact"], joint_query=pair["query"],
    conditioner_ref=pair["query"].target_refs[0],
    target_ref=pair["query"].target_refs[1],
    producer_permission_ceiling=("SOURCE_FREE_DEV",))
res = C.compute_pair_support_signature(rel)
src = Path(C.__file__).read_bytes()
print(json.dumps({
    "pid": os.getpid(),
    "python": sys.version.split()[0],
    "consumer_module_file": str(Path(C.__file__).resolve()),
    "consumer_module_sha256": hashlib.sha256(src).hexdigest(),
    "producer_module_file": str(Path(G.__file__).resolve()),
    "producer_sha256": hashlib.sha256(Path(G.__file__).read_bytes()).hexdigest(),
    "native_reattested": GB.REATTESTED,
    "relation_object_id": rel.object_id,
    "relation_content_hash": rel.content_hash,
    "roles": {"conditioner": rel.conditioner_source_native_variable,
              "target": rel.target_source_native_variable},
    "operation_role_order": rel.operation_role_order,
    "cells": {f"{r['condition_state']}{t['target_state']}": t["joint_support_count"]
              for r in rel.conditional_count_profile for t in r["target_counts"]},
    "denominators": {r["condition_state"]: r["condition_denominator_support"]
                     for r in rel.conditional_count_profile},
    "separation_class": res["separation_class"],
    "decision_state": res["decision_state"],
    "support_vectors": res["support_vectors"],
    "zero_cell_semantics": res["zero_cell_semantics"],
    "joint_support_total": res["joint_support_total"],
    "condition_states_with_positive_denominator":
        res["condition_states_with_positive_denominator"],
    "result_hash": res["result_hash"],
    "read_relation_object_id": res["read_relation_object_id"],
    "generic_native_semantics_hold": res["generic_native_semantics_hold"],
    "production_owner_commit": res["production_owner_commit"],
}, indent=1))
