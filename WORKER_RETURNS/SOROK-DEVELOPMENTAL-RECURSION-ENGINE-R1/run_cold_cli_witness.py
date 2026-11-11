"""Reproduce two actual P2 batches through three cold CLI invocations."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from developmental_recursion.contracts import EventProposal
from developmental_recursion.engine import BatchEngine
from developmental_recursion.p2_owner import P2Owner, load_p2

RETURN = Path(__file__).resolve().parent


def run(output_path: Path):
    with tempfile.TemporaryDirectory(prefix="sorok-recursion-cli-") as td:
        tmp = Path(td)
        state = tmp / "person"
        fanin = load_p2().start(state)
        case = fanin.deps["case_for"](True)
        pack = {"case": case, "source": fanin.deps["source_for"](case),
                "participants": tuple(fanin.session.read_root()["actor_ids"])}
        owner = P2Owner(fanin, **pack)
        source_ref = owner.source_ref
        before = owner.snapshot()
        owner.close()
        (tmp / "pack.json").write_text(json.dumps(pack))
        previous = None
        previous_experiences = None
        outputs = []
        requests = []
        for sequence, mode in enumerate(("bootstrap", "advance", "finish"), 1):
            retro = None
            if previous is not None:
                retro = {"batch_id": previous["batch_id"],
                         "history_hash": previous["history_hash"],
                         "event_ids": [row["event_id"] for row in previous["events"]],
                         "impressions": [{"grade": "RENDER_PROPOSAL_ONLY"}]}
            proposals = None
            if mode != "finish":
                cold = P2Owner(load_p2().open(state), **pack)
                now = cold.snapshot().clock
                cold.close()
                proposals = [EventProposal(
                    f"cli-{sequence}-{index}", now + 6 * (index + 1),
                    "ADMIT_EVENT", (source_ref,), tuple(pack["participants"]), {},
                    {"mode": "ACTUAL" if sequence == 1 else "SCHEDULED_ONLY", "span": 4}
                    if index == 0 else None,
                ).document() for index in range(3)]
            (tmp / "response.json").write_text(json.dumps({
                "retrospective": retro, "prospective": proposals,
            }))
            request_path = tmp / f"request-{sequence}.json"
            command = [sys.executable, "-B", str(RETURN / "run_developmental_recursion.py"),
                       mode, "--state-root", str(state), "--source-pack", str(tmp / "pack.json"),
                       "--journal", str(tmp / "journal.sqlite"),
                       "--cycle-store", str(tmp / "cycle.json"),
                       "--model-response", str(tmp / "response.json"),
                       "--model-request-out", str(request_path)]
            child = subprocess.run(command, capture_output=True, text=True, timeout=240,
                                   env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
            if child.returncode:
                raise RuntimeError(child.stderr)
            result = json.loads(child.stdout)
            request = json.loads(request_path.read_text())
            expected_mode = {"bootstrap": "BOOTSTRAP", "advance": "ORDINARY",
                             "finish": "TERMINAL"}[mode]
            assert request["mode"] == expected_mode
            if previous is not None:
                assert request["previous"]["events"] == previous_experiences
            assert "records" not in result
            assert "root_hash" not in json.dumps(result)
            assert "body_public" not in json.dumps(result)
            assert "actor_ref" not in json.dumps(result)
            assert "objective" not in json.dumps(request["previous"])
            outputs.append(result)
            requests.append(request)
            if mode != "finish":
                assert len(result["events"]) == 3
                previous = result
                cold = P2Owner(load_p2().open(state), **pack)
                engine = BatchEngine(cold, tmp / "journal.sqlite")
                try:
                    history = engine.history(result["batch_id"])
                    previous_experiences = [
                        {"event_id": row["event_id"], "accessible": row["accessible"]}
                        for row in history["records"]
                    ]
                    assert all(row["accessible"]["status"] == "OBSERVED"
                               for row in previous_experiences)
                finally:
                    engine.close()
                    cold.close()
        cold = P2Owner(load_p2().open(state), **pack)
        after = cold.snapshot()
        assert after.root == before.root
        assert after.clock > before.clock
        assert cold.fanin.session.verify()["ok"] is True
        cycle = json.loads((tmp / "cycle.json").read_text())
        assert cycle["phase"] == "COMPLETE"
        assert len(cycle["retrospectives"]) == 2
        cold.close()
        receipt = {"grade": "TEST_ONLY_ACTUAL_P2_OWNER_WITH_FILE_MODEL_TRANSPORT",
                   "commands": [row["command"] for row in outputs],
                   "model_modes": [row["mode"] for row in requests],
                   "batch_event_counts": [len(row["events"]) for row in outputs],
                   "retrospective_count": len(cycle["retrospectives"]),
                   "same_root": after.root == before.root,
                   "before_clock": before.clock, "after_clock": after.clock,
                   "cold_verified": True, "provider_calls_between_events": 0,
                   "retrospective_uses_developing_actor_perceptions": True,
                   "default_output_omits_actor_private_experience": True,
                   "native_psychological_transitions": "MISSING_RULE"}
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(receipt, indent=2) + "\n")
        return receipt


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else RETURN / "evidence/cold_cli.json"
    print(json.dumps(run(target), indent=2))
