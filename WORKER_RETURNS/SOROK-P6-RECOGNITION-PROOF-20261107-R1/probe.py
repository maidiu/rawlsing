#!/usr/bin/env python3
"""Run the frozen P6 CLI and expose recognition/availability semantics.

This proof is sourcefree. It does not edit the P6 runtime or shared state.
Exit 0 means the expected recognition/access contract was observed; exit 1
means the actual frozen output contradicts it and records the counterexample.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from argparse import Namespace
from pathlib import Path

HERE = Path(__file__).resolve()
P6 = HERE.parents[1] / "SOROK-P6-ONE-LIVING-HOUSE-R1"
P5 = HERE.parents[1] / "SOROK-P5-CONTINUOUS-EXPERIENCE-R1"
sys.path.insert(0, str(P6))
sys.path.insert(0, str(P5))

from run_p6 import experience  # noqa: E402
import house  # noqa: E402
from developmental_recursion.contracts import digest  # noqa: E402


def cli(state: Path, *args: str):
    proc = subprocess.run(
        [sys.executable, "-B", str(P6 / "run_p6.py"), "--state", str(state), *args],
        cwd=str(P6), capture_output=True, text=True, timeout=120,
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    try:
        body = json.loads(proc.stdout)
    except json.JSONDecodeError:
        body = {"raw_stdout": proc.stdout, "raw_stderr": proc.stderr[-1000:]}
    return proc.returncode, body


def changed_input_control(tmp: Path):
    """Change one object identity while preserving clock/available cardinality."""
    normal = tmp / "normal"
    changed = tmp / "changed"
    normal_out = experience(normal, Namespace(command="new", request_id=None))
    original_objects = house.OBJECTS
    original_source = house.SOURCE
    try:
        changed_objects = {key: dict(value) for key, value in original_objects.items()}
        changed_objects["cup"] = changed_objects.pop("mug")
        house.OBJECTS = changed_objects
        house.SOURCE = digest({"rooms": house.ROOMS, "objects": house.OBJECTS,
                               "history": house.HISTORY})
        changed_out = experience(changed, Namespace(command="new", request_id=None))
    finally:
        house.OBJECTS = original_objects
        house.SOURCE = original_source
    return {
        "normal_clock": normal_out["clock"],
        "changed_clock": changed_out["clock"],
        "normal_available": normal_out["available"],
        "changed_available": changed_out["available"],
        "gross_facts_stable": (
            normal_out["clock"] == changed_out["clock"]
            and len(normal_out["available"]) == len(changed_out["available"])
            and normal_out["room"] == changed_out["room"]
        ),
        "identity_changed": changed_out["available"] != normal_out["available"],
    }


def main() -> int:
    failures = []
    with tempfile.TemporaryDirectory(dir=HERE.parent, prefix=".probe-") as td:
        state = Path(td) / "state"
        opening = cli(state, "new")
        view0 = cli(state, "view")
        unavailable_workshop = cli(state, "look", "sandals")
        looked = cli(state, "look", "mug")
        after_look = cli(state, "view")
        moved = cli(state, "go", "living room")
        living = cli(state, "view")
        unavailable_missing = cli(state, "look", "missing-object")
        looked_living = cli(state, "look", "sandals")
        changed = changed_input_control(Path(td))

    def add(name, passed, actual):
        if not passed:
            failures.append({"assertion": name, "actual": actual})

    opening_body = opening[1]
    add("new exits 0", opening[0] == 0, opening[0])
    add("no specialized object names before recognition",
        not ({"bench", "mug"} & set(opening_body.get("available", ()))),
        opening_body.get("available"))
    add("no specialized detail before recognition",
        not any(word in str(opening_body.get("detail")) for word in ("bench", "mug")),
        opening_body.get("detail"))
    add("view before recognition equals opening semantics",
        view0[0] == 0 and view0[1].get("available") == opening_body.get("available")
        and view0[1].get("detail") == opening_body.get("detail"),
        {"opening": opening_body.get("available"), "view": view0[1].get("available")})
    add("unavailable/foreign object refuses",
        unavailable_workshop[0] == 0
        and unavailable_workshop[1].get("admission") == "UNAVAILABLE",
        unavailable_workshop[1])
    add("legitimate look admits",
        looked[0] == 0 and looked[1].get("admission") == "ADMITTED",
        looked[1])
    add("legitimate look exposes observed detail",
        any("chip" in str(row.get("text", "")) for row in looked[1].get("narration", ())),
        looked[1].get("narration"))
    add("look does not expose unrelated photo detail",
        not any("photograph" in str(row.get("text", "")).lower()
                for row in looked[1].get("narration", ())),
        looked[1].get("narration"))
    add("moving to a room does not itself recognize specialized objects",
        not ({"sandals", "photo", "coaster"} & set(moved[1].get("available", ()))),
        moved[1].get("available"))
    add("living view does not expose specialized names before recognition",
        not ({"sandals", "photo", "coaster"} & set(living[1].get("available", ()))),
        living[1].get("available"))
    add("unknown/private object refuses",
        unavailable_missing[0] == 0
        and unavailable_missing[1].get("admission") == "UNAVAILABLE",
        unavailable_missing[1])
    add("after access, sandal detail is observable",
        looked_living[0] == 0
        and any("Blue thread" in str(row.get("text", ""))
                for row in looked_living[1].get("narration", ())),
        looked_living[1].get("narration"))
    add("changed input preserves gross facts",
        changed["gross_facts_stable"] and changed["identity_changed"], changed)

    evidence = {
        "schema": "SOROK_P6_RECOGNITION_PROOF@1",
        "sourcefree": True,
        "frozen_sha": "41b21babf72c4c8b0b4b012d3c8b7d7f6247791f",
        "runtime": "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py",
        "commands": [
            "run_p6.py --state <temp> new",
            "run_p6.py --state <temp> view",
            "run_p6.py --state <temp> look sandals",
            "run_p6.py --state <temp> look mug",
            "run_p6.py --state <temp> go 'living room'",
            "run_p6.py --state <temp> view",
            "run_p6.py --state <temp> look missing-object",
            "run_p6.py --state <temp> look sandals",
        ],
        "outputs": {
            "opening": opening_body,
            "view_before": view0[1],
            "unavailable_workshop": unavailable_workshop[1],
            "look_mug": looked[1],
            "living_after_move": moved[1],
            "living_view": living[1],
            "unavailable_missing": unavailable_missing[1],
            "look_sandals_living": looked_living[1],
            "changed_input_control": changed,
        },
        "assertions": {"total": 13, "failures": failures},
        "result": "PASS" if not failures else "FAILING_COUNTEREXAMPLE",
        "fix_location": [
            "run_p6.experience: objects = frame.pop('objects'); result['available'] = sorted(objects); result['detail'] = objects.get(selected)",
            "house.scene: returns every object key/glance in the current room",
            "attention.select: empty history selects the first object, so view exposes detail before recognition",
            "attention.register is only called after an admitted look; view/output never gates on that exposure",
        ],
    }
    out = HERE.parent / "evidence.json"
    out.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf8")
    print(json.dumps({
        "result": evidence["result"],
        "failures": failures,
        "evidence": str(out),
    }, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
