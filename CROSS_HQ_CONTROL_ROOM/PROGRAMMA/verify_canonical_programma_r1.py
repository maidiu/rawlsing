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

for rel, snippets in (
    (SOROK + "06_WORKING_WHOLE_SOROK_ARCHITECTURAL_SPINE_R1.md",
     ("## Post-W8 source-qualified original-product proof", "## B occurrence", "## PSR1 actual")),
    (SOROK + "10_RECONCILIATION_QUEUE_SOURCE_GAPS_AND_CLOSEOUT_CHECK_R1.md",
     ("Source-qualified post-W8 work-now", "## Post-cut work now", "## PSR1 bounded work-now additions")),
):
    f = ROOT / rel
    if f.is_file():
        content = f.read_text(encoding="utf-8")
        for marker in snippets:
            check(marker in content, f"{rel}: lost combined LIVE/PS receiving marker {marker}")



# Additional conserved evidence families. Structural checks guard against
# accidental omission or duplicate identity, not scientific/current acceptance.
# additional conserved evidence families
parse_rows(PYAT + "05_ROADMAP/SATURATION_REQUIREMENT_OWNER_LINKS.jsonl", 345, "origin_key")
parse_rows(SOROK + "12_W1_W2_INPUT_DISPOSITIONS_R1.jsonl", 100, "source_row_id")
stages = parse_rows(SOROK + "14_W7_RECURSIVE_PHASE_GATES_AND_WORK_PACKAGES_R1.jsonl", 668)
if stages:
    check(stages[0].get("record_type") == "MANIFEST", "Sorok phase manifest missing")

for relative, array_name, n in (
    (SOROK + "07_GITHUB_ACCESSIBLE_ASSET_LOCATOR_R1.json", "assets", 304),
    (SOROK + "08_INITIAL_EVIDENCE_GRADED_DEPENDENCY_AND_SEAM_REGISTER_R1.json", "seams", 22),
):
    p = required(relative)
    if p.is_file():
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            rows = raw[array_name]
            ids = [entry.get("id") for entry in rows]
            check(len(rows) == n and len(set(ids)) == n and all(ids),
                  f"{relative}: expected {n} distinct records")
        except (ValueError, TypeError, KeyError) as exc:
            errors.append(f"{relative}: not a valid conserved register: {exc}")

gap_path = required(PYAT + "05_ROADMAP/NEXT_R_GAP49_NEXT_DECISIONS.md")
if gap_path.is_file():
    import re
    found = set(re.findall(r"\bGAP-\d{3}\b", gap_path.read_text(encoding="utf-8")))
    expected = {f"GAP-{n:03d}" for n in range(1, 50)}
    check(found == expected, f"Pyat GAP01–49 identities changed: absent={sorted(expected - found)} unexpected={sorted(found - expected)}")

# Selected protected NEXT-R documentary preservation. The first canonical
# convergence lost source-qualified accepted locator/currentness sections even
# while all registry counts stayed green. Test the original assertion anchors,
# not only the file identities. Any later intentional retirement must be
# independently justified and update this guard in the same qualified change.
# This is documentary conservation, NOT proof the frozen claims remain current.
# Historical source-cut statements remain subject to later operative decisions.
# protected NEXT-R documentary preservation
protected_next_r = {
    "ASSET_LOCATOR.md": ("## NEXT R — four exact SAT-F missing lookup entries", "F-01 F018 effective-N", "F-04 C3 physical decoder/codec"),
    "CROSS_PLAN_IDS.md": ("## NEXT R — source identity, functional owners and distinct J references", "3,135"),
    "REMAINING_REAL_PYAT_WORK.md": ("## NEXT R — existing GAP-001", "49/49 original GAP"),
    "SATURATION_CODEX_REUSE_HANDOFF.md": ("## NEXT R current P6 and reuse selection cut",),
    "SECTIONS/01_SOURCE_GOVERNANCE.md": ("## NEXT R current-source and independent-source-preparation correction",),
    "SECTIONS/02_U_EPRE_WORKLOAD.md": ("## NEXT R actual worklist compiler / original35 issuer separation", "## PSR1 group-definition/membership"),
    "SECTIONS/05_LEARNED_LIFECYCLE.md": ("## NEXT R learned producer is already read",),
    "SECTIONS/06_FIELD_FORGE_F5.md": ("## NEXT R FF/F5 conditional source/science leaf", "## Post-R2 asset-function succession", "## PSR1 post-FF-R2 seam adequacy"),
    "SECTIONS/07_F6_FIELDS.md": ("## NEXT R F6 independent-source transport",),
    "SECTIONS/08_F7_TEMPORAL.md": ("## NEXT R F7 accepted clocks",),
    "SECTIONS/09_N9_WORLD.md": ("## NEXT R actually read D05/P41", "## PSR1 native selected-world boundary"),
    "SECTIONS/10_N10_POSSIBILITY_F8.md": ("## NEXT R N10E/N10W real consumer ceiling", "## PSR1 post-FF seam applicability"),
    "SECTIONS/11_N11_N12_GATE.md": ("## NEXT R terminal independent no-drop authority",),
}
for rel, markers in protected_next_r.items():
    path = ROOT / PYAT / "05_ROADMAP" / rel
    if path.is_file():
        body = path.read_text(encoding="utf-8")
        for marker in markers:
            check(marker in body, f"{rel}: accepted NEXT-R or qualified new receiving evidence disappeared: {marker}")
    else:
        check(False, f"{rel}: previously protected guide path missing")

if errors:
    for error in errors:
        print("FAIL", error, file=sys.stderr)
    sys.exit(1)
print("PASS canonical tree: Pyat 782/892/62/82, FF 26/16, cross 18/16, Sorok 144/38, no prototype")
print("SCOPE: static source identities and navigation only; no proof of correct science, native joins or live HQ updates")
