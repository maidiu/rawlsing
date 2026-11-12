"""S2-B sourcefree DIRECT I02 section-stream producer — independent of v1 release.

This is a substantive bounded-construction bridge, not a scientific/source
issuer. It receives actual typed S1-B/E-compatible C11 section iterables and
SourceReleaseManifest. It does NOT call validate_c11_source_release(), build
ReplayManifest.closure_refs, create C11LogicalRelease, mint _C11_VALIDATION_SEAL
or materialize the public/internal object graph. All public and internal
semantic object refs, source/authority identities, typed absence declarations,
respondent joins, native/canonical/component aliases and occurrence identities
are checked as rows are consumed into SQLite.

M16/M17/M18 use an explicitly DIFFERENT external direct replay descriptor,
not the historical ReplayManifest. That remaining semantic equivalence, a
competent external expected-root issuer, and S2-C physical native first-reader
are NOT proven/issued by this bridge. It is deliberately marked DIRECT_SCHEMA
so a verified direct certificate cannot be substituted for a v1 sealed release.

Native sourcefree I03 comparison remains a separate real-consumer test, not a
claim that the direct physical product is installed as an old C11 release.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections.abc import Iterable, Mapping
from types import MappingProxyType
import os
import sqlite3
import tempfile

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry, require_positive_authority, validate_authority_snapshot,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, AuthoritySnapshot, CanonicalSemanticObject,
    EmpiricalCoordinateFact, EmpiricalUniverse, ExactRef,
    RespondentEvent, RoutingEligibilityFact, SourceUniverseRelation,
    WeightMeasureFact, canonical_json, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_c11_integrity import (
    C11InternalRecord, RespondentIdentity, QuestionVariableBinding,
    EmpiricalPredicateReplayBinding, ComparatorReplayBinding,
    DiscoveryBranchReplayBinding, StructuralAdmissionReplayBinding,
    TypedAbsence, M01_M18, assert_internal_carrier_record,
    authority_snapshot_set_hash, validate_public_carrier_object,
)
from rawlsing_next.pre553_c11_ingest import (
    SourceReleaseManifest, C11SourceReleaseCandidate,
    INGEST_CONTRACT_VERSION, _walk_authority_refs,
)
from rawlsing_next._pre553_external_i02_certificate import (
    DIRECT_SCHEMA, ExternalI02IntegrityError, ExternalI02Roots,
    _schema, _insert_object, _check_relations, _logical_root,
    _digest_file, _fail,
)

_FAMILIES = MappingProxyType({
    "EmpiricalUniverse": EmpiricalUniverse,
    "RespondentIdentity": RespondentIdentity,
    "QuestionVariableBinding": QuestionVariableBinding,
    "RespondentEvent": RespondentEvent,
    "RoutingEligibilityFact": RoutingEligibilityFact,
    "EmpiricalCoordinateFact": EmpiricalCoordinateFact,
    "WeightMeasureFact": WeightMeasureFact,
    "AuthoritySnapshot": AuthoritySnapshot,
    "SourceUniverseRelation": SourceUniverseRelation,
    "EmpiricalPredicateReplayBinding": EmpiricalPredicateReplayBinding,
    "ComparatorReplayBinding": ComparatorReplayBinding,
    "DiscoveryBranchReplayBinding": DiscoveryBranchReplayBinding,
    "StructuralAdmissionReplayBinding": StructuralAdmissionReplayBinding,
})
_OPTIONAL_ABSENCE = MappingProxyType({
    "WeightMeasureFact": frozenset({"NOT_APPLICABLE", "MISSING", "NOT_AUTHORIZED", "UNKNOWN"}),
    "SourceUniverseRelation": frozenset({"DISTINCT_BY_DEFAULT"}),
    "EmpiricalPredicateReplayBinding": frozenset({"NOT_APPLICABLE", "DEFERRED"}),
    "ComparatorReplayBinding": frozenset({"DEFERRED"}),
    "DiscoveryBranchReplayBinding": frozenset({"DEFERRED"}),
    "StructuralAdmissionReplayBinding": frozenset({"NOT_APPLICABLE"}),
})
_CORE = frozenset({
    "EmpiricalUniverse", "RespondentIdentity", "QuestionVariableBinding",
    "RespondentEvent", "RoutingEligibilityFact", "EmpiricalCoordinateFact",
    "AuthoritySnapshot",
})
_CANDIDATE_FIELDS = MappingProxyType({
    "EmpiricalUniverse": "empirical_universes",
    "RespondentIdentity": "respondent_identities",
    "QuestionVariableBinding": "question_variable_bindings",
    "RespondentEvent": "respondent_events",
    "RoutingEligibilityFact": "routing_eligibility_facts_or_exact_rules",
    "EmpiricalCoordinateFact": "empirical_coordinate_facts",
    "WeightMeasureFact": "weight_measure_facts_or_typed_absence",
    "AuthoritySnapshot": "authority_snapshots",
    "SourceUniverseRelation": "source_universe_relations_or_explicit_distinct_default",
    "EmpiricalPredicateReplayBinding": "predicate_replay_bindings_when_retained_objects_require_them",
    "ComparatorReplayBinding": "comparator_replay_bindings_or_typed_deferred_state",
    "DiscoveryBranchReplayBinding": "discovery_branch_replay_bindings_or_typed_deferred_state",
    "StructuralAdmissionReplayBinding": "structural_admission_replay_bindings_or_typed_not_applicable_state",
})


@dataclass(frozen=True)
class SourcefreeDirectI02Sections:
    """Each sections[family] may be a one-shot, bounded sourcefree iterator.

    Producer credentials / original35 access are NOT obtained from this type.
    The declared census and source manifest are inputs, not self-issued proof;
    callers must hold an independently qualified expected logical + physical
    root before treating a cold certificate as externally authenticated.
    """
    manifest: SourceReleaseManifest
    sections: Mapping[str, Iterable[object]]
    typed_absences: Mapping[str, TypedAbsence]
    replay_protocol_authority_ref: AuthorityRef
    replay_protocol_version: str
    deterministic_tie_order_rules_ref: ExactRef


def direct_sections_from_candidate(
    candidate: C11SourceReleaseCandidate, *,
    replay_protocol_authority_ref: AuthorityRef,
    replay_protocol_version: str,
    deterministic_tie_order_rules_ref: ExactRef,
) -> SourcefreeDirectI02Sections:
    """Original typed sourcefree candidate adapter, NOT legacy I02 validation.

    Does not access candidate.candidate_replay_manifest at all: it may be None.
    The sections remain iterable inputs; no new all-object/closure tuple made.
    For genuinely bounded end-to-end input, callers should supply one-shot
    decoders to SourcefreeDirectI02Sections directly, not legacy candidate
    tuples. The fixture adapter proves semantic interfacing, not full pipeline
    input economy.
    """
    if type(candidate) is not C11SourceReleaseCandidate:
        _fail("exact sourcefree C11 candidate required")
    sections = {}
    absences = {}
    for family, field in _CANDIDATE_FIELDS.items():
        section = getattr(candidate, field)
        if isinstance(section, TypedAbsence):
            absences[family] = section
            sections[family] = iter(())
        else:
            sections[family] = iter(section)
    return SourcefreeDirectI02Sections(
        candidate.source_release_manifest, MappingProxyType(sections),
        MappingProxyType(absences), replay_protocol_authority_ref,
        replay_protocol_version, deterministic_tie_order_rules_ref,
    )


def _coverage(counts: Mapping[str, int]) -> dict[str, list[str]]:
    """Truthful atom labels: do NOT relabel direct replay as legacy M16 seal."""
    coverage = {
        "M01": ["EmpiricalUniverse"],
        "M02": ["RespondentIdentity"],
        "M03": ["QuestionVariableBinding"],
        "M04": ["RespondentEvent"],
        "M05": ["QuestionVariableBinding", "RespondentEvent"],
        "M06": ["RespondentEvent.typed_state"],
        "M07": ["RoutingEligibilityFact"],
        "M08": ["EmpiricalCoordinateFact"],
        "M09": ["WeightMeasureFact|TypedAbsence"],
        "M10": ["AuthoritySnapshot"],
        "M11": ["SourceUniverseRelation|DISTINCT_BY_DEFAULT"],
        "M12": ["RoutingEligibilityFact", "EmpiricalPredicateReplayBinding|TypedAbsence"],
        "M13": ["ComparatorReplayBinding|DEFERRED"],
        "M14": ["DiscoveryBranchReplayBinding|DEFERRED"],
        "M15": ["StructuralAdmissionReplayBinding|NOT_APPLICABLE"],
        "M16": ["DIRECT_SOURCEFREE_REPLAY_DESCRIPTOR_NOT_LEGACY_REPLAY_MANIFEST"],
        "M17": ["AuthoritySnapshot", "DIRECT_SOURCEFREE_REPLAY_DESCRIPTOR_NOT_LEGACY"],
        "M18": ["DIRECT_SOURCEFREE_REPLAY_DESCRIPTOR_NOT_LEGACY"],
    }
    if (set(coverage) != set(M01_M18)
            or any(counts.get(f, 0) == 0 for f in _CORE)):
        _fail("sourcefree direct I02 has missing applicable M01-M18 family")
    return coverage


def _check_direct_relations(db: sqlite3.Connection, *, declared_universes: set[str]) -> None:
    # Global source/ref/alias/selector closure is inherited from the same
    # physically protected and externally rooted v1-derived verifier.
    if db.execute("""
        SELECT 1 FROM main.objects o
        WHERE o.family='RespondentIdentity' AND o.universe
              NOT IN (SELECT ref FROM main.objects WHERE family='EmpiricalUniverse')
        LIMIT 1
    """).fetchone():
        _fail("direct sourcefree respondent outside declared universe")
    if db.execute("""
        SELECT 1 FROM main.objects e LEFT JOIN main.scoped_names s
            ON e.respondent=s.ref AND e.universe=s.universe
        WHERE e.family IN ('RespondentEvent','RoutingEligibilityFact',
                           'EmpiricalCoordinateFact','WeightMeasureFact')
          AND s.ref IS NULL LIMIT 1
    """).fetchone():
        _fail("direct sourcefree event/coordinate/weight/routing has wrong respondent")
    if db.execute("""
        SELECT 1 FROM main.objects q
        WHERE q.family='QuestionVariableBinding' AND
          q.universe NOT IN (SELECT ref FROM main.objects WHERE family='EmpiricalUniverse')
        LIMIT 1
    """).fetchone():
        _fail("direct sourcefree binding references wrong universe")
    for (actual,) in db.execute("""
        SELECT ref FROM main.objects WHERE family='EmpiricalUniverse' ORDER BY ref
    """):
        if actual not in declared_universes:
            _fail("undeclared sourcefree direct universe")


def build_sourcefree_direct_i02(
    source: SourcefreeDirectI02Sections,
    universe_ref: ExactRef,
    destination: str | Path,
    *,
    chunk_size: int = 512,
) -> ExternalI02Roots:
    """Build a DIRECT scoped certificate without a legacy I02 release/closure.

    SQLite is the sort, identity, occurrence and authority-join store; no
    all-object or all-ref Python list. The small authority snapshot census is
    retained for existing competent public validators; its size is separately
    bounded by manifest source declarations, not the corpus size.

    This is sourcefree G1–G4 *construction capital*, not original35 source
    equivalence, legacy replay M16–M18 parity, or native S2-C release issuance.
    """
    if type(source) is not SourcefreeDirectI02Sections:
        _fail("exact sourcefree direct section input required")
    manifest = source.manifest
    if (type(manifest) is not SourceReleaseManifest
            or manifest.ingest_contract_version != INGEST_CONTRACT_VERSION):
        _fail("sourcefree direct manifest is not original exact C11 source contract")
    if type(universe_ref) is not ExactRef:
        _fail("exact sourcefree direct universe required")
    if not 1 <= chunk_size <= 16384:
        raise ValueError("chunk_size must be 1..16384")
    if set(source.sections) != set(_FAMILIES):
        _fail("all original C11 family streams required; unknown/missing family")
    if not set(source.typed_absences).issubset(_OPTIONAL_ABSENCE):
        _fail("unrecognized/mandatory C11 family cannot carry typed absence")
    for family, absent in source.typed_absences.items():
        if type(absent) is not TypedAbsence or absent.state not in _OPTIONAL_ABSENCE[family]:
            _fail("sourcefree direct typed negative state not lawful")
    if not isinstance(source.replay_protocol_authority_ref, AuthorityRef):
        _fail("direct sourcefree replay protocol authority required")
    if not isinstance(source.deterministic_tie_order_rules_ref, ExactRef):
        _fail("direct sourcefree deterministic replay tie-order ref required")
    if not isinstance(source.replay_protocol_version, str) or not source.replay_protocol_version:
        _fail("direct sourcefree replay protocol version required")
    declared = manifest.declared_record_counts_by_logical_family
    if set(declared) - (set(_FAMILIES) | {"ReplayManifest"}):
        _fail("undeclared extra sourcefree direct record family")
    if set(declared) < _CORE or declared.get("ReplayManifest") != 1:
        _fail("sourcefree direct source manifest missing mandatory original counts")
    declared_universes = {ref.key for ref in manifest.declared_universe_refs}
    if universe_ref.key not in declared_universes:
        _fail("selected universe not in original source manifest")
    target = Path(destination).absolute()
    if target.suffix != ".sqlite" or target.exists() or target.is_symlink():
        _fail("direct sourcefree destination must be new SQLite artifact")
    if not target.parent.is_dir() or target.parent.is_symlink():
        _fail("trusted direct sourcefree staging directory required")

    # Registry is a small authority census, not a full object/ref corpus.
    snapshots = tuple(source.sections["AuthoritySnapshot"])
    if len(snapshots) != declared.get("AuthoritySnapshot", -1):
        _fail("sourcefree direct authority census does not match source manifest")
    if any(type(a) is not AuthoritySnapshot for a in snapshots):
        _fail("sourcefree direct authority snapshot type mismatch")
    for snap in snapshots:
        validate_authority_snapshot(snap)
    if ({a.authority_ref.key for a in snapshots} !=
            {a.key for a in manifest.declared_authority_snapshot_refs} or
            len(set(a.authority_ref.key for a in snapshots)) != len(snapshots)):
        _fail("sourcefree direct authority exact snapshot census differs")
    registry = AuthorityRegistry(snapshots)
    require_positive_authority(
        registry.resolve_exact(source.replay_protocol_authority_ref).snapshot,
        authority_kind="REPLAY_PROTOCOL",
    )

    fd, staged = tempfile.mkstemp(prefix=".s2b-direct-stage-", suffix=".tmp", dir=target.parent)
    os.close(fd)
    db = None
    try:
        db = sqlite3.connect(staged)
        db.execute("PRAGMA journal_mode=DELETE")
        db.execute("PRAGMA synchronous=FULL")
        db.execute("PRAGMA temp_store=FILE")
        db.execute("PRAGMA cache_size=-2048")
        _schema(db)
        db.executescript("""
          CREATE TABLE scoped_names(
            universe TEXT NOT NULL, respondent_key TEXT NOT NULL,
            ref TEXT NOT NULL UNIQUE, PRIMARY KEY(universe,respondent_key)
          );
          CREATE TABLE event_occurrences(
            identity TEXT PRIMARY KEY, event_ref TEXT NOT NULL UNIQUE
          );
        """)
        # One-shot generators are consumed exactly once. Source declaration
        # counts and external expected roots, not self-rehashed refs, are
        # necessary to authenticate completeness.
        seen = {}
        total = 0
        for family, record_type in _FAMILIES.items():
            count = 0
            iterable = snapshots if family == "AuthoritySnapshot" else source.sections[family]
            for obj in iterable:
                if type(obj) is not record_type:
                    _fail("sourcefree direct section contains wrong exact record family")
                if isinstance(obj, CanonicalSemanticObject):
                    validate_public_carrier_object(obj, registry)
                    for ref in _walk_authority_refs(obj.semantic_fields):
                        registry.resolve_exact(ref)
                elif isinstance(obj, C11InternalRecord):
                    assert_internal_carrier_record(obj)
                    for ref in _walk_authority_refs(obj.semantic_projection()):
                        registry.resolve_exact(ref)
                else:
                    _fail("sourcefree direct received non-C11 carrier object")
                if isinstance(obj, QuestionVariableBinding):
                    registry.resolve_exact(obj.semantic_authority_ref)
                    registry.resolve_exact(obj.topology_authority_ref)
                    if isinstance(obj.canonical_question_ref_or_typed_absence, ExactRef):
                        require_positive_authority(
                            registry.resolve_exact(obj.semantic_authority_ref).snapshot,
                            authority_kind="NATIVE_CANONICAL_MAPPING_HARMONIZATION",
                        )
                if isinstance(obj, RespondentIdentity):
                    if isinstance(obj.identity_map_authority_ref_or_typed_absence, AuthorityRef):
                        registry.resolve_exact(obj.identity_map_authority_ref_or_typed_absence)
                    if db.execute("""
                        SELECT 1 FROM main.scoped_names
                        WHERE universe=? AND respondent_key=? LIMIT 1
                    """, (obj.empirical_universe_ref.key, obj.respondent_key)).fetchone():
                        _fail("duplicate sourcefree respondent identity within universe")
                    db.execute("INSERT INTO main.scoped_names VALUES (?,?,?)", (
                        obj.empirical_universe_ref.key, obj.respondent_key, obj.ref.key,
                    ))
                if isinstance(obj, RespondentEvent):
                    identity = canonical_json({
                        "universe": exact_ref(obj.empirical_universe_ref).as_dict(),
                        "respondent": exact_ref(obj.scoped_respondent_ref).as_dict(),
                        "native_question": exact_ref(obj.native_question_ref).as_dict(),
                        "component": obj.component_or_subitem_ref,
                        "event_group_id": obj.event_group_id,
                        "event_id": obj.response_event_id_or_deterministic_index,
                    })
                    if db.execute("""
                        SELECT 1 FROM main.event_occurrences
                        WHERE identity=? OR event_ref=? LIMIT 1
                    """, (identity, obj.ref.key)).fetchone():
                        _fail("duplicate sourcefree event occurrence identity")
                    db.execute("INSERT INTO main.event_occurrences VALUES (?,?)",
                               (identity, obj.ref.key))
                if isinstance(obj, SourceUniverseRelation):
                    for ref in obj.source_universe_refs:
                        if exact_ref(ref).key not in declared_universes:
                            _fail("direct source relation contains undeclared universe")
                if db.execute(
                    "SELECT 1 FROM main.objects WHERE ref=? LIMIT 1", (obj.ref.key,)
                ).fetchone():
                    _fail("duplicate exact sourcefree corpus object reference")
                _insert_object(db, obj, family=family)
                db.execute("INSERT INTO main.closure VALUES(?)", (obj.ref.key,))
                count += 1
                total += 1
                if total % chunk_size == 0:
                    db.commit()
            if family in source.typed_absences and count != 0:
                _fail("direct typed-absent family also contains physical records")
            if family in declared and declared[family] != count:
                _fail("sourcefree direct record omission/census mismatch: " + family)
            if family in _CORE and (family not in declared or not count):
                _fail("sourcefree direct required family empty or undeclared: " + family)
            seen[family] = count

        if (set(db.execute(
            "SELECT ref FROM main.objects WHERE family='EmpiricalUniverse'"
        )) != {(ref.key,) for ref in manifest.declared_universe_refs}):
            _fail("sourcefree direct exact universe census differs from manifest")
        # Both exceptional legacy source closure inputs are carried as source
        # *identities*, not as an internally materialized ReplayManifest tuple.
        for ref in (manifest.source_artifact_ref, manifest.source_snapshot_retention_ref):
            db.execute("INSERT INTO main.closure VALUES (?)", (ref.key,))
        _check_direct_relations(db, declared_universes=declared_universes)
        _check_relations(db, source=manifest.source_artifact_ref.key)
        coverage = _coverage(seen)
        replay_descriptor = {
            "schema": DIRECT_SCHEMA,
            "source_manifest": manifest.semantic_projection(),
            "replay_protocol_authority_ref": source.replay_protocol_authority_ref.as_dict(),
            "replay_protocol_version": source.replay_protocol_version,
            "tie_order_rules_ref": source.deterministic_tie_order_rules_ref.as_dict(),
            "authority_snapshot_set_hash": authority_snapshot_set_hash(snapshots),
            "explicit_absences": {
                f: source.typed_absences[f].as_dict()
                for f in sorted(source.typed_absences)
            },
            "historical_replay_manifest": "NOT_CONSTRUCTED_NOT_CLAIMED",
        }
        direct_release = ExactRef(
            "C11_DIRECT_SOURCEFREE_RELEASE", manifest.release_id,
            semantic_hash({"schema": DIRECT_SCHEMA,
                           "manifest": manifest.semantic_projection()}),
        )
        replay_ref = ExactRef(
            "C11_DIRECT_SOURCEFREE_REPLAY", manifest.release_id,
            semantic_hash(replay_descriptor),
        )
        headers = {
            "schema": DIRECT_SCHEMA,
            "release": direct_release.key,
            "source": manifest.source_artifact_ref.key,
            "replay": replay_ref.key,
            "universe": universe_ref.key,
            "coverage": canonical_json(coverage),
            "declared_counts": canonical_json(dict(declared)),
            "actual_counts": canonical_json(seen),
            "source_manifest_hash": manifest.content_hash,
            "replay_descriptor": canonical_json(replay_descriptor),
            "chunk_size_is_nonsemantic": "true",
            "legacy_replay_m16_m18_equivalence": "NOT_PROVEN",
            "original_source_current_issuer": "NOT_ISSUED",
        }
        for key, value in headers.items():
            db.execute("INSERT INTO main.header VALUES(?,?)", (key, value))
        db.commit()
        root = _logical_root(db, schema=DIRECT_SCHEMA)
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            _fail("sourcefree direct external I02 SQLite integrity failure")
        db.close()
        db = None
        with open(staged, "rb") as src:
            os.fsync(src.fileno())
        try:
            os.link(staged, target, follow_symlinks=False)
        except FileExistsError as exc:
            raise ExternalI02IntegrityError(
                "direct sourcefree publication collision"
            ) from exc
        os.unlink(staged)
        dirfd = os.open(target.parent, os.O_RDONLY)
        try:
            os.fsync(dirfd)
        finally:
            os.close(dirfd)
        return ExternalI02Roots(
            root, _digest_file(target), direct_release.key,
            manifest.source_artifact_ref.key, replay_ref.key,
            universe_ref.key, DIRECT_SCHEMA,
        )
    finally:
        if db is not None:
            db.close()
        if os.path.exists(staged):
            os.unlink(staged)


__all__ = [
    "SourcefreeDirectI02Sections",
    "direct_sections_from_candidate",
    "build_sourcefree_direct_i02",
]
