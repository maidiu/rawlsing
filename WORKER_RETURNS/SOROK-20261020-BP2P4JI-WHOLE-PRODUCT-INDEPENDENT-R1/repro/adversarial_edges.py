"""Independent adversarial edges beyond the author's court."""
from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
from pathlib import Path

TARGET = Path(__file__).resolve().parents[1] / "runtime" / "target"
sys.path.insert(0, str(TARGET))

import bp2p4  # noqa: E402
bp2p4.install()

from bp2p4 import reunion  # noqa: E402
from bp2p4.c12_verify import chain_digest, verify_branch_chain  # noqa: E402
from bp2p4.product import JoinedProduct, JoinedProductRefusal  # noqa: E402
from bp4.store import C12Store  # noqa: E402


def main():
    root = Path(tempfile.mkdtemp(prefix="bp2p4ji-adv-"))
    intact = reunion.build_fresh(root / "bp2")
    p = JoinedProduct(root / "product", artifacts=intact)
    try:
        p.say("an episode that the attacker will delete")
        before = chain_digest(p.store, "root")
        after = None
        db = p.store.path
    finally:
        p.close()
    with sqlite3.connect(db) as conn:
        conn.execute("DROP TRIGGER IF EXISTS episode_no_delete")
        deleted = conn.execute(
            "DELETE FROM episode WHERE branch_id='root'").rowcount
        conn.commit()
    store = C12Store(db)
    try:
        remaining = verify_branch_chain(store, "root")
        after = chain_digest(store, "root")
        episode_count = len(store.episodes("root"))
    finally:
        store.close()

    # Clock: a root without the post-BP2 world-root marker must be refused.
    unbound = Path(tempfile.mkdtemp(prefix="bp2p4ji-unbound-"))
    s = C12Store(unbound / "c12.sqlite")
    s.create_root("root", clock=10, actor_ids=["A", "B"],
                  state={"world": {}, "actors": {}})
    s.close()
    clock_hold = None
    try:
        JoinedProduct(unbound, artifacts=intact)
        clock_hold = "NO_REFUSAL"
    except JoinedProductRefusal as exc:
        clock_hold = exc.code

    document = {
        "schema": "BP2P4JI_ADVERSARIAL_EDGES@1",
        "sqlite_trigger_delete": {
            "deleted_rows": deleted,
            "remaining_episode_count": episode_count,
            "remaining_chain_verify": remaining,
            "chain_digest_before": before,
            "chain_digest_after": after,
            "detectable_without_stored_digest": False,
            "detectable_against_stored_digest": before != after,
            "trust_boundary": (
                "chain_digest is an unkeyed value. A raw-DB attacker who can also "
                "rewrite the application's stored digest defeats it; only an "
                "independently custodied signed anchor would close this."),
        },
        "clock_without_join_marker": clock_hold,
        "literal_origin_verified": {
            "target": intact.target_id,
            "consumed": intact.consumed_state_hash,
            "mode": intact.mode,
        },
    }
    print(json.dumps(document, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
