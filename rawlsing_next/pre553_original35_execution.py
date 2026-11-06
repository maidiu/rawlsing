"""D: bounded original35 manifest and original-source C11 execution bridge.

A source_configuration library is the selector; the B operation plan is the
accounting layer. This module decodes caller-authorized original bytes through
the existing physical decoder, builds the existing governed C11 release and
repository, and records RAW observed-sample products. It never invents source
semantics, native rights or a second compiler.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import json
import os
from pathlib import Path
import time
from typing import Any, Mapping

from rawlsing_next.pre553_original35_operations import (
    EXECUTABLE, OPERATION_F1, build_original35_operation_plan,
)
from rawlsing_next.pre553_physical_decoder import decode_dta, decode_sav
from rawlsing_next.pre553_empirical_objects import RespondentEvent
from rawlsing_next.source_configuration.factory import (
    build_source_backed_c11_repository_from_config,
    build_validated_c11_release_from_config,
)
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.reader import decode_config_with_source_read_permission
from rawlsing_next.pre553_original35_physical_stream import bounded_physical_cell_stream
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.pre553_source_native_preimage_adapter import (
    NativeSourceIdentity, NativeSourcePackage, NativeSourceRule,
    materialize_native_preimages,
)
from rawlsing_next.pre553_universal_workload import (
    compile_universal_workload, execute_universal_workload,
)

SCHEMA = "PRE553_ORIGINAL35_EXECUTION@1.0.0"
DEFAULT_BINDING = Path(".local-logs/pyat-universal35/source-runtime-binding.local.json")


class Original35ExecutionError(ValueError):
    pass


@dataclass(frozen=True)
class SourceExecutionResult:
    source_id: str
    status: str
    source_sha256: str | None
    config_path: str | None
    source_format: str | None
    row_count: int
    physical_slots: int
    response_slots: int
    operation_counts: Mapping[str, int]
    c11_release_ref: Mapping[str, Any] | None
    c11_object_count: int
    raw_state_counts: Mapping[str, int]
    question_state_counts: Mapping[str, Mapping[str, int]]
    respondent_count: int
    max_events_per_respondent: int
    respondents_with_3plus_items: int
    repository_ref: str | None
    elapsed_seconds: float
    maxrss_bytes: int
    reasons: tuple[str, ...]

    def material(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA, "source_id": self.source_id, "status": self.status,
            "source_sha256": self.source_sha256, "config_path": self.config_path,
            "source_format": self.source_format, "row_count": self.row_count,
            "physical_slots": self.physical_slots,
            "response_slots": self.response_slots,
            "operation_counts": dict(self.operation_counts),
            "c11_release_ref": dict(self.c11_release_ref) if self.c11_release_ref else None,
            "c11_object_count": self.c11_object_count,
            "raw_state_counts": dict(self.raw_state_counts),
            "question_state_counts": {
                key: dict(value) for key, value in self.question_state_counts.items()
            },
            "respondent_count": self.respondent_count,
            "max_events_per_respondent": self.max_events_per_respondent,
            "respondents_with_3plus_items": self.respondents_with_3plus_items,
            "repository_ref": self.repository_ref,
            "elapsed_seconds": round(self.elapsed_seconds, 3),
            "maxrss_bytes": self.maxrss_bytes,
            "reasons": list(self.reasons), "native": False,
        }


def load_runtime_binding(path: str | Path | None = None) -> dict[str, Any]:
    target = Path(path or os.environ.get("PYAT_SOURCE_RUNTIME_BINDING", DEFAULT_BINDING))
    if not target.is_file():
        raise Original35ExecutionError("SOURCE_RUNTIME_BINDING_REQUIRED:" + str(target))
    document = json.loads(target.read_text(encoding="utf8"))
    root = document.get("USER_ORIGINAL35_DATA_ROOT")
    if not isinstance(root, str) or not Path(root).is_dir():
        raise Original35ExecutionError("SOURCE_ROOT_UNAVAILABLE")
    return document


def _encoding(config) -> str | None:
    reader = config.document["identity"].get("reader") or {}
    value = reader.get("encoding")
    return value.get("value") if isinstance(value, Mapping) else None


def _maxrss() -> int:
    try:
        import resource
        return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    except Exception:
        return 0


def _raw_products(release) -> tuple[dict[str, int], dict[str, dict[str, int]], int, int, int]:
    states: Counter[str] = Counter()
    by_question: dict[str, Counter[str]] = defaultdict(Counter)
    by_respondent: dict[str, set[str]] = defaultdict(set)
    objects = list(release.public_objects)
    for obj in objects:
        if not isinstance(obj, RespondentEvent):
            continue
        state = str(obj.typed_state)
        states[state] += 1
        question = str(dict(obj.native_question_ref).get("object_id", "UNKNOWN"))
        by_question[question][state] += 1
        respondent = str(dict(obj.scoped_respondent_ref).get("object_id", "UNKNOWN"))
        by_respondent[respondent].add(question)
    max_items = max((len(value) for value in by_respondent.values()), default=0)
    three_plus = sum(1 for value in by_respondent.values() if len(value) >= 3)
    return (dict(sorted(states.items())),
            {key: dict(sorted(value.items())) for key, value in sorted(by_question.items())},
            len(by_respondent), max_items, three_plus)


def execute_source(source_id: str, *, library: SourceConfigLibrary,
                   source_root: str | Path, state_root: str | Path | None = None,
                   allow_decode: bool = True) -> SourceExecutionResult:
    started = time.time()
    reasons: list[str] = []
    config = library.load_original(source_id)
    selection = library.select(source_id, source_root=source_root)
    resolution = selection.get("source_resolution") or {}
    if resolution.get("status") != "RESOLVED_UNDER_EFFECTIVE_ROOT":
        raise Original35ExecutionError(
            "SOURCE_PATH_UNRESOLVED:" + str(resolution.get("status")))
    path = Path(resolution["resolved_source_path"])
    if not path.is_file():
        raise Original35ExecutionError("SOURCE_NOT_PRESENT_HERE:" + source_id)
    plan = build_original35_operation_plan(
        [config.document], source_presence={source_id: True},
        require_all35=False)
    row = plan.rows[0]
    if not allow_decode:
        return SourceExecutionResult(
            source_id=source_id, status="MANIFEST_ONLY", source_sha256=row.source_sha256,
            config_path=selection.get("original_config_path"),
            source_format=selection.get("source_format"), row_count=0,
            physical_slots=len(row.physical_slots),
            response_slots=row.response_slot_count,
            operation_counts=row.counts, c11_release_ref=None,
            c11_object_count=0, raw_state_counts={}, question_state_counts={},
            respondent_count=0, max_events_per_respondent=0,
            respondents_with_3plus_items=0, repository_ref=None,
            elapsed_seconds=time.time() - started, maxrss_bytes=_maxrss(),
            reasons=("MANIFEST_ONLY_NOT_DECODED",))
    fmt = str(selection.get("source_format") or "").upper()
    encoding = _encoding(config)
    try:
        if fmt == "SAV":
            incidence = decode_sav(path, encoding=encoding)
        elif fmt == "DTA":
            incidence = decode_dta(path, encoding=encoding)
        else:
            raise Original35ExecutionError("SOURCE_FORMAT_UNSUPPORTED:" + fmt)
        if incidence.source_sha256 != row.source_sha256:
            raise Original35ExecutionError("SOURCE_SHA_MISMATCH_AFTER_DECODE:" + source_id)
        release = build_validated_c11_release_from_config(config, incidence=incidence)
        repository, _repo_release = build_source_backed_c11_repository_from_config(
            config, incidence)
        raw_states, question_states, respondents, max_items, three_plus = _raw_products(release)
        release_ref = release.release_ref.as_dict()
    except Exception as exc:
        reason = type(exc).__name__ + ":" + str(exc)
        return SourceExecutionResult(
            source_id=source_id, status="C11_RELEASE_REFUSED",
            source_sha256=row.source_sha256,
            config_path=selection.get("original_config_path"),
            source_format=fmt, row_count=0,
            physical_slots=len(row.physical_slots),
            response_slots=row.response_slot_count,
            operation_counts=row.counts, c11_release_ref=None,
            c11_object_count=0, raw_state_counts={}, question_state_counts={},
            respondent_count=0, max_events_per_respondent=0,
            respondents_with_3plus_items=0, repository_ref=None,
            elapsed_seconds=time.time() - started, maxrss_bytes=_maxrss(),
            reasons=(reason,))
    result = SourceExecutionResult(
        source_id=source_id, status="ORIGINAL_C11_RELEASE_EXECUTED",
        source_sha256=incidence.source_sha256,
        config_path=selection.get("original_config_path"),
        source_format=fmt, row_count=incidence.row_count,
        physical_slots=len(row.physical_slots), response_slots=row.response_slot_count,
        operation_counts=row.counts, c11_release_ref=release_ref,
        c11_object_count=len(list(release.public_objects)),
        raw_state_counts=raw_states, question_state_counts=question_states,
        respondent_count=respondents, max_events_per_respondent=max_items,
        respondents_with_3plus_items=three_plus,
        repository_ref=getattr(repository, "repository_id", None),
        elapsed_seconds=time.time() - started, maxrss_bytes=_maxrss(),
        reasons=tuple(reasons))
    if state_root is not None:
        target = Path(state_root) / (source_id + ".json")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result.material(), indent=2, sort_keys=True) + "\n",
                          encoding="utf8")
    return result




def execute_native_compiler_source(source_id: str, *, library: SourceConfigLibrary,
                                   source_root: str | Path, host: str,
                                   purpose: str, as_of: str,
                                   max_items: int | None = None,
                                   resolver: Any | None = None,
                                   incidence: Any | None = None,
                                   state_root: str | Path | None = None) -> dict[str, Any]:
    """Run supported route-qualified items through CURRENT R03/I03/Batch facts.

    ``incidence`` must be a caller-admitted PhysicalSourceIncidence. Otherwise a
    caller-supplied current source-read ``resolver`` is required; this function
    never decodes original bytes without the existing admission decision.
    """
    started = time.time()
    config = library.load_original(source_id)
    doc = config.document
    selection = library.select(source_id, source_root=source_root)
    resolution = selection["source_resolution"]
    if resolution.get("status") != "RESOLVED_UNDER_EFFECTIVE_ROOT":
        raise Original35ExecutionError("SOURCE_PATH_UNRESOLVED")
    path = Path(resolution["resolved_source_path"])
    respondent = doc.get("respondents") or {}
    if "HOUSEHOLD" in str(respondent.get("subject_unit", "")).upper():
        raise Original35ExecutionError(
            "NON_SCALAR_HOUSEHOLD_TOPOLOGY_REQUIRES_STREAM_OCCURRENCE_PLAN")
    plan = build_original35_operation_plan(
        [doc], source_presence={source_id: True}, require_all35=False)
    qualified = []
    for op in plan.operations:
        if (op.source_id == source_id and op.kind == OPERATION_F1
                and op.status == EXECUTABLE
                and op.route_status == "ELIGIBLE_APPLICABLE"
                and op.response_values):
            original_id = op.item_ids[0]
            physical = op.source_variable_codes[0]
            if not original_id or not physical:
                raise Original35ExecutionError("ORIGINAL_ID_OR_PHYSICAL_CODE_ABSENT")
            qualified.append((physical, op.response_values, original_id))
    if max_items is not None:
        if type(max_items) is not int or max_items < 1:
            raise Original35ExecutionError("DIAGNOSTIC_MAX_ITEMS_INVALID")
        qualified = qualified[:max_items]
    if not qualified:
        raise Original35ExecutionError("NO_ROUTE_QUALIFIED_SUBSTANTIVE_ITEMS")
    selected_names = {name for name, _, _ in qualified}
    coordinate = None
    for slot in doc.get("coordinate_slots", []):
        name = slot["slot"]["name"]
        if name not in selected_names:
            coordinate = name
            break
    if coordinate is None:
        raise Original35ExecutionError("COORDINATE_FACT_ABSENT_NOT_GUESSED")
    fmt = str(selection.get("source_format") or "").upper()
    if incidence is None:
        if resolver is None:
            raise Original35ExecutionError(
                "CURRENT_SOURCE_READ_DECISION_REQUIRED_BEFORE_IO")
        incidence = decode_config_with_source_read_permission(
            config, source_path=path, resolver=resolver, host=host,
            purpose=purpose, consumer_use="D_ORIGINAL35_NATIVE_EXECUTION",
            semantic_use_scope=("RAW_OBSERVED_SAMPLE",))
    if incidence.source_sha256 != doc["binding"]["source_sha256"]:
        raise Original35ExecutionError("SOURCE_SHA_MISMATCH_AFTER_DECODE")
    selected_variables = tuple(sorted(selected_names | {coordinate}))
    stream = bounded_physical_cell_stream(
        incidence, include_variables=selected_variables)
    package = NativeSourcePackage(
        source=NativeSourceIdentity(
            source_id=source_id, family=str(doc["identity"]["family"]),
            wave=str(doc["identity"]["wave"]),
            canonical_filename=str(doc["identity"]["source_artifact_id"]),
            declared_sha256=incidence.source_sha256, source_format=fmt,
            expected_rows=incidence.row_count),
        selected=tuple(NativeSourceRule(
            implementation_id=item_id,
            source_variable_code=name, unit="person")
            for name, _values, item_id in qualified),
        coordinate_variable=coordinate,
        study_product_id=str(doc["identity"]["study_product_id"]),
        release_id=str(doc["identity"]["release_id"]),
        instrument_release_id=str(doc["identity"]["instrument_release_id"]),
        as_of=as_of)
    bundle = materialize_native_preimages(package=package, incidence=stream)
    compilation = compile_universal_workload(
        bundle=bundle, as_of=as_of, host=host, purpose=purpose)
    result = execute_universal_workload(
        compilation=compilation, source_factory=lambda _ref: bundle.physical_stream)
    material = {
        "schema": "PRE553_ORIGINAL35_NATIVE_COMPILER_RESULT@1.0.0",
        "source_id": source_id, "source_sha256": incidence.source_sha256,
        "selected_items": [name for name, _, _ in qualified],
        "selected_original_ids": {name: item_id for name, _, item_id in qualified},
        "selected_values": {name: list(values) for name, values, _ in qualified},
        "coordinate_variable": coordinate,
        "source_custody": dict(incidence.source_custody or {}),
        "diagnostic_max_items": max_items,
        "row_count": incidence.row_count,
        "compilation_hash": compilation.content_hash,
        "expected_jobs": [list(job) for job in compilation.expected_jobs],
        "executed_operation_ids": list(result.executed_operation_ids),
        "fact_refs": [ref.as_dict() for ref in result.fact_refs],
        "receipt_refs": [ref.as_dict() for ref in result.receipt_refs],
        "anti_join": result.anti_join(),
        "native_result_count": len(result.native_results),
        "failed": list(result.failed),
        "elapsed_seconds": round(time.time() - started, 3),
        "maxrss_bytes": _maxrss(), "native": False,
    }
    if state_root is not None:
        target = Path(state_root) / (source_id + ".native.json")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(material, indent=2, sort_keys=True) + "\n",
                          encoding="utf8")
    return material


def execute_all(*, library: SourceConfigLibrary, source_root: str | Path,
                state_root: str | Path | None = None,
                allow_decode: bool = True) -> list[SourceExecutionResult]:
    results = []
    for source_id in library.source_ids():
        results.append(execute_source(
            source_id, library=library, source_root=source_root,
            state_root=state_root, allow_decode=allow_decode))
    return results


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--binding", default=str(DEFAULT_BINDING))
    parser.add_argument("--state", default=".local-logs/pyat-universal35/d-state")
    args = parser.parse_args(argv)
    binding = load_runtime_binding(args.binding)
    root = binding["USER_ORIGINAL35_DATA_ROOT"]
    library = SourceConfigLibrary(index_path="source_pre553_validation/integration/SOURCE_LIBRARY_INDEX.json",
                                  source_root=root)
    ids = library.source_ids() if args.all else tuple(args.source)
    if not ids:
        parser.error("--source or --all required")
    for source_id in ids:
        result = execute_source(source_id, library=library, source_root=root,
                                state_root=args.state,
                                allow_decode=not args.manifest_only)
        print(json.dumps(result.material(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "DEFAULT_BINDING", "Original35ExecutionError", "SCHEMA",
    "SourceExecutionResult", "execute_all",
    "execute_native_compiler_source", "execute_source",
    "load_runtime_binding", "main",
]
