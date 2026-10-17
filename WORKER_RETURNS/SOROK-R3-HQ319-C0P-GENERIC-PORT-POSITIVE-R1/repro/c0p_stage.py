#!/usr/bin/env python3
"""C0P independent staging — exact bytes from named commits, blob-authenticated.

Git blob SHA-1 is recomputed from the true binary preimage (b"blob " + len + NUL
+ bytes) and cross-checked against `git rev-parse <commit>:<path>`, plus SHA-256.
Nothing is trusted from any author's manifest or ledger.

Sources staged:
  SC0   generic two-contract port SPEC + frozen K9/K10 oracles (241d35fa)
  Pyat E06  native bridge candidate (9b51422d)
  Pyat GF1  generic native pair-relation candidate (894808d9)
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(os.environ["C0P_REPO"])
OUT = Path(os.environ["C0P_STAGE"])

SC0 = "WORKER_RETURNS/SOROK-R3-POSTASTRA-SC0-WORLD-PORT-CONTRACT-R1"
E06 = "WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-E06-E04E05-NATIVE-BRIDGE-R1"
GF1 = "WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1"

SC0_COMMIT = "241d35fa8a13ea03c68fbe55554ce81c210b745f"
E06_COMMIT = "9b51422d9e4a23b5f036f5fd8e81866a5745ac0f"
GF1_COMMIT = "894808d946c431d9b0105e04514cf1a7c9afe395"

# (commit, repo_path, staged_relpath)
CLOSURE = [
    (SC0_COMMIT, f"{SC0}/01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json", "sc0/01_envelope.json"),
    (SC0_COMMIT, f"{SC0}/02_K9_PROVIDER_SWAP_ORACLES.json", "sc0/02_k9_oracles.json"),
    (SC0_COMMIT, f"{SC0}/03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json", "sc0/03_k10_oracles.json"),
    (SC0_COMMIT, f"{SC0}/04_N9_N10E_N10W_OWNER_BINDING.md", "sc0/04_owner_binding.md"),
    (SC0_COMMIT, f"{SC0}/05_FREEZE_VS_UNRESOLVED_DECISIONS.md", "sc0/05_freeze_vs_unresolved.md"),
    (SC0_COMMIT, f"{SC0}/00_RETURN.md", "sc0/00_return.md"),
    (E06_COMMIT, f"{E06}/bridge.py", "pyat_e06/bridge.py"),
    (E06_COMMIT, f"{E06}/01_FROZEN_E04T_E05R_BRIDGE_CONTRACT.json", "pyat_e06/01_frozen_bridge_contract.json"),
    (E06_COMMIT, f"{E06}/02_ACTUAL_NATIVE_TO_TWO_CONSUMER_PRODUCTS.json", "pyat_e06/02_two_consumer_products.json"),
    (E06_COMMIT, f"{E06}/03_CROSS_BOUNDARY_GRANT_LOSS_RESTORATION_COLD_HOSTILES.md", "pyat_e06/03_hostiles.md"),
    (E06_COMMIT, f"{E06}/04_OWNER_INSTALLATION_AND_ISSUER_HOLDS.md", "pyat_e06/04_owner_holds.md"),
    (E06_COMMIT, f"{E06}/00_RETURN.md", "pyat_e06/00_return.md"),
    (E06_COMMIT, f"{E06}/README.md", "pyat_e06/README.md"),
    (GF1_COMMIT, f"{GF1}/court/repro/gf1_native.py", "pyat_gf1/gf1_native.py"),
    (GF1_COMMIT, f"{GF1}/court/repro/gf1_bootstrap.py", "pyat_gf1/gf1_bootstrap.py"),
    (GF1_COMMIT, f"{GF1}/court/repro/test_gf1_generic_pair.py", "pyat_gf1/test_gf1_generic_pair.py"),
    (GF1_COMMIT, f"{GF1}/00_RETURN.md", "pyat_gf1/00_return.md"),
    (GF1_COMMIT, f"{GF1}/03_SOURCE_ROLES_MISSING_COLD_GRANT_HOSTILES.md", "pyat_gf1/03_hostiles.md"),
    (GF1_COMMIT, f"{GF1}/04_FIELD_FORGE_GENERIC_SEMANTIC_OWNER_WARRANT.md",
     "pyat_gf1/04_field_forge_warrant.md"),
]


def blob_of(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ledger, failures = [], []
    for commit, path, staged in CLOSURE:
        data = subprocess.run(["git", "-C", str(REPO), "cat-file", "blob", f"{commit}:{path}"],
                              check=True, capture_output=True).stdout
        store = subprocess.run(["git", "-C", str(REPO), "rev-parse", f"{commit}:{path}"],
                               check=True, capture_output=True, text=True).stdout.strip()
        b, s = blob_of(data), hashlib.sha256(data).hexdigest()
        ok = b == store
        if not ok:
            failures.append(staged)
        dest = OUT / staged
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        ledger.append(dict(commit=commit, repo_path=path, staged=staged, bytes=len(data),
                           computed_blob_sha1=b, git_store_blob_sha1=store,
                           computed_sha256=s, all_match=ok))
        print(f"{'OK  ' if ok else 'FAIL'} {staged:52s} blob={b[:14]} bytes={len(data)}")
    (OUT.parent / "_c0p_stage_ledger.json").write_text(
        json.dumps(dict(ledger=ledger, failures=failures), indent=2) + "\n")
    print(f"\n{len(ledger)} objects; FAILURES: {failures or 'none'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
