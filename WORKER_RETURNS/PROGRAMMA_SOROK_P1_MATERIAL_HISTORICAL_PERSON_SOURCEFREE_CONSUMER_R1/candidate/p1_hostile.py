"""P1 source-C12 hostile receipt: tamper, restore, selfhash custody hold, forgery."""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from p1_consumer import DEPS  # noqa: E402  (installs M35/JOIN-E and paths)

from joined.session import JoinedSession  # noqa: E402
from r30a.first_session import SessionRefusal  # noqa: E402
from r31j.scenarios import evaluated  # noqa: E402
from bp1.canon import digest  # noqa: E402
import firstclass  # noqa: E402


def _tamper_body(db_path: Path, *, selfhash: bool) -> None:
    db = sqlite3.connect(db_path)
    try:
        db.execute("DROP TRIGGER episode_no_update")
        row = db.execute("SELECT body,hash FROM episode WHERE branch_id='root' AND seq=0").fetchone()
        body = json.loads(row[0])
        body["p1_tamper"] = "coordinated" if selfhash else "plain"
        if selfhash:
            preimage = {k: v for k, v in body.items() if k != "hash"}
            preimage.pop("episode_id", None)
            body["hash"] = digest(preimage)
        db.execute("UPDATE episode SET body=?,hash=? WHERE branch_id='root' AND seq=0",
                   (json.dumps(body, sort_keys=True), body["hash"]))
        db.commit()
    finally:
        db.close()


def run(root: Path) -> dict:
    root = root.resolve()
    state = root / "clean"
    s = JoinedSession.start(state, perform="omit")
    try:
        assert s.verify()["ok"] is True
    finally:
        s.close()
    db_path = state / "product" / "c12.sqlite"
    backup = db_path.read_bytes()

    _tamper_body(db_path, selfhash=False)
    simple = {"rejected": False, "error": ""}
    try:
        JoinedSession.open(state)
    except Exception as exc:  # exact typed refusal is asserted below
        simple.update(rejected=isinstance(exc, SessionRefusal),
                      error=type(exc).__name__ + ":" + str(exc))
    db_path.write_bytes(backup)
    restored = JoinedSession.open(state)
    try:
        restore = {"ok": restored.verify()["ok"]}
    finally:
        restored.close()

    _tamper_body(db_path, selfhash=True)
    coord_ok = False
    coord_open = None
    try:
        coord_open = JoinedSession.open(state)
        coord_ok = coord_open.verify()["ok"]
    finally:
        if coord_open is not None:
            coord_open.close()
    db_path.write_bytes(backup)
    after_coord = JoinedSession.open(state)
    try:
        coord_restore = {"ok": after_coord.verify()["ok"]}
    finally:
        after_coord.close()

    case = evaluated(share=True, e2=False)["case"]
    base = firstclass.source_from_case(case)
    mutations = {
        "wrong_owner": {"b_owner": "FAKE_OWNER"},
        "wrong_event_ref": {"b_event_ref": "TEST_ONLY_FAKE_EVENT"},
        "wrong_event_hash": {"b_event_hash": "0" * 64},
        "wrong_clock": {"b_clock": 999},
        "wrong_operation": {"b_operation": "REFUSE_TOOL", "b_quantity": 0},
        "wrong_quantity": {"b_quantity": 5},
        "wrong_e1_ref": {"a_e1_ref": "TEST_ONLY_FAKE_E1"},
        "wrong_e1_hash": {"a_e1_hash": "0" * 64},
        "wrong_e1_clock": {"a_e1_clock": 999},
    }
    forge = {"attempted": len(mutations), "rejected": 0, "codes": []}
    for label, change in mutations.items():
        source = dict(base)
        source.update(change)
        target = root / "forgeries" / label
        try:
            firstclass.c9_only(target, case=case, source=source)
        except firstclass.MaterialSourceRefusal as exc:
            assert exc.code == "MATERIAL_SOURCE_PREIMAGE_MISMATCH"
            assert not (target / "bp2").exists()
            forge["rejected"] += 1
            forge["codes"].append(label + ":MATERIAL_SOURCE_PREIMAGE_MISMATCH")
    return {
        "schema": "SOROK_P1_HOSTILE_RECEIPT@1",
        "grade": "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
        "native": False,
        "simple_c12_tamper": simple,
        "exact_restore": restore,
        "coordinated_selfhash": {
            "restore_after_coordinated": coord_restore,
            "c12_selfhash_ok": coord_ok,
            "verdict": "TRUST_CUSTODY_HOLD" if coord_ok else "REJECTED",
            "external_anchor": "ABSENT_OWNER_ANCHOR_REQUIRED",
            "production_accept": False,
        },
        "source_preimage_forgeries": forge,
        "holds": [
            "C12_SELFHASH_IS_NOT_SEPARATE_CUSTODY",
            "EXTERNAL_OWNER_ANCHOR_REQUIRED",
            "C9_ACTOR_NATIVE_ANCHOR_ABSENT",
            "CP_A5_SEPARATE_ROOT_HOLD",
        ],
    }


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    data = run(Path(args.root))
    Path(args.output).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps(data, indent=2, sort_keys=True))
