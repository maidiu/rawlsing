"""Fresh-process cold reader for the S2-G durable learned lifecycle artifact.

CLI:
    python test_pyat960_s2g_fresh_process.py <artifact_path> <expected_root> <s2f_closure_path> <expected_consumer_hash>

The child imports only the adapter and reopens the artifact/S2F closure.  It
never imports the synthetic native fixtures or receives the native in-memory
learned result.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import time

from rawlsing_next.pre553_durable_learned_lifecycle import (
    ExternalCurrentAttestation,
    open_learned_lifecycle,
)

SOURCE_EXTENSIONS = (".sav", ".dta", ".parquet", ".csv", ".rdata", ".rds")


def run(
    *,
    artifact_path: str,
    expected_root: str,
    s2f_closure_path: str,
    expected_consumer_hash: str,
    attestation_path: str | None = None,
    expected_attestation_root: str | None = None,
) -> dict:
    source_opens = []

    def _audit(event, args):
        if event == "open" and args:
            text = str(args[0]).lower()
            if text.endswith(SOURCE_EXTENSIONS):
                source_opens.append(str(args[0]))

    sys.addaudithook(_audit)
    started = time.monotonic()
    artifact = open_learned_lifecycle(
        artifact_path, expected_root=expected_root
    ).require_trusted()
    current_state = None
    if attestation_path is not None:
        document = json.loads(Path(attestation_path).read_text(encoding="utf-8"))
        attestation = ExternalCurrentAttestation(**document)
        current, consumed = artifact.consume_current(
            s2f_closure_path,
            attestation=attestation,
            expected_attestation_root=expected_attestation_root,
        )
        current_state = current.state
    else:
        consumed = artifact.consume(s2f_closure_path)
    elapsed = time.monotonic() - started
    return {
        "root_identity": artifact.root_identity,
        "artifact_identity": artifact.artifact_identity,
        "state": consumed.state,
        "reason_code": consumed.reason_code,
        "consumer_result_hash": consumed.consumer_result_hash,
        "composition_identity": consumed.composition_identity,
        "m1_disposition_ref": consumed.m1_disposition_ref.as_dict()
        if consumed.m1_disposition_ref is not None
        else None,
        "m2_release_ref": consumed.m2_release_ref.as_dict()
        if consumed.m2_release_ref is not None
        else None,
        "b5_selection_receipt_ref": consumed.b5_selection_receipt_ref.as_dict()
        if consumed.b5_selection_receipt_ref is not None
        else None,
        "source_opens": source_opens,
        "elapsed_seconds": elapsed,
        "current_state": current_state,
        "matches_expected": consumed.consumer_result_hash == expected_consumer_hash,
    }


def main(argv: list[str]) -> int:
    if len(argv) not in (5, 7):
        raise SystemExit(
            "usage: test_pyat960_s2g_fresh_process.py <artifact> <expected_root> <s2f_closure> <expected_consumer_hash> [attestation expected_attestation_root]"
        )
    observed = run(
        artifact_path=argv[1],
        expected_root=argv[2],
        s2f_closure_path=argv[3],
        expected_consumer_hash=argv[4],
        attestation_path=argv[5] if len(argv) == 7 else None,
        expected_attestation_root=argv[6] if len(argv) == 7 else None,
    )
    print(json.dumps(observed, sort_keys=True))
    if observed["source_opens"]:
        raise SystemExit("cold learned consumer opened a source file")
    if not observed["matches_expected"]:
        raise SystemExit("cold learned consumer identity differs from expected")
    return 0


def test_fresh_process_runner_import_has_no_side_effects():
    assert callable(run)
    assert callable(main)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
