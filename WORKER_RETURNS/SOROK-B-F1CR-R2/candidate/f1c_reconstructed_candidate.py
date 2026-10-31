"""F1C TEST_ONLY intervention receiver. No native actor/rule/source grant.

Run with the exact R31J return extracted at sibling runtime/. The final report
embeds this file so only the five commissioned report artifacts need committing.
"""
from __future__ import annotations

import copy
import dataclasses
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types

HERE = Path(__file__).resolve().parent
RT = HERE / "runtime"
sys.path[:0] = [str(RT / "candidate"), str(RT)]
import historical_actor_producer as H
from bp1.canon import digest
from bp2_joined.producer import JoinedProducer
from bp2_joined.binding import validate_occurrence_payload
from bp2p4 import reunion as R
from bp2p4.c12_verify import verify_branch_chain as old_verify
from r31j.pre_c9 import PreC9Producer
from r31j.product import R31JProduct
from r31j.assertion import p01

R31J = "64fec28c374d8f77fb0b412d0c934d798ede03e8"
F2_BLOB = "c1699c8da5e944ed079708e272c3af50d5a30a44"
GRADE = "TEST_ONLY_COUNTERFACTUAL_INTERVENTION_NOT_NATIVE_B"
ASSERTION = "f1c.same_receiver_assertion -> r31j.assertion.p01 (unchanged)"


class Hold(AssertionError):
    pass


def require(condition, code):
    if not condition:
        raise Hold(code)


def freeze():
    life = H.build_life("A_REPAIR_LONG")
    # Retain BOTH complete ledgers and all shared causal parents. These are
    # inherited TEST_ONLY biographies, never a source of natural B autonomy.
    prior = {
        "A": {"snapshot": life.a_snapshot,
              "events": [dataclasses.asdict(e) for e in life.a_ledger.events]},
        "B": {"snapshot": life.b_snapshot,
              "events": [dataclasses.asdict(e) for e in life.b_ledger.events]},
        "shared": {"material": life.material, "witness": life.witness,
                   "objective": life.objective},
    }
    # History ends at 241. A new, explicit laboratory custody condition at 242
    # places ONE focal tool with B. It does not rewrite either actor's earlier
    # tools_remaining or assert that the old history proves absence of skill.
    world = {
        "grade": GRADE, "valid_time": {"domain": "F1C_FIXTURE_WORLD", "tick": 242},
        "parents": [digest(prior["A"]), digest(prior["B"]), digest(prior["shared"])],
        "custody_condition": "TEST_ONLY_RETURN_OF_SHARED_TASK_TOOL_TO_B_AT_242",
        "tool_id": "TEST_ONLY_F1C_FOCAL_TOOL_1", "tool_holder": "B", "tool_owner": "B",
        "household_relation": "UNKNOWN_NOT_IN_SOURCE",
        "material_units": {"A": life.a_snapshot["state"]["material_remaining"],
                           "B": life.b_snapshot["state"]["material_remaining"]},
        "exclusive_holdings": {"A": 0, "B": 1, "spent": 0},
        "transfer_right": {"holder": "B", "scope": "TEST_ONLY_LAB_TRANSFER",
                           "native_grant": False, "signature": None},
        "B_free_hours": life.b_snapshot["state"]["free_hours"],
        "B_competing_commitment": "scheduled_finishing_ledger_discipline",
        "B_transfer_cost_hours": 1, "encumbered": False,
    }
    frozen = {"prior": copy.deepcopy(prior), "world": world}
    return life, frozen, digest(frozen)


def intervene(frozen, action, *, observed=True, cut_source=False,
              no_resource=False, encumbered=False, duplicate=False, native=False):
    require(not native, "NATIVE_B_GRANT_ABSENT")
    w = copy.deepcopy(frozen["world"])
    if no_resource:
        w["exclusive_holdings"]["B"] = 0
    if encumbered:
        w["encumbered"] = True
    # These hostile altered-source variants are openly distinct W inputs, not
    # claimed to be part of the fixed-world SHARE/REFUSE intervention contrast.
    post = copy.deepcopy(w)
    performed = action in ("SHARE", "REFUSE")
    record = {
        "grade": GRADE, "native": False, "action": action,
        "kind": "TEST_ONLY_INTERVENTION" if performed else "NON_EVENT_CONDITION",
        "performer": "B" if performed else None,
        "issuer": "TEST_ONLY_F1C_LAB_OPERATOR", "signature": None,
        "world_before_hash": digest(w), "frozen_parent_hash": digest(frozen),
        "valid": {"domain": "F1C_FIXTURE_WORLD", "tick": 250},
        "observed": {"domain": "F1C_FIXTURE_WORLD", "tick": 251},
        "A_event_access": observed and performed and not cut_source,
        "A_tool_access": action == "SHARE", "A_B_motive": "UNKNOWN",
    }
    if action == "SHARE":
        require(w["exclusive_holdings"]["B"] == 1, "B_HAS_NO_TRANSFERABLE_TOOL")
        require(not w["encumbered"], "B_TOOL_TRANSFER_RIGHT_DENIED")
        require(w["B_free_hours"] >= 1, "B_COMPETING_COMMITMENT_NO_CAPACITY")
        post["exclusive_holdings"] = {"A": 1, "B": 0, "spent": 0}
        post["tool_holder"] = "A"
        post["tool_owner"] = "A"
        post["B_free_hours"] -= w["B_transfer_cost_hours"]
    if duplicate:
        post["exclusive_holdings"]["B"] = 1
    require(sum(post["exclusive_holdings"].values()) == 1,
            "FOCAL_TOOL_CONSERVATION_FAILED")
    require(post["exclusive_holdings"]["A"] + post["exclusive_holdings"]["B"] == 1,
            "FOCAL_TOOL_CUSTODY_FAILED")
    record["world_after_hash"] = digest(post)
    record["receipt_hash"] = digest(record)
    return w, post, None if cut_source else record, record


class Receiver(PreC9Producer):
    """Isolated subclass; never calls retroactive prepare_life or rewrites it."""
    def __init__(self, root, life, frozen, post, source):
        self.historical_life = life
        self.frozen, self.post, self.intervention_source = frozen, post, source
        share = post["exclusive_holdings"]["A"] == 1
        # These are scoped compatibility fields for the original receiver.
        # They assert a laboratory intervention only; never a native owner.
        self.source = {
            "schema": "F1C_TEST_ONLY_R31J_RECEIVER_SOURCE@1", "grade": GRADE,
            "b_actor": life.b_source.actor_id, "b_owner": "TEST_ONLY_F1C_LAB_OPERATOR",
            "b_event_ref": "TEST_ONLY_F1C_INTERVENTION_250",
            "b_event_hash": (source or {}).get("receipt_hash", ""),
            "b_performed": bool(source and source["performer"]),
            "b_operation": "SHARE_TOOL" if share else ("REFUSE_TOOL" if source and source["action"] == "REFUSE" else ""),
            "b_quantity": int(share), "b_to_actor": life.a_source.actor_id,
            "material_feasible_after": share, "native": False,
            "psychology_claim": False,
            "gm01_result_hash": digest({"post": post, "source": source}),
        }
        self.gm01 = {"material_feasible_after": share}
        JoinedProducer.__init__(self, root, actor="A")

    def stage_world(self):
        occurrence = super().stage_world()
        payload = copy.deepcopy(occurrence.payload)
        payload["f1c_material_ledger"] = self.post
        payload["f1c_frozen_root"] = digest(self.frozen)
        if self.intervention_source is None:
            # A B-only source severance: preserve the physical resource transfer,
            # baselines and B cost, but withhold the B-specific source from C8.
            payload.pop("gm01_pre_c9_source", None)
        else:
            payload["f1c_test_intervention"] = self.intervention_source
        validate_occurrence_payload(payload)
        candidate = dict(occurrence.candidate, payload=payload,
                         candidate_id="BP2-OCC-" + digest(payload)[:24].upper())
        self.occurrence = dataclasses.replace(occurrence, payload=payload, candidate=candidate)
        return self.occurrence

    def stage_c9(self, **kwargs):
        kwargs["material_access"] = "granted" if self.post["exclusive_holdings"]["A"] else "denied"
        return JoinedProducer.stage_c9(self, **kwargs)


def assemble(producer, outcome):
    persisted = outcome.receipts["persisted"]
    env = producer.env
    paths = {"journal_path": Path(persisted["journal_path"]),
             "key_path": env.key_path, "key_id": env.key_store.key_id,
             "anchor_log": env.anchor.log_path, "anchor_watermark": env.anchor.watermark_path,
             "c9_path": Path(persisted["c9_db_path"])}
    return R._assemble(mode="FRESH", root=producer.root, life=producer.historical_life,
                       persisted=persisted, paths=paths, receipt={"persisted": persisted}, e2=None)


def load_f2():
    # Exact independently reviewed verifier, used as an add-on, not overlaid on
    # or adopted into the inherited source. Its raw-SQLite/anchor limits remain.
    data = subprocess.check_output(["git", "cat-file", "blob", F2_BLOB])
    import hashlib
    require(hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() == F2_BLOB,
            "F2_VERIFIER_BLOB_MISMATCH")
    module = types.ModuleType("bp2p4.f1c_f2_addon")
    module.__package__ = "bp2p4"
    exec(compile(data, "git-blob:" + F2_BLOB, "exec"), module.__dict__)
    return module


def live_prior(life):
    return {
        "A": {"snapshot": life.a_snapshot,
              "events": [dataclasses.asdict(e) for e in life.a_ledger.events]},
        "B": {"snapshot": life.b_snapshot,
              "events": [dataclasses.asdict(e) for e in life.b_ledger.events]},
        "shared": {"material": life.material, "witness": life.witness,
                   "objective": life.objective},
    }


def same_receiver_assertion(root, life, frozen, expected_hash, action="SHARE", *,
                            observed=True, cut_source=False, omit_e2=False,
                            no_resource=False, encumbered=False, duplicate=False,
                            native=False):
    require(digest(frozen) == expected_hash, "A_B_OR_SHARED_PREHISTORY_CHANGED")
    live = live_prior(life)
    require(digest(live["A"]) == digest(frozen["prior"]["A"]),
            "LIVE_A_HISTORY_CHANGED")
    require(digest(live["B"]) == digest(frozen["prior"]["B"]),
            "LIVE_B_HISTORY_CHANGED")
    require(digest(live["shared"]) == digest(frozen["prior"]["shared"]),
            "LIVE_SHARED_HISTORY_CHANGED")
    require(life.a_snapshot == frozen["prior"]["A"]["snapshot"], "A_BASELINE_CHANGED_AFTER_B")
    require(life.b_snapshot == frozen["prior"]["B"]["snapshot"], "B_BASELINE_CHANGED_AFTER_B")
    before, post, source, lab_record = intervene(
        frozen, action, observed=observed, cut_source=cut_source,
        no_resource=no_resource, encumbered=encumbered, duplicate=duplicate, native=native)
    producer = Receiver(root / "bp2", life, frozen, post, source)
    product = None
    try:
        outcome = producer.run()
        if not outcome.ok:
            error = Hold("C9_RECEIVER_HOLD:" + outcome.stage_reached + ":" + outcome.failure_code)
            error.source_context = {"world_before_hash": digest(before), "world_after": post,
                                    "test_intervention": lab_record,
                                    "frozen_baseline_hash": expected_hash,
                                    "C9_target_id": (outcome.receipts.get("persisted") or {}).get("target_id", ""),
                                    "performed_A_E2": False,
                                    "final_p01_execution": "NOT_RUN_TARGETLESS_CONSTRUCTION_HOLD"}
            raise error
        artifacts = assemble(producer, outcome)
        # First actual consumer reads source from VERIFIED committed C8 bytes,
        # not from the caller's lab record or an unchanged cached SHARE value.
        admitted_source = producer.out9.event["payload"].get("gm01_pre_c9_source", {})
        product = R31JProduct(root / "product", artifacts=artifacts,
                             source=admitted_source,
                             c8_state_digest=artifacts.c8_state_digest,
                             e1_event_hash=artifacts.e1_event_hash,
                             target_id=artifacts.target_id)
        world = product._world("root")
        # Post-event projection only. Historical snapshots and ledgers stay byte
        # identical; B keeps its loss/cost and competing obligation in C12.
        world.actor_state["A"]["tools_remaining"] = post["exclusive_holdings"]["A"]
        world.actor_state["B"]["tools_remaining"] = post["exclusive_holdings"]["B"]
        world.actor_state["B"]["free_hours"] = post["B_free_hours"]
        world.resources["workshop"]["tool_available"] = bool(post["exclusive_holdings"]["A"])
        product._checkpoint("root", world.clock, world)
        a0 = product.observe_verified()
        state_before = copy.deepcopy(a0["self"]["state"])
        action_result = product.record_omission() if omit_e2 else product.material_inspect()
        waited = product.wait(30)
        other = product.other()
        durable = product.store.latest_state("root")["world"]
        state_after = durable["actor_state"]["A"]
        episodes = product.store.episodes("root")
        source_episode = next(e for e in episodes if e["kind"] == "GM01_SOURCE")
        observed_record = {
            "status": a0.get("status"), "claims": [c["kind"] for c in a0.get("claims", [])],
            "tools_before": state_before["tools_remaining"], "tools_after": state_after["tools_remaining"],
            "completed_before": state_before["completed_units"], "completed_after": state_after["completed_units"],
            "material_before": state_before["material_remaining"], "material_after": state_after["material_remaining"],
            "action": action_result, "a2_other_units": other["public"]["completed_units"],
            "a2_offscreen": [product.store.world_event("root", e)["kind"] for e in waited["offscreen_events"]],
            "c12_verify": a0["c12_verify"], "source_episode": source_episode,
            "c8_state_digest": a0["c8"]["state_digest"],
        }
        # This inherited assertion is not altered for any rival or countercut.
        passed = p01(observed_record, {"other": life.b_source.actor_id,
                                      "result_hash": producer.source["gm01_result_hash"]})
        used = int(bool(action_result.get("admitted")))
        terminal = {"A": state_after["tools_remaining"],
                    "B": durable["actor_state"]["B"]["tools_remaining"], "spent": used}
        require(sum(terminal.values()) == 1, "DURABLE_TOOL_CONSERVATION_FAILED")
        material_terminal = {"A": state_after["material_remaining"],
                             "B": durable["actor_state"]["B"]["material_remaining"], "spent": used}
        require(sum(material_terminal.values()) == sum(before["material_units"].values()),
                "DURABLE_MATERIAL_CONSERVATION_FAILED")
        require(durable["actor_state"]["B"]["free_hours"] == post["B_free_hours"],
                "B_TRANSFER_COST_ERASED")
        addon = load_f2()
        legacy = old_verify(product.store, "root")
        repaired = addon.verify_branch_chain(product.store, "root")
        require(not legacy["ok"], "FROZEN_ORIGINAL_C12_RED_DISAPPEARED")
        require(repaired["ok"], "F2_ADDON_VERIFICATION_FAILED:" + str(repaired["errors"]))
        product.close()
        product = None
        cold = R31JProduct.reopen(root / "product")
        try:
            cold_state = cold.store.latest_state("root")["world"]
            require(cold_state == durable, "COLD_REOPEN_CHANGED_EFFECT")
            require(addon.verify_branch_chain(cold.store, "root")["ok"], "COLD_C12_INVALID")
        finally:
            cold.close()
        require(life.a_snapshot == frozen["prior"]["A"]["snapshot"], "RETROACTIVE_A_MUTATION")
        require(life.b_snapshot == frozen["prior"]["B"]["snapshot"], "RETROACTIVE_B_MUTATION")
        return {
            "assertion": ASSERTION, "p01": passed, "action": action_result,
            "baseline_hash": expected_hash, "world_before_hash": digest(before),
            "world_after": post, "terminal_tool_ledger": terminal,
            "terminal_material_ledger": material_terminal,
            "B_source_admitted": bool(admitted_source), "cold_effect_equal": True,
            "access": {"A_B_act": lab_record["A_event_access"], "A_tool": lab_record["A_tool_access"],
                       "B_motive": "UNKNOWN", "basis": "EXPLICIT_TEST_ONLY_RECEIPTS_NOT_G1_ISSUANCE"},
            "appraisal": "HOLD_G1_UNISSUED", "recruitment": "HOLD_G2_UNISSUED",
            "acquisition_or_evaluated_nochange": "HOLD_ORIGINAL_RULE_T_UNISSUED",
            "H0": "PREEXISTING_SKILL_AND_SHARED_TASK_HISTORY_PRESENT",
            "original_c12_errors": legacy["errors"], "F2_addon": repaired,
            "authenticity_completeness": "HOLD_RAW_SQLITE_INJECTION_DELETION_REHASH_EXTERNAL_ANCHOR",
            "c9_target": artifacts.target_id, "e2_receipt_hash": artifacts.e2_receipt_hash,
            "durable_world_hash": durable["hash"], "native": False,
            "clocks": {"prehistory": 241, "fixed_world": 242, "B_valid": 250,
                       "observation": 251, "actor_access": 253,
                       "world_domain": "F1C_FIXTURE_WORLD",
                       "admission": {"domain": "BP2_LOGICAL", "tick": producer.event_time},
                       "performance": action_result.get("clock"),
                       "performance_domain": "BP4_WORLD",
                       "bridge": "DECLARED_SOURCEFREE_PROCESS_ORDER_NOT_NUMERIC_GLOBAL_TIME"},
        }
    finally:
        if product is not None:
            product.close()
        producer.close()


def main():
    life, frozen, frozen_hash = freeze()
    cases = [
        ("SHARE", {}, True), ("REFUSE", {"action": "REFUSE"}, False),
        ("SILENCE", {"action": "SILENCE"}, False),
        ("UNOBSERVED_SHARE", {"observed": False}, True),
        ("UNOBSERVED_REFUSE", {"action": "REFUSE", "observed": False}, False),
        ("B_SOURCE_SEVERED", {"cut_source": True}, False),
        ("B_SOURCE_RESTORED", {}, True),
        ("E2_OMITTED", {"omit_e2": True}, False),
        ("NO_B_RESOURCE", {"no_resource": True}, False),
        ("ENCUMBERED_B_TOOL", {"encumbered": True}, False),
        ("DUPLICATE_TOOL", {"duplicate": True}, False),
        ("NATIVE_SOURCE_SMUGGLED", {"native": True}, False),
    ]
    results = []
    expected_holds = {
        "REFUSE": "C9_RECEIVER_HOLD:later_e2:NO_PROPOSAL",
        "SILENCE": "C9_RECEIVER_HOLD:later_e2:NO_PROPOSAL",
        "UNOBSERVED_REFUSE": "C9_RECEIVER_HOLD:later_e2:NO_PROPOSAL",
        "NO_B_RESOURCE": "B_HAS_NO_TRANSFERABLE_TOOL",
        "ENCUMBERED_B_TOOL": "B_TOOL_TRANSFER_RIGHT_DENIED",
        "DUPLICATE_TOOL": "FOCAL_TOOL_CONSERVATION_FAILED",
        "NATIVE_SOURCE_SMUGGLED": "NATIVE_B_GRANT_ABSENT",
    }
    with tempfile.TemporaryDirectory(prefix="f1c-courts-", dir=HERE) as tmp:
        for name, kwargs, expected in cases:
            try:
                value = same_receiver_assertion(Path(tmp) / name, life, frozen, frozen_hash, **kwargs)
                require(name not in expected_holds, "EXPECTED_EXACT_HOLD_NOT_RETURNED:" + name)
                require(value["p01"] == expected, "UNEXPECTED_FINAL_ASSERTION:" + name)
                if name == "UNOBSERVED_SHARE":
                    require(value["access"]["A_tool"] and not value["access"]["A_B_act"],
                            "TOOL_EVENT_ACCESS_COLLAPSED")
                require(value["access"]["B_motive"] == "UNKNOWN", "B_MOTIVE_FABRICATED")
                require(value["acquisition_or_evaluated_nochange"] == "HOLD_ORIGINAL_RULE_T_UNISSUED",
                        "UNISSUED_T_LAUNDERED_TO_NOCHANGE")
                if name == "B_SOURCE_SEVERED":
                    require(value["action"]["admitted"] and not value["B_source_admitted"],
                            "SOURCE_CUT_DID_NOT_REACH_REAL_CONSUMER")
                results.append({"case": name, "expected": expected, "observed": value["p01"], "receipt": value})
            except Hold as e:
                if name not in expected_holds or str(e) != expected_holds[name]:
                    raise
                results.append({"case": name, "expected": expected, "observed": False,
                                "exact_expected_hold": True, "hold": str(e),
                                "source_context": getattr(e, "source_context", None),
                                "baseline_hash": frozen_hash,
                                "intervention_type": "NON_EVENT_CONDITION" if name == "SILENCE" else "TEST_ONLY_INTERVENTION",
                                "appraisal": "HOLD_G1_UNISSUED", "recruitment": "HOLD_G2_UNISSUED"})
        altered = copy.deepcopy(frozen)
        altered["prior"]["A"]["snapshot"]["state"]["tools_remaining"] = 99
        try:
            same_receiver_assertion(Path(tmp) / "RETROACTIVE_A", life, altered, frozen_hash)
            raise AssertionError("RETROACTIVE_A_NOT_REFUSED")
        except Hold as e:
            require(str(e) == "A_B_OR_SHARED_PREHISTORY_CHANGED", "WRONG_BASELINE_REFUSAL")
            results.append({"case": "RETROACTIVE_A", "observed": False, "hold": str(e)})
    receipts = {r["case"]: r.get("receipt") for r in results}
    base = receipts["SHARE"]
    cut = receipts["B_SOURCE_SEVERED"]
    restored = receipts["B_SOURCE_RESTORED"]
    require(base["world_before_hash"] == cut["world_before_hash"] == restored["world_before_hash"],
            "B_ONLY_CUT_CHANGED_WORLD_BASELINE")
    require(base["world_after"] == cut["world_after"] == restored["world_after"],
            "B_ONLY_CUT_CHANGED_TRANSFER_OR_B_COST")
    print(json.dumps({"grade": GRADE, "frozen": frozen, "frozen_hash": frozen_hash,
                      "results": results, "cases": len(results),
                      "three_courts": {"engineering": "PENDING_RESULT_INTERPRETATION",
                                       "science": "HOLD", "authority": "HOLD"}}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
