"""R31J pre-C8/pre-C9 GM01 source-owned material producer."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import bp2p4.bootstrap as _bootstrap
_bootstrap.install()
from bp1.canon import digest, seal
from bp2_joined.binding import build_world_occurrence, validate_occurrence_payload
from bp2_joined.producer import JoinedProducer, _c9_summary
import historical_actor_producer as H


def prepare_life(gm01: dict, variant: str = "A_REPAIR_LONG"):
    life = H.build_life(variant)
    snapshot = deepcopy(life.a_snapshot)
    snapshot["state"] = dict(snapshot["state"])
    snapshot["state"]["tools_remaining"] = 1 if gm01.get("material_feasible_after") else 0
    snapshot["state"]["material_remaining"] = max(4, int(snapshot["state"].get("material_remaining", 4)))
    snapshot.pop("hash", None)
    snapshot["state_hash"] = digest(snapshot["state"])
    snapshot = seal(snapshot)
    return replace(life, a_snapshot=snapshot)


def gm01_source(gm01: dict, case: dict) -> dict:
    b_event = next(r for r in case["records"] if r["kind"] == "OTHER_PERFORMED")
    e1 = next(r for r in case["records"] if r["kind"] == "E1_EVENT")
    e2 = next((r for r in case["records"] if r["kind"] == "A_E2_PERFORMED"), None)
    return {
        "schema": "R31J_GM01_PRE_C9_SOURCE@1",
        "grade": "TEST_ONLY_SOURCEFREE_PRE_C9_MATERIAL",
        "b_actor": b_event["subject"],
        "b_owner": b_event["owner"],
        "b_event_ref": b_event["ref"],
        "b_event_hash": b_event["content_hash"],
        "b_performed": b_event["performed"],
        "b_operation": b_event["payload"].get("operation"),
        "b_quantity": b_event["payload"].get("quantity"),
        "b_to_actor": b_event["payload"].get("to_actor"),
        "b_clock": b_event["at"],
        "a_e1_ref": e1["ref"],
        "a_e1_hash": e1["content_hash"],
        "a_e1_clock": e1["at"],
        "a_e2_ref": e2["ref"] if e2 else "",
        "a_e2_hash": e2["content_hash"] if e2 else "",
        "a_e2_performed": bool(e2 and e2["performed"]),
        "material_feasible_after": gm01.get("material_feasible_after"),
        "gm01_result_hash": gm01.get("result_hash", ""),
        "gm01_readset": list(gm01.get("readset", [])),
        "native": False,
        "psychology_claim": False,
    }


class PreC9Producer(JoinedProducer):
    """Stable producer whose C8 occurrence binds the GM01 B source before C9."""

    def __init__(self, root, *, gm01: dict, case: dict,
                 variant: str = "A_REPAIR_LONG"):
        self.gm01 = gm01
        self.case = case
        self.historical_variant = variant
        self.historical_life = prepare_life(gm01, variant)
        self.source = gm01_source(gm01, case)
        super().__init__(root, actor="A")

    def stage_world(self):
        self.stage = "world_occurrence"
        occurrence = build_world_occurrence(self.historical_life, actor=self.actor_key)
        payload = deepcopy(occurrence.payload)
        payload["gm01_pre_c9_source"] = self.source
        payload["world"]["material_ref"] = "TEST_ONLY_R31J_GM01_MATERIAL_" + self.source["b_event_hash"][:16]
        payload["world"]["material_receipt_id"] = self.source["b_event_hash"]
        validate_occurrence_payload(payload)
        candidate = dict(occurrence.candidate)
        candidate["payload"] = payload
        candidate["candidate_id"] = "BP2-OCC-" + digest(payload)[:24].upper()
        occurrence = replace(
            occurrence,
            payload=payload,
            candidate=candidate,
            material_ref=payload["world"]["material_ref"],
            material_receipt_id=self.source["b_event_hash"],
        )
        self.occurrence = occurrence
        self.clock["value"] = occurrence.event_time
        return occurrence

    def run_without_e2(self):
        self.stage_world()
        self.stage_c8()
        self.stage_out9()
        access = "granted" if self.gm01.get("material_feasible_after") else "denied"
        self.stage_c9(material_access=access)
        return {
            "ok": True,
            "stage_reached": "c9_commit",
            "c8_state_digest": self.out9.readset["state_digest"],
            "c8_content_hash": self.out9.event.get("content_hash"),
            "e1_event_hash": self.e1_event["hash"],
            "c9": _c9_summary(self, self.pipeline),
            "gm01_source": self.source,
            "material_access": access,
        }

    def run_share_e2(self):
        return self.run()
