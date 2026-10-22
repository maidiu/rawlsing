"""R31J observable over the pre-C9 source-bound product."""
from __future__ import annotations

from r31j.build import product


def observable(root, *, gm01, case, perform="e2", need_e2=True):
    product_obj, built, producer = product(
        root, gm01=gm01, case=case, need_e2=need_e2, perform=perform)
    try:
        a0 = product_obj.observe_verified()
        before = a0["self"]["state"]
        if perform == "e2":
            action = product_obj.material_inspect()
        else:
            action = product_obj.record_omission()
        waited = product_obj.wait(30)
        other = product_obj.other()
        state = product_obj.store.latest_state(product_obj.branch_id)
        after = state["world"]["actor_state"]["A"]
        episodes = product_obj.store.episodes(product_obj.branch_id)
        source_episode = next(e for e in episodes if e["kind"] == "GM01_SOURCE")
        return {
            "status": a0.get("status"),
            "claims": [claim["kind"] for claim in a0.get("claims", [])],
            "others": [row["actor"] for row in a0.get("others_present", [])],
            "tools_before": before.get("tools_remaining"),
            "material_before": before.get("material_remaining"),
            "completed_before": before.get("completed_units"),
            "action": action,
            "tools_after": after.get("tools_remaining"),
            "material_after": after.get("material_remaining"),
            "completed_after": after.get("completed_units"),
            "a2_clock": waited.get("clock"),
            "a2_offscreen": [
                product_obj.store.world_event(product_obj.branch_id, event_id)["kind"]
                for event_id in waited.get("offscreen_events", [])],
            "a2_other_units": other["public"]["completed_units"],
            "c8_state_digest": a0.get("c8", {}).get("state_digest"),
            "e1_target": a0.get("c9", {}).get("target_id"),
            "c12_verify": a0.get("c12_verify", {}),
            "source_episode": source_episode,
            "c9_target_id": built["target_id"],
            "c8_pre_c9_digest": built["c8_state_digest"],
            "e1_pre_c9_hash": built["e1_event_hash"],
            "producer": built["receipt"],
            "product_binding": product_obj.pre_c9_binding,
            "c12_world_hash": state["world"]["hash"],
            "episodes": [e["kind"] for e in episodes],
        }
    finally:
        product_obj.close()
        producer.close()
