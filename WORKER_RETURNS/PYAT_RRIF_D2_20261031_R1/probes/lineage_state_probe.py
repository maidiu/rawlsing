"""Read-only static state probe for the six RRIF-D2 lineages.

No branch source is imported or executed. This script reads the checked-out
PRE-MAIN tree and prints exact file/blob presence for the paths named by the
RRIF-C unresolved rows. It is evidence for SOURCE_CURRENT_COMPARISONS.md.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PRE = "8e44ca9c751049d65e6def47600b5c073ee04b29"

LINEAGES = {
    "LIN-B5_OWNER_TRUST": [
        "rawlsing_next/pre553_authenticated_b5_ingress_candidate.py",
        "rawlsing_next/pre553_b5_issuer_verification_candidate.py",
        "rawlsing_next/pre553_b5_mandatory_boundary_candidate.py",
        "rawlsing_next/pre553_b5_owner_held_verifier_candidate.py",
        "rawlsing_next/pre553_b5_separate_principal_verifier_candidate.py",
        "rawlsing_next/pre553_n04_b5_checkpoint_interface_correction.py",
        "rawlsing_next/repro/b5_mandatory_patch.py",
        "rawlsing_next/repro/c02f_bypass_court.py",
        "rawlsing_next/repro/c02g_issuer_court.py",
        "rawlsing_next/repro/c02h_separate_principal_court.py",
        "rawlsing_next/repro/c02j_mandatory_overlay.py",
        "rawlsing_next/repro/c02j_owner_court.py",
        "rawlsing_next/repro/n04_corrected_overlay.py",
    ],
    "LIN-EE14_G1_OWNER_INGRESS": [
        "rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py",
    ],
    "LIN-R56_SOURCE_NATIVE_ADAPTER": [
        "rawlsing_next/pre553_source_native_preimage_adapter.py",
    ],
    "LIN-R157_SOURCE_CONFIGURATION": [
        "rawlsing_next/pre553_source_read_admission.py",
        "rawlsing_next/source_configuration/__init__.py",
        "rawlsing_next/source_configuration/cli.py",
        "rawlsing_next/source_configuration/data/SRC27/lits_full_bindings.py",
        "rawlsing_next/source_configuration/data/SRC27/lits_lane_build.py",
        "rawlsing_next/source_configuration/errors.py",
        "rawlsing_next/source_configuration/evidence.py",
        "rawlsing_next/source_configuration/factory.py",
        "rawlsing_next/source_configuration/fixture.py",
        "rawlsing_next/source_configuration/library.py",
        "rawlsing_next/source_configuration/reader.py",
        "rawlsing_next/source_configuration/schema.py",
        "rawlsing_next/source_configuration/tools/__init__.py",
        "rawlsing_next/source_configuration/tools/build_evidence.py",
        "rawlsing_next/source_configuration/tools/build_p0_example.py",
        "rawlsing_next/source_configuration/tools/build_p3_example.py",
        "rawlsing_next/source_configuration/tools/publish_p0.py",
        "rawlsing_next/source_configuration/tools/publish_p3.py",
        "rawlsing_next/source_configuration/validator.py",
    ],
    "LIN-SRC04_EMPIRICAL_QUERY": [
        "rawlsing_next/_pre553_query_common.py",
        "rawlsing_next/_pre553_query_eval.py",
        "rawlsing_next/_pre553_query_predicate.py",
        "rawlsing_next/pre553_empirical_query.py",
        "rawlsing_next/pre553_observed_response.py",
    ],
    "LIN-S00D_VALUE_QUARANTINE": [
        "rawlsing_next/s00d_producer_binding_quarantine.py",
    ],
}


def git_blob(path: str) -> str | None:
    p = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", f"{PRE}:{path}"],
        capture_output=True, text=True,
    )
    return p.stdout.strip() if p.returncode == 0 else None


def disk_sha(path: str) -> str | None:
    p = REPO / path
    if not p.is_file():
        return None
    return hashlib.sha256(p.read_bytes()).hexdigest()


out = {"premain": PRE, "lineages": {}}
for lineage, paths in LINEAGES.items():
    rows = []
    for path in paths:
        rows.append({
            "path": path,
            "git_blob_at_premain": git_blob(path),
            "disk_present": (REPO / path).is_file(),
            "disk_sha256": disk_sha(path),
        })
    out["lineages"][lineage] = rows
print(json.dumps(out, indent=1, sort_keys=True))
