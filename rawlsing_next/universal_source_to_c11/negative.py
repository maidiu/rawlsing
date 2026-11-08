"""Negative and refusal evidence for the universal receive seam."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from rawlsing_next.source_configuration.errors import (
    SourceConfigurationBindingError,
    SourceConfigurationFactoryError,
    SourceConfigurationSchemaError,
)
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    build_validated_c11_release_from_config,
)
from rawlsing_next.source_configuration.reader import reader_configuration_from_config
from rawlsing_next.source_configuration.schema import validate_source_config
from rawlsing_next.source_configuration.library import SourceNotPrepared

from .registry import UniversalSourceRegistry

SOURCE_BYTE_SUFFIXES = frozenset({".sav", ".dta", ".por", ".db", ".mdb", ".accdb"})


def _record(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"name": name, "passed": passed, "detail": detail}


def run_negative_suite(registry: UniversalSourceRegistry) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    # 1. Unknown source ID is refused by the registry.
    try:
        registry.slot("SRC99")
    except SourceNotPrepared as exc:
        checks.append(_record("unknown_source_refused", True, str(exc)))
    else:
        checks.append(_record("unknown_source_refused", False, "SRC99 was accepted"))

    src01 = registry.slot("SRC01")
    src02 = registry.slot("SRC02")

    # 2. A fixture stream from another source is refused before construction.
    try:
        build_validated_c11_release_from_config(
            src01.fixture_config, stream=src02.fixture_stream)
    except (SourceConfigurationBindingError, SourceConfigurationFactoryError) as exc:
        checks.append(_record("cross_source_fixture_refused", True, type(exc).__name__))
    else:
        checks.append(_record("cross_source_fixture_refused", False, "cross-source fixture accepted"))

    # 3. A fixture may not reuse the original source SHA.
    forged = deepcopy(src01.fixture_config.document)
    forged["binding"]["source_sha256"] = forged["identity"]["expected_source_sha256"]
    try:
        validate_source_config(forged)
    except SourceConfigurationSchemaError as exc:
        checks.append(_record("fixture_original_sha_reuse_refused", True, type(exc).__name__))
    else:
        checks.append(_record("fixture_original_sha_reuse_refused", False, "fixture SHA reuse accepted"))

    # 4. A fixture config is not an original source-read transport.
    try:
        reader_configuration_from_config(src01.fixture_config)
    except SourceConfigurationBindingError as exc:
        checks.append(_record("fixture_reader_refused", True, str(exc)))
    else:
        checks.append(_record("fixture_reader_refused", False, "fixture reader accepted"))

    # 5. A wrong active source SHA is refused by the generic factory.
    try:
        build_governed_c11_projection(
            src01.fixture_config, source_sha256=src02.fixture_stream.source_sha256)
    except SourceConfigurationBindingError as exc:
        checks.append(_record("wrong_active_source_sha_refused", True, str(exc)))
    else:
        checks.append(_record("wrong_active_source_sha_refused", False, "wrong active SHA accepted"))

    # 6. Original execution remains NOT_RUN for all 35 original configs.
    original_not_run = []
    for source_id in registry.source_ids:
        document = registry.slot(source_id).original_config.document
        scope = document["supported_scope"]
        if scope.get("native_validation_expectation") != "NOT_RUN":
            original_not_run.append(source_id)
        if scope.get("original_source_execution") != "NOT_PERFORMED_UNDER_R157_PREPARATION":
            original_not_run.append(source_id)
    checks.append(_record(
        "original_execution_not_run_for_all_35",
        not original_not_run,
        "all original configs preserve NOT_RUN" if not original_not_run else f"drift: {original_not_run}",
    ))

    # 7. No original source byte carriers are bundled in the imported package.
    carriers = []
    for relative in ("rawlsing_next/source_configuration", "source_pre553_validation"):
        for path in (registry.root / relative).rglob("*"):
            if path.is_file() and path.suffix.lower() in SOURCE_BYTE_SUFFIXES:
                carriers.append(path.relative_to(registry.root).as_posix())
    checks.append(_record(
        "no_original_source_byte_carriers_bundled",
        not carriers,
        "no SAV/DTA/POR/DB carriers" if not carriers else f"carriers: {carriers}",
    ))

    # 8. Original operation plan remains metadata-only and unexecuted.
    plan = registry.library.original_plan(
        "SRC01",
        source_path="/never/opened/SRC01.sav",
        host="universal-source-to-c11-negative",
        purpose="NEGATIVE_REFUSAL_ONLY",
        consumer_use="NEGATIVE_REFUSAL_ONLY",
        semantic_use_scope=("NEGATIVE_REFUSAL_ONLY",),
    )
    plan_ok = (
        plan.get("source_read_performed") is False
        and plan.get("original_workload_issued") is False
    )
    checks.append(_record(
        "original_plan_metadata_only",
        plan_ok,
        "source_read_performed=false, original_workload_issued=false",
    ))

    return {
        "schema": "PYAT_777_UNIVERSAL_SOURCE_TO_C11_NEGATIVE_EVIDENCE@1.0.0",
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
        "original_source_bytes_read": False,
        "original_source_execution_performed": False,
        "source_read_permission_created": False,
        "protected_or_production_merge_performed": False,
    }
