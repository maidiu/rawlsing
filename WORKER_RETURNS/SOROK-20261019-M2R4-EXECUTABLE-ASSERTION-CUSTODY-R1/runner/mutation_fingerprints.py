#!/usr/bin/env python3
"""Record exact mutation fingerprints for every proof-witness claim."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
KERNEL = RETURN / "runs" / "r4_green" / "kernel.py"
CONTRACTS = [RETURN / "proofs" / "test_fresh_i2_adversarial.py.proof.json",
             RETURN / "proofs" / "test_r4_i2_new_hostiles.py.proof.json"]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    baseline = KERNEL.read_bytes()
    baseline_sha = sha(baseline)
    rows = []
    for contract_path in CONTRACTS:
        contract = json.loads(contract_path.read_text())
        for claim in contract["claims"]:
            fault = claim["fault"]
            old = fault["old"].encode()
            new = fault["new"].encode()
            count = baseline.count(old)
            mutant = baseline.replace(old, new, 1)
            rows.append(dict(
                claim_id=claim["claim_id"],
                contract=contract_path.name,
                positive_node=claim["positive_node"],
                fault_path=fault["path"],
                old_occurrences=count,
                old_sha256=sha(old),
                new_sha256=sha(new),
                patch_fingerprint=sha(sha(old).encode() + b"->" + sha(new).encode()),
                baseline_kernel_sha256=baseline_sha,
                mutant_kernel_sha256=sha(mutant),
                restored_kernel_sha256=baseline_sha,
                mutant_is_different=mutant != baseline,
            ))
    payload = dict(schema="SOROK_M2R4E_MUTATION_FINGERPRINTS@1",
                   kernel_path="runs/r4_green/kernel.py",
                   baseline_kernel_sha256=baseline_sha,
                   restored_kernel_sha256=sha(KERNEL.read_bytes()),
                   claims=rows)
    (RETURN / "evidence" / "mutation_fingerprints.json").write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"claims": len(rows), "restored": payload["restored_kernel_sha256"] == baseline_sha}))
    return 0 if all(r["old_occurrences"] == 1 and r["mutant_is_different"] for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
