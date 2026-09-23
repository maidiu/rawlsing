#!/usr/bin/env python3
"""EE-P2R5B local I02 successor-release mechanical executor.

This driver performs no semantic choice. It:
- verifies the exact LiTS-I carrier identity and frozen decoder status;
- replays the exact accepted AS2B base construction from vendored accepted bytes;
- verifies the accepted base candidate/release identities;
- obtains the frozen F02 q310/q311 package from the exact vendored F02 producer;
- constructs only the q310/q311 I02 source extension under those frozen refs;
- builds one complete PRE553_C11_INGEST@1.0.0 candidate;
- lets I02 mint the successor release identity;
- atomically ingests into C11Repository and proves exact resolution;
- emits facts only. It claims no R5A realization authority and no equality between
  the frozen F02 scope anchor and the accepted I02 runtime release.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
from decimal import Decimal
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from rawlsing_next.pre553_c11_ingest import (
    C11SourceReleaseCandidate,
    SourceReleaseManifest,
    build_candidate_replay_manifest,
    ingest_c11_source_release,
    record_counts_for_candidate,
    validate_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import (
    M01_M18,
    QuestionVariableBinding,
    TypedAbsence,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    RoutingEligibilityFact,
    canonical_json,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ONLY,
    PhysicalMissingState,
    PhysicalSourceIncidence,
    decode_dta,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    OccurrenceRule,
    PhysicalSlot,
    ResponseSlotRule,
    ResponseValueRule,
    physical_value_binding_key,
    project_c11_candidate_from_physical_cells,
)

CONTRACT = "EE_P2R5B_I02_SUCCESSOR_RELEASE_MECHANICAL_EXECUTION@1.0.0"
PASS_TERMINAL = (
    "EE_P2R5B_PASS__I02_SUCCESSOR_RELEASE_LOCAL_EXECUTION_FULLY_MECHANIZED__"
    "EXACT_SOURCE_ACCESS_ONLY_REMAINS__NO_REALIZATION_AUTHORITY_CLAIMED"
)
SOURCE_NAME = "LITS-2006-data.dta"
SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
SOURCE_ROWS = 29_002
SOURCE_VARIABLES = 1_198
ACCEPTED_BASE_CANDIDATE_HASH = "7f81a222ea2611638d7ce7ac55c695120b57323832e6dc17ff65c1992201659c"
ACCEPTED_BASE_RELEASE_HASH = "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
ACCEPTED_BASE_REPLAY_HASH = "6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd"
ACCEPTED_BASE_PROJECTION_HASH = "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872"
FROZEN_F02_SCOPE_HASH = "bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297"

HERE = Path(__file__).resolve().parent
SUPPORT = HERE / "SUPPORT"
AS2B = SUPPORT / "FROZEN_BASE" / "AS2B_LITS1_MECHANICAL_SOURCE_CERTIFICATION_20260827" / "run_as2b_lits1_mechanical_certification.py"
AS2A_LEDGER = SUPPORT / "FROZEN_BASE" / "AS2A_LITS1_SHARED_CERTIFICATION_20260827" / "01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv"
AS2A_PACKAGE = SUPPORT / "FROZEN_BASE" / "AS2A_LITS1_SHARED_CERTIFICATION_20260827" / "04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json"
F02 = SUPPORT / "FROZEN_F02" / "prev3_lits1_selector_closure.py"

FROZEN_GIT_BLOBS = {
    AS2B: "c51b56779ab9d79126619b7733d41f5253c8150f",
    AS2A_LEDGER: "c24e0d6acc6f2b823f0fc3fa5fb8a52b7c1cab0c",
    AS2A_PACKAGE: "174b931e8aa89111086e3d46159b47154bed7f16",
    F02: "7b45b277164fa90c3da739aab26b516f7a8cb8dc",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    h = hashlib.sha1()
    h.update(f"blob {len(payload)}\0".encode("ascii"))
    h.update(payload)
    return h.hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load frozen module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def exact_ref(value: Mapping[str, Any]) -> ExactRef:
    return ExactRef(value["kind"], value["object_id"], value["content_hash"])


def authority_ref(value: Mapping[str, Any]) -> AuthorityRef:
    return AuthorityRef(
        value["authority_id"],
        value["authority_version"],
        value["authority_content_hash"],
    )


def local_ref(kind: str, tag: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:prev3:ee-p2r5b:{tag}:sha256:{digest}", digest)


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def verify_frozen_support() -> dict[str, str]:
    observed: dict[str, str] = {}
    for path, expected in FROZEN_GIT_BLOBS.items():
        if not path.is_file():
            raise RuntimeError(f"frozen support file missing: {path}")
        got = git_blob_sha1(path)
        if got != expected:
            raise RuntimeError(f"frozen support Git blob mismatch: {path}: {got} != {expected}")
        observed[str(path.relative_to(HERE))] = got
    return observed


def selected_incidence(incidence: PhysicalSourceIncidence, names: Iterable[str]) -> PhysicalSourceIncidence:
    wanted = frozenset(names)
    variables = tuple(v for v in incidence.variables if v.name in wanted)
    if {v.name for v in variables} != wanted:
        missing = sorted(wanted - {v.name for v in variables})
        raise RuntimeError(f"required source slots unavailable: {missing}")
    if incidence._frame is None:
        raise RuntimeError("frozen compatibility decoder did not retain the exact source frame")
    frame = incidence._frame[[v.name for v in variables]]
    return PhysicalSourceIncidence(
        source_sha256=incidence.source_sha256,
        source_format=incidence.source_format,
        row_count=incidence.row_count,
        variables=variables,
        reader_configuration={**incidence.reader_configuration, "transport": "EE_P2R5B_EXACT_SELECTED_SLOT_STREAM"},
        file_metadata=incidence.file_metadata,
        _frame=frame,
    )


def exact_cells(selected: PhysicalSourceIncidence, base_module):
    for cell in selected.iter_cells(batch_size=20_000):
        yield base_module.exact_cell(cell)


def adapt_f02_authority_snapshot(raw: Mapping[str, Any], f02_module) -> AuthoritySnapshot:
    """Carrier-wrap an exact frozen F02 authority ref without enlarging its grant.

    The exact authority id/version/content hash, kind, operations, scope, parent refs,
    and negative ceiling are copied from F02. governed_object_families is deliberately
    empty: this adapter does not invent a public-object-family grant that F02 never made.
    """
    aref = authority_ref(raw["authority_ref"])
    material = {
        "schema": "EE_P2R5B_F02_AUTHORITY_SNAPSHOT_CARRIER_ADAPTER@1.0.0",
        "frozen_f02_snapshot": raw,
        "f02_contract": f02_module.CONTRACT_ID,
        "f02_commission_tip": f02_module.F02_COMMISSION_TIP,
        "no_authority_expansion": True,
    }
    scope = dict(raw["scope"])
    scope["negative_ceiling"] = raw["negative_ceiling"]
    return AuthoritySnapshot(
        typed_state=raw["decision_state"],
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=local_ref(
            "F02AuthoritySnapshotCarrierReplay", "f02-authority-snapshot", material
        ),
        authority_id=aref.authority_id,
        authority_version=aref.authority_version,
        authority_content_hash=aref.authority_content_hash,
        authority_kind=raw["authority_kind"],
        decision_state=raw["decision_state"],
        governed_operations=tuple(raw["governed_operations"]),
        governed_object_families=(),
        scope_envelope=scope,
        effective_time_or_interval=f"F02_COMMISSION_TIP:{f02_module.F02_COMMISSION_TIP}",
        parent_authority_refs=tuple(authority_ref(x) for x in raw["parent_authority_refs"]),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash(material),
        replay_protocol_ref=local_ref(
            "F02AuthorityMaterial", "f02-authority-material", raw
        ),
    )


def canonical_authority_union(*groups: Iterable[AuthoritySnapshot]) -> tuple[AuthoritySnapshot, ...]:
    by_key: dict[str, AuthoritySnapshot] = {}
    for group in groups:
        for snapshot in group:
            key = snapshot.authority_ref.key
            existing = by_key.get(key)
            if existing is not None and existing.authority_ref != snapshot.authority_ref:
                raise RuntimeError("conflicting authority ref in candidate closure")
            by_key[key] = snapshot
    return tuple(sorted(by_key.values(), key=lambda x: x.authority_ref.key))


def build_extension_projection(
    *,
    base_projection,
    base_context: Mapping[str, Any],
    slots: Mapping[str, int],
    closure: Mapping[str, Any],
    f02_module,
):
    if slots.get("q310") != 230 or slots.get("q311") != 231:
        raise RuntimeError("accepted source physical q310/q311 slot identities changed")
    if f02_module.QUESTION_SPECS["q310"][0] != 229 or f02_module.QUESTION_SPECS["q311"][0] != 230:
        raise RuntimeError("frozen F02 zero-based ledger coordinates changed")

    f02_raw = closure["authorities"]["snapshots"]
    f02_snapshots = tuple(
        adapt_f02_authority_snapshot(f02_raw[name], f02_module)
        for name in ("source_semantics", "routing", "predicate_grammar", "replay")
    )
    authorities = canonical_authority_union(base_projection.authority_snapshots, f02_snapshots)
    auth_refs = {name: authority_ref(closure["authorities"]["refs"][name])
                 for name in ("source_semantics", "routing", "predicate_grammar", "replay")}

    qbindings = []
    response_slots = []
    qrefs: dict[str, ExactRef] = {}
    for q in ("q310", "q311"):
        package = closure["questions"][q]
        qref = exact_ref(package["question_ref"])
        qrefs[q] = qref
        binding = QuestionVariableBinding(
            empirical_universe_ref=base_projection.universes[0].ref,
            native_question_ref=qref,
            instrument_question_version=base_projection.instrument_release_id,
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=auth_refs["source_semantics"],
            topology_authority_ref=auth_refs["source_semantics"],
        )
        qbindings.append(binding)
        topology_ref = exact_ref(package["slot_ref"])
        occurrence = OccurrenceRule(
            "f02-scalar-0",
            topology_ref,
            {"kind": "SCALAR_SINGULAR", "index": 0},
        )
        rules = tuple(
            ResponseValueRule(
                physical_value_binding_key(Decimal(value), PhysicalMissingState.OBSERVED_STORAGE_VALUE),
                "SUBSTANTIVE_RESPONSE",
                (occurrence,),
            )
            for value in (1, 2, 3)
        ) + (
            ResponseValueRule(
                physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING),
                "MISSING",
                (occurrence,),
            ),
        )
        response_slots.append(
            ResponseSlotRule(PhysicalSlot(slots[q], q), binding, rules)
        )

    risk_set_ref = local_ref(
        "RISK_SET",
        "f02-q310-q311-selected-respondents",
        {
            "source_sha256": SOURCE_SHA256,
            "universe_ref": base_projection.universes[0].ref.as_dict(),
            "respondent_count": SOURCE_ROWS,
            "question_refs": [qrefs[q].as_dict() for q in ("q310", "q311")],
            "f02_routing_refs": [
                closure["questions"][q]["routing_ref"] for q in ("q310", "q311")
            ],
            "law": "PHYSICAL_SLOT_PRESENT_ALL_ROWS__CELL_MISSINGNESS_PRESERVED",
        },
    )
    member_set_ref = local_ref(
        "MEMBER_SET",
        "f02-selected-respondent-row-set",
        {
            "source_sha256": SOURCE_SHA256,
            "row_ordinal_1based_first": 1,
            "row_ordinal_1based_last": SOURCE_ROWS,
            "count": SOURCE_ROWS,
            "respondent_namespace": base_projection.universes[0].respondent_namespace,
        },
    )
    routing = tuple(
        RoutingEligibilityFact(
            typed_state="ELIGIBLE_APPLICABLE",
            authority_snapshot_refs=(auth_refs["routing"],),
            dependency_refs=(respondent.ref, qrefs[q]),
            producer_replay_locator_or_reference_root=local_ref(
                "F02RoutingReplay",
                f"{q}-row-{row}",
                {
                    "source_sha256": SOURCE_SHA256,
                    "physical_row_ordinal_1based": row,
                    "respondent_ref": respondent.ref.as_dict(),
                    "question_ref": qrefs[q].as_dict(),
                    "f02_routing_ref": closure["questions"][q]["routing_ref"],
                },
            ),
            empirical_universe_ref=base_projection.universes[0].ref,
            scoped_respondent_ref=respondent.ref,
            question_or_target_ref=qrefs[q],
            risk_set_ref=risk_set_ref,
            routing_rule_ref=exact_ref(closure["questions"][q]["routing_ref"]),
            applicability_state="ELIGIBLE_APPLICABLE",
            routing_state="ELIGIBLE_APPLICABLE",
            parent_predicate_refs=(),
            member_set_replay_ref=member_set_ref,
        )
        for row, respondent in enumerate(base_projection.respondents, 1)
        for q in ("q310", "q311")
    )

    projection_material = {
        "schema": "EE_P2R5B_F02_I02_EXTENSION_PROJECTION@1.0.0",
        "source_sha256": SOURCE_SHA256,
        "accepted_base_projection_ref": base_projection.projection_identity_ref.as_dict(),
        "accepted_base_release_hash": ACCEPTED_BASE_RELEASE_HASH,
        "frozen_f02_scope_anchor": closure["new_release_ref"],
        "questions": {
            q: {
                "question_ref": closure["questions"][q]["question_ref"],
                "response_slot_ref": closure["questions"][q]["slot_ref"],
                "routing_ref": closure["questions"][q]["routing_ref"],
                "response_value_state_refs": closure["questions"][q]["value_state_refs"],
            }
            for q in ("q310", "q311")
        },
        "f02_authority_refs": closure["authorities"]["refs"],
        "negative_ceiling": f02_module.NEGATIVE_CEILING,
        "row_binding": "SAME_ACCEPTED_AS2B_RESPONDENT_REFS__PHYSICAL_ROW_1BASED",
        "no_realization_authority_claim": True,
    }
    projection_ref = local_ref(
        "GovernedC11Projection",
        "f02-i02-extension-projection",
        projection_material,
    )

    # A coordinate slot is retained only because the accepted source-backed facade
    # requires every standalone projection object to carry a coordinate section.
    # The generated extension coordinate facts are discarded; the final successor
    # candidate retains the accepted base coordinate facts unchanged.
    projection = base_module_class(base_projection)(
        projection_identity_ref=projection_ref,
        source_artifact_id=base_projection.source_artifact_id,
        expected_source_sha256=base_projection.expected_source_sha256,
        source_family_id=base_projection.source_family_id,
        study_product_id=base_projection.study_product_id,
        release_id=f"LITS1-R5B-EXTENSION-TEMP-{SOURCE_SHA256[:16]}-{FROZEN_F02_SCOPE_HASH[:16]}",
        instrument_release_id=base_projection.instrument_release_id,
        source_snapshot_retention_ref=base_projection.source_snapshot_retention_ref,
        universes=base_projection.universes,
        respondents=base_projection.respondents,
        row_bindings=base_projection.row_bindings,
        questions=tuple(qbindings),
        response_slots=tuple(response_slots),
        coordinate_slots=(base_projection.coordinate_slots[0],),
        routing=routing,
        weight_slots=(),
        authority_snapshots=authorities,
        source_relations=base_projection.source_relations,
        predicate_replay=base_projection.predicate_replay,
        comparator_replay=base_projection.comparator_replay,
        discovery_replay=base_projection.discovery_replay,
        structural_replay=base_projection.structural_replay,
        required_authority_refs=tuple(sorted(
            (auth_refs["source_semantics"], auth_refs["routing"], auth_refs["replay"]),
            key=lambda x: x.key,
        )),
        projection_authority_ref=auth_refs["source_semantics"],
        replay_authority_ref=auth_refs["replay"],
        tie_order_ref=base_projection.tie_order_ref,
        replay_protocol_version=f02_module.CONTRACT_ID,
    )
    return projection, tuple(qbindings), routing, authorities, auth_refs, projection_material


def base_module_class(base_projection):
    # Preserve the exact accepted AS2B linearized constructor class, whose only
    # difference from the frozen production constructor is removal of quadratic
    # repetition in row-reference validation.
    return type(base_projection)


def f02_source_scan(incidence: PhysicalSourceIncidence, f02_module) -> dict[str, Any]:
    if incidence._frame is None:
        raise RuntimeError("source frame unavailable for exact F02 replay check")
    frame = incidence._frame[["q310", "q311"]]

    def scalar(value: Any) -> Any:
        if hasattr(value, "item"):
            try:
                return value.item()
            except Exception:
                pass
        return value

    rows = [
        {
            "row_ordinal": i,
            "q310": scalar(q310),
            "q311": scalar(q311),
        }
        for i, (q310, q311) in enumerate(frame.itertuples(index=False, name=None))
    ]
    summary = f02_module.scan_records(rows)
    f02_module.verify_real_source_summary(summary)
    return summary


def ref_root(items: Iterable[Any]) -> str:
    h = hashlib.sha256()
    for item in sorted(items, key=lambda x: x.ref.key):
        h.update((canonical_json(item.ref.as_dict()) + "\n").encode("utf-8"))
    return h.hexdigest()


def row_alignment_root(respondents: Iterable[Any]) -> str:
    h = hashlib.sha256()
    for physical_row, respondent in enumerate(respondents, 1):
        material = {
            "physical_row_ordinal_1based": physical_row,
            "f02_replay_row_ordinal_0based": physical_row - 1,
            "respondent_ref": respondent.ref.as_dict(),
        }
        h.update((canonical_json(material) + "\n").encode("utf-8"))
    return h.hexdigest()


def declared_counts(candidate_kwargs: Mapping[str, Any]) -> dict[str, int]:
    def count(value: Any) -> int:
        return 0 if isinstance(value, TypedAbsence) else len(value)

    return {
        "EmpiricalUniverse": len(candidate_kwargs["empirical_universes"]),
        "RespondentIdentity": len(candidate_kwargs["respondent_identities"]),
        "QuestionVariableBinding": len(candidate_kwargs["question_variable_bindings"]),
        "RespondentEvent": len(candidate_kwargs["respondent_events"]),
        "RoutingEligibilityFact": len(candidate_kwargs["routing_eligibility_facts_or_exact_rules"]),
        "EmpiricalCoordinateFact": len(candidate_kwargs["empirical_coordinate_facts"]),
        "WeightMeasureFact": count(candidate_kwargs["weight_measure_facts_or_typed_absence"]),
        "AuthoritySnapshot": len(candidate_kwargs["authority_snapshots"]),
        "SourceUniverseRelation": count(candidate_kwargs["source_universe_relations_or_explicit_distinct_default"]),
        "EmpiricalPredicateReplayBinding": count(candidate_kwargs["predicate_replay_bindings_when_retained_objects_require_them"]),
        "ComparatorReplayBinding": count(candidate_kwargs["comparator_replay_bindings_or_typed_deferred_state"]),
        "DiscoveryBranchReplayBinding": count(candidate_kwargs["discovery_branch_replay_bindings_or_typed_deferred_state"]),
        "StructuralAdmissionReplayBinding": count(candidate_kwargs["structural_admission_replay_bindings_or_typed_not_applicable_state"]),
        "ReplayManifest": 1,
    }


def build_successor_candidate(
    *,
    base_candidate: C11SourceReleaseCandidate,
    base_projection,
    extension_candidate: C11SourceReleaseCandidate,
    extension_questions: tuple[QuestionVariableBinding, ...],
    extension_routing: tuple[RoutingEligibilityFact, ...],
    all_authorities: tuple[AuthoritySnapshot, ...],
    f02_replay_authority_ref: AuthorityRef,
    f02_module,
) -> C11SourceReleaseCandidate:
    kwargs = {
        "empirical_universes": base_candidate.empirical_universes,
        "respondent_identities": base_candidate.respondent_identities,
        "question_variable_bindings": tuple(sorted(
            (*base_candidate.question_variable_bindings, *extension_questions),
            key=lambda x: x.ref.key,
        )),
        "respondent_events": tuple(sorted(
            (*base_candidate.respondent_events, *extension_candidate.respondent_events),
            key=lambda x: x.ref.key,
        )),
        "routing_eligibility_facts_or_exact_rules": tuple(sorted(
            (*base_candidate.routing_eligibility_facts_or_exact_rules, *extension_routing),
            key=lambda x: x.ref.key,
        )),
        "empirical_coordinate_facts": base_candidate.empirical_coordinate_facts,
        "weight_measure_facts_or_typed_absence": base_candidate.weight_measure_facts_or_typed_absence,
        "authority_snapshots": all_authorities,
        "source_universe_relations_or_explicit_distinct_default": base_candidate.source_universe_relations_or_explicit_distinct_default,
        "predicate_replay_bindings_when_retained_objects_require_them": base_candidate.predicate_replay_bindings_when_retained_objects_require_them,
        "comparator_replay_bindings_or_typed_deferred_state": base_candidate.comparator_replay_bindings_or_typed_deferred_state,
        "discovery_branch_replay_bindings_or_typed_deferred_state": base_candidate.discovery_branch_replay_bindings_or_typed_deferred_state,
        "structural_admission_replay_bindings_or_typed_not_applicable_state": base_candidate.structural_admission_replay_bindings_or_typed_not_applicable_state,
    }
    counts = declared_counts(kwargs)
    manifest = SourceReleaseManifest(
        source_artifact_id=base_candidate.source_release_manifest.source_artifact_id,
        source_artifact_content_hash=SOURCE_SHA256,
        source_family_id=base_candidate.source_release_manifest.source_family_id,
        study_product_id=base_candidate.source_release_manifest.study_product_id,
        release_id=f"LITS1-I02-F02-SUCCESSOR-{SOURCE_SHA256[:16]}-{FROZEN_F02_SCOPE_HASH[:16]}",
        instrument_release_id=base_candidate.source_release_manifest.instrument_release_id,
        ingest_contract_version=base_candidate.source_release_manifest.ingest_contract_version,
        declared_universe_refs=tuple(sorted(
            (x.ref for x in kwargs["empirical_universes"]), key=lambda x: x.key
        )),
        declared_authority_snapshot_refs=tuple(sorted(
            (x.authority_ref for x in all_authorities), key=lambda x: x.key
        )),
        declared_record_counts_by_logical_family=counts,
        source_snapshot_retention_ref=base_candidate.source_release_manifest.source_snapshot_retention_ref,
    )
    candidate = C11SourceReleaseCandidate(
        source_release_manifest=manifest,
        **kwargs,
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=f02_replay_authority_ref,
        deterministic_tie_order_rules_ref=base_projection.tie_order_ref,
        replay_protocol_version=f02_module.CONTRACT_ID,
    )
    candidate = replace(candidate, candidate_replay_manifest=replay)
    if dict(record_counts_for_candidate(candidate)) != counts:
        raise RuntimeError("successor candidate declared counts differ from exact constructed counts")
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    support_blobs = verify_frozen_support()
    base_module = load_module(AS2B, "ee_p2r5b_frozen_as2b")
    f02_module = load_module(F02, "ee_p2r5b_frozen_f02")

    if sha256_file(args.source) != SOURCE_SHA256:
        raise RuntimeError("LiTS-I exact source SHA mismatch")

    incidence = decode_dta(args.source, encoding="latin1")
    if incidence.source_sha256 != SOURCE_SHA256:
        raise RuntimeError("decoder source SHA mismatch")
    if incidence.row_count != SOURCE_ROWS or len(incidence.variables) != SOURCE_VARIABLES:
        raise RuntimeError("decoder source shape mismatch")
    if incidence.reader_configuration.get("authority_status") != COMPATIBILITY_ONLY:
        raise RuntimeError("decoder compatibility status mismatch")
    if incidence.reader_configuration.get("encoding") != "latin1":
        raise RuntimeError("decoder frozen encoding execution configuration mismatch")

    package, ledger, slots = base_module.read_banked_authority()
    base_projection, base_context = base_module.build_projection(incidence, package, ledger, slots)
    if base_projection.cache_identity != ACCEPTED_BASE_PROJECTION_HASH:
        raise RuntimeError("accepted base GovernedC11Projection identity did not reproduce")

    base_names = tuple(
        x.slot.name for x in (
            *base_projection.response_slots,
            *base_projection.coordinate_slots,
            *base_projection.weight_slots,
        )
    )
    base_stream = selected_incidence(incidence, base_names)
    base_candidate = project_c11_candidate_from_physical_cells(
        source_sha256=SOURCE_SHA256,
        row_count=SOURCE_ROWS,
        cells=exact_cells(base_stream, base_module),
        projection=base_projection,
    )
    if base_candidate.candidate_replay_manifest.semantic_projection_hash != ACCEPTED_BASE_CANDIDATE_HASH:
        raise RuntimeError("accepted base candidate semantic projection did not reproduce")
    base_release = validate_c11_source_release(base_candidate)
    if base_release.semantic_release_hash != ACCEPTED_BASE_RELEASE_HASH:
        raise RuntimeError("accepted base I02 release identity did not reproduce")
    if base_release.replay_manifest.content_hash != ACCEPTED_BASE_REPLAY_HASH:
        raise RuntimeError("accepted base ReplayManifest identity did not reproduce")

    closure = f02_module.build_selector_closure()
    if closure["new_release_ref"]["content_hash"] != FROZEN_F02_SCOPE_HASH:
        raise RuntimeError("frozen F02 scope anchor identity mismatch")
    if closure["base_release_ref"]["content_hash"] != ACCEPTED_BASE_RELEASE_HASH:
        raise RuntimeError("frozen F02 base lineage mismatch")

    source_scan = f02_source_scan(incidence, f02_module)

    (
        extension_projection,
        extension_questions,
        extension_routing,
        all_authorities,
        extension_auth_refs,
        extension_projection_material,
    ) = build_extension_projection(
        base_projection=base_projection,
        base_context=base_context,
        slots=slots,
        closure=closure,
        f02_module=f02_module,
    )

    extension_names = ("country", "q310", "q311")
    extension_stream = selected_incidence(incidence, extension_names)
    extension_candidate = project_c11_candidate_from_physical_cells(
        source_sha256=SOURCE_SHA256,
        row_count=SOURCE_ROWS,
        cells=exact_cells(extension_stream, base_module),
        projection=extension_projection,
    )
    if len(extension_candidate.respondent_events) != SOURCE_ROWS * 2:
        raise RuntimeError("q310/q311 extension event cardinality mismatch")
    if len(extension_routing) != SOURCE_ROWS * 2:
        raise RuntimeError("q310/q311 extension routing cardinality mismatch")

    successor_candidate = build_successor_candidate(
        base_candidate=base_candidate,
        base_projection=base_projection,
        extension_candidate=extension_candidate,
        extension_questions=extension_questions,
        extension_routing=extension_routing,
        all_authorities=all_authorities,
        f02_replay_authority_ref=extension_auth_refs["replay"],
        f02_module=f02_module,
    )

    repository = C11Repository()
    ingest = ingest_c11_source_release(successor_candidate, repository)
    if not ingest.accepted or ingest.release_ref is None:
        raise RuntimeError(f"I02 successor ingest rejected: {ingest.disposition}: {ingest.errors}")
    resolved = repository.resolve_release_exact(ingest.release_ref)
    if resolved.release_ref != ingest.release_ref:
        raise RuntimeError("C11Repository exact release resolution mismatch")
    if ingest.semantic_release_hash != ingest.release_ref.content_hash:
        raise RuntimeError("I02 returned release ref/hash mismatch")

    coverage = {k: list(v) for k, v in ingest.m01_m18_coverage.items()}
    if tuple(sorted(coverage)) != tuple(sorted(M01_M18)):
        raise RuntimeError("M01-M18 exact coverage key set mismatch")
    if any(not coverage[key] for key in M01_M18):
        raise RuntimeError("M01-M18 contains an unclosed empty item")

    selector_refs = {
        selector_id: item["predicate_ref"]
        for selector_id, item in sorted(closure["selectors"].items())
    }
    f02_questions = {
        q: {
            "question_ref": closure["questions"][q]["question_ref"],
            "response_slot_ref": closure["questions"][q]["slot_ref"],
            "routing_ref": closure["questions"][q]["routing_ref"],
            "response_value_state_refs": closure["questions"][q]["value_state_refs"],
        }
        for q in ("q310", "q311")
    }
    f02_authority_refs = {
        name: closure["authorities"]["refs"][name]
        for name in ("source_semantics", "routing", "predicate_grammar", "replay")
    }

    extension_scan_path = args.output_dir / "successor_release_extension_scan.json"
    replay_path = args.output_dir / "successor_release_replay_manifest.json"
    coverage_path = args.output_dir / "successor_release_m01_m18.json"
    receipt_path = args.output_dir / "successor_release_receipt.json"

    extension_scan_receipt = {
        "schema": "EE_P2R5B_F02_EXTENSION_SOURCE_REPLAY@1.0.0",
        "source_sha256": SOURCE_SHA256,
        "row_coordinate_relation": {
            "i02_physical_row": "ONE_BASED",
            "f02_replay_row": "ZERO_BASED",
            "exact_relation": "f02_row = i02_physical_row - 1",
            "row_alignment_root_sha256": row_alignment_root(base_projection.respondents),
        },
        "source_scan": source_scan,
        "extension_event_ref_root_sha256": ref_root(extension_candidate.respondent_events),
        "extension_routing_ref_root_sha256": ref_root(extension_routing),
        "extension_event_count": len(extension_candidate.respondent_events),
        "extension_routing_count": len(extension_routing),
        "f02_questions": f02_questions,
        "selector_refs": selector_refs,
        "authority_refs": f02_authority_refs,
        "negative_ceiling": f02_module.NEGATIVE_CEILING,
    }
    write_json(extension_scan_path, extension_scan_receipt)
    write_json(replay_path, resolved.replay_manifest.as_dict())
    write_json(coverage_path, coverage)

    receipt = {
        "schema": "EE_P2R5B_SUCCESSOR_RELEASE_RECEIPT@1.0.0",
        "status": "PASS",
        "terminal": PASS_TERMINAL,
        "contract": CONTRACT,
        "source": {
            "name": SOURCE_NAME,
            "sha256": SOURCE_SHA256,
            "rows": incidence.row_count,
            "variables": len(incidence.variables),
            "format": incidence.source_format,
            "decoder_call": 'decode_dta(source_path, encoding="latin1")',
            "decoder_compatibility_status": incidence.reader_configuration.get("authority_status"),
        },
        "frozen_support_git_blobs": support_blobs,
        "accepted_base_replay": {
            "projection_hash": base_projection.cache_identity,
            "candidate_projection_hash": base_candidate.candidate_replay_manifest.semantic_projection_hash,
            "release_ref": base_release.release_ref.as_dict(),
            "semantic_release_hash": base_release.semantic_release_hash,
            "replay_manifest_ref": base_release.replay_manifest.ref.as_dict(),
            "replay_manifest_hash": base_release.replay_manifest.content_hash,
            "reproduced_exactly": True,
        },
        "frozen_f02_scope_anchor": {
            "ref": closure["new_release_ref"],
            "content_hash": FROZEN_F02_SCOPE_HASH,
            "role_claimed_here": "FROZEN_F02_SEMANTIC_SCOPE_AND_PROVENANCE_ANCHOR_ONLY",
            "accepted_i02_release_claimed": False,
        },
        "extension": {
            "projection_material": extension_projection_material,
            "question_and_member_refs": f02_questions,
            "authority_refs": f02_authority_refs,
            "selector_refs": selector_refs,
            "source_scan_receipt_file": extension_scan_path.name,
            "source_scan_receipt_sha256": sha256_file(extension_scan_path),
            "question_binding_refs": {
                binding.native_question_ref.object_id: binding.ref.as_dict()
                for binding in extension_questions
            },
            "event_count": len(extension_candidate.respondent_events),
            "routing_count": len(extension_routing),
        },
        "accepted_i02_successor": {
            "ingest_contract": successor_candidate.source_release_manifest.ingest_contract_version,
            "ingest_disposition": ingest.disposition.value,
            "accepted": ingest.accepted,
            "source_release_manifest": successor_candidate.source_release_manifest.semantic_projection(),
            "source_release_manifest_hash": successor_candidate.source_release_manifest.content_hash,
            "candidate_projection_hash": successor_candidate.candidate_replay_manifest.semantic_projection_hash,
            "release_ref": ingest.release_ref.as_dict(),
            "semantic_release_hash": ingest.semantic_release_hash,
            "replay_manifest_ref": ingest.replay_manifest_ref.as_dict(),
            "replay_manifest_file": replay_path.name,
            "replay_manifest_file_sha256": sha256_file(replay_path),
            "m01_m18_file": coverage_path.name,
            "m01_m18_file_sha256": sha256_file(coverage_path),
            "m01_m18_coverage": coverage,
            "record_counts": dict(record_counts_for_candidate(successor_candidate)),
            "repository_release_count": len(repository),
            "repository_snapshot_identity": repository.snapshot_identity(),
            "resolve_release_exact": "PASS",
        },
        "r5a_boundary": {
            "realization_authority_claimed": False,
            "scope_anchor_runtime_release_equality_claimed": False,
            "release_alias_claimed": False,
            "realization_binding_emitted": False,
            "facts_emitted_for_future_binding_only": True,
            "frozen_scope_anchor": closure["new_release_ref"],
            "actual_accepted_i02_runtime_release_ref": ingest.release_ref.as_dict(),
            "exact_source_sha256": SOURCE_SHA256,
            "extension_member_identities": f02_questions,
            "authority_identities": f02_authority_refs,
            "replay_manifest_ref": ingest.replay_manifest_ref.as_dict(),
            "m01_m18_closed": True,
        },
        "forbidden_modifications_observed": {
            "selector_remint": False,
            "d02_f02_workload_mutation": False,
            "source_semantic_widening": False,
            "future_release_hash_hardcoded": False,
            "r5a_authority_issued": False,
            "production_mixed_i05_changed": False,
        },
    }
    write_json(receipt_path, receipt)
    print(json.dumps({
        "status": "PASS",
        "receipt": str(receipt_path),
        "accepted_i02_runtime_release_ref": ingest.release_ref.as_dict(),
        "replay_manifest_ref": ingest.replay_manifest_ref.as_dict(),
        "terminal": PASS_TERMINAL,
        "r5a_realization_authority_claimed": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
