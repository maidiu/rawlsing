#!/usr/bin/env python3
"""Source-to-product priority visibility/no-drop court, not empirical or scientific proof."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
MARKER = "PYAT-PRODUCT-PRIORITIES-20261110-R1"
LENS = ("What is possible? What is facilitated? What is inhibited or repressed? "
        "By which forces? In contradiction with what other tendencies? "
        "Under what conditions might those relations change?")
AGENDA = "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/REMAINING_REAL_PYAT_WORK.md"
FRONT = (
    "CROSS_HQ_CONTROL_ROOM/PROGRAMMA/00_PROGRAMMA_RAWLSING.md",
    "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md",
    "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/00_PROGRAMMA_SOROK.md",
)
SECTIONS = {
    "S01": "01_SOURCE_GOVERNANCE.md", "S02": "02_U_EPRE_WORKLOAD.md",
    "S03": "03_ROUTE_B_C11.md", "S04": "04_F1_F4_EMPIRICAL.md",
    "S05": "05_LEARNED_LIFECYCLE.md", "S06": "06_FIELD_FORGE_F5.md",
    "S07": "07_F6_FIELDS.md", "S08": "08_F7_TEMPORAL.md",
    "S09": "09_N9_WORLD.md", "S10": "10_N10_POSSIBILITY_F8.md",
    "S11": "11_N11_N12_GATE.md",
}
PREF = "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/"
ROW = re.compile(r"^\| \*\*.(PP26-\d{2}).\*\* \[(S\d{2})\]\(SECTIONS/([^)]*)\)", re.M)
EXPECTED = tuple(f"PP26-{i:02}" for i in range(1, 28))


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    def content(rel: str) -> str:
        path = root / rel
        if not path.is_file():
            errors.append("missing expected PROGRAMMA file: " + rel)
            return ""
        return path.read_text(encoding="utf-8")

    agenda = content(AGENDA)
    hits = ROW.findall(agenda)
    if tuple(item[0] for item in hits) != EXPECTED:
        errors.append("27 ordered/unique PP26 obligation rows absent/changed")
    by_section: dict[str, list[str]] = {k: [] for k in SECTIONS}
    for item_id, sec, filename in hits:
        if sec not in SECTIONS or filename != SECTIONS.get(sec):
            errors.append(f"mismatched section locator for {item_id}: {sec}/{filename}")
        else:
            by_section[sec].append(item_id)
    for term in (MARKER, LENS, "ParquetC11Carrier", "PERSISTENCE_HELD",
                 "OBSERVED_EMPIRICAL", "EXPLICIT_EXPERIMENTAL_MODEL",
                 "STRONG_CAUSAL/STRUCTURAL", "V550", "PP26-20", "PP26-21", "PP26-27"):
        if term not in agenda:
            errors.append("agenda lost required user/product clause: " + term)
    for rel in FRONT:
        body = content(rel)
        if MARKER not in body[:2600] or LENS not in body[:2600]:
            errors.append("front door lost exact user question: " + rel)
        if "CURRENT PROTECTED STATUS" not in body[:1600]:
            errors.append("front door currentness absent at entry: " + rel)
    for sec, name in SECTIONS.items():
        rel = PREF + name
        body = content(rel)
        if MARKER not in body[:2800] or LENS not in body[:2800]:
            errors.append("roadmap section lost user question: " + rel)
        if "REMAINING_REAL_PYAT_WORK.md" not in body[:2800]:
            errors.append("roadmap section lost central agenda link: " + rel)
        for item in by_section[sec]:
            if (chr(96) + item + chr(96)) not in body[:10000]:
                errors.append(f"{rel}: lost local {item} source/consumer obligation")
    return errors


def self_test() -> None:
    paths = (AGENDA, *FRONT, *(PREF + x for x in SECTIONS.values()))
    with tempfile.TemporaryDirectory(prefix="pyat-priority-visibility-") as raw:
        temp = Path(raw)
        for rel in paths:
            dest = temp / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, dest)
        if validate(temp):
            raise AssertionError("uncorrupted snapshot should pass")
        agenda_path = temp / AGENDA
        original = agenda_path.read_text(encoding="utf-8")
        agenda_path.write_text(original.replace("PP26-13", "PPXX-13", 1), encoding="utf-8")
        if not validate(temp):
            raise AssertionError("missing ledger obligation not detected")
        agenda_path.write_text(original, encoding="utf-8")
        sorok = temp / FRONT[2]
        before = sorok.read_text(encoding="utf-8")
        sorok.write_text(before.replace(LENS, "VAGUE", 1), encoding="utf-8")
        if not validate(temp):
            raise AssertionError("lost Sorok user question not detected")
    print("PASS negative self-test: missing row and Sorok question independently rejected")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    errors = validate(ROOT)
    for problem in errors:
        print("FAIL " + problem, file=sys.stderr)
    if errors:
        return 1
    print("PASS PP26 visibility: 27/27 rows, 11 S sections, 3 HQ front doors")
    print("SCOPE: documentary navigation only; no native science or actor promotion")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
