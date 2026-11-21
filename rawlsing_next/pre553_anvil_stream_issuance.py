"""Narrow saved-stream typed issuance seam for existing native I03.

This is a candidate on an isolated branch, not an issuer.  The caller must
supply one held, source-specific issuance decision containing exact stream
roots, question, authorized operation, external typed authorities, query and
predicate preimages, and approved raw/nonanswer outcome domains.  The seam only
validates that decision, constructs the existing ``RuntimeObjectCatalog`` and
reuses ``execute_anvil_stream_i03``; it does not infer source semantics, issue
new authority, or create permanent refs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from rawlsing_next.pre553_anvil_stream_native_i03 import (
    VerifiedAnvilStreamEstate,
    _stream_exact_universe,
    execute_anvil_stream_i03,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    authority_ref,
    exact_ref,
)
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError


class StreamIssuanceError(DirectEstateError):
    """The held source/stream issuance decision is absent, conflicting or stale."""


@dataclass(frozen=True)
class HeldStreamIssuanceDecision:
    """Externally held source decision; no field is inferred from saved metadata.

    ``approved_raw_domain`` and ``approved_nonanswer_states`` are supplied by
    the competent source owner.  An empty nonanswer tuple means only ordinary
    substantive/empty outcomes are allowed.  No q103 mapping or risk policy is
    encoded here.
    """

    source_id: str
    source_root: str
    release_root: str
    universe_root: str
    replay_root: str
    question_ref: ExactRef
    authorized_operation: str
    authorities: tuple[AuthoritySnapshot, ...]
    predicate: EmpiricalPredicate
    query: EmpiricalQuerySpec
    approved_raw_domain: tuple[str, ...]
    approved_nonanswer_states: tuple[str, ...] = ()


def _same_exact_string(value: str, expected: str, label: str) -> None:
    if type(value) is not str or value != expected:
        raise StreamIssuanceError(f"stream {label} differs from held issuance decision")


def _question_present(estate: VerifiedAnvilStreamEstate, question_ref: ExactRef) -> None:
    matches = 0
    for binding in estate.iter_family("QuestionVariableBinding"):
        native = exact_ref(
            getattr(binding, "native_question_ref", None), "question binding ref"
        )
        if native == question_ref:
            matches += 1
    if matches != 1:
        raise StreamIssuanceError(
            "question ref is not exactly one verified saved-stream binding"
        )


def _raw_domain(fact) -> tuple[str, ...]:
    cells = fact.target_topology.get("complete_cell_semantic_projection") or ()
    result = []
    for row in cells:
        cell = row.get("cell")
        if not isinstance(cell, str):
            raise StreamIssuanceError("raw outcome cell is not a scalar source label")
        result.append(cell)
    return tuple(sorted(result))


def issue_and_execute_stream_i03(
    *,
    estate: VerifiedAnvilStreamEstate,
    decision: HeldStreamIssuanceDecision,
    effective_current: Callable[[], bool] | None = None,
):
    """Validate a held decision, build the existing catalog, and execute I03.

    ``effective_current`` must be the current external authority check for the
    held decision.  When absent, the verified estate's own current check still
    applies, but no source-specific authority freshness is asserted.
    """
    if type(estate) is not VerifiedAnvilStreamEstate:
        raise StreamIssuanceError("exact verified ANVIL stream estate required")
    if type(decision) is not HeldStreamIssuanceDecision:
        raise StreamIssuanceError("exact held stream issuance decision required")
    if effective_current is not None and effective_current() is not True:
        raise StreamIssuanceError("effective source/operation authority refused")

    estate._live()
    if type(decision.source_id) is not str or decision.source_id != estate._held.source_id:
        raise StreamIssuanceError("stream source identity differs from held issuance decision")
    _same_exact_string(decision.source_root, estate.i02.source, "source root")
    _same_exact_string(decision.release_root, estate.i02.release, "release root")
    _same_exact_string(decision.universe_root, estate.i02.universe, "universe root")
    _same_exact_string(decision.replay_root, estate.i02.replay, "replay root")
    if estate.native_release_ref.key != decision.release_root:
        raise StreamIssuanceError("stream native release differs from held release")

    question_ref = exact_ref(decision.question_ref, "held question_ref")
    _question_present(estate, question_ref)

    query = decision.query
    predicate = decision.predicate
    if type(query) is not EmpiricalQuerySpec or type(predicate) is not EmpiricalPredicate:
        raise StreamIssuanceError("exact typed query and predicate required")
    if exact_ref(query.condition_predicate_ref, "query condition") != predicate.ref:
        raise StreamIssuanceError("query condition is not the held predicate")
    targets = tuple(exact_ref(ref, "query target") for ref in query.target_refs)
    if targets != (question_ref,):
        raise StreamIssuanceError("query does not target exactly the held question")
    universes = tuple(
        exact_ref(ref, "query universe") for ref in query.empirical_universe_refs
    )
    held_universe = _stream_exact_universe(decision.universe_root)
    if universes != (held_universe,):
        raise StreamIssuanceError("query universe is not the held stream universe")

    authorities = tuple(decision.authorities)
    if not authorities or any(type(x) is not AuthoritySnapshot for x in authorities):
        raise StreamIssuanceError("exact held authority snapshots required")
    if type(decision.authorized_operation) is not str or not decision.authorized_operation:
        raise StreamIssuanceError("exact authorized operation required")
    authority_registry = AuthorityRegistry(authorities)
    query_authority_refs = tuple(
        authority_ref(ref, "query authority") for ref in query.query_authority_refs
    )
    if not query_authority_refs:
        raise StreamIssuanceError("query carries no exact authority ref")
    for query_authority in query_authority_refs:
        authority_registry.require(
            query_authority,
            operation=decision.authorized_operation,
            object_family="EmpiricalQuerySpec@1.0.0",
        )

    catalog = RuntimeObjectCatalog(
        authorities=authorities,
        predicates=(predicate,),
        queries=(query,),
        discovery_authorities=(),
    )
    # Existing native I03; no alternate evaluator or catalog path.
    result = execute_anvil_stream_i03(
        estate=estate,
        runtime_catalog=catalog,
        query_ref=query.ref,
        predicate_ref=predicate.ref,
    )
    if effective_current is not None and effective_current() is not True:
        raise StreamIssuanceError("effective source/operation authority revoked during execution")

    approved_raw = tuple(decision.approved_raw_domain)
    if not approved_raw or any(type(x) is not str for x in approved_raw):
        raise StreamIssuanceError("approved raw outcome domain must be non-empty text")
    for fact in result.facts:
        if fact.typed_state in decision.approved_nonanswer_states:
            continue
        cells = _raw_domain(fact)
        if not set(cells).issubset(set(approved_raw)):
            raise StreamIssuanceError("native raw outcome is outside the approved domain")
    estate._recheck_unchanged_members()
    return result


__all__ = [
    "HeldStreamIssuanceDecision",
    "StreamIssuanceError",
    "issue_and_execute_stream_i03",
]
