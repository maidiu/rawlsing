"""GF1K fresh-process import/identity and genuine relation replay."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path

COURT = Path(os.environ["GF1K_COURT"]).resolve()
GF1G = Path(os.environ["GF1K_GF1G"]).resolve()
os.environ["GF1G_COURT"] = str(COURT)
os.environ["GF1G_ORACLE"] = str(GF1G / "01_FROZEN_ORACLE.json")
spec = importlib.util.spec_from_file_location(
    "gf1g_fixture", GF1G / "phase_a/test_gf1g_precommitted.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
import gf1_pair_support_consumer as consumer

relation = module._template()
result = consumer.compute_pair_support_signature(relation)
print(json.dumps({
    "pid": os.getpid(),
    "consumer_file": str(Path(consumer.__file__).resolve()),
    "consumer_sha256": hashlib.sha256(Path(consumer.__file__).read_bytes()).hexdigest(),
    "relation_hash": relation.content_hash,
    "result_hash": result["result_hash"],
    "separation_class": result["separation_class"],
    "role_order": result["operation_role_order"],
    "production_owner_commit": result["production_owner_commit"],
}, sort_keys=True))
