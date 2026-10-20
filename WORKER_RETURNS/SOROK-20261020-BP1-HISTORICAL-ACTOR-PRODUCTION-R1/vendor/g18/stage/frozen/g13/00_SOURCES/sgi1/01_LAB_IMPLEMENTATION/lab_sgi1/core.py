"""S-GI1 lab core: canonical hashing, deterministic receipted RNG, typed states.

PROVISIONAL_LAB_RULE__NOT_ADOPTED. Every stochastic operation is scoped, seeded and
receipted; no unreported redraws are possible at this layer.
"""
from __future__ import annotations

import hashlib
import json
import time
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import LAB_RULE_STATUS

# ---------------------------------------------------------------------------
# Canonical serialization / hashing
# ---------------------------------------------------------------------------

def canon(obj: Any) -> bytes:
    """Canonical JSON bytes: sorted keys, NFC-normalized strings, UTF-8, no float noise."""
    return json.dumps(
        _nfc(obj), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _nfc(obj: Any) -> Any:
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, dict):
        return {_nfc(k): _nfc(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_nfc(v) for v in obj]
    return obj


def h_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def h_obj(obj: Any) -> str:
    return h_bytes(canon(obj))


def h_concat(*parts: str) -> str:
    return h_bytes("\x1f".join(parts).encode("utf-8"))


# ---------------------------------------------------------------------------
# Typed states (S-G 02 §7 plus explicit lab boundary states)
# ---------------------------------------------------------------------------

class S:
    MOTHER_ANCHOR_MISSING = "MOTHER_ANCHOR_MISSING"
    TARGET_PENDING = "TARGET_PENDING"
    SCENARIOS_VALID_EMPTY = "SCENARIOS_VALID_EMPTY"
    SCENARIOS_UNKNOWN = "SCENARIOS_UNKNOWN"
    SCENARIO_INFEASIBLE = "SCENARIO_INFEASIBLE"
    SCENARIO_UNDERDETERMINED = "SCENARIO_UNDERDETERMINED"
    EMPIRICAL_USE_DENIED = "EMPIRICAL_USE_DENIED"
    GENERIC_QUERY_NONCOMPARABLE = "GENERIC_QUERY_NONCOMPARABLE"
    DEDUP_UNDERDETERMINED = "DEDUP_UNDERDETERMINED"
    SELECTION_AUTHORITY_UNBOUND = "SELECTION_AUTHORITY_UNBOUND"
    SELECTION_BIAS_UNQUANTIFIED_HOLD = "SELECTION_BIAS_UNQUANTIFIED_HOLD"
    ENDPOINT_INFEASIBLE = "ENDPOINT_INFEASIBLE"
    ENDPOINT_UNDERDETERMINED = "ENDPOINT_UNDERDETERMINED"
    HISTORY_SEARCH_EXHAUSTED = "HISTORY_SEARCH_EXHAUSTED"
    PREHISTORY_OWNER_RULE_MISSING = "PREHISTORY_OWNER_RULE_MISSING"
    INDEPENDENT_PROJECT_PROOF_MISSING = "INDEPENDENT_PROJECT_PROOF_MISSING"
    SHARED_HISTORY_CONTRADICTION_HOLD = "SHARED_HISTORY_CONTRADICTION_HOLD"
    CONCEPTION_BIOLOGY_AUTHORITY_HOLD = "CONCEPTION_BIOLOGY_AUTHORITY_HOLD"
    CHILD_GENERATION_NOT_ADMITTED = "CHILD_GENERATION_NOT_ADMITTED"
    ACTOR_INIT_HOLD = "ACTOR_INIT_HOLD"
    EXACT_REPLAY_DIVERGENCE = "EXACT_REPLAY_DIVERGENCE"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"
    COMMITTED = "COMMITTED"
    # lab-typed extensions (explicit, not silently folded into above)
    LAB_CONCEPTION_BOUNDARY = "LAB_CONCEPTION_BOUNDARY__NO_ADOPTED_BIOLOGICAL_SEMANTICS"
    LAB_PASS = "LAB_PASS_AT_DECLARED_GRAIN"
    FUTURE_CHILD_INFORMATION_LEAK = "FUTURE_CHILD_INFORMATION_LEAK"
    ACTOR_ID_COLLISION_OR_SUBJECT_REUSE_INTEGRITY_FAILURE = (
        "ACTOR_ID_COLLISION_OR_SUBJECT_REUSE_INTEGRITY_FAILURE"
    )
    AMBIGUOUS_SAME_TIME_CAUSAL_ORDER = "AMBIGUOUS_SAME_TIME_CAUSAL_ORDER"
    CAUSAL_TEMPORAL_INVERSION = "CAUSAL_TEMPORAL_INVERSION"
    NOT_EXECUTED_AUTHORITY_HOLD = "NOT_EXECUTED_AUTHORITY_HOLD"


# ---------------------------------------------------------------------------
# Deterministic receipted RNG (ADP020-style lab implementation)
# ---------------------------------------------------------------------------

@dataclass
class DrawReceipt:
    receipt_id: str
    stream: str
    scope_hash: str
    root_seed: str
    slot: str
    occurrence_index: int
    bound: int
    draw_value: int
    candidate_set_hash: str
    draw_index: int

    def as_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)


class ScopedRNG:
    """Counter-based deterministic stream. draw() emits a receipt; no silent draws.

    scope_hash MUST NOT contain any future-child outcome material. Callers pass a
    scope hash computed from (run id, mother anchor hash, target hash, grammar
    version, decision semantics version) only.
    """

    def __init__(self, root_seed: str, stream: str, scope_hash: str):
        self.root_seed = root_seed
        self.stream = stream
        self.scope_hash = scope_hash
        self.draws: List[DrawReceipt] = []
        self._counter = 0

    def _raw(self, slot: str, occurrence_index: int, n: int) -> int:
        digest = hashlib.sha256(
            "\x1e".join(
                [self.root_seed, self.stream, self.scope_hash, slot, str(occurrence_index), str(n)]
            ).encode("utf-8")
        ).digest()
        return int.from_bytes(digest[:8], "big")

    def draw(self, bound: int, slot: str, candidate_set_hash: str,
             occurrence_index: int = 0) -> DrawReceipt:
        if bound <= 0:
            raise ValueError("bound must be positive")
        idx = self._counter
        self._counter += 1
        val = self._raw(slot, occurrence_index, idx) % bound
        rec = DrawReceipt(
            receipt_id=h_concat("DRAW", self.stream, self.scope_hash, slot, str(idx)),
            stream=self.stream,
            scope_hash=self.scope_hash,
            root_seed=self.root_seed,
            slot=slot,
            occurrence_index=occurrence_index,
            bound=bound,
            draw_value=val,
            candidate_set_hash=candidate_set_hash,
            draw_index=idx,
        )
        self.draws.append(rec)
        return rec

    @property
    def draw_count(self) -> int:
        return len(self.draws)

    def ledger(self) -> Dict[str, Any]:
        return {
            "stream": self.stream,
            "scope_hash": self.scope_hash,
            "root_seed": self.root_seed,
            "draw_count": self.draws,
            "n_draws": len(self.draws),
        }


# ---------------------------------------------------------------------------
# Receipt / ledger plumbing
# ---------------------------------------------------------------------------

@dataclass
class CostCounters:
    model_calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    generic_queries: int = 0
    actor_events: int = 0
    history_attempts: int = 0
    rejected_candidates: int = 0
    rng_draws: int = 0
    replay_ledger_bytes: int = 0
    causal_state_changes: int = 0
    wall_seconds: float = 0.0
    replay_seconds: float = 0.0

    def as_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)


class Ledger:
    """Append-only receipt ledger. Every lab action leaves a typed receipt."""

    def __init__(self, name: str):
        self.name = name
        self.entries: List[Dict[str, Any]] = []
        self.t0 = time.perf_counter()

    def add(self, kind: str, payload: Dict[str, Any]) -> str:
        entry = {
            "seq": len(self.entries),
            "kind": kind,
            "t_offset_s": round(time.perf_counter() - self.t0, 6),
            "payload": payload,
        }
        entry["receipt_hash"] = h_obj(entry)
        self.entries.append(entry)
        return entry["receipt_hash"]

    def of_kind(self, kind: str) -> List[Dict[str, Any]]:
        return [e for e in self.entries if e["kind"] == kind]

    def as_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "entries": self.entries}

    def hash(self) -> str:
        return h_obj({"name": self.name, "entries": self.entries})


def typed(state: str, detail: Optional[Dict[str, Any]] = None, **extra: Any) -> Dict[str, Any]:
    out: Dict[str, Any] = {"status": state, "lab_rule": LAB_RULE_STATUS}
    if detail:
        out["detail"] = detail
    out.update(extra)
    return out
