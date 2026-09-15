#!/usr/bin/env python3
"""Deterministically validate the N02 positively proved 2,104-row subset.

This validator does not create routing authority. It verifies byte identity of the
accepted Authority-45 source carriers copied into this N02 return and checks only
the lossless status translation frozen by 01_POSITIVELY_PROVED_SUBSET_MANIFEST_R1.json.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

B03 = [
    ("proved_subset/B03/NATIVE_CURRENT_REBIND_01.csv", "e407539b7f53d48d61ac45d58b779516477e8762"),
    ("proved_subset/B03/NATIVE_CURRENT_REBIND_02.csv", "ba091ce6131ec2efc2717cce17ddd8443b1b8e3b"),
    ("proved_subset/B03/NATIVE_CURRENT_REBIND_03.csv", "540da0ead40469f21fba4bd841d7a8f70eb56fb5"),
    ("proved_subset/B03/NATIVE_CURRENT_REBIND_04.csv", "1ccd0ac1dfa3c6809b89ba1b5ca721ef49de38c2"),
    ("proved_subset/B03/NATIVE_CURRENT_REBIND_05.csv", "41e5b7f247086c8a63e0b2e557e36ef78b50fe1d"),
    ("proved_subset/B03/NATIVE_CURRENT_REBIND_06.csv", "b8bd430bdce006aafc5e01a2353bf46c19726bfc"),
]
B04 = (
    "proved_subset/B04/06_AUTHORITY44_CURRENT_18276_IMPLEMENTATION_REBINDINGS.csv",
    "157237719203917e63e031295e30a466183c5948",
)
B05 = [
    ("proved_subset/B05/01_AUTH44_REBOUND_EVIDENCE_01.jsonl", "992ab4fa7d69b3deb69541b99c5ac26d600e9ee2"),
    ("proved_subset/B05/01_AUTH44_REBOUND_EVIDENCE_02.jsonl", "2b0a8be915a073a0fa2d51c10423320c8c6185d7"),
    ("proved_subset/B05/01_AUTH44_REBOUND_EVIDENCE_03.jsonl", "9804f0b8a326340a5d422fff8b3b2b4273e9f8a6"),
    ("proved_subset/B05/01_AUTH44_REBOUND_EVIDENCE_04.jsonl", "e53d6c726865d3d16fa9ddcddd7d17ffe38f7206"),
    ("proved_subset/B05/01_AUTH44_REBOUND_EVIDENCE_05.jsonl", "3817ad78b9013d223c2761bbd3116a8badaa561e"),
    ("proved_subset/B05/01_AUTH44_REBOUND_EVIDENCE_06.jsonl", "90c654b868e163f1520e812f7af7e0998cd06081"),
    ("proved_subset/B05/01_AUTH44_REBOUND_EVIDENCE_07.jsonl", "ce914e6be1ac800ec34ad8233f42eef0b06c41e0"),
]

U = "UNCONDITIONAL_OR_GENERAL_RESPONDENT_UNIVERSE__CURRENT_AUTHORITY"
P = "POSITIVE_EXECUTABLE_ROUTING_OR_APPLICABILITY_PREDICATE__CURRENT_AUTHORITY"
N = "GOVERNED_KNOWN_ABSENCE_OR_NONAPPLICABILITY__CURRENT_AUTHORITY"
EXPECTED = {U: 660, P: 1427, N: 17}


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def checked_bytes(rel: str, expected_blob: str) -> bytes:
    data = (ROOT / rel).read_bytes()
    actual = git_blob_sha(data)
    if actual != expected_blob:
        raise AssertionError(f"blob identity drift for {rel}: {actual} != {expected_blob}")
    return data


def main() -> None:
    statuses: Counter[str] = Counter()
    ids: set[str] = set()
    group_counts: Counter[str] = Counter()

    for rel, blob in B03:
        rows = csv.DictReader(io.StringIO(checked_bytes(rel, blob).decode("utf-8")))
        for row in rows:
            qid = row["qid"]
            if qid in ids:
                raise AssertionError(f"duplicate current implementation id: {qid}")
            ids.add(qid)
            code = row["s"]
            if code == "G":
                statuses[U] += 1
            elif code in {"R", "E", "M", "B", "S", "C"}:
                statuses[P] += 1
            else:
                raise AssertionError(f"unrecognized B03 authority code: {code}")
            group_counts["B03"] += 1

    rel, blob = B04
    rows = csv.DictReader(io.StringIO(checked_bytes(rel, blob).decode("utf-8")))
    for row in rows:
        qid = row["current_question_implementation_id"]
        if qid in ids:
            raise AssertionError(f"duplicate current implementation id: {qid}")
        ids.add(qid)
        evidence = row["salvaged_evidence_type"]
        if evidence == "SOURCE_NATIVE_EXECUTABLE_ROUTING_EVIDENCE":
            statuses[P] += 1
        elif evidence == "SOURCE_NATIVE_COUNTRY_NONAPPLICABILITY_EVIDENCE":
            statuses[N] += 1
        else:
            raise AssertionError(f"unrecognized B04 evidence type: {evidence}")
        group_counts["B04"] += 1

    for rel, blob in B05:
        text = checked_bytes(rel, blob).decode("utf-8")
        for line in text.splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            qid = row["question_implementation_id"]
            if qid in ids:
                raise AssertionError(f"duplicate current implementation id: {qid}")
            ids.add(qid)
            evidence = row["evidence_class"]
            if evidence == "EXECUTABLE_ROUTING_PREDICATE_EVIDENCE":
                statuses[P] += 1
            elif "NONAPPLIC" in evidence.upper():
                statuses[N] += 1
            else:
                raise AssertionError(f"unrecognized B05 evidence class: {evidence}")
            group_counts["B05"] += 1

    if dict(statuses) != EXPECTED:
        raise AssertionError(f"status totals drift: {dict(statuses)} != {EXPECTED}")
    if dict(group_counts) != {"B03": 2032, "B04": 11, "B05": 61}:
        raise AssertionError(f"authority carrier totals drift: {dict(group_counts)}")
    if len(ids) != 2104:
        raise AssertionError(f"unique current implementation count drift: {len(ids)}")

    print(json.dumps({
        "status": "PASS__POSITIVELY_PROVED_SUBSET_ONLY",
        "unique_current_implementation_ids": len(ids),
        "authority_carrier_counts": dict(group_counts),
        "status_counts": dict(statuses),
        "full_18276_reconciliation": "NOT_CLAIMED__N02_BLOCKER_REMAINS"
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
