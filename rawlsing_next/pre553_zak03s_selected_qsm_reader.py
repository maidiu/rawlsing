"""ZAK-03S: opt-in sourcefree historical QSM selection at the real Route-B reader.

A QSM question-relation disposition is *not* a PREDICATE_GRAMMAR or
TARGET_USE_PERMISSION.  This adapter requires both a selected, byte-exact
historical QSM coverage row and an independently positive *current* target-use
snapshot already declared in each requested I03 query.  It does not issue either
authority, alter C11, or claim production/native adoption.

The real source-backed C11 / I03 / I05 executor is invoked exactly once after
the fail-closed checks.  I05 executes but is not declared QSM-qualified by this
adapter: its own discovery grammar has independent authority and consumers.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

from data.ddm_build_copy.ddm_v550_question_relation_authority import (
    active_authority_path,
    canonical_country_code,
    canonical_source_family,
    canonical_wave,
    load_question_relation_authority,
    resolve_question_relation_authority,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_route_b_production import (
    I03ExecutionRequest,
    RouteBProductionResult,
    execute_route_b_production,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    GovernedC11Projection,
    SourceBackedC11SessionCache,
)
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence


CONTRACT = "ZAK03S_QSM_SELECTED_TO_ROUTE_B_I03@1.0.0"
POSITIVE_QSM_DISPOSITIONS = frozenset({
    "GOVERNED_QSMV2_RELATION_AUTHORITY",
    "GOVERNED_MANUAL_RELATION_AUTHORITY",
    "FROZEN_ACCEPTED_GSS",
    "GOVERNED_NON_DIRECTIONAL_DISPOSITION",
    "GOVERNED_NEUTRAL_COVERAGE",
    "GOVERNED_CONTEXT_ONLY",
    "GOVERNED_NON_RELATIONAL",
    "ACTIVE",
})

COVERAGE_ONLY_STATUSES = frozenset({
    "RESOLVED_DIRECTIONAL_AUTHORITY",
    "RESOLVED_NEUTRAL_COVERAGE_AUTHORITY",
    "RESOLVED_CONTEXT_ONLY_AUTHORITY",
    "RESOLVED_NON_RELATIONAL_AUTHORITY",
})


class SelectedQsmRouteError(Pre553IntegrityError):
    """The selected historical source-to-request dependency is not established."""


@dataclass(frozen=True)
class SelectedQsmRequest:
    # The exact path is selected *by the caller*, not by an environment default.
    authority_path: str | Path
    expected_file_sha256: str
    expected_row_hash: str
    expected_authority_version: str
    expected_rule_id: str
    source_family: str
    canonical_wave: str
    country_code: str
    var_code: str
    native_question_ref: ExactRef
    target_use_ref: ExactRef
    target_use_authority_ref: AuthorityRef
    target_use_operation: str


@dataclass(frozen=True)
class SelectedQsmRouteResult:
    """Separate selector receipt; cannot be misrepresented as a native C11 fact."""
    route: RouteBProductionResult
    binding_receipt: Mapping[str, Any]


def _must(condition: bool, reason: str) -> None:
    if not condition:
        raise SelectedQsmRouteError(reason)


def _file_sha(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _exact_selection(selection: SelectedQsmRequest, projection: GovernedC11Projection):
    _must(isinstance(selection, SelectedQsmRequest), "exact selected QSM request required")
    _must(isinstance(projection, GovernedC11Projection), "exact governed projection required")
    _must(
        isinstance(selection.authority_path, (str, Path))
        and bool(str(selection.authority_path).strip()),
        "explicit selected QSM path is required; environment fallback forbidden",
    )
    path = active_authority_path(selection.authority_path)
    _must(path.is_file(), "selected QSM file unavailable")
    _must(_file_sha(path) == selection.expected_file_sha256, "selected QSM file SHA mismatch")
    index = load_question_relation_authority(path)
    _must(index.file_sha256 == selection.expected_file_sha256,
          "QSM cached/index file identity differs from exact selection")
    result = resolve_question_relation_authority(
        source_family=selection.source_family,
        canonical_wave_value=selection.canonical_wave,
        country_code=selection.country_code,
        var_code=selection.var_code,
        authority_path=path,
    )
    _must(result.resolved and result.match_count == 1,
          "exact selected historical QSM row unavailable or ambiguous")
    _must(result.authority_artifact_sha256 == selection.expected_file_sha256,
          "resolver selected a different QSM source file")
    row = result.authority_row
    _must(row is not None, "missing selected QSM row")
    _must(row.get("row_payload_hash") == selection.expected_row_hash,
          "selected QSM row hash changed")
    _must(row.get("authority_version") == selection.expected_authority_version,
          "selected QSM rule version changed")
    _must(row.get("authority_rule_id") == selection.expected_rule_id,
          "selected QSM rule identity changed")
    _must(result.status in COVERAGE_ONLY_STATUSES,
          "selected QSM row does not allow question-coverage lineage")
    _must(row.get("authority_status", "").upper() in POSITIVE_QSM_DISPOSITIONS,
          "historical QSM authority disposition is not positive")
    _must(
        canonical_source_family(row.get("source_family")) ==
        canonical_source_family(selection.source_family)
        and canonical_wave(selection.source_family, row.get("canonical_wave")) ==
        canonical_wave(selection.source_family, selection.canonical_wave)
        and canonical_country_code(row.get("country_code_scope")) ==
        canonical_country_code(selection.country_code),
        "historical QSM source/wave/country scope mismatch",
    )
    # A request ref supplied by a caller cannot invent an actual projection
    # question: it must resolve to an exact response-slot QVB and universe.
    _must(len(projection.universes) == 1,
          "multi-universe QSM lineage requires separately issued mapping")
    universe = projection.universes[0]
    _must(
        canonical_source_family(universe.source_family) ==
        canonical_source_family(selection.source_family)
        and canonical_wave(universe.source_family, universe.raw_wave) ==
        canonical_wave(selection.source_family, selection.canonical_wave)
        and canonical_country_code(universe.country_geography) ==
        canonical_country_code(selection.country_code),
        "selected QSM source identity is not the governed C11 universe",
    )
    matched = [
        slot for slot in projection.response_slots
        if slot.question_binding.native_question_ref == selection.native_question_ref
        and slot.question_binding.empirical_universe_ref == universe.ref
        # Same native physical variable code, never a guessed alias or a
        # question-label-to-variable-name inference. Different naming requires
        # a separately issued source mapping, which this adapter cannot grant.
        and slot.slot.name.casefold() == row.get("var_code", "").casefold()
    ]
    _must(len(matched) == 1,
          "historical question lacks unique same-code native C11 response-slot binding")
    return path, result, universe


def execute_selected_qsm_route_b(
    *,
    selection: SelectedQsmRequest,
    source: PhysicalSourceIncidence | ExactPhysicalCellStream,
    projection: GovernedC11Projection,
    runtime_catalog: RuntimeObjectCatalog,
    i03_requests: tuple[I03ExecutionRequest, ...],
    discovery_authority_ref: ExactRef,
    cache: SourceBackedC11SessionCache | None = None,
    batch_size: int = 10_000,
) -> SelectedQsmRouteResult:
    """Execute a *selected* question-coverage dependency at the actual reader.

    All requested I03 queries must target the selected QVB and declare the
    separate current target-use permission.  Missing declarations fail closed;
    no new query, snapshot, authority or scientific interpretation is minted.
    """
    path, resolution, universe = _exact_selection(selection, projection)
    _must(isinstance(runtime_catalog, RuntimeObjectCatalog),
          "actual RuntimeObjectCatalog required")
    _must(bool(i03_requests), "at least one actually consumed I03 request required")
    registry = AuthorityRegistry(runtime_catalog.authorities)
    registry.require(
        selection.target_use_authority_ref,
        authority_kind="TARGET_USE_PERMISSION",
        operation=selection.target_use_operation,
        object_family="EmpiricalFact@1.0.0",
        source_universe_ref=universe.ref.as_dict(),
        target_use_ref=selection.target_use_ref.as_dict(),
    )
    for request in i03_requests:
        _must(isinstance(request, I03ExecutionRequest), "exact I03 execution request required")
        query = runtime_catalog.resolve_query_exact(request.query_ref)
        _must(
            universe.ref in tuple(exact_ref(ref, "query empirical universe") for ref in query.empirical_universe_refs),
            "selected QSM universe absent from actual I03 query",
        )
        _must(
            selection.native_question_ref in tuple(exact_ref(ref, "query target") for ref in query.target_refs),
            "selected historical question not an I03 query target",
        )
        grain = query.requested_output_grain
        _must(
            grain.get("target_use_ref") == selection.target_use_ref.as_dict()
            and grain.get("target_use_authority_ref") ==
                selection.target_use_authority_ref.as_dict()
            and grain.get("target_use_operation") == selection.target_use_operation,
            "actual I03 reader lacks selected target-use permission triple",
        )
        _must(selection.target_use_ref in query.dependency_refs,
              "actual query dependency closure lacks target-use identity")
        _must(selection.target_use_authority_ref in query.authority_snapshot_refs,
              "actual query authority closure lacks target-use authorization")

    # First reader is the existing real producer, not a test-only query imitation.
    route = execute_route_b_production(
        source=source,
        projection=projection,
        runtime_catalog=runtime_catalog,
        i03_requests=i03_requests,
        discovery_authority_ref=discovery_authority_ref,
        cache=cache,
        batch_size=batch_size,
    )
    _must(len(route.i03_results) == len(i03_requests),
          "real reader failed to return every selected I03 request")
    _must(all(result.facts for result in route.i03_results),
          "real reader produced no checkable I03 result")
    _must(_file_sha(path) == selection.expected_file_sha256,
          "selected QSM file changed during actual operation")

    material = {
        "contract": CONTRACT,
        "selection_kind": "HISTORICAL_QSM_QUESTION_COVERAGE_ONLY",
        "qsm_artifact_sha256": resolution.authority_artifact_sha256,
        "qsm_row_sha256": resolution.authority_row["row_payload_hash"],
        "qsm_rule_id": resolution.authority_row["authority_rule_id"],
        "qsm_rule_version": resolution.authority_row["authority_version"],
        "qsm_resolution": resolution.status,
        "qsm_lookup": resolution.lookup_key,
        "source_universe_ref": universe.ref.as_dict(),
        "native_question_ref": selection.native_question_ref.as_dict(),
        "target_use_ref": selection.target_use_ref.as_dict(),
        "target_use_authority_ref": selection.target_use_authority_ref.as_dict(),
        "target_use_operation": selection.target_use_operation,
        "reader": "rawlsing_next.pre553_route_b_production.execute_route_b_production",
        "route_receipt_identity": route.replay_receipt["receipt_identity"],
        "c11_release_ref": route.c11_release.release_ref.as_dict(),
        "i03_query_refs": [x.query_ref.as_dict() for x in route.i03_results],
        "i03_fact_refs": [
            [fact.ref.as_dict() for fact in x.facts] for x in route.i03_results
        ],
        "i05_receipt_refs": [x.ref.as_dict() for x in route.i05_result.receipts],
        "i05_historical_qsm_authority_established": False,
        "original35_native_or_historical_production": False,
    }
    return SelectedQsmRouteResult(route, {**material, "binding_root": semantic_hash(material)})
