#!/usr/bin/env python3
"""Non-authoritative documentary entrypoint guard for the Rawlsing HQ OATH R2.

Checks presence and exact parity of the actual first-contact blocks and root
OpenCode project instructions. Does NOT establish live GitHub currentness,
agent comprehension, writer leases, independent receiving or protected adoption.
"""
from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = (
    ROOT / "CROSS_HQ_CONTROL_ROOM/PROGRAMMA/00_PROGRAMMA_RAWLSING.md",
    ROOT / "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md",
    ROOT / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/00_PROGRAMMA_SOROK.md",
)
INSTRUCTIONS = ROOT / "AGENTS.md"
START = "# HQ OATH — PROGRAMMA FIRST CONTACT\n<!-- HQ_OATH_R2_FIRST_CONTACT_START -->"
END = "<!-- HQ_OATH_R2_FIRST_CONTACT_END -->"
REQUIRED = (
    "under pain of eternal damnation",
    "CURRENT_PROGRESS.md",
    "CURRENT_PROGRESS.json",
    "HQ_CURRENTNESS_HOLD",
    "Every new implementation",
    "independent-review",
    "exact HEAD",
    "Before every HQ handoff",
    "operating machine",
)
# Some required concepts appear with equivalent wording; these mandatory
# literal sentinels intentionally remain a minimal subset of the actual oath.
REQUIRED = tuple(x for x in REQUIRED if x not in ("Every new implementation", "independent-review"))

def first_block(value: str) -> str:
    if not value.startswith(START):
        raise ValueError("HQ OATH is not the very first block")
    if value.count(END) != 1:
        raise ValueError("HQ OATH ending marker missing or duplicated")
    end = value.index(END) + len(END)
    block = value[:end]
    if not all(token in block for token in REQUIRED):
        raise ValueError("HQ OATH lost an operational invariant")
    if not value[end:].startswith("\n\n---\n\n# PROGRAMMA "):
        raise ValueError("HQ OATH must immediately precede original PROGRAMMA front door")
    return block

def validate(inputs: tuple[str, ...], instructions: str) -> None:
    blocks = tuple(first_block(value) for value in inputs)
    if len(set(blocks)) != 1:
        raise ValueError("shared, PYAT or SOROK HQ OATH diverged")
    if not instructions.startswith("# HQ OATH — REQUIRED FIRST CONTACT FOR PROGRAMMA WORK"):
        raise ValueError("project-level OpenCode AGENTS.md lacks first-contact HQ OATH")
    if not all(str(path.relative_to(ROOT)) in instructions for path in ENTRYPOINTS):
        raise ValueError("project AGENTS.md lacks exact canonical front-door pointers")

def self_test(values: tuple[str, ...], instructions: str) -> None:
    validate(values, instructions)
    bad = []
    for i, value in enumerate(values):
        altered = list(values)
        altered[i] = value.replace(START, "# stale\\n", 1)
        bad.append((tuple(altered), instructions))
        altered = list(values)
        altered[i] = value.replace(END, "", 1)
        bad.append((tuple(altered), instructions))
        altered = list(values)
        altered[i] = value.replace("HQ_CURRENTNESS_HOLD", "untracked", 1)
        bad.append((tuple(altered), instructions))
    bad.append((values, instructions.replace(
        "# HQ OATH — REQUIRED FIRST CONTACT FOR PROGRAMMA WORK",
        "# missing HQ entrypoint", 1)))
    for index, (candidate, guide) in enumerate(bad, 1):
        try:
            validate(candidate, guide)
        except ValueError:
            pass
        else:
            raise AssertionError(f"mutation {index} escaped HQ OATH guard")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    values = tuple(p.read_text(encoding="utf-8") for p in ENTRYPOINTS)
    guide = INSTRUCTIONS.read_text(encoding="utf-8")
    validate(values, guide)
    if args.self_test:
        self_test(values, guide)
    print("PASS_HQ_OATH_FRONTDOORS_AND_OPENCODE_INSTRUCTIONS"
          + ("_SELF_TEST" if args.self_test else "")
          + "; NOT_LIVE_CURRENTNESS_OR_AGENT_ACCREDITATION")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, AssertionError) as exc:
        print(f"HQ_OATH_GUARD_FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
