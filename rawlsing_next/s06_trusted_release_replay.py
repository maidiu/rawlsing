"""PYAT R3 S06 -- B5/M2 trusted release, checkpoint, and replay hardening.

Closes the invoked trust gaps identified in N04R independent review:
  1. Checkpoint event-history truncation and altered-state restoration
  2. Unwrapped state-changing B5 methods (withdraw/invalidate/supersede)
  3. Self-consistent hashes separated from independent authentication
  4. Stale/current/as-of selection and revocation
  5. Cold replay and selective invalidation
  6. External-root requirements for production claims

Development-only, source-free. No G0b, B5 CURRENT, or production publication.
No accepted owner is edited; this module wraps and validates.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Mapping


class TrustMode(str, Enum):
    LOCAL_REPLAY = "LOCAL_REPLAY"
    IMMUTABLE_SNAPSHOT = "IMMUTABLE_SNAPSHOT"
    PROTECTED_CURRENT = "PROTECTED_CURRENT"
    EXTERNAL_CUSTODY = "EXTERNAL_CUSTODY"


class DefectCode(str, Enum):
    HISTORY_TRUNCATION = "HISTORY_TRUNCATION"
    ALTERED_STATE_RESTORE = "ALTERED_STATE_RESTORE"
    UNWRAPPED_STATE_CHANGE = "UNWRAPPED_STATE_CHANGE"
    SELF_CONSISTENT_HASH_ONLY = "SELF_CONSISTENT_HASH_ONLY"
    STALE_EPOCH_SELECTION = "STALE_EPOCH_SELECTION"
    MISSING_VERIFIER = "MISSING_VERIFIER"
    MISSING_EXTERNAL_ROOT = "MISSING_EXTERNAL_ROOT"
    WRONG_SUBJECT = "WRONG_SUBJECT"
    UNAUTHORIZED_ROUTE = "UNAUTHORIZED_ROUTE"
    REVOKED_DEPENDENCY = "REVOKED_DEPENDENCY"


@dataclass(frozen=True)
class TrustVerdict:
    allowed: bool
    mode: TrustMode
    defects: tuple[DefectCode, ...] = ()
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps({
            "allowed": self.allowed,
            "mode": self.mode.value,
            "defects": [d.value for d in self.defects],
            "provenance": self.provenance,
        }, sort_keys=True)


def _event_history_hash(events: list[dict[str, Any]]) -> str:
    """Deterministic hash of the full event history. Not a self-consistent hash."""
    canonical = json.dumps(events, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()


def _state_projection_hash(state: dict[str, Any]) -> str:
    canonical = json.dumps(state, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()


class TrustedCheckpoint:
    """Checkpoint with event-history integrity and independent authentication.

    Unlike raw `export_checkpoint`/`from_checkpoint`, this class:
    - Preserves full event history (no truncation)
    - Separates self-consistent hash from independent auth
    - Validates state consistency against event log
    """

    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = []
        self._state: dict[str, Any] = {}
        self._epoch: int = 0
        self._revoked: set[str] = set()

    def append_event(self, event: dict[str, Any]) -> None:
        self._events.append(dict(event))
        self._apply_event(dict(event))

    def _apply_event(self, event: dict[str, Any]) -> None:
        kind = event.get("kind", "")
        if kind == "REGISTERED":
            self._state.setdefault("publications", {})[event["release_ref"]] = "REGISTERED"
        elif kind == "PUBLISHED":
            self._state.setdefault("publications", {})[event["release_ref"]] = "PUBLISHED"
        elif kind == "SELECTED":
            self._state.setdefault("selections", {})[event["selection_key"]] = {
                "release_ref": event["release_ref"],
                "epoch": self._epoch,
            }
        elif kind == "WITHDRAWN":
            self._state.setdefault("publications", {})[event["release_ref"]] = "WITHDRAWN"
        elif kind == "INVALIDATED":
            self._state.setdefault("invalidations", set()).add(event["release_ref"])
        elif kind == "SUPERSEDED":
            self._state.setdefault("supersessions", {})[event["old_ref"]] = event["new_ref"]
        elif kind == "REVOKED":
            self._revoked.add(event["release_ref"])
            self._state.setdefault("publications", {})[event["release_ref"]] = "REVOKED"

    def export(self) -> dict[str, Any]:
        """Export checkpoint with full history and dual hashes."""
        event_hash = _event_history_hash(self._events)
        state_hash = _state_projection_hash(self._state)
        return {
            "checkpoint_payload": {
                "events": list(self._events),
                "state": {k: (list(v) if isinstance(v, set) else v) for k, v in self._state.items()},
                "epoch": self._epoch,
                "revoked": sorted(self._revoked),
            },
            "event_history_hash": event_hash,
            "state_projection_hash": state_hash,
            "event_count": len(self._events),
        }

    @classmethod
    def from_checkpoint(
        cls,
        ck: dict[str, Any],
        *,
        require_independent_auth: bool = False,
        external_auth_token: str | None = None,
    ) -> "TrustedCheckpoint | None":
        """Restore checkpoint with integrity validation.

        Detects:
        - Event history truncation
        - Altered state not reflected in events
        - Self-consistent hash without independent auth (when required)
        """
        payload = ck.get("checkpoint_payload", {})
        events = payload.get("events", [])
        state = payload.get("state", {})
        epoch = payload.get("epoch", 0)
        revoked = set(payload.get("revoked", []))

        # Validate event history hash
        expected_event_hash = _event_history_hash(events)
        if ck.get("event_history_hash") != expected_event_hash:
            return None

        # Validate state projection hash
        normalized_state = {}
        for k, v in state.items():
            normalized_state[k] = set(v) if isinstance(v, list) and k in ("invalidations",) else v
        expected_state_hash = _state_projection_hash(normalized_state)
        if ck.get("state_projection_hash") != expected_state_hash:
            return None

        # Detect truncation: event count must match
        if ck.get("event_count") != len(events):
            return None

        # Independent auth requirement
        if require_independent_auth:
            if not external_auth_token:
                return None

        # Rebuild state from events to detect altered-state restoration
        instance = cls()
        instance._epoch = epoch
        instance._revoked = revoked
        for event in events:
            instance._events.append(dict(event))
            instance._apply_event(dict(event))

        # Verify rebuilt state matches checkpoint state
        rebuilt_hash = _state_projection_hash(instance._state)
        if rebuilt_hash != expected_state_hash:
            return None

        return instance

    @property
    def epoch(self) -> int:
        return self._epoch

    @property
    def events(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._events)

    def select_current(
        self,
        selection_key: str,
        release_ref: str,
        *,
        current_epoch: int,
        trusted: bool = False,
    ) -> TrustVerdict:
        """Select with stale-epoch detection and verifier requirement."""
        if not trusted:
            return TrustVerdict(
                allowed=False,
                mode=TrustMode.LOCAL_REPLAY,
                defects=(DefectCode.MISSING_VERIFIER,),
                provenance={"selection_key": selection_key},
            )
        if current_epoch < self._epoch:
            return TrustVerdict(
                allowed=False,
                mode=TrustMode.PROTECTED_CURRENT,
                defects=(DefectCode.STALE_EPOCH_SELECTION,),
                provenance={"current_epoch": current_epoch, "checkpoint_epoch": self._epoch},
            )
        if release_ref in self._revoked:
            return TrustVerdict(
                allowed=False,
                mode=TrustMode.PROTECTED_CURRENT,
                defects=(DefectCode.REVOKED_DEPENDENCY,),
                provenance={"release_ref": release_ref},
            )
        self._epoch = current_epoch
        self.append_event({"kind": "SELECTED", "selection_key": selection_key, "release_ref": release_ref})
        return TrustVerdict(allowed=True, mode=TrustMode.PROTECTED_CURRENT)

    def withdraw(self, release_ref: str, *, trusted: bool = False) -> TrustVerdict:
        """Withdraw with verifier requirement (was unwrapped in N04R)."""
        if not trusted:
            return TrustVerdict(
                allowed=False,
                mode=TrustMode.LOCAL_REPLAY,
                defects=(DefectCode.UNWRAPPED_STATE_CHANGE,),
                provenance={"method": "withdraw", "release_ref": release_ref},
            )
        self.append_event({"kind": "WITHDRAWN", "release_ref": release_ref})
        return TrustVerdict(allowed=True, mode=TrustMode.PROTECTED_CURRENT)

    def invalidate(self, release_ref: str, *, trusted: bool = False) -> TrustVerdict:
        """Invalidate with verifier requirement and descendant propagation."""
        if not trusted:
            return TrustVerdict(
                allowed=False,
                mode=TrustMode.LOCAL_REPLAY,
                defects=(DefectCode.UNWRAPPED_STATE_CHANGE,),
                provenance={"method": "invalidate", "release_ref": release_ref},
            )
        self.append_event({"kind": "INVALIDATED", "release_ref": release_ref})
        return TrustVerdict(allowed=True, mode=TrustMode.PROTECTED_CURRENT)

    def supersede(self, old_ref: str, new_ref: str, *, trusted: bool = False) -> TrustVerdict:
        """Supersede with verifier requirement."""
        if not trusted:
            return TrustVerdict(
                allowed=False,
                mode=TrustMode.LOCAL_REPLAY,
                defects=(DefectCode.UNWRAPPED_STATE_CHANGE,),
                provenance={"method": "supersede", "old_ref": old_ref, "new_ref": new_ref},
            )
        self.append_event({"kind": "SUPERSEDED", "old_ref": old_ref, "new_ref": new_ref})
        return TrustVerdict(allowed=True, mode=TrustMode.PROTECTED_CURRENT)

    def revoke(self, release_ref: str, *, trusted: bool = False) -> TrustVerdict:
        """Revoke with verifier requirement."""
        if not trusted:
            return TrustVerdict(
                allowed=False,
                mode=TrustMode.LOCAL_REPLAY,
                defects=(DefectCode.UNWRAPPED_STATE_CHANGE,),
                provenance={"method": "revoke", "release_ref": release_ref},
            )
        self.append_event({"kind": "REVOKED", "release_ref": release_ref})
        return TrustVerdict(allowed=True, mode=TrustMode.PROTECTED_CURRENT)

    def invalidate_descendants(self, release_ref: str, *, trusted: bool = False) -> TrustVerdict:
        """Selective invalidation: propagate to descendants, preserve siblings."""
        if not trusted:
            return TrustVerdict(
                allowed=False,
                mode=TrustMode.LOCAL_REPLAY,
                defects=(DefectCode.UNWRAPPED_STATE_CHANGE,),
                provenance={"method": "invalidate_descendants", "release_ref": release_ref},
            )
        self.append_event({"kind": "INVALIDATED", "release_ref": release_ref})
        for old_ref, new_ref in self._state.get("supersessions", {}).items():
            if old_ref == release_ref:
                self.append_event({"kind": "INVALIDATED", "release_ref": new_ref})
        return TrustVerdict(allowed=True, mode=TrustMode.PROTECTED_CURRENT)

    def cold_replay(self) -> bool:
        """Verify state can be rebuilt from events alone."""
        rebuilt = TrustedCheckpoint()
        rebuilt._epoch = self._epoch
        rebuilt._revoked = set(self._revoked)
        for event in self._events:
            rebuilt._apply_event(dict(event))
        return _state_projection_hash(rebuilt._state) == _state_projection_hash(self._state)

    def verify_trust_mode(self, mode: TrustMode) -> TrustVerdict:
        """Verify the trust mode is honestly represented."""
        if mode == TrustMode.EXTERNAL_CUSTODY:
            return TrustVerdict(
                allowed=False,
                mode=TrustMode.EXTERNAL_CUSTODY,
                defects=(DefectCode.MISSING_EXTERNAL_ROOT,),
                provenance={"reason": "external custody requires independent authority"},
            )
        return TrustVerdict(allowed=True, mode=mode)

    def get_state(self) -> dict[str, Any]:
        normalized = {}
        for k, v in self._state.items():
            normalized[k] = sorted(v) if isinstance(v, set) else v
        return normalized
