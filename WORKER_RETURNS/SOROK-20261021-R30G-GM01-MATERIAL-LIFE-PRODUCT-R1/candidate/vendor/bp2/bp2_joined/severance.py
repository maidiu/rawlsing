"""Six same-assertion source-edge severances and their restoration.

Each edge is cut physically at the place the joined chain actually depends on
it, never by swapping in a mock packet:

    C8_PROOF                 the OUT9 proof verifier is withheld
    BP1_ACTOR_OTHER_HISTORY  the other actor's sealed history feeds the ingress
    RULE_A_SOURCE            the CAN008 RULE_A resource is withheld
    RULE_T_GRANT_BINDING     the CAN011 target grant resource is withheld
    TARGET_COMMIT_READ_HASH  the committed target row is physically mutated
    PERFORMED_E2             the later action names its own actor as actuator

Supplementary variations cut the same edges deeper (self offer, empty rule
registry, self-issued target request, pre-commit action) and use an identical
fresh root for restoration.

The named downstream assertion is ``producer.joined_consumer_assertion``. Every
trial must redden that exact function and return to passing after restoration.
"""
from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from . import producer as producer_module
from .producer import JoinedOutcome, JoinedProducer, joined_consumer_assertion

SEVERANCE_EDGES = (
    "C8_PROOF",
    "BP1_ACTOR_OTHER_HISTORY",
    "RULE_A_SOURCE",
    "RULE_T_GRANT_BINDING",
    "TARGET_COMMIT_READ_HASH",
    "PERFORMED_E2",
)

SUPPLEMENTARY_EDGES = (
    "BP1_OTHER_SELF_OFFER",
    "RULE_A_REGISTRY_EMPTY",
    "RULE_T_SELF_ISSUED",
    "E2_ACTION_BEFORE_COMMIT",
)

_EDGE_TO_SEVER = {
    "C8_PROOF": "C8_PROOF_WITHHELD",
    "BP1_ACTOR_OTHER_HISTORY": "BP1_ACTOR_SWAPPED",
    "BP1_OTHER_SELF_OFFER": "BP1_OTHER_SELF_OFFER",
    "RULE_A_SOURCE": "RULE_A_WITHHELD",
    "RULE_A_REGISTRY_EMPTY": "RULE_A_REGISTRY_EMPTY",
    "RULE_T_GRANT_BINDING": "RULE_T_GRANT_WITHHELD",
    "RULE_T_SELF_ISSUED": "RULE_T_SELF_ISSUED",
    "TARGET_COMMIT_READ_HASH": "TARGET_RECORD_MUTATED",
    "PERFORMED_E2": "E2_SELF_ACTUATOR",
    "E2_ACTION_BEFORE_COMMIT": "E2_ACTION_BEFORE_COMMIT",
}

EDGE_CUT_DESCRIPTION = {
    "C8_PROOF": "OUT9 ingress called without the BP3 keyed journal proof verifier",
    "BP1_ACTOR_OTHER_HISTORY": (
        "actor ingress carries the OTHER BP1 actor's sealed snapshot and identity"),
    "RULE_A_SOURCE": "no CAN008 RULE_A resource is supplied to the CAN008 port",
    "RULE_T_GRANT_BINDING": "no CAN011 target grant resource is supplied to the CAN011 port",
    "TARGET_COMMIT_READ_HASH": (
        "the committed target_state row is rewritten after commit, before the "
        "later read"),
    "PERFORMED_E2": "the later performed-action receipt binds the focal actor as its own actuator",
    "BP1_OTHER_SELF_OFFER": (
        "the declared other-person offer is replaced by the focal actor's own "
        "performed act"),
    "RULE_A_REGISTRY_EMPTY": "the response registry is the empty production registry",
    "RULE_T_SELF_ISSUED": "the CAN011 target request is marked self-issued",
    "E2_ACTION_BEFORE_COMMIT": "the later action time precedes the target commit time",
}

# Edges whose RED run leaves the C9 store untouched and therefore restore on the
# same root; TARGET/E2 edges restore the same root by repairing the exact bytes
# or re-performing the later stage.
_SAME_ROOT_RESUME = {
    "C8_PROOF",
    "BP1_ACTOR_OTHER_HISTORY",
    "RULE_A_SOURCE",
    "RULE_T_GRANT_BINDING",
}


@dataclass
class SeveranceTrial:
    edge: str
    sever: str
    cut: str
    assertion: str
    red: dict
    restored: dict
    restore_basis: str
    same_root: bool
    same_source_tree: bool = True
    supplementary: bool = False

    @property
    def proves(self) -> bool:
        return bool(self.red.get("red")) and not bool(self.restored.get("red"))

    def as_dict(self) -> dict:
        return {
            "edge": self.edge,
            "sever": self.sever,
            "cut": self.cut,
            "assertion": self.assertion,
            "red": self.red,
            "restored": self.restored,
            "restore_basis": self.restore_basis,
            "same_root": self.same_root,
            "same_source_tree": self.same_source_tree,
            "supplementary": self.supplementary,
            "proves": self.proves,
        }


def _evaluate(outcome: JoinedOutcome) -> dict:
    """Run the named assertion on one outcome and record the typed result."""
    try:
        joined_consumer_assertion(outcome)
    except AssertionError as error:
        return {
            "red": True,
            "assertion_message": str(error),
            "ok": outcome.ok,
            "stage": outcome.stage_reached,
            "failure_code": outcome.failure_code,
        }
    receipt = outcome.receipt()
    return {
        "red": False,
        "assertion_message": "PASS",
        "ok": outcome.ok,
        "stage": outcome.stage_reached,
        "failure_code": "",
        "c8_occurrence_id": receipt.get("c8_occurrence_id", ""),
        "target_record_hash": receipt.get("target_record_hash", ""),
        "consumed_state_hash": receipt.get("consumed_state_hash", ""),
        "e2_receipt_hash": receipt.get("e2_receipt_hash", ""),
    }


def _restore_same_root(edge: str, producer: JoinedProducer,
                       red_outcome: JoinedOutcome) -> JoinedOutcome:
    if edge in _SAME_ROOT_RESUME:
        return producer.resume()
    if edge == "TARGET_COMMIT_READ_HASH":
        producer.restore_target_row()
        e2 = producer.stage_e2()
        return producer.outcome_after_e2(e2)
    if edge == "PERFORMED_E2":
        e2 = producer.stage_e2()
        return producer.outcome_after_e2(e2)
    raise ValueError("not a same-root edge: " + edge)


def run_severance(edge: str, root) -> SeveranceTrial:
    """Cut one source edge, assert RED, restore, assert PASS (same root)."""
    if edge not in _EDGE_TO_SEVER:
        raise ValueError("unknown severance edge: " + edge)
    sever = _EDGE_TO_SEVER[edge]
    root = Path(root)
    if edge in _SAME_ROOT_RESUME or edge in {"TARGET_COMMIT_READ_HASH", "PERFORMED_E2"}:
        with JoinedProducer(root) as producer:
            red_outcome = producer.run(sever=sever)
            red = _evaluate(red_outcome)
            restored_outcome = _restore_same_root(edge, producer, red_outcome)
            restored = _evaluate(restored_outcome)
        return SeveranceTrial(
            edge=edge,
            sever=sever,
            cut=EDGE_CUT_DESCRIPTION[edge],
            assertion="bp2_joined.producer.joined_consumer_assertion",
            red=red,
            restored=restored,
            restore_basis="same_root_exact_state_restored",
            same_root=True,
        )
    # supplementary: the RED run commits, so restoration uses an identical fresh
    # root built from the same staged source closure and the same fixtures.
    with tempfile.TemporaryDirectory() as td:
        with JoinedProducer(Path(td) / "red") as producer:
            red = _evaluate(producer.run(sever=sever))
    with tempfile.TemporaryDirectory() as td:
        with JoinedProducer(Path(td) / "restored") as producer:
            restored = _evaluate(producer.run())
    return SeveranceTrial(
        edge=edge,
        sever=sever,
        cut=EDGE_CUT_DESCRIPTION[edge],
        assertion="bp2_joined.producer.joined_consumer_assertion",
        red=red,
        restored=restored,
        restore_basis="identical_fresh_root_uncut",
        same_root=False,
        supplementary=True,
    )


def run_all_severances(root) -> list[SeveranceTrial]:
    """Run the six load-bearing edges, then the four deeper variations."""
    root = Path(root)
    trials: list[SeveranceTrial] = []
    for index, edge in enumerate(SEVERANCE_EDGES):
        trials.append(run_severance(edge, root / f"edge-{index + 1}-{edge.lower()}"))
    for index, edge in enumerate(SUPPLEMENTARY_EDGES):
        trials.append(
            run_severance(edge, root / f"extra-{index + 1}-{edge.lower()}"))
    return trials


def severance_receipt(trials: list[SeveranceTrial]) -> dict:
    primary = [t for t in trials if not t.supplementary]
    return {
        "schema": "BP2_SEVERANCE_RECEIPT@1",
        "named_assertion": "bp2_joined.producer.joined_consumer_assertion",
        "edge_count": len(primary),
        "supplementary_count": len(trials) - len(primary),
        "all_primary_proved": all(t.proves for t in primary),
        "all_supplementary_proved": all(t.proves for t in trials if t.supplementary),
        "trials": [t.as_dict() for t in trials],
    }


__all__ = [
    "EDGE_CUT_DESCRIPTION",
    "SEVERANCE_EDGES",
    "SUPPLEMENTARY_EDGES",
    "SeveranceTrial",
    "run_all_severances",
    "run_severance",
    "severance_receipt",
]
