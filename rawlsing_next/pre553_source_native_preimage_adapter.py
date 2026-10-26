"""PRE553 governed source-native occurrence projection.

The adapter turns an exact decoded physical source into a governed C11
projection. Rectangular one-row-per-respondent sources retain the existing
scalar behaviour. Repeated sources must supply an explicit governed row and
occurrence mapping; rows are bound to source respondent identifiers and cells
are bound to the declared source occasion. Equal values at different occasions
therefore remain distinct C11 events.
"""
from __future__ import annotations

import hashlib
import json
import math
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
    PhysicalCell,
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
    SourceBackedC11FacadeError,
    build_validated_source_backed_c11_release_from_stream,
    physical_value_binding_key,
)

SCHEMA = "PRE553_NATIVE_OCCURRENCE_PREIMAGE_BUNDLE@1.0.0"
OCCURRENCE_BINDING_SCHEMA = "PRE553_GOVERNED_OCCURRENCE_BINDING@1.0.0"
ADMINISTERED = "ADMINISTERED_MEASUREMENT_U"
HELD_NATIVE_ABSENT = "HELD_NATIVE_VARIABLE_ABSENT"
HELD_NOT_ADMINISTERED = "HELD_NOT_ADMINISTERED"
HELD_PACKAGE = "HELD_PACKAGE_UNRESOLVED"
EXCLUDED = "EXCLUDED_NOT_ADMINISTERED_U"
NOT_IN_INVENTORY = "UNKNOWN_NOT_IN_SOURCE"


class NativePreimageRefusal(ValueError):
    """A source-native projection cannot be built without inventing meaning."""

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
    return ExactRef(kind, f"urn:rawlsing:r56:{kind.lower()}:{tag}", digest)


def _authority_ref(kind: str, tag: str, material: Any = None) -> AuthorityRef:
    digest = _hash({"kind": kind, "tag": tag, "material": material})
    return AuthorityRef(kind, f"urn:rawlsing:r56:authority:{tag}", digest)


def token(value: Any) -> str:
    """Return a stable textual token for an exact source value."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isfinite(value) and value.is_integer():
            return str(int(value))
        return repr(value)
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _normalized_source_identity(value: Any) -> str:
    """Return the admitted exact token for a source identity value.

    Mapping keys are validated on the same representation used for source-cell
    lookup. Unsupported types and non-finite floats are refused before any
    mapping dictionary is constructed.
    """
    if isinstance(value, (bool, int, str)):
        return token(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise NativePreimageRefusal(
                "NON_FINITE_SOURCE_IDENTITY", repr(value))
        return token(value)
    raise NativePreimageRefusal(
        "NON_ADMITTED_SOURCE_IDENTITY_TYPE", type(value).__name__)


def _normalized_respondent_identity(value: Any) -> str:
    """Return the admitted string respondent key for a governed mapping value.

    Scalar numerics/bools retain the adapter's historical string form; empty
    strings and non-scalar/None values are refused rather than silently
    stringified into an ambiguous respondent identity.
    """
    if isinstance(value, str):
        if not value.strip():
            raise NativePreimageRefusal("EMPTY_RESPONDENT_KEY")
        return value
    if isinstance(value, (bool, int)):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise NativePreimageRefusal(
                "NON_FINITE_RESPONDENT_KEY", repr(value))
        return str(value)
    raise NativePreimageRefusal(
        "NON_ADMITTED_RESPONDENT_KEY_TYPE", type(value).__name__)


def _observed(cell: PhysicalCell | None) -> bool:
    return cell is not None and cell.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE


@dataclass(frozen=True)
class NativeSourceIdentity:
    source_id: str
    family: str
    wave: str
    canonical_filename: str
    declared_sha256: str
    source_format: str
    expected_rows: int | None = None

    def __post_init__(self) -> None:
        for name in ("source_id", "family", "wave", "canonical_filename", "source_format"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise NativePreimageRefusal("SOURCE_IDENTITY_FIELD_REQUIRED", name)
        if not isinstance(self.declared_sha256, str) or len(self.declared_sha256) != 64:
            raise NativePreimageRefusal("DECLARED_SOURCE_SHA_REQUIRED", self.canonical_filename)
        if self.expected_rows is not None and (
            not isinstance(self.expected_rows, int) or self.expected_rows < 1
        ):
            raise NativePreimageRefusal("EXPECTED_ROW_COUNT_INVALID", self.canonical_filename)

    @property
    def identity_hash(self) -> str:
        return _hash({
            "source_id": self.source_id, "family": self.family, "wave": self.wave,
            "canonical_filename": self.canonical_filename,
            "declared_sha256": self.declared_sha256,
            "source_format": self.source_format, "expected_rows": self.expected_rows,
        })


@dataclass(frozen=True)
class NativeSourceRule:
    implementation_id: str
    source_variable_code: str
    unit: str = "person"
    administered: bool = True
    semantic_direction: str = "NOT_CERTIFIED"
    value_aliases: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("implementation_id", "source_variable_code", "unit"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise NativePreimageRefusal("SOURCE_RULE_FIELD_REQUIRED", name)
        if not isinstance(self.administered, bool):
            raise NativePreimageRefusal("SOURCE_RULE_ADMINISTERED_FLAG_REQUIRED",
                                        self.implementation_id)
        if not isinstance(self.value_aliases, Mapping):
            raise NativePreimageRefusal("SOURCE_RULE_VALUE_ALIASES_REQUIRED",
                                        self.implementation_id)


@dataclass(frozen=True)
class NativeSourcePackage:
    source: NativeSourceIdentity
    selected: tuple[NativeSourceRule, ...]
    excluded: tuple[NativeSourceRule, ...] = ()
    held: tuple[NativeSourceRule, ...] = ()
    unknown: tuple[NativeSourceRule, ...] = ()
    coordinate_variable: str = ""
    coordinate_unit: str = "person"
    coordinate_effective_time: str = "TEST_ONLY"
    study_product_id: str = "R56-SYNTHETIC-STUDY"
    release_id: str = "R56-SYNTHETIC-RELEASE"
    instrument_release_id: str = "R56-SYNTHETIC-INSTRUMENT"
    as_of: str = "TEST_ONLY"

    def __post_init__(self) -> None:
        if not self.selected:
            raise NativePreimageRefusal("SELECTED_SOURCE_RULE_REQUIRED")
        if not self.coordinate_variable:
            raise NativePreimageRefusal("COORDINATE_VARIABLE_REQUIRED")
        for name in ("coordinate_variable", "coordinate_unit", "coordinate_effective_time",
                     "study_product_id", "release_id", "instrument_release_id", "as_of"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise NativePreimageRefusal("SOURCE_PACKAGE_FIELD_REQUIRED", name)
        ids = [rule.implementation_id for rule in self.selected]
        if len(ids) != len(set(ids)):
            raise NativePreimageRefusal("DUPLICATE_IMPLEMENTATION_ID")
        variables = [rule.source_variable_code for rule in self.selected]
        if len(variables) != len(set(variables)):
            raise NativePreimageRefusal("DUPLICATE_SELECTED_SOURCE_VARIABLE")
        administered_units = {rule.unit for rule in self.selected if rule.administered}
        if len(administered_units) > 1:
            raise NativePreimageRefusal(
                "CROSS_UNIT_POOLING_UNAUTHORIZED", ",".join(sorted(administered_units)))

    @property
    def package_hash(self) -> str:
        return _hash({
            "source": self.source.identity_hash,
            "selected": [
                {"implementation_id": r.implementation_id,
                 "source_variable_code": r.source_variable_code, "unit": r.unit,
                 "administered": r.administered,
                 "semantic_direction": r.semantic_direction,
                 "value_aliases": dict(r.value_aliases)}
                for r in self.selected
            ],
            "excluded": [r.implementation_id for r in self.excluded],
            "held": [r.implementation_id for r in self.held],
            "unknown": [r.implementation_id for r in self.unknown],
            "coordinate_variable": self.coordinate_variable,
            "coordinate_unit": self.coordinate_unit,
            "study_product_id": self.study_product_id,
            "release_id": self.release_id,
            "instrument_release_id": self.instrument_release_id,
            "as_of": self.as_of,
        })


@dataclass(frozen=True)
class OccurrenceBinding:
    source_value: str
    occurrence_key: str
    fields: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.source_value, str) or not self.source_value:
            raise NativePreimageRefusal("OCCURRENCE_SOURCE_VALUE_REQUIRED")
        if not isinstance(self.occurrence_key, str) or not self.occurrence_key:
            raise NativePreimageRefusal("OCCURRENCE_KEY_REQUIRED")
        if not isinstance(self.fields, Mapping) or not self.fields:
            raise NativePreimageRefusal("OCCURRENCE_FIELDS_REQUIRED", self.occurrence_key)


@dataclass(frozen=True)
class VariableOccurrencePlan:
    source_variable_code: str
    topology_kind: str
    bindings: tuple[OccurrenceBinding, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source_variable_code, str) or not self.source_variable_code:
            raise NativePreimageRefusal("OCCURRENCE_VARIABLE_REQUIRED")
        if not isinstance(self.topology_kind, str) or not self.topology_kind:
            raise NativePreimageRefusal("OCCURRENCE_TOPOLOGY_REQUIRED",
                                        self.source_variable_code)
        if not self.bindings:
            raise NativePreimageRefusal("OCCURRENCE_BINDINGS_REQUIRED",
                                        self.source_variable_code)
        values = [b.source_value for b in self.bindings]
        keys = [b.occurrence_key for b in self.bindings]
        if len(values) != len(set(values)):
            raise NativePreimageRefusal("DUPLICATE_OCCURRENCE_SOURCE_VALUE",
                                        self.source_variable_code)
        if len(keys) != len(set(keys)):
            raise NativePreimageRefusal("DUPLICATE_OCCURRENCE_KEY",
                                        self.source_variable_code)
        for binding in self.bindings:
            kind = binding.fields.get("kind")
            if kind is not None and kind != self.topology_kind:
                raise NativePreimageRefusal(
                    "OCCURRENCE_FIELD_TOPOLOGY_MISMATCH",
                    f"{self.source_variable_code}:{binding.occurrence_key}")
        if self.topology_kind == "SCALAR_SINGULAR" and len(self.bindings) != 1:
            raise NativePreimageRefusal("SCALAR_OCCURRENCE_PLAN_AMBIGUOUS",
                                        self.source_variable_code)

    @property
    def by_source_value(self) -> Mapping[str, OccurrenceBinding]:
        return {b.source_value: b for b in self.bindings}


@dataclass(frozen=True)
class GovernedRowOccurrencePlan:
    respondent_variable: str
    occasion_variable: str
    variable_plans: tuple[VariableOccurrencePlan, ...]
    respondent_key_by_source_value: Mapping[str, str]

    def __post_init__(self) -> None:
        for name in ("respondent_variable", "occasion_variable"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise NativePreimageRefusal("ROW_OCCURRENCE_FIELD_REQUIRED", name)
        if not self.variable_plans:
            raise NativePreimageRefusal("ROW_OCCURRENCE_VARIABLE_PLAN_REQUIRED")
        variables = [p.source_variable_code for p in self.variable_plans]
        if len(variables) != len(set(variables)):
            raise NativePreimageRefusal("DUPLICATE_OCCURRENCE_VARIABLE_PLAN")
        if not isinstance(self.respondent_key_by_source_value, Mapping):
            raise NativePreimageRefusal("RESPONDENT_KEY_MAPPING_REQUIRED")
        values = list(self.respondent_key_by_source_value.values())
        try:
            raw_duplicate = len(values) != len(set(values))
        except TypeError:
            raw_duplicate = False
        if raw_duplicate:
            raise NativePreimageRefusal("DUPLICATE_RESPONDENT_KEY_MAPPING")

    @property
    def plan_by_variable(self) -> Mapping[str, VariableOccurrencePlan]:
        return {p.source_variable_code: p for p in self.variable_plans}

    def normalized_respondent_mapping(self) -> Mapping[str, str]:
        """Return the admitted source-token -> respondent-key bijection.

        All admission, normalization and uniqueness checks run before the
        lookup dictionary is constructed. A duplicate normalized source key or
        destination key therefore refuses instead of being collapsed by a
        last-wins dictionary comprehension.
        """
        normalized: list[tuple[str, str]] = []
        for source_value, respondent_key in self.respondent_key_by_source_value.items():
            normalized.append((
                _normalized_source_identity(source_value),
                _normalized_respondent_identity(respondent_key),
            ))
        source_tokens = [source_token for source_token, _ in normalized]
        respondent_keys = [respondent_key for _, respondent_key in normalized]
        if len(source_tokens) != len(set(source_tokens)):
            duplicates = sorted(
                source_token for source_token in set(source_tokens)
                if source_tokens.count(source_token) > 1)
            raise NativePreimageRefusal(
                "DUPLICATE_NORMALIZED_SOURCE_KEY", ",".join(duplicates))
        if len(respondent_keys) != len(set(respondent_keys)):
            duplicates = sorted(
                respondent_key for respondent_key in set(respondent_keys)
                if respondent_keys.count(respondent_key) > 1)
            raise NativePreimageRefusal(
                "DUPLICATE_RESPONDENT_KEY_MAPPING", ",".join(duplicates))
        return {
            source_token: respondent_key
            for source_token, respondent_key in normalized
        }


@dataclass(frozen=True)
class AdministeredItem:
    implementation_id: str
    source_variable_code: str
    classification: str
    reason: str
    unit: str
    semantic_direction: str

    def as_dict(self) -> dict:
        return {
            "implementation_id": self.implementation_id,
            "source_variable_code": self.source_variable_code,
            "classification": self.classification,
            "reason": self.reason,
            "unit": self.unit,
            "semantic_direction": self.semantic_direction,
        }


@dataclass(frozen=True)
class NativePreimageBundle:
    schema: str
    source_sha256: str
    package_hash: str
    projection: GovernedC11Projection
    physical_stream: ExactPhysicalCellStream
    release: Any
    administered: tuple[AdministeredItem, ...]
    held: tuple[AdministeredItem, ...]
    excluded: tuple[AdministeredItem, ...]
    unknown: tuple[AdministeredItem, ...]
    bundle_hash: str
    question_refs: Mapping[str, ExactRef]
    risk_set_ref: ExactRef
    respondent_rows: tuple[Mapping[str, Any], ...]
    occurrence_bindings: tuple[Mapping[str, Any], ...]
    source_format: str = "UNKNOWN"

    @property
    def administered_ids(self) -> tuple[str, ...]:
        return tuple(x.implementation_id for x in self.administered)


def build_authority_set(*, source: NativeSourceIdentity,
                        as_of: str) -> tuple[AuthoritySnapshot, ...]:
    def snapshot(tag: str, kind: str, families: tuple[str, ...]) -> AuthoritySnapshot:
        digest = _hash({
            "source_sha256": source.declared_sha256, "tag": tag,
            "kind": kind, "as_of": as_of,
        })
        return AuthoritySnapshot(
            typed_state="ALLOW",
            authority_snapshot_refs=(),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{tag}"),
            authority_id=f"R56-TEST-ONLY-AUTH-{tag}",
            authority_version="1.0.0",
            authority_content_hash=digest,
            authority_kind=kind,
            decision_state="ALLOW",
            governed_operations=(f"R56-OP-{tag}",),
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


def _row_cells(cells: Iterable[PhysicalCell], row_count: int) -> dict[int, dict[str, PhysicalCell]]:
    rows: dict[int, dict[str, PhysicalCell]] = {}
    for cell in cells:
        row = rows.setdefault(cell.row_ordinal, {})
        if cell.variable_name in row:
            raise NativePreimageRefusal(
                "DUPLICATE_PHYSICAL_CELL", f"row={cell.row_ordinal}:{cell.variable_name}")
        row[cell.variable_name] = cell
    if set(rows) != set(range(1, row_count + 1)):
        raise NativePreimageRefusal("INCIDENCE_ROW_ORDINALS_INCOMPLETE",
                                    f"observed={sorted(rows)} expected={row_count}")
    return rows


def _require_observed_cell(row: Mapping[str, PhysicalCell], variable: str,
                           *, context: str) -> PhysicalCell:
    cell = row.get(variable)
    if not _observed(cell):
        raise NativePreimageRefusal("MISSING_GOVERNED_SOURCE_IDENTITY",
                                    f"{context}:{variable}")
    return cell


def _governed_declaration(cell: PhysicalCell, binding: OccurrenceBinding) -> dict:
    return {
        "schema": OCCURRENCE_BINDING_SCHEMA,
        "source_declaration": cell.source_missing_declaration,
        "occurrence_key": binding.occurrence_key,
        "source_value": binding.source_value,
        "fields": dict(binding.fields),
    }


def _occurrence_rule(plan: VariableOccurrencePlan, binding: OccurrenceBinding,
                     source_id: str) -> OccurrenceRule:
    fields = dict(binding.fields)
    fields.setdefault("kind", plan.topology_kind)
    if fields["kind"] != plan.topology_kind:
        raise NativePreimageRefusal(
            "OCCURRENCE_FIELD_TOPOLOGY_MISMATCH", binding.occurrence_key)
    return OccurrenceRule(
        binding.occurrence_key,
        _ref("TOPOLOGY", f"{source_id}-{plan.source_variable_code}-"
                         f"{binding.occurrence_key}"),
        fields,
    )


def materialize_native_preimages(
    *,
    package: NativeSourcePackage,
    incidence: PhysicalSourceIncidence | ExactPhysicalCellStream,
    row_occurrence_plan: GovernedRowOccurrencePlan | None = None,
    authorities: tuple[AuthoritySnapshot, ...] | None = None,
) -> NativePreimageBundle:
    """Materialize a governed C11 release from exact source cells.

    A supplied row/occurrence plan is mandatory for repeated-cell sources. No
    row index, floor, modulo, adjacency or fixed occasion count is used.
    """
    if incidence.source_sha256 != package.source.declared_sha256:
        raise NativePreimageRefusal(
            "WRONG_SOURCE_EDITION",
            f"incidence={incidence.source_sha256} package={package.source.declared_sha256}")
    if package.source.expected_rows is not None and incidence.row_count != package.source.expected_rows:
        raise NativePreimageRefusal(
            "SOURCE_ROW_COUNT_MISMATCH",
            f"incidence={incidence.row_count} expected={package.source.expected_rows}")
    if isinstance(incidence, PhysicalSourceIncidence) and package.source.source_format:
        if incidence.source_format != package.source.source_format:
            raise NativePreimageRefusal(
                "SOURCE_FORMAT_MISMATCH",
                f"incidence={incidence.source_format} package={package.source.source_format}")

    all_cells = tuple(incidence.iter_cells())
    rows = _row_cells(all_cells, incidence.row_count)
    source = package.source
    if authorities is None:
        authorities = build_authority_set(source=source, as_of=package.as_of)
    else:
        authorities = tuple(authorities)
        if len(authorities) != 7 or any(not isinstance(a, AuthoritySnapshot) for a in authorities):
            raise NativePreimageRefusal("SUPPLIED_AUTHORITY_SET_INVALID")
        if any(a.typed_state != "ALLOW" or a.decision_state != "ALLOW" for a in authorities):
            raise NativePreimageRefusal("SUPPLIED_AUTHORITY_NOT_ALLOW")
        expected_kinds = (
            "SOURCE_SEMANTICS_TOPOLOGY",
            "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
            "COORDINATE_SEMANTICS",
            "ROUTING_RISK_SET",
            "WEIGHT_DESIGN_ESTIMAND",
            "REPLAY_PROTOCOL",
            "SOURCE_SEMANTICS_TOPOLOGY",
        )
        if tuple(a.authority_kind for a in authorities) != expected_kinds:
            raise NativePreimageRefusal("SUPPLIED_AUTHORITY_ROLE_MISMATCH")
        for authority in authorities:
            scope = authority.scope_envelope
            if not isinstance(scope, Mapping) or scope.get("source_sha256") != source.declared_sha256:
                raise NativePreimageRefusal(
                    "SUPPLIED_AUTHORITY_SOURCE_MISMATCH", authority.authority_id)
    source_auth, mapping_auth, coord_auth, routing_auth, weight_auth, replay_auth, projection_auth = authorities
    variable_names = {name for row in rows.values() for name in row}
    for required in (package.coordinate_variable,):
        if required not in variable_names:
            raise NativePreimageRefusal("COORDINATE_VARIABLE_ABSENT", required)

    plan_by_variable: Mapping[str, VariableOccurrencePlan] = {}
    if row_occurrence_plan is not None:
        for name in (row_occurrence_plan.respondent_variable,
                     row_occurrence_plan.occasion_variable):
            if name not in variable_names:
                raise NativePreimageRefusal("ROW_OCCURRENCE_VARIABLE_ABSENT", name)
        plan_by_variable = row_occurrence_plan.plan_by_variable
        selected_names = {r.source_variable_code for r in package.selected if r.administered}
        if set(plan_by_variable) != selected_names:
            raise NativePreimageRefusal(
                "OCCURRENCE_PLAN_SELECTED_VARIABLE_MISMATCH",
                f"plan={sorted(plan_by_variable)} selected={sorted(selected_names)}")
        if package.coordinate_variable in plan_by_variable:
            raise NativePreimageRefusal("COORDINATE_AND_RESPONSE_SLOT_COLLISION",
                                        package.coordinate_variable)

    respondent_token_by_row: dict[int, str] = {}
    occasion_token_by_row: dict[int, str] = {}
    if row_occurrence_plan is None:
        for row_ordinal in sorted(rows):
            respondent_token_by_row[row_ordinal] = f"ROW-{row_ordinal:04d}"
    else:
        mapping = row_occurrence_plan.normalized_respondent_mapping()
        allowed = set(mapping)
        for row_ordinal, row in rows.items():
            respondent_cell = _require_observed_cell(
                row, row_occurrence_plan.respondent_variable, context="respondent")
            respondent_token = token(respondent_cell.raw_value)
            if respondent_token not in allowed or not mapping[respondent_token]:
                raise NativePreimageRefusal("UNMAPPED_SOURCE_RESPONDENT", respondent_token)
            occasion_cell = _require_observed_cell(
                row, row_occurrence_plan.occasion_variable, context="occasion")
            respondent_token_by_row[row_ordinal] = mapping[respondent_token]
            occasion_token_by_row[row_ordinal] = token(occasion_cell.raw_value)

    respondent_keys = sorted(set(respondent_token_by_row.values()))
    by_respondent_key = {}
    for key in respondent_keys:
        source_tokens = sorted(
            {token(rows[row][row_occurrence_plan.respondent_variable].raw_value)
             for row in rows if respondent_token_by_row[row] == key}
        ) if row_occurrence_plan else (key,)
        by_respondent_key[key] = _ref(
            "SOURCE_RESPONDENT", f"{source.source_id}-{key}",
            {"source_tokens": source_tokens})

    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", f"universe-{source.source_id}"),
        raw_source_identity=f"RAW-{source.family}-{source.wave}",
        source_family=source.family,
        study_product_release=f"{package.study_product_id}/{package.release_id}",
        instrument_release=package.instrument_release_id,
        country_geography="ZZ",
        sampling_geography="ZZ-SYNTHETIC",
        raw_wave=source.wave,
        canonical_wave_if_governed=None,
        field_or_reference_time=package.as_of,
        target_population_and_sample_frame="SYNTHETIC_SOURCEFREE",
        sampling_design_regime="TEST_ONLY",
        respondent_namespace=f"NS-{source.source_id}",
        source_artifact_import_lineage=f"LINEAGE-{source.source_id}",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    respondents = tuple(
        RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=f"{source.source_id}:{key}",
            source_native_respondent_key_ref_or_typed_absence=by_respondent_key[key],
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        )
        for key in respondent_keys
    )
    respondent_by_key = {key: respondents[i] for i, key in enumerate(respondent_keys)}
    row_bindings = tuple(
        RowRespondentBinding(row, respondent_by_key[respondent_token_by_row[row]].ref)
        for row in sorted(rows)
    )

    administered: list[AdministeredItem] = []
    held: list[AdministeredItem] = []
    excluded: list[AdministeredItem] = []
    unknown: list[AdministeredItem] = []
    question_bindings: list[QuestionVariableBinding] = []
    question_refs: dict[str, ExactRef] = {}
    response_slots: list[ResponseSlotRule] = []
    routing_questions: list[tuple[str, ExactRef]] = []
    occurrence_evidence: list[dict] = []

    for rule in package.selected:
        variable_name = rule.source_variable_code
        if not rule.administered:
            held.append(AdministeredItem(
                implementation_id=rule.implementation_id,
                source_variable_code=variable_name,
                classification=HELD_NOT_ADMINISTERED,
                reason="SOURCE_RULE_NOT_ADMINISTERED",
                unit=rule.unit, semantic_direction=rule.semantic_direction))
            continue
        if variable_name not in variable_names:
            held.append(AdministeredItem(
                implementation_id=rule.implementation_id,
                source_variable_code=variable_name,
                classification=HELD_NATIVE_ABSENT,
                reason="NATIVE_VARIABLE_NOT_IN_SOURCE",
                unit=rule.unit, semantic_direction=rule.semantic_direction))
            continue
        native_question_ref = _ref(
            "QUESTION_NATIVE", f"{source.source_id}-{variable_name}",
            {"wave": source.wave, "variable": variable_name})
        binding = QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=native_question_ref,
            instrument_question_version=source.wave,
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref,
        )
        question_bindings.append(binding)
        question_refs[variable_name] = native_question_ref
        routing_questions.append((variable_name, native_question_ref))
        occurrence_rules_by_key: dict[tuple[str, str], OccurrenceRule] = {}
        value_rules: dict[tuple[str, str], ResponseValueRule] = {}
        per_respondent_occurrences: dict[str, set[str]] = {}
        for row_ordinal, row in rows.items():
            cell = row.get(variable_name)
            if cell is None:
                raise NativePreimageRefusal(
                    "SELECTED_VARIABLE_CELL_ABSENT",
                    f"row={row_ordinal}:{variable_name}")
            if row_occurrence_plan is None:
                occurrence_rule = OccurrenceRule(
                    "0", _ref("TOPOLOGY", f"{source.source_id}-{variable_name}-scalar"),
                    {"kind": "SCALAR_SINGULAR", "index": 0})
                transformed = cell
            else:
                variable_plan = plan_by_variable[variable_name]
                occasion_token = occasion_token_by_row[row_ordinal]
                occurrence_binding = variable_plan.by_source_value.get(occasion_token)
                if occurrence_binding is None:
                    raise NativePreimageRefusal(
                        "UNMAPPED_SOURCE_OCCASION",
                        f"{variable_name}:{occasion_token}")
                occurrence_rule = _occurrence_rule(
                    variable_plan, occurrence_binding, source.source_id)
                declaration = _governed_declaration(cell, occurrence_binding)
                transformed = PhysicalCell(
                    row_ordinal=cell.row_ordinal,
                    variable_ordinal=cell.variable_ordinal,
                    variable_name=cell.variable_name,
                    raw_value=cell.raw_value,
                    missing_state=cell.missing_state,
                    source_missing_declaration=declaration,
                    raw_value_label=cell.raw_value_label,
                )
                occurrence_evidence.append({
                    "variable": variable_name, "row": row_ordinal,
                    "source_respondent": respondent_token_by_row[row_ordinal],
                    "source_occasion": occasion_token,
                    "occurrence_key": occurrence_binding.occurrence_key,
                    "fields": dict(occurrence_rule.multiplicity_order_rank_fields),
                })
            occurrence_key = (variable_name, occurrence_rule.key)
            occurrence_rules_by_key.setdefault(occurrence_key, occurrence_rule)
            physical_key = physical_value_binding_key(
                transformed.raw_value, transformed.missing_state,
                transformed.source_missing_declaration)
            respondent_key = respondent_token_by_row[row_ordinal]
            seen = per_respondent_occurrences.setdefault(respondent_key, set())
            if occurrence_rule.key in seen:
                raise NativePreimageRefusal(
                    "DUPLICATE_OCCURRENCE_IDENTITY",
                    f"{variable_name}:{respondent_key}:{occurrence_rule.key}")
            seen.add(occurrence_rule.key)
            rule_key = (occurrence_rule.key, physical_key)
            if rule_key not in value_rules:
                if transformed.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE:
                    raw_token = token(transformed.raw_value)
                    canonical = rule.value_aliases.get(raw_token, raw_token)
                    state = "SUBSTANTIVE_RESPONSE"
                else:
                    canonical = None
                    state = "MISSING"
                value_rules[rule_key] = ResponseValueRule(
                    physical_key, state, (occurrence_rule,), canonical,
                    mapping_auth.authority_ref)
        response_slots.append(ResponseSlotRule(
            PhysicalSlot(
                rows[min(rows)][variable_name].variable_ordinal, variable_name),
            binding,
            tuple(value_rules[key] for key in sorted(value_rules))))
        administered.append(AdministeredItem(
            implementation_id=rule.implementation_id,
            source_variable_code=variable_name,
            classification=ADMINISTERED,
            reason="EXACT_GOVERNED_SOURCE_OCCURRENCE",
            unit=rule.unit, semantic_direction=rule.semantic_direction))

    for rule in package.excluded:
        excluded.append(AdministeredItem(
            implementation_id=rule.implementation_id,
            source_variable_code=rule.source_variable_code,
            classification=EXCLUDED, reason="EXCLUDED_BY_PACKAGE",
            unit=rule.unit, semantic_direction=rule.semantic_direction))
    for rule in package.held:
        held.append(AdministeredItem(
            implementation_id=rule.implementation_id,
            source_variable_code=rule.source_variable_code,
            classification=HELD_PACKAGE, reason="HELD_BY_PACKAGE",
            unit=rule.unit, semantic_direction=rule.semantic_direction))
    for rule in package.unknown:
        unknown.append(AdministeredItem(
            implementation_id=rule.implementation_id,
            source_variable_code=rule.source_variable_code,
            classification=NOT_IN_INVENTORY, reason="UNKNOWN_BY_PACKAGE",
            unit=rule.unit, semantic_direction=rule.semantic_direction))

    if not administered:
        raise NativePreimageRefusal("NO_ADMINISTERED_MEASUREMENT_U")

    coordinate_cell = rows[1].get(package.coordinate_variable)
    coordinate_slot = CoordinateSlotRule(
        PhysicalSlot(coordinate_cell.variable_ordinal, package.coordinate_variable),
        _ref("COORDINATE_NATIVE",
             f"{source.source_id}-{package.coordinate_variable}"),
        _ref("UNIT_TAXONOMY", f"{source.source_id}-{package.coordinate_unit}"),
        package.coordinate_effective_time,
        coord_auth.authority_ref,
        copy_observed_raw=True,
    )
    risk_ref = _ref("RISK_SET", f"{source.source_id}-whole")
    routing = tuple(
        RoutingEligibilityFact(
            typed_state="ELIGIBLE_APPLICABLE",
            authority_snapshot_refs=(routing_auth.authority_ref,),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_ref(
                "REPLAY_ROOT", f"routing-{respondent.respondent_key}-{variable_name}"),
            empirical_universe_ref=universe.ref,
            scoped_respondent_ref=respondent.ref,
            question_or_target_ref=question_ref,
            risk_set_ref=risk_ref,
            routing_rule_ref=_ref("ROUTING_RULE", f"{source.source_id}-{variable_name}"),
            applicability_state="ELIGIBLE_APPLICABLE",
            routing_state="ELIGIBLE_APPLICABLE",
            parent_predicate_refs=(),
            member_set_replay_ref=_ref(
                "MEMBER_SET", f"{source.source_id}-{variable_name}-all"),
        )
        for respondent in respondents
        for variable_name, question_ref in routing_questions
    )

    def transformed_cells() -> Iterable[PhysicalCell]:
        for row_ordinal in sorted(rows):
            for variable_name in sorted(rows[row_ordinal]):
                cell = rows[row_ordinal][variable_name]
                if row_occurrence_plan is None or variable_name not in plan_by_variable:
                    yield cell
                    continue
                variable_plan = plan_by_variable[variable_name]
                occasion_token = occasion_token_by_row[row_ordinal]
                occurrence_binding = variable_plan.by_source_value[occasion_token]
                yield PhysicalCell(
                    row_ordinal=cell.row_ordinal,
                    variable_ordinal=cell.variable_ordinal,
                    variable_name=cell.variable_name,
                    raw_value=cell.raw_value,
                    missing_state=cell.missing_state,
                    source_missing_declaration=_governed_declaration(
                        cell, occurrence_binding),
                    raw_value_label=cell.raw_value_label,
                )

    stream = ExactPhysicalCellStream(
        source_sha256=source.declared_sha256,
        row_count=incidence.row_count,
        cell_iter_factory=lambda: tuple(transformed_cells()),
    )
    projection = GovernedC11Projection(
        projection_identity_ref=_ref(
            "C11_SEMANTIC_PROJECTION", f"{source.source_id}-{source.wave}"),
        source_artifact_id=source.canonical_filename,
        expected_source_sha256=source.declared_sha256,
        source_family_id=source.family,
        study_product_id=package.study_product_id,
        release_id=package.release_id,
        instrument_release_id=package.instrument_release_id,
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:rawlsing:r56:snapshot:{source.source_id}",
            source.declared_sha256),
        universes=(universe,),
        respondents=respondents,
        row_bindings=row_bindings,
        questions=tuple(question_bindings),
        response_slots=tuple(response_slots),
        coordinate_slots=(coordinate_slot,),
        routing=routing,
        weight_slots=(),
        authority_snapshots=authorities,
        source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(a.authority_ref for a in authorities),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=_ref("ORDER_RULE", f"{source.source_id}-canonical-ref-sort"),
        replay_protocol_version="1.0.0",
    )
    try:
        release = build_validated_source_backed_c11_release_from_stream(stream, projection)
    except (SourceBackedC11FacadeError, ValueError) as error:
        raise NativePreimageRefusal("C11_VALIDATION_REFUSED", str(error)) from error
    material = {
        "schema": SCHEMA,
        "source_sha256": source.declared_sha256,
        "package_hash": package.package_hash,
        "projection": projection.projection_identity_ref.as_dict(),
        "release": release.release_ref.as_dict(),
        "administered": [x.as_dict() for x in administered],
        "held": [x.as_dict() for x in held],
        "excluded": [x.as_dict() for x in excluded],
        "unknown": [x.as_dict() for x in unknown],
    }
    respondent_rows = tuple({
        "row": row, "respondent_key": respondent_token_by_row[row],
        "source_respondent": (
            token(rows[row][row_occurrence_plan.respondent_variable].raw_value)
            if row_occurrence_plan else f"ROW-{row:04d}"),
        "source_occasion": occasion_token_by_row.get(row),
        "projected_respondent_ref": respondent_by_key[respondent_token_by_row[row]].ref.as_dict(),
    } for row in sorted(rows))
    return NativePreimageBundle(
        schema=SCHEMA, source_sha256=source.declared_sha256,
        package_hash=package.package_hash, projection=projection,
        physical_stream=stream, release=release,
        administered=tuple(administered), held=tuple(held),
        excluded=tuple(excluded), unknown=tuple(unknown),
        bundle_hash=_hash(material), question_refs=dict(question_refs),
        risk_set_ref=risk_ref, respondent_rows=respondent_rows,
        occurrence_bindings=tuple(occurrence_evidence),
        source_format=source.source_format,
    )


__all__ = [
    "ADMINISTERED", "EXCLUDED", "HELD_NATIVE_ABSENT", "HELD_NOT_ADMINISTERED",
    "HELD_PACKAGE", "NOT_IN_INVENTORY", "OCCURRENCE_BINDING_SCHEMA", "SCHEMA",
    "AdministeredItem", "GovernedRowOccurrencePlan", "NativePreimageBundle",
    "NativePreimageRefusal", "NativeSourceIdentity", "NativeSourcePackage",
    "NativeSourceRule", "OccurrenceBinding", "VariableOccurrencePlan",
    "build_authority_set", "materialize_native_preimages", "token",
]
