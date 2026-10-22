"""Executable R29P sourcefree generated-actor to cold C12/A0/A2 runner."""
from __future__ import annotations

import json
from pathlib import Path

import historical_actor_producer as H
from bp2p4 import reunion as R
from bp4.world import initial_world

import stable_actor_binding as S
from r29p.product import R29PProduct


def build_bundle(root, *, variant="A_REPAIR_LONG", world=None, e2="default"):
    """Run the real R27P stable producer and construct the R29P product."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    producer = S.StableJoinedProducer(root / "bp2", variant=variant)
    try:
        outcome = producer.run()
        if not outcome.ok:
            raise RuntimeError(
                "R29P_PRODUCER_REFUSED:" + outcome.stage_reached + ":" + outcome.failure_code)
        receipt = outcome.receipt()
        persisted = receipt["persisted"]
        env = producer.env
        paths = {
            "journal_path": Path(persisted["journal_path"]),
            "key_path": env.key_path,
            "key_id": env.key_store.key_id,
            "anchor_log": env.anchor.log_path,
            "anchor_watermark": env.anchor.watermark_path,
            "c9_path": Path(persisted["c9_db_path"]),
        }
        artifacts = R._assemble(
            mode="FRESH", root=root / "bp2", life=producer.life,
            persisted=persisted, paths=paths, receipt=receipt, e2=None)
        product = R29PProduct(
            root / "product", artifacts=artifacts, variant=variant,
            world=world, e2=e2)
        return product, artifacts, producer
    except Exception:
        producer.close()
        raise


def product_from_artifacts(root, artifacts, *, world=None, e2="default"):
    """Construct another product root over the same verified source artifacts."""
    return R29PProduct(
        Path(root), artifacts=artifacts, world=world, e2=e2)


def observable(product) -> dict:
    """One named A0/A2 read: A0 claims + tools + A2 offscreen life."""
    observed = product.observe_verified()
    if observed.get("status") != "OK":
        return {
            "status": observed.get("status"),
            "code": observed.get("code", ""),
            "native": False,
            "c12_verify": observed.get("c12_verify", {}),
        }
    say = product.say("I will inspect the fitting before the shift ends.")
    waited = product.wait(30)
    other = product.other()
    offscreen = [
        product.store.world_event(product.branch_id, event_id)["kind"]
        for event_id in waited.get("offscreen_events", [])
    ]
    return {
        "status": "OK",
        "code": "",
        "native": False,
        "claims": [claim["kind"] for claim in observed.get("claims", [])],
        "others": [row["actor"] for row in observed.get("others_present", [])],
        "self_history": observed["self"].get("history_hash"),
        "self_source_hash": product.seed.life.a_source.source_hash,
        "tools": observed["self"]["state"].get("tools_remaining"),
        "say": say.get("status"),
        "a2_clock": waited.get("clock"),
        "a2_other_units": other["public"].get("completed_units"),
        "a2_offscreen": offscreen,
        "c12_verify": observed.get("c12_verify", {}),
    }


def stable_view(observed: dict) -> dict:
    """Remove path/key-dependent identities from a cross-run comparison."""
    return {
        key: observed.get(key)
        for key in (
            "status", "code", "claims", "others", "self_history",
            "self_source_hash", "tools", "say", "a2_clock",
            "a2_other_units", "a2_offscreen",
        )
    }


def run_fork(root, *, variant="A_REPAIR_LONG") -> dict:
    """Create a persistent root, fork it, and diverge both branches."""
    product, artifacts, producer = build_bundle(root, variant=variant)
    producer.close()
    try:
        before = product.observe_verified()
        product.say("We inspect the shared fitting together.")
        product.wait(30)
        fork = product.fork("alt")
        shared_before = product.store.shared_root_equal("root", "alt")
        product.use("alt")
        alt_say = product.say("The alternate branch sends it to market.")
        branches = product.branches()
        shared_after = product.store.shared_root_equal("root", "alt")
        root_verify = product.store.verify("root")
        alt_verify = product.store.verify("alt")
        return {
            "schema": "R29P_FORK_RUN@1",
            "before_claims": [claim["kind"] for claim in before.get("claims", [])],
            "fork": fork,
            "shared_before": shared_before,
            "shared_after": shared_after,
            "alt_say": alt_say,
            "branches": branches,
            "root_verify": root_verify,
            "alt_verify": alt_verify,
            "artifacts": artifacts.public(),
        }
    finally:
        product.close()


def run_m6(root, *, variant="A_REPAIR_LONG") -> dict:
    """Create a root with B's independent offscreen life and actor-only access."""
    product, artifacts, producer = build_bundle(root, variant=variant)
    producer.close()
    try:
        product.say("The fitting is on the bench.")
        product.wait(30)
        before = product.observe_verified()
        travel = product.travel("market")
        attend = product.attend()
        after = product.observe_verified()
        episodes = product.store.episodes(product.branch_id)
        return {
            "schema": "R29P_M6_RUN@1",
            "before_claims": [
                (claim["kind"], claim.get("m6_receiver_state"),
                 claim.get("m6_permission"))
                for claim in before.get("claims", [])
            ],
            "travel": travel,
            "attend": attend,
            "after_claims": [
                (claim["kind"], claim.get("m6_receiver_state"),
                 claim.get("m6_permission"))
                for claim in after.get("claims", [])
            ],
            "episode_kinds": [row["kind"] for row in episodes],
            "b_episodes": [
                row["kind"] for row in episodes
                if row["actor_id"] == "B"
            ],
            "verify": product.c12_verify(),
            "artifacts": artifacts.public(),
        }
    finally:
        product.close()


def world_with_b_units(artifacts, units: int):
    world = initial_world(artifacts.life)
    world.actor_state["B"]["completed_units"] = units
    return world


def world_without_contact(artifacts):
    world = initial_world(artifacts.life)
    world.positions["B"] = "market"
    return world
