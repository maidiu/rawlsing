"""Fresh-process C05 cold reader. Read-only except an exact idempotent retry."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from c05_observe_prior89 import counts, snapshot  # noqa: E402
from developmental_recursion.contracts import canonical  # noqa: E402
from developmental_recursion.continuing_relations import (  # noqa: E402
    record_relation_change,
)
from developmental_recursion.p2_owner import load_p2  # noqa: E402


def main() -> int:
    config = json.loads(sys.argv[1])
    fanin = load_p2().open(Path(config["state_root"]))
    try:
        session = fanin.session
        warm = snapshot(
            session, config["actor_ids"], config["event_ids"],
            config["as_of_by_event"], config["all_clocks"])
        before = counts(session)
        retry_config = config["retry"]
        retried = record_relation_change(
            session,
            actor_id=retry_config["actor_id"],
            other_actor_id=retry_config["other_actor_id"],
            relation=retry_config["relation"],
            change=retry_config["change"],
            clock=retry_config["clock"],
            operation_id=retry_config["operation_id"],
            exposed_actor_ids=retry_config["exposed_actor_ids"],
            value=retry_config["value"],
            private_state=retry_config["private_state"],
        )
        after = counts(session)
        print(canonical({
            "snapshot": warm,
            "retry": {
                "status": retried.get("status"),
                "primary_episode_id": retried.get("primary_episode_id"),
                "head_episode_id": retried.get("head_episode_id"),
                "current_status": retried.get("current_status"),
                "representation_depth": retried.get("representation_depth"),
                "counts_before": before,
                "counts_after": after,
            },
        }))
    finally:
        fanin.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
