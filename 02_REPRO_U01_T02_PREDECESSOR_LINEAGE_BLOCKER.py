#!/usr/bin/env python3
"""Reproduce U01's bounded T02 predecessor-lineage blocker.

Run against an actual checkout of producer tip 161b207f1efb6f8291c1dae3258bb710438f6b54:

    python 02_REPRO_U01_T02_PREDECESSOR_LINEAGE_BLOCKER.py --producer-root /path/to/checkout

Exit 0 means the commissioned blocker is reproduced: a generation-1 successor
with a forged predecessor content hash is accepted by the lineage gate when the
prior row is not co-present in the batch. A repaired adapter should make this
script fail at the final assertion and should be freshly independently qualified.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

PRODUCER_SHA = "161b207f1efb6f8291c1dae3258bb710438f6b54"
IMPLEMENTATION_PATH = "rawlsing_next/sdtf_r4_generic_batch_adapter.py"
IMPLEMENTATION_BLOB = "c1a495c7a23d4ebee086fd5410d9627f4aefb695"
PRODUCER_TEST_PATH = "rawlsing_next/tests/test_sdtf_r4_generic_batch_adapter.py"
PRODUCER_TEST_BLOB = "7b4190601757fa69352d1a990c27242c67226cae"
TEST_IDENTITY = "u01_predecessor_hash_forgery_is_accepted_when_prior_snapshot_absent"


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True, stderr=subprocess.STDOUT
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer-root", required=True, type=Path)
    args = parser.parse_args()
    root = args.producer_root.resolve()

    head = _git(root, "rev-parse", "HEAD")
    if head != PRODUCER_SHA:
        raise SystemExit(f"wrong producer checkout: {head}")
    if _git(root, "rev-parse", f"HEAD:{IMPLEMENTATION_PATH}") != IMPLEMENTATION_BLOB:
        raise SystemExit("implementation blob mismatch")
    if _git(root, "rev-parse", f"HEAD:{PRODUCER_TEST_PATH}") != PRODUCER_TEST_BLOB:
        raise SystemExit("producer test blob mismatch")

    sys.path.insert(0, str(root))
    from rawlsing_next.pre553_empirical_objects import ExactRef
    from rawlsing_next.sdtf_r4_generic_batch_adapter import (
        CANDIDATE_ROW_KIND,
        PREDECESSOR_CHAIN_INVALID,
        adapt_generic_r4_batch,
    )
    from rawlsing_next.tests import test_sdtf_r4_generic_batch_adapter as fx

    actual_g0 = fx._row("lineage-forged", generation=0)
    actual_g0_ref = ExactRef(**actual_g0["ref"])
    forged_hash = fx._h("u01-forged-predecessor-hash")
    if forged_hash == actual_g0_ref.content_hash:
        raise SystemExit("test construction collision")

    forged_predecessor = ExactRef(
        CANDIDATE_ROW_KIND,
        actual_g0_ref.object_id,
        forged_hash,
    ).as_dict()
    successor = fx._row(
        "lineage-forged",
        generation=1,
        predecessor=forged_predecessor,
    )

    # Deliberately omit g0 from the batch. The frozen S03 law still requires
    # predecessor_row_ref to be the exact prior row ref, not merely the right
    # kind/object_id with an arbitrary hash.
    result = adapt_generic_r4_batch(
        fx._batch([successor], tag="u01-forged-predecessor")
    )
    receipt = result.candidate_receipts[0]

    assert PREDECESSOR_CHAIN_INVALID not in receipt.integrity_failures, (
        "candidate no longer reproduces U01 blocker; fresh qualification needed"
    )
    print(
        "BLOCKER_REPRODUCED",
        TEST_IDENTITY,
        "successor=fixture:lineage-forged:g1",
        f"actual_g0_hash={actual_g0_ref.content_hash}",
        f"accepted_forged_predecessor_hash={forged_hash}",
        f"integrity_failures={receipt.integrity_failures}",
        f"runtime_projection_state={receipt.runtime_projection_state}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
