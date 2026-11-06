"""Cold-process P2 integration entrypoint for the reusable recursion engine.

The response file is an explicitly supplied model-transport fixture. P2 source
inputs are supplied independently and checked by the existing native owners.
This entrypoint makes no original psychological or independent-B claim.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from developmental_recursion.contracts import detached
from developmental_recursion.p2_owner import P2Owner, load_p2


class FileProvider:
    def __init__(self, response_path: Path, request_path: Path | None = None):
        self.response_path = response_path
        self.request_path = request_path

    def call(self, request):
        if self.request_path is not None:
            self.request_path.write_text(json.dumps(detached(request), indent=2) + "\n")
        return json.loads(self.response_path.read_text())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("bootstrap", "advance", "finish"))
    parser.add_argument("--state-root", type=Path, required=True)
    parser.add_argument("--source-pack", type=Path, required=True)
    parser.add_argument("--journal", type=Path, required=True)
    parser.add_argument("--cycle-store", type=Path, required=True)
    parser.add_argument("--model-response", type=Path, required=True)
    parser.add_argument("--model-request-out", type=Path)
    parser.add_argument("--context", type=Path)
    parser.add_argument("--engineering", action="store_true")
    args = parser.parse_args(argv)
    # Deferred imports permit interface inspection while independent packages
    # are being implemented, without a second temporary engine implementation.
    from developmental_recursion.engine import BatchEngine
    from developmental_recursion.model_cycle import RecursionCycle

    pack = json.loads(args.source_pack.read_text())
    owner = P2Owner(load_p2().open(args.state_root), case=pack["case"],
                    source=pack["source"], participants=tuple(pack["participants"]))
    try:
        engine = BatchEngine(owner, args.journal)
        provider = FileProvider(args.model_response, args.model_request_out)
        cycle = RecursionCycle(engine, provider, args.cycle_store)
        context = json.loads(args.context.read_text()) if args.context else None
        result = getattr(cycle, args.command)(context=context)
        if args.engineering:
            output = result
        else:
            # The developing actor's private experience belongs to the internal
            # retrospective request. Default CLI output is an operator summary,
            # not an authorization to publish that experience to a portal user.
            output = {
                "grade": owner.grade,
                "command": args.command,
                "batch_id": result.get("batch_id"),
                "history_hash": result.get("history_hash"),
                "events": [{"event_id": row["event_id"],
                            "experience_status": row["accessible"].get("status")}
                           for row in result.get("records", [])],
            }
        print(json.dumps(output, sort_keys=True, allow_nan=False))
        return 0
    finally:
        owner.close()


if __name__ == "__main__":
    raise SystemExit(main())
