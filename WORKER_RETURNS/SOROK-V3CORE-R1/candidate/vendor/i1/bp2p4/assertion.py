"""THE named downstream A0/A2 joined-consumer assertion.

One function is the acceptance target for every severance trial:

``bp2p4.assertion.joined_downstream_a0_a2_assertion``

It constructs the joined product from the actual BP2 artifacts and runs the real
BP4 A0-A3 surface. A source cut raises ``AssertionError`` with a precise message;
an intact source returns a receipt. Nothing here checks a dict this worker wrote:
every expected value is read from the physical BP2 artifacts through
``JoinedProduct.seed`` / ``verify_join``.

The assertion deliberately advances the product (SAY, WAIT, ATTEND), so every
trial needs a fresh product root. That is why severance restoration is a fresh
root built from the same intact artifact bytes rather than a rewind.
"""
from __future__ import annotations

from pathlib import Path

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from bp4.perception import render_requested_event  # noqa: E402

from .envelope import EnvelopeRefusal  # noqa: E402
from .product import JoinedProduct, JoinedProductRefusal  # noqa: E402
from .reunion import ReunionRefusal  # noqa: E402
from .seed import SeedRefusal  # noqa: E402

ASSERTION_NAME = "bp2p4.assertion.joined_downstream_a0_a2_assertion"
CONSTRUCTION_CODES = (JoinedProductRefusal, SeedRefusal, ReunionRefusal,
                      EnvelopeRefusal)


def joined_downstream_a0_a2_assertion(root, artifacts, *, e2="default",
                                      world=None, materialize: bool = True,
                                      product_cls=JoinedProduct) -> dict:
    """Run the one joined A0/A2 product assertion over actual BP2 artifacts.

    ``product_cls`` defaults to the unchanged BP2P4J product; a guarded
    subclass can run the identical acceptance checks without a second
    assertion implementation.
    """
    try:
        product = product_cls(Path(root), artifacts=artifacts, e2=e2,
                              world=world, materialize=materialize)
    except CONSTRUCTION_CODES as error:
        raise AssertionError(
            "JOINED_PRODUCT_SOURCE: " + str(getattr(error, "code", error))) from error
    try:
        source = product.verify_join()
        custody = source["custody"]
        practice = source["practice"]
        expected_actor = product.seed.life.a_source.actor_id

        # ---------------- A0: encounter / observation ----------------
        a0 = product.observe()
        if a0.get("status") != "OK":
            raise AssertionError("A0_OBSERVE_NOT_OK: " + str(a0.get("code")))
        if a0.get("actor") != "A":
            raise AssertionError("A0_ACTOR_IDENTITY: " + str(a0.get("actor")))
        if a0.get("clock") != 10:
            raise AssertionError("A0_WORLD_CLOCK_ORIGIN: " + str(a0.get("clock")))
        if a0["self"]["position"] != "workshop":
            raise AssertionError("A0_POSITION: " + str(a0["self"]["position"]))
        if a0["c9"]["target_id"] != custody["target_id"]:
            raise AssertionError("A0_SOURCE_TARGET: A0 reports a different BP2 target")
        if a0["c9"]["state_hash"] != custody["consumed_state_hash"]:
            raise AssertionError("A0_SOURCE_CONSUMED: A0 reports a different consumed hash")
        if a0["c9"]["e2_admitted"] is not True:
            raise AssertionError("A0_E2_ADMITTED: BP2 performed E2 not admitted")
        if a0["c8"]["state_digest"] != custody["c8_state_digest"]:
            raise AssertionError("A0_C8_DIGEST: A0 reports a different C8 occurrence")
        if a0["c8"]["writer_version"] != custody["c8_writer_version"]:
            raise AssertionError("A0_C8_WRITER_VERSION")
        if a0["c8"]["occurrence_count"] != 1:
            raise AssertionError("A0_C8_OCCURRENCE_COUNT: " + str(a0["c8"]["occurrence_count"]))
        projects = a0["self"]["state"].get("projects") or []
        if not practice["established"]:
            raise AssertionError("A0_PRACTICE_NOT_ESTABLISHED")
        if len(projects) != 1 or projects[0].get("source_target_ref") != custody["target_record_hash"]:
            raise AssertionError("A0_PRACTICE_NOT_BOUND_TO_BP2_TARGET")
        if projects[0].get("practice_label") != custody["practice"]["practice_label"]:
            raise AssertionError("A0_PRACTICE_LABEL_MISMATCH")
        if a0["self"]["state"].get("tools_remaining") != 1:
            raise AssertionError("A0_TOOL_FROM_PERFORMED_E2_MISSING")
        claim_kinds = [claim["kind"] for claim in a0["claims"]]
        if claim_kinds != ["ARRIVAL"]:
            raise AssertionError("A0_CLAIM_SET: " + ",".join(claim_kinds))
        if not str(a0["claims"][0]["m6_receiver_state"]).startswith("READY"):
            raise AssertionError("A0_M6_STATE: " + str(a0["claims"][0]["m6_receiver_state"]))
        if a0["native_claims"] != {"actor": False, "rule": False, "c8_trust": False,
                                   "world": False, "c12": False, "c11": False}:
            raise AssertionError("A0_NATIVE_CLAIM")

        # ---------------- A1: SAY / DO ----------------
        said = product.say("I am here about the bench.")
        if said.get("admitted") is not True:
            raise AssertionError("A1_SAY_NOT_ADMITTED")
        if "B" not in said.get("observable_by", []):
            raise AssertionError("A1_SAY_NOT_OBSERVABLE_BY_OTHER")
        inspected = product.inspect()
        if inspected.get("status") != "NO_CHANGE":
            raise AssertionError("A1_INSPECT_NOT_NO_CHANGE")

        # ---------------- A2: elapsed time + independent offscreen life ----
        waited = product.wait(30)
        if waited.get("clock") != 40:
            raise AssertionError("A2_WAIT_CLOCK: " + str(waited.get("clock")))
        offscreen_ids = waited.get("offscreen_events") or []
        if not offscreen_ids:
            raise AssertionError("A2_OFFSCREEN_EVENT_MISSING")
        offscreen = product.store.world_event(product.branch_id, offscreen_ids[-1])
        if offscreen is None or offscreen.get("kind") != "OFFSCREEN_REPAIR":
            raise AssertionError(
                "A2_OFFSCREEN_KIND: " + str((offscreen or {}).get("kind")))
        if offscreen.get("owner_receipt", {}).get("owner_ref") != "TEST_ONLY_BP4_WORLD_OWNER":
            raise AssertionError("A2_OFFSCREEN_NOT_SOURCE_OWNED")
        other = product.other()
        if other["public"]["completed_units"] != 4:
            raise AssertionError(
                "A2_OFFSCREEN_CONSEQUENCE: completed_units="
                + str(other["public"]["completed_units"]))
        if "cash" in other["public"]:
            raise AssertionError("A2_OTHER_PRIVATE_STATE_LEAKED")

        # ---------------- A2: actor-limited M6 perception ----------------
        state_before = product._runtime_state(product.branch_id)
        events = product.store.world_events(product.branch_id)
        hidden = render_requested_event("A", 40, state_before, events,
                                        offscreen["event_id"])
        if hidden.get("state") != "NONRENDERABLE":
            raise AssertionError("A2_M6_ACCESS_LEAKED_BEFORE_ATTEND")
        if hidden.get("code") != "NO_ACTOR_PERCEPTION":
            raise AssertionError("A2_M6_REFUSAL_CODE: " + str(hidden.get("code")))
        travelled = product.travel("market")
        if travelled.get("status") != "OK":
            raise AssertionError("A2_TRAVEL_DENIED: " + str(travelled.get("code")))
        attended = product.attend()
        if attended.get("status") != "NO_CHANGE":
            raise AssertionError("A2_ATTEND_NOT_NO_CHANGE")
        if not attended.get("new_knowledge"):
            raise AssertionError("A2_ATTEND_NO_NEW_KNOWLEDGE")

        # ---------------- A2: cold reentry in the same process ----------------
        reentry = product.reenter()
        if reentry.get("status") != "OK":
            raise AssertionError("A2_REENTRY_NOT_OK: " + str(reentry.get("code")))
        if reentry.get("clock") != 40:
            raise AssertionError("A2_REENTRY_CLOCK: " + str(reentry.get("clock")))
        reentry_kinds = [claim["kind"] for claim in reentry["claims"]]
        if "OFFSCREEN_REPAIR" not in reentry_kinds:
            raise AssertionError("A2_REENTRY_CLAIMS: " + ",".join(reentry_kinds))
        visible = next(claim for claim in reentry["claims"]
                       if claim["kind"] == "OFFSCREEN_REPAIR")
        if visible.get("m6_permission") != "PERMIT_FIRST_PERSON_KNOWLEDGE":
            raise AssertionError("A2_REENTRY_M6_PERMISSION")
        if reentry["c9"]["target_id"] != custody["target_id"]:
            raise AssertionError("A2_REENTRY_SOURCE_TARGET")
        if reentry["c9"]["state_hash"] != custody["consumed_state_hash"]:
            raise AssertionError("A2_REENTRY_SOURCE_CONSUMED")
        if reentry["native_claims"] != {"actor": False, "rule": False, "c8_trust": False,
                                        "world": False, "c12": False, "c11": False}:
            raise AssertionError("A2_REENTRY_NATIVE_CLAIM")

        receipt = {
            "schema": "BP2P4J_JOINED_A0_A2_ASSERTION@1",
            "assertion": ASSERTION_NAME,
            "status": "PASS",
            "mode": source["artifacts"]["mode"],
            "target_id": custody["target_id"],
            "target_record_hash": custody["target_record_hash"],
            "consumed_state_hash": custody["consumed_state_hash"],
            "c8_occurrence_id": custody["c8_occurrence_id"],
            "c8_state_digest": custody["c8_state_digest"],
            "c8_commit_receipt_id": custody["c8_commit_receipt_id"],
            "e1_event_hash": custody["e1_event_hash"],
            "rule_a_content_hash": custody["rule_a_content_hash"],
            "rule_t_content_hash": custody["rule_t_content_hash"],
            "response_hash": custody["response_hash"],
            "grant_hash": custody["grant_hash"],
            "e2_receipt_hash": custody["e2_receipt_hash"],
            "e2_admitted": custody["e2_admitted"],
            "practice": custody["practice"],
            "clock": custody["clock"],
            "envelope": source["envelope"],
            "a0": {
                "clock": a0["clock"],
                "position": a0["self"]["position"],
                "claims": claim_kinds,
                "claim_hashes": [claim["claim_hash"] for claim in a0["claims"]],
                "projects": projects,
                "tools_remaining": a0["self"]["state"].get("tools_remaining"),
            },
            "a1": {"say": said, "inspect": inspected},
            "a2": {
                "wait": waited,
                "offscreen_event_id": offscreen["event_id"],
                "offscreen_event_hash": offscreen["hash"],
                "other_completed_units": other["public"]["completed_units"],
                "m6_hidden_before_attend": hidden,
                "travel": travelled,
                "attend": attended,
                "reentry_claim_kinds": reentry_kinds,
                "reentry_claim_hashes": {claim["kind"]: claim["claim_hash"]
                                         for claim in reentry["claims"]},
                "reentry_target": reentry["c9"]["target_id"],
            },
            "native": False,
            "grade": "TEST_ONLY_SOURCEFREE_JOINED_PRODUCT_ALPHA_NOT_NATIVE",
        }
        receipt["receipt_hash"] = digest(receipt)
        return receipt
    finally:
        product.close()


__all__ = ["ASSERTION_NAME", "joined_downstream_a0_a2_assertion"]
