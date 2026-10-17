"""GF1E — execution evidence for the named consumer.

Produces 02_EXECUTED_CONSUMER_EVIDENCE.json: the consumer outputs for the four
differential patterns plus a real native-chain baseline relation, and the
physical import identities (module __file__ + Git blob) of the consumer and the
relation owner.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
WORKER_RETURNS = RET.parent
GF1_COURT = WORKER_RETURNS / "PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1" / "court"
GF1_RT = GF1_COURT / "runtime_root"
GF1_REPRO = GF1_COURT / "repro"
sys.path[:0] = [str(RET / "repro"), str(GF1_REPRO), str(GF1_RT)]

from gf1e_relations import four_relations                  # noqa: E402
from gf1_pair_support_consumer import compute_pair_support_signature  # noqa: E402


def git_blob(path: Path) -> str:
    b = path.read_bytes()
    h = hashlib.sha1()
    h.update(b"blob " + str(len(b)).encode() + b"\0" + b)
    return h.hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


patterns = {name: compute_pair_support_signature(rel)
            for name, rel in four_relations().items()}

real = None
real_relation = None
import gf1_bootstrap as GB                                # noqa: E402
import gf1_native as N                                    # noqa: E402
from generic_native_pair_relation import (                # noqa: E402
    produce_generic_native_pair_relation as PRODUCE_GENERIC)

bundle = N.run_native(profile="BASELINE", root=GB.RT / "gf1_run")
items, _ = N.collect_link_material(bundle)
item = [it for it in items if it["kind"] == "QUERY"][0]
real_relation = PRODUCE_GENERIC(
    joint_fact=item["fact"], joint_query=item["query"],
    conditioner_ref=item["query"].target_refs[0],
    target_ref=item["query"].target_refs[1],
    producer_permission_ceiling=("SOURCE_FREE_DEV",))
real = compute_pair_support_signature(real_relation)

import gf1_pair_support_consumer as consumer_mod           # noqa: E402
import generic_native_pair_relation as relation_mod        # noqa: E402

consumer_file = Path(consumer_mod.__file__).resolve()
relation_file = Path(relation_mod.__file__).resolve()

evidence = dict(
    schema="PYAT_R27_GF1E_02_EXECUTED_CONSUMER_EVIDENCE@1",
    consumer_source="gf1_pair_support_consumer.py",
    differential_patterns=patterns,
    real_native_baseline=dict(
        relation_object_id=real_relation.object_id,
        relation_content_hash=real_relation.content_hash,
        operation_role_order=real_relation.operation_role_order,
        roles=dict(conditioner=real_relation.conditioner_source_native_variable,
                   target=real_relation.target_source_native_variable),
        eligible_joint_risk_total=real_relation.eligible_joint_risk_total,
        consumer=real,
    ),
    import_identities=[
        dict(module=consumer_mod.__name__,
             file=str(consumer_file.relative_to(WORKER_RETURNS.parent)),
             git_blob_sha1=git_blob(consumer_file),
             sha256=sha256(consumer_file)),
        dict(module=relation_mod.__name__,
             file=str(relation_file.relative_to(WORKER_RETURNS.parent)),
             git_blob_sha1=git_blob(relation_file),
             sha256=sha256(relation_file)),
    ],
)
(RET / "02_EXECUTED_CONSUMER_EVIDENCE.json").write_text(
    json.dumps(evidence, indent=1, sort_keys=True) + "\n")
print("consumer classes:", {k: v["separation_class"] for k, v in patterns.items()})
print("real baseline class:", real["separation_class"])
print("consumer file:", consumer_file.name, "blob", git_blob(consumer_file)[:12])
