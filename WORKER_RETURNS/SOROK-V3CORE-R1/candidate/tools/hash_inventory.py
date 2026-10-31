#!/usr/bin/env python3
"""Generate the rollback/provenance inventory for SOROK V3CORE-R1."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

CANDIDATE = Path(__file__).resolve().parent.parent
RETURN = CANDIDATE.parent
REPO = next(parent for parent in CANDIDATE.parents if (parent / ".git").exists())

BASE = "750548ddbb9b4392a16ce93097b856f349e16182"
INPUTS = {
    "RCF_A": "e66dc53a5d7eeb2b6b3259000eb04b8e79e1f6f7",
    "R5": "aebb2452b277bfc91fc78dec8d6001f8a844cc8c",
    "O1": "501ea1f5bf07468b2c0437f452a81f3515cfdb6f",
    "I1": "7d44e30064f8e873e1a3ff9cb05fe75456756b88",
}
ARCHIVE = Path("/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging.zip")
ARCHIVE_EXPECTED = "953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086"
ARCHIVE_ROOT = ARCHIVE.parent / "Rawlsing_code_bundle_staging"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root: Path, *, skip: set[Path] | None = None) -> dict[str, str]:
    skip = skip or set()
    rows: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path in skip:
            continue
        relative = str(path.relative_to(CANDIDATE))
        rows[relative] = sha256(path)
    return rows


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True).strip()


def main() -> int:
    key_sources = [
        "vendor/v3/core/state.py",
        "vendor/v3/core/derived.py",
        "vendor/v3/core/invariants.py",
        "vendor/v3/core/config_loader.py",
        "vendor/v3/core/year_record.py",
        "vendor/v3/core/generation_integrity.py",
        "vendor/v3/engine/yearly_step.py",
        "vendor/v3/engine/step_runner.py",
        "vendor/v3/psyche/flow.py",
        "vendor/v3/render/phenomenology.py",
        "vendor/v3/v3config.yaml",
        "vendor/v3/v3_yearly_step_order.yaml",
        "vendor/v3/psyche/channels.py",
        "vendor/v3/io/parent_baseline_from_behavior.py",
        "vendor/v3/engine/expectation_baseline.py",
        "vendor/v3/engine/llm_contract.py",
        "vendor/v3/engine/run_llm_band.py",
        "vendor/v3/engine/effects/metabolization_effects.py",
        "vendor/v2/parent_type_inference.py",
        "vendor/i1/bp2p4/i1_product.py",
        "vendor/i1/bp2p4/product.py",
        "vendor/i1/vendor/bp4/bp4/product.py",
        "vendor/i1/vendor/bp4/bp4/store.py",
    ]
    payload = {
        "schema": "SOROK_V3CORE_R1_ROLLBACK_AND_PROVENANCE@1",
        "repository": "maidiu/rawlsing",
        "branch": "agent/sorok-v3core-r1-sourcefree-activity-time-adapter-20261030",
        "base_commit": BASE,
        "base_subject": git("show", "-s", "--format=%s", BASE),
        "inputs": {
            name: {
                "commit": commit,
                "subject": git("show", "-s", "--format=%s", commit),
            }
            for name, commit in INPUTS.items()
        },
        "archive": {
            "path": str(ARCHIVE),
            "observed_sha256": sha256(ARCHIVE) if ARCHIVE.exists() else "",
            "expected_td_r05_sha256": ARCHIVE_EXPECTED,
            "container_status": "MISMATCH_PRESERVED",
        },
        "historical_source_files": {
            path: {"sha256": sha256(CANDIDATE / path)} for path in key_sources if (CANDIDATE / path).exists()
        },
        "reference_sources_outside_candidate": {
            str(path.relative_to(ARCHIVE_ROOT)): {
                "sha256": sha256(path),
                "note": note,
            }
            for path, note in {
                ARCHIVE_ROOT / "server" / "generation" / "simulation.py": "runtime YearRecord dict fields",
                ARCHIVE_ROOT / "server" / "generation" / "store.py": "clean_ready/degraded_ready/blocked readiness",
                ARCHIVE_ROOT / "server" / "session_state.py": "_generation_state_is_ready",
            }.items()
            if path.exists()
        },
        "adapter_source_files": inventory(CANDIDATE / "v3core_adapter"),
        "candidate_test_files": inventory(CANDIDATE / "tests"),
        "candidate_tool_files": inventory(CANDIDATE / "tools"),
        "evidence_files": inventory(
            CANDIDATE / "evidence",
            skip={CANDIDATE / "evidence" / "source_hash_manifest.json"},
        ),
        "rollback": {
            "pre_main_base": BASE,
            "candidate_path": "WORKER_RETURNS/SOROK-V3CORE-R1/candidate",
            "return_path": "WORKER_RETURNS/SOROK-V3CORE-R1",
            "remove_worktree_command": (
                "git -C /Users/matthewsmith/Desktop/Rawlsing worktree remove "
                "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/v3core-return --force"
            ),
            "delete_branch_command": (
                "git -C /Users/matthewsmith/Desktop/Rawlsing branch -D "
                "agent/sorok-v3core-r1-sourcefree-activity-time-adapter-20261030"
            ),
            "restore_source_rule": (
                "Every vendored historical file is identified by SHA-256 above; restore by checking out "
                "the pinned input commit and re-reading the exact path. The adapter never edits vendor files."
            ),
        },
        "authority": {
            "science_issued": False,
            "native_person_claimed": False,
            "canonical_c9_claimed": False,
            "rival_store_created": False,
            "self_reviewed": False,
        },
    }
    output = RETURN / "04_ROLLBACK_SOURCE_HASHES_AND_PROVENANCE.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (CANDIDATE / "evidence" / "source_hash_manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
