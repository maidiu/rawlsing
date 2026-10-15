"""Reviewer path composition; all candidate bytes remain pinned and unchanged."""

from pathlib import Path
import sys, os

R = Path(__file__).resolve().parents[1]
M = R / "runtime/m01"
sys.path.insert(0, str(M / "repro"))
import bootstrap
from cell import Cell, Refusal, owner, old, digest, VERSION
from candidate.positive_chain import (
    seal_event,
    run_positive_chain,
    LedgerIntegrityError,
)
from candidate.candidate_registry_fixture import event_digest


def native_epistemic(cell, access="CLAIM_ACCESSIBLE", operation="ADD", target=None):
    return dict(
        actor_id=cell.ctx.actor_id,
        claim_ref=cell.claim_id,
        stance_kind="BELIEF",
        stance_operation=operation,
        causal_parent_refs=[cell.e1.event_id],
        actor_facing_basis_refs=[cell.e1.event_id + ":" + cell.e1.event_hash],
        memory_basis_refs=[],
        owning_rule_id=cell.binding.rule_id,
        owning_rule_version=cell.binding.rule_version,
        owning_rule_hash=cell.binding.rule_content_hash,
        effective_causal_time=cell.e1.effective_causal_time,
        claim_accessibility=access,
        context=cell.ctx,
        pre_state_hash=cell.ctx.state_hash,
        target_record_ref=target,
    )
