#!/usr/bin/env python3
"""Run one connected P6 cold-reopen encounter and write actual evidence."""
from __future__ import annotations

import argparse
import json
import os
import platform
import shlex
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RUN = REPO / "WORKER_RETURNS" / "SOROK-P6-ONE-LIVING-HOUSE-R1" / "run_p6.py"
INSPECT = HERE / "inspect_state.py"
FROZEN = "41b21babf72c4c8b0b4b012d3c8b7d7f6247791f"

COMMANDS = (
    ("new", ("new",)),
    ("orientation", ("view",)),
    ("Nadia works while the user waits", ("say", "I can wait while you finish that.")),
    ("room entry", ("go", "living room")),
    ("banal observation", ("look", "coaster")),
    ("sandals linked history", ("look", "sandals")),
    ("photo linked history", ("look", "photo")),
    ("return to workshop", ("go", "workshop")),
    ("revisit workshop", ("view",)),
    ("leave the mug alone", ("say", "I'll leave the mug alone for now.")),
    ("revisit living room", ("go", "living room")),
    ("final view", ("view",)),
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ledger_turns(state: Path):
    path = state / "p4_receipts.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))["turns"]


def interval_summary(interval):
    if not isinstance(interval, dict):
        return None
    segments = interval.get("segments") or [{}]
    world = segments[0].get("world") or {}
    before = world.get("state_before") or {}
    after = world.get("state_after") or {}
    return {
        "status": interval.get("status"),
        "start": interval.get("start"),
        "end": interval.get("end"),
        "reason": world.get("reason", ""),
        "actual_action_event_id": world.get("actual_action_event_id", ""),
        "material_remaining": [before.get("material_remaining"), after.get("material_remaining")],
        "free_hours": [before.get("free_hours"), after.get("free_hours")],
    }


def turn_summary(turn):
    receipt = turn["receipt"]
    summary = {
        "action": turn["action"],
        "before_clock": turn["before"]["clock"],
        "after_clock": turn["after"]["clock"],
    }
    speech = receipt.get("speech")
    if speech:
        summary["speech"] = {
            "admission": speech["admission"],
            "text": speech["attempt"]["text"],
            "request_edge": speech["attempt"]["request_edge"],
            "performed_event_id": (speech.get("performed") or {}).get("event_id"),
        }
        summary["uptake"] = {
            "status": receipt["uptake"]["status"],
            "mode": receipt["uptake"]["mode"],
        }
    performed = receipt.get("performed")
    if performed:
        summary["performed"] = {
            "kind": performed["kind"],
            "event_id": performed["event_id"],
            "summary": performed["summary"],
        }
    expression = receipt.get("expression")
    if expression:
        summary["expression"] = {
            "kind": expression["kind"],
            "event_id": expression["event_id"],
            "summary": expression["summary"],
        }
    interval = interval_summary(receipt.get("interval"))
    if interval:
        summary["interval"] = interval
    return summary


def human_result(result):
    lines = [f"clock {result.get('clock')}; room {result.get('room')}"]
    if result.get("orientation"):
        lines.append(result["orientation"])
    if "available" in result:
        lines.append("available: " + ", ".join(result["available"]))
    if result.get("detail"):
        lines.append("detail: " + result["detail"])
    for row in result.get("narration") or []:
        lines.append("  " + row["text"])
    if result.get("admission"):
        lines.append("admission: " + result["admission"])
    if result.get("invitation"):
        lines.append("invitation: " + result["invitation"])
    return lines


def human_turn(summary):
    if not summary:
        return []
    action = summary["action"]
    label = action.get("operation", "ACTION")
    if label == "SAY":
        label += f" {action.get('text', '')!r}"
    elif action.get("target"):
        label += " " + str(action["target"])
    lines = [f"receipt: {label}; clock {summary['before_clock']} -> {summary['after_clock']}"]
    if "speech" in summary:
        speech = summary["speech"]
        lines.append(
            f"  P4 speech: {speech['admission']}; request_edge={speech['request_edge']}; "
            f"text={speech['text']!r}"
        )
        lines.append(
            f"  uptake: {summary['uptake']['status']}; mode={summary['uptake']['mode']}"
        )
    if "performed" in summary:
        performed = summary["performed"]
        lines.append(f"  performed {performed['kind']}: {performed['summary']}")
    if "expression" in summary:
        expression = summary["expression"]
        lines.append(f"  expression {expression['kind']}: {expression['summary']}")
    if "interval" in summary:
        interval = summary["interval"]
        material = interval["material_remaining"]
        free = interval["free_hours"]
        lines.append(
            f"  material/time: {interval['status']} {interval['start']} -> {interval['end']}; "
            f"material {material[0]} -> {material[1]}; free_hours {free[0]} -> {free[1]}"
        )
        if interval["reason"]:
            lines.append("  interval reason: " + interval["reason"])
        if interval["actual_action_event_id"]:
            lines.append("  actual action event: " + interval["actual_action_event_id"])
    return lines


def prepare_state(value):
    if value:
        state = Path(value).resolve()
        if state.exists() and any(state.iterdir()):
            raise SystemExit(f"refusing non-empty state: {state}")
        state.mkdir(parents=True, exist_ok=True)
        return state
    scratch = Path(tempfile.gettempdir()) / "sorok-p6-cold-demo"
    scratch.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix="run-", dir=scratch))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, help="empty bounded scratch state directory")
    args = parser.parse_args()
    state = prepare_state(args.state)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    records = []
    for seq, (label, command) in enumerate(COMMANDS, 1):
        turns_before = len(ledger_turns(state))
        started = now()
        start = time.monotonic()
        process = subprocess.run(
            [sys.executable, str(RUN), "--state", str(state), *command],
            cwd=REPO, env=env, capture_output=True, text=True,
        )
        elapsed = round(time.monotonic() - start, 3)
        turns = ledger_turns(state)
        receipt = turn_summary(turns[-1]) if len(turns) > turns_before else None
        try:
            result = json.loads(process.stdout)
        except json.JSONDecodeError:
            result = None
        record = {
            "seq": seq,
            "label": label,
            "command": [sys.executable, str(RUN), "--state", str(state), *command],
            "started": started,
            "seconds": elapsed,
            "exit": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "result": result,
            "receipt": receipt,
        }
        records.append(record)
        print(f"[{seq:02d}] {label}: exit {process.returncode} in {elapsed:.2f}s")
        if process.returncode != 0 or result is None:
            print(process.stdout, end="")
            print(process.stderr, end="", file=sys.stderr)
            break

    house = None
    if records and all(row["exit"] == 0 for row in records):
        started = now()
        start = time.monotonic()
        process = subprocess.run(
            [sys.executable, str(INSPECT), "--state", str(state)],
            cwd=REPO, env=env, capture_output=True, text=True,
        )
        elapsed = round(time.monotonic() - start, 3)
        try:
            house = json.loads(process.stdout)
        except json.JSONDecodeError:
            house = None
        records.append({
            "seq": len(records) + 1,
            "label": "read-only house history evidence",
            "command": [sys.executable, str(INSPECT), "--state", str(state)],
            "started": started,
            "seconds": elapsed,
            "exit": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "result": None,
            "receipt": None,
        })
        print(f"[{len(records):02d}] house history: exit {process.returncode} in {elapsed:.2f}s")

    (HERE / "actual_run.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in records),
        encoding="utf-8",
    )
    if house is not None:
        (HERE / "house_history.json").write_text(
            json.dumps(house, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    looked = [
        row["receipt"]["action"]["target"]
        for row in records
        if row.get("receipt") and row["receipt"]["action"].get("operation") == "INSPECT_OBJECT"
    ]
    objects = sorted((house or {}).get("objects", {}))
    left_alone = [ref for ref in objects if ref not in looked]
    lines = [
        "# Actual P6 cold-reopen CLI run",
        "",
        f"- Frozen runtime: `{FROZEN}`",
        f"- Runtime path: `{RUN}`",
        f"- Started: {records[0]['started'] if records else now()}",
        f"- State: `{state}`",
        f"- CWD: `{REPO}`",
        f"- Python: `{sys.executable}` ({platform.python_version()})",
        f"- Platform: `{platform.platform()}`",
        "- Environment: `PYTHONDONTWRITEBYTECODE=1`; no source or runtime edits.",
        "- Every P6 command below is a separate OS process; each invocation validates the cold checkpoint.",
        "",
        "## Commands and actual user-visible output",
        "",
    ]
    for row in records:
        command = shlex.join(row["command"])
        lines.extend([
            f"### {row['seq']}. {row['label']}",
            "",
            f"```text",
            f"$ {command}",
            f"```",
            "",
            f"`exit {row['exit']} | {row['seconds']:.2f}s`",
            "",
        ])
        if row["result"]:
            lines.extend(human_result(row["result"]))
            lines.append("")
        if row["receipt"]:
            lines.extend(human_turn(row["receipt"]))
            lines.append("")
        if row["exit"] != 0:
            lines.append("STDOUT:")
            lines.append("```text")
            lines.append(row["stdout"].rstrip())
            lines.append("```")
            lines.append("STDERR:")
            lines.append("```text")
            lines.append(row["stderr"].rstrip())
            lines.append("```")
            lines.append("")
    lines.extend(["## House history evidence", ""])
    if house is None:
        lines.append("House history helper failed; see `actual_run.jsonl`.")
    else:
        lines.extend([
            f"Epoch: {house['epoch']}; root: `{house['root']}`",
            "",
            "```text",
        ])
        for ref, row in sorted(house["history"].items()):
            lines.append(
                f"{ref}: object={row['object']} clock={row['clock']} "
                f"depends_on={row['depends_on']}"
                + (f" depicts={row['depicts']}" if row.get("depicts") else "")
            )
        lines.extend([
            "```",
            "",
            "## Leave-alone check",
            "",
            f"Looked at: {', '.join(looked) if looked else 'none'}.",
            f"Not looked at in this encounter: {', '.join(left_alone) if left_alone else 'none'}.",
            "The explicit leave-alone choice was the final say: "
            "\"I'll leave the mug alone for now.\"",
            "",
            "## Evidence and scope",
            "",
            "- Raw command records, stdout/stderr and timings: `actual_run.jsonl`.",
            "- House history: `house_history.json`.",
            "- Scope: sourcefree, test-only, actual P6/P5/P4/P3 code and actual state receipts.",
            "- Missing handoff: recognition is a separate in-flight patch and query-order is a separate proof; neither is claimed here.",
            "- Not claimed: native science, actor authority, human acceptance, PR779 merge, protected/shared-progress edits.",
            "",
        ])
    (HERE / "TRANSCRIPT.md").write_text("\n".join(lines), encoding="utf-8")
    return 0 if records and all(row["exit"] == 0 for row in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
