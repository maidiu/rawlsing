"""Hard-process-crash custody reproduction for the batch engine.

The child process receives a real owner receipt, then calls ``os._exit`` before
the engine can record the event.  The parent verifies the durable reservation,
then a new process resumes the same operation.  This is evidence only; it is
not production code and it supplies no developmental science.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from developmental_recursion.contracts import (  # noqa: E402
    EventProposal,
    RealizedEvent,
    RecursionRefusal,
    StateIdentity,
    digest,
)
from developmental_recursion.engine import BatchEngine  # noqa: E402


class DurableOwner:
    """A file-backed owner with real receipts, used only by this evidence run."""

    def __init__(self, directory: Path):
        self.path = directory / "owner.json"
        if not self.path.is_file():
            self._write(
                {
                    "root": "evidence-root",
                    "actor": "evidence-actor",
                    "branch": "evidence-branch",
                    "clock": 0,
                    "order": [],
                    "receipts": {},
                    "pending": {},
                    "crashed": False,
                }
            )

    def _read(self) -> dict:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, state: dict) -> None:
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(state, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
        os.replace(temporary, self.path)

    def snapshot(self) -> StateIdentity:
        state = self._read()
        return StateIdentity(
            state["root"],
            state["actor"],
            state["branch"],
            state["clock"],
            digest({"order": state["order"], "clock": state["clock"]}),
        )

    def validate_proposal(self, proposal: EventProposal) -> None:
        state = self._read()
        if proposal.event_id in state["pending"]:
            raise RecursionRefusal("AMBIGUOUS_PRIOR_OPERATION_HOLD")
        if proposal.operation != "ACT":
            raise RecursionRefusal("EVIDENCE_OPERATION_NOT_AUTHORIZED")
        if proposal.event_time <= state["clock"]:
            raise RecursionRefusal("EVIDENCE_EVENT_CLOCK_NOT_FUTURE")

    def _result_from_document(self, document: dict) -> RealizedEvent:
        return RealizedEvent(
            operation_id=document["operation_id"],
            proposal_hash=document["proposal_hash"],
            before=StateIdentity(**document["before"]),
            after=StateIdentity(**document["after"]),
            status=document["status"],
            objective=document["objective"],
            accessible=document["accessible"],
            consequences=document["consequences"],
            readset=tuple(document["readset"]),
            receipt_ref=document["receipt_ref"],
        )

    def realize(
        self,
        operation_id: str,
        proposal: EventProposal,
        expected: StateIdentity,
    ) -> RealizedEvent:
        state = self._read()
        if operation_id in state["receipts"]:
            result = self._result_from_document(state["receipts"][operation_id])
            if result.proposal_hash != digest(proposal.document()):
                raise RecursionRefusal("EVIDENCE_OPERATION_REUSE_MISMATCH")
            if result.before != expected:
                raise RecursionRefusal("EVIDENCE_OPERATION_BEFORE_MISMATCH")
            if self.snapshot() != result.after:
                raise RecursionRefusal("EVIDENCE_OPERATION_STATE_MISMATCH")
            return result
        if operation_id in state["pending"]:
            raise RecursionRefusal("AMBIGUOUS_PRIOR_OPERATION_HOLD")
        if self.snapshot() != expected:
            raise RecursionRefusal("EVIDENCE_STALE_STATE")
        if os.environ.get("SOROK_SLOW_EVENT") == proposal.event_id:
            import time

            time.sleep(0.5)

        before = expected
        prior = list(state["order"])
        state["order"].append(proposal.event_id)
        state["clock"] = proposal.event_time
        after = StateIdentity(
            state["root"],
            state["actor"],
            state["branch"],
            state["clock"],
            digest({"order": state["order"], "clock": state["clock"]}),
        )
        result = RealizedEvent(
            operation_id=operation_id,
            proposal_hash=digest(proposal.document()),
            before=before,
            after=after,
            status="REALIZED",
            objective={"event_id": proposal.event_id, "prior_order": prior},
            accessible={"event_id": proposal.event_id, "accessible": True},
            consequences={
                "event_id": proposal.event_id,
                "durable_psychological_transition": "MISSING_RULE",
            },
            readset=tuple(proposal.source_refs),
            receipt_ref="file:" + operation_id,
        )
        state["receipts"][operation_id] = result.document()
        self._write(state)

        if os.environ.get("SOROK_CRASH_AFTER_RECEIPT") == proposal.event_id:
            state["crashed"] = True
            self._write(state)
            os._exit(17)
        return result


def proposals() -> list[EventProposal]:
    return make_proposals("e", 1)


def make_proposals(prefix: str, start: int) -> list[EventProposal]:
    return [
        EventProposal(
            f"{prefix}{index}", start + index - 1, "ACT", ("evidence-source",),
            ("evidence-actor",), {"batch": "hard-crash-evidence"},
        )
        for index in (1, 2, 3)
    ]


def child(mode: str) -> None:
    root = Path(os.environ["SOROK_CRASH_STATE"])
    journal = root / "journal.sqlite"
    owner = DurableOwner(root)
    engine = BatchEngine(owner, journal)
    batch = proposals()
    if mode == "crash":
        engine.run_batch("batch", batch)
        raise SystemExit("owner did not simulate a crash")
    result = engine.run_batch("batch", batch)
    assert len(result["records"]) == 3
    assert owner.snapshot().clock == 3
    history = engine.history("batch")
    assert history == result
    assert engine.verify() is True
    print(
        json.dumps(
            {
                "mode": mode,
                "history_hash": result["history_hash"],
                "event_ids": [record["event_id"] for record in result["records"]],
                "statuses": [record["status"] for record in result["records"]],
                "scientific_consequences": [
                    record["consequences"]["durable_psychological_transition"]
                    for record in result["records"]
                ],
            },
            sort_keys=True,
        )
    )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="sorok-engine-hard-crash-") as directory:
        root = Path(directory)
        environment = dict(os.environ)
        environment["SOROK_CRASH_STATE"] = str(root)
        environment["SOROK_CRASH_AFTER_RECEIPT"] = "e1"
        crash = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "crash"],
            env=environment,
            capture_output=True,
            text=True,
        )
        if crash.returncode != 17:
            raise SystemExit(
                "expected hard exit 17, got "
                + str(crash.returncode)
                + "\nstdout="
                + crash.stdout
                + "\nstderr="
                + crash.stderr
            )

        connection = sqlite3.connect(root / "journal.sqlite")
        try:
            batch = connection.execute(
                "SELECT status FROM batches WHERE batch_id='batch'"
            ).fetchone()
            reservation = connection.execute(
                "SELECT status, result_json, record_json FROM events "
                "WHERE batch_id='batch' AND event_index=0"
            ).fetchone()
        finally:
            connection.close()
        assert batch == ("RUNNING",), batch
        assert reservation == ("RESERVED", None, None), reservation

        clean_environment = dict(os.environ)
        clean_environment["SOROK_CRASH_STATE"] = str(root)
        clean_environment.pop("SOROK_CRASH_AFTER_RECEIPT", None)
        recovery = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "recover"],
            env=clean_environment,
            capture_output=True,
            text=True,
            check=True,
        )
        verification = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "verify"],
            env=clean_environment,
            capture_output=True,
            text=True,
            check=True,
        )
        recovered = json.loads(recovery.stdout)
        assert recovered["event_ids"] == ["e1", "e2", "e3"]
        assert recovered["statuses"] == ["REALIZED", "REALIZED", "REALIZED"]
        assert recovered["scientific_consequences"] == ["MISSING_RULE"] * 3
        print(
            json.dumps(
                {
                    "hard_crash_exit": crash.returncode,
                    "batch_after_crash": batch[0],
                    "reservation_after_crash": reservation[0],
                    "recorded_result_after_crash": reservation[1],
                    "recovery": recovered,
                    "verification": json.loads(verification.stdout)["mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in {"crash", "recover", "verify"}:
        child(sys.argv[1])
    else:
        main()
