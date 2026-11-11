#!/usr/bin/env python3
"""Run the existing history worker against an explicitly configured real model.

Use a fresh sourcefree state directory. Credentials are read only from the
specified environment variable and are never included in the written receipts.
This command proves model-assisted engineering, not native actor science.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1"))

from run_p4 import new, open_owner, run_history_worker
from rawlsing_next.sorok_history.owner import HistoricalWorld
from rawlsing_next.sorok_history.provider import (
    EndpointModelTransport, HistoricalModelProvider, ProviderConfig,
)


class RecordingEndpoint(EndpointModelTransport):
    """The actual endpoint transport, with task-local request/output custody."""

    def __init__(self, *args, receipts, **kwargs):
        super().__init__(*args, **kwargs)
        self.receipts = receipts
        self.calls = 0
        self.offset = len(list(receipts.glob("provider-*.json")))

    async def __call__(self, request):
        self.calls += 1
        path = self.receipts / f"provider-{self.offset + self.calls:02d}.json"
        record = {"request": dict(request), "transport": "REAL_HTTP_ENDPOINT"}
        started = time.perf_counter()
        try:
            response = await super().__call__(request)
            record["response"] = response
            return response
        except Exception as exc:
            # Transport error strings deliberately contain no authorization data.
            record["failure"] = {
                "type": type(exc).__name__, "code": getattr(exc, "code", None),
            }
            raise
        finally:
            record["wall_seconds"] = time.perf_counter() - started
            path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--receipts", required=True, type=Path)
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--key-env", default="SOROK_HISTORY_MODEL_API_KEY")
    parser.add_argument("--max-output-tokens", type=int, default=8192,
                        help="Total response bound, including provider reasoning tokens.")
    parser.add_argument("--resume", action="store_true",
                        help="Resume this command's existing durable failed/pending job.")
    args = parser.parse_args()
    if args.state.exists() and not args.resume:
        parser.error("state must be fresh; never replace an existing encounter")
    if args.resume and not (args.state / "p4_receipts.json").is_file():
        parser.error("resume requires an existing P4 encounter")
    key = os.environ.get(args.key_env)
    if not key:
        print(json.dumps({"grade": "LIVE_PROVIDER_NOT_RUN", "missing_env": args.key_env}))
        return 2
    args.state.mkdir(parents=True, exist_ok=args.resume)
    args.receipts.mkdir(parents=True, exist_ok=True)
    if not args.resume:
        opening = new(args.state, args.state / "p4_receipts.json", "recognized_plan")
        (args.receipts / "opening.json").write_text(json.dumps(opening, indent=2) + "\n")
    config = ProviderConfig(
        endpoint=args.endpoint, model=args.model, api_key=key,
        timeout_s=120, max_attempts=1, max_output_tokens=args.max_output_tokens,
    )
    transport = RecordingEndpoint(
        args.endpoint, args.model, api_key=key, timeout_s=120, receipts=args.receipts,
    )
    provider = HistoricalModelProvider(config=config, transport=transport)
    outcome = run_history_worker(args.state, provider=provider)
    owner = open_owner(args.state / "actual-p2")
    try:
        history = HistoricalWorld(owner.base_owner.fanin.session)
        surfaces = history.visible_surfaces()
        rows = []
        for target in surfaces:
            stored = history.target(target["id"])
            job = history.job(stored["job_id"])
            event = history.inspect(target["id"])
            rows.append({"target": stored, "job": job,
                         "inspection": history.read_inspection(event["event_id"])})
    finally:
        owner.close()
    # Reopen the existing owner, without any provider invocation, for cold readback.
    owner = open_owner(args.state / "actual-p2")
    try:
        history = HistoricalWorld(owner.base_owner.fanin.session)
        cold_equal = all(history.target(row["target"]["id"]) == row["target"] for row in rows)
    finally:
        owner.close()
    result = {"schema": "SOROK_MI_LIVE_EXECUTION@1", "source_grade": "SOURCEFREE_S2",
              "provider_calls": transport.calls, "provider_live": provider.live,
              "outcome": outcome, "targets": rows, "cold_target_equal": cold_equal,
              "native_science": "HOLD", "protected_merge": "NOT_AUTHORIZED"}
    execution = args.receipts / f"execution-{transport.offset + transport.calls:02d}.json"
    execution.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": outcome.get("status"), "provider_calls": transport.calls,
                      "provider_live": provider.live, "cold_target_equal": cold_equal,
                      "receipts": str(args.receipts)}))
    return 0 if outcome.get("accepted") and cold_equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
