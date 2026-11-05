#!/usr/bin/env python3
"""Canonical PROGRAMMA tree integrity (source conservation; NOT a semantic/scientific proof)."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PROG = "CROSS_HQ_CONTROL_ROOM/PROGRAMMA/"
PYAT = "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/"
SOROK = "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/"
errors = []

def check(condition, reason):
    if not condition:
        errors.append(reason)

def required(path):
    p = ROOT / path
    check(p.is_file(), "required canonical path absent: " + path)
    return p

def parse_rows(path, expected, identity=None):
    p = required(path)
    if not p.is_file():
        return []
    rows = []
    for line_number, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except (ValueError, TypeError) as exc:
            errors.append(f"{path}:{line_number} invalid JSONL: {exc}")
    check(len(rows) == expected, f"{path}: {len(rows)} rows, expected {expected}")
    if identity:
        ids = [x.get(identity) for x in rows]
        check(all(ids) and len(set(ids)) == len(ids),
              f"{path}: missing or duplicate {identity}")
    return rows

for name in (
    "README.md",
    PROG + "00_PROGRAMMA_RAWLSING.md",
    PROG + "SHARED_RULE_SOURCE_MANIFEST_R1.json",
    PROG + "02_CANONICAL_RECEIVING_AND_CODE_CAPITAL.md",
    PYAT + "00_PROGRAMMA_PYAT.md",
    PYAT + "05_HISTORICAL_FUNCTION_SUCCESSION_AND_WORK_SELECTION_LAW_R1.md",
    PYAT + "05_ROADMAP/README.md",
    SOROK + "00_PROGRAMMA_SOROK.md",
    SOROK + "READ_FIRST.md",
    SOROK + "06_WORKING_WHOLE_SOROK_ARCHITECTURAL_SPINE_R1.md",
    SOROK + "10_RECONCILIATION_QUEUE_SOURCE_GAPS_AND_CLOSEOUT_CHECK_R1.md",
):
    required(name)

parse_rows(PYAT + "05_ROADMAP/INDEX.jsonl", 782, "id")
parse_rows(PYAT + "05_ROADMAP/G1_ROW_DISPOSITIONS.jsonl", 892)
parse_rows(PYAT + "05_ROADMAP/COMPONENT_STATUS.jsonl", 62, "id")
parse_rows(PYAT + "05_ROADMAP/CURRENT_SEAM_STATES.jsonl", 82, "edge_id")
parse_rows(PYAT + "05_ROADMAP/FIELD_FORGE_R2_FUNCTION_ASSET_REGISTER_20261104_R1.jsonl", 26, "stable_id")
parse_rows(PYAT + "05_ROADMAP/FIELD_FORGE_R2_DEPENDENCY_COURT_20261104_R1.jsonl", 16, "stable_id")
parse_rows(PYAT + "05_ROADMAP/RECEIVING_SOURCE_TO_ACTOR_20261103_R1.jsonl", 18, "STABLE_ID")
parse_rows(SOROK + "16_PYAT_SOROK_SOURCE_TO_ACTOR_RECEIVING_20261103_R1.jsonl", 16, "STABLE_ID")
parse_rows(SOROK + "16_POST_FF_SEAM_AND_ACTOR_MECHANISM_RECEIVING_20261104_R1.jsonl", 13)

f = required(SOROK + "09_INHERITED_144_FUNCTIONS_TO_WORKING_SPINE_R1.json")
if f.is_file():
    try:
        records = json.loads(f.read_text(encoding="utf-8"))["records"]
        check(len(records) == 144, "Sorok inherited functions: expected 144")
        check(len({x.get("id") for x in records}) == 144, "Sorok function IDs missing/duplicate")
    except (ValueError, KeyError, TypeError) as exc:
        errors.append("Sorok inherited functions unparsable: " + str(exc))

seams = parse_rows(SOROK + "15_W7_VERSIONED_SEAMS_AND_GATE_JOIN_CANDIDATES_R1.jsonl", 39)
if seams:
    check(seams[0].get("record_type") == "MANIFEST" and seams[0].get("count") == 38,
          "Sorok 38-seam manifest missing/changed")
    children = seams[1:]
    check(all(x.get("record_type") == "VERSIONED_SEAM" for x in children),
          "Sorok seam rows wrong type")
    ids = [x.get("seam_id") for x in children]
    check(len(set(ids)) == 38 and all(ids), "Sorok 38 seam IDs missing/duplicate")

check(not (ROOT / SOROK / "LIVING_REFERENCE_CANDIDATE_R1").exists(),
      "unaccepted Sorok living-reference prototype must not be copied into canonical guide")
for label, rel in (
    ("shared", PROG + "00_PROGRAMMA_RAWLSING.md"),
    ("Pyat", PYAT + "00_PROGRAMMA_PYAT.md"),
    ("Sorok", SOROK + "00_PROGRAMMA_SOROK.md"),
):
    p = ROOT / rel
    if p.is_file():
        check("CURRENT PROTECTED STATUS" in p.read_text(encoding="utf-8")[:1600],
              label + " front door retains misleading historical candidate status")

if errors:
    for error in errors:
        print("FAIL", error, file=sys.stderr)
    sys.exit(1)
print("PASS canonical tree: Pyat 782/892/62/82, FF 26/16, cross 18/16, Sorok 144/38, no prototype")
print("SCOPE: static source identities and navigation only; no proof of correct science, native joins or live HQ updates")
