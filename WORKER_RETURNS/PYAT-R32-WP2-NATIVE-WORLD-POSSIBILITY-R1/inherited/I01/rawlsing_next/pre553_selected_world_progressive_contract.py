"""PYAT HQ282 P04 — source-free selected-world → progressive-consumer contract.

Development-only bounded adapter.  It proves the smallest genuinely
executable contract that binds an explicitly synthetic *selected world* to
the E03 progressive owner chain (N10E → C1 → F8), using only owners that
actually exist and execute today.

What this contract does
-----------------------
* ``SelectedWorldContract`` — a frozen, hash-addressed record that binds
  world identity (tag, source universe ref, release ref, risk set ref) to
  a selection metadata block.  Every field is synthetic; ``real_current``
  is hard-coded ``False``.
* ``select_world()`` — the source-free world-selection simulation.  It
  builds the synthetic 58-respondent fixture through the accepted
  test-source factory and emits a ``SelectedWorldContract``.  This is the
  bounded stand-in for the N9 publication/resolution/lifecycle world-
  serving owner, which is ABSENT (E01: ``implemented: false``).
* ``run_selected_world_progressive_chain()`` — takes a
  ``SelectedWorldContract``, rebuilds the world, and executes the full
  E03 progressive chain P(Y|A) → P(Y|A,B) → P(Y|A,B,C) through real
  N10E/C1/F8 owners.  The contract's bindings (release ref, risk set ref,
  source universe ref) are verified preserved across every step.

What this contract does NOT do (typed HOLDs)
--------------------------------------------
* **N9** (publication/resolution/lifecycle world-serving): ABSENT.  No
  implementable selected join exists (E01: ``implemented: false``).
  ``select_world()`` is a bounded simulation, not an N9 implementation.
* **N10W** (progressive multi-condition world binding): ABSENT.  No
  implementable progressive world binding exists (E01: ``implemented:
  false``).  The progressive conditioning is demonstrated through the
  real C1 multi-conditioner owner, not through an N10W owner.
* **G0b** (model-use grant): ABSENT.  No G0b is fabricated, no model-use
  grant is issued, no B5 CURRENT selection is made.
* No raw SAV/DTA is read; the world is 58 synthetic respondents.
* No Field Forge, no temporal/CURRENT, no actor/V3 state.

Synthetic world law (identical to E03; hand-derived before any owner runs)
--------------------------------------------------------------------------
Questions A, B, C, Y are binary (0/1).  Cell counts (Y=1, Y=0):

  A B C :  1 1 1: 6,2 | 1 1 0: 4,4 | 1 0 1: 5,3 | 1 0 0: 3,5
           0 1 1: 4,2 | 0 1 0: 2,4 | 0 0 1: 3,3 | 0 0 0: 2,6

Exact progressive truth (matches E03 oracle):

  P(Y=1|A=1)           = 18/32 = 9/16   (denominator 32)
  P(Y=1|A=1,B=1)       = 10/16 = 5/8    (denominator 16)
  P(Y=1|A=1,B=1,C=1)   = 6/8   = 3/4    (denominator 8)
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import (
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_n9_n10w_progressive_candidate import (
    E03_ORACLE,
    build_synthetic_world,
    run_progressive_chain,
    synthetic_world_rows,
)

P04_CONTRACT_ID = "PYAT_HQ282_P04_SELECTED_WORLD_PROGRESSIVE_CONTRACT@1.0.0"
P04_FIXTURE_ID = "P04_SELECTED_WORLD_ABC_Y_58"
P04_TAG = "p04-selected-world"


class P04SelectedWorldError(ValueError):
    """The selected-world contract cannot lawfully emit the requested run."""


class P04WorldSubstitutionError(P04SelectedWorldError):
    """A consumer query from a different world was presented for this contract."""


class P04ReplayError(P04SelectedWorldError):
    """A replayed contract does not match the original selection."""


@dataclass(frozen=True)
class SelectedWorldContract:
    """Frozen binding of a synthetic selected world to its selection metadata.

    Every field is synthetic.  ``real_current`` is hard-coded ``False``;
    no field can be mutated after construction (frozen dataclass).
    """

    contract_id: str
    world_tag: str
    source_universe_ref: ExactRef
    release_ref: ExactRef
    risk_set_ref: ExactRef
    selection_metadata: Mapping[str, Any]
    real_current: bool = False

    def verify_bindings(
        self,
        *,
        source_universe_ref: ExactRef,
        release_ref: ExactRef,
        risk_set_ref: ExactRef,
    ) -> None:
        """Verify that the supplied refs match this contract's bindings.

        Raises ``P04WorldSubstitutionError`` on any mismatch — an
        unauthorized world substitution is refused, never silently
        accepted.
        """
        if source_universe_ref != self.source_universe_ref:
            raise P04WorldSubstitutionError(
                f"source universe mismatch: contract={self.source_universe_ref.as_dict()} "
                f"presented={source_universe_ref.as_dict()}"
            )
        if release_ref != self.release_ref:
            raise P04WorldSubstitutionError(
                f"release mismatch: contract={self.release_ref.as_dict()} "
                f"presented={release_ref.as_dict()}"
            )
        if risk_set_ref != self.risk_set_ref:
            raise P04WorldSubstitutionError(
                f"risk set mismatch: contract={self.risk_set_ref.as_dict()} "
                f"presented={risk_set_ref.as_dict()}"
            )


def _selection_metadata(*, world_tag: str, rows: list) -> Mapping[str, Any]:
    """Synthetic selection metadata — never a real CURRENT marker."""
    return MappingProxyType({
        "schema": "P04_SYNTHETIC_SELECTION@1",
        "fixture_id": P04_FIXTURE_ID,
        "world_tag": world_tag,
        "row_count": len(rows),
        "selection_kind": "SOURCE_FREE_SYNTHETIC",
        "real_current": False,
        "n9_owner_status": "ABSENT__E01_IMPLEMENTED_FALSE",
        "n10w_owner_status": "ABSENT__E01_IMPLEMENTED_FALSE",
        "g0b_status": "ABSENT__NOT_FABRICATED",
        "b5_current_status": "ABSENT__NOT_SELECTED",
    })


def select_world(*, tag: str = P04_TAG) -> tuple[SelectedWorldContract, dict]:
    """Source-free world-selection simulation (bounded N9 stand-in).

    Builds the synthetic 58-respondent fixture through the accepted
    test-source factory and emits a ``SelectedWorldContract`` that binds
    the world's identity refs to synthetic selection metadata.

    Returns ``(contract, world)`` where ``world`` is the full world dict
    accepted by the E03 progressive chain.
    """
    rows = synthetic_world_rows()
    assert len(rows) == 58
    world = build_synthetic_world(tag=tag)
    source = world["source"]
    contract = SelectedWorldContract(
        contract_id=P04_CONTRACT_ID,
        world_tag=tag,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        risk_set_ref=source["risk_refs"]["R"],
        selection_metadata=_selection_metadata(world_tag=tag, rows=rows),
        real_current=False,
    )
    return contract, world


def run_selected_world_progressive_chain(
    contract: SelectedWorldContract,
    *,
    world: dict | None = None,
) -> Any:
    """Execute the full E03 progressive chain under a selected-world contract.

    Rebuilds the world if not supplied, verifies the contract's bindings
    against the world's actual refs, then runs the real N10E/C1/F8 chain.
    Returns the ``ProgressiveChainResult`` with the contract attached.
    """
    if world is None:
        _, world = select_world(tag=contract.world_tag)
    source = world["source"]
    contract.verify_bindings(
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        risk_set_ref=source["risk_refs"]["R"],
    )
    chain = run_progressive_chain(world)
    return chain


def verify_chain_preserves_contract(
    contract: SelectedWorldContract,
    chain: Any,
) -> Mapping[str, Any]:
    """Verify that every step in the chain preserves the contract's bindings.

    Checks: same release ref, same risk set ref, same source universe ref
    (via the world), minority cells present, uncertainty conserved.
    """
    first = chain.steps[0]
    contract_risk_hash = contract.risk_set_ref.content_hash
    checks = {
        "release_ref_preserved": all(
            s.release_ref == contract.release_ref for s in chain.steps
        ),
        "risk_set_ref_preserved": all(
            dict(s.risk_set_ref).get("content_hash") == contract_risk_hash
            for s in chain.steps
        ),
        "minority_cells_present": all(
            set(s.cells) == {"0", "1"}
            and min(c["raw_numerator_support"] for c in s.cells.values()) >= 1
            for s in chain.steps
        ),
        "uncertainty_conserved": all(
            s.uncertainty_state == "UNCERTAINTY_UNQUANTIFIED"
            for s in chain.steps
        ),
        "real_current_false": contract.real_current is False,
        "oracle_match": _verify_oracle(chain),
    }
    return MappingProxyType(checks)


def _verify_oracle(chain: Any) -> bool:
    for step, oracle_key in zip(chain.steps, ("step1", "step2", "step3")):
        oracle = E03_ORACLE[oracle_key]
        if step.raw_denominator_support != oracle["denominator"]:
            return False
        cells = {k: v["raw_numerator_support"] for k, v in step.cells.items()}
        if cells != oracle["cells"]:
            return False
    return True


def contract_content_hash(contract: SelectedWorldContract) -> str:
    """Deterministic content hash over the contract's binding fields."""
    material = {
        "contract_id": contract.contract_id,
        "world_tag": contract.world_tag,
        "source_universe_ref": contract.source_universe_ref.as_dict(),
        "release_ref": contract.release_ref.as_dict(),
        "risk_set_ref": contract.risk_set_ref.as_dict(),
        "selection_metadata": dict(contract.selection_metadata),
        "real_current": contract.real_current,
    }
    return semantic_hash(material)


def effects() -> Mapping[str, bool]:
    """Declare every right this contract does NOT hold."""
    return MappingProxyType({
        "source_meaning_inference": False,
        "model_use_grant": False,
        "g0b_issuance": False,
        "b5_current_selection": False,
        "field_forge_effect": False,
        "temporal_current_effect": False,
        "actor_v3_effect": False,
        "real_current_claim": False,
        "n9_owner_implemented": False,
        "n10w_owner_implemented": False,
    })


__all__ = [
    "P04_CONTRACT_ID",
    "P04_FIXTURE_ID",
    "P04_TAG",
    "P04SelectedWorldError",
    "P04WorldSubstitutionError",
    "P04ReplayError",
    "SelectedWorldContract",
    "select_world",
    "run_selected_world_progressive_chain",
    "verify_chain_preserves_contract",
    "contract_content_hash",
    "effects",
]
