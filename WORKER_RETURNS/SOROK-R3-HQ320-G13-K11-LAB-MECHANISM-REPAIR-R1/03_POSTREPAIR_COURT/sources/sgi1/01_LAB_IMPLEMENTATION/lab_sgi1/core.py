"""S-GI1 lab core: canonical hashing, deterministic receipted RNG, typed states.

PROVISIONAL_LAB_RULE__NOT_ADOPTED. Every stochastic operation is scoped, seeded and
receipted; no unreported redraws are possible at this layer.

G13 REPAIR (defect family 5 -- ADP020-compatible RNG).

The pre-repair laboratory sampler was a SHA256-concatenation digest reduced with
Python's ``%``. That is a modulo-biased, non-HMAC sampler with no seed lineage and
no rejection contract. It is NOT ADP-020 and was never labelled as ADP-020.

This module now implements the accepted ADP-020 mechanism for every lawful root:

  * ``ADP020_HMAC_SHA256_UNIFORM_BELOW_V1@1.0.0`` unbiased rejection mapping;
  * ``V3_CAUSAL_HMAC_SHA256_COUNTER_V1@1.0.0`` root -> scope -> stream seed lineage
    with the exact ADP-020 domain separator;
  * exact 32-byte/64-lowercase-hex root-seed validation (ADP-020 s5.1);
  * typed refusal of malformed roots before any draw.

The historical laboratory root tokens are retained ONLY as an explicitly
enumerated, receipted compatibility surface. They are NOT ADP-020 roots, they are
never reported as ADP-020 compliant, and every use raises the typed hold
``ADP020_REAL_ROOT_SEED_REQUIRED``. They exist so that the frozen historical
selection outcomes (and therefore the original 24 K11 cases and 98 predicates)
remain reproducible while the repaired sampler is the only mechanism available to
any new caller. They are not a grant and are not usable by any production,
V3, N12, actor or biological path.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import re
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
# Deterministic receipted RNG
#   G13 repair: accepted ADP-020 mechanism + declared legacy-token compatibility
# ---------------------------------------------------------------------------

ADP020_AUTHORITY = "ADP-020@1.0.0"
ADP020_SEED_SCHEME = "V3_CAUSAL_HMAC_SHA256_COUNTER_V1@1.0.0"
ADP020_SAMPLER = "ADP020_HMAC_SHA256_UNIFORM_BELOW_V1@1.0.0"
ADP020_DOMAIN_SEPARATOR = b"RAWLSING\x00ADP-020\x00V3_CAUSAL_HMAC_SHA256_COUNTER_V1\x00"

ADP020_ALLOWED_SCOPE_KINDS = ("RUN", "ACTOR", "JOINT", "GENEALOGY")
ADP020_STREAM_RE = re.compile(r"^v3\.causal\.[a-z0-9][a-z0-9_.-]{0,127}$")
_ROOT_HEX_RE = re.compile(r"^[0-9a-f]{64}$")

# Explicitly enumerated historical laboratory root tokens. Each is receipted as
# LEGACY_LAB_ROOT_TOKEN (non-ADP020) and raises ADP020_REAL_ROOT_SEED_REQUIRED.
# Provenance: the frozen SGI1 K11 runner (R0/R1/R2) and the frozen G12 assay
# harness (G12_SEED/G12). No other token is accepted.
DECLARED_LEGACY_LAB_ROOT_TOKENS = ("R0", "R1", "R2", "G12_SEED", "G12")

LEGACY_LAB_SAMPLER_NAME = "LEGACY_LAB_SHA256_CONCAT_MODULO_NOT_ADP020"

U64_MAX = 2 ** 64


class RngAuthorityError(ValueError):
    """Typed refusal raised before any draw when RNG metadata is not lawful."""

    def __init__(self, code: str, detail: Optional[Dict[str, Any]] = None):
        super().__init__(code)
        self.code = code
        self.detail = detail or {}


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
    # G13 repair: ADP-020 lineage + unbiased-mapping receipt fields.
    sampler: str = ADP020_SAMPLER
    authority: str = ADP020_AUTHORITY
    seed_scheme: str = ADP020_SEED_SCHEME
    root_seed_provenance: str = "EXPLICIT_CALLER_SEED"
    scope_kind: str = "GENEALOGY"
    scope_id: str = ""
    root_seed_sha256: str = ""
    scope_seed_sha256: str = ""
    stream_seed_sha256: str = ""
    entropy_block_count: int = 1
    accepted_raw_u64: int = 0
    rejection_limit_u64: int = 0
    draw_coordinate_hash: str = ""
    draw_replay_hash: str = ""
    adp020_entitlement: str = "SAMPLER_MECHANISM_CONFORMANT"
    hold: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)


def classify_root_seed(root_seed: str) -> Dict[str, Any]:
    """Classify a root seed as ADP020 lawful or a declared legacy lab token."""
    if not isinstance(root_seed, str) or not root_seed:
        raise RngAuthorityError(
            "RNG_ROOT_SEED_INVALID",
            {"reason": "root seed must be a non-empty string",
             "got_type": type(root_seed).__name__},
        )
    if _ROOT_HEX_RE.match(root_seed):
        return {
            "kind": "ADP020_EXACT_ROOT_SEED",
            "material": bytes.fromhex(root_seed),
            "root_seed_provenance": "EXPLICIT_CALLER_SEED",
            "adp020_entitlement": "SAMPLER_MECHANISM_CONFORMANT",
        }
    if root_seed in DECLARED_LEGACY_LAB_ROOT_TOKENS:
        return {
            "kind": "DECLARED_LEGACY_LAB_ROOT_TOKEN",
            "material": None,
            "root_seed_provenance": "LEGACY_LAB_ROOT_TOKEN",
            "adp020_entitlement": "NOT_GRANTED",
            "hold": "ADP020_REAL_ROOT_SEED_REQUIRED",
            "legacy_token": root_seed,
        }
    raise RngAuthorityError(
        "RNG_ROOT_SEED_INVALID",
        {"reason": "root seed must be 64 lowercase hex characters (ADP-020 s5.1) "
                   "or an explicitly declared historical laboratory token",
         "declared_legacy_lab_root_tokens": list(DECLARED_LEGACY_LAB_ROOT_TOKENS),
         "got_length": len(root_seed)},
    )


def _canonical_coordinate(obj: Dict[str, Any]) -> bytes:
    return json.dumps(_nfc(obj), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


class ScopedRNG:
    """Counter-derived, receipted, replayable scoped stream (G13 repaired).

    Lawful use (ADP-020 exact 32-byte root): HMAC seed lineage plus unbiased
    UNIFORM_BELOW rejection. Historical laboratory tokens fall back to the
    pre-repair sampler ONLY as an explicitly receipted, non-ADP020 compatibility
    surface that always carries the ADP020_REAL_ROOT_SEED_REQUIRED hold.
    """

    MAX_REJECTION_BLOCKS = 10000

    def __init__(self, root_seed: str, stream: str, scope_hash: str,
                 scope_kind: str = "GENEALOGY"):
        if not isinstance(stream, str) or not ADP020_STREAM_RE.match(stream):
            raise RngAuthorityError(
                "RNG_STREAM_UNREGISTERED",
                {"reason": "stream must match the ADP-020 v3.causal.* namespace",
                 "stream": stream if isinstance(stream, str) else type(stream).__name__},
            )
        if scope_kind not in ADP020_ALLOWED_SCOPE_KINDS:
            raise RngAuthorityError(
                "RNG_SCOPE_IDENTITY_MISSING",
                {"reason": "scope_kind must be one of RUN/ACTOR/JOINT/GENEALOGY",
                 "scope_kind": scope_kind},
            )
        if not isinstance(scope_hash, str) or not scope_hash:
            raise RngAuthorityError(
                "RNG_SCOPE_IDENTITY_MISSING",
                {"reason": "scope identity must be a non-empty string"},
            )

        # Root classification is DEFERRED to first draw so that an unlawful root
        # raises at the draw boundary (where a typed refusal belongs) rather than
        # at construction. `self.classification` is None until then.
        self._classification: Optional[Dict[str, Any]] = None
        self._legacy_mode = False
        self._scope_seed = self._stream_seed = b""
        self._scope_seed_sha256 = self._stream_seed_sha256 = ""
        self._root_seed_sha256 = ""
        self.root_seed = root_seed
        self.stream = stream
        self.scope_hash = scope_hash
        self.scope_kind = scope_kind
        self.scope_id = scope_hash
        self.draws: List[DrawReceipt] = []
        self._counter = 0

    # -- deferred root classification -----------------------------------
    @property
    def classification(self) -> Dict[str, Any]:
        self._ensure_classified()
        return self._classification

    @property
    def legacy_mode(self) -> bool:
        self._ensure_classified()
        return self._legacy_mode

    @property
    def root_seed_sha256(self) -> str:
        self._ensure_classified()
        return self._root_seed_sha256

    @property
    def scope_seed_sha256(self) -> str:
        self._ensure_classified()
        return self._scope_seed_sha256

    @property
    def stream_seed_sha256(self) -> str:
        self._ensure_classified()
        return self._stream_seed_sha256

    def _ensure_classified(self) -> None:
        """Classify the root seed and derive its lineage exactly once."""
        if self._classification is not None:
            return
        cls = classify_root_seed(self.root_seed)
        self._classification = cls
        self._legacy_mode = cls["kind"] == "DECLARED_LEGACY_LAB_ROOT_TOKEN"
        self._root_seed_sha256 = hashlib.sha256(
            (cls["material"] if not self._legacy_mode
             else b"LEGACY_LAB_ROOT_TOKEN\x00" + self.root_seed.encode("utf-8"))
        ).hexdigest()
        if self._legacy_mode:
            # No ADP-020 lineage is fabricated for a non-ADP020 root.
            self._scope_seed = self._stream_seed = b""
            self._scope_seed_sha256 = ""
            self._stream_seed_sha256 = ""
            return
        self._scope_seed = hmac.new(
            cls["material"],
            ADP020_DOMAIN_SEPARATOR
            + _canonical_coordinate({"kind": "scope", "scope_kind": self.scope_kind,
                                     "scope_id": self.scope_hash}),
            hashlib.sha256).digest()
        self._stream_seed = hmac.new(
            self._scope_seed,
            ADP020_DOMAIN_SEPARATOR
            + _canonical_coordinate({"kind": "stream", "stream_name": self.stream}),
            hashlib.sha256).digest()
        self._scope_seed_sha256 = self._scope_seed.hex()
        self._stream_seed_sha256 = self._stream_seed.hex()

    # -- entropy ---------------------------------------------------------
    def _raw(self, slot: str, occurrence_index: int, draw_index: int,
             block_index: int = 0, uniform_below_n: int = 0) -> int:
        """One entropy block. ADP-020 s8.1 for lawful roots."""
        coordinate = {
            "scope_kind": self.scope_kind,
            "scope_id": self.scope_id,
            "stream_name": self.stream,
            "anchor_event_index": -1,
            "anchor_event_id_or_init_checkpoint_hash": "INIT:" + self._scope_seed_sha256,
            "rule_invocation_id": "LAB_SOROK_G13_REPAIRED",
            "decision_slot": slot,
            "occurrence_index": occurrence_index,
            "draw_index": draw_index,
            "uniform_below_n": uniform_below_n,
            "block_index": block_index,
        }
        digest = hmac.new(
            self._stream_seed,
            ADP020_DOMAIN_SEPARATOR + _canonical_coordinate(coordinate),
            hashlib.sha256,
        ).digest()
        return int.from_bytes(digest[:8], "big")

    def _raw_legacy(self, slot: str, occurrence_index: int, draw_index: int) -> int:
        """Pre-repair laboratory sampler. RETAINED, NOT ADP-020, never disguised."""
        digest = hashlib.sha256(
            "\x1e".join([self.root_seed, self.stream, self.scope_hash, slot,
                         str(occurrence_index), str(draw_index)]).encode("utf-8")
        ).digest()
        return int.from_bytes(digest[:8], "big")

    # -- draw ------------------------------------------------------------
    def draw(self, bound: int, slot: str, candidate_set_hash: str,
             occurrence_index: int = 0) -> DrawReceipt:
        self._ensure_classified()
        if not isinstance(bound, int) or bound <= 0 or bound > U64_MAX - 1:
            raise RngAuthorityError(
                "RNG_STOCHASTIC_PARAMETERS_INVALID",
                {"reason": "bound must satisfy 1 <= n <= 2**64-1", "bound": bound},
            )
        idx = self._counter
        self._counter += 1

        if self._legacy_mode:
            val = self._raw_legacy(slot, occurrence_index, idx) % bound
            rec = DrawReceipt(
                receipt_id=h_concat("DRAW", self.stream, self.scope_hash, slot, str(idx)),
                stream=self.stream, scope_hash=self.scope_hash, root_seed=self.root_seed,
                slot=slot, occurrence_index=occurrence_index, bound=bound,
                draw_value=val, candidate_set_hash=candidate_set_hash, draw_index=idx,
                sampler=LEGACY_LAB_SAMPLER_NAME,
                authority="NONE__NOT_ADP020",
                seed_scheme="LEGACY_LAB_SHA256_CONCAT_V0",
                root_seed_provenance=self._classification["root_seed_provenance"],
                scope_kind=self.scope_kind, scope_id=self.scope_id,
                root_seed_sha256=self._root_seed_sha256,
                entropy_block_count=1,
                accepted_raw_u64=self._raw_legacy(slot, occurrence_index, idx),
                rejection_limit_u64=0,
                adp020_entitlement="NOT_GRANTED",
                hold="ADP020_REAL_ROOT_SEED_REQUIRED",
            )
            self.draws.append(rec)
            return rec

        # ADP-020 s8.1 UNIFORM_BELOW(n) with rejection.
        limit = U64_MAX - (U64_MAX % bound)
        block_index = 0
        blocks = 0
        while True:
            x = self._raw(slot, occurrence_index, idx, block_index, bound)
            blocks += 1
            if x < limit:
                break
            block_index += 1
            if blocks > self.MAX_REJECTION_BLOCKS:
                raise RngAuthorityError(
                    "RNG_REPLAY_MISMATCH",
                    {"reason": "rejection did not converge", "bound": bound},
                )
        val = x % bound
        coordinate_hash = h_obj({
            "scope_kind": self.scope_kind, "scope_id": self.scope_id,
            "stream_name": self.stream, "slot": slot,
            "occurrence_index": occurrence_index, "draw_index": idx,
            "uniform_below_n": bound, "block_index": block_index,
        })
        rec = DrawReceipt(
            receipt_id=h_concat("DRAW", self.stream, self.scope_hash, slot, str(idx)),
            stream=self.stream, scope_hash=self.scope_hash, root_seed=self.root_seed,
            slot=slot, occurrence_index=occurrence_index, bound=bound,
            draw_value=val, candidate_set_hash=candidate_set_hash, draw_index=idx,
            sampler=ADP020_SAMPLER, authority=ADP020_AUTHORITY,
            seed_scheme=ADP020_SEED_SCHEME,
            root_seed_provenance=self._classification["root_seed_provenance"],
            scope_kind=self.scope_kind, scope_id=self.scope_id,
            root_seed_sha256=self._root_seed_sha256,
            scope_seed_sha256=self._scope_seed_sha256,
            stream_seed_sha256=self._stream_seed_sha256,
            entropy_block_count=blocks, accepted_raw_u64=x, rejection_limit_u64=limit,
            draw_coordinate_hash=coordinate_hash,
            draw_replay_hash=h_obj({
                "coordinate_hash": coordinate_hash, "accepted_raw_u64": x,
                "mapped": val, "bound": bound,
                "stream_seed_sha256": self._stream_seed_sha256,
            }),
        )
        self.draws.append(rec)
        return rec

    @property
    def draw_count(self) -> int:
        return len(self.draws)

    def lineage_receipt(self) -> Dict[str, Any]:
        """Exact ADP-020 s13.2 first-use-of-stream record (or typed legacy hold)."""
        return {
            "authority": ADP020_AUTHORITY,
            "seed_scheme": ADP020_SEED_SCHEME,
            "sampler": ADP020_SAMPLER if not self._legacy_mode else LEGACY_LAB_SAMPLER_NAME,
            "scope_kind": self.scope_kind,
            "scope_id": self.scope_id,
            "stream_name": self.stream,
            "root_seed_sha256": self._root_seed_sha256,
            "scope_seed_sha256": self._scope_seed_sha256,
            "stream_seed_sha256": self._stream_seed_sha256,
            "adp020_entitlement": self._classification["adp020_entitlement"],
            "hold": self._classification.get("hold"),
        }

    def ledger(self) -> Dict[str, Any]:
        return {
            "stream": self.stream,
            "scope_hash": self.scope_hash,
            "scope_kind": self.scope_kind,
            "root_seed": self.root_seed,
            "root_seed_provenance": self._classification["root_seed_provenance"],
            "root_seed_sha256": self._root_seed_sha256,
            "scope_seed_sha256": self._scope_seed_sha256,
            "stream_seed_sha256": self._stream_seed_sha256,
            "sampler": ADP020_SAMPLER if not self._legacy_mode else LEGACY_LAB_SAMPLER_NAME,
            "adp020_entitlement": self._classification["adp020_entitlement"],
            "hold": self._classification.get("hold"),
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
