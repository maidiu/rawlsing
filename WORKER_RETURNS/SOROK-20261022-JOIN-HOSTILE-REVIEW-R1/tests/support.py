import json
import os
import shutil
from pathlib import Path

from joined.session import JoinedSession
from r30a.first_session import FirstSession, SessionRefusal
from r31j.build import product as build_product
from r31j.scenarios import evaluated

DEFAULT_CANDIDATE_ROOT = (
    Path(__file__).resolve().parents[3]
    / "WORKER_RETURNS"
    / "SOROK-20261022-SAME-PERSON-JOIN-R1"
)
CANDIDATE_ROOT = Path(
    os.environ.get("SOROK_JOIN_CANDIDATE_ROOT", str(DEFAULT_CANDIDATE_ROOT))
).resolve()

J_SOURCE_REF = "64fec28c374d8f77fb0b412d0c934d798ede03e8"
E_SOURCE_REF = "a2760d3687b063513fe0a5b9589c56c998d4ccb5"
JOIN_SCHEMA = "SOROK_SAME_PERSON_JOIN@1"


def start(root, *, perform="omit", attention="focused"):
    return JoinedSession.start(Path(root), perform=perform, attention=attention)


def read_meta(root):
    return json.loads((Path(root) / "session.json").read_text())


def write_meta(root, meta):
    (Path(root) / "session.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf8"
    )


def make_donor(root, *, share, e2, perform="omit"):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    scenario = evaluated(share=share, e2=e2)
    product, built, producer = build_product(
        root,
        gm01=scenario["gm01"],
        case=scenario["case"],
        variant="A_REPAIR_LONG",
    )
    producer.close()
    if perform == "e2":
        product.material_inspect()
    elif perform == "omit":
        product.record_omission()
    else:
        raise ValueError(perform)
    session = JoinedSession._attach_new(
        product,
        root,
        scenario="available",
        attention="focused",
        variant="A_REPAIR_LONG",
    )
    session.meta.update(
        schema=JOIN_SCHEMA,
        grade="TEST_ONLY_SOURCEFREE_NOT_NATIVE",
        material_performance=perform,
        j_source_ref=J_SOURCE_REF,
        e_source_ref=E_SOURCE_REF,
    )
    session._save_join_meta()
    return session


def clone_session(source_root, target_root, *, attention):
    source_root = Path(source_root)
    target_root = Path(target_root)
    shutil.copytree(source_root, target_root)
    meta = read_meta(target_root)
    old_product_root = Path(meta["product_root"])
    meta["product_root"] = str((target_root / old_product_root.name).resolve())
    meta["state_root"] = str(target_root.resolve())
    write_meta(target_root, meta)
    return JoinedSession.open(target_root, attention=attention)


def r29p_donor(root):
    donor_root = Path(root)
    session = FirstSession.start(
        donor_root, scenario="available", attention="focused"
    )
    try:
        return Path(session.product.root)
    finally:
        session.close()


def gm01_episode_source(session):
    rows = [
        row
        for row in session.episodes("A")
        if row["kind"] == "GM01_SOURCE"
    ]
    return rows[-1]["body"]["gm01_source"]
