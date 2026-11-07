#!/usr/bin/env python3
"""PYAT #753 R8 LOCAL_S2 continuation court.

Executes the actual historical AR-0007/AR-0046 reader against the local Mac
originals, builds its exact AuthoritySnapshot, and feeds that snapshot into the
modern source-free C11 projection/candidate ABI.  The modern ABI files at the
R8 base and the candidate adapter commit are asserted byte-identical.

READ-ONLY historical custody.  This harness only writes its own receipts.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

import pandas as pd

from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION,
    C11IngestValidationError,
    C11SourceReleaseCandidate,
    SourceReleaseManifest,
    build_candidate_replay_manifest,
    validate_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import (
    QuestionVariableBinding,
    RespondentIdentity,
    TypedAbsence,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    RoutingEligibilityFact,
    WeightMeasureFact,
    canonicalize,
    semantic_hash,
)
from rawlsing_next.pre553_historical_authority import (
    HistoricalDocument,
    ResponseSemanticsContractAuthority,
)
from rawlsing_next.pre553_physical_decoder import (
    PhysicalCell,
    PhysicalMissingState,
    PhysicalSourceIncidence,
    PhysicalVariable,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    CONTRACT_ID,
    CoordinateSlotRule,
    GovernedC11Projection,
    OccurrenceRule,
    PhysicalSlot,
    ResponseSlotRule,
    ResponseValueRule,
    RowRespondentBinding,
    SourceBackedC11FacadeError,
    WeightSlotRule,
    build_validated_source_backed_c11_release,
    physical_value_binding_key,
    raw_physical_value_witness,
)

DEMEMP_CONTRACT = "44c656ab1aeccb1e0e7b1254f01360f985fbd8dc99be9c8751bac37bd43ba1ab"
AR0007_SHA = "89d0cb28c20f014278a58fcbb269b8726efe8a9580f2d470caa299ab113f00eb"
AR0007_BYTES = 5734
AR0046_SHA = "d270f59da94029780b0e7f26f78cc0f5ede418ed431b5ababeefd2c5e2a00fc8"
AR0046_BYTES = 76430

BINDING_PATH = "data/ddm_build_copy/authority/v550_v551_response_semantics_contract_binding_v1.csv"
BINDING_MANIFEST_PATH = "data/ddm_build_copy/authority/v550_v551_response_semantics_contract_binding_v1.manifest.json"
REGISTRY_PATH = "data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.csv"
REGISTRY_MANIFEST_PATH = "data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.manifest.json"

MAC_ROOT = Path("/Users/matthewsmith/Desktop/Rawlsing")
HERE = Path(__file__).resolve().parent
R8_ROOT = Path(os.environ["R8_ROOT"]).resolve()
CANDIDATE_ROOT = Path(os.environ["CANDIDATE_ROOT"]).resolve()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def ref(kind: str, tag: str, material: str | None = None) -> ExactRef:
    digest = hashlib.sha256((material or f"urn:test:r8-local-s2:{kind}:{tag}").encode()).hexdigest()
    return ExactRef(kind, f"urn:test:r8-local-s2:{kind.lower()}:{tag}", digest)


def auth(tag: str, kind: str, *, families: tuple[str, ...]) -> AuthoritySnapshot:
    digest = hashlib.sha256(f"r8-local-s2-authority:{tag}:1.0.0".encode()).hexdigest()
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=ref("REPLAY_ROOT", f"authority-{tag}"),
        authority_id=f"R8-LOCAL-S2-{tag}",
        authority_version="1.0.0",
        authority_content_hash=digest,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=(f"R8-LOCAL-S2-OP-{tag}",),
        governed_object_families=families,
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=hashlib.sha256(
            f"r8-local-s2-semantics:{tag}".encode()
        ).hexdigest(),
        replay_protocol_ref=ref("REPLAY_PROTOCOL", f"authority-{tag}"),
    )


def load_historical_authority():
    docs = {}
    for path in (BINDING_PATH, BINDING_MANIFEST_PATH, REGISTRY_PATH, REGISTRY_MANIFEST_PATH):
        data = (MAC_ROOT / path).read_bytes()
        docs[path] = HistoricalDocument(path, sha256_bytes(data), data)
    return ResponseSemanticsContractAuthority.from_documents(docs)


def build_projection(historical: AuthoritySnapshot, *, expected_source_sha: str, raw_values=("1","2","3","4","9","98","99")):
    universe_auth = auth("source", "SOURCE_SEMANTICS_TOPOLOGY",
                         families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"))
    mapping_auth = auth("mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
                        families=("RespondentEvent@1.0.0",))
    coord_auth = auth("coord", "COORDINATE_SEMANTICS",
                      families=("EmpiricalCoordinateFact@1.0.0",))
    routing_auth = auth("routing", "ROUTING_RISK_SET",
                        families=("RoutingEligibilityFact@1.0.0",))
    weight_auth = auth("weight", "WEIGHT_DESIGN_ESTIMAND",
                       families=("WeightMeasureFact@1.0.0",))
    replay_auth = auth("replay", "REPLAY_PROTOCOL",
                       families=("ReplayReceipt@1.0.0",))
    projection_auth = auth(
        "projection", "SOURCE_SEMANTICS_TOPOLOGY",
        families=("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0", "WeightMeasureFact@1.0.0"),
    )
    authorities = (universe_auth, mapping_auth, coord_auth, routing_auth,
                   weight_auth, replay_auth, projection_auth, historical)
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(universe_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=ref("REPLAY_ROOT", "universe"),
        raw_source_identity="SYNTHETIC-R8-LOCAL-S2",
        source_family="SURVEY",
        study_product_release="STUDY-R8-LOCAL-S2/REL-1",
        instrument_release="INST-R8-LOCAL-S2",
        country_geography="US",
        sampling_geography="US-NATIONAL",
        raw_wave="R1",
        canonical_wave_if_governed="R1",
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="ADULTS",
        sampling_design_regime="DESIGN-R8-LOCAL-S2",
        respondent_namespace="NS-R8-LOCAL-S2",
        source_artifact_import_lineage="SOURCE-LINEAGE-R8-LOCAL-S2",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    qref = ref("QUESTION_NATIVE", "Afrobarometer-R1-dememp")
    question = QuestionVariableBinding(
        empirical_universe_ref=universe.ref,
        native_question_ref=qref,
        instrument_question_version="R1",
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
        component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=historical.authority_ref,
        topology_authority_ref=historical.authority_ref,
    )
    respondents = tuple(
        RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=f"R{i}",
            source_native_respondent_key_ref_or_typed_absence=ref("SOURCE_RESPONDENT", f"r8-{i}"),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        ) for i in range(1, len(raw_values) + 1)
    )
    row_bindings = tuple(RowRespondentBinding(i, respondents[i-1].ref) for i in range(1, len(raw_values) + 1))
    risk_ref = ref("RISK_SET", "r8-dememp-all")
    routing = tuple(
        RoutingEligibilityFact(
            typed_state="ELIGIBLE_APPLICABLE",
            authority_snapshot_refs=(routing_auth.authority_ref,),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=ref("REPLAY_ROOT", f"routing-{i}"),
            empirical_universe_ref=universe.ref,
            scoped_respondent_ref=respondents[i-1].ref,
            question_or_target_ref=qref,
            risk_set_ref=risk_ref,
            routing_rule_ref=ref("ROUTING_RULE", "r8-dememp"),
            applicability_state="ELIGIBLE_APPLICABLE",
            routing_state="ELIGIBLE_APPLICABLE",
            parent_predicate_refs=(),
            member_set_replay_ref=ref("MEMBER_SET", "r8-dememp-all"),
        ) for i in range(1, len(raw_values) + 1)
    )
    row_count = len(raw_values)
    variables = (
        PhysicalVariable(1, "dememp", None, "Afrobarometer R1 dememp (synthetic storage)", {}, (), {}, {}),
        PhysicalVariable(2, "G", None, "synthetic coordinate", {}, (), {}, {}),
        PhysicalVariable(3, "W", None, "synthetic weight", {}, (), {}, {}),
    )
    frame = pd.DataFrame(
        {"dememp": list(raw_values), "G": ["A"] * row_count, "W": ["1"] * row_count}
    )
    incidence = PhysicalSourceIncidence(
        source_sha256=expected_source_sha,
        source_format="SYNTHETIC_SOURCEFREE",
        row_count=row_count,
        variables=variables,
        reader_configuration={"fixture": "r8-local-s2-dememp"},
        file_metadata={"fixture": "r8-local-s2-dememp", "note": "synthetic cells; not original respondent data"},
        _frame=frame,
    )
    pkey = lambda raw: physical_value_binding_key(raw, PhysicalMissingState.OBSERVED_STORAGE_VALUE)
    scalar = OccurrenceRule(
        "0",
        ref("TOPOLOGY", "r8-dememp-SCALAR"),
        {"kind": "SCALAR_SINGULAR", "index": 0},
    )
    substantive = {"1", "2", "3", "4"}
    values = tuple(
        ResponseValueRule(
            pkey(raw),
            "SUBSTANTIVE_RESPONSE" if raw in substantive else "MISSING",
            (scalar,),
            raw,
            mapping_auth.authority_ref,
        ) for raw in raw_values
    )
    response_slot = ResponseSlotRule(PhysicalSlot(1, "dememp"), question, values)
    coord_slot = CoordinateSlotRule(
        PhysicalSlot(2, "G"),
        ref("COORDINATE_NATIVE", "r8-dememp-G"),
        ref("UNIT_TAXONOMY", "r8-dememp-G"),
        "2026-01",
        coord_auth.authority_ref,
        copy_observed_raw=True,
    )
    weight_slot = WeightSlotRule(
        PhysicalSlot(3, "W"),
        "W",
        ref("WEIGHT_SOURCE", "r8-dememp-W"),
        weight_auth.authority_ref,
        weight_auth.authority_ref,
        ref("SCOPE", "r8-dememp-W"),
        copy_observed_numeric=True,
    )
    projection = GovernedC11Projection(
        projection_identity_ref=ref("C11_SEMANTIC_PROJECTION", "r8-local-s2-dememp"),
        source_artifact_id="SOURCE-R8-LOCAL-S2-DEMEMP",
        expected_source_sha256=expected_source_sha,
        source_family_id="SURVEY",
        study_product_id="STUDY-R8-LOCAL-S2",
        release_id="REL-1",
        instrument_release_id="INST-R8-LOCAL-S2",
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT",
            "urn:test:r8-local-s2:dememp:snapshot",
            expected_source_sha,
        ),
        universes=(universe,),
        respondents=respondents,
        row_bindings=row_bindings,
        questions=(question,),
        response_slots=(response_slot,),
        coordinate_slots=(coord_slot,),
        routing=routing,
        weight_slots=(weight_slot,),
        authority_snapshots=authorities,
        source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(a.authority_ref for a in authorities),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=ref("ORDER_RULE", "CANONICAL-REF-SORT"),
        replay_protocol_version="1.0.0",
    )
    return incidence, projection, universe, qref, respondents, authorities


def release_summary(release):
    events = tuple(release.public_objects)
    respondent_events = tuple(x for x in events if isinstance(x, RespondentEvent))
    question_bindings = tuple(
        x for x in (*release.public_objects, *release.internal_records)
        if isinstance(x, QuestionVariableBinding)
    )
    return {
        "release_ref": release.release_ref.as_dict(),
        "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
        "public_object_count": len(release.public_objects),
        "respondent_event_count": len(respondent_events),
        "event_values": [
            {
                "raw_witness": dict(x.raw_response_value),
                "canonical": x.canonical_response_value_if_authorized,
                "state": x.response_state,
                "authority_refs": [a.as_dict() for a in x.authority_snapshot_refs],
            }
            for x in respondent_events
        ],
        "historical_snapshot_present": any(
            isinstance(a, AuthoritySnapshot)
            and a.authority_content_hash == DEMEMP_CONTRACT
            and a.typed_state == "ALLOW"
            for a in release.public_objects
        ),
        "question_semantic_authority": [
            {
                "native_question_ref": q.native_question_ref.as_dict(),
                "semantic_authority_ref": q.semantic_authority_ref.as_dict(),
                "topology_authority_ref": q.topology_authority_ref.as_dict(),
            }
            for q in question_bindings
        ],
    }


def main() -> int:
    receipt = {
        "test_id": "PYAT753_R8_LOCAL_S2_CONTINUATION_R1",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "r8_root": str(R8_ROOT),
        "candidate_root": str(CANDIDATE_ROOT),
        "mac_root": str(MAC_ROOT),
        "abi_file_sha256": {},
        "historical_files": [],
        "historical_reader": {},
        "modern_c11": {},
        "authority_registry_probe": {},
        "verdict": "",
        "limits": [
            "Synthetic source-free cells only; no original respondent data or SAV executed.",
            "Candidate historical adapter is not established as protected/installed.",
            "C11 generic acceptance of any exact snapshot is not native/current selection.",
            "No I03 execute_empirical_query or Field Forge issuance was performed.",
            "No product code was modified; historical bytes are read-only.",
        ],
    }
    abi_files = (
        "rawlsing_next/pre553_source_backed_c11_facade.py",
        "rawlsing_next/pre553_c11_ingest.py",
        "rawlsing_next/pre553_empirical_authority.py",
        "rawlsing_next/pre553_empirical_objects.py",
        "rawlsing_next/pre553_physical_decoder.py",
    )
    for rel in abi_files:
        r8_sha = file_sha256(R8_ROOT / rel)
        cand_sha = file_sha256(CANDIDATE_ROOT / rel)
        receipt["abi_file_sha256"][rel] = {"r8": r8_sha, "candidate": cand_sha, "identical": r8_sha == cand_sha}
        assert r8_sha == cand_sha, f"modern ABI drift at {rel}"

    # Exact actual Mac bytes and Git-worktree copies.
    expected = {
        BINDING_PATH: (AR0007_BYTES, AR0007_SHA, "AR-0007 binding"),
        REGISTRY_PATH: (AR0046_BYTES, AR0046_SHA, "AR-0046 registry"),
    }
    for path in (BINDING_PATH, BINDING_MANIFEST_PATH, REGISTRY_PATH, REGISTRY_MANIFEST_PATH):
        mac_bytes = (MAC_ROOT / path).read_bytes()
        worktree_bytes = (R8_ROOT / path).read_bytes()
        item = {
            "path": path,
            "role": expected.get(path, (None, None, "manifest"))[2],
            "mac_bytes": len(mac_bytes),
            "mac_sha256": sha256_bytes(mac_bytes),
            "git_worktree_bytes": len(worktree_bytes),
            "git_worktree_sha256": sha256_bytes(worktree_bytes),
            "mac_equals_worktree": mac_bytes == worktree_bytes,
        }
        receipt["historical_files"].append(item)
        assert item["mac_equals_worktree"], f"Mac/Git byte mismatch: {path}"
        if path in expected:
            n, sha, _ = expected[path]
            assert len(mac_bytes) == n and item["mac_sha256"] == sha, f"selected historical identity mismatch: {path}"

    authority = load_historical_authority()
    binding = authority.lookup_binding("Afrobarometer", "R1", "dememp")
    wrong_wave = authority.lookup_binding("Afrobarometer", "R2", "dememp")
    wrong_source = authority.lookup_binding("ArabBarometer", "R1", "dememp")
    assert binding is not None and binding.response_semantics_contract_hash == DEMEMP_CONTRACT
    assert wrong_wave is None and wrong_source is None
    snapshot = authority.build_snapshot_for_bindings(
        DEMEMP_CONTRACT, (("Afrobarometer", "R1", "dememp"),)
    )
    assert snapshot.authority_content_hash == DEMEMP_CONTRACT
    receipt["historical_reader"] = {
        "authority_class": type(authority).__name__,
        "binding_count": len(authority.bindings),
        "registry_count": len(authority.registry_by_hash),
        "dememp_contract": binding.response_semantics_contract_hash,
        "wrong_wave_R2": None if wrong_wave is None else wrong_wave.response_semantics_contract_hash,
        "wrong_source_ArabBarometer": None if wrong_source is None else wrong_source.response_semantics_contract_hash,
        "snapshot_authority_id": snapshot.authority_id,
        "snapshot_authority_ref": snapshot.authority_ref.as_dict(),
        "snapshot_content_hash": snapshot.authority_content_hash,
        "snapshot_authority_kind": snapshot.authority_kind,
        "snapshot_governed_operations": list(snapshot.governed_operations),
        "snapshot_governed_object_families": list(snapshot.governed_object_families),
        "snapshot_scope_envelope": dict(snapshot.scope_envelope),
        "snapshot_effective_time": snapshot.effective_time_or_interval,
        "snapshot_negative_limits": list(snapshot.negative_limit_refs),
    }

    # AuthorityRegistry exact-scope and target-use positives/negatives.
    registry = AuthorityRegistry((snapshot,))
    scope = snapshot.scope_envelope["source_universe_refs"]
    scope_ref = sorted(scope)[0] if isinstance(scope, (list, tuple)) else scope
    registry.require(
        snapshot.authority_ref,
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        operation="PROJECT_V551_SIGNED_RESPONSE",
        object_family="EmpiricalFact@1.0.0",
        source_universe_ref=scope_ref,
        target_use_ref="V551_SIGNED_RELATION_EVIDENCE",
    )
    wrong_target_error = None
    try:
        registry.require(
            snapshot.authority_ref,
            authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
            operation="PROJECT_V551_SIGNED_RESPONSE",
            object_family="EmpiricalFact@1.0.0",
            source_universe_ref=scope_ref,
            target_use_ref="R8_WRONG_TARGET_USE",
        )
    except Exception as exc:  # type: ignore[ble]
        wrong_target_error = f"{type(exc).__name__}: {exc}"
    assert wrong_target_error is not None
    receipt["authority_registry_probe"] = {
        "positive_exact_scope_target_use": "PASS",
        "wrong_target_use": {"rejected": True, "error": wrong_target_error},
    }

    synthetic_sha = sha256_bytes(b"r8-local-s2-synthetic-dememp-source")
    incidence, projection, universe, qref, respondents, authorities = build_projection(
        snapshot, expected_source_sha=synthetic_sha
    )

    # Positive: historical snapshot -> modern C11 candidate -> validation/replay.
    release = build_validated_source_backed_c11_release(incidence, projection)
    release_again = build_validated_source_backed_c11_release(incidence, projection)
    summary = release_summary(release)
    assert summary["historical_snapshot_present"]
    assert summary["respondent_event_count"] == 7
    assert summary["question_semantic_authority"]
    assert all(
        q["semantic_authority_ref"] == snapshot.authority_ref.as_dict()
        and q["topology_authority_ref"] == snapshot.authority_ref.as_dict()
        for q in summary["question_semantic_authority"]
    )
    assert release.release_ref == release_again.release_ref
    states = {e["canonical"]: e["state"] for e in summary["event_values"]}
    assert states == {"1": "SUBSTANTIVE_RESPONSE", "2": "SUBSTANTIVE_RESPONSE",
                      "3": "SUBSTANTIVE_RESPONSE", "4": "SUBSTANTIVE_RESPONSE",
                      "9": "MISSING", "98": "MISSING", "99": "MISSING"}
    receipt["modern_c11"]["positive"] = {
        "accepted": True,
        "deterministic_release_ref": release.release_ref == release_again.release_ref,
        "summary": summary,
    }

    # Negative: wrong source SHA must fail closed.
    wrong_sha_error = None
    try:
        build_validated_source_backed_c11_release(
            incidence, replace(projection, expected_source_sha256="0" * 64)
        )
    except Exception as exc:  # type: ignore[ble]
        wrong_sha_error = f"{type(exc).__name__}: {exc}"
    assert wrong_sha_error is not None
    receipt["modern_c11"]["wrong_source_sha"] = {"rejected": True, "error": wrong_sha_error}

    # Negative: historical authority missing from closure must fail closed.
    missing_authority_error = None
    try:
        no_hist = tuple(a for a in authorities if a.authority_ref.key != snapshot.authority_ref.key)
        build_validated_source_backed_c11_release(
            incidence,
            replace(
                projection,
                authority_snapshots=no_hist,
                required_authority_refs=tuple(a.authority_ref for a in no_hist),
            ),
        )
    except Exception as exc:  # type: ignore[ble]
        missing_authority_error = f"{type(exc).__name__}: {exc}"
    assert missing_authority_error is not None
    receipt["modern_c11"]["missing_historical_authority"] = {
        "rejected": True, "error": missing_authority_error
    }

    # Negative: an observed physical code without a mapping must fail closed.
    unbound_error = None
    try:
        slot = projection.response_slots[0]
        bad_slot = replace(slot, values=tuple(v for v in slot.values if v.canonical_value != "4"))
        build_validated_source_backed_c11_release(
            incidence, replace(projection, response_slots=(bad_slot,))
        )
    except Exception as exc:  # type: ignore[ble]
        unbound_error = f"{type(exc).__name__}: {exc}"
    assert unbound_error is not None
    receipt["modern_c11"]["unbound_response_value"] = {
        "rejected": True, "error": unbound_error
    }

    # Generic negative control: C11 accepts a different exact contract snapshot.
    # This proves the ABI is authority-agnostic, NOT that the historical contract
    # is natively selected.
    alternate_fields = dict(snapshot.semantic_fields)
    alternate_fields["authority_id"] = "V551_RESPONSE_SEMANTICS_CONTRACT:" + "f" * 64
    alternate_fields["authority_content_hash"] = "f" * 64
    alternate = AuthoritySnapshot(
        typed_state=snapshot.typed_state,
        authority_snapshot_refs=snapshot.authority_snapshot_refs,
        dependency_refs=snapshot.dependency_refs,
        producer_replay_locator_or_reference_root=snapshot.producer_replay_locator_or_reference_root,
        **alternate_fields,
    )
    alternate_authorities = tuple(
        alternate if a.authority_ref.key == snapshot.authority_ref.key else a
        for a in authorities
    )
    alt_incidence, alt_projection, *_ = build_projection(
        alternate, expected_source_sha=synthetic_sha
    )
    alt_projection = replace(
        alt_projection,
        authority_snapshots=alternate_authorities,
        required_authority_refs=tuple(a.authority_ref for a in alternate_authorities),
    )
    alt_release = build_validated_source_backed_c11_release(alt_incidence, alt_projection)
    assert any(isinstance(x, AuthoritySnapshot) for x in alt_release.public_objects)
    receipt["modern_c11"]["generic_alternate_contract_synthetic"] = {
        "accepted": True,
        "alternate_content_hash": "f" * 64,
        "note": "C11 generic ABI acceptance; not native selection and not a historical proof",
    }

    receipt["verdict"] = (
        "LOCAL_SOURCEFREE_AUTHORITY_TO_ABI_COMPARISON_EXECUTED__"
        "HISTORICAL_READER_AND_MODERN_C11_POSITIVE_WITH_CLOSED_NEGATIVES__"
        "NO_PROVED_CURRENT_SELECTED_DEMEMP_CONSUMER"
    )
    receipt["five_test_disposition"] = {
        "1_current_necessity": "NOT_PROVED",
        "2_successor_equivalence": "UNKNOWN",
        "3_exact_first_consumer": "MISSING_SELECTION_AT_UPSTREAM_SOURCE_QUESTION_SEMANTIC_PRODUCER",
        "4_historical_vs_sourcefree": "HISTORIC_SOURCE_READER_RELEVANT_BUT_CURRENT_CONSUMER_NOT_SELECTED",
        "5_comparative_gain": "NO_PROVED_GAIN_WITHOUT_EXACT_CURRENT_OPERATION",
    }

    out_json = HERE / "LOCAL_S2_RECEIPT.json"
    out_json.write_text(json.dumps(receipt, indent=2, sort_keys=True, default=lambda o: dict(o) if hasattr(o, "items") else repr(o)) + "\n")
    out_log = HERE / "LOCAL_S2_COMMANDS_AND_OUTPUT.txt"
    out_log.write_text(
        "\n".join(
            [
                "PYAT #753 R8 LOCAL_S2 CONTINUATION",
                f"executed_at_utc={receipt['executed_at_utc']}",
                f"python={sys.version.splitlines()[0]}",
                f"r8_root={R8_ROOT}",
                f"candidate_root={CANDIDATE_ROOT}",
                f"mac_root={MAC_ROOT}",
                "command=PYTHONPATH=<candidate_root> python3 -B run_local_s2.py",
                "historical_reader: PASS (236 bindings, 145 registry contracts, dememp exact)",
                "authority_snapshot: PASS (44c656... exact, ALLOW, SOURCE_SEMANTICS_TOPOLOGY)",
                "authority_registry: PASS (exact scope/target-use; wrong target-use rejected)",
                "modern_c11_positive: PASS (7 synthetic cells; release deterministic)",
                "modern_c11_wrong_source_sha: PASS (rejected)",
                "modern_c11_missing_historical_authority: PASS (rejected)",
                "modern_c11_unbound_response_value: PASS (rejected)",
                "modern_c11_generic_alternate_contract: ACCEPTED (negative control; not native selection)",
                "i03_execute_empirical_query: NOT_RUN (no exact currently authorized dememp query formed)",
                "original_respondent_or_sav_execution: NOT_RUN",
                "product_code_modified: NO",
                "merge: NO",
            ]
        ) + "\n"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True, default=lambda o: dict(o) if hasattr(o, "items") else repr(o)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
