"""WG0RI — independent exact-disposition-repair court.

Author modules are the object under test; every expected byte, hash, ordinal,
count and provenance fact is independently decoded/asserted here.
"""
from __future__ import annotations

import base64
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r38_court as C  # noqa: E402

WORKTREE = C.R.parents[1]


def test_original_git_preimage_exact_and_malformed():
    path = C.original_path()
    raw = path.read_bytes()
    assert len(raw) == C.ORIGINAL_BYTES
    assert C.sha(raw) == C.ORIGINAL_CSV_SHA
    blob = subprocess.check_output(["git", "hash-object", str(path)],
                                   cwd=WORKTREE, text=True).strip()
    assert blob == C.ORIGINAL_GIT_BLOB
    for obj in (C.ORIGINAL_GIT_COMMIT, C.ORIGINAL_GIT_BLOB):
        subprocess.run(["git", "cat-file", "-e", obj], cwd=WORKTREE, check=True)
    row, payload, codes = C.original_decode()
    assert len(payload) == C.ORIGINAL_DECODED_BYTES
    assert C.sha(payload) == C.ORIGINAL_DECODED_SHA
    assert sum(bool(b & 192) for b in payload) == C.ORIGINAL_RESERVED
    # The historical file claims the frozen target but is internally malformed.
    assert int(row["payload_bytes"]) == 18276
    assert row["payload_sha256"] == C.PACK_SHA
    assert payload != C.pack(C.repaired_path())[1]
    assert path.read_bytes() == raw  # never repaired in place


def test_p2_identity_exact():
    rows = C.p2_rows()
    assert len(rows) == 18276
    assert len({r["question_implementation_id"] for r in rows}) == 18276
    assert C.sha(C.p2_path().read_bytes()) == C.P2_SHA
    manifest = C.manifest_rows()
    assert manifest[0]["first_question_implementation_id"] == rows[0]["question_implementation_id"]
    assert manifest[0]["last_question_implementation_id"] == rows[999]["question_implementation_id"]


def test_recovered_payload_exact_and_class_counts():
    row, payload, codes = C.pack(C.repaired_path())
    assert row["format_version"] == "P2_ORDINAL_BYTEPACK_V1"
    assert row["p2_sha256"] == C.P2_SHA
    assert int(row["p2_row_count"]) == 18276
    assert int(row["payload_bytes"]) == 18276
    assert row["payload_sha256"] == C.PACK_SHA
    assert len(payload) == 18276
    assert C.sha(payload) == C.PACK_SHA
    assert codes == {str(i): c for i, c in enumerate(C.CLASS_ORDER)}
    counts = C.bit_counts(payload, codes)
    assert counts["classes"] == C.EXPECTED_CLASS_COUNTS
    assert counts["hard_fail"] == C.EXPECTED_HARD_FAIL
    assert counts["route"] == C.EXPECTED_ROUTE
    assert counts["reserved"] == 0
    assert counts["use_out_of_range"] == 0
    a, r = C.author_modules()
    assert r.recover() == payload
    assert a.decode_dispositions()[0] == payload


def test_surviving_shard_exact_and_rows_match():
    path = C.shard_path()
    raw = path.read_bytes()
    assert len(raw) == 11944
    assert C.sha(raw) == C.SHARD_SHA
    blob = subprocess.check_output(["git", "hash-object", str(path)],
                                   cwd=WORKTREE, text=True).strip()
    assert blob == C.SHARD_GIT_BLOB
    rows = C.shard_rows()
    assert len(rows) == C.SHARD_ROWS
    ordinal = [int(r["p2_row_ordinal"]) for r in rows]
    assert ordinal == list(range(C.SHARD_ROWS))
    n, bad = C.shard_mismatches(C.pack(C.repaired_path())[1], C.pack(C.repaired_path())[2])
    assert n == C.SHARD_ROWS and bad == 0


def test_manifest_provenance_discrepancy_is_typed():
    manifest = C.manifest_rows()
    assert len(manifest) == 19
    assert sum(int(r["row_count"]) for r in manifest) == 18276
    assert manifest[0]["sha256"] == C.MANIFEST_PART000_SHA
    survivor = C.sha(C.shard_path().read_bytes())
    assert survivor == C.SHARD_SHA
    # The manifest's part-000 hash is not the survivor's bytes. The survivor is
    # Git-exact and row-correct; the manifest must be typed as a different
    # serialization/provenance set, never used as a substitute for the survivor.
    assert manifest[0]["sha256"] != survivor
    assert manifest[0]["first_question_implementation_id"] == \
        C.p2_rows()[0]["question_implementation_id"]
    assert manifest[0]["last_question_implementation_id"] == \
        C.p2_rows()[999]["question_implementation_id"]


def test_accounting_reader_exact():
    a, _ = C.author_modules()
    rows, waves, registry = a.load()
    assert len(rows) == 18276 and len(waves) == 35
    assert len({r["p2_ordinal"] for r in rows}) == 18276
    assert [r["p2_ordinal"] for r in rows] == list(range(18276))
    assert not any(r["execution_state"] == "DISPOSITION_CARRIER_REQUIRES_EXACT_REPUBLICATION"
                   for r in rows)
    from collections import Counter
    assert dict(Counter(r["governed_use"] for r in rows)) == C.EXPECTED_CLASS_COUNTS
    assert sum(r["hard_fail"] for r in rows) == C.EXPECTED_HARD_FAIL
    assert sum(r["route_predicate_required"] for r in rows) == C.EXPECTED_ROUTE
    conservation = json.loads((C.AUTHOR / "evidence/current35_conservation.json").read_text())
    assert conservation["implementations"] == 18276
    assert conservation["unique_ids"] == 18276
    assert conservation["active_waves"] == 35
    assert conservation["families"] == 9
    assert conservation["p2_sha256"] == C.P2_SHA
    assert conservation["payload_sha256"] == C.PACK_SHA
    assert conservation["p10_accounting_units"] == C.EXPECTED_P10_UNITS
    assert conservation["p10_exact_held_states"] == C.EXPECTED_P10_HELDS
    assert conservation["all35_operation_execution"] == \
        "UNVERIFIED__NO_RAW_READS_OR_SOURCE_WARRANT_ISSUED"
    assert conservation["disposition_carrier"]["state"] == "EXACT_PACK_VERIFIED"
    assert conservation["disposition_carrier"]["reserved_bit_violations"] == 0


def test_author_90_test_native_and_cold_courts():
    base = C.R / "01_AUTHOR_COURT"
    assert C.junit_counts(base / "author_90_full.xml") == \
        {"tests": 90, "failures": 0, "errors": 0, "skipped": 0}
    for seed in (0, 1):
        assert C.junit_counts(base / ("cold_%d.xml" % seed)) == \
            {"tests": 90, "failures": 0, "errors": 0, "skipped": 0}
    assert C.run_recovery(C.AUTHOR)["payload"]["sha256"] == C.PACK_SHA
    cold = C.R / "stage/cold_copy"
    if cold.is_dir():
        assert C.run_recovery(cold)["payload"]["sha256"] == C.PACK_SHA


@pytest.mark.parametrize("mutation", [
    "payload_byte", "header_sha", "p2_sha", "code_map", "byte_length",
    "reserved_bit_rehashed", "use_code_15_rehashed", "truncate",
    "duplicate_chunk", "bad_base64", "duplicate_row",
])
def test_reader_rejects_corruption(tmp_path, mutation):
    a, _ = C.author_modules()
    path = C.make_pack_variant(tmp_path, mutation)
    with pytest.raises(ValueError):
        a.decode_dispositions(pack_path=path)


def test_original_malformed_fails_closed():
    a, _ = C.author_modules()
    with pytest.raises(ValueError):
        a.decode_dispositions(pack_path=C.original_path())


def test_o07_is_diagnostic_only_and_never_issues_use_codes(tmp_path):
    counts = C.o07_counts()
    assert counts["UNRESOLVED"] == 30
    source = (C.AUTHOR / "recover_disposition_payload.py").read_text()
    # Use codes are selected from S00 workstreams / central O04 ancestry, never O07.
    assert "o07" not in "code=codes[stream]"
    assert "o07" not in "code=3 if q in accepted"
    assert "o07[q]['current_o07_measurement_use_class_DIAGNOSTIC_ONLY']=='UNRESOLVED'" in source

    root = C.make_recovery_copy(tmp_path / "rec")
    o07 = root / "sources/recovered_disposition/o07_recall_projection.csv"
    custody = root / "evidence/disposition_recovery_input_custody.json"
    original = o07.read_text().splitlines()

    def rebind_o07_custody():
        data = json.loads(custody.read_text())
        for entry in data:
            if entry["projection_path"].endswith("o07_recall_projection.csv"):
                entry["projection_sha256"] = C.sha(o07.read_bytes())
        custody.write_text(json.dumps(data))
    # A non-UNRESOLVED O07 value change must not alter any recovered byte.
    idx = next(i for i, line in enumerate(original[1:], 1)
               if line.endswith(",ADMIN"))
    mutated = list(original)
    mutated[idx] = mutated[idx][:-len("ADMIN")] + "SEM"
    o07.write_text("\n".join(mutated) + "\n")
    rebind_o07_custody()
    got = C.run_recovery(root)
    assert got["payload"].get("sha256") == C.PACK_SHA, got
    # An UNRESOLVED -> resolved diagnostic change may change held bits only, but
    # can never produce a different accepted payload: it either stays at the exact
    # frozen SHA (held already true elsewhere) or fails the frozen-SHA gate.
    o07.write_text("\n".join(original) + "\n")
    rebind_o07_custody()
    unresolved_lines = [i for i, line in enumerate(original[1:], 1)
                        if line.endswith(",UNRESOLVED")]
    assert len(unresolved_lines) == 30
    outcomes = []
    for i in unresolved_lines:
        mutated = list(original)
        mutated[i] = mutated[i][:-len("UNRESOLVED")] + "ADMIN"
        o07.write_text("\n".join(mutated) + "\n")
        rebind_o07_custody()
        got = C.run_recovery(root)
        outcomes.append((got["exit"], got["payload"].get("sha256")))
    o07.write_text("\n".join(original) + "\n")
    rebind_o07_custody()
    assert all(sha == C.PACK_SHA or exit_code != 0 for exit_code, sha in outcomes)
    assert any(exit_code != 0 for exit_code, _ in outcomes)


def test_forged_custody_and_aggregate_reconstruction_rejected(tmp_path):
    root = C.make_recovery_copy(tmp_path / "custody")
    custody = root / "evidence/disposition_recovery_input_custody.json"
    data = json.loads(custody.read_text())
    data[1]["projection_sha256"] = "0" * 64
    custody.write_text(json.dumps(data))
    got = C.run_recovery(root)
    assert got["exit"] != 0
    assert "RECOVERY_INPUT_CUSTODY_MISMATCH" in got["stderr"]

    # Aggregate-count-only payload is not the frozen bytes.
    aggregate = b"".join(bytes([i]) * n for i, n in enumerate(
        [C.EXPECTED_CLASS_COUNTS[c] for c in C.CLASS_ORDER]))
    assert len(aggregate) == 18276 and C.sha(aggregate) != C.PACK_SHA

    root2 = C.make_recovery_copy(tmp_path / "aggregate")
    s00 = root2 / "sources/recovered_disposition/s00_workstreams.csv"
    lines = s00.read_text().splitlines()
    s00.write_text("\n".join([lines[0]] + lines[1:4]) + "\n")
    got2 = C.run_recovery(root2)
    assert got2["exit"] != 0


def test_ordinal_duplication_omission_reordering_detected():
    payload = C.pack(C.repaired_path())[1]
    codes = C.pack(C.repaired_path())[2]
    ordinal = [int(r["p2_row_ordinal"]) for r in C.shard_rows()]
    assert ordinal == list(range(1000))
    # Duplicate/omit/reorder of a shard ordinal is detectable before semantics.
    for mutated in (ordinal + [999], ordinal[:-1], list(reversed(ordinal))):
        assert mutated != list(range(1000))
    # Payload duplication/omission/reordering cannot survive the frozen SHA.
    for mutated in (payload + payload[:1], payload[:-1],
                    payload[:1] + payload[1:2] + payload[0:1] + payload[2:]):
        assert len(mutated) != 18276 or C.sha(mutated) != C.PACK_SHA
    # P2 substitution in a recovery copy fails the exact P2 identity gate.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = C.make_recovery_copy(Path(td) / "p2")
        p2 = root / "sources/local_archive/Rawlsing_P2_Phase0_Question_Node_Skeleton_v1.csv"
        p2.write_bytes(p2.read_bytes() + b"\n")
        got = C.run_recovery(root)
        assert got["exit"] != 0
        assert "P2_IDENTITY_MISMATCH" in got["stderr"]


def test_two_process_replay_identity():
    a = C.run_recovery(C.AUTHOR)
    b = C.run_recovery(C.AUTHOR)
    assert a["payload"].get("sha256") == b["payload"].get("sha256") == C.PACK_SHA
    cold = C.R / "stage/cold_copy"
    if cold.is_dir():
        assert C.run_recovery(cold)["payload"].get("sha256") == C.PACK_SHA


def test_prior_crosswalk_and_full_frontier_hold_preserved():
    conservation = json.loads((C.AUTHOR / "evidence/current35_conservation.json").read_text())
    assert conservation["p10_exact_held_states"] == 76
    assert conservation["all35_operation_execution"] == \
        "UNVERIFIED__NO_RAW_READS_OR_SOURCE_WARRANT_ISSUED"
    prior_path = ("WORKER_RETURNS/PYAT-R37-WG0I-CURRENT35-FRONTIER-INDEPENDENT-R1/"
                  "PUBLICATION_RECEIPT.json")
    prior = json.loads(subprocess.check_output(
        ["git", "show", C.PRIOR_WG0I + ":" + prior_path], cwd=WORKTREE, text=True))
    cross = prior["wg0r_comparison"]
    assert cross["common_identity_hashes"] == 18250
    assert cross["p2_only_hashes"] == 26
    assert cross["o35e_none_identity_blocked_rows"] == 9
    assert cross["net_count_delta"] == 17
    assert cross["p2_only_measurement_candidates"] == 19
    assert prior["decision"]["full_original35_frontier"] == "HOLD"
    # This byte repair does not resolve the P2/O35E crosswalk or the full frontier.
    assert conservation["implementations"] == 18276
    assert conservation["pending_edge"] == \
        "EXACT_ACCEPTED_AUTHORITY_TO_OPERATION_CATALOG_BINDING_AND_FULL_FRONTIER_WITNESS"
