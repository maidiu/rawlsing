"""Tests for S06 trusted release, checkpoint, and replay hardening.

Each test demonstrates a defect or its fix. A passing test that reproduces
an exploitable acceptance path is evidence of a defect, not safety.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rawlsing_next.s06_trusted_release_replay import (
    DefectCode,
    TrustMode,
    TrustVerdict,
    TrustedCheckpoint,
    _event_history_hash,
    _state_projection_hash,
)


def make_checkpoint_with_events():
    ck = TrustedCheckpoint()
    ck._epoch = 5
    ck.append_event({"kind": "REGISTERED", "release_ref": "rel-1"})
    ck.append_event({"kind": "PUBLISHED", "release_ref": "rel-1"})
    ck.append_event({"kind": "SELECTED", "selection_key": "key-1", "release_ref": "rel-1"})
    return ck


# --- Positive restore ---

def test_valid_checkpoint_restore():
    ck = make_checkpoint_with_events()
    exported = ck.export()
    restored = TrustedCheckpoint.from_checkpoint(exported)
    assert restored is not None
    assert len(restored.events) == 3
    assert restored.get_state()["publications"]["rel-1"] == "PUBLISHED"


def test_cold_replay_from_events():
    ck = make_checkpoint_with_events()
    assert ck.cold_replay() is True


def test_state_rebuilt_matches_checkpoint():
    ck = make_checkpoint_with_events()
    exported = ck.export()
    restored = TrustedCheckpoint.from_checkpoint(exported)
    assert restored is not None
    assert restored.get_state() == ck.get_state()


# --- Hostile negative restore: altered state ---

def test_altered_publication_state_rejected():
    """N04R defect: raw executor accepted altered state. Fix: reject."""
    ck = make_checkpoint_with_events()
    exported = ck.export()
    exported["checkpoint_payload"]["state"]["publications"]["rel-1"] = "REGISTERED"
    restored = TrustedCheckpoint.from_checkpoint(exported)
    assert restored is None


def test_truncated_event_history_rejected():
    """N04R defect: history truncation. Fix: reject."""
    ck = make_checkpoint_with_events()
    exported = ck.export()
    exported["checkpoint_payload"]["events"] = exported["checkpoint_payload"]["events"][:2]
    exported["event_count"] = 3
    exported["event_history_hash"] = _event_history_hash(exported["checkpoint_payload"]["events"])
    restored = TrustedCheckpoint.from_checkpoint(exported)
    assert restored is None


def test_bad_event_hash_rejected():
    ck = make_checkpoint_with_events()
    exported = ck.export()
    exported["event_history_hash"] = "0" * 64
    restored = TrustedCheckpoint.from_checkpoint(exported)
    assert restored is None


def test_bad_state_hash_rejected():
    ck = make_checkpoint_with_events()
    exported = ck.export()
    exported["state_projection_hash"] = "0" * 64
    restored = TrustedCheckpoint.from_checkpoint(exported)
    assert restored is None


def test_event_count_mismatch_rejected():
    ck = make_checkpoint_with_events()
    exported = ck.export()
    exported["event_count"] = 99
    restored = TrustedCheckpoint.from_checkpoint(exported)
    assert restored is None


# --- Mutation after checkpoint ---

def test_mutation_after_checkpoint_detected():
    ck = make_checkpoint_with_events()
    exported = ck.export()
    original_hash = exported["event_history_hash"]
    ck.append_event({"kind": "PUBLISHED", "release_ref": "rel-2"})
    assert ck.export()["event_history_hash"] != original_hash


# --- Self-consistent hash vs independent auth ---

def test_self_consistent_hash_not_independent_auth():
    """N04R defect: self-consistent hash treated as independent auth. Fix: separate."""
    ck = make_checkpoint_with_events()
    exported = ck.export()
    restored = TrustedCheckpoint.from_checkpoint(exported, require_independent_auth=True, external_auth_token=None)
    assert restored is None


def test_independent_auth_token_accepted():
    ck = make_checkpoint_with_events()
    exported = ck.export()
    restored = TrustedCheckpoint.from_checkpoint(exported, require_independent_auth=True, external_auth_token="valid-token")
    assert restored is not None


# --- Unwrapped state-changing methods ---

def test_unwrapped_withdraw_rejected_without_trust():
    """N04R defect: withdraw_product was unwrapped. Fix: require trust."""
    ck = make_checkpoint_with_events()
    verdict = ck.withdraw("rel-1", trusted=False)
    assert verdict.allowed is False
    assert DefectCode.UNWRAPPED_STATE_CHANGE in verdict.defects


def test_unwrapped_invalidate_rejected_without_trust():
    ck = make_checkpoint_with_events()
    verdict = ck.invalidate("rel-1", trusted=False)
    assert verdict.allowed is False
    assert DefectCode.UNWRAPPED_STATE_CHANGE in verdict.defects


def test_unwrapped_supersede_rejected_without_trust():
    ck = make_checkpoint_with_events()
    verdict = ck.supersede("rel-1", "rel-2", trusted=False)
    assert verdict.allowed is False
    assert DefectCode.UNWRAPPED_STATE_CHANGE in verdict.defects


def test_trusted_withdraw_accepted():
    ck = make_checkpoint_with_events()
    verdict = ck.withdraw("rel-1", trusted=True)
    assert verdict.allowed is True
    assert ck.get_state()["publications"]["rel-1"] == "WITHDRAWN"


# --- Stale/current/as-of selection ---

def test_stale_epoch_selection_rejected():
    ck = make_checkpoint_with_events()
    verdict = ck.select_current("key-1", "rel-1", current_epoch=0, trusted=True)
    assert verdict.allowed is False
    assert DefectCode.STALE_EPOCH_SELECTION in verdict.defects


def test_current_epoch_selection_accepted():
    ck = make_checkpoint_with_events()
    verdict = ck.select_current("key-2", "rel-1", current_epoch=5, trusted=True)
    assert verdict.allowed is True


def test_revoked_dependency_rejected():
    ck = make_checkpoint_with_events()
    ck.revoke("rel-1", trusted=True)
    verdict = ck.select_current("key-3", "rel-1", current_epoch=10, trusted=True)
    assert verdict.allowed is False
    assert DefectCode.REVOKED_DEPENDENCY in verdict.defects


# --- Selective invalidation ---

def test_invalidate_descendants_propagates():
    ck = make_checkpoint_with_events()
    ck.supersede("rel-1", "rel-2", trusted=True)
    ck.invalidate_descendants("rel-1", trusted=True)
    state = ck.get_state()
    assert "rel-1" in state.get("invalidations", [])
    assert "rel-2" in state.get("invalidations", [])


def test_unrelated_siblings_preserved():
    ck = make_checkpoint_with_events()
    ck.append_event({"kind": "REGISTERED", "release_ref": "rel-3"})
    ck.append_event({"kind": "PUBLISHED", "release_ref": "rel-3"})
    ck.supersede("rel-1", "rel-2", trusted=True)
    ck.invalidate_descendants("rel-1", trusted=True)
    state = ck.get_state()
    assert state["publications"]["rel-3"] == "PUBLISHED"
    assert "rel-3" not in state.get("invalidations", [])


# --- External root requirements ---

def test_external_custody_claim_rejected_without_root():
    """N04R defect: local replay treated as external custody. Fix: reject."""
    ck = make_checkpoint_with_events()
    verdict = ck.verify_trust_mode(TrustMode.EXTERNAL_CUSTODY)
    assert verdict.allowed is False
    assert DefectCode.MISSING_EXTERNAL_ROOT in verdict.defects


def test_local_replay_mode_accepted():
    ck = make_checkpoint_with_events()
    verdict = ck.verify_trust_mode(TrustMode.LOCAL_REPLAY)
    assert verdict.allowed is True


def test_immutable_snapshot_mode_accepted():
    ck = make_checkpoint_with_events()
    verdict = ck.verify_trust_mode(TrustMode.IMMUTABLE_SNAPSHOT)
    assert verdict.allowed is True


# --- Wrong subject ---

def test_wrong_subject_not_restored():
    ck = make_checkpoint_with_events()
    exported = ck.export()
    exported["checkpoint_payload"]["state"]["publications"] = {"rel-99": "PUBLISHED"}
    exported["state_projection_hash"] = _state_projection_hash(exported["checkpoint_payload"]["state"])
    restored = TrustedCheckpoint.from_checkpoint(exported)
    assert restored is None


# --- Replay determinism ---

def test_replay_deterministic():
    ck = make_checkpoint_with_events()
    e1 = ck.export()
    e2 = ck.export()
    assert e1["event_history_hash"] == e2["event_history_hash"]
    assert e1["state_projection_hash"] == e2["state_projection_hash"]


def test_dual_hash_distinct():
    """Self-consistent state hash and event history hash are distinct."""
    ck = make_checkpoint_with_events()
    exported = ck.export()
    assert exported["event_history_hash"] != exported["state_projection_hash"]
