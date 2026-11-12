"""Cold restart between owner-held formation and a later distinct decision."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
ENGINE_ROOT = ROOT / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P3_ROOT = ROOT / "WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
for _path in (str(ENGINE_ROOT), str(P3_ROOT), str(P3_ROOT / "tests")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from developmental_recursion.engine import BatchEngine  # noqa: E402
from developmental_recursion.model_cycle import RecursionCycle  # noqa: E402
from p3_fixture_support import (  # noqa: E402
    COUNTERPART, PROJECT, batch_events, build_case, reopen_owner,
)


def response_for(result: dict) -> dict:
    return result["consequences"]["test_only_psychological"]


def test_cold_restart_then_later_recruit_reads_owner_held_formation(tmp_path):
    case = build_case(tmp_path)
    first = case.cycle.bootstrap(context={"fixture": "cold-bootstrap"})
    formation = batch_events(first)[0]
    formed = case.owner.store.query(
        project=PROJECT, counterpart=COUNTERPART, as_of=formation["after"]["clock"])
    assert len(formed) == 2
    formed_hashes = {row["hash"] for row in formed}
    assert response_for(formation)["status"] == "COMPUTED_TEST_ONLY_RESPONSE"
    case.owner.close()

    base, owner = reopen_owner(case)
    try:
        engine = BatchEngine(owner, case.journal_path)
        cycle = RecursionCycle(engine, case.provider, case.cycle_store_path)
        second = cycle.advance(context={"fixture": "cold-ordinary"})
        recruit = batch_events(second)[1]
        response = response_for(recruit)
        stream_hashes = {
            row["record_hash"] for row in response["streams"] if row.get("record_hash")
        }
        assert stream_hashes == formed_hashes
        assert set(recruit["readset"]) & formed_hashes
        assert response["native_action"] == "NOT_ISSUED_BY_P3_RULE"
        final = cycle.finish(context={"fixture": "cold-terminal"})
        assert final["batch_id"] == second["batch_id"]
        assert owner.store.head()["count"] == 2
    finally:
        owner.close()
