"""PRE553 source-native preimage adapter (B49 T2).

Materializes one exact ``GovernedC11Projection`` from a selected source-rule
package (T1) and an independently specified native instrument inventory plus a
frozen synthetic physical incidence. It classifies every selected package item
as administered measurement U, held, excluded or absent, and never invents a
native field, occurrence or source value.

The adapter consumes only documentary source authority and the existing
physical/C11 owner classes. It does not read raw source bytes, does not issue a
source grant, and does not create scientific E_pre eligibility.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_c11_integrity import (
    QuestionVariableBinding,
    RespondentIdentity,
    TypedAbsence,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalUniverse,
    ExactRef,
    RoutingEligibilityFact,
)
from rawlsing_next.pre553_physical_decoder import (
    PhysicalMissingState,
    PhysicalSourceIncidence,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateSlotRule,
    ExactPhysicalCellStream,
    GovernedC11Projection,
    OccurrenceRule,
    PhysicalSlot,
    ResponseSlotRule,
    ResponseValueRule,
    RowRespondentBinding,
    WeightSlotRule,
    WeightValueRule,
    physical_value_binding_key,
)
from rawlsing_next.pre553_inherited_source_rules import (
    SelectedSourceRulePackage,
    SourceIdentity,
)

SCHEMA = "PRE553_NATIVE_PREIMAGE_BUNDLE@1.0.0"

ADMINISTERED = "ADMINISTERED_MEASUREMENT_U"
HELD_NATIVE_ABSENT = "HELD_NATIVE_VARIABLE_ABSENT"
HELD_PACKAGE = "HELD_PACKAGE_UNRESOLVED"
EXCLUDED = "EXCLUDED_NOT_ADMINISTERED_U"
NOT_IN_INVENTORY = "UNKNOWN_NOT_IN_INVENTORY"


class NativePreimageRefusal(ValueError):
    """A native preimage could not be materialized without inventing a field."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode()).hexdigest()


def _ref(kind: str, tag: str, material: Any = None) -> ExactRef:
    digest = _hash({"kind": kind, "tag": tag, "material": material})
    return ExactRef(kind, f"urn:rawlsing:b49:{kind.lower()}:{tag}", digest)


def _authority_ref(kind: str, tag: str, material: Any = None) -> AuthorityRef:
    digest = _hash({"kind": kind, "tag": tag, "material": material})
    return AuthorityRef(kind, f"urn:rawlsing:b49:authority:{tag}", digest)


@dataclass(frozen=True)
class NativeInstrumentVariable:
    """One exact native instrument variable declared by the source instrument."""

    variable_name: str
    ordinal: int
    declared_domain: tuple[str, ...]
    representation_authority_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.variable_name, str) or not self.variable_name.strip():
            raise NativePreimageRefusal("NATIVE_VARIABLE_NAME_REQUIRED")
        if not isinstance(self.ordinal, int) or isinstance(self.ordinal, bool) or self.ordinal < 1:
            raise NativePreimageRefusal("NATIVE_VARIABLE_ORDINAL_REQUIRED", self.variable_name)


@dataclass(frozen=True)
class InstrumentInventory:
    """Independent instrument inventory for one source edition."""

    source_id: str
    source_sha256: str
    variables: tuple[NativeInstrumentVariable, ...]
    respondent_count: int
    id_variable: str
    country_variable: str
    weight_variable: str
    country_scope: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source_sha256, str) or len(self.source_sha256) != 64:
            raise NativePreimageRefusal("INVENTORY_SOURCE_SHA_REQUIRED")
        if not isinstance(self.respondent_count, int) or self.respondent_count < 1:
            raise NativePreimageRefusal("INVENTORY_RESPONDENT_COUNT_REQUIRED")
        names = [v.variable_name for v in self.variables]
        if len(names) != len(set(names)):
            raise NativePreimageRefusal("DUPLICATE_NATIVE_VARIABLE")
        for required in (self.id_variable, self.country_variable, self.weight_variable):
            if required not in names:
                raise NativePreimageRefusal("INVENTORY_SUPPORT_VARIABLE_MISSING", required)

    @property
    def by_name(self) -> Mapping[str, NativeInstrumentVariable]:
        return {v.variable_name: v for v in self.variables}

    @property
    def inventory_hash(self) -> str:
        return _hash({
            "source_id": self.source_id,
            "source_sha256": self.source_sha256,
            "variables": [
                {"name": v.variable_name, "ordinal": v.ordinal,
                 "domain": list(v.declared_domain)}
                for v in self.variables
            ],
            "respondent_count": self.respondent_count,
            "id_variable": self.id_variable,
            "country_variable": self.country_variable,
            "weight_variable": self.weight_variable,
            "country_scope": list(self.country_scope),
        })


@dataclass(frozen=True)
class AdministeredItem:
    """One classified package item with its exact native disposition."""

    implementation_id: str
    source_variable_code: str
    classification: str
    reason: str
    variable_ordinal: int | None
    semantic_direction: str

    def as_dict(self) -> dict:
        return {
            "implementation_id": self.implementation_id,
            "source_variable_code": self.source_variable_code,
            "classification": self.classification,
            "reason": self.reason,
            "variable_ordinal": self.variable_ordinal,
            "semantic_direction": self.semantic_direction,
        }


@dataclass(frozen=True)
class NativePreimageBundle:
    """Exact source-native projection plus its administered-U classification."""

    schema: str
    source_sha256: str
    package_hash: str
    inventory_hash: str
    projection: GovernedC11Projection
    authorities: tuple[AuthoritySnapshot, ...]
    administered: tuple[AdministeredItem, ...]
    held: tuple[AdministeredItem, ...]
    excluded: tuple[AdministeredItem, ...]
    unknown: tuple[AdministeredItem, ...]
    bundle_hash: str
    question_refs: Mapping[str, ExactRef] = field(default_factory=dict)
    risk_set_ref: ExactRef | None = None

    @property
    def administered_ids(self) -> tuple[str, ...]:
        return tuple(x.implementation_id for x in self.administered)


def build_authority_set(
    *,
    source: SourceIdentity,
    as_of: str,
) -> tuple[AuthoritySnapshot, ...]:
    """Build the exact authority snapshots the projection closure requires.

    These are TEST_ONLY, sourcefree authority snapshots that name the exact source
    identity and as-of. They are not a source grant, a scientific decision or a
    competent issuer record; deployment must replace them with real issuers.
    """
    def snapshot(tag: str, kind: str, families: tuple[str, ...]) -> AuthoritySnapshot:
        digest = _hash({
            "source_sha256": source.declared_sha256,
            "tag": tag,
            "kind": kind,
            "as_of": as_of,
        })
        return AuthoritySnapshot(
            typed_state="ALLOW",
            authority_snapshot_refs=(),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{tag}"),
            authority_id=f"B49-TEST-ONLY-AUTH-{tag}",
            authority_version="1.0.0",
            authority_content_hash=digest,
            authority_kind=kind,
            decision_state="ALLOW",
            governed_operations=(f"B49-OP-{tag}",),
            governed_object_families=families,
            scope_envelope={
                "source_universe_refs": "EXPLICIT_UNRESTRICTED",
                "target_use_refs": "EXPLICIT_UNRESTRICTED",
                "predicate_or_risk_set_refs": "EXPLICIT_UNRESTRICTED",
                "source_sha256": source.declared_sha256,
                "as_of": as_of,
                "grade": "TEST_ONLY_SOURCEFREE",
            },
            effective_time_or_interval=as_of,
            parent_authority_refs=(),
            negative_limit_refs=(),
            supersession_refs=(),
            interpretation_semantics_fingerprint=_hash({
                "source_sha256": source.declared_sha256, "semantics": tag,
            }),
            replay_protocol_ref=_ref("REPLAY_PROTOCOL", tag),
        )

    return (
        snapshot("source", "SOURCE_SEMANTICS_TOPOLOGY",
                 ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0")),
        snapshot("mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
                 ("RespondentEvent@1.0.0",)),
        snapshot("coordinate", "COORDINATE_SEMANTICS",
                 ("EmpiricalCoordinateFact@1.0.0",)),
        snapshot("routing", "ROUTING_RISK_SET",
                 ("RoutingEligibilityFact@1.0.0",)),
        snapshot("weight", "WEIGHT_DESIGN_ESTIMAND",
                 ("WeightMeasureFact@1.0.0",)),
        snapshot("replay", "REPLAY_PROTOCOL", ("ReplayReceipt@1.0.0",)),
        snapshot("projection", "SOURCE_SEMANTICS_TOPOLOGY",
                 ("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0",
                  "WeightMeasureFact@1.0.0")),
    )


def _observed_values(
    incidence: PhysicalSourceIncidence | ExactPhysicalCellStream,
    variable_name: str,
) -> tuple[tuple[str, Any, PhysicalMissingState], ...]:
    """Return the exact observed physical key, raw value and state per variable."""
    seen: list[tuple[str, Any, PhysicalMissingState]] = []
    for cell in incidence.iter_cells():
        if cell.variable_name != variable_name:
            continue
        key = physical_value_binding_key(cell.raw_value, cell.missing_state)
        raw = None if cell.missing_state is not PhysicalMissingState.OBSERVED_STORAGE_VALUE else cell.raw_value
        if (key, cell.missing_state) not in [(k, st) for k, _, st in seen]:
            seen.append((key, raw, cell.missing_state))
    return tuple(seen)


def materialize_native_preimages(
    *,
    package: SelectedSourceRulePackage,
    inventory: InstrumentInventory,
    incidence: PhysicalSourceIncidence | ExactPhysicalCellStream,
    authorities: tuple[AuthoritySnapshot, ...],
    as_of: str,
    source_family: str = "LiTS",
    study_product_id: str = "LiTS-I-SYNTHETIC",
    release_id: str = "B49-SYNTHETIC-REL-1",
    instrument_release_id: str = "B49-SYNTHETIC-INST-1",
) -> NativePreimageBundle:
    """Materialize the exact source-native C11 projection.

    Refuses a wrong source edition, a foreign family, an incidence whose
    respondents/rows disagree with the declared inventory, and any item whose
    native variable is absent without recording it explicitly as held.
    """
    if inventory.source_sha256 != package.source.declared_sha256:
        raise NativePreimageRefusal(
            "WRONG_SOURCE_EDITION",
            f"inventory={inventory.source_sha256} package={package.source.declared_sha256}",
        )
    if incidence.source_sha256 != package.source.declared_sha256:
        raise NativePreimageRefusal(
            "INCIDENCE_SOURCE_EDITION_MISMATCH",
            f"incidence={incidence.source_sha256}",
        )
    if incidence.row_count != inventory.respondent_count:
        raise NativePreimageRefusal(
            "INCIDENCE_ROW_COUNT_MISMATCH",
            f"incidence={incidence.row_count} inventory={inventory.respondent_count}",
        )
    by_name = inventory.by_name
    source_auth, mapping_auth, coord_auth, routing_auth, weight_auth, replay_auth, projection_auth = authorities
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", f"universe-{package.source.source_id}"
        ),
        raw_source_identity=f"RAW-{package.source.family}-{package.source.wave}",
        source_family=source_family,
        study_product_release=f"{study_product_id}/{release_id}",
        instrument_release=instrument_release_id,
        country_geography=",".join(inventory.country_scope),
        sampling_geography=",".join(inventory.country_scope),
        raw_wave=package.source.wave,
        canonical_wave_if_governed=None,
        field_or_reference_time=as_of,
        target_population_and_sample_frame="SYNTHETIC_NONRESPONDENT_FIXTURE",
        sampling_design_regime="B49_SYNTHETIC_DESIGN",
        respondent_namespace=f"NS-{package.source.source_id}",
        source_artifact_import_lineage=f"SOURCE-LINEAGE-{package.source.source_id}",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    respondents = tuple(
        RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=f"SYN-{i}",
            source_native_respondent_key_ref_or_typed_absence=_ref(
                "SOURCE_RESPONDENT", f"{package.source.source_id}-SYN-{i}"
            ),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        )
        for i in range(1, inventory.respondent_count + 1)
    )
    administered: list[AdministeredItem] = []
    held: list[AdministeredItem] = []
    excluded: list[AdministeredItem] = []
    unknown: list[AdministeredItem] = []
    question_bindings: dict[str, QuestionVariableBinding] = {}
    question_refs: dict[str, ExactRef] = {}
    response_slots: list[ResponseSlotRule] = []
    for rule in package.selected:
        variable = by_name.get(rule.source_variable_code)
        if variable is None:
            held.append(AdministeredItem(
                implementation_id=rule.implementation_id,
                source_variable_code=rule.source_variable_code,
                classification=HELD_NATIVE_ABSENT,
                reason="NATIVE_VARIABLE_NOT_IN_DECLARED_INVENTORY",
                variable_ordinal=None,
                semantic_direction=rule.semantic_direction,
            ))
            continue
        binding = QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=_ref(
                "QUESTION_NATIVE", rule.source_variable_code,
                {"ordinal": variable.ordinal, "source_id": package.source.source_id},
            ),
            instrument_question_version=package.source.wave,
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref,
        )
        question_bindings[rule.implementation_id] = binding
        question_refs[rule.source_variable_code] = binding.native_question_ref
        observed = _observed_values(incidence, rule.source_variable_code)
        if not observed:
            held.append(AdministeredItem(
                implementation_id=rule.implementation_id,
                source_variable_code=rule.source_variable_code,
                classification=HELD_NATIVE_ABSENT,
                reason="NO_OBSERVED_SYNTHETIC_CELL_FOR_VARIABLE",
                variable_ordinal=variable.ordinal,
                semantic_direction=rule.semantic_direction,
            ))
            continue
        occurrences = (
            OccurrenceRule(
                "0",
                _ref("TOPOLOGY", f"{rule.source_variable_code}-scalar"),
                {"kind": "SCALAR_SINGULAR", "index": 0},
            ),
        )
        values = []
        for key, raw, state in observed:
            if state is PhysicalMissingState.OBSERVED_STORAGE_VALUE:
                values.append(ResponseValueRule(
                    key, "SUBSTANTIVE_RESPONSE", occurrences, str(raw),
                    mapping_auth.authority_ref,
                ))
            else:
                values.append(ResponseValueRule(
                    key, "MISSING", occurrences, None,
                ))
        response_slots.append(ResponseSlotRule(
            PhysicalSlot(variable.ordinal, variable.variable_name),
            binding,
            tuple(values),
        ))
        administered.append(AdministeredItem(
            implementation_id=rule.implementation_id,
            source_variable_code=rule.source_variable_code,
            classification=ADMINISTERED,
            reason="EXACT_SELECTED_RULE_WITH_NATIVE_VARIABLE_AND_OBSERVED_VALUE",
            variable_ordinal=variable.ordinal,
            semantic_direction=rule.semantic_direction,
        ))
    for rule in package.excluded:
        excluded.append(AdministeredItem(
            implementation_id=rule.implementation_id,
            source_variable_code=rule.source_variable_code,
            classification=EXCLUDED,
            reason=rule.reason,
            variable_ordinal=(
                by_name[rule.source_variable_code].ordinal
                if rule.source_variable_code in by_name else None
            ),
            semantic_direction=rule.semantic_direction,
        ))
    for rule in package.held:
        held.append(AdministeredItem(
            implementation_id=rule.implementation_id,
            source_variable_code=rule.source_variable_code,
            classification=HELD_PACKAGE,
            reason=rule.reason,
            variable_ordinal=(
                by_name[rule.source_variable_code].ordinal
                if rule.source_variable_code in by_name else None
            ),
            semantic_direction=rule.semantic_direction,
        ))
    for rule in (*package.superseded, *package.unknown):
        unknown.append(AdministeredItem(
            implementation_id=rule.implementation_id,
            source_variable_code=rule.source_variable_code,
            classification=NOT_IN_INVENTORY,
            reason=rule.reason,
            variable_ordinal=None,
            semantic_direction=rule.semantic_direction,
        ))
    if not administered:
        raise NativePreimageRefusal("NO_ADMINISTERED_MEASUREMENT_U")
    country_var = by_name[inventory.country_variable]
    weight_var = by_name[inventory.weight_variable]
    risk_ref = _ref("RISK_SET", f"{package.source.source_id}-whole")
    routing: list[RoutingEligibilityFact] = []
    for respondent in respondents:
        for item in administered:
            binding = question_bindings[item.implementation_id]
            routing.append(RoutingEligibilityFact(
                typed_state="ELIGIBLE_APPLICABLE",
                authority_snapshot_refs=(routing_auth.authority_ref,),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref(
                    "REPLAY_ROOT", f"routing-{respondent.respondent_key}-{item.source_variable_code}"
                ),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                question_or_target_ref=binding.native_question_ref,
                risk_set_ref=risk_ref,
                routing_rule_ref=_ref(
                    "ROUTING_RULE", f"{package.source.source_id}-{item.source_variable_code}"
                ),
                applicability_state="ELIGIBLE_APPLICABLE",
                routing_state="ELIGIBLE_APPLICABLE",
                parent_predicate_refs=(),
                member_set_replay_ref=_ref(
                    "MEMBER_SET", f"{package.source.source_id}-all"
                ),
            ))
    weight_observed = _observed_values(incidence, weight_var.variable_name)
    weight_values = []
    for key, raw, state in weight_observed:
        if state is PhysicalMissingState.OBSERVED_STORAGE_VALUE:
            from decimal import Decimal as _Decimal

            weight_values.append(WeightValueRule(
                key,
                _Decimal(str(raw)) if isinstance(raw, float) else raw,
            ))
        else:
            weight_values.append(WeightValueRule(key, None, state="WEIGHT_MISSING"))
    projection = GovernedC11Projection(
        projection_identity_ref=_ref(
            "C11_SEMANTIC_PROJECTION", f"{package.source.source_id}-{package.source.wave}"
        ),
        source_artifact_id=package.source.canonical_filename,
        expected_source_sha256=package.source.declared_sha256,
        source_family_id=source_family,
        study_product_id=study_product_id,
        release_id=release_id,
        instrument_release_id=instrument_release_id,
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT",
            f"urn:rawlsing:b49:snapshot:{package.source.source_id}",
            package.source.declared_sha256,
        ),
        universes=(universe,),
        respondents=respondents,
        row_bindings=tuple(
            RowRespondentBinding(i, respondents[i - 1].ref)
            for i in range(1, inventory.respondent_count + 1)
        ),
        questions=tuple(question_bindings.values()),
        response_slots=tuple(response_slots),
        coordinate_slots=(
            CoordinateSlotRule(
                PhysicalSlot(country_var.ordinal, country_var.variable_name),
                _ref("COORDINATE_NATIVE", f"{package.source.source_id}-{country_var.variable_name}"),
                _ref("UNIT_TAXONOMY", f"{package.source.source_id}-country"),
                as_of,
                coord_auth.authority_ref,
                copy_observed_raw=True,
            ),
        ),
        routing=tuple(routing),
        weight_slots=(
            WeightSlotRule(
                PhysicalSlot(weight_var.ordinal, weight_var.variable_name),
                weight_var.variable_name,
                _ref("WEIGHT_SOURCE", f"{package.source.source_id}-{weight_var.variable_name}"),
                weight_auth.authority_ref,
                weight_auth.authority_ref,
                _ref("SCOPE", f"{package.source.source_id}-whole"),
                values=tuple(weight_values),
            ),
        ),
        authority_snapshots=authorities,
        source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(a.authority_ref for a in authorities),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=_ref("ORDER_RULE", f"{package.source.source_id}-canonical-ref-sort"),
        replay_protocol_version="1.0.0",
    )
    material = {
        "schema": SCHEMA,
        "source_sha256": package.source.declared_sha256,
        "package_hash": package.package_hash,
        "inventory_hash": inventory.inventory_hash,
        "projection": projection.projection_identity_ref.as_dict(),
        "administered": [x.as_dict() for x in administered],
        "held": [x.as_dict() for x in held],
        "excluded": [x.as_dict() for x in excluded],
        "unknown": [x.as_dict() for x in unknown],
    }
    return NativePreimageBundle(
        schema=SCHEMA,
        source_sha256=package.source.declared_sha256,
        package_hash=package.package_hash,
        inventory_hash=inventory.inventory_hash,
        projection=projection,
        authorities=authorities,
        administered=tuple(administered),
        held=tuple(held),
        excluded=tuple(excluded),
        unknown=tuple(unknown),
        bundle_hash=_hash(material),
        question_refs=dict(question_refs),
        risk_set_ref=risk_ref,
    )


def _is_number(value: str) -> bool:
    try:
        float(value)
    except (TypeError, ValueError):
        return False
    return True


__all__ = [
    "ADMINISTERED",
    "AdministeredItem",
    "EXCLUDED",
    "HELD_NATIVE_ABSENT",
    "HELD_PACKAGE",
    "InstrumentInventory",
    "NOT_IN_INVENTORY",
    "NativeInstrumentVariable",
    "NativePreimageBundle",
    "NativePreimageRefusal",
    "SCHEMA",
    "build_authority_set",
    "materialize_native_preimages",
]
