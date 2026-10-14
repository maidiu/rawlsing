#!/usr/bin/env python3
"""Stage exact authorized sourcefree imports with verified Git blob preimages.

Usage: python3 staging/stage_coverage.py   (from the return directory)
Writes staged files under staging/ns/ and a staging_manifest.json with observed
git hash-object SHA-1 vs pinned expected blobs.  No owner file is modified.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
NS = RETURN / "staging" / "ns"

# (source rev, repo-relative path, expected git blob sha1, staged relative path)
PINS = [
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "rawlsing_next/pre553_analytical_composition.py",
     "604c8d591d4cc2b646e9b149cdb233fc9d69cf6b",
     "rawlsing_next/pre553_analytical_composition.py"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "rawlsing_next/pre553_empirical_possibility_provider.py",
     "23167aa25291fb148b1e3cf210ac33fe7769b783",
     "rawlsing_next/pre553_empirical_possibility_provider.py"),
    ("b497f85713847cecc169d4d71c7629655d562dc0",
     "rawlsing_next/pre553_postastra_pe_generic_world_possibility.py",
     "58484f4c3d9aae148d4116dcf00420c432aefcbd",
     "rawlsing_next/pre553_postastra_pe_generic_world_possibility.py"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "rawlsing_next/tests/n10e_empirical_slice_fixture.py",
     "0e384f72fa615dc72a0dcb08a36472a64b7b1e4a",
     "rawlsing_next/tests/n10e_empirical_slice_fixture.py"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "rawlsing_next/tests/n10e_at17_successor_requal.py",
     "35b2427c0c5ef97bcd53d20f5dee9d365228459b",
     "rawlsing_next/tests/n10e_at17_successor_requal.py"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "rawlsing_next/tests/c1_at08_at13_fixture.py",
     "0393cc8c17a313b7944b2a5287d0406d6cbe3849",
     "rawlsing_next/tests/c1_at08_at13_fixture.py"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "rawlsing_next/tests/test_pre553_empirical_possibility_provider.py",
     "f776cc2b26be222132d86abbcb1ad429991fa61d",
     "rawlsing_next/tests/test_pre553_empirical_possibility_provider.py"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "rawlsing_next/tests/test_pre553_analytical_composition.py",
     "2210fc1b4cb99552aafc8797c12d780a78e7983b",
     "rawlsing_next/tests/test_pre553_analytical_composition.py"),
    ("b497f85713847cecc169d4d71c7629655d562dc0",
     "rawlsing_next/tests/test_postastra_pe_fixture.py",
     "c9674d5fe9d01621eda0fdb4a999391eba422d92",
     "rawlsing_next/tests/test_postastra_pe_fixture.py"),
    ("b497f85713847cecc169d4d71c7629655d562dc0",
     "rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py",
     "92f59875583bf513c6fdbcd3ad7fe2b49e45e212",
     "rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "rawlsing_next/tests/n10e_empirical_slice_fresh_process_runner.py",
     "19e8d47084ebb5763037a83c4afbc2036f30c49a",
     "rawlsing_next/tests/n10e_empirical_slice_fresh_process_runner.py"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "rawlsing_next/tests/c1_at08_at13_fresh_process_runner.py",
     "39ddca69e171143e2a539d5494bc2c94de6f9762",
     "rawlsing_next/tests/c1_at08_at13_fresh_process_runner.py"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "rawlsing_next/tests/mx01r2_fresh_process_runner.py",
     "d843132330e2a92f7ea7a6aa31e39566559963d0",
     "rawlsing_next/tests/mx01r2_fresh_process_runner.py"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "rawlsing_next/tests/c1_at18_at19_fresh_process_runner.py",
     "99a65b681c9a570541a44beae33537821f0739f3",
     "rawlsing_next/tests/c1_at18_at19_fresh_process_runner.py"),
    ("4fb21a8108d29f4c820326204bfcfee41500788c",
     "rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py",
     "d2fe653dadf94893b0fdfd268f36683f8dfed9af",
     "rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py"),
    # fixture data closure for staged N10E/C1/PE tests (ROOT=parents[2] => staging/ns)
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/02_VALUE_RELATION_ORACLE.json",
     "c6acafae820c065215fdbe7a703480a8b19fbc57",
     "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/02_VALUE_RELATION_ORACLE.json"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/03_SYNTHETIC_AUTHORITY_FREEZE.json",
     "333989fa7b57c221d6aa5ebfc25d9d76e0acad32",
     "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/03_SYNTHETIC_AUTHORITY_FREEZE.json"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/04_SLICE_PROJECTION.json",
     "8e5bd3d23db1e39aebee0a55d49934a0d400dd48",
     "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/04_SLICE_PROJECTION.json"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json",
     "5d1583dc31c837282ea40448285109a31bb1db41",
     "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/04_CURRENT_AT07_IDENTITY_SPINE.json",
     "462bb282ddc2cc9667f1890f2d65f2fae9a3a72c",
     "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/04_CURRENT_AT07_IDENTITY_SPINE.json"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/FORWARD_HISTORICAL_CANONICAL.json",
     "2d725dc592291ac7e8da4e4b0fb90f96dbeacec4",
     "WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/FORWARD_HISTORICAL_CANONICAL.json"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/FORWARD_SUCCESSOR_CANONICAL.json",
     "8143c96ed8ebdf3b87632d193a30e9924cbd1ced",
     "WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/FORWARD_SUCCESSOR_CANONICAL.json"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/REVERSE_HISTORICAL_CANONICAL.json",
     "634d4dd6c6c90e6c02220b17071795e9b7bdbd3e",
     "WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/REVERSE_HISTORICAL_CANONICAL.json"),
    ("7f29aec36d24f16da52d84f17c00f08db3a55434",
     "WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/REVERSE_SUCCESSOR_CANONICAL.json",
     "712455f3b84a0685d0876dc5218421edf7dae724",
     "WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/REVERSE_SUCCESSOR_CANONICAL.json"),
    # frozen SC0 oracle preimages (independent pinned specs)
    ("241d35fa8a13ea03c68fbe55554ce81c210b745f",
     "WORKER_RETURNS/SOROK-R3-POSTASTRA-SC0-WORLD-PORT-CONTRACT-R1/02_K9_PROVIDER_SWAP_ORACLES.json",
     "9ccb66f9b08a4aa8b96582295bb2966d250fd72d",
     "oracles/02_K9_PROVIDER_SWAP_ORACLES.json"),
    ("241d35fa8a13ea03c68fbe55554ce81c210b745f",
     "WORKER_RETURNS/SOROK-R3-POSTASTRA-SC0-WORLD-PORT-CONTRACT-R1/03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json",
     "e78b3ee91da1fb18deaf8d8f226800ad855adbae",
     "oracles/03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json"),
    ("241d35fa8a13ea03c68fbe55554ce81c210b745f",
     "WORKER_RETURNS/SOROK-R3-POSTASTRA-SC0-WORLD-PORT-CONTRACT-R1/01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json",
     "610ac870fde6cfe63796592b3c6b1e1bf1e37150",
     "oracles/01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json"),
]


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + f"{len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    rows = []
    all_ok = True
    for rev, repo_path, expected, staged_rel in PINS:
        raw = subprocess.check_output(["git", "-C", str(REPO), "show", f"{rev}:{repo_path}"])
        observed = git_blob_sha1(raw)
        out = (RETURN / staged_rel) if staged_rel.startswith("oracles/") else (NS / staged_rel)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(raw)
        ok = observed == expected
        all_ok = all_ok and ok
        rows.append({
            "source_rev": rev,
            "repo_path": repo_path,
            "expected_blob_sha1": expected,
            "observed_blob_sha1": observed,
            "staged_path": staged_rel,
            "bytes": len(raw),
            "match": ok,
        })
        print(f"{'OK ' if ok else 'BAD'} {observed} {staged_rel} ({len(raw)} bytes)")
    manifest = {
        "schema": "SOROK_HQ298_SC0_STAGING_MANIFEST@1",
        "git_blob_preimage": "sha1('blob <len>\\0' + bytes) — actual NUL separator after length",
        "entries": rows,
        "all_match": all_ok,
    }
    (RETURN / "staging" / "staging_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
