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
from rawlsing_next.sorok_history.owner import HistoricalWorld, SurfaceParticular, digest
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
        except BaseException as exc:
            # Transport error strings deliberately contain no authorization data.
            record["failure"] = {
                "type": type(exc).__name__, "code": getattr(exc, "code", None),
            }
            raise
        finally:
            record["wall_seconds"] = time.perf_counter() - started
            path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")


def source_initializer(manifest):
    """Trusted sourcefree initialization through the existing foreground owner.

    This supplies experimental source rights, never a model-asserted grant.
    The same adapter accepts every domain; it contains no domain story branches.
    """
    if manifest.get("evidence_class") != "SOURCEFREE_SYNTHETIC":
        raise ValueError("only explicitly synthetic engineering sources are authorized")
    surfaces = manifest["surfaces"]
    if not 1 <= len(surfaces) <= 7:
        raise ValueError("source cohort must contain 1..7 new surfaces")

    def establish(session):
        here = session.world().positions[session.meta["user_actor"]]
        parent = session.events()[0]
        session.travel("market" if here == "workshop" else "workshop")
        session.travel(here)
        event = session.events()[-1]
        history = HistoricalWorld(session)
        targets = [history.capture_visible_tool_resource()]
        for surface in surfaces:
            row = history.admit_surface(SurfaceParticular(
                event["event_id"], surface["source_ref"], surface["domain"], here,
                surface["physical"], tuple(surface["unresolved"])))
            targets.append(row["id"])
        parent_ref = {"kind": "WORLD_EVENT", "object_id": parent["event_id"],
                      "content_hash": parent["hash"]}
        entities = []
        for item in manifest["entities"]:
            record = {**item, "evidence_class": "SOURCEFREE_SYNTHETIC",
                      "source_event_ref": parent_ref}
            entities.append({"ref": {"kind": record["kind"],
                "object_id": record["object_id"], "content_hash": digest(record)},
                "record": record})
        record = {"kind": "PLACE", "object_id": "source:initial-place",
                  "location": parent["location"], "evidence_class": "SOURCEFREE_SYNTHETIC",
                  "source_event_ref": parent_ref}
        entities.append({"ref": {"kind": "PLACE", "object_id": record["object_id"],
                                  "content_hash": digest(record)}, "record": record})
        history.configure_experimental_history(source_event_ref=parent_ref,
            target_ids=targets, entities=entities, earliest=parent["clock"])
    return establish


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--receipts", required=True, type=Path)
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--key-env", default="SOROK_HISTORY_MODEL_API_KEY")
    parser.add_argument("--max-output-tokens", type=int, default=8192,
                        help="Total response bound, including provider reasoning tokens.")
    parser.add_argument("--reasoning-effort", choices=["low", "high", "max"])
    parser.add_argument("--jobs", type=int, choices=range(1, 4), default=1)
    parser.add_argument("--source-manifest", type=Path,
                        help="Trusted SOURCEFREE_SYNTHETIC cohort; no native authority.")
    parser.add_argument("--independent", action="store_true",
                        help="Run normal work before inference; omit all inspection.")
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
        manifest = (json.loads(args.source_manifest.read_text())
                    if args.source_manifest else None)
        opening = new(args.state, args.state / "p4_receipts.json", "recognized_plan",
                      establish=source_initializer(manifest) if manifest else None)
        if manifest:
            (args.receipts / "source-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        (args.receipts / "opening.json").write_text(json.dumps(opening, indent=2) + "\n")
    if args.independent and not args.resume:
        # Resume services the existing outbox/requirement; never issue another
        # foreground work action merely to obtain a new history-provider result.
        import subprocess
        performed = subprocess.run([sys.executable, str(ROOT / "WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py"),
            "--state", str(args.state), "work"], capture_output=True, text=True)
        (args.receipts / "ordinary-work-before.json").write_text(json.dumps({
            "exit_code": performed.returncode, "stdout": performed.stdout,
            "stderr": performed.stderr}, indent=2) + "\n")
        if performed.returncode:
            return performed.returncode
    config = ProviderConfig(
        endpoint=args.endpoint, model=args.model, api_key=key,
        timeout_s=120, max_attempts=1, max_output_tokens=args.max_output_tokens,
        reasoning_effort=args.reasoning_effort,
    )
    transport = RecordingEndpoint(
        args.endpoint, args.model, api_key=key, timeout_s=120, receipts=args.receipts,
    )
    provider = HistoricalModelProvider(config=config, transport=transport)
    owner = open_owner(args.state / "actual-p2")
    try:
        intervals_before = sum((r.get("domain") or {}).get("mode") == "ACTUAL"
                               for r in owner.base_owner.fanin.session.read_interval_states())
    finally:
        owner.close()
    outcomes = [run_history_worker(args.state, provider=provider) for _ in range(args.jobs)]
    outcome = outcomes[-1]
    owner = open_owner(args.state / "actual-p2")
    try:
        history = HistoricalWorld(owner.base_owner.fanin.session)
        surfaces = history.visible_surfaces()
        rows = []
        for target in surfaces:
            stored = history.target(target["id"])
            job = history.job(stored["job_id"])
            row = {"target": stored, "job": job,
                   "world_depth": history.query_depth(target["id"])}
            if not args.independent:
                event = history.inspect(target["id"])
                row["inspection"] = history.read_inspection(event["event_id"])
            rows.append(row)
        processed = history.job(outcome["job_id"]) if outcome.get("job_id") else None
        processed_read = history.query_depth(processed["target_id"]) if processed else None
        intervals_after = sum((r.get("domain") or {}).get("mode") == "ACTUAL"
                              for r in owner.base_owner.fanin.session.read_interval_states())
        graph = history.history_graph()
        inspections = sum(event["kind"] == "INSPECT" for event in owner.base_owner.fanin.session.events())
    finally:
        owner.close()
    # Reopen the existing owner, without any provider invocation, for cold readback.
    owner = open_owner(args.state / "actual-p2")
    try:
        history = HistoricalWorld(owner.base_owner.fanin.session)
        cold_equal = all(history.target(row["target"]["id"]) == row["target"] for row in rows)
        cold_world_equal = (history.query_depth(processed["target_id"]) == processed_read
                            if processed else True)
    finally:
        owner.close()
    result = {"schema": "SOROK_MI_LIVE_EXECUTION@1", "source_grade": "SOURCEFREE_S2",
              "provider_calls": transport.calls, "provider_live": provider.live,
              "outcome": outcome, "outcomes": outcomes, "targets": rows, "cold_target_equal": cold_equal,
              "history_graph": graph, "inspection_count": inspections,
              "independent": args.independent,
              "processed_target_world_depth": processed_read,
              "cold_world_read_equal": cold_world_equal,
              "actual_intervals_before": intervals_before, "actual_intervals_after": intervals_after,
              "native_science": "HOLD", "protected_merge": "NOT_AUTHORIZED"}
    execution = args.receipts / f"execution-{transport.offset + transport.calls:02d}.json"
    execution.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": outcome.get("status"), "provider_calls": transport.calls,
                      "provider_live": provider.live, "cold_target_equal": cold_equal,
                      "receipts": str(args.receipts)}))
    return 0 if outcome.get("accepted") and cold_equal and cold_world_equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
