"""Verify exact documentary anchors and no production edits; no network/source reads."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[1]
BASE = "9561723cfe0932869e781f2be27e9c80b050ad7a"
FREEZE = "d58046079707417eddaeeed4343fc9e65a33eb20"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def check_anchor(a):
    raw = git("show", a["commit"] + ":" + a["path"])
    assert git("rev-parse", a["commit"] + ":" + a["path"]).decode().strip() == a["blob"], a["id"]
    assert hashlib.sha256(raw).hexdigest() == a["sha256"], a["id"]
    lines = raw.decode().splitlines()
    assert "\n".join(lines[a["line_start"]-1:a["line_end"]]) == a["excerpt"], a["id"]
    assert a["claim"] and a["adoption_grade"], a["id"]


def main():
    anchors = json.loads((PACKET / "08_EXACT_SOURCE_ANCHORS.json").read_text())["anchors"]
    supplement = PACKET / "evidence/supplemental_anchors.json"
    extra = json.loads(supplement.read_text())["anchors"] if supplement.exists() else []
    for a in anchors + extra:
        check_anchor(a)
    assert len({a["id"] for a in anchors + extra}) == len(anchors + extra)
    with (PACKET / "06_ADVERSARIAL_ELIGIBILITY_CANARIES.csv").open() as f:
        cases = list(csv.DictReader(f))
    assert len(cases) == 28
    assert len({r["id"] for r in cases}) == len(cases)
    assert all(r["anchor_id"] in {a["id"] for a in anchors} for r in cases)
    for path in git("ls-tree", "-r", "--name-only", FREEZE, str(PACKET.relative_to(ROOT))).decode().splitlines():
        assert (ROOT / path).read_bytes() == git("show", FREEZE + ":" + path), path
    changed = git("diff", "--name-only", BASE).decode().splitlines()
    prefix = str(PACKET.relative_to(ROOT)) + "/"
    assert all(p.startswith(prefix) for p in changed), changed
    matrix = json.loads(git("show", BASE + ":PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/ESTATE_35X_REQUIREMENTS_MATRIX.json"))
    assert len(matrix["sources"]) == 35
    result = {"status": "EXACT_DOCUMENTARY_PACKET_VERIFIED", "frozen_commit": FREEZE,
              "pinned_anchors": len(anchors), "supplemental_anchors": len(extra),
              "canary_classes": len(cases), "original_waves_conserved": 35,
              "production_changes": 0, "source_execution": "NOT_RUN"}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
