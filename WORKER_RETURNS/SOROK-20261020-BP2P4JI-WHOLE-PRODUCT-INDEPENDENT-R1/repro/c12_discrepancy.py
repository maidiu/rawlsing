"""Mandatory special court: resolve the BP2P4J C12 verifier contradiction.

Runs the author's exact JoinedProduct/BP4 store on a fresh valid episode and
shows (a) the delivered independent verifier fails a valid episode, (b) the row
itself is intact under its true preimage, (c) the author's 'clean' test passes
only because it has no episode row, and (d) the minimal correct verifier.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

TARGET = Path(__file__).resolve().parents[1] / "runtime" / "target"
sys.path.insert(0, str(TARGET))

import bp2p4  # noqa: E402
bp2p4.install()

from bp1.canon import digest  # noqa: E402
from bp2p4 import reunion  # noqa: E402
from bp2p4.c12_verify import chain_digest, verify_branch_chain  # noqa: E402
from bp2p4.product import JoinedProduct  # noqa: E402


def episode_rows(store):
    return list(store.db.execute(
        "SELECT seq,body,hash FROM episode WHERE branch_id='root' ORDER BY seq"))


def repaired_verify(store, branch_id="root"):
    """Minimal correct episode verification: exclude hash AND episode_id."""
    errors = []
    for seq, body, stored_hash in episode_rows(store):
        parsed = json.loads(body)
        preimage = {k: v for k, v in parsed.items() if k not in ("hash", "episode_id")}
        if parsed.get("hash") != digest(preimage) or stored_hash != parsed.get("hash"):
            errors.append(f"episode:{seq}")
    return {"ok": not errors, "errors": errors}


def main():
    root = Path(tempfile.mkdtemp(prefix="bp2p4ji-c12-"))
    intact = reunion.build_fresh(root / "bp2")
    product = JoinedProduct(root / "product", artifacts=intact)
    try:
        before = verify_branch_chain(product.store, "root")
        before_upstream = product.store.verify("root")
        product.say("a valid episode that exposes the verifier preimage")
        after = verify_branch_chain(product.store, "root")
        after_upstream = product.store.verify("root")
        rows = episode_rows(product.store)
        body = json.loads(rows[0][1])
        without_hash = digest({k: v for k, v in body.items() if k != "hash"})
        without_hash_and_id = digest(
            {k: v for k, v in body.items() if k not in ("hash", "episode_id")})
        document = {
            "schema": "BP2P4JI_C12_DISCREPANCY@1",
            "pre_episode": {
                "independent_verify": before,
                "upstream_verify": before_upstream,
            },
            "post_episode": {
                "independent_verify": after,
                "upstream_verify": after_upstream,
            },
            "episode_row": {
                "seq": rows[0][0],
                "stored_column_hash": rows[0][2],
                "body_hash_field": body.get("hash"),
                "has_episode_id": "episode_id" in body,
                "digest_body_minus_hash": without_hash,
                "digest_body_minus_hash_and_episode_id": without_hash_and_id,
                "true_preimage_matches": without_hash_and_id == body.get("hash"),
                "delivered_verifier_preimage_matches": without_hash == body.get("hash"),
            },
            "repaired_verify": repaired_verify(product.store),
            "conclusion": (
                "The C12 episode row is intact. BP4's C12Store.verify is "
                "self-referential (includes hash), and BP2P4J's independent "
                "c12_verify is also wrong for episodes (includes episode_id, "
                "which was appended after hashing). The author's clean test has "
                "no episode row, so it does not exercise the failing path."),
            "chain_digest": chain_digest(product.store, "root"),
        }
        print(json.dumps(document, indent=2, sort_keys=True))
        return 0 if (not after["ok"] and document["episode_row"]["true_preimage_matches"]
                     and document["repaired_verify"]["ok"]) else 1
    finally:
        product.close()


if __name__ == "__main__":
    raise SystemExit(main())
