"""Seven same-assertion source-edge severances and their restoration.

The named downstream assertion is
``bp2p4.assertion.joined_downstream_a0_a2_assertion``. Each edge is cut in the
actual source the same user-facing consumer reads:

1. ``BP2_C8_PROOF``           tampered external anchor watermark -> keyed proof refuses
2. ``BP2_ACTOR_HISTORY``      a BP1 actor source that is not the one in the C8 occurrence
3. ``BP2_RULE_A``             the committed CAN008 response row is removed
4. ``BP2_RULE_T``             the separate CAN011 authorization row is removed
5. ``BP2_TARGET_HASH``        the sealed target preimage is rewritten
6. ``BP2_E2``                 the performed E2 receipt names the actor as its own actuator
7. ``BP4_C10_M6_ACCESS``      actor A's durable perception of the arrival is removed

Trials 1-6 fail at product construction, so they restore the exact bytes of the
same artifact directory and re-run on the same root. Trial 7 fails after the
product run, so it restores on a fresh root built from byte-identical artifacts.
Supplementary variations cut the same edges deeper.
"""
from __future__ import annotations

import dataclasses
import json
import shutil
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from bp1.source import reseal_with_changed_source_ref  # noqa: E402

from .assertion import ASSERTION_NAME, joined_downstream_a0_a2_assertion  # noqa: E402
from .reunion import BP2Artifacts, clone_artifacts  # noqa: E402

SEVERANCE_EDGES = (
    "BP2_C8_PROOF",
    "BP2_ACTOR_HISTORY",
    "BP2_RULE_A",
    "BP2_RULE_T",
    "BP2_TARGET_HASH",
    "BP2_E2",
    "BP4_C10_M6_ACCESS",
)

SUPPLEMENTARY_EDGES = (
    "BP2_OTHER_HISTORY_ALIASED",
    "BP2_E2_NOT_PERFORMED",
    "BP2_PRACTICE_NOT_MATERIALIZED",
)

EDGE_CUT_DESCRIPTION = {
    "BP2_C8_PROOF": "the external monotonic anchor watermark is rewritten so the keyed journal proof refuses",
    "BP2_ACTOR_HISTORY": "the BP1 actor source presented to the consumer is not the source inside the committed C8 occurrence",
    "BP2_RULE_A": "the committed CAN008 response row is deleted from the BP2 C9 store",
    "BP2_RULE_T": "the separate CAN011 authorization row is deleted from the BP2 C9 store",
    "BP2_TARGET_HASH": "the sealed target record preimage is rewritten, breaking the committed record digest",
    "BP2_E2": "the performed E2 owner receipt binds the focal actor as its own actuator",
    "BP4_C10_M6_ACCESS": "actor A's durable perception of the arrival event is deleted, dropping the actor-visible claim source",
    "BP2_OTHER_HISTORY_ALIASED": "the independent other actor's snapshot is replaced by the focal actor's snapshot",
    "BP2_E2_NOT_PERFORMED": "no independently performed E2 receipt is presented",
    "BP2_PRACTICE_NOT_MATERIALIZED": "the committed practice is not materialized into the actor/world state",
}


class SeveranceError(RuntimeError):
    pass


@dataclass
class SeveranceTrial:
    edge: str
    assertion: str
    cut: str
    baseline: dict
    red: dict
    restored: dict
    restore_basis: str
    same_root: bool
    supplementary: bool = False

    @property
    def proves(self) -> bool:
        return (self.baseline.get("red") is False
                and self.red.get("red") is True
                and self.restored.get("red") is False)

    def as_dict(self) -> dict:
        return {
            "edge": self.edge,
            "assertion": self.assertion,
            "cut": self.cut,
            "baseline": self.baseline,
            "red": self.red,
            "restored": self.restored,
            "restore_basis": self.restore_basis,
            "same_root": self.same_root,
            "supplementary": self.supplementary,
            "proves": self.proves,
        }


def _run(root, artifacts, *, product_cls=None, **kwargs) -> dict:
    try:
        if product_cls is None:
            receipt = joined_downstream_a0_a2_assertion(root, artifacts, **kwargs)
        else:
            receipt = joined_downstream_a0_a2_assertion(
                root, artifacts, product_cls=product_cls, **kwargs)
    except AssertionError as error:
        return {"red": True, "message": str(error)}
    except Exception as error:  # noqa: BLE001 - unexpected failure is still RED
        return {"red": True, "message": type(error).__name__ + ": " + str(error)}
    return {
        "red": False,
        "receipt_hash": receipt["receipt_hash"],
        "target_id": receipt["target_id"],
        "consumed_state_hash": receipt["consumed_state_hash"],
        "c8_state_digest": receipt["c8_state_digest"],
        "practice_established": receipt["practice"]["established"],
        "offscreen_completed_units": receipt["a2"]["other_completed_units"],
        "reentry_claims": receipt["a2"]["reentry_claim_kinds"],
    }


# ---------------------------------------------------------------------------
# physical cuts
# ---------------------------------------------------------------------------
def _cut_anchor_watermark(artifacts: BP2Artifacts) -> Callable[[], None]:
    path = artifacts.anchor_watermark
    original = path.read_bytes()
    document = json.loads(original)
    document["version"] = int(document["version"]) + 1
    path.write_text(json.dumps(document, sort_keys=True, separators=(",", ":")),
                    encoding="utf8")
    return lambda: path.write_bytes(original)


def _cut_actor_history(artifacts: BP2Artifacts):
    faulted = dataclasses.replace(
        artifacts.life,
        a_source=reseal_with_changed_source_ref(
            artifacts.life.a_source, "TEST_ONLY_BP1_SOURCE_A_FAULTED"))
    return dataclasses.replace(artifacts, life=faulted)


def _cut_other_history(artifacts: BP2Artifacts):
    faulted = dataclasses.replace(artifacts.life, b_snapshot=artifacts.life.a_snapshot)
    return dataclasses.replace(artifacts, life=faulted)


def _cut_response_row(artifacts: BP2Artifacts) -> Callable[[], None]:
    path = artifacts.c9_path
    with sqlite3.connect(path) as db:
        row = db.execute("SELECT hash, body FROM response").fetchall()
        wanted = artifacts.target.get("response_hash")
        keys = [key for key, body in row if json.loads(body).get("receipt_hash") == wanted]
        if not keys:
            raise SeveranceError("RESPONSE_ROW_NOT_FOUND")
        original = [(key, body) for key, body in row if key in keys]
        db.execute("DELETE FROM response WHERE hash=?", (keys[0],))
        db.commit()

    def restore() -> None:
        with sqlite3.connect(path) as db:
            for key, body in original:
                db.execute("INSERT OR REPLACE INTO response VALUES (?,?)", (key, body))
            db.commit()
    return restore


def _cut_target_journal(artifacts: BP2Artifacts) -> Callable[[], None]:
    path = artifacts.c9_path
    with sqlite3.connect(path) as db:
        row = db.execute("SELECT body FROM target_journal WHERE id=?",
                         (artifacts.target_record_hash,)).fetchone()
        if row is None:
            raise SeveranceError("TARGET_JOURNAL_ROW_NOT_FOUND")
        original = row[0]
        db.execute("DELETE FROM target_journal WHERE id=?",
                   (artifacts.target_record_hash,))
        db.commit()

    def restore() -> None:
        with sqlite3.connect(path) as db:
            db.execute("INSERT OR REPLACE INTO target_journal VALUES (?,?)",
                       (artifacts.target_record_hash, original))
            db.commit()
    return restore


def _cut_target_preimage(artifacts: BP2Artifacts) -> Callable[[], None]:
    path = artifacts.c9_path
    with sqlite3.connect(path) as db:
        row = db.execute("SELECT body FROM target_state WHERE id=?",
                         (artifacts.target_id,)).fetchone()
        if row is None:
            raise SeveranceError("TARGET_ROW_NOT_FOUND")
        original = row[0]
        body = json.loads(original)
        body["record_preimage"]["governed_payload"]["practice_label"] = "FAULTED_LABEL"
        db.execute("UPDATE target_state SET body=? WHERE id=?",
                   (json.dumps(body, sort_keys=True, separators=(",", ":")),
                    artifacts.target_id))
        db.commit()

    def restore() -> None:
        with sqlite3.connect(path) as db:
            db.execute("UPDATE target_state SET body=? WHERE id=?",
                       (original, artifacts.target_id))
            db.commit()
    return restore


def _cut_e2_self_actuator(artifacts: BP2Artifacts) -> dict:
    receipt = dict(artifacts.e2_receipt or {})
    if not receipt:
        raise SeveranceError("E2_RECEIPT_MISSING")
    receipt = dict(receipt)
    receipt["actuator_ref"] = artifacts.life.a_source.actor_id
    receipt.pop("hash", None)
    from candidate import seal

    return seal(receipt)


def _prepare_m6_perception_fault(root: Path, artifacts: BP2Artifacts) -> None:
    """Create the product root, then delete actor A's arrival perception."""
    from .product import JoinedProduct

    product = JoinedProduct(root, artifacts=artifacts)
    product.close()
    db_path = Path(root) / "c12.sqlite"
    with sqlite3.connect(db_path) as db:
        db.execute("DROP TRIGGER IF EXISTS perception_no_delete")
        db.execute(
            "DELETE FROM perception WHERE branch_id='root' AND actor_id='A'")
        db.commit()


# ---------------------------------------------------------------------------
# trials
# ---------------------------------------------------------------------------
def _fresh(destination: Path) -> BP2Artifacts:
    """Run BP2's producer at a trial-specific root.

    The BP3 journal identity binds the absolute journal path, so a copied
    artifact directory cannot keep a valid keyed proof. Each file-mutation trial
    therefore produces its own real BP2 run in place.
    """
    from .reunion import build_fresh

    return build_fresh(destination)


def run_severance(edge: str, workdir, intact: BP2Artifacts, *,
                  product_cls=None) -> SeveranceTrial:
    if edge not in EDGE_CUT_DESCRIPTION:
        raise ValueError("unknown severance edge: " + edge)
    base = Path(workdir) / edge.lower()
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)

    # ---- baseline on the intact artifacts ----
    baseline = _run(base / "baseline_root", intact, product_cls=product_cls)

    # ---- fault ----
    fault_root = base / "fault_root"
    restore_bytes: Callable[[], None] | None = None
    kwargs: dict[str, Any] = {}
    prepare: Callable[[Path, BP2Artifacts], None] | None = None
    same_root = True

    if edge == "BP2_C8_PROOF":
        fault_artifacts = _fresh(base / "fault_artifacts")
        restore_bytes = _cut_anchor_watermark(fault_artifacts)
    elif edge == "BP2_ACTOR_HISTORY":
        fault_artifacts = _cut_actor_history(intact)
    elif edge == "BP2_OTHER_HISTORY_ALIASED":
        fault_artifacts = _cut_other_history(intact)
    elif edge == "BP2_RULE_A":
        fault_artifacts = _fresh(base / "fault_artifacts")
        restore_bytes = _cut_response_row(fault_artifacts)
    elif edge == "BP2_RULE_T":
        fault_artifacts = _fresh(base / "fault_artifacts")
        restore_bytes = _cut_target_journal(fault_artifacts)
    elif edge == "BP2_TARGET_HASH":
        fault_artifacts = _fresh(base / "fault_artifacts")
        restore_bytes = _cut_target_preimage(fault_artifacts)
    elif edge == "BP2_E2":
        fault_artifacts = intact
        kwargs["e2"] = _cut_e2_self_actuator(intact)
    elif edge == "BP2_E2_NOT_PERFORMED":
        fault_artifacts = intact
        kwargs["e2"] = None
    elif edge == "BP2_PRACTICE_NOT_MATERIALIZED":
        fault_artifacts = intact
        kwargs["materialize"] = False
    elif edge == "BP4_C10_M6_ACCESS":
        fault_artifacts = intact
        prepare = _prepare_m6_perception_fault
        same_root = False
    else:  # pragma: no cover - guarded above
        raise ValueError(edge)

    if prepare is not None:
        prepare(fault_root, fault_artifacts)
    red = _run(fault_root, fault_artifacts, product_cls=product_cls, **kwargs)

    # ---- restoration ----
    if same_root:
        if restore_bytes is not None:
            restore_bytes()
            restored_artifacts = fault_artifacts
        else:
            # Parameter faults (life/source/E2/practice) changed no bytes; the
            # original source is restored by using the intact artifacts and the
            # default parameters.
            restored_artifacts = intact
        restored = _run(
            base / "restored_root", restored_artifacts,
            product_cls=product_cls)
        restore_basis = ("same_root_exact_bytes_restored"
                         if restore_bytes is not None
                         else "same_root_original_source_restored")
    else:
        restored = _run(
            base / "restored_root", fault_artifacts,
            product_cls=product_cls)
        restore_basis = "fresh_c12_root_same_bp2_artifacts"

    return SeveranceTrial(
        edge=edge,
        assertion=ASSERTION_NAME,
        cut=EDGE_CUT_DESCRIPTION[edge],
        baseline=baseline,
        red=red,
        restored=restored,
        restore_basis=restore_basis,
        same_root=same_root,
        supplementary=edge in SUPPLEMENTARY_EDGES,
    )


def run_all_severances(workdir, intact: BP2Artifacts, *,
                       product_cls=None) -> list[SeveranceTrial]:
    trials = []
    for edge in SEVERANCE_EDGES:
        trials.append(run_severance(edge, Path(workdir) / "primary", intact,
                                    product_cls=product_cls))
    for edge in SUPPLEMENTARY_EDGES:
        trials.append(run_severance(edge, Path(workdir) / "supplementary", intact,
                                    product_cls=product_cls))
    return trials


def severance_receipt(trials: list[SeveranceTrial]) -> dict:
    primary = [trial for trial in trials if not trial.supplementary]
    supplementary = [trial for trial in trials if trial.supplementary]
    return {
        "schema": "BP2P4J_SEVERANCE_RECEIPT@1",
        "named_assertion": ASSERTION_NAME,
        "edge_count": len(primary),
        "supplementary_count": len(supplementary),
        "all_primary_proved": all(trial.proves for trial in primary),
        "all_supplementary_proved": all(trial.proves for trial in supplementary),
        "edges": [trial.edge for trial in primary],
        "trials": [trial.as_dict() for trial in trials],
    }


__all__ = [
    "EDGE_CUT_DESCRIPTION",
    "SEVERANCE_EDGES",
    "SUPPLEMENTARY_EDGES",
    "SeveranceError",
    "SeveranceTrial",
    "run_all_severances",
    "run_severance",
    "severance_receipt",
]
