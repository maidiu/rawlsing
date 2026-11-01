#!/usr/bin/env python3
"""Real subprocess probes for journal CAS, cold replay and interrupted state writes."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import evidence_store
import living_reference as lr

ROOT = Path(__file__).resolve().parent


def append_process(journal: Path, kind: str, marker: int, expected_head: str) -> subprocess.Popen:
    code = (
        "import json,sys,evidence_store\n"
        "journal=sys.argv[1]; kind=sys.argv[2]; marker=int(sys.argv[3]); expected=sys.argv[4]\n"
        "body={'kind':kind,'created_at':'2026-11-01T19:00:0%d+00:00'%marker,"
        "'actor':{'principal':'probe-%d'%marker,'role':'PROBE','verified':False},"
        "'source':{},'payload':{'marker':marker}}\n"
        "print(json.dumps(evidence_store.append_event(journal, body, expected_head=expected)))\n"
    )
    return subprocess.Popen([sys.executable, "-c", code, str(journal), kind, str(marker), expected_head], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="sorok-fault-probe-") as directory:
        root = Path(directory)
        journal = root / "evidence" / "journal.jsonl"
        state_path = root / "state.json"
        genesis = lr._event("GENESIS", {"baseline_sha": lr.STARTUP_SHA}, created_at="2026-11-01T19:00:00+00:00")
        evidence_store.append_event(journal, genesis)
        head = evidence_store.journal_head(journal)
        p1 = append_process(journal, "QUARANTINE", 1, head)
        p2 = append_process(journal, "CANDIDATE_EVIDENCE", 2, head)
        out1, err1 = p1.communicate(timeout=30)
        out2, err2 = p2.communicate(timeout=30)
        events = evidence_store.read_journal(journal)
        concurrent = {
            "exit_codes": [p1.returncode, p2.returncode],
            "events_after": len(events),
            "stale_flags": [json.loads(out1).get("stale_expected_head"), json.loads(out2).get("stale_expected_head")],
            "markers": [e.get("payload", {}).get("marker") for e in events if e.get("kind") != "GENESIS"],
            "stderr": [err1, err2],
        }
        state = lr.rebuild_from_journal(journal, operating=True)
        lr._save(state, state_path, revision=int(state.get("revision") or 0))
        digest = state["state_digest"]
        state_path.write_text('{"interrupted":', encoding="utf-8")
        recovered = lr._load_state(state_path, recover=True)
        interrupted = {
            "recovered": recovered["state_digest"] == digest,
            "revision": recovered.get("revision"),
            "journal_head": recovered.get("journal_head"),
        }
        cold = subprocess.run(
            [sys.executable, "living_reference.py", "--state", str(state_path), "export"],
            cwd=ROOT, capture_output=True, text=True,
        )
        cold_state = json.loads(cold.stdout) if cold.returncode == 0 else {}
        result = {
            "schema": "SOROK_PROGRAMMA_FAULT_PROBE@1",
            "concurrent_stale_cas": concurrent,
            "interrupted_state_write": interrupted,
            "cold_reload": {"exit_code": cold.returncode, "state_digest_equal": cold_state.get("state_digest") == digest},
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if concurrent["events_after"] == 3 and interrupted["recovered"] and cold.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
