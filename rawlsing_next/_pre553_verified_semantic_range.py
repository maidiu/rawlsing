"""S2-A sourcefree I02-derived *semantic range* integrity for the native I03 selector.

This is a bounded query cursor over an EXISTING completely I02-validated C11
release. It is not a saved C11 carrier, external-memory I02 certification,
independent source issuer, or newly accepted science. The witness must be
constructed from the original sealed corpus and its root held independently of
the derived selector index. Never accept a root computed from index postings.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from hashlib import sha256
from heapq import merge
from types import MappingProxyType
from typing import Any

from rawlsing_next.pre553_c11_repository import (
    C11LogicalRelease, _C11_VALIDATION_SEAL,
)
from rawlsing_next.pre553_c11_integrity import RespondentIdentity, QuestionVariableBinding
from rawlsing_next.pre553_empirical_objects import (
    ExactRef, EmpiricalUniverse, RespondentEvent, canonical_json, exact_ref, semantic_hash,
)
from rawlsing_next._pre553_query_common import EmpiricalQueryExecutionError

_SCHEMA = "PYAT_I02_CERTIFIED_SEMANTIC_RANGE_PILOT@1"
_Key = tuple[str, str, str]  # exact respondent-ref key, selector kind, exact target-ref key
_RangeDigest = tuple[int, str]
_EMPTY_DIGEST = sha256(b"").hexdigest()


class SemanticRangeIntegrityError(EmpiricalQueryExecutionError):
    """Refuse a selector whose completeness is not justified by the held witness."""


def _ref(value: Any, name: str) -> ExactRef:
    return exact_ref(value, name)


def _event_sig(event: RespondentEvent) -> list[str]:
    # A structurally plausible event with forged content under a genuine ref
    # cannot be admitted as one of the witnessed occurrences.
    actual = semantic_hash(event.semantic_projection())
    if actual != event.ref.content_hash:
        raise SemanticRangeIntegrityError("event semantic projection does not match its exact ref")
    return [event.ref.key, event.typed_state, actual]


def _digest(events: Sequence[RespondentEvent]) -> _RangeDigest:
    """Constant-extra-memory digest over an *already ordered* occurrence stream.

    Length-prefix each canonical signature to eliminate delimiting ambiguity;
    the I02 seal owns global occurrence uniqueness, and a poisoned duplicate
    changes this held count/hash. No full-range JSON list is ever allocated.
    """
    digest = sha256()
    count = 0
    for event in events:
        material = canonical_json(_event_sig(event)).encode("utf-8")
        digest.update(len(material).to_bytes(8, "big"))
        digest.update(material)
        count += 1
    return count, digest.hexdigest()


def _bindings(
    release: C11LogicalRelease, universe_ref: ExactRef,
) -> tuple[dict[str, tuple[RespondentEvent, ...]], dict[_Key, tuple[RespondentEvent, ...]]]:
    if not isinstance(release, C11LogicalRelease) or release._validation_seal is not _C11_VALIDATION_SEAL:
        raise SemanticRangeIntegrityError("semantic range requires a genuine I02-sealed release")
    universes = [
        obj for obj in release._public_non_events
        if isinstance(obj, EmpiricalUniverse) and obj.ref == universe_ref
    ]
    if len(universes) != 1:
        raise SemanticRangeIntegrityError("the chosen universe is not exactly present in sealed I02")
    respondents: dict[str, list[RespondentEvent]] = {}
    for obj in release.internal_records:
        if (isinstance(obj, RespondentIdentity)
                and _ref(obj.empirical_universe_ref, "respondent.universe") == universe_ref):
            if obj.ref.key in respondents:
                raise SemanticRangeIntegrityError("duplicate respondent ref in sealed release")
            respondents[obj.ref.key] = []
    # I02 validates native question membership and mapping-authority positivity,
    # but these are distinct from native->canonical target equality. Reconstruct
    # the exact admitted question aliases from *sealed QuestionVariableBinding*
    # records, not from the untrusted derived selector or an event's assertion.
    # Multiple genuine instrument-version bindings for the same native ref are
    # allowed; a canonical event alias must match at least one accepted binding.
    admitted_native: dict[str, set[str]] = {}
    for record in release.internal_records:
        if not isinstance(record, QuestionVariableBinding):
            continue
        if _ref(record.empirical_universe_ref, "binding.universe") != universe_ref:
            continue
        native_key = _ref(record.native_question_ref, "binding.native").key
        aliases = admitted_native.setdefault(native_key, set())
        if isinstance(record.canonical_question_ref_or_typed_absence, ExactRef):
            aliases.add(record.canonical_question_ref_or_typed_absence.key)
    postings: dict[_Key, list[RespondentEvent]] = {}
    for event in release.public_objects:
        if not isinstance(event, RespondentEvent):
            continue
        if _ref(event.empirical_universe_ref, "event.universe") != universe_ref:
            continue
        respondent = _ref(event.scoped_respondent_ref, "event.respondent").key
        if respondent not in respondents:
            raise SemanticRangeIntegrityError("event belongs to an absent respondent")
        _event_sig(event)
        native = _ref(event.native_question_ref, "event.native")
        admissible = admitted_native.get(native.key)
        if admissible is None:
            raise SemanticRangeIntegrityError(
                "native event lacks an exact sealed question binding in its universe"
            )
        canonical = None
        if event.canonical_question_ref_if_authorized is not None:
            canonical = _ref(event.canonical_question_ref_if_authorized, "event.canonical")
            if canonical.key not in admissible:
                raise SemanticRangeIntegrityError(
                    "event canonical alias disagrees with sealed QuestionVariableBinding"
                )
            # Multiple different instrument-version grants for the same
            # native question are not evidence of which version produced this
            # event: RespondentEvent carries no question-version discriminator.
            # Do not certify one arbitrary member of a conflicting union.
            if len(admissible) > 1:
                raise SemanticRangeIntegrityError(
                    "ambiguous instrument-version canonical binding for event"
                )
        respondents[respondent].append(event)
        aliases = [("native", native)]
        if canonical is not None:
            aliases.append(("canonical", canonical))
        if event.component_or_subitem_ref is not None:
            aliases.append(("component", _ref(event.component_or_subitem_ref, "event.component")))
        for kind, alias in aliases:
            postings.setdefault((respondent, kind, alias.key), []).append(event)
    ordered = {
        key: tuple(sorted(value, key=lambda obj: obj.ref.key))
        for key, value in respondents.items()
    }
    mapped = {
        key: tuple(sorted(value, key=lambda obj: obj.ref.key))
        for key, value in postings.items()
    }
    return ordered, mapped


def _root_payload(release_ref: ExactRef, source_ref: ExactRef, replay_ref: ExactRef,
                  universe_ref: ExactRef, digests: Mapping[_Key, _RangeDigest]) -> dict[str, Any]:
    return {
        "schema": _SCHEMA,
        "release": release_ref.as_dict(),
        "source": source_ref.as_dict(),
        "replay": replay_ref.as_dict(),
        "universe": universe_ref.as_dict(),
        "complete_selector_multimap": [
            {"key": list(k), "count": digests[k][0], "digest": digests[k][1]}
            for k in sorted(digests)
        ],
    }


@dataclass(frozen=True, slots=True)
class I02SemanticRangeWitness:
    """Complete selector-keyspace root; created from the I02 release, NOT the cache.

    A future durable issuer must pin this root outside the persisted candidate
    and prove its global construction in the I02 proof transaction (S2-B).
    """
    release_ref: ExactRef
    source_ref: ExactRef
    replay_ref: ExactRef
    universe_ref: ExactRef
    range_digests: Mapping[_Key, _RangeDigest]
    root: str

    @classmethod
    def from_validated_release(
        cls, release: C11LogicalRelease, universe_ref: ExactRef,
    ) -> "I02SemanticRangeWitness":
        _, postings = _bindings(release, universe_ref)
        digests = MappingProxyType({key: _digest(events) for key, events in postings.items()})
        root = semantic_hash(_root_payload(
            release.release_ref, release.source_artifact_ref, release.replay_manifest.ref,
            universe_ref, digests,
        ))
        return cls(release.release_ref, release.source_artifact_ref,
                   release.replay_manifest.ref, universe_ref, digests, root)


@dataclass(frozen=True, slots=True)
class CertifiedRespondentEvents(Sequence[RespondentEvent]):
    """Per-respondent native-compatible selector, with bounded occurrence cursor."""
    respondent_key: str
    all_events: tuple[RespondentEvent, ...]
    _postings: Mapping[_Key, tuple[RespondentEvent, ...]]
    _witness: I02SemanticRangeWitness

    def __len__(self) -> int:
        return len(self.all_events)

    def __getitem__(self, i):
        return self.all_events[i]

    def _verified_alias(self, kind: str, target: ExactRef) -> tuple[RespondentEvent, ...]:
        key = (self.respondent_key, kind, target.key)
        rows = self._postings.get(key, ())
        observed = _digest(rows)
        expected = self._witness.range_digests.get(key, (0, _EMPTY_DIGEST))
        if observed != expected:
            raise SemanticRangeIntegrityError(
                "certified semantic range mismatch: missing/extra occurrence or alias"
            )
        return rows

    def select(
        self, target: ExactRef, *, native_only: bool = False,
        include_component: bool = False, states: frozenset[str] | None = None,
    ) -> Iterator[RespondentEvent]:
        # Check WHOLE alias ranges first, before filtering by state. This
        # detects missing nonselected typed states and multiplicity as well.
        parts = [self._verified_alias("native", target)]
        if not native_only:
            parts.append(self._verified_alias("canonical", target))
            if include_component:
                parts.append(self._verified_alias("component", target))
        # Up to three already-sorted alias postings. Merge lazily and suppress
        # the same event under multiple authorized aliases without materializing
        # a full combined range/dedup dictionary.
        previous_key = None
        previous_event = None
        for event in merge(*parts, key=lambda obj: obj.ref.key):
            key = event.ref.key
            if key == previous_key:
                if event != previous_event:
                    raise SemanticRangeIntegrityError("alias points to conflicting event body")
                continue
            previous_key, previous_event = key, event
            if states is None or event.typed_state in states:
                yield event

    def iter_pages(self, *, max_page_events: int = 128) -> Iterator[tuple[RespondentEvent, ...]]:
        """Bound each page; never expose inventory_refs()->tuple of the corpus."""
        if not 1 <= max_page_events <= 256:
            raise ValueError("page size must be 1..256")
        for offset in range(0, len(self.all_events), max_page_events):
            yield self.all_events[offset:offset + max_page_events]


def certified_i03_events(
    release: C11LogicalRelease,
    universe_ref: ExactRef,
    *,
    witness: I02SemanticRangeWitness,
    independently_held_root: str,
    candidate_postings: Mapping[_Key, tuple[RespondentEvent, ...]] | None = None,
) -> Mapping[str, CertifiedRespondentEvents]:
    """Prepare an I03-compatible respondent event mapping for a sourcefree I02 release.

    candidate_postings represents the untrusted secondary index in hostile tests.
    It is deliberately never allowed to supply or overwrite the trusted root.
    The caller must hold the root OUTSIDE that candidate; this function does not
    issue rights, trust a self-hash, commit an index, or update I03 caches.
    """
    if (not isinstance(witness, I02SemanticRangeWitness)
            or witness.root != independently_held_root):
        raise SemanticRangeIntegrityError("no independently held semantic index root")
    if (release.release_ref != witness.release_ref
            or release.source_artifact_ref != witness.source_ref
            or release.replay_manifest.ref != witness.replay_ref
            or universe_ref != witness.universe_ref):
        raise SemanticRangeIntegrityError("wrong release/source/replay/universe for semantic ranges")
    if semantic_hash(_root_payload(
        witness.release_ref, witness.source_ref, witness.replay_ref,
        witness.universe_ref, witness.range_digests,
    )) != witness.root:
        raise SemanticRangeIntegrityError("witness keyspace root invalid")
    respondents, canonical = _bindings(release, universe_ref)
    # This pilot retains a full existing in-memory I02 release as its provenance
    # oracle. Verify the held complete keyspace against that independent source
    # before allowing the derived index to answer EMPTY. This is NOT bounded
    # saved-artifact reopening or the later S2-B global physical proof.
    source_digests = {key: _digest(events) for key, events in canonical.items()}
    if source_digests != dict(witness.range_digests):
        raise SemanticRangeIntegrityError("I02 corpus differs from independently held witness")
    rows = canonical if candidate_postings is None else candidate_postings
    return MappingProxyType({
        respondent: CertifiedRespondentEvents(
            respondent, source_events, rows, witness,
        )
        for respondent, source_events in respondents.items()
    })
