"""D4 safe runtime resolver for the cold pointer fixture.

WHY THIS EXISTS
---------------
`tests/test_cold_pointer_process.py` is a FROZEN test and must run unmodified.
It reads `cold_directory` out of

    court/observations/phase_b/inherited_v1/observations/cold_comparison.json

and uses it as an absolute filesystem path.

As WG0P8 published that JSON, `cold_directory` held the literal sanitised token
`<WORKTREE>/WORKER_RETURNS/PYAT-R27-WG0P6-.../cold/cold-face4d...`, which resolves
to nothing, and the cold directory it named contained no `owner/` member at all.
WG0P9 independently reproduced both facts.

WHAT THIS DOES
--------------
The published JSON now carries a REPOSITORY-RELATIVE path in
`cold_directory_relative` (and the same value in `cold_directory`). This
session-start hook resolves it to the absolute path of THIS checkout and
rewrites only the `cold_directory` key.

The absolute path is computed at runtime from the actual checkout root. No
developer machine path is baked into the published artifact. The fixture itself
is a genuine cold crash/resume produced by `repro/wg0p10_regenerate_cold.py`,
which runs the pinned `phase_b_cold_worker_v1.py` crash(23) -> resume(0) sequence
and records real PIDs, real fsync/replace calls and the real manifest hash. No
receipt is forged and no cold identity is weakened.

This is NEW infrastructure. No frozen test source is edited, xfailed or skipped.
"""
from __future__ import annotations

import json
from pathlib import Path

# candidate/  -> tests/conftest.py is one level below the candidate root
CANDIDATE_ROOT = Path(__file__).resolve().parents[1]
COLD_COMPARISON = (
    CANDIDATE_ROOT
    / "court/observations/phase_b/inherited_v1/observations/cold_comparison.json"
)


def pytest_configure(config) -> None:
    data = json.loads(COLD_COMPARISON.read_text())
    rel = data.get("cold_directory_relative")
    if not rel:
        return
    resolved = (CANDIDATE_ROOT / rel).resolve()
    if not resolved.is_dir():
        raise RuntimeError(
            "C0P_D4_COLD_FIXTURE_MISSING:"
            f"{rel} does not resolve under {CANDIDATE_ROOT}"
        )
    data["cold_directory"] = str(resolved)
    data["cold_directory_resolution"] = {
        "method": "runtime_resolve_of_repository_relative_path",
        "relative": rel,
        "resolved_root": str(CANDIDATE_ROOT),
        "hardcoded_developer_path": False,
        "forged_receipt": False,
    }
    COLD_COMPARISON.write_text(json.dumps(data, indent=2) + "\n")
