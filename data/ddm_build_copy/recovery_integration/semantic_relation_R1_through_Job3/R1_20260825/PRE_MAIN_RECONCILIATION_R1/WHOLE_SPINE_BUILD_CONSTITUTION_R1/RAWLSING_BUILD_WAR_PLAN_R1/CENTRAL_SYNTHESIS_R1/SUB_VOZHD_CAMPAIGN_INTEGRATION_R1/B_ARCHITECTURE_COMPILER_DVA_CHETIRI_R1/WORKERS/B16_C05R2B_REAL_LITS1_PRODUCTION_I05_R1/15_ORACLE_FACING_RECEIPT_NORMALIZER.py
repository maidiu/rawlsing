#!/usr/bin/env python3
"""Lossless B16 canonical DiscoveryResultReceipt envelope -> frozen-validator projection."""
from __future__ import annotations
import argparse, copy, json
from pathlib import Path

def project(run: dict) -> dict:
    out=copy.deepcopy(run)
    rows=[]
    for x in out["i05"]["receipts"]:
        row={
            "ref":{"kind":"DiscoveryResultReceipt@1.0.0","object_id":x["object_id"],"content_hash":x["content_hash"]},
            "typed_state":x["typed_state"],
            "authority_snapshot_refs":copy.deepcopy(x["authority_snapshot_refs"]),
            "dependency_refs":copy.deepcopy(x["dependency_refs"]),
            "producer_replay_locator_or_reference_root":copy.deepcopy(x["producer_replay_locator_or_reference_root"]),
        }
        row.update(copy.deepcopy(x["semantic_fields"]))
        rows.append(row)
    out["i05"]["receipts"]=rows
    return out

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("input",type=Path); p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(project(json.loads(a.input.read_text())),indent=2,sort_keys=True)+"\n")
