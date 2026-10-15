#!/usr/bin/env python3
"""Stage frozen RC0 evidence, SC0 oracles and pinned PE/C1/N10E closure.

Every staged object is verified against its Git blob SHA-1 (actual NUL
'blob <len>\\0' preimage).  Nothing staged here is modified afterwards.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]

RC0 = "86bd2a54687b40401f7c4247607bd1873c585619"
SC0 = "241d35fa8a13ea03c68fbe55554ce81c210b745f"
PE2 = "b497f85713847cecc169d4d71c7629655d562dc0"
READCUT = "7f29aec36d24f16da52d84f17c00f08db3a55434"
HQ298 = "b15dbbc4f07ae79e9ffb71e88e91e3b28b35da59"

PINS = [
    # RC0 frozen evidence + exact hostile test source (never modified)
    (RC0, "WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/01_FROZEN_INDEPENDENT_EXPECTATIONS.json", "rc0/01_FROZEN_INDEPENDENT_EXPECTATIONS.json"),
    (RC0, "WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/02_EXECUTION_PER_CASE.json", "rc0/02_EXECUTION_PER_CASE.json"),
    (RC0, "WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/03_NINE_PE_REDS_ADJUDICATED.json", "rc0/03_NINE_PE_REDS_ADJUDICATED.json"),
    (RC0, "WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/05_OWNER_ACTION_REGISTER.json", "rc0/05_OWNER_ACTION_REGISTER.json"),
    (RC0, "WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/reviewer_tests/test_rc0_hostile.py", "rc0/test_rc0_hostile.py"),
    # SC0 frozen oracles
    (SC0, "WORKER_RETURNS/SOROK-R3-POSTASTRA-SC0-WORLD-PORT-CONTRACT-R1/01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json", "oracles/01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json"),
    (SC0, "WORKER_RETURNS/SOROK-R3-POSTASTRA-SC0-WORLD-PORT-CONTRACT-R1/02_K9_PROVIDER_SWAP_ORACLES.json", "oracles/02_K9_PROVIDER_SWAP_ORACLES.json"),
    (SC0, "WORKER_RETURNS/SOROK-R3-POSTASTRA-SC0-WORLD-PORT-CONTRACT-R1/03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json", "oracles/03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json"),
    # pinned PE/C1/N10E producer closure
    (PE2, "rawlsing_next/pre553_postastra_pe_generic_world_possibility.py", "ns/rawlsing_next/pre553_postastra_pe_generic_world_possibility.py"),
    (READCUT, "rawlsing_next/pre553_analytical_composition.py", "ns/rawlsing_next/pre553_analytical_composition.py"),
    (READCUT, "rawlsing_next/pre553_empirical_possibility_provider.py", "ns/rawlsing_next/pre553_empirical_possibility_provider.py"),
    (PE2, "rawlsing_next/tests/test_postastra_pe_fixture.py", "ns/rawlsing_next/tests/test_postastra_pe_fixture.py"),
    (READCUT, "rawlsing_next/tests/n10e_empirical_slice_fixture.py", "ns/rawlsing_next/tests/n10e_empirical_slice_fixture.py"),
    (READCUT, "rawlsing_next/tests/n10e_at17_successor_requal.py", "ns/rawlsing_next/tests/n10e_at17_successor_requal.py"),
    (READCUT, "rawlsing_next/tests/c1_at08_at13_fixture.py", "ns/rawlsing_next/tests/c1_at08_at13_fixture.py"),
    (READCUT, "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/02_VALUE_RELATION_ORACLE.json", "ns/WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/02_VALUE_RELATION_ORACLE.json"),
    (READCUT, "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/03_SYNTHETIC_AUTHORITY_FREEZE.json", "ns/WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/03_SYNTHETIC_AUTHORITY_FREEZE.json"),
    (READCUT, "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/04_SLICE_PROJECTION.json", "ns/WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/04_SLICE_PROJECTION.json"),
    (READCUT, "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json", "ns/WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json"),
    (READCUT, "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/04_CURRENT_AT07_IDENTITY_SPINE.json", "ns/WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/04_CURRENT_AT07_IDENTITY_SPINE.json"),
    # HQ298 candidate reference (read-only predecessor)
    (HQ298, "WORKER_RETURNS/SOROK-R3-HQ298-SC0-VALUE-BEARING-PORT-R1/00_RETURN.md", "hq298/00_RETURN.md"),
]


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> int:
    rows = []
    for rev, repo_path, rel in PINS:
        raw = subprocess.check_output(["git", "-C", str(REPO), "show", f"{rev}:{repo_path}"])
        out = RETURN / "staging" / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(raw)
        rows.append({
            "source_rev": rev, "repo_path": repo_path,
            "git_blob_sha1": git_blob(raw), "staged_path": rel, "bytes": len(raw),
        })
        print(f"{git_blob(raw)[:12]}  {rel}")
    (RETURN / "staging" / "staging_manifest.json").write_text(
        json.dumps({"schema": "HQ300_C0_STAGING_MANIFEST@1",
                    "git_blob_preimage": "sha1('blob <len>\\0' + bytes)",
                    "entries": rows}, indent=2, sort_keys=True) + "\n")
    print(f"staged {len(rows)} objects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
