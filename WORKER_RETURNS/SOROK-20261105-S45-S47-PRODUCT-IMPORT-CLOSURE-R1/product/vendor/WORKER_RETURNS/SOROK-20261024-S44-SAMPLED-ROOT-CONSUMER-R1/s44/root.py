"""Bounded source-bound sampled antecedent root over the real BP1/JOIN-E life."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

from .bootstrap import install

install()

from bp1.composer import TwoActorLife, build_actor_history  # noqa: E402
from bp1.ledger import ActorLedger, make_objective_event, verify_snapshot  # noqa: E402
from bp1.source import issue_actor_source  # noqa: E402
from lab_sgi1.joint import (  # noqa: E402
    material_joint_opportunity,
    observe_joint_actions,
    validate_joint,
)

from .bundle import (  # noqa: E402
    A_ID,
    B_ID,
    GRADE,
    effective_probability,
    normalize_bundle,
)
from .errors import S44Refusal  # noqa: E402
from .rng import (  # noqa: E402
    draw_bernoulli,
    draw_candidate,
    sha256_hex,
)

ROOT_SCHEMA = "S44_GENERATED_ANTECEDENT_ROOT@1"
ROOT_GRADE = "TEST_ONLY_SOURCEFREE_SAMPLED_ANTECEDENT_ROOT_NOT_NATIVE"


@dataclass
class SampledRoot:
    bundle: dict
    life: TwoActorLife
    receipt: dict

    @property
    def root_hash(self) -> str:
        return self.receipt["root_hash"]


def _draw(bundle: dict, name: str, draws: list[dict],
          conditional_value: Any = None):
    rule = bundle["rules"].get(name)
    if rule is None:
        raise S44Refusal("S44_RULE_MISSING", name)
    if rule.get("operation") == "BERNOULLI_RATIONAL":
        n = int(rule["numerator_if_false"])
        d = int(rule["denominator_if_false"])
        if conditional_value is not None:
            n, d = effective_probability(bundle, name, int(conditional_value))
        receipt, value = draw_bernoulli(
            bundle["root_seed"], bundle_hash=bundle["bundle_hash"],
            rule=rule, numerator=n, denominator=d,
            conditional_value=conditional_value,
        )
        receipt["rule_name"] = name
        draws.append(receipt)
        return value, receipt
    receipt, value = draw_candidate(
        bundle["root_seed"], bundle_hash=bundle["bundle_hash"], rule=rule,
        conditional_value=conditional_value,
    )
    receipt["rule_name"] = name
    draws.append(receipt)
    return value, receipt


def _source(actor_id: str, *, role: str, seed: str, birth: int, cash: int,
            hours: int, material: int, other: str):
    return issue_actor_source(
        actor_id=actor_id,
        role=role,
        seed=seed,
        birth_clock=birth,
        initial_cash=cash,
        initial_free_hours=hours,
        material_units=material,
        other_actor_id=other,
        known_unknowns=(
            "CHILDHOOD_HISTORY_SPARSE",
            "PSYCHOLOGICAL_LAW_UNISSUED",
            "NATIVE_ACTOR_SOURCE_NOT_GRANTED",
        ),
    )


def generate_root(bundle_input: Mapping[str, Any]) -> SampledRoot:
    bundle = normalize_bundle(bundle_input)
    draws: list[dict] = []
    values = {}
    for name in (
        "a_material", "b_material", "a_cash", "b_cash", "a_hours", "b_hours",
        "a_birth", "b_birth", "joint_time", "joint_payment", "joint_hours",
        "joint_units",
    ):
        value, _ = _draw(bundle, name, draws)
        values[name] = int(value)

    predecessor = values["a_material"]
    b_extra_refusal, b_draw = _draw(
        bundle, "b_extra_refusal", draws, conditional_value=predecessor
    )
    a_optional_decline, a_draw = _draw(
        bundle, "a_optional_decline", draws,
        conditional_value=values["joint_time"],
    )

    a_source = _source(
        A_ID, role="repair",
        seed=f"S44_{bundle['root_seed'][:24]}_A_{values['a_material']}",
        birth=values["a_birth"], cash=values["a_cash"], hours=values["a_hours"],
        material=values["a_material"], other=B_ID,
    )
    b_source = _source(
        B_ID, role="finishing",
        seed=f"S44_{bundle['root_seed'][:24]}_B_{values['b_material']}",
        birth=values["b_birth"], cash=values["b_cash"], hours=values["b_hours"],
        material=values["b_material"], other=A_ID,
    )
    a_events, a_replay = build_actor_history(a_source)
    b_events, b_replay = build_actor_history(b_source)
    material = material_joint_opportunity(
        effective_index=values["joint_time"],
        units=values["joint_units"],
        payment_per_actor=values["joint_payment"],
        task_hours=values["joint_hours"],
    )
    anchor = {"actor_id": a_source.actor_id, "history_events": a_events}
    witness = observe_joint_actions(anchor, b_events, material)
    if witness["status"] != "WITNESSED" or not validate_joint(anchor, b_events, witness):
        raise S44Refusal("S44_JOINT_PERFORMED_ACTION_NOT_WITNESSED")
    objective = make_objective_event(
        material, witness, [a_source.actor_id, b_source.actor_id]
    )
    a_ledger = ActorLedger(a_source, prior_history_events=a_events)
    b_ledger = ActorLedger(b_source, prior_history_events=b_events)
    for ledger in (a_ledger, b_ledger):
        ledger.append_shared_objective(
            objective, parents=(ledger.prior_history_event_id,)
        )
    a_action = next(x for x in witness["actions"]
                    if x["owner_id"] == a_source.actor_id)
    b_action = next(x for x in witness["actions"]
                    if x["owner_id"] == b_source.actor_id)
    for ledger, action in ((a_ledger, a_action), (b_ledger, b_action)):
        ledger.append_performed_action(
            action, material, objective["objective_event_id"],
            parents=(ledger.prior_history_event_id,
                     ledger.objective_events[-1].event_id),
        )
    a_ledger.append_other_action(
        b_action, material, parents=(a_ledger.objective_events[-1].event_id,)
    )
    b_ledger.append_other_action(
        a_action, material, parents=(b_ledger.objective_events[-1].event_id,)
    )
    for ledger, other in ((a_ledger, b_source.actor_id),
                          (b_ledger, a_source.actor_id)):
        ledger.append_relation_view(
            other, "UNKNOWN_OR_NONRECIPROCAL",
            "NO_PSYCHIC_RELATION_OWNER_GRANT",
            parents=(ledger.events[-1].event_id,),
        )
    if b_extra_refusal:
        b_ledger.append_no_change(
            "OTHER_REFUSES_VOLUNTARY_EXTRA_TASK",
            parents=(b_ledger.events[-1].event_id,),
        )
    if a_optional_decline:
        a_ledger.append_no_change(
            "FOCAL_DECLINES_OPTIONAL_TASK",
            parents=(a_ledger.events[-1].event_id,),
        )
    for ledger in (a_ledger, b_ledger):
        accepted, errors = ledger.verify()
        if not accepted:
            raise S44Refusal("S44_HISTORICAL_LEDGER_INVALID", ",".join(errors))
    a_snapshot, b_snapshot = a_ledger.snapshot(), b_ledger.snapshot()
    for snapshot in (a_snapshot, b_snapshot):
        accepted, reason = verify_snapshot(snapshot)
        if not accepted:
            raise S44Refusal("S44_SNAPSHOT_INVALID", str(reason))
    life = TwoActorLife(
        a_source=a_source, b_source=b_source, a_events=a_events,
        b_events=b_events, a_replay=a_replay, b_replay=b_replay,
        material=material, witness=witness, objective=objective,
        a_ledger=a_ledger, b_ledger=b_ledger,
        a_snapshot=a_snapshot, b_snapshot=b_snapshot,
    )
    body = {
        "schema": ROOT_SCHEMA,
        "grade": ROOT_GRADE,
        "native": False,
        "psychology_claim": False,
        "selected_finished_life": False,
        "root_bundle_hash": bundle["bundle_hash"],
        "root_seed_sha256": sha256_hex(bytes.fromhex(bundle["root_seed"])),
        "root_seed_source": bundle["root_seed_source"],
        "actor_ids": sorted([a_source.actor_id, b_source.actor_id]),
        "source_hashes": [a_source.source_hash, b_source.source_hash],
        "source_refs": [a_source.source_ref, b_source.source_ref],
        "initial_facts": {
            "a_material": values["a_material"],
            "b_material": values["b_material"],
            "a_cash": values["a_cash"],
            "b_cash": values["b_cash"],
            "a_free_hours": values["a_hours"],
            "b_free_hours": values["b_hours"],
            "a_birth_clock": values["a_birth"],
            "b_birth_clock": values["b_birth"],
        },
        "joint": {
            "effective_index": values["joint_time"],
            "units": values["joint_units"],
            "payment_per_actor": values["joint_payment"],
            "task_hours": values["joint_hours"],
            "material_event_ref": material["event_id"],
            "objective_ref": objective["objective_event_id"],
            "witness_ref": witness["event_id"],
        },
        "selected_branches": {
            "a_optional_decline": bool(a_optional_decline),
            "b_extra_refusal": bool(b_extra_refusal),
            "conditions": {
                "b_extra_refusal": {
                    "predecessor": "a_material",
                    "value": predecessor,
                    "receipt_hash": b_draw["decision_replay_identity_hash"],
                },
                "a_optional_decline": {
                    "predecessor": "joint_time",
                    "value": values["joint_time"],
                    "receipt_hash": a_draw["decision_replay_identity_hash"],
                },
            },
        },
        "draw_receipts": draws,
        "candidate_set_hashes": {
            row["rule_name"]: row.get("candidate_set_hash", "")
            for row in draws
        },
        "event_refs": {
            a_source.actor_id: [e.event_id for e in a_ledger.events],
            b_source.actor_id: [e.event_id for e in b_ledger.events],
        },
        "ledger_event_hashes": {
            a_source.actor_id: [e.hash for e in a_ledger.events],
            b_source.actor_id: [e.hash for e in b_ledger.events],
        },
        "g18_history_refs": {
            "a": [e["event_id"] for e in a_events],
            "b": [e["event_id"] for e in b_events],
        },
        "g18_history_hashes": {
            "a": a_replay["history_hash"], "b": b_replay["history_hash"],
        },
        "snapshot_hashes": {
            "a": a_snapshot["hash"], "b": b_snapshot["hash"],
        },
        "state": {"a": a_snapshot["state"], "b": b_snapshot["state"]},
        "material_world": material,
        "no_effect_branches": [
            name for name, value in (
                ("a_optional_decline", a_optional_decline),
                ("b_extra_refusal", b_extra_refusal),
            ) if not value
        ],
        "product_model_calls": 0,
    }
    body["root_hash"] = sha256_hex(body)
    body["root_id"] = "S44_ROOT_" + body["root_hash"][:24].upper()
    life.historical_receipt = body  # type: ignore[attr-defined]
    return SampledRoot(bundle=bundle, life=life, receipt=body)


__all__ = ["ROOT_SCHEMA", "ROOT_GRADE", "SampledRoot", "generate_root"]
