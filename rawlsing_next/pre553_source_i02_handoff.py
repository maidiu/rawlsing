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

The direct builder is the actual first owner.  Its cold ``VerifiedExternalI02``
reader and legacy sealed-body native I03 bridge have their own host/dependency
constraints; this module exposes the certificate roots/path rather than
claiming a cold reader that did not run.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import tempfile
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from rawlsing_next._pre553_direct_i02_sourcefree import (
    SourcefreeDirectI02Sections,
    build_sourcefree_direct_i02,
)
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION,
    SourceReleaseManifest,
)
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact,
    ExactRef,
    RespondentEvent,
    WeightMeasureFact,
    canonical_json,
)
from rawlsing_next.pre553_operation_fate_census import (
    CensusRefusal,
    FrozenInputCensus,
    verify_frozen_inputs,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalSourceIncidence
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.pre553_r157_projection_adapter import (
    IDENTITY_CLASS_ORIGINAL,
    SourceConfig,
    build_governed_c11_projection,
    decode_config_with_source_read_permission,
    decode_fixture_config,
    row_native_keys_from_transport,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    GovernedC11Projection,
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
    cell_passes: int
    full_c11_builds: int
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
    for operation in frontier.operations:
        keys = tuple(operation.targets) + tuple(key for key, _ in operation.conditions)
        for key in keys:
            if key.item_id not in slot_names:
                raise SourceI02Refusal(
                    "OPERATION_TARGET_NOT_IN_SOURCE",
                    {"operation_id": getattr(operation, "op_id", None), "item": key.item_id},
                )
    if frontier.source_identity.get("source_sha256") != expected_sha:
        raise SourceI02Refusal("FRONTIER_SOURCE_SHA_MISMATCH")
    try:
        audit = verify_frozen_inputs(
            census, inventory=inventory, policy=policy, frontier=frontier)
    except CensusRefusal as exc:
        raise SourceI02Refusal(exc.code, exc.detail) from exc
    return audit


def _project_spooled_families(
    *,
    config: SourceConfig,
    projection: GovernedC11Projection,
    incidence: PhysicalSourceIncidence,
    spool_paths: Mapping[str, Path],
    batch_size: int,
    row_native_keys: Mapping[int, ExactRef | TypedAbsence] | None = None,
) -> tuple[dict[str, int], dict[str, Any]]:
    """Run exactly one bounded physical cell pass into the private spool."""
    rows = {binding.row_ordinal: binding.respondent_ref for binding in projection.row_bindings}
    respondent_by_ref = {item.ref: item for item in projection.respondents}
    response = {slot.slot.key: slot for slot in projection.response_slots}
    coordinate = {slot.slot.key: slot for slot in projection.coordinate_slots}
    weight = {slot.slot.key: slot for slot in projection.weight_slots}
    projected = set(response) | set(coordinate) | set(weight)
    seen: dict[tuple[int, str], set[int]] = {key: set() for key in projected}
    handles = {
        family: spool_paths[family].open("wb")
        for family in SPOOL_FAMILIES
    }
    counts = {family: 0 for family in SPOOL_FAMILIES}
    key_slot = config.document["respondents"].get("source_native_key_slot")
    key_cells: list[PhysicalCell] = []

    def write(family: str, obj: Any) -> None:
        handles[family].write(
            canonical_json(obj.as_dict()).encode("utf-8") + b"\n")
        counts[family] += 1

    try:
        for cell in incidence.iter_cells(batch_size):
            if not isinstance(cell, PhysicalCell):
                raise SourceI02Refusal("NON_PHYSICAL_CELL_TRANSPORT")
            key = (cell.variable_ordinal, cell.variable_name)
            if key not in projected:
                continue
            if cell.row_ordinal not in rows:
                raise SourceI02Refusal("CELL_ROW_OUTSIDE_PROJECTION", cell.row_ordinal)
            if key_slot is not None and key == (key_slot["ordinal"], key_slot["name"]):
                key_cells.append(cell)
            if cell.row_ordinal in seen[key]:
                raise SourceI02Refusal(
                    "DUPLICATE_PHYSICAL_ROW_SLOT", (cell.row_ordinal, key))
            seen[key].add(cell.row_ordinal)
            respondent = respondent_by_ref[rows[cell.row_ordinal]]
            physical_key = _cell_key(cell)
            if key in response:
                slot = response[key]
                rule = {item.physical_key: item for item in slot.values}.get(physical_key)
                if rule is None:
                    raise SourceI02Refusal(
                        "UNBOUND_RESPONSE_CELL",
                        {"row": cell.row_ordinal, "slot": key},
                    )
                for occurrence in rule.occurrences:
                    write(
                        "RespondentEvent",
                        _event(
                            incidence.source_sha256, cell.row_ordinal, respondent,
                            slot, cell, rule, occurrence, projection,
                        ),
                    )
            if key in coordinate:
                slot = coordinate[key]
                rule = {item.physical_key: item for item in slot.values}.get(
                    physical_key)
                write(
                    "EmpiricalCoordinateFact",
                    _coordinate(
                        incidence.source_sha256, cell.row_ordinal, respondent,
                        slot, cell, rule, projection,
                    ),
                )
            if key in weight:
                slot = weight[key]
                rule = {item.physical_key: item for item in slot.values}.get(
                    physical_key)
                write(
                    "WeightMeasureFact",
                    _weight(
                        incidence.source_sha256, cell.row_ordinal, respondent,
                        slot, cell, rule, projection,
                    ),
                )
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
    return counts, {"rows": len(rows), "projected_slots": len(projected)}


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
) -> SourceI02Handoff:
    """Build one bounded source→direct-I02 handoff.

    The S1-C census is verified before any source read.  A configured
    source-native key slot must have explicit independently derived
    ``row_native_keys``; this adapter does not perform a second key pass.
    """
    if not isinstance(config, SourceConfig):
        config = SourceConfig(config)
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
    if doc["binding"]["identity_class"] == IDENTITY_CLASS_ORIGINAL:
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
        incidence = decode_fixture_config(config, source_path, batch_size=batch_size)
    try:
        if incidence.source_sha256 != doc["binding"]["source_sha256"]:
            raise SourceI02Refusal("DECODED_SOURCE_SHA_MISMATCH")
        if incidence.row_count != doc["binding"]["row_count"]:
            raise SourceI02Refusal("DECODED_SOURCE_ROWS_MISMATCH")
        spool_dir = Path(tempfile.mkdtemp(
            prefix=".s1e-i02-spool-", dir=target.parent))
        spool_paths = {
            family: spool_dir / f"{family}.jsonl" for family in SPOOL_FAMILIES
        }
        try:
            counts, _ = _project_spooled_families(
                config=config,
                projection=projection,
                incidence=incidence,
                spool_paths=spool_paths,
                batch_size=batch_size,
                row_native_keys=row_native_keys,
            )
            manifest, source, declared_counts, absences = _manifest_and_sections(
                projection=projection,
                incidence=incidence,
                spool_paths=spool_paths,
                counts=counts,
                universe_ref=universe_ref,
            )
            roots = build_sourcefree_direct_i02(
                source,
                universe_ref,
                target,
                chunk_size=chunk_size,
            )
            spool_bytes = sum(path.stat().st_size for path in spool_paths.values())
            operation_fates = tuple({
                "operation_id": operation.op_id,
                "disposition": operation.disposition,
                "claim_class": operation.claim_class,
                "execution_state": operation.execution_state,
                "result_state": operation.result_state,
            } for operation in frontier.operations)
            stats = SourceI02Stats(
                source_reads=1,
                cell_passes=1,
                full_c11_builds=0,
                source_rows=incidence.row_count,
                source_columns=len(incidence.variables),
                event_count=counts["RespondentEvent"],
                coordinate_count=counts["EmpiricalCoordinateFact"],
                weight_count=counts["WeightMeasureFact"],
                spool_bytes=spool_bytes,
                spool_files=len(spool_paths),
                cleanup_complete=True,
            )
            return SourceI02Handoff(
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
        finally:
            for path in spool_paths.values():
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass
            try:
                spool_dir.rmdir()
            except OSError:
                pass
    finally:
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
    "build_source_i02_handoff",
    "open_direct_native_i03",
]
