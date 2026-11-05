#!/usr/bin/env python3
"""Real subprocess probes for journal CAS, cold replay and interrupted state writes."""
from __future__ import annotations

import copy
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
        # Actual concurrent commit_event state writers, not only journal appends.
        commit_root = root / "commit"
        commit_journal = commit_root / "evidence" / "journal.jsonl"
        commit_state = commit_root / "state.json"
        lr.commit_event(lr._event("GENESIS", {"baseline_sha": lr.ENGINEERING_BASELINE}, created_at="2026-11-01T19:01:00+00:00"), journal_path=commit_journal, state_path=commit_state)
        fixtures = []
        for index, node_id in enumerate(("CP-A5-R2", "B-F1CR-R2")):
            fixture_path = commit_root / f"fixture_{index}.json"
            fixture_path.write_text(json.dumps({
                "node_id": node_id, "dimension": "engineering", "to": "CANDIDATE_UPGRADED",
                "evidence": {"kind": "SYNTHETIC_DEMO", "note": f"probe-{index}"},
            }), encoding="utf-8")
            fixtures.append(fixture_path)
        writers = [
            subprocess.Popen(
                [sys.executable, "living_reference.py", "--state", str(commit_state), "apply-authorized-transition", str(path)],
                cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for path in fixtures
        ]
        writer_output = [process.communicate(timeout=60) for process in writers]
        commit_events = evidence_store.read_journal(commit_journal)
        live = lr._load_state(commit_state)
        replay = lr.rebuild_from_journal(commit_journal, operating=True)
        concurrent_commit = {
            "exit_codes": [process.returncode for process in writers],
            "stderr": [item[1] for item in writer_output],
            "events": len(commit_events),
            "revision": live.get("revision"),
            "head_matches": live.get("journal_head") == commit_events[-1]["event_id"],
            "state_digest_equal": live.get("state_digest") == replay.get("state_digest"),
        }
        # A complete valid-prefix tail loss must be refused, not silently accepted.
        before = commit_state.read_bytes()
        lines = commit_journal.read_text(encoding="utf-8").splitlines()
        commit_journal.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
        tail_refusal = None
        try:
            lr._load_state(commit_state)
        except evidence_store.JournalRegression as error:
            tail_refusal = str(error)
        tail_unchanged = commit_state.read_bytes() == before
        journal_before = commit_journal.read_bytes()
        commit_tail_refusal = None
        try:
            lr.commit_event(lr._event("QUARANTINE", {"excluded_history_ids": ["PROBE_TAIL"]}), journal_path=commit_journal, state_path=commit_state)
        except evidence_store.JournalRegression as error:
            commit_tail_refusal = str(error)
        journal_unchanged = commit_journal.read_bytes() == journal_before
        recovered_tail = lr._load_state(commit_state, recover=True)
        complete_tail = {
            "refused": tail_refusal,
            "newer_state_unchanged": tail_unchanged,
            "commit_event_refused": commit_tail_refusal,
            "journal_unchanged": journal_unchanged,
            "explicit_recovery": recovered_tail.get("journal_regression_recovery", {}).get("status"),
            "recovery_revision": recovered_tail.get("revision"),
        }
        # A changed patch must not replay under its former declared digest.
        patch = lr._load(lr.OSCIENCE_PATCH)
        original_digest = lr._digest(patch)
        tampered = copy.deepcopy(patch)
        tampered["workstream_evidence_upserts"][0]["domains"] = ["TAMPERED"]
        patch_tamper = None
        try:
            lr.ingest_oscience(lr.build_state(lr.observe_source_cut(git_enabled=False)), tampered, patch_digest=original_digest)
        except ValueError as error:
            patch_tamper = str(error)
        result = {
            "schema": "SOROK_PROGRAMMA_FAULT_PROBE@1",
            "concurrent_stale_cas": concurrent,
            "interrupted_state_write": interrupted,
            "cold_reload": {"exit_code": cold.returncode, "state_digest_equal": cold_state.get("state_digest") == digest},
            "concurrent_commit_event": concurrent_commit,
            "complete_tail_loss": complete_tail,
            "patch_tamper": patch_tamper,
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        passed = (
            concurrent["events_after"] == 3 and interrupted["recovered"] and cold.returncode == 0
            and concurrent_commit["exit_codes"] == [0, 0]
            and concurrent_commit["events"] == 3
            and concurrent_commit["revision"] == 3
            and concurrent_commit["head_matches"]
            and concurrent_commit["state_digest_equal"]
            and tail_refusal is not None and tail_unchanged
            and commit_tail_refusal is not None and journal_unchanged
            and complete_tail["explicit_recovery"] == "EXPLICIT_RECOVERY_FROM_SHORTER_JOURNAL"
            and patch_tamper is not None
        )
        return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
