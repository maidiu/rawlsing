"""Sourcefree legacy transport, not an actor/world writer or source qualification.

Only explicitly referenced material observations become migration candidates.
No candidate here is a canonical fact, actor memory, issued rule or native grant.
"""
from dataclasses import dataclass
import hashlib
import json
from actor_reader import ReaderHeld, canon


@dataclass(frozen=True)
class LegacyFactBindingV1:
    path: tuple[str | int, ...]
    source_ref: str
    grade: str = "SOURCEFREE_TEST_ONLY"


@dataclass(frozen=True)
class LegacyActorSourceV1:
    actor_id: str
    source_cut: str
    source_json: str
    source_sha256: str
    bindings: tuple[LegacyFactBindingV1, ...]


@dataclass(frozen=True)
class LegacyFactCandidateV1:
    legacy_path: tuple[str | int, ...]
    value_json: str
    source_ref: str
    source_sha256: str


@dataclass(frozen=True)
class QuarantineRefV1:
    field: str
    category: str
    source_sha256: str


@dataclass(frozen=True)
class UnknownRefV1:
    legacy_path: tuple[str | int, ...]
    reason: str


@dataclass(frozen=True)
class MigrationRecordV1:
    actor_id: str
    source_cut: str
    source_sha256: str
    retained_candidates: tuple[LegacyFactCandidateV1, ...]
    unknowns: tuple[UnknownRefV1, ...]
    quarantine: tuple[QuarantineRefV1, ...]
    status: str = "PARTIAL_HELD_SOURCE_OWNER_ADMISSION"
    grade: str = "SOURCEFREE_MIGRATION_CANDIDATE_NOT_CANONICAL_ACTOR"


# These exact legacy names come from pinned M01 BackboneState, not invented
# psycho-causal fields. World descriptors cannot be copied into actor authority.
WORLD_FIELDS = frozenset({"field", "calibration_regime", "boundary_map", "strata_salience",
    "strata_stack", "collective_infrastructure", "v5_runtime_input_bundle", "v5_runtime_input_refs", "v5_bridge_status"})
NARRATOR_FIELDS = frozenset({"rendered_output", "narration_support"})
ANALYST_FIELDS = frozenset({"pressure_flow_history", "pressure_flow_memory", "surface_psyche_profile",
    "analyst_pressure_account", "micro_trace_this_year", "generation_diagnostics", "yearly_integrity"})
PLACEHOLDER_FIELDS = frozenset({"cracks", "frameworks", "frameworks_dormant"})
NONCAUSAL_FIELDS = frozenset({"age", "child_model"})
OBSERVABLE_FIELDS = frozenset({"year", "events_this_year", "capacity", "reproduction_constraints"})
MATERIAL_CAPACITY_FIELDS = frozenset({"time", "money", "health", "mobility"})


def category(field: str) -> str:
    if field in WORLD_FIELDS:
        return "WORLD_OWNER_ADMISSION_HELD"
    if field in NARRATOR_FIELDS:
        return "NARRATOR_PROSE_ARCHIVE_ONLY"
    if field in ANALYST_FIELDS:
        return "ANALYST_TRACE_NOT_ACTOR_MEMORY"
    if field in PLACEHOLDER_FIELDS:
        return "PLACEHOLDER_ARCHIVE_ONLY"
    if field in NONCAUSAL_FIELDS:
        return "AGE_TYPE_ASSUMPTION_NONCAUSAL"
    if field == "expectation_baseline":
        return "EXPECTATION_DEFAULT_RULE_HELD"
    if field == "metabolic_style" or field == "registers":
        return "DERIVED_CACHE_NOT_CAUSAL_INPUT"
    if field in OBSERVABLE_FIELDS:
        return "UNBOUND_OBSERVATION_NOT_ADMITTED"
    return "LEGACY_SEMANTIC_RULE_HELD"


def migrate_legacy_actor(source: LegacyActorSourceV1) -> MigrationRecordV1:
    """Pure/idempotent transport of explicit bindings; never instantiates BackboneState."""
    actual_hash = hashlib.sha256(source.source_json.encode()).hexdigest()
    if actual_hash != source.source_sha256:
        raise ReaderHeld("LEGACY_SOURCE_HASH_MISMATCH")
    data = json.loads(source.source_json)
    if not isinstance(data, dict) or not source.actor_id or not source.source_cut:
        raise ReaderHeld("LEGACY_SOURCE_SHAPE_HELD")
    retained, unknowns, seen = [], [], set()
    for binding in source.bindings:
        if (not binding.path or not binding.source_ref or binding.grade != "SOURCEFREE_TEST_ONLY"
            or any(type(part) not in (str, int) for part in binding.path)):
            raise ReaderHeld("LEGACY_BINDING_SCOPE_HELD")
        if binding.path in seen:
            raise ReaderHeld("DUPLICATE_LEGACY_BINDING")
        seen.add(binding.path)
        root = binding.path[0]
        if root not in OBSERVABLE_FIELDS or (root == "capacity" and
            (len(binding.path) < 2 or binding.path[1] not in MATERIAL_CAPACITY_FIELDS)):
            unknowns.append(UnknownRefV1(binding.path, "FIELD_NOT_ADMITTED_TO_MATERIAL_CANDIDATE"))
            continue
        value = data
        try:
            for part in binding.path:
                if type(value) is dict and type(part) is str:
                    value = value[part]
                elif type(value) is list and type(part) is int and part >= 0:
                    value = value[part]
                else:
                    raise KeyError(part)
        except (KeyError, IndexError):
            unknowns.append(UnknownRefV1(binding.path, "MISSING_SOURCE_VALUE"))
            continue
        # A container is not proof for every nested scalar/default/other actor.
        if isinstance(value, (dict, list)):
            unknowns.append(UnknownRefV1(binding.path, "EXACT_SCALAR_BINDING_REQUIRED"))
            continue
        retained.append(LegacyFactCandidateV1(binding.path, canon(value), binding.source_ref, actual_hash))
    quarantine = tuple(QuarantineRefV1(field, category(field), actual_hash) for field in sorted(data))
    return MigrationRecordV1(source.actor_id, source.source_cut, actual_hash,
        tuple(retained), tuple(unknowns), quarantine)
