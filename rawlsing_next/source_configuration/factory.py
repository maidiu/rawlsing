"""Executable config-to-existing-owner factory.

The only production target is the existing ``GovernedC11Projection`` and its
source-backed C11 facade.  This module deliberately contains no alternate
engine, no synthetic original universe, and no default authority.
"""
from __future__ import annotations

from dataclasses import fields as dataclass_fields
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalUniverse,
    ExactRef,
    SourceUniverseRelation,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateSlotRule,
    CoordinateValueRule,
    ExactPhysicalCellStream,
    GovernedC11Projection,
    OccurrenceRule,
    PhysicalSlot,
    PhysicalSlotOwnerAuthorization,
    PhysicalSlotOwnerSet,
    ResponseSlotRule,
    ResponseValueRule,
    RowRespondentBinding,
    WeightSlotRule,
    WeightValueRule,
    build_source_backed_c11_repository,
    build_validated_source_backed_c11_release,
    build_validated_source_backed_c11_release_from_stream,
    physical_value_binding_key,
)
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState

from .errors import SourceConfigurationBindingError, SourceConfigurationFactoryError
from .schema import (
    IDENTITY_CLASS_FIXTURE,
    SourceConfig,
    validate_source_config,
)


def _doc(config: SourceConfig | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(config, SourceConfig):
        return config.document
    validate_source_config(config)
    return config


def _typed_absence(value: Mapping[str, Any]) -> TypedAbsence:
    return TypedAbsence(value["typed_absence_state"], value.get("detail"))


def _ref(value: Mapping[str, Any]) -> ExactRef:
    return exact_ref(value, "exact ref")


def _active_identity(doc: Mapping[str, Any], *, source_sha256: str | None,
                     row_count: int | None) -> tuple[str, int, str, str, str]:
    identity = doc["identity"]
    binding = doc["binding"]
    active_sha = binding["source_sha256"] if source_sha256 is None else source_sha256
    active_rows = binding["row_count"] if row_count is None else row_count
    if active_sha != binding["source_sha256"]:
        raise SourceConfigurationBindingError(
            "active source SHA differs from the frozen config binding")
    if active_rows != binding["row_count"]:
        raise SourceConfigurationBindingError(
            "active row count differs from the frozen config binding")
    if binding["identity_class"] == "ORIGINAL_SOURCE":
        if active_sha != identity["expected_source_sha256"]:
            raise SourceConfigurationBindingError(
                "original binding SHA differs from the original source identity")
        if active_rows != identity["source_row_count"]:
            raise SourceConfigurationBindingError(
                "original binding row count differs from the original source identity")
        return (active_sha, active_rows, identity["source_artifact_id"],
                identity["study_product_id"], identity["release_id"])
    fixture = binding["fixture_provenance"]
    if active_sha == identity["expected_source_sha256"]:
        raise SourceConfigurationBindingError(
            "fixture binding may not reuse the original source SHA")
    return (
        active_sha,
        active_rows,
        f"R157_FIXTURE:{fixture['fixture_id']}",
        fixture["fixture_study_product_id"],
        fixture["fixture_release_id"],
    )


def _respondents(doc: Mapping[str, Any], *, active_rows: int,
                 universes: Sequence[EmpiricalUniverse]) -> tuple[Any, ...]:
    universe = universes[0]
    section = doc["respondents"]
    pattern = section["respondent_key_pattern"]
    identity_map = section.get("identity_map_authority_ref")
    identity_map_ref = None if identity_map is None else _authority_ref(identity_map)
    fixture = doc["binding"].get("fixture_provenance")
    respondents = []
    for row in range(1, active_rows + 1):
        if fixture is not None:
            native_key = ExactRef(
                "R157_NONRESPONDENT_FIXTURE_ROW",
                f"urn:rawlsing:r157:fixture:{fixture['fixture_id']}:row:{row}",
                semantic_hash({
                    "fixture_id": fixture["fixture_id"],
                    "row_ordinal": row,
                    "fixture_source_sha256": doc["binding"]["source_sha256"],
                }),
            )
        else:
            native_key = TypedAbsence(
                "UNKNOWN",
                "source-native respondent key is not established in this P0/P3 config slice",
            )
        from rawlsing_next.pre553_c11_integrity import RespondentIdentity
        respondents.append(RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=pattern.format(row_ordinal=row),
            source_native_respondent_key_ref_or_typed_absence=native_key,
            identity_map_authority_ref_or_typed_absence=(
                identity_map_ref if identity_map_ref is not None else TypedAbsence("NOT_AUTHORIZED")
            ),
        ))
    return tuple(respondents)


def _authority_ref(value: Mapping[str, Any]) -> AuthorityRef:
    return AuthorityRef(
        value["authority_id"], value["authority_version"], value["authority_content_hash"])


def _question(payload: Mapping[str, Any]) -> QuestionVariableBinding:
    native = {key: value for key, value in payload.items()
              if key in {field.name for field in dataclass_fields(QuestionVariableBinding)}}
    for name in ("empirical_universe_ref", "native_question_ref"):
        native[name] = _ref(native[name])
    for name in ("canonical_question_ref_or_typed_absence", "component_subitem_ref_or_typed_absence"):
        value = native.get(name)
        if isinstance(value, Mapping):
            native[name] = _typed_absence(value) if "typed_absence_state" in value else _ref(value)
    for name in ("semantic_authority_ref", "topology_authority_ref"):
        native[name] = _authority_ref(native[name])
    return QuestionVariableBinding(**native)


def _occurrence(payload: Mapping[str, Any]) -> OccurrenceRule:
    component = payload.get("component_ref")
    return OccurrenceRule(
        payload["key"],
        _ref(payload["topology_ref"]),
        payload["multiplicity_order_rank_fields"],
        None if component is None else _ref(component),
    )


def _response_slots(doc: Mapping[str, Any], questions: Mapping[str, QuestionVariableBinding]) -> tuple[ResponseSlotRule, ...]:
    result = []
    for section in doc["response_slots"]:
        values = tuple(ResponseValueRule(
            physical_key=physical_value_binding_key(
                value["raw_value"],
                PhysicalMissingState(value["missing_state"]),
                value.get("source_missing_declaration"),
            ),
            response_state=value["response_state"],
            occurrences=tuple(_occurrence(item) for item in value["occurrences"]),
            canonical_value=value.get("canonical_value"),
            transform_authority_ref=(None if value.get("transform_authority_ref") is None
                                     else _authority_ref(value["transform_authority_ref"])),
            extra_authority_refs=tuple(_authority_ref(x) for x in value.get("extra_authority_refs") or ()),
        ) for value in section["values"])
        result.append(ResponseSlotRule(
            PhysicalSlot(section["slot"]["ordinal"], section["slot"]["name"]),
            questions[section["question_id"]],
            values,
        ))
    return tuple(result)


def _coordinate_slots(doc: Mapping[str, Any]) -> tuple[CoordinateSlotRule, ...]:
    result = []
    for section in doc["coordinate_slots"]:
        values = tuple(CoordinateValueRule(
            physical_key=physical_value_binding_key(
                value["raw_value"],
                PhysicalMissingState(value["missing_state"]),
                value.get("source_missing_declaration"),
            ),
            coordinate_state=value["coordinate_state"],
            canonical_value=value.get("canonical_value"),
            extra_authority_refs=tuple(_authority_ref(x) for x in value.get("extra_authority_refs") or ()),
        ) for value in section.get("values", ()))
        normalization = section.get("normalization_ref")
        if isinstance(normalization, Mapping):
            if "typed_absence_state" in normalization:
                normalization = _typed_absence(normalization)
            elif "authority_id" in normalization:
                normalization = _authority_ref(normalization)
            else:
                normalization = _ref(normalization)
        result.append(CoordinateSlotRule(
            slot=PhysicalSlot(section["slot"]["ordinal"], section["slot"]["name"]),
            native_coordinate_ref=_ref(section["native_coordinate_ref"]),
            unit_taxonomy_ref=_ref(section["unit_taxonomy_ref"]),
            effective_time=section["effective_time"],
            source_semantic_authority_ref=_authority_ref(section["source_semantic_authority_ref"]),
            canonical_coordinate_ref=(None if section.get("canonical_coordinate_ref") is None
                                       else _ref(section["canonical_coordinate_ref"])),
            normalization_ref=normalization,
            values=values,
            copy_observed_raw=section.get("copy_observed_raw", False),
        ))
    return tuple(result)


def _weight_slots(doc: Mapping[str, Any]) -> tuple[WeightSlotRule, ...]:
    result = []
    for section in doc["weight_slots"]:
        values = tuple(WeightValueRule(
            physical_key=physical_value_binding_key(
                value["raw_value"],
                PhysicalMissingState(value.get("missing_state", "OBSERVED_STORAGE_VALUE")),
                value.get("source_missing_declaration"),
            ),
            exact_value=value["exact_value"],
            state=value.get("state", "WEIGHT_VALID_AUTHORIZED"),
        ) for value in section.get("values", ()))
        normalization = section.get("normalization_ref")
        if isinstance(normalization, Mapping):
            if "typed_absence_state" in normalization:
                normalization = _typed_absence(normalization)
            elif "authority_id" in normalization:
                normalization = _authority_ref(normalization)
            else:
                normalization = _ref(normalization)
        result.append(WeightSlotRule(
            slot=PhysicalSlot(section["slot"]["ordinal"], section["slot"]["name"]),
            weight_basis_id=section["weight_basis_id"],
            weight_source_ref=_ref(section["weight_source_ref"]),
            design_authority_ref=_authority_ref(section["design_authority_ref"]),
            estimand_authority_ref=_authority_ref(section["estimand_authority_ref"]),
            effective_scope_ref=_ref(section["effective_scope_ref"]),
            normalization_ref=normalization,
            values=values,
            copy_observed_numeric=section.get("copy_observed_numeric", False),
            extra_authority_refs=tuple(_authority_ref(x) for x in section.get("extra_authority_refs") or ()),
        ))
    return tuple(result)


def _routing(doc: Mapping[str, Any], questions: Mapping[str, QuestionVariableBinding],
             respondents: Sequence[Any], *, active_rows: int) -> tuple[Any, ...]:
    from rawlsing_next.pre553_empirical_objects import RoutingEligibilityFact
    result = []
    for rule in doc["routing"]:
        question = questions[rule["question_id"]]
        selector = rule["row_selector"]
        rows = tuple(range(1, active_rows + 1)) if selector == "ALL" else tuple(selector)
        if any(row < 1 or row > active_rows for row in rows):
            raise SourceConfigurationFactoryError(
                "routing row selector is outside the active source row range")
        authority = _authority_ref(rule["authority_ref"])
        replay_root = rule.get("replay_root")
        for row in rows:
            respondent = respondents[row - 1]
            root = (_ref(replay_root) if replay_root is not None else ExactRef(
                "ROUTING_REPLAY_ROOT",
                f"urn:rawlsing:r157:routing:{doc['config_id']}:{rule['question_id']}:{row}",
                semantic_hash({
                    "config_id": doc["config_id"],
                    "question_id": rule["question_id"],
                    "row_ordinal": row,
                    "respondent_ref": respondent.ref.as_dict(),
                }),
            ))
            result.append(RoutingEligibilityFact(
                typed_state=rule["typed_state"],
                authority_snapshot_refs=(authority,),
                dependency_refs=(respondent.ref, *(_ref(x) for x in rule.get("dependency_refs", ()))),
                producer_replay_locator_or_reference_root=root,
                empirical_universe_ref=respondent.empirical_universe_ref,
                scoped_respondent_ref=respondent.ref,
                question_or_target_ref=question.native_question_ref,
                risk_set_ref=_ref(rule["risk_set_ref"]),
                routing_rule_ref=_ref(rule["routing_rule_ref"]),
                applicability_state=rule["typed_state"],
                routing_state=rule["typed_state"],
                parent_predicate_refs=tuple(_ref(x) for x in rule.get("parent_predicate_refs", ())),
                member_set_replay_ref=_ref(rule["member_set_replay_ref"]),
            ))
    return tuple(result)


def _slot_owner_sets(doc: Mapping[str, Any]) -> tuple[PhysicalSlotOwnerSet, ...]:
    result = []
    for item in doc.get("slot_owner_sets", ()):
        owners = tuple(
            PhysicalSlotOwnerAuthorization(
                owner["owner_family"],
                tuple(_authority_ref(x) for x in owner["authority_refs"]),
            )
            for owner in item["owners"]
        )
        result.append(PhysicalSlotOwnerSet(
            PhysicalSlot(item["slot"]["ordinal"], item["slot"]["name"]), owners))
    return tuple(result)


def _source_relations(doc: Mapping[str, Any]) -> tuple[SourceUniverseRelation, ...] | TypedAbsence:
    section = doc["source_relations"]
    if "relations" not in section:
        return TypedAbsence(section["typed_absence_state"])
    return tuple(SourceUniverseRelation(**payload) for payload in section["relations"])


def _replay_absence(doc: Mapping[str, Any], name: str) -> TypedAbsence:
    return _typed_absence(doc["replay"][name])


def build_governed_c11_projection(
    config: SourceConfig | Mapping[str, Any],
    *,
    source_sha256: str | None = None,
    row_count: int | None = None,
) -> GovernedC11Projection:
    """Construct the actual ``GovernedC11Projection`` from a validated config.

    The caller may repeat the active SHA/row count after a permitted decode;
    they must match the frozen binding.  No respondent/value witness is invented
    here: response events and coordinates are created by the existing facade
    only when the physical cell stream is projected.
    """
    doc = _doc(config)
    active_sha, active_rows, artifact_id, study_id, release_id = _active_identity(
        doc, source_sha256=source_sha256, row_count=row_count)
    authority_snapshots = tuple(
        AuthoritySnapshot(**payload) for payload in doc["authority"]["snapshots"])
    universes = tuple(EmpiricalUniverse(**payload) for payload in doc["universe"]["universes"])
    questions_by_id = {
        section["question_id"]: _question(section) for section in doc["questions"]
    }
    respondents = _respondents(doc, active_rows=active_rows, universes=universes)
    row_bindings = tuple(
        RowRespondentBinding(row, respondent.ref)
        for row, respondent in enumerate(respondents, 1)
    )
    binding = doc["binding"]
    if binding["identity_class"] == IDENTITY_CLASS_FIXTURE:
        fixture = binding["fixture_provenance"]
        study_id = fixture["fixture_study_product_id"]
        release_id = fixture["fixture_release_id"]
        instrument_id = fixture["fixture_instrument_release_id"]
        snapshot_ref = _ref(binding["source_snapshot_ref"])
    else:
        instrument_id = doc["identity"]["instrument_release_id"]
        snapshot_ref = _ref(doc["identity"]["source_snapshot_retention_ref"])
    required = tuple(_authority_ref(x) for x in doc["authority"]["required_refs"])
    projection = GovernedC11Projection(
        projection_identity_ref=_ref(doc["authority"]["projection_identity_ref"]),
        source_artifact_id=artifact_id,
        expected_source_sha256=active_sha,
        source_family_id=doc["identity"]["source_family_id"],
        study_product_id=study_id,
        release_id=release_id,
        instrument_release_id=instrument_id,
        source_snapshot_retention_ref=snapshot_ref,
        universes=universes,
        respondents=respondents,
        row_bindings=row_bindings,
        questions=tuple(questions_by_id.values()),
        response_slots=_response_slots(doc, questions_by_id),
        coordinate_slots=_coordinate_slots(doc),
        routing=_routing(doc, questions_by_id, respondents, active_rows=active_rows),
        weight_slots=_weight_slots(doc),
        authority_snapshots=authority_snapshots,
        source_relations=_source_relations(doc),
        predicate_replay=_replay_absence(doc, "predicate"),
        comparator_replay=_replay_absence(doc, "comparator"),
        discovery_replay=_replay_absence(doc, "discovery"),
        structural_replay=_replay_absence(doc, "structural"),
        required_authority_refs=required,
        projection_authority_ref=_authority_ref(doc["authority"]["projection_authority_ref"]),
        replay_authority_ref=_authority_ref(doc["authority"]["replay_authority_ref"]),
        tie_order_ref=_ref(doc["authority"]["tie_order_ref"]),
        replay_protocol_version=doc["authority"]["replay_protocol_version"],
        slot_owner_sets=_slot_owner_sets(doc),
    )
    return projection


# Explicit frozen name used by P0_RETURN.json and source lanes.
construct_governed_c11_projection = build_governed_c11_projection


def _verify_transport(projection: GovernedC11Projection, *,
                      stream: ExactPhysicalCellStream | None,
                      incidence: PhysicalSourceIncidence | None) -> None:
    if (stream is None) == (incidence is None):
        raise SourceConfigurationFactoryError(
            "exactly one of stream or incidence is required")
    source_sha = stream.source_sha256 if stream is not None else incidence.source_sha256
    source_rows = stream.row_count if stream is not None else incidence.row_count
    if source_sha != projection.expected_source_sha256:
        raise SourceConfigurationBindingError("physical transport SHA differs from active config binding")
    if source_rows != len(projection.row_bindings):
        raise SourceConfigurationBindingError("physical transport row count differs from active config binding")


def build_validated_c11_release_from_config(
    config: SourceConfig | Mapping[str, Any],
    *,
    stream: ExactPhysicalCellStream | None = None,
    incidence: PhysicalSourceIncidence | None = None,
    source_sha256: str | None = None,
    row_count: int | None = None,
    batch_size: int = 10_000,
):
    """Build and validate a native C11 release through the existing owner."""
    if stream is not None and incidence is not None:
        raise SourceConfigurationFactoryError("pass exactly one physical transport")
    if stream is None and incidence is None:
        raise SourceConfigurationFactoryError("a permitted physical stream/incidence is required")
    active_sha = source_sha256
    active_rows = row_count
    if stream is not None:
        active_sha = active_sha or stream.source_sha256
        active_rows = active_rows or stream.row_count
    if incidence is not None:
        active_sha = active_sha or incidence.source_sha256
        active_rows = active_rows or incidence.row_count
    projection = build_governed_c11_projection(
        config, source_sha256=active_sha, row_count=active_rows)
    _verify_transport(projection, stream=stream, incidence=incidence)
    if stream is not None:
        return build_validated_source_backed_c11_release_from_stream(stream, projection)
    return build_validated_source_backed_c11_release(incidence, projection, batch_size=batch_size)


def build_source_backed_c11_repository_from_config(
    config: SourceConfig | Mapping[str, Any],
    source: ExactPhysicalCellStream | PhysicalSourceIncidence,
    *,
    cache: Any = None,
    batch_size: int = 10_000,
):
    """Build the existing source-backed C11 repository from a validated config."""
    if not isinstance(source, (ExactPhysicalCellStream, PhysicalSourceIncidence)):
        raise SourceConfigurationFactoryError("existing physical transport is required")
    projection = build_governed_c11_projection(
        config, source_sha256=source.source_sha256, row_count=source.row_count)
    return build_source_backed_c11_repository(
        source, projection, cache=cache, batch_size=batch_size)
