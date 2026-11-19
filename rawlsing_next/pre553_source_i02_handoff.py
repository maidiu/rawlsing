"""Q2 S1-E: bounded source→direct-I02 handoff.

This module composes existing owners only:

* S1-B ``SourceConfig`` / ``GovernedC11Projection`` and physical decoder;
* S1-B source-read admission for an original source, if used;
* the existing S1-C frozen operation/fate census verifier;
* the existing S2-B ``SourcefreeDirectI02Sections`` and
  ``build_sourcefree_direct_i02`` builder.

It does not hand-code question meaning, create a second semantic registry,
mint an issuer/permission, or build a complete C11 candidate/public/internal
object graph.  One bounded physical cell pass generates only RespondentEvent,
EmpiricalCoordinateFact and WeightMeasureFact rows into a private ephemeral
spool; static typed sections come from the existing projection.  The spool is
used to obtain exact declared counts and is deleted after the direct builder
consumes it.

An optional caller-owned ``body_sink`` receives the same one-shot 13-family
objects synchronously while the direct builder consumes them (see
``pre553_source_i02_streams``).  That is the body-preserving producer ABI for a
future source-direct physical consumer; it is not a second source read, a
permanent body store, or a mocked native I03.

The direct builder is the actual first owner.  Its cold ``VerifiedExternalI02``
reader and legacy sealed-body native I03 bridge have their own host/dependency
constraints; this module exposes the certificate roots/path rather than
claiming a cold reader that did not run.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
import json
import os
from pathlib import Path
import sqlite3
import tempfile
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from rawlsing_next._pre553_direct_i02_sourcefree import (
    SourcefreeDirectI02Sections,
    build_sourcefree_direct_i02,
)
from rawlsing_next._pre553_external_i02_certificate import (
    DIRECT_SCHEMA,
    ExternalI02Roots,
)
from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION,
    SourceReleaseManifest,
)
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact,
    ExactRef,
    AuthorityRef,
    RespondentEvent,
    WeightMeasureFact,
    canonical_json,
    canonicalize,
    exact_ref,
)
from rawlsing_next.pre553_operation_fate_census import (
    CensusRefusal,
    FrozenInputCensus,
    verify_frozen_inputs,
)
from rawlsing_next.pre553_source_i02_streams import (
    SourceI02BodySink,
    SourceI02BodyTee,
    SourceI02BodyTransportRefusal,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState, PhysicalSourceIncidence
from rawlsing_next.pre553_physical_cell_journal import (
    PhysicalCellJournal, PhysicalCellJournalReceipt,
)
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.pre553_r157_projection_adapter import (
    IDENTITY_CLASS_ORIGINAL,
    SourceConfig,
    build_governed_c11_projection,
    decode_config_with_source_read_permission,
    row_native_keys_from_transport,
)
from rawlsing_next.pre553_physical_decoder import decode_dta, decode_sav
from rawlsing_next.pre553_source_backed_c11_facade import (
    GovernedC11Projection,
    RESPONSE_OWNER_FAMILY,
    COORDINATE_OWNER_FAMILY,
    WEIGHT_OWNER_FAMILY,
    ResponseValueRule,
    SourceBackedC11FacadeError,
    _cell_key,
    _coordinate,
    _event,
    _weight,
)
from rawlsing_next.universal_grammar.types import (
    GrammarPolicy,
    ScientificFrontier,
    SourceInventory,
)

SOURCE_I02_SCHEMA = "PYAT960_SOURCE_DIRECT_I02_HANDOFF@1.0.0"
SPOOL_FAMILIES = (
    "RespondentEvent",
    "EmpiricalCoordinateFact",
    "WeightMeasureFact",
)
STATIC_FAMILIES = (
    "EmpiricalUniverse",
    "RespondentIdentity",
    "QuestionVariableBinding",
    "RoutingEligibilityFact",
    "AuthoritySnapshot",
    "SourceUniverseRelation",
    "EmpiricalPredicateReplayBinding",
    "ComparatorReplayBinding",
    "DiscoveryBranchReplayBinding",
    "StructuralAdmissionReplayBinding",
)
ALL_FAMILIES = STATIC_FAMILIES + SPOOL_FAMILIES


class SourceI02Refusal(ValueError):
    """A source/census/operation/identity defect refused before or at the builder."""

    def __init__(self, code: str, detail: Any = None):
        super().__init__(code if detail is None else f"{code}: {detail}")
        self.code = code
        self.detail = detail


class SourceI02Hold(SourceI02Refusal):
    """A dependency or host capability is absent; not a green result."""


@dataclass(frozen=True)
class SourceI02Stats:
    source_reads: int
    source_prehash_passes: int
    snapshot_acquisitions: int
    decode_calls: int
    key_witness_passes: int
    cell_passes: int
    full_c11_builds: int
    source_open_model: str
    source_rows: int
    source_columns: int
    event_count: int
    coordinate_count: int
    weight_count: int
    spool_bytes: int
    spool_files: int
    cleanup_complete: bool


@dataclass(frozen=True)
class SourceI02Handoff:
    schema: str
    destination: str
    roots: ExternalI02Roots
    manifest: SourceReleaseManifest
    counts: Mapping[str, int]
    universe_ref: ExactRef
    source_sha256: str
    row_count: int
    census_audit: Mapping[str, Any]
    operation_fates: tuple[Mapping[str, Any], ...]
    stats: SourceI02Stats
    direct_sections_consumed: bool = True
    body_transport: Mapping[str, Any] | None = None
    physical_cell_journal: PhysicalCellJournalReceipt | None = None

    def open_certificate(self):
        """Open the existing cold reader; its host capability may be unavailable."""
        from rawlsing_next._pre553_external_i02_certificate import VerifiedExternalI02
        return VerifiedExternalI02(self.destination, roots=self.roots)


def _pub_from_dict(family: str, payload: Mapping[str, Any]) -> Any:
    from rawlsing_next.pre553_empirical_objects import (
        AuthoritySnapshot, EmpiricalUniverse, RespondentEvent,
        RoutingEligibilityFact, SourceUniverseRelation, WeightMeasureFact,
        EmpiricalCoordinateFact,
    )
    classes = {
        "EmpiricalUniverse": EmpiricalUniverse,
        "RespondentEvent": RespondentEvent,
        "RoutingEligibilityFact": RoutingEligibilityFact,
        "EmpiricalCoordinateFact": EmpiricalCoordinateFact,
        "WeightMeasureFact": WeightMeasureFact,
        "AuthoritySnapshot": AuthoritySnapshot,
        "SourceUniverseRelation": SourceUniverseRelation,
    }
    if family not in classes:
        raise SourceI02Refusal("UNSUPPORTED_SPOOL_FAMILY", family)
    cls = classes[family]
    return cls(
        typed_state=payload["typed_state"],
        authority_snapshot_refs=payload["authority_snapshot_refs"],
        dependency_refs=payload["dependency_refs"],
        producer_replay_locator_or_reference_root=(
            payload["producer_replay_locator_or_reference_root"]
        ),
        object_id=payload["object_id"],
        content_hash=payload["content_hash"],
        **payload["semantic_fields"],
    )


def _spool_section(path: Path, family: str) -> Iterable[Any]:
    def rows() -> Iterable[Any]:
        with path.open("rb") as handle:
            for line in handle:
                if not line.strip():
                    continue
                payload = json.loads(line)
                obj = _pub_from_dict(family, payload)
                if obj.object_id != payload["object_id"] or obj.content_hash != payload["content_hash"]:
                    raise SourceI02Refusal("SPOOL_RECONSTRUCTION_IDENTITY_DRIFT", family)
                yield obj
    return rows()


def _verify_census_before_source(
    *,
    config: SourceConfig,
    projection: GovernedC11Projection,
    census: FrozenInputCensus,
    inventory: SourceInventory,
    policy: GrammarPolicy,
    frontier: ScientificFrontier,
) -> Mapping[str, Any]:
    """Verify the supplied operation/fate inputs before any source byte open."""
    doc = config.document
    expected_sha = doc["binding"]["source_sha256"]
    if inventory.source_sha256 != expected_sha:
        raise SourceI02Refusal(
            "SOURCE_CENSUS_SHA_MISMATCH",
            {"inventory": inventory.source_sha256, "config": expected_sha},
        )
    if inventory.source_id != doc["identity"]["source_id"]:
        raise SourceI02Refusal(
            "SOURCE_CENSUS_ID_MISMATCH",
            {"inventory": inventory.source_id, "config": doc["identity"]["source_id"]},
        )
    slot_names = {entry["name"] for entry in doc["physical_slots"]}
    for occurrence in inventory.occurrences:
        if occurrence.key.item_id not in slot_names:
            raise SourceI02Refusal(
                "SELECTED_OCCURRENCE_NOT_IN_SOURCE",
                {"item": occurrence.key.item_id, "slots": sorted(slot_names)},
            )
    projected_slot_names = (
        {slot.slot.name for slot in projection.response_slots}
        | {slot.slot.name for slot in projection.coordinate_slots}
        | {slot.slot.name for slot in projection.weight_slots}
    )
    for operation in frontier.operations:
        keys = tuple(operation.targets) + tuple(key for key, _ in operation.conditions)
        for key in keys:
            if key.item_id not in slot_names:
                raise SourceI02Refusal(
                    "OPERATION_TARGET_NOT_IN_SOURCE",
                    {"operation_id": getattr(operation, "op_id", None), "item": key.item_id},
                )
            # A held/unknown operation may legitimately target preparation-only
            # source material.  An ELIGIBLE operation may not: the direct body
            # must contain a projected semantic owner for every eligible target.
            if (operation.disposition == "ELIGIBLE"
                    and key.item_id not in projected_slot_names):
                raise SourceI02Refusal(
                    "ELIGIBLE_OPERATION_TARGET_NOT_PROJECTED",
                    {
                        "operation_id": getattr(operation, "op_id", None),
                        "item": key.item_id,
                        "projected_items": sorted(projected_slot_names),
                    },
                )
    # Routing and occurrence dimensions are config/projection preimages, not
    # source-byte facts.  Refuse an ELIGIBLE operation whose semantic preimage
    # is already impossible before opening the source.
    routing_by_question = _routing_states_by_question(config, projection)
    sections_by_name = _sections_by_name(doc)
    for operation in frontier.operations:
        if operation.disposition != "ELIGIBLE":
            continue
        for key in tuple(operation.targets) + tuple(
            key for key, _ in operation.conditions
        ):
            key_sections = sections_by_name.get(key.item_id, ())
            if not key_sections:
                continue
            realized, dimension = _occurrence_dimension_realized(
                key, [section for _family, section in key_sections])
            if not realized:
                raise SourceI02Hold(
                    "OPERATION_OCCURRENCE_DIMENSION_NOT_REALIZED",
                    {
                        "operation_id": operation.op_id,
                        "item_id": key.item_id,
                        "dimension": dimension,
                        "key": key.key,
                    },
                )
            response_owned = any(
                family == "RespondentEvent" for family, _section in key_sections)
            if response_owned:
                for family, section in key_sections:
                    if family != "RespondentEvent":
                        continue
                    states = routing_by_question.get(
                        section["question_id"], Counter())
                    if int(states.get("ELIGIBLE_APPLICABLE", 0)) == 0:
                        raise SourceI02Refusal(
                            "OPERATION_ROUTING_FATE_MISMATCH",
                            {
                                "operation_id": operation.op_id,
                                "item_id": key.item_id,
                                "question_id": section["question_id"],
                                "routing_states": dict(sorted(states.items())),
                            },
                        )
    if frontier.source_identity.get("source_sha256") != expected_sha:
        raise SourceI02Refusal("FRONTIER_SOURCE_SHA_MISMATCH")
    try:
        audit = verify_frozen_inputs(
            census, inventory=inventory, policy=policy, frontier=frontier)
    except CensusRefusal as exc:
        raise SourceI02Refusal(exc.code, exc.detail) from exc
    return audit


def _unresolved_response_state(cell: PhysicalCell) -> str:
    """Preserve source-decoded missingness; unbound observed does not mean answer."""
    if cell.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE:
        return "INVALID_UNRESOLVED"
    if cell.missing_state in {
        PhysicalMissingState.FORMAT_USER_MISSING_VALUE,
        PhysicalMissingState.FORMAT_USER_MISSING_RANGE,
        PhysicalMissingState.FORMAT_EXTENDED_MISSING,
        PhysicalMissingState.SYSTEM_MISSING,
        PhysicalMissingState.SOURCE_CELL_ABSENT_OR_UNREPRESENTED,
    }:
        return "MISSING"
    raise SourceI02Refusal(
        "UNSUPPORTED_PHYSICAL_MISSING_STATE", cell.missing_state.value)


def _occurrence_templates(slot: Any) -> tuple[Any, ...]:
    """Only reuse one unequivocal source-authorized occurrence topology.

    A union of mismatched known response-value occurrences would invent
    multiplicities for an unknown physical value. Reject heterogeneous
    templates instead of silently creating a fabricated repeated answer.
    """
    template = None
    for value in slot.values:
        current = {}
        for occurrence in value.occurrences:
            if (occurrence.key in current
                    and current[occurrence.key] != occurrence):
                raise SourceI02Refusal("AMBIGUOUS_RESPONSE_OCCURRENCE_KEY")
            current[occurrence.key] = occurrence
        if not current:
            raise SourceI02Refusal("UNMAPPED_RESPONSE_HAS_EMPTY_KNOWN_OCCURRENCE")
        if template is None:
            template = current
        elif template != current:
            raise SourceI02Refusal(
                "UNMAPPED_RESPONSE_OCCURRENCE_TOPOLOGY_AMBIGUOUS",
                {"known_template_keys": sorted(template),
                 "conflicting_template_keys": sorted(current)},
            )
    if not template:
        raise SourceI02Refusal("UNBOUND_RESPONSE_SLOT_HAS_NO_OCCURRENCE_TEMPLATE")
    return tuple(template[key] for key in sorted(template))


def _unmapped_event_with_physical_missingness(
    *,
    source_sha256: str,
    row_ordinal: int,
    respondent: Any,
    slot: Any,
    cell: PhysicalCell,
    raw_rule: ResponseValueRule,
    occurrence: Any,
    projection: GovernedC11Projection,
    owner_authority_refs: tuple[AuthorityRef, ...] = (),
) -> RespondentEvent:
    """Retain source missingness without changing any previously mapped event.

    The actual physical typed raw value stays in the established canonical
    raw_response_value witness. The source-declared missing classification and
    declaration are additional *uninterpreted* semantic fields only for
    fallback events. None of these fields supplies a missing source mapping,
    scientific response, routing status, transform, or occurrence authority.
    """
    original = _event(
        source_sha256, row_ordinal, respondent, slot, cell,
        raw_rule, occurrence, projection, owner_authority_refs,
    )
    fields = dict(original.semantic_fields)
    fields["uninterpreted_physical_missing_state"] = cell.missing_state.value
    fields["uninterpreted_source_missing_declaration"] = canonicalize(
        cell.source_missing_declaration
    )
    fields["uninterpreted_physical_cell_key"] = _cell_key(cell)
    return RespondentEvent(
        typed_state=original.typed_state,
        authority_snapshot_refs=original.authority_snapshot_refs,
        dependency_refs=original.dependency_refs,
        producer_replay_locator_or_reference_root=(
            original.producer_replay_locator_or_reference_root
        ),
        **fields,
    )


def _project_spooled_families(
    *,
    config: SourceConfig,
    projection: GovernedC11Projection,
    incidence: PhysicalSourceIncidence,
    spool_paths: Mapping[str, Path],
    batch_size: int,
    row_native_keys: Mapping[int, ExactRef | TypedAbsence] | None = None,
    physical_journal: PhysicalCellJournal | None = None,
) -> tuple[dict[str, int], dict[str, Any]]:
    """Run exactly one bounded physical cell pass into the private spool."""
    rows = {binding.row_ordinal: binding.respondent_ref for binding in projection.row_bindings}
    respondent_by_ref = {item.ref: item for item in projection.respondents}
    response = {slot.slot.key: slot for slot in projection.response_slots}
    coordinate = {slot.slot.key: slot for slot in projection.coordinate_slots}
    weight = {slot.slot.key: slot for slot in projection.weight_slots}
    owner_sets = {slot.slot.key: slot for slot in projection.slot_owner_sets}
    projected = set(response) | set(coordinate) | set(weight)
    seen: dict[tuple[int, str], set[int]] = {key: set() for key in projected}
    handles = {
        family: spool_paths[family].open("wb")
        for family in SPOOL_FAMILIES
    }
    counts = {family: 0 for family in SPOOL_FAMILIES}
    slot_counts: Counter[tuple[str, tuple[int, str]]] = Counter()
    key_slot = config.document["respondents"].get("source_native_key_slot")
    key_cells: list[PhysicalCell] = []
    unresolved_response_cells = 0
    unresolved_response_events = 0

    def write(family: str, obj: Any) -> None:
        handles[family].write(
            canonical_json(obj.as_dict()).encode("utf-8") + b"\n")
        counts[family] += 1

    try:
        for cell in incidence.iter_cells(batch_size):
            if not isinstance(cell, PhysicalCell):
                raise SourceI02Refusal("NON_PHYSICAL_CELL_TRANSPORT")
            # Physical evidence is written BEFORE the semantic projection
            # filters. Fully unprojected variables and unknown mapping slots
            # are preserved in this sourcefree companion without inventing
            # a semantic 14th family, response occurrence or source authority.
            if physical_journal is not None:
                physical_journal.accept(cell)
            key = (cell.variable_ordinal, cell.variable_name)
            if key_slot is not None and key == (key_slot["ordinal"], key_slot["name"]):
                key_cells.append(cell)
            if key not in projected:
                continue
            if cell.row_ordinal not in rows:
                raise SourceI02Refusal("CELL_ROW_OUTSIDE_PROJECTION", cell.row_ordinal)
            if cell.row_ordinal in seen[key]:
                raise SourceI02Refusal(
                    "DUPLICATE_PHYSICAL_ROW_SLOT", (cell.row_ordinal, key))
            seen[key].add(cell.row_ordinal)
            respondent = respondent_by_ref[rows[cell.row_ordinal]]
            physical_key = _cell_key(cell)
            owner_set = owner_sets.get(key)
            if key in response:
                slot = response[key]
                response_auths = (
                    owner_set.authority_refs_for(RESPONSE_OWNER_FAMILY)
                    if owner_set is not None else ()
                )
                rule = {item.physical_key: item for item in slot.values}.get(physical_key)
                if rule is None:
                    # Preserve the exact physical cell in C11's existing
                    # 13-family body, without asserting substantive meaning.
                    # Observed and source-declared missing remain distinct;
                    # every recovered occurrence is from existing topology.
                    state = _unresolved_response_state(cell)
                    occurrences = _occurrence_templates(slot)
                    unresolved_response_cells += 1
                    for occurrence in occurrences:
                        raw_rule = ResponseValueRule(
                            physical_key=physical_key,
                            response_state=state,
                            occurrences=(occurrence,),
                            canonical_value=None,
                            transform_authority_ref=None,
                            extra_authority_refs=(),
                        )
                        write(
                            "RespondentEvent",
                            _unmapped_event_with_physical_missingness(
                                source_sha256=incidence.source_sha256,
                                row_ordinal=cell.row_ordinal,
                                respondent=respondent,
                                slot=slot, cell=cell, raw_rule=raw_rule,
                                occurrence=occurrence, projection=projection,
                                owner_authority_refs=response_auths,
                            ),
                        )
                        slot_counts[("RespondentEvent", key)] += 1
                        unresolved_response_events += 1
                else:
                    # A shared physical slot can have approved coordinate or
                    # weight owners too. Never skip their emission merely
                    # because the response interpretation is unresolved.
                    for occurrence in rule.occurrences:
                        write(
                            "RespondentEvent",
                            _event(
                                incidence.source_sha256, cell.row_ordinal, respondent,
                                slot, cell, rule, occurrence, projection,
                                response_auths,
                            ),
                        )
                        slot_counts[("RespondentEvent", key)] += 1
            if key in coordinate:
                slot = coordinate[key]
                rule = {item.physical_key: item for item in slot.values}.get(
                    physical_key)
                write(
                    "EmpiricalCoordinateFact",
                    _coordinate(
                        incidence.source_sha256, cell.row_ordinal, respondent,
                        slot, cell, rule, projection,
                        owner_set.authority_refs_for(COORDINATE_OWNER_FAMILY)
                        if owner_set is not None else (),
                    ),
                )
                slot_counts[("EmpiricalCoordinateFact", key)] += 1
            if key in weight:
                slot = weight[key]
                rule = {item.physical_key: item for item in slot.values}.get(
                    physical_key)
                write(
                    "WeightMeasureFact",
                    _weight(
                        incidence.source_sha256, cell.row_ordinal, respondent,
                        slot, cell, rule, projection,
                        owner_set.authority_refs_for(WEIGHT_OWNER_FAMILY)
                        if owner_set is not None else (),
                    ),
                )
                slot_counts[("WeightMeasureFact", key)] += 1
    finally:
        for handle in handles.values():
            handle.close()
    expected_rows = set(rows)
    for key, actual in seen.items():
        if actual != expected_rows:
            raise SourceI02Refusal(
                "PROJECTED_SLOT_INCOMPLETE",
                {"slot": key, "missing_rows": sorted(expected_rows - actual)},
            )
    if key_slot is not None:
        key_stream = ExactPhysicalCellStream(
            source_sha256=incidence.source_sha256,
            row_count=incidence.row_count,
            cell_iter_factory=lambda: tuple(key_cells),
        )
        derived = row_native_keys_from_transport(config, stream=key_stream)
        if row_native_keys is None or dict(derived) != dict(row_native_keys):
            raise SourceI02Refusal("ROW_NATIVE_KEY_WITNESS_MISMATCH")
    return (
        counts,
        {
            "rows": len(rows), "projected_slots": len(projected),
            "unresolved_response_cells": unresolved_response_cells,
            "unresolved_response_events": unresolved_response_events,
        },
        dict(slot_counts),
        key_slot is not None,
    )


def _normalised_token(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value).strip().lower()
    if not text:
        return None
    try:
        number = float(text)
    except (TypeError, ValueError):
        return text
    if number.is_integer():
        return str(int(number))
    return format(number, "g")


def _collect_scalar_tokens(value: Any, out: set[str], depth: int = 0) -> None:
    if depth > 8:
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            token = _normalised_token(key)
            if token is not None:
                out.add(token)
            _collect_scalar_tokens(item, out, depth + 1)
        return
    if isinstance(value, (list, tuple, set, frozenset)):
        for item in value:
            _collect_scalar_tokens(item, out, depth + 1)
        return
    if value is None or isinstance(value, TypedAbsence):
        return
    token = _normalised_token(value)
    if token is not None:
        out.add(token)


def _section_tokens(section: Mapping[str, Any]) -> set[str]:
    tokens: set[str] = set()
    _collect_scalar_tokens(section, tokens)
    return tokens


def _occurrence_dimension_realized(
    key: Any,
    sections: Iterable[Mapping[str, Any]],
) -> tuple[bool, str | None]:
    dimensions = (
        ("option_id", getattr(key, "option_id", None)),
        ("form_id", getattr(key, "form_id", None)),
        ("repeat_id", getattr(key, "repeat_id", None)),
    )
    present = [(name, _normalised_token(value))
               for name, value in dimensions
               if _normalised_token(value) is not None]
    if not present:
        return True, None
    tokens: set[str] = set()
    for section in sections:
        tokens.update(_section_tokens(section))
    for name, token in present:
        if token not in tokens:
            return False, name
    return True, None


def _sections_by_slot(
    doc: Mapping[str, Any], family_key: str,
) -> dict[str, tuple[Mapping[str, Any], ...]]:
    result: dict[str, list[Mapping[str, Any]]] = {}
    for section in doc.get(family_key, ()):
        name = section["slot"]["name"]
        result.setdefault(name, []).append(section)
    return {name: tuple(values) for name, values in result.items()}


def _native_question_key(section: Mapping[str, Any]) -> str:
    return exact_ref(section["native_question_ref"], "native_question_ref").key


_UNRESOLVED_ROUTING_STATES = frozenset({"ROUTING_UNKNOWN", "RULE_UNAVAILABLE"})


def _sections_by_name(
    doc: Mapping[str, Any],
) -> dict[str, tuple[tuple[str, Mapping[str, Any]], ...]]:
    result: dict[str, list[tuple[str, Mapping[str, Any]]]] = {}
    for family_key, family in (
        ("response_slots", "RespondentEvent"),
        ("coordinate_slots", "EmpiricalCoordinateFact"),
        ("weight_slots", "WeightMeasureFact"),
    ):
        for section in doc.get(family_key, ()):
            result.setdefault(section["slot"]["name"], []).append(
                (family, section))
    return {name: tuple(values) for name, values in result.items()}


def _routing_states_by_question(
    config: SourceConfig,
    projection: GovernedC11Projection,
) -> dict[str, Counter[str]]:
    doc = config.document
    question_id_by_native = {
        _native_question_key(section): section["question_id"]
        for section in doc.get("questions", ())
    }
    routing_by_question: dict[str, Counter[str]] = {}
    for fact in projection.routing:
        question_key = exact_ref(
            fact.question_or_target_ref, "question_or_target_ref").key
        question_id = question_id_by_native.get(question_key)
        if question_id is None:
            continue
        routing_by_question.setdefault(question_id, Counter())[
            fact.routing_state] += 1
    return routing_by_question


def _operation_source_antijoin(
    *,
    config: SourceConfig,
    projection: GovernedC11Projection,
    frontier: ScientificFrontier,
    census: FrozenInputCensus,
    slot_counts: Mapping[tuple[str, tuple[int, str]], int],
) -> tuple[tuple[Mapping[str, Any], ...], Mapping[str, Any]]:
    """Join every operation target/condition to actual direct-I02 bodies.

    This is deliberately more than an operation-label copy.  An ELIGIBLE
    operation must have a projected semantic owner for every target/condition,
    at least one emitted body, a realized occurrence dimension, and an eligible
    source-routing denominator for every emitted response target.  Held/unknown
    operations may legitimately retain unprojected preparation material, but
    their unrealized state is recorded, never silently converted to a positive.
    """
    doc = config.document
    sections_by_name = _sections_by_name(doc)
    response_by_name = _sections_by_slot(doc, "response_slots")
    coordinate_by_name = _sections_by_slot(doc, "coordinate_slots")
    weight_by_name = _sections_by_slot(doc, "weight_slots")
    routing_by_question = _routing_states_by_question(config, projection)
    source_by_id = {row.operation_id: row for row in census.source_candidates}
    fate_by_id = {row.operation_id: row for row in census.scientific_fates}

    def realizations_for(key: Any) -> tuple[Mapping[str, Any], ...]:
        item = key.item_id
        result: list[Mapping[str, Any]] = []
        response_sections = response_by_name.get(item, ())
        if response_sections:
            realized, dimension = _occurrence_dimension_realized(
                key, response_sections)
            for section in response_sections:
                slot = (section["slot"]["ordinal"], section["slot"]["name"])
                states = routing_by_question.get(section["question_id"], Counter())
                result.append({
                    "key": key.key,
                    "item_id": item,
                    "family": "RespondentEvent",
                    "slot": slot,
                    "question_id": section["question_id"],
                    "emitted": int(slot_counts.get(
                        ("RespondentEvent", slot), 0)),
                    "routing_states": dict(sorted(states.items())),
                    "routable_rows": int(states.get("ELIGIBLE_APPLICABLE", 0)),
                    "routing_unresolved": any(
                        name in _UNRESOLVED_ROUTING_STATES
                        for name in states),
                    "occurrence_realized": realized,
                    "occurrence_dimension": dimension,
                })
        coordinate_sections = coordinate_by_name.get(item, ())
        if coordinate_sections:
            realized, dimension = _occurrence_dimension_realized(
                key, coordinate_sections)
            for section in coordinate_sections:
                slot = (section["slot"]["ordinal"], section["slot"]["name"])
                result.append({
                    "key": key.key,
                    "item_id": item,
                    "family": "EmpiricalCoordinateFact",
                    "slot": slot,
                    "question_id": None,
                    "emitted": int(slot_counts.get(
                        ("EmpiricalCoordinateFact", slot), 0)),
                    "routing_states": {},
                    "routable_rows": None,
                    "occurrence_realized": realized,
                    "occurrence_dimension": dimension,
                })
        weight_sections = weight_by_name.get(item, ())
        if weight_sections:
            realized, dimension = _occurrence_dimension_realized(
                key, weight_sections)
            for section in weight_sections:
                slot = (section["slot"]["ordinal"], section["slot"]["name"])
                result.append({
                    "key": key.key,
                    "item_id": item,
                    "family": "WeightMeasureFact",
                    "slot": slot,
                    "question_id": None,
                    "emitted": int(slot_counts.get(
                        ("WeightMeasureFact", slot), 0)),
                    "routing_states": {},
                    "routable_rows": None,
                    "occurrence_realized": realized,
                    "occurrence_dimension": dimension,
                })
        return tuple(result)

    rows: list[Mapping[str, Any]] = []
    eligible_count = 0
    eligible_realized_count = 0
    held_unrealized_count = 0
    for operation in frontier.operations:
        source_row = source_by_id.get(operation.op_id)
        fate_row = fate_by_id.get(operation.op_id)
        if source_row is None or fate_row is None:
            raise SourceI02Refusal(
                "OPERATION_PREIMAGE_MISSING", operation.op_id)
        keys = tuple(operation.targets) + tuple(
            key for key, _ in operation.conditions)
        key_records = tuple(
            (key, realizations_for(key),
             any(family == "RespondentEvent"
                 for family, _section in sections_by_name.get(key.item_id, ())))
            for key in keys
        )
        realizations = tuple(
            realization
            for _, key_realizations, _response_only in key_records
            for realization in key_realizations
        )
        eligible = operation.disposition == "ELIGIBLE"
        realized_all = bool(key_records)
        routing_unresolved_keys: list[str] = []
        for key, key_realizations, response_owned in key_records:
            if not key_realizations:
                realized_all = False
                continue
            if not any(
                row["emitted"] > 0 and row["occurrence_realized"]
                for row in key_realizations
            ):
                realized_all = False
            if not eligible:
                continue
            if not any(row["occurrence_realized"] for row in key_realizations):
                dimension = next(
                    (row["occurrence_dimension"] for row in key_realizations
                     if row["occurrence_dimension"] is not None),
                    None,
                )
                raise SourceI02Hold(
                    "OPERATION_OCCURRENCE_DIMENSION_NOT_REALIZED",
                    {
                        "operation_id": operation.op_id,
                        "item_id": key.item_id,
                        "dimension": dimension,
                        "key": key.key,
                    },
                )
            response_rows = [
                row for row in key_realizations
                if row["family"] == "RespondentEvent" and row["emitted"] > 0
            ]
            if response_owned and response_rows and all(
                row["routable_rows"] == 0 for row in response_rows
            ):
                raise SourceI02Refusal(
                    "OPERATION_ROUTING_FATE_MISMATCH",
                    {
                        "operation_id": operation.op_id,
                        "item_id": key.item_id,
                        "question_id": response_rows[0]["question_id"],
                        "routing_states": response_rows[0]["routing_states"],
                    },
                )
            if any(row.get("routing_unresolved") for row in response_rows):
                routing_unresolved_keys.append(key.key)
        source_realized = realized_all and not routing_unresolved_keys
        if eligible:
            eligible_count += 1
            if not realized_all:
                raise SourceI02Refusal(
                    "ELIGIBLE_OPERATION_SOURCE_NOT_REALIZED",
                    {
                        "operation_id": operation.op_id,
                        "keys": [key.key for key, _, _ in key_records],
                        "realizations": realizations,
                    },
                )
            if source_realized:
                eligible_realized_count += 1
        elif not realized_all:
            held_unrealized_count += 1
        rows.append({
            "operation_id": operation.op_id,
            "operation_hash": operation.canonical_hash,
            "disposition": operation.disposition,
            "claim_class": operation.claim_class,
            "execution_state": operation.execution_state,
            "result_state": operation.result_state,
            "measure_kind": operation.measure_kind,
            "measure_id": operation.measure_id,
            "weight_ref": operation.weight_ref,
            "estimand": operation.estimand,
            "design_ref": operation.design_ref,
            "variance_policy": operation.variance_policy,
            "source_preimage": {
                "source_id": source_row.source_id,
                "source_sha256": source_row.source_sha256,
                "wave": source_row.wave,
                "edition": source_row.edition,
                "instrument_ref": source_row.instrument_ref,
                "universe_scope": source_row.universe_scope,
                "source_authority_ref": source_row.source_authority_ref,
                "source_decision_ref": source_row.source_decision_ref,
                "meaning_ref": source_row.meaning_ref,
                "source_grade": source_row.source_grade,
                "operation_hash": source_row.operation_hash,
                "occurrence_ids": source_row.occurrence_ids,
                "science_eligibility_decision_ref": (
                    fate_row.eligibility_decision_ref),
                "u_item_ref": fate_row.u_item_ref,
                "u_unit_ref": fate_row.u_unit_ref,
                "u_app_ref": fate_row.u_app_ref,
                "e_pre_ref_or_absence": fate_row.e_pre_ref_or_absence,
                "science_grade": fate_row.science_grade,
                "operation_hash_matches": (
                    source_row.operation_hash
                    == operation.canonical_hash
                    == fate_row.operation_hash
                ),
                "measure": {
                    "measure_kind": operation.measure_kind,
                    "measure_id": operation.measure_id,
                    "weight_ref": operation.weight_ref,
                    "estimand": operation.estimand,
                    "design_ref": operation.design_ref,
                    "variance_policy": operation.variance_policy,
                },
            },
            "source_realization": realizations,
            "source_realized": source_realized,
            "routing_unresolved_keys": tuple(routing_unresolved_keys),
            "unrealized_keys": tuple(
                key.key for key, key_realizations, _response_owned in key_records
                if not any(
                    row["emitted"] > 0 and row["occurrence_realized"]
                    and not row.get("routing_unresolved")
                    for row in key_realizations
                )
            ),
            "operation_source_state": (
                "ELIGIBLE_REALIZED" if eligible and source_realized
                else "ELIGIBLE_TYPED_HOLD" if eligible
                else "HELD_OR_UNKNOWN_SOURCE_STATE"
            ),
            "native_first_reader_state": (
                "HOLD_ROUTING_OR_BODY_UNRESOLVED"
                if eligible and not source_realized
                else "HOLD_DEPENDENCY_LINUX_PROC_SELF_FD_AND_SEALED_BODY_RELEASE"
            ),
            "issued_receipt_refs": (),
        })
    audit = {
        "operation_count": len(rows),
        "eligible_operation_count": eligible_count,
        "eligible_realized_count": eligible_realized_count,
        "held_operation_count": len(rows) - eligible_count,
        "held_unrealized_count": held_unrealized_count,
        "source_realized_operation_count": sum(
            1 for row in rows if row["source_realized"]),
        "unrealized_eligible_count": sum(
            1 for row in rows
            if row["disposition"] == "ELIGIBLE" and not row["source_realized"]),
        "unrealized_eligible_policy": "TYPED_HOLD_NOT_REFUSED",
        "native_first_reader_state": (
            "HOLD_DEPENDENCY_LINUX_PROC_SELF_FD_AND_SEALED_BODY_RELEASE"),
    }
    return tuple(rows), audit


def _manifest_and_sections(
    *,
    projection: GovernedC11Projection,
    incidence: PhysicalSourceIncidence,
    spool_paths: Mapping[str, Path],
    counts: Mapping[str, int],
    universe_ref: ExactRef,
) -> tuple[SourceReleaseManifest, SourcefreeDirectI02Sections,
           Mapping[str, int], Mapping[str, Any]]:
    sections: dict[str, Iterable[Any]] = {}
    absences: dict[str, TypedAbsence] = {}
    declared_counts = {
        "EmpiricalUniverse": len(projection.universes),
        "RespondentIdentity": len(projection.respondents),
        "QuestionVariableBinding": len(projection.questions),
        "RespondentEvent": counts["RespondentEvent"],
        "RoutingEligibilityFact": len(projection.routing),
        "EmpiricalCoordinateFact": counts["EmpiricalCoordinateFact"],
        "WeightMeasureFact": counts["WeightMeasureFact"],
        "AuthoritySnapshot": len(projection.authority_snapshots),
        "ReplayManifest": 1,
    }
    sections["EmpiricalUniverse"] = tuple(projection.universes)
    sections["RespondentIdentity"] = tuple(projection.respondents)
    sections["QuestionVariableBinding"] = tuple(projection.questions)
    sections["RoutingEligibilityFact"] = tuple(projection.routing)
    sections["AuthoritySnapshot"] = tuple(projection.authority_snapshots)
    if isinstance(projection.source_relations, TypedAbsence):
        absences["SourceUniverseRelation"] = projection.source_relations
        sections["SourceUniverseRelation"] = iter(())
        declared_counts["SourceUniverseRelation"] = 0
    else:
        sections["SourceUniverseRelation"] = tuple(projection.source_relations)
        declared_counts["SourceUniverseRelation"] = len(projection.source_relations)
    replay_map = (
        ("EmpiricalPredicateReplayBinding", projection.predicate_replay),
        ("ComparatorReplayBinding", projection.comparator_replay),
        ("DiscoveryBranchReplayBinding", projection.discovery_replay),
        ("StructuralAdmissionReplayBinding", projection.structural_replay),
    )
    for family, value in replay_map:
        if isinstance(value, TypedAbsence):
            absences[family] = value
            sections[family] = iter(())
            declared_counts[family] = 0
        else:
            sections[family] = tuple(value)
            declared_counts[family] = len(value)
    if projection.weight_slots:
        sections["WeightMeasureFact"] = _spool_section(
            spool_paths["WeightMeasureFact"], "WeightMeasureFact")
    else:
        absences["WeightMeasureFact"] = TypedAbsence("NOT_APPLICABLE")
        sections["WeightMeasureFact"] = iter(())
        declared_counts["WeightMeasureFact"] = 0
    sections["RespondentEvent"] = _spool_section(
        spool_paths["RespondentEvent"], "RespondentEvent")
    sections["EmpiricalCoordinateFact"] = _spool_section(
        spool_paths["EmpiricalCoordinateFact"], "EmpiricalCoordinateFact")

    if universe_ref.key not in {item.ref.key for item in projection.universes}:
        raise SourceI02Refusal("SELECTED_UNIVERSE_NOT_IN_PROJECTION")
    manifest = SourceReleaseManifest(
        source_artifact_id=projection.source_artifact_id,
        source_artifact_content_hash=incidence.source_sha256,
        source_family_id=projection.source_family_id,
        study_product_id=projection.study_product_id,
        release_id=projection.release_id,
        instrument_release_id=projection.instrument_release_id,
        ingest_contract_version=INGEST_CONTRACT_VERSION,
        declared_universe_refs=tuple(
            sorted((item.ref for item in projection.universes), key=lambda ref: ref.key)),
        declared_authority_snapshot_refs=tuple(
            sorted((item.authority_ref for item in projection.authority_snapshots),
                   key=lambda ref: ref.key)),
        declared_record_counts_by_logical_family=declared_counts,
        source_snapshot_retention_ref=projection.source_snapshot_retention_ref,
    )
    source = SourcefreeDirectI02Sections(
        manifest=manifest,
        sections=MappingProxyType(sections),
        typed_absences=MappingProxyType(absences),
        replay_protocol_authority_ref=projection.replay_authority_ref,
        replay_protocol_version=projection.replay_protocol_version,
        deterministic_tie_order_rules_ref=projection.tie_order_ref,
    )
    return manifest, source, MappingProxyType(declared_counts), MappingProxyType(absences)


def _cleanup_spool(
    spool_paths: Mapping[str, Path],
    spool_dir: Path | None,
) -> tuple[bool, list[str]]:
    leftovers: list[str] = []
    for path in spool_paths.values():
        try:
            path.unlink()
        except FileNotFoundError:
            continue
        except OSError:
            leftovers.append(str(path))
    if spool_dir is not None:
        try:
            spool_dir.rmdir()
        except FileNotFoundError:
            pass
        except OSError:
            leftovers.append(str(spool_dir))
    return not leftovers, leftovers


def _target_matches_manifest(
    target: Path,
    manifest: SourceReleaseManifest,
) -> bool:
    """Return true only for a complete certificate published from this input."""
    try:
        if not target.is_file() or target.is_symlink():
            return False
        connection = sqlite3.connect(f"file:{target}?mode=ro", uri=True)
        try:
            rows = connection.execute(
                "SELECT name,value FROM main.header "
                "WHERE name IN ('schema','source_manifest_hash','source')"
            ).fetchall()
        finally:
            connection.close()
    except Exception:
        return False
    header = dict(rows)
    return (
        header.get("schema") == DIRECT_SCHEMA
        and header.get("source_manifest_hash") == manifest.content_hash
        and header.get("source") == manifest.source_artifact_ref.key
    )


def _invalidate_target(target: Path, primary: BaseException) -> None:
    """Best-effort fail-closed removal of our own published certificate."""
    try:
        target.unlink()
    except FileNotFoundError:
        return
    except OSError as exc:
        if hasattr(primary, "add_note"):
            primary.add_note(
                f"Q2 certificate invalidation failed for {target}: {exc}")
        return
    try:
        dirfd = os.open(target.parent, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(dirfd)
    finally:
        os.close(dirfd)


def build_source_i02_handoff(
    *,
    config: SourceConfig | Mapping[str, Any],
    source_path: str | Path,
    destination: str | Path,
    census: FrozenInputCensus,
    inventory: SourceInventory,
    policy: GrammarPolicy,
    frontier: ScientificFrontier,
    row_native_keys: Mapping[int, ExactRef | TypedAbsence] | None = None,
    universe_ref: ExactRef | None = None,
    batch_size: int = 512,
    chunk_size: int = 512,
    resolver: Any = None,
    host: str | None = None,
    purpose: str | None = None,
    consumer_use: str | None = None,
    semantic_use_scope: tuple[str, ...] | None = None,
    body_sink: SourceI02BodySink | None = None,
    physical_journal: PhysicalCellJournal | None = None,
) -> SourceI02Handoff:
    """Build one bounded source→direct-I02 handoff.

    The S1-C census is verified before any source read.  A configured
    source-native key slot must have explicit independently derived
    ``row_native_keys``; this adapter does not perform a second key pass.

    If ``body_sink`` is supplied, the same one-shot 13-family objects consumed
    by the existing direct builder are synchronously transported to the sink.
    The sink stages only; ``finish`` commits it against the published exact
    certificate roots.  On any failure the adapter aborts the sink and removes
    its own published certificate.  The sink never causes a source reread.
    """
    if not isinstance(config, SourceConfig):
        config = SourceConfig(config)
    if (physical_journal is not None
            and type(physical_journal) is not PhysicalCellJournal):
        raise SourceI02Refusal("EXACT_PHYSICAL_JOURNAL_SINK_REQUIRED")
    doc = config.document
    target = Path(destination).absolute()
    if (target.suffix != ".sqlite" or target.exists() or target.is_symlink()
            or not target.parent.is_dir() or target.parent.is_symlink()):
        raise SourceI02Refusal(
            "OUTPUT_DESTINATION_INVALID",
            "new non-symlink .sqlite destination in an existing private directory required",
        )
    slot = doc["respondents"].get("source_native_key_slot")
    if slot is not None and row_native_keys is None:
        raise SourceI02Hold(
            "KEY_WITNESS_REQUIRED",
            "configured source_native_key_slot requires independently derived row_native_keys",
        )
    projection = build_governed_c11_projection(
        config,
        source_sha256=doc["binding"]["source_sha256"],
        row_count=doc["binding"]["row_count"],
        row_native_keys=row_native_keys,
    )
    if universe_ref is None:
        universe_ref = projection.universes[0].ref
    audit = _verify_census_before_source(
        config=config, projection=projection, census=census,
        inventory=inventory, policy=policy, frontier=frontier,
    )
    original_source = (
        doc["binding"]["identity_class"] == IDENTITY_CLASS_ORIGINAL)
    # Raw physical retention is separately permissioned. Existing original
    # construction/read grants do NOT imply export/retention of all cells.
    # Sourcefree C0 permits explicit private journals for engineering only.
    if original_source and physical_journal is not None:
        raise SourceI02Hold("ORIGINAL_PHYSICAL_JOURNAL_RETENTION_RIGHTS_UNISSUED")
    source_prehash_passes = 1 if original_source else 0
    source_reads = 1 + source_prehash_passes
    source_open_model = (
        "ORIGINAL_PREHASH_PLUS_SNAPSHOT"
        if original_source else
        "FIXTURE_SNAPSHOT_ONLY"
    )
    sink: SourceI02BodyTee | None = None
    incidence: PhysicalSourceIncidence | None = None
    spool_dir: Path | None = None
    spool_paths: Mapping[str, Path] | None = None
    manifest: SourceReleaseManifest | None = None
    published = False
    try:
        if body_sink is not None:
            sink = SourceI02BodyTee(
                body_sink,
                source_sha256=doc["binding"]["source_sha256"],
                source_id=doc["identity"]["source_id"],
                universe_ref=universe_ref,
                projection_identity_ref=projection.projection_identity_ref,
            )
            sink.begin()
        if original_source:
            if resolver is None:
                raise SourceI02Hold(
                    "SOURCE_READ_RESOLVER_REQUIRED",
                    "original source requires an independently supplied resolver",
                )
            if not all((host, purpose, consumer_use, semantic_use_scope)):
                raise SourceI02Refusal("SOURCE_READ_REQUEST_FIELDS_REQUIRED")
            incidence = decode_config_with_source_read_permission(
                config,
                source_path=source_path,
                resolver=resolver,
                host=host,
                purpose=purpose,
                consumer_use=consumer_use,
                semantic_use_scope=semantic_use_scope,
            )
        else:
            source_format = doc["identity"]["source_format"]
            decoder = decode_sav if source_format == "SAV" else decode_dta
            # The fixture path performs the same content-bound snapshot hash in
            # the decoder; avoiding the pre-hash keeps the source path to one
            # governed open while the exact binding is checked below.
            incidence = decoder(source_path, encoding=None)
        if incidence.source_sha256 != doc["binding"]["source_sha256"]:
            raise SourceI02Refusal("DECODED_SOURCE_SHA_MISMATCH")
        if incidence.row_count != doc["binding"]["row_count"]:
            raise SourceI02Refusal("DECODED_SOURCE_ROWS_MISMATCH")
        if physical_journal is not None:
            physical_journal.begin(incidence)
        spool_dir = Path(tempfile.mkdtemp(
            prefix=".s1e-i02-spool-", dir=target.parent))
        spool_paths = {
            family: spool_dir / f"{family}.jsonl" for family in SPOOL_FAMILIES
        }
        counts, _metrics, slot_counts, key_witness_pass = (
            _project_spooled_families(
                config=config,
                projection=projection,
                incidence=incidence,
                spool_paths=spool_paths,
                batch_size=batch_size,
                row_native_keys=row_native_keys,
                physical_journal=physical_journal,
            )
        )
        operation_fates, operation_audit = _operation_source_antijoin(
            config=config,
            projection=projection,
            frontier=frontier,
            census=census,
            slot_counts=slot_counts,
        )
        audit = dict(audit)
        audit["operation_source_antijoin"] = operation_audit
        manifest, source, declared_counts, _absences = _manifest_and_sections(
            projection=projection,
            incidence=incidence,
            spool_paths=spool_paths,
            counts=counts,
            universe_ref=universe_ref,
        )
        teed_source = sink.attach(source) if sink is not None else source
        roots = build_sourcefree_direct_i02(
            teed_source,
            universe_ref,
            target,
            chunk_size=chunk_size,
        )
        published = True
        spool_bytes = sum(path.stat().st_size for path in spool_paths.values())
        cleanup_ok, leftovers = _cleanup_spool(spool_paths, spool_dir)
        if not cleanup_ok:
            raise SourceI02Refusal("SPOOL_CLEANUP_INCOMPLETE", leftovers)
        stats = SourceI02Stats(
            source_reads=source_reads,
            source_prehash_passes=source_prehash_passes,
            snapshot_acquisitions=1,
            decode_calls=1,
            key_witness_passes=1 if key_witness_pass else 0,
            cell_passes=1,
            full_c11_builds=0,
            source_open_model=source_open_model,
            source_rows=incidence.row_count,
            source_columns=len(incidence.variables),
            event_count=counts["RespondentEvent"],
            coordinate_count=counts["EmpiricalCoordinateFact"],
            weight_count=counts["WeightMeasureFact"],
            spool_bytes=spool_bytes,
            spool_files=len(spool_paths),
            cleanup_complete=True,
        )
        handoff = SourceI02Handoff(
            schema=SOURCE_I02_SCHEMA,
            destination=str(target),
            roots=roots,
            manifest=manifest,
            counts=declared_counts,
            universe_ref=universe_ref,
            source_sha256=incidence.source_sha256,
            row_count=incidence.row_count,
            census_audit=audit,
            operation_fates=operation_fates,
            stats=stats,
        )
        if physical_journal is not None:
            raw_receipt = physical_journal.finish()
            handoff = replace(handoff, physical_cell_journal=raw_receipt)
        if sink is not None:
            body_transport = sink.finish(
                roots=roots,
                manifest=manifest,
                counts=declared_counts,
            )
            handoff = replace(handoff, body_transport=body_transport)
        return handoff
    except BaseException as exc:
        # The body sink, physical journal, and direct-I02 publisher are
        # separately owned resources in one failed source transaction.
        # An exception in one abort MUST NOT strand the other resource.
        # Preserve the original first fault, appending cleanup failures as
        # diagnostics rather than converting a rollback defect into success.
        cleanup_errors: list[str] = []
        if sink is not None:
            try:
                sink.abort(exc)
            except BaseException as cleanup_exc:
                cleanup_errors.append(
                    f"body sink abort failed: {type(cleanup_exc).__name__}: {cleanup_exc}"
                )
        if physical_journal is not None:
            try:
                physical_journal.abort()
            except BaseException as cleanup_exc:
                cleanup_errors.append(
                    f"physical journal abort failed: {type(cleanup_exc).__name__}: {cleanup_exc}"
                )
        try:
            if published or (
                manifest is not None
                and _target_matches_manifest(target, manifest)
            ):
                _invalidate_target(target, exc)
        except BaseException as cleanup_exc:
            cleanup_errors.append(
                f"direct-I02 invalidation failed: {type(cleanup_exc).__name__}: {cleanup_exc}"
            )
        if cleanup_errors and hasattr(exc, "add_note"):
            exc.add_note("source-I02 rollback incomplete: " + "; ".join(cleanup_errors))
        raise
    finally:
        if spool_paths is not None:
            _cleanup_spool(spool_paths, spool_dir)
        if incidence is not None:
            incidence.close()


def open_direct_native_i03(
    handoff: SourceI02Handoff,
    repository: Any,
    release_ref: ExactRef,
):
    """Open the existing direct-I02 → native-I03 selector bridge.

    The caller must supply the already-sealed body repository/release; this
    function never builds a legacy candidate.  The returned verified reader
    must remain open for the native selector lifetime.  On hosts without the
    cold certificate /proc/self/fd capability the underlying owner raises its
    explicit dependency error; this module does not fake that capability.
    """
    from rawlsing_next._pre553_external_i02_certificate import (
        install_direct_sourcefree_i02_i03,
    )
    reader = handoff.open_certificate()
    try:
        install_direct_sourcefree_i02_i03(
            repository, release_ref, handoff.universe_ref, reader)
    except Exception:
        reader.close()
        raise
    return reader



__all__ = [
    "SOURCE_I02_SCHEMA",
    "SourceI02Refusal",
    "SourceI02Hold",
    "SourceI02Stats",
    "SourceI02Handoff",
    "SourceI02BodySink",
    "SourceI02BodyTransportRefusal",
    "build_source_i02_handoff",
    "open_direct_native_i03",
]
