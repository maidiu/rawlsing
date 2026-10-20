#!/usr/bin/env python3
"""Export BP1 two-actor, NO_CHANGE and DENY receipts as machine-readable evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
for _path in (
    RETURN / "candidate",
    RETURN / "vendor/g18/candidate",
    RETURN / "vendor/c9r",
    RETURN / "vendor/c9r/runtime/native",
):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from bp1 import (  # noqa: E402
    build_denied_life,
    build_no_change_life,
    build_two_actor_life,
)


def main():
    out_dir = RETURN / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)
    two = build_two_actor_life()
    (out_dir / "two_actor_life.json").write_text(
        json.dumps(two.receipt(), indent=2, sort_keys=True) + "\n")
    no_change = build_no_change_life()
    (out_dir / "no_change_life.json").write_text(
        json.dumps(no_change, indent=2, sort_keys=True) + "\n")
    denied = build_denied_life()
    (out_dir / "denied_life.json").write_text(
        json.dumps(denied, indent=2, sort_keys=True) + "\n")
    print(json.dumps(dict(
        two_actor_states=two.receipt()["state_hashes"],
        performed_units=[a["after"]["completed_units"] - a["before"]["completed_units"]
                         for a in two.witness["actions"]],
        no_change_unchanged=no_change["state_unchanged"],
        denied_unchanged=denied["state_unchanged"],
    ), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
