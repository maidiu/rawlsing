"""GF1F — capture the real frozen44 dispositions and the executed consumer values."""
import hashlib
import json
import os
import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
PINCAND = RET / "candidate" / "court" / "runtime_root"
COURT_REPRO = RET / "candidate" / "court" / "repro"
sys.path[:0] = [str(RET / "repro"), str(COURT_REPRO), str(PINCAND)]

import gf1_pair_support_consumer as C
import generic_native_pair_relation as R
from independent_relation import build_relation


def git_blob(p):
    b = Path(p).read_bytes()
    h = hashlib.sha1()
    h.update(b"blob " + str(len(b)).encode() + b"\0" + b)
    return h.hexdigest()


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


oracle = json.loads((RET / "01_INDEPENDENT_FROZEN_PAIR_ORACLE.json").read_text())

universe_values = []
for row in oracle["universe"]:
    cells = row["cells"]
    out = C.compute_pair_support_signature(build_relation(cells, eligible=row["eligible"]))
    universe_values.append(dict(
        cells=cells, expected_class=row["expected_class"],
        actual_class=out["separation_class"],
        support_vectors=out["support_vectors"],
        joint_support_total=out["joint_support_total"],
        condition_states_with_positive_denominator=out["condition_states_with_positive_denominator"],
        result_hash=out["result_hash"],
    ))

named = {}
for name, case in oracle["named_cases"].items():
    cells = {k: case[k] for k in ("00", "01", "10", "11")}
    out = C.compute_pair_support_signature(build_relation(cells))
    named[name] = dict(cells=cells, expected_class=case["expected_class"],
                       actual_class=out["separation_class"], result_hash=out["result_hash"])

# real native baseline relation -> consumer
real = None
try:
    import gf1_bootstrap as GB
    import gf1_native as N
    from generic_native_pair_relation import produce_generic_native_pair_relation as PRODUCE
    bundle = N.run_native(profile="BASELINE", root=GB.RT / "gf1_run")
    items, _ = N.collect_link_material(bundle)
    item = [it for it in items if it["kind"] == "QUERY"][0]
    rel = PRODUCE(joint_fact=item["fact"], joint_query=item["query"],
                  conditioner_ref=item["query"].target_refs[0],
                  target_ref=item["query"].target_refs[1],
                  producer_permission_ceiling=("SOURCE_FREE_DEV",))
    out = C.compute_pair_support_signature(rel)
    real = dict(relation_object_id=rel.object_id, relation_content_hash=rel.content_hash,
                eligible_joint_risk_total=rel.eligible_joint_risk_total,
                consumer=out)
except Exception as exc:  # noqa: BLE001 - record, never fake
    real = {"error": type(exc).__name__ + ": " + str(exc)}

consumer_file = Path(C.__file__).resolve()
relation_file = Path(R.__file__).resolve()
record = dict(
    schema="GF1F_REAL_FROZEN44_AND_CONSUMER_VALUES@1",
    candidate="eeb726357204653b22458dc267dd70ba0009bd77",
    universe=universe_values,
    named_cases=named,
    real_native_baseline=real,
    imports=[
        dict(module="gf1_pair_support_consumer", file=consumer_file.name,
             sha256=sha256(consumer_file), git_blob_sha1=git_blob(consumer_file)),
        dict(module="generic_native_pair_relation", file=relation_file.name,
             sha256=sha256(relation_file), git_blob_sha1=git_blob(relation_file)),
    ],
)
(RET / "02_REAL_FROZEN44_AND_CONSUMER_VALUES.json").write_text(
    json.dumps(record, indent=1, sort_keys=True) + "\n")
print("universe recorded", len(universe_values),
      "| classes", {c: sum(1 for v in universe_values if v["actual_class"] == c)
                    for c in set(v["actual_class"] for v in universe_values)})
print("real native baseline class:",
      real.get("consumer", {}).get("separation_class") if "consumer" in real else real)
print("consumer sha256", sha256(consumer_file))
